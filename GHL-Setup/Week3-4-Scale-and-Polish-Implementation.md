# Week 3-4: Scale & Polish Implementation - CircuitOS

## 🚀 USER EXPERIENCE & AUTOMATION

**Focus:** Onboarding, Training, Data Hygiene, Lead Reactivation
**Expected Impact:** 10x faster onboarding, automated maintenance, recovered revenue from cold leads
**Implementation Time:** ~18 hours

---

## System 1: Business Onboarding Wizard

### Goal: 7-Minute Setup (vs 2-4 Hours)

---

### Part 1: GHL Form - "Business Onboarding Wizard"

**Create Multi-Step Form in GHL**

**URL:** `https://yourdomain.com/onboarding`

#### Step 1: Business Basics (2 minutes)
```
Form Fields:
1. Business Name* (text)
2. Industry* (dropdown)
   - Gym/Fitness Studio
   - Restaurant/Cafe
   - Retail Store
   - Professional Services
   - Healthcare Practice
   - Other

3. Location* (address autocomplete)
   - Street Address
   - City
   - State
   - ZIP Code

4. Contact Info* (text)
   - Phone
   - Website
   - Email

5. Business Description (text area)
   - "Describe your business in 2-3 sentences"
   - AI will use this to generate ICP
```

#### Step 2: Target Customer Profile (3 minutes)
```
Form Fields:
1. Who is your ideal customer?* (text area)
   - Example: "Busy professionals aged 25-45 who want to get fit but don't have time for long gym sessions"

2. What problem do you solve?* (text area)
   - Example: "30-minute high-intensity workouts that deliver results without wasting time"

3. Average customer value* (number)
   - "What's the average amount a customer spends with you per year?"
   - Example: $2,388 (12-month membership at $199/mo)

4. Service radius* (number)
   - "How far will customers travel to use your service?"
   - Example: 5 miles

5. Top 3 competitors (text, optional)
   - For competitive intelligence
```

#### Step 3: AI Auto-Configuration (30 seconds - Backend Processing)
```
Form Submit → Trigger GHL Workflow: "Auto-Configure Business"

Workflow Steps:
1. Call Claude API to generate ICP profile
2. Set up 7 AI Employees with industry-specific prompts
3. Create email templates with business name/location
4. Configure Virtual LPR detection zones
5. Set up review monitoring
6. Create initial workflows
```

#### Step 4: Test Lead Processing (1 minute)
```
Display on-screen:
"We're processing a sample lead to show you how the system works..."

Backend:
1. Create test contact with industry-typical data
2. Run through full workflow:
   - Virtual LPR detection
   - Lead scoring (show score breakdown)
   - Email generation (show 3 variants)
3. Display results:
   ✅ Lead Score: 82/100
   ✅ High Intent: Yes
   ✅ Email Variant A: [Preview]
   ✅ Email Variant B: [Preview]
   ✅ Email Variant C: [Preview]

"This is what your leads will experience. Ready to go live?"
```

#### Step 5: Activate & Go Live (1 minute)
```
Checklist Display:
✅ Business profile created
✅ AI Employees configured
✅ Virtual LPR activated
✅ Email campaigns ready
✅ Review monitoring enabled

Final Steps:
[ ] Connect Google My Business (OAuth)
[ ] Connect Instantly.ai (API key)
[ ] Install website tracking pixel

[Activate Now] button → Enables all workflows

Confirmation:
"🎉 You're Live!
Your first leads will be detected within 24 hours.
Check your dashboard at [link]"
```

---

### Part 2: Auto-Configuration Backend

**File:** `/api/onboarding/auto-configure-business.js`

```javascript
import Anthropic from "@anthropic-ai/sdk";
import { createClient } from "@supabase/supabase-js";

const anthropic = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY });
const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_KEY);

export default async function handler(req, res) {
  const {
    business_name,
    industry,
    location,
    ideal_customer,
    problem_solved,
    avg_customer_value,
    service_radius,
  } = req.body;

  try {
    // Step 1: Generate ICP Profile with Claude
    const icpPrompt = `You are a world-class business strategist. Based on the following business information, create a detailed Ideal Customer Profile (ICP).

Business: ${business_name}
Industry: ${industry}
Location: ${location.city}, ${location.state}
Ideal Customer: ${ideal_customer}
Problem Solved: ${problem_solved}
Avg Customer Value: $${avg_customer_value}
Service Radius: ${service_radius} miles

Create an ICP with:
1. Demographics (age, income, occupation, family status)
2. Psychographics (values, interests, lifestyle)
3. Behaviors (online activity, purchase patterns)
4. Pain points (3-5 specific problems)
5. Buying triggers (what motivates them to buy)
6. Decision criteria (how they choose a provider)

