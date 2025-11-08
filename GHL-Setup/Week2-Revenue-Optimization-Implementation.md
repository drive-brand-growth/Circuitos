# Week 2: Revenue Optimization Implementation - CircuitOS

## 📈 DRIVE REVENUE GROWTH - HIGH ROI SYSTEMS

**Focus:** A/B Testing, ROI Attribution, Lead Quality Feedback, Dashboards
**Expected Lift:** +20-35% reply rates, provable ROI, +8-10% LPR accuracy
**Implementation Time:** ~24 hours

---

## System 1: A/B Testing Infrastructure

### Expected Impact: +20-35% Reply Rates

**Current State:** Email Campaign Manager generates 3 variants (A/B/C) but NO tracking of winners
**Goal:** Automatically test, measure, and scale winning variants

---

### Part 1: Supabase Schema

```sql
-- Email A/B Test Tracking
CREATE TABLE email_ab_tests (
   id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
   campaign_id VARCHAR(255) NOT NULL,
   variant VARCHAR(1) NOT NULL, -- 'A', 'B', or 'C'
   subject_line TEXT,
   email_body TEXT,
   tone VARCHAR(50), -- 'professional', 'casual', 'urgent'
   sends INT DEFAULT 0,
   opens INT DEFAULT 0,
   replies INT DEFAULT 0,
   conversions INT DEFAULT 0,
   open_rate DECIMAL(5,2),
   reply_rate DECIMAL(5,2),
   conversion_rate DECIMAL(5,2),
   statistical_confidence DECIMAL(5,2), -- 0-100%
   is_winner BOOLEAN DEFAULT false,
   test_started_at TIMESTAMP,
   test_ended_at TIMESTAMP,
   winner_declared_at TIMESTAMP,
   created_at TIMESTAMP DEFAULT NOW()
);

-- Track which variant each contact received
CREATE TABLE contact_email_variants (
   id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
   contact_id VARCHAR(255) NOT NULL,
   campaign_id VARCHAR(255) NOT NULL,
   variant VARCHAR(1) NOT NULL,
   sent_at TIMESTAMP DEFAULT NOW(),
   opened_at TIMESTAMP,
   replied_at TIMESTAMP,
   converted_at TIMESTAMP,
   UNIQUE(contact_id, campaign_id)
);

-- Indexes
CREATE INDEX idx_ab_tests_campaign ON email_ab_tests(campaign_id);
CREATE INDEX idx_ab_tests_winner ON email_ab_tests(is_winner);
CREATE INDEX idx_contact_variants_campaign ON contact_email_variants(campaign_id, variant);
```

---

### Part 2: GHL Custom Fields

Add to Contact:
```
- email_variant_sent: Dropdown ('A', 'B', 'C')
- campaign_id: Text (UUID of current campaign)
- ab_test_group: Text (for segmentation)
```

---

### Part 3: GHL Workflow - Send A/B Test Variants

**Workflow:** "Email Campaign - A/B Test"

**Trigger:** Contact tagged "High Intent"

**Step 1: Randomly Assign Variant**
```javascript
// Use modulo to split evenly into 3 groups
const variant = ['A', 'B', 'C'][Math.floor(Math.random() * 3)];

Update Contact:
   - email_variant_sent = variant
   - campaign_id = "{{campaign.id}}"
```

**Step 2: Call Email Campaign Manager (with variant parameter)**
```javascript
POST to: https://your-vercel.com/api/ai-employees/email-campaign-manager
Body: {
   "contact": {{contact}},
   "business": {{business}},
   "campaign_id": "{{campaign.id}}",
   "variant_to_generate": "{{contact.email_variant_sent}}", // Force specific variant
   "tone": {
      "A": "professional",
      "B": "casual",
      "C": "urgent"
   }["{{contact.email_variant_sent}}"]
}
```

**Step 3: Send Email via Instantly.ai**
```
Send email with subject/body from chosen variant

Track send:
POST to Supabase:
INSERT INTO email_ab_tests (campaign_id, variant, sends)
VALUES ('{{campaign.id}}', '{{variant}}', 1)
ON CONFLICT (campaign_id, variant) DO UPDATE SET sends = sends + 1;

INSERT INTO contact_email_variants (contact_id, campaign_id, variant, sent_at)
VALUES ('{{contact.id}}', '{{campaign.id}}', '{{variant}}', NOW());
```

---

### Part 4: GHL Workflow - Track Email Engagement

**Workflow:** "Track A/B Test Engagement"

**Trigger 1: Email Opened**
```
Lookup: contact_email_variants WHERE contact_id = {{contact.id}}
Get: campaign_id, variant

Update Supabase:
1. UPDATE email_ab_tests SET opens = opens + 1 WHERE campaign_id = X AND variant = Y
2. UPDATE contact_email_variants SET opened_at = NOW() WHERE contact_id = {{contact.id}}

Calculate new open_rate = (opens / sends) * 100
```

**Trigger 2: Email Replied**
```
Update Supabase:
1. UPDATE email_ab_tests SET replies = replies + 1
2. UPDATE contact_email_variants SET replied_at = NOW()

Calculate new reply_rate = (replies / sends) * 100
```

**Trigger 3: Deal Closed Won**
```
Update Supabase:
1. UPDATE email_ab_tests SET conversions = conversions + 1
2. UPDATE contact_email_variants SET converted_at = NOW()

Calculate new conversion_rate = (conversions / sends) * 100
```

---

### Part 5: Statistical Significance Calculator

**File:** `/api/ab-testing/calculate-winner.js`

```javascript
import { createClient } from "@supabase/supabase-js";

const supabase = createClient(
  process.env.SUPABASE_URL,
  process.env.SUPABASE_KEY
);

export default async function handler(req, res) {
  const { campaign_id } = req.body;

  // Fetch all variants for this campaign
  const { data: variants } = await supabase
    .from("email_ab_tests")
    .select("*")
    .eq("campaign_id", campaign_id)
    .order("reply_rate", { ascending: false });

  if (!variants || variants.length < 2) {
    return res.json({ message: "Need at least 2 variants to compare" });
  }

  // Require minimum sample size (100 sends per variant)
  const minSampleSize = 100;
  if (variants.some(v => v.sends < minSampleSize)) {
    return res.json({
      message: `Waiting for minimum ${minSampleSize} sends per variant`,
      current_samples: variants.map(v => ({ variant: v.variant, sends: v.sends }))
    });
  }

  // Calculate statistical significance using chi-square test
  const [best, secondBest] = variants;

  const chiSquare = calculateChiSquare(
    best.replies,
    best.sends,
    secondBest.replies,
    secondBest.sends
  );

  const pValue = chiSquareToPValue(chiSquare);
  const confidence = (1 - pValue) * 100;

  // Require 95% confidence to declare winner
  if (confidence >= 95) {
    // Declare winner!
    await supabase
      .from("email_ab_tests")
      .update({
        is_winner: true,
        winner_declared_at: new Date(),
        statistical_confidence: confidence,
        test_ended_at: new Date(),
      })
      .eq("campaign_id", campaign_id)
      .eq("variant", best.variant);

    // Pause losing variants
    await supabase
      .from("email_ab_tests")
      .update({
        is_winner: false,
        test_ended_at: new Date(),
      })
      .eq("campaign_id", campaign_id)
      .neq("variant", best.variant);

    return res.json({
      winner: best.variant,
      confidence: Math.round(confidence),
      best_reply_rate: best.reply_rate,
      lift_over_second: ((best.reply_rate - secondBest.reply_rate) / secondBest.reply_rate * 100).toFixed(1),
      action: "Scale winner to all remaining leads",
    });
  } else {
    return res.json({
      message: "No statistically significant winner yet",
      confidence: Math.round(confidence),
      required_confidence: 95,
      current_leader: best.variant,
      keep_testing: true,
    });
  }
}

function calculateChiSquare(successA, totalA, successB, totalB) {
  const failureA = totalA - successA;
  const failureB = totalB - successB;

  const pooledProportion = (successA + successB) / (totalA + totalB);

  const expectedSuccessA = totalA * pooledProportion;
  const expectedFailureA = totalA * (1 - pooledProportion);
  const expectedSuccessB = totalB * pooledProportion;
  const expectedFailureB = totalB * (1 - pooledProportion);

  const chiSquare =
    Math.pow(successA - expectedSuccessA, 2) / expectedSuccessA +
    Math.pow(failureA - expectedFailureA, 2) / expectedFailureA +
    Math.pow(successB - expectedSuccessB, 2) / expectedSuccessB +
    Math.pow(failureB - expectedFailureB, 2) / expectedFailureB;

  return chiSquare;
}

function chiSquareToPValue(chiSquare) {
  // Simplified p-value calculation for df=1 (2 groups)
  // For production, use a statistics library like jStat
  // This is an approximation
  return Math.exp(-chiSquare / 2);
}
```