Output as structured JSON.`;

    const icpResponse = await anthropic.messages.create({
      model: "claude-sonnet-4-5-20250929",
      max_tokens: 2000,
      temperature: 0.5,
      messages: [{ role: "user", content: icpPrompt }],
    });

    const icp = JSON.parse(icpResponse.content[0].text);

    // Step 2: Generate Industry-Specific Email Templates
    const emailPrompt = `Create 3 cold email templates for ${business_name} (${industry}) targeting: ${ideal_customer}.

Requirements:
- Variant A: Professional tone
- Variant B: Casual/friendly tone
- Variant C: Urgent/scarcity tone
- Each email: 50-75 words
- Subject line for each
- Personalization placeholders: {{first_name}}, {{city}}, {{lpr_score}}

Output as JSON array.`;

    const emailResponse = await anthropic.messages.create({
      model: "claude-sonnet-4-5-20250929",
      max_tokens: 2000,
      temperature: 0.7,
      messages: [{ role: "user", content: emailPrompt }],
    });

    const emailTemplates = JSON.parse(emailResponse.content[0].text);

    // Step 3: Configure Virtual LPR Detection Zones
    const detectionZones = calculateDetectionZones(location, service_radius);

    // Step 4: Create GHL Business Profile
    const ghlProfile = await createGHLBusinessProfile({
      business_name,
      industry,
      location,
      icp,
      emailTemplates,
      detectionZones,
      avg_customer_value,
    });

    // Step 5: Initialize 7 AI Employees with Industry Prompts
    await initializeAIEmployees({
      business_id: ghlProfile.id,
      industry,
      icp,
    });

    // Step 6: Create Test Lead
    const testLead = await createTestLead({
      business_id: ghlProfile.id,
      industry,
      icp,
    });

    return res.json({
      success: true,
      business_id: ghlProfile.id,
      icp,
      email_templates: emailTemplates,
      test_lead: testLead,
      setup_complete: true,
    });
  } catch (error) {
    console.error("Onboarding error:", error);
    return res.status(500).json({ error: error.message });
  }
}

function calculateDetectionZones(location, service_radius) {
  // Calculate lat/lng boundaries for Virtual LPR detection
  const milesPerLatDegree = 69;
  const milesPerLngDegree = 69 * Math.cos((location.lat * Math.PI) / 180);

  return {
    center: { lat: location.lat, lng: location.lng },
    radius_miles: service_radius,
    bounds: {
      north: location.lat + service_radius / milesPerLatDegree,
      south: location.lat - service_radius / milesPerLatDegree,
      east: location.lng + service_radius / milesPerLngDegree,
      west: location.lng - service_radius / milesPerLngDegree,
    },
  };
}

async function createGHLBusinessProfile(data) {
  const ghlApiKey = process.env.GHL_API_KEY;

  const response = await fetch("https://rest.gohighlevel.com/v1/locations/", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${ghlApiKey}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      name: data.business_name,
      address: data.location.address,
      city: data.location.city,
      state: data.location.state,
      postalCode: data.location.zip,
      customFields: {
        industry: data.industry,
        icp_profile: JSON.stringify(data.icp),
        email_templates: JSON.stringify(data.emailTemplates),
        virtual_lpr_zones: JSON.stringify(data.detectionZones),
        avg_customer_value: data.avg_customer_value,
      },
    }),
  });

  return response.json();
}

async function initializeAIEmployees({ business_id, industry, icp }) {
  // Load industry-specific system prompts from templates
  const industryPrompts = {
    "Gym/Fitness Studio": {
      lead_scorer_additions: "Prioritize fitness goals, proximity to gym, and ability to commit to regular schedule.",
      copywriter_tone: "Motivational, results-focused, urgent (limited spots available)",
    },
    "Restaurant/Cafe": {
      lead_scorer_additions: "Prioritize food preferences, dining frequency, group size potential.",
      copywriter_tone: "Warm, inviting, focused on experience and ambiance",
    },
    // Add more industries...
  };

  const prompts = industryPrompts[industry] || industryPrompts["Professional Services"];

  await supabase.from("ai_employee_config").insert({
    business_id,
    industry,
    custom_prompts: prompts,
    icp_context: JSON.stringify(icp),
  });
}

async function createTestLead({ business_id, industry, icp }) {
  // Generate realistic test lead based on ICP
  const testData = {
    first_name: "Sarah",
    last_name: "Johnson",
    email: "test_lead@example.com",
    phone: "(555) 123-4567",
    city: icp.demographics.location,
    source: "Virtual LPR (Test)",
    customFields: {
      lprScore: 82,
      fitScore: 38,
      intentScore: 28,
      timingScore: 16,
      distance_miles: 2.3,
      median_income: icp.demographics.income,
      age_bracket: icp.demographics.age,
    },
  };

  // Create in GHL
  const ghlApiKey = process.env.GHL_API_KEY;
  const response = await fetch("https://rest.gohighlevel.com/v1/contacts/", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${ghlApiKey}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      locationId: business_id,
      ...testData,
    }),
  });

  return response.json();
}
```