---

### Part 6: GHL Workflow - Daily A/B Test Analysis

**Workflow:** "Daily A/B Test Winner Check"

**Trigger:** Scheduled - Daily at 11:00 PM

**Step 1: Check All Active Campaigns**
```javascript
GET from Supabase:
SELECT DISTINCT campaign_id
FROM email_ab_tests
WHERE is_winner IS NULL
  AND test_started_at > NOW() - INTERVAL '30 days';
```

**Step 2: For Each Campaign, Calculate Winner**
```javascript
For each campaign_id:
   POST to /api/ab-testing/calculate-winner
   Body: { "campaign_id": "{{campaign_id}}" }

   Response:
   {
      "winner": "B",
      "confidence": 97,
      "best_reply_rate": 12.5,
      "lift_over_second": 45.2
   }
```

**Step 3: If Winner Found, Update Campaign**
```
IF: winner declared
THEN:
   1. Stop sending variants A and C
   2. Send variant B to all remaining leads
   3. Update Email Campaign Manager system prompt:
      "Use variant B style for all future campaigns (proven 45% lift)"
   4. Send notification to owner:
      "🎉 A/B Test Winner: Variant B (+45% reply rate)"
```

**Step 4: Send Daily Report**
```
Email to Owner:
Subject: Daily A/B Test Results

Hi {{owner.first_name}},

Here's today's A/B testing performance:

Active Tests: {{active_test_count}}
Winners Declared: {{winners_today}}

Top Performing Campaign:
- Variant: {{winner.variant}}
- Reply Rate: {{winner.reply_rate}}%
- Confidence: {{winner.confidence}}%
- Lift: +{{winner.lift}}% vs other variants

Next Steps:
✅ Scaling variant {{winner.variant}} to remaining leads
✅ Applying learnings to future campaigns

[View Detailed Results]({{supabase_dashboard_link}})

Regards,
CircuitOS A/B Testing System
```

---

## System 2: ROI Attribution Tracking

### Expected Impact: Prove Value with Data

---

### Part 1: Supabase Schema