---

## System 2: Data Hygiene Automation

### Goal: Keep Database Clean Automatically

---

### Part 1: GHL Workflow - "Weekly Data Hygiene"

**Trigger:** Scheduled - Every Sunday at 2:00 AM

**Step 1: Mark Invalid Emails**
```sql
-- Get hard bounces from Instantly.ai
API Call: GET https://api.instantly.ai/api/v1/bounces

For each hard bounce:
   Update GHL Contact:
   - email_status = "invalid"
   - email_opt_out = true
   - Add Tag: "Email Invalid - Hard Bounce"
   - Remove from all email campaigns
```

**Step 2: Mark Disconnected Phone Numbers**
```sql
-- Get SMS delivery failures from GHL
GET from GHL API: /conversations/messages
Filter: status = "undelivered" AND error_code = "phone_disconnected"

For each disconnected number:
   Update Contact:
   - phone_status = "disconnected"
   - Add Tag: "Phone Disconnected"
   - Remove from all SMS campaigns
```

**Step 3: Calculate Data Quality Score**
```javascript
For each contact:
   data_quality_score = 0;

   // Email (20 points)
   if (email && email_status === "valid") score += 20;

   // Phone (20 points)
   if (phone && phone_status === "active") score += 20;

   // Address (15 points)
   if (address && city && state && zip) score += 15;

   // LPR Score (25 points)
   if (lprScore >= 70) score += 25;
   else if (lprScore >= 40) score += 15;
   else if (lprScore > 0) score += 5;

   // Recent Activity (20 points)
   if (last_activity_date within 30 days) score += 20;
   else if (last_activity_date within 90 days) score += 10;

   Update Contact:
   - data_quality_score = score (0-100)
```

**Step 4: Archive Low-Quality Leads**
```
Find contacts WHERE:
   - data_quality_score < 30
   - last_activity_date > 180 days ago
   - never converted

Action:
   - Update status = "Archived - Low Quality"
   - Remove from active campaigns
   - Move to "Archive" pipeline
   - Schedule deletion in 90 days (GDPR retention)
```

**Step 5: Send Data Hygiene Report**
```
Email to Owner:
Subject: Weekly Data Hygiene Report

Hi {{owner.first_name}},

Here's this week's database cleanup:

📧 EMAIL HEALTH:
- Invalid emails found: {{invalid_email_count}}
- Hard bounces: {{hard_bounce_count}}
- Cleaned: {{cleaned_email_count}}

📱 PHONE HEALTH:
- Disconnected numbers: {{disconnected_count}}
- Cleaned: {{cleaned_phone_count}}

📊 DATA QUALITY:
- Avg quality score: {{avg_quality_score}}/100
- High quality (80+): {{high_quality_count}}
- Low quality (<30): {{low_quality_count}}

🗂️ ARCHIVED:
- Low-quality leads archived: {{archived_count}}
- Scheduled for deletion (90 days): {{deletion_scheduled_count}}

NEXT STEPS:
✅ All invalid contacts removed from campaigns
✅ Data quality scores updated
✅ Low-quality leads archived

[View Detailed Report]({{dashboard_link}})

Your database is {{health_percentage}}% healthy!

Regards,
CircuitOS Data Hygiene System
```

---

## System 3: Cold Lead Reactivation

### Goal: Recover Revenue from Old Leads

---

### Part 1: GHL Workflow - "Quarterly Reactivation Campaign"

**Trigger:** Scheduled - Jan 1, Apr 1, Jul 1, Oct 1 at 9:00 AM

**Step 1: Find Reactivation Candidates**
```
Search GHL Contacts WHERE:
   - status = "Archived" OR "Cold Lead"
   - original lpr_score >= 60 (was high quality)
   - last_activity_date between 90-365 days ago
   - email_status = "valid"
   - phone_status = "active" OR null
   - never converted
   - still in service area (distance_miles <= service_radius)

Result: "Reactivation Candidate" list
```