```sql
-- Revenue Attribution
CREATE TABLE revenue_attribution (
   id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
   contact_id VARCHAR(255) NOT NULL,
   deal_id VARCHAR(255),
   deal_value DECIMAL(10,2),
   conversion_date DATE,

   -- First Touch Attribution
   first_touch_channel VARCHAR(100), -- 'Virtual LPR', 'Website Form', 'Referral'
   first_touch_source VARCHAR(255), -- Specific source (e.g., 'Google Organic', 'Facebook Ad')
   first_touch_date DATE,
   first_lpr_score INT, -- Initial lead score

   -- Last Touch Attribution
   last_touch_channel VARCHAR(100), -- 'Cold Email Variant B', 'SMS', 'Phone Call'
   last_touch_action VARCHAR(255), -- Specific action that closed them
   last_touch_date DATE,

   -- All Touchpoints (Multi-Touch Attribution)
   touchpoint_sequence JSONB, -- [{channel, date, action, lpr_score_before, lpr_score_after}]
   total_touchpoints INT,

   -- Cost Attribution
   virtual_lpr_cost DECIMAL(10,4) DEFAULT 0.00, -- Free
   ai_employee_cost DECIMAL(10,4), -- Claude API calls
   email_campaign_cost DECIMAL(10,4), -- Instantly.ai
   sales_rep_time_cost DECIMAL(10,4), -- Time spent by rep
   total_cac DECIMAL(10,2), -- Customer Acquisition Cost

   -- ROI Metrics
   ltv_projected DECIMAL(10,2), -- Lifetime Value (projected)
   ltv_actual DECIMAL(10,2), -- Actual LTV (updated over time)
   roi_percentage DECIMAL(10,2), -- (Revenue - CAC) / CAC * 100
   payback_period_days INT, -- Days to recover CAC

   created_at TIMESTAMP DEFAULT NOW(),
   updated_at TIMESTAMP DEFAULT NOW()
);

-- Channel Performance Summary
CREATE VIEW channel_performance AS
SELECT
   first_touch_channel,
   COUNT(*) as total_conversions,
   SUM(deal_value) as total_revenue,
   AVG(total_cac) as avg_cac,
   AVG(roi_percentage) as avg_roi,
   AVG(payback_period_days) as avg_payback_days,
   SUM(deal_value) / COUNT(*) as avg_deal_value
FROM revenue_attribution
GROUP BY first_touch_channel
ORDER BY total_revenue DESC;

-- Create indexes
CREATE INDEX idx_revenue_contact ON revenue_attribution(contact_id);
CREATE INDEX idx_revenue_date ON revenue_attribution(conversion_date DESC);
CREATE INDEX idx_revenue_channel ON revenue_attribution(first_touch_channel);
```

---

### Part 2: GHL Workflow - Track Attribution on Deal Close

**Workflow:** "Calculate ROI Attribution"

**Trigger:** Deal stage changed to "Closed Won"

**Step 1: Gather All Contact Activities**
```javascript
GET from GHL API:
- Contact creation date + source
- All emails sent/received (from/to this contact)
- All SMS sent/received
- All phone calls logged
- All workflow triggers
- All tags added/removed (with timestamps)

Build touchpoint timeline:
[
   { date: "2025-01-15", channel: "Virtual LPR", action: "Website visit detected", lpr_score: 0 },
   { date: "2025-01-15", channel: "AI Lead Scorer", action: "Initial score calculated", lpr_score: 82 },
   { date: "2025-01-16", channel: "Cold Email Variant B", action: "Email sent", lpr_score: 82 },
   { date: "2025-01-18", channel: "Email Reply", action: "Lead replied", lpr_score: 88 },
   { date: "2025-01-19", channel: "Phone Call", action: "Sales rep called", lpr_score: 88 },
   { date: "2025-01-20", channel: "Deal Close", action: "Contract signed", lpr_score: 100 }
]
```

**Step 2: Calculate Costs**
```javascript
// Virtual LPR Cost
virtual_lpr_cost = 0.00; // Free (Google Analytics, GMB API)

// AI Employee Costs
ai_calls = [
   { function: "Lead Scorer", calls: 1, cost_per_call: 0.01 },
   { function: "Email Campaign Manager", calls: 3, cost_per_call: 0.02 },
   { function: "Channel Router", calls: 2, cost_per_call: 0.01 }
];
ai_employee_cost = ai_calls.reduce((sum, a) => sum + (a.calls * a.cost_per_call), 0);
// Example: 0.01 + 0.06 + 0.02 = $0.09

// Email Campaign Cost
emails_sent = 4; // To this contact
instantly_cost_per_email = 0.07 / 30; // $0.07/mo ÷ 30 sends per day (approx)
email_campaign_cost = emails_sent * instantly_cost_per_email;
// Example: 4 × $0.0023 = $0.01

// Sales Rep Time Cost
rep_time_minutes = 45; // From call logs + manual tasks
rep_hourly_rate = 30; // $30/hr
sales_rep_time_cost = (rep_time_minutes / 60) * rep_hourly_rate;
// Example: 0.75 × $30 = $22.50

// Total CAC
total_cac = virtual_lpr_cost + ai_employee_cost + email_campaign_cost + sales_rep_time_cost;
// Example: $0.00 + $0.09 + $0.01 + $22.50 = $22.60
```