**Step 2: Generate Personalized Reactivation Email**
```
For each candidate, call Master Copywriter:

POST to /api/ai-employees/master-copywriter
Body: {
   "contact": {{contact}},
   "business": {{business}},
   "email_type": "reactivation",
   "context": {
      "last_interaction": "{{last_activity_date}}",
      "original_interest": "{{original_source}}",
      "time_since_last_contact": "{{days_since_last_contact}} days",
      "original_lpr_score": {{lprScore}}
   }
}

Claude generates:
Subject: "It's been a while, {{first_name}} - here's what's new"

Body:
Hi {{first_name}},

It's been {{months_since_last_contact}} months since we last connected. I noticed you showed interest in {{business.category}} back in {{original_month}}.

A lot has changed since then:
- {{new_feature_1}}
- {{new_feature_2}}
- {{new_offer}}

I wanted to reach out because I think you'd be a great fit for {{current_promotion}}.

Still interested? Reply "YES" and I'll send you the details.

Not the right time? No worries - just hit unsubscribe and we won't bother you again.

Best,
{{business.owner_name}}
{{business.name}}

P.S. This offer ends {{expiration_date}} - spots are limited!
```

**Step 3: Send Reactivation Email**
```
Send via Instantly.ai:
- Subject line from Claude
- Body from Claude
- Track as "Reactivation Campaign Q{{quarter}}"
```

**Step 4: Monitor Responses**
```
IF: Lead replies with "YES" OR positive intent
THEN:
   - Move from "Archived" to "Active Lead"
   - Update status = "Re-engaged"
   - Trigger "High-Intent Cold Email Sequence"
   - Notify sales rep: "Lead {{name}} re-engaged!"

IF: Lead clicks unsubscribe
THEN:
   - Process unsubscribe (CAN-SPAM workflow)
   - Move to "Permanently Unsubscribed" list

IF: No response after 7 days
THEN:
   - Send follow-up SMS (if phone available)
   - Wait 7 more days
   - If still no response: Return to "Archived" status
```

**Step 5: Quarterly Reactivation Report**
```
Email to Owner:
Subject: Q{{quarter}} Reactivation Campaign Results

Hi {{owner.first_name}},

Your quarterly reactivation campaign is complete!

📧 CAMPAIGN STATS:
- Emails sent: {{emails_sent}}
- Open rate: {{open_rate}}%
- Reply rate: {{reply_rate}}%
- Re-engaged leads: {{reengaged_count}}

💰 REVENUE RECOVERED:
- Deals closed from reactivation: {{deals_closed}}
- Revenue generated: ${{revenue_generated}}
- ROI: {{roi_percentage}}%

🔥 TOP RE-ENGAGED LEADS:
{{#each top_reengaged}}
   - {{name}}: {{status}} ({{lpr_score}}/100)
{{/each}}

NEXT STEPS:
✅ {{reengaged_count}} leads moved to active status
✅ Sales rep notified of hot leads
✅ Follow-up sequences initiated

[View Full Campaign Report]({{dashboard_link}})

Next reactivation campaign: {{next_quarter_date}}

Regards,
CircuitOS Reactivation System
```

---

## System 4: Sales Rep Training Program

### Goal: Certify Reps on CircuitOS

---

### Part 1: GHL Course - "CircuitOS Sales Rep Certification"

**Module 1: Understanding the System (10 minutes)**
```
Lessons:
1. What is Virtual LPR? (Video: 3 min)
   - How we detect leads without them filling out forms
   - Why our leads are higher quality than traditional methods

2. How AI Employees Work (Video: 4 min)
   - 7 AI Employees and their roles
   - When AI escalates to you
   - How to read AI-generated context

3. Your Role in the Process (Video: 3 min)
   - When you get involved (high-intent leads only)
   - How to use AI insights to close faster
   - What NOT to do (don't override AI scoring)

Quiz: 5 questions
```

**Module 2: Reading Lead Scores (15 minutes)**
```
Lessons:
1. LPR Score Breakdown (Video: 5 min)
   - FIT Score (0-40): Demographics, location, affordability
   - INTENT Score (0-40): Behavior signals, urgency
   - TIMING Score (0-20): When they're ready to buy

2. Score Interpretation (Interactive: 5 min)
   - 90-100: RED HOT - Call immediately
   - 70-89: HIGH INTENT - Email first, then call within 24 hours
   - 40-69: MEDIUM INTENT - Let AI nurture, you follow up after reply
   - 0-39: LOW INTENT - AI only, don't waste your time

3. Real Examples (Case Studies: 5 min)
   - Lead with score 95: What to do? (Call now)
   - Lead with score 55: What to do? (Wait for AI to warm them up)
   - Lead with score 25: What to do? (Ignore, AI will handle)

Practice Exercise: 10 sample leads, you decide action
```