**Step 3: Calculate ROI**
```javascript
// Deal value (from GHL deal object)
deal_value = {{deal.value}}; // e.g., $2,388 (12-month gym membership)

// Projected LTV (can be 2-5x initial deal value)
ltv_multiplier = 2.5; // Average customer stays 2.5x initial contract
ltv_projected = deal_value * ltv_multiplier;
// Example: $2,388 × 2.5 = $5,970

// ROI
roi_percentage = ((ltv_projected - total_cac) / total_cac) * 100;
// Example: (($5,970 - $22.60) / $22.60) × 100 = 26,307%

// Payback period (days to recover CAC from monthly revenue)
monthly_revenue = deal_value / 12; // e.g., $199/mo
payback_period_days = Math.ceil((total_cac / monthly_revenue) * 30);
// Example: ($22.60 / $199) × 30 = 3.4 days
```

**Step 4: Store Attribution Data**
```javascript
INSERT INTO revenue_attribution (
   contact_id,
   deal_id,
   deal_value,
   conversion_date,
   first_touch_channel,
   first_touch_date,
   first_lpr_score,
   last_touch_channel,
   last_touch_date,
   touchpoint_sequence,
   total_touchpoints,
   virtual_lpr_cost,
   ai_employee_cost,
   email_campaign_cost,
   sales_rep_time_cost,
   total_cac,
   ltv_projected,
   roi_percentage,
   payback_period_days
) VALUES (
   '{{contact.id}}',
   '{{deal.id}}',
   {{deal.value}},
   '{{deal.closed_date}}',
   '{{first_touchpoint.channel}}',
   '{{first_touchpoint.date}}',
   {{first_touchpoint.lpr_score}},
   '{{last_touchpoint.channel}}',
   '{{last_touchpoint.date}}',
   '{{touchpoint_sequence_json}}',
   {{total_touchpoints}},
   0.00,
   {{ai_employee_cost}},
   {{email_campaign_cost}},
   {{sales_rep_time_cost}},
   {{total_cac}},
   {{ltv_projected}},
   {{roi_percentage}},
   {{payback_period_days}}
);
```

**Step 5: Send Attribution Report to Owner**
```
Email:
Subject: 🎉 New Customer ROI Report - {{contact.name}}

Hi {{owner.first_name}},

Great news! {{contact.name}} just became a customer. Here's the ROI breakdown:

💰 REVENUE:
Deal Value: ${{deal.value}}
Projected LTV: ${{ltv_projected}}

📊 ACQUISITION COST:
Virtual LPR: $0.00 (free)
AI Employees: ${{ai_employee_cost}}
Email Campaign: ${{email_campaign_cost}}
Sales Rep Time: ${{sales_rep_time_cost}}
TOTAL CAC: ${{total_cac}}

🚀 ROI METRICS:
ROI: {{roi_percentage}}%
Payback Period: {{payback_period_days}} days

🔍 ATTRIBUTION:
First Touch: {{first_touch_channel}} ({{first_touch_date}})
Last Touch: {{last_touch_channel}} ({{last_touch_date}})
Total Touchpoints: {{total_touchpoints}}

Journey:
{{#each touchpoint_sequence}}
   {{date}} - {{channel}}: {{action}}
{{/each}}

[View Full Report]({{dashboard_link}})

Keep up the great work!
CircuitOS Attribution System
```

---

### Part 3: ROI Dashboard (GHL Widget)

```html
<div style="padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 12px; margin-bottom: 20px;">
  <h2 style="margin: 0 0 20px 0;">💰 ROI Dashboard</h2>

  <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px;">
    <div style="background: rgba(255,255,255,0.2); padding: 15px; border-radius: 8px;">
      <p style="margin: 0; font-size: 12px; opacity: 0.9;">Total Revenue (30 days)</p>
      <p style="margin: 5px 0 0 0; font-size: 28px; font-weight: bold;">$<span id="total-revenue">--</span></p>
    </div>

    <div style="background: rgba(255,255,255,0.2); padding: 15px; border-radius: 8px;">
      <p style="margin: 0; font-size: 12px; opacity: 0.9;">Total CAC</p>
      <p style="margin: 5px 0 0 0; font-size: 28px; font-weight: bold;">$<span id="total-cac">--</span></p>
    </div>

    <div style="background: rgba(255,255,255,0.2); padding: 15px; border-radius: 8px;">
      <p style="margin: 0; font-size: 12px; opacity: 0.9;">Average ROI</p>
      <p style="margin: 5px 0 0 0; font-size: 28px; font-weight: bold;"><span id="avg-roi">--</span>%</p>
    </div>
  </div>

  <div style="margin-top: 20px; background: rgba(255,255,255,0.2); padding: 15px; border-radius: 8px;">
    <h3 style="margin: 0 0 10px 0;">Top Performing Channels</h3>
    <table style="width: 100%; color: white;">
      <thead>
        <tr style="border-bottom: 1px solid rgba(255,255,255,0.3);">
          <th style="text-align: left; padding: 8px;">Channel</th>
          <th style="text-align: right; padding: 8px;">Conversions</th>
          <th style="text-align: right; padding: 8px;">Revenue</th>
          <th style="text-align: right; padding: 8px;">Avg ROI</th>
        </tr>
      </thead>
      <tbody id="channel-performance">
        <tr><td colspan="4" style="text-align: center; padding: 20px;">Loading...</td></tr>
      </tbody>
    </table>
  </div>
</div>

<script>
async function loadROIData() {
  const response = await fetch('https://your-vercel.com/api/analytics/roi-dashboard');
  const data = await response.json();

  document.getElementById('total-revenue').textContent = data.totalRevenue.toLocaleString();
  document.getElementById('total-cac').textContent = data.totalCAC.toLocaleString();
  document.getElementById('avg-roi').textContent = data.avgROI.toLocaleString();

  const tbody = document.getElementById('channel-performance');
  tbody.innerHTML = data.topChannels.map(ch => `
    <tr>
      <td style="padding: 8px;">${ch.channel}</td>
      <td style="text-align: right; padding: 8px;">${ch.conversions}</td>
      <td style="text-align: right; padding: 8px;">$${ch.revenue.toLocaleString()}</td>
      <td style="text-align: right; padding: 8px;">${ch.avgROI}%</td>
    </tr>
  `).join('');
}

loadROIData();
setInterval(loadROIData, 300000); // Refresh every 5 minutes
</script>
```

---

## Week 2 Completion Checklist

### Day 1: A/B Testing
- [ ] Create Supabase tables (email_ab_tests, contact_email_variants)
- [ ] Deploy statistical significance calculator
- [ ] Create GHL workflows (send variants, track engagement, daily winner check)
- [ ] Test with 3 sample campaigns

### Day 2: ROI Attribution
- [ ] Create Supabase revenue_attribution table
- [ ] Build attribution tracking workflow
- [ ] Deploy ROI dashboard
- [ ] Test with 5 historical closed deals

### Day 3: Lead Quality Feedback (Part 3 of Week 2)
- [ ] Add lead quality rating fields to GHL
- [ ] Create feedback collection workflow
- [ ] Connect feedback to ML retraining system

### Day 4: Performance Dashboards
- [ ] Deploy all dashboard widgets
- [ ] Connect real-time data feeds
- [ ] Train team on dashboard usage

---

## Expected Outcomes After Week 2

✅ **Revenue Growth:**
- +20-35% reply rates from A/B testing
- +15-25% conversion rates from optimized campaigns
- Provable ROI for every closed deal

✅ **Data-Driven Decisions:**
- Know which channels drive highest ROI
- Optimize spend based on CAC by channel
- Track customer journey from first touch to close

✅ **Continuous Improvement:**
- Automatic winner selection and scaling
- Lead quality feedback improves LPR accuracy over time
- Real-time visibility into all metrics

**Monthly Revenue Impact:** +$2,000-10,000 (depending on current volume)

---

## Next: Week 3-4 (Scale & Polish)

See: `/GHL-Setup/Week3-4-Scale-and-Polish-Implementation.md`