**Module 3: Responding to AI-Generated Leads (10 minutes)**
```
Lessons:
1. When AI Escalates to You (Video: 3 min)
   - GHL task created: "High-Intent Lead - Call Now"
   - Email reply detected: Lead asked a question
   - Channel router: AI determined call is next best step

2. Using AI Context (Video: 4 min)
   - Review lead's full journey (Virtual LPR → Email sequence → Reply)
   - Read AI's analysis: "This lead is ready because..."
   - Use AI-generated talking points in your call script

3. Continuing the Conversation (Video: 3 min)
   - Lead already received 3 AI emails - acknowledge this
   - Reference their specific questions/objections from replies
   - Close using AI's recommended approach

Role Play: Mock call with AI-escalated lead (recorded, graded by AI)
```

**Module 4: Troubleshooting (5 minutes)**
```
Lessons:
1. "Why isn't this lead responding?" (2 min)
   - Check email_status (might be invalid)
   - Check data_quality_score (might be low-quality lead)
   - Check reply history (might have replied but workflow failed)

2. "How do I manually trigger AI actions?" (2 min)
   - Add tag: "Re-score Lead" → Triggers Lead Scorer
   - Add tag: "Generate Email" → Triggers Master Copywriter
   - Create task: "AI Review" → Triggers manual AI analysis

3. "When do I mark a lead as 'Bad Quality'?" (1 min)
   - Wrong contact info (email/phone don't match person)
   - Outside service area (moved away)
   - Not actually interested (responded by mistake)
   - Action: Add tag "Bad Lead" → Trains ML to avoid similar leads

Troubleshooting Quiz: 5 scenarios, what would you do?
```

**Final Exam (10 questions)**
```
Must score 80% to pass

Questions cover:
- LPR score interpretation
- When to call vs email
- How to use AI context
- Troubleshooting common issues
- Best practices

PASS: Receive "CircuitOS Certified Sales Operator" badge
FAIL: Retake after reviewing modules
```

**Certificate:**
```
Upon passing:
- Digital certificate emailed
- Added to GHL profile: "Certified: {{date}}"
- Unlock access to "Advanced Sales Strategies" bonus module
```

---

## Week 3-4 Completion Checklist

### Week 3: User Experience
- [ ] Build business onboarding wizard (7-step form)
- [ ] Deploy auto-configuration backend
- [ ] Create sales rep training course (4 modules)
- [ ] Test onboarding with 3 sample businesses

### Week 4: Automation
- [ ] Create weekly data hygiene workflow
- [ ] Build quarterly reactivation campaign
- [ ] Deploy all automated reports
- [ ] Train team on new systems

---

## Expected Outcomes After Weeks 3-4

✅ **Faster Onboarding:**
- 7 minutes vs 2-4 hours (97% time savings)
- Automatic ICP generation
- Industry-specific AI configuration
- Test lead demo before going live

✅ **Automated Maintenance:**
- Weekly data cleanup (no manual work)
- Data quality scores (know which leads are good)
- Archive low-quality leads automatically
- GDPR-compliant retention

✅ **Revenue Recovery:**
- Quarterly reactivation campaigns
- 10-20% of cold leads re-engaged
- $1,000-5,000/quarter recovered revenue
- Automated personalization with AI

✅ **Team Readiness:**
- Sales reps certified on CircuitOS
- Know when/how to engage with AI-generated leads
- Troubleshooting skills
- Higher close rates from better preparation

**Total Impact (Weeks 3-4):**
- Onboarding: 10x faster
- Database: 95%+ clean data
- Revenue: +$4,000-20,000/year from reactivation
- Sales: +15-25% close rate from trained reps

---

## 🎉 All Systems Complete!

After completing Weeks 1-4, you'll have:
- ✅ **Week 1:** Legal compliance + operational reliability
- ✅ **Week 2:** Revenue optimization + data-driven decisions
- ✅ **Week 3-4:** User experience + automated maintenance

**Your CircuitOS is now WORLD-CLASS.**

---

## Next Steps

1. **Instagram/Facebook Graph API Integration** (your request)
   - See: `/GHL-Setup/Social-Media-Integration/Instagram-Facebook-Graph-API.md`

2. **Monthly Optimization**
   - Review A/B test winners
   - Analyze ROI by channel
   - Retrain ML models
   - Scale what works

3. **Expansion**
   - Add more AI Employees (custom use cases)
   - Integrate additional platforms (LinkedIn, TikTok)
   - Build client-facing dashboards
   - Create white-label offering for agencies

**You're ready to dominate your market with CircuitOS.**
