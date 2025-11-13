# Cold Email Orchestrator Skill
## High-Deliverability Email Sequencing & Platform Integration

**Priority**: CRITICAL (Gap #2)
**Platform**: Instantly.ai (Recommended - $37/mo)
**Purpose**: Execute cold email sequences with maximum deliverability

---

## Platform Integration

### Recommended: Instantly.ai

**Why Instantly**:
- Best deliverability (95%+ inbox rate)
- Unlimited email accounts ($37/mo flat fee)
- Built-in warm-up automation
- Best API for programmatic sending
- Real-time reply detection

**API Setup**:
```javascript
const instantly = {
  apiKey: process.env.INSTANTLY_API_KEY,
  baseURL: 'https://api.instantly.ai/v1',
  endpoints: {
    campaigns: '/campaigns',
    leads: '/leads',
    sequences: '/sequences',
    analytics: '/analytics'
  }
}
```

### Alternative Platforms

| Platform | Cost | Best For | API Quality |
|----------|------|----------|-------------|
| Instantly.ai | $37/mo | Deliverability | ⭐⭐⭐⭐⭐ |
| Smartlead | $39/mo | AI optimization | ⭐⭐⭐⭐ |
| Lemlist | $59/mo | Personalization | ⭐⭐⭐ |
| Woodpecker | $49/mo | Simplicity | ⭐⭐⭐ |

---

## Sequence Builder

### 7-Touch Cold Email Sequence (Default)

**Day 1: Initial Outreach**
```
Subject: {{firstName}}, quick question about {{business}}
Body: [Hook + Story + Soft CTA]
Goal: Start conversation
Send Time: 9:00 AM local time
```

**Day 3: Value Add (If No Reply)**
```
Subject: RE: Quick question about {{business}}
Body: [Additional value, no ask]
Goal: Build credibility
Send Time: 2:00 PM local time
```

**Day 5: Case Study (If No Reply)**
```
Subject: How {{competitor_city}} gym added $11K/month
Body: [Relevant case study + CTA]
Goal: Prove it works
Send Time: 10:00 AM local time
```

**Day 7: Break-Up Email (If No Reply)**
```
Subject: Should I close your file?
Body: [Polite exit, last chance CTA]
Goal: Pattern interrupt
Send Time: 3:00 PM local time
```

**Day 10: Different Angle (If No Reply)**
```
Subject: Different question, {{firstName}}
Body: [New hook, different pain point]
Goal: Re-engage
Send Time: 11:00 AM local time
```

**Day 14: Final Touch (If No Reply)**
```
Subject: Last one, promise
Body: [Brief, valuable resource + soft CTA]
Goal: Leave door open
Send Time: 1:00 PM local time
```

**Day 21: Long-term Nurture Tag**
```
Action: Move to monthly newsletter sequence
Goal: Stay top of mind
```

---

## A/B Testing Framework

### What to Test

**Subject Lines** (Biggest impact on open rate):
```
Variant A: Pain-focused
"{{firstName}}, your gym is bleeding $4,100/month"

Variant B: Curiosity-focused
"The $11,500 secret {{competitor_city}} gyms know"

Variant C: Direct benefit
"{{firstName}}, want 10 new PT clients by Dec 15?"

Sample Size: 100 per variant
Metric: Open rate
Winner: Highest open rate → Use for next 1000
```

**Email Body** (Impact on reply rate):
```
Variant A: Story-heavy
Focus: Case study, social proof

Variant B: Data-heavy
Focus: Statistics, numbers

Variant C: Question-heavy
Focus: Engage with questions

Sample Size: 100 per variant
Metric: Reply rate
Winner: Highest reply rate → Use for next 1000
```

**Send Time** (Impact on open rate):
```
Test Times:
- 9:00 AM (start of day check)
- 2:00 PM (post-lunch)
- 6:00 PM (end of day wind-down)

Segment by timezone (auto-adjust)
Test across 300 sends
Winner: Highest open rate
```

---

## Deliverability Optimization

### Email Warm-Up Protocol

**Week 1**: 5 emails/day per account
**Week 2**: 10 emails/day per account
**Week 3**: 20 emails/day per account
**Week 4**: 40 emails/day per account
**Week 5+**: Max 50 emails/day per account (safe limit)

**Warm-Up Features** (Instantly.ai built-in):
- Auto-reply to warm-up emails
- Gradual volume increase
- Spam folder avoidance
- Domain reputation building

### Domain Health Monitoring

**Check Daily**:
- Bounce rate (<2% = healthy)
- Spam complaint rate (<0.1% = healthy)
- Unsubscribe rate (<0.5% = healthy)
- Reply rate (>3% = excellent)

**Red Flags** (pause sending if):
- Bounce rate >5%
- Spam complaints >0.5%
- Deliverability drop >10%

### SPF, DKIM, DMARC Setup

**Required DNS Records**:
```
SPF Record:
v=spf1 include:instantly.ai ~all

DKIM Record:
instantly._domainkey.yourdomain.com
(Provided by Instantly.ai in settings)

DMARC Record:
v=DMARC1; p=quarantine; rua=mailto:admin@yourdomain.com
```

**Verification**:
- Use Instantly.ai domain checker
- Test with Mail-Tester.com (aim for 10/10 score)
- Monitor with Google Postmaster Tools

---

## Reply Detection & Routing

### Auto-Detection Rules

**Positive Reply** (interested):
```
Triggers: "yes", "interested", "tell me more", "call me"
Action:
1. Stop sequence immediately
2. Tag lead as "Hot - Replied"
3. Notify sales rep via Slack/SMS
4. Add to "Replied Leads" CRM list
5. Send to DMN agent for qualification
```

**Negative Reply** (not interested):
```
Triggers: "not interested", "unsubscribe", "remove me"
Action:
1. Stop sequence immediately
2. Tag lead as "Not Interested"
3. Add to suppression list
4. Remove from all future sequences
5. Log reason if provided
```

**Out-of-Office** (auto-reply):
```
Triggers: "out of office", "away", "vacation"
Action:
1. Pause sequence for 7 days
2. Resume after pause
3. No notification needed
```

**Question Reply** (needs info):
```
Triggers: "?", "how much", "details", "pricing"
Action:
1. Stop sequence
2. Tag as "Warm - Asking Questions"
3. Route to DMN agent for response
4. If DMN responds successfully → Hot lead
```

---

## Sequence Personalization

### Dynamic Variables

**Basic Tokens**:
```javascript
{{firstName}} // John
{{lastName}} // Doe
{{business}} // MetroFlex Gym
{{city}} // Brooklyn
{{state}} // NY
{{industry}} // Fitness
```

**Advanced Tokens** (from Virtual LPR):
```javascript
{{neighborhood}} // Park Slope
{{lprScore}} // 78
{{awarenessLevel}} // Solution Aware
{{pain_point_1}} // member retention
{{intent_signal}} // searched for "personal trainer"
{{distance_miles}} // 1.2
{{median_income}} // $87,500
{{competitor_reference}} // Other gyms in Brooklyn
```

**Conditional Logic**:
```javascript
{% if lprScore > 70 %}
  "You're exactly who we built this for."
{% elseif lprScore > 40 %}
  "I think you'd be a great fit for this."
{% else %}
  "Not sure if this is right for you, but..."
{% endif %}
```

---

## Analytics & Tracking

### Key Metrics Dashboard

**Sequence Performance**:
- Emails sent: 1,000
- Delivered: 965 (96.5%)
- Opened: 478 (49.5% open rate)
- Clicked: 81 (8.4% click rate)
- Replied: 52 (5.4% reply rate)
- Positive replies: 31 (3.2% conversion)

**Benchmarks** (Industry standards):
- Open rate: 45-55% = Excellent
- Click rate: 5-10% = Excellent
- Reply rate: 3-8% = Excellent
- Positive reply rate: 2-5% = Excellent

**Red Flags**:
- Open rate <30% = Bad subject lines or deliverability issue
- Click rate <2% = Weak offer or CTA
- Reply rate <1% = Copy not resonating

### A/B Test Results Tracking

```javascript
{
  test_id: "subject_line_test_001",
  variants: [
    {
      id: "A",
      subject: "{{firstName}}, your gym is bleeding $4,100/month",
      sent: 100,
      opened: 58,
      open_rate: 58.0,
      clicked: 11,
      click_rate: 19.0,
      replied: 6,
      reply_rate: 10.3
    },
    {
      id: "B",
      subject: "The $11,500 secret {{competitor_city}} gyms know",
      sent: 100,
      opened: 47,
      open_rate: 47.0,
      clicked: 8,
      click_rate: 17.0,
      replied: 4,
      reply_rate: 8.5
    },
    {
      id: "C",
      subject: "{{firstName}}, want 10 new PT clients by Dec 15?",
      sent: 100,
      opened: 51,
      open_rate: 51.0,
      clicked: 9,
      click_rate: 17.6,
      replied: 5,
      reply_rate: 9.8
    }
  ],
  winner: "A",
  confidence: 95,
  next_action: "Use Variant A for next 1000 sends"
}
```

---

## Integration with Virtual LPR

### Lead Scoring → Sequence Selection

**High Intent (LPR 70-100)**:
- Sequence: Aggressive 7-touch, 14-day
- Copy: Direct offer, urgency
- Follow-up: Daily for first 5 days

**Medium Intent (LPR 40-69)**:
- Sequence: Standard 7-touch, 21-day
- Copy: Value-first, education
- Follow-up: Every 3 days

**Low Intent (LPR 20-39)**:
- Sequence: Long nurture, 60-day
- Copy: Problem awareness only
- Follow-up: Weekly

**Awareness Level Adaptation**:
```javascript
if (awarenessLevel === 5) { // Most Aware
  sequence = "direct_offer_3_touch"
} else if (awarenessLevel >= 3) { // Solution/Product Aware
  sequence = "standard_7_touch"
} else { // Unaware/Problem Aware
  sequence = "education_10_touch"
}
```

---

## Skill Output Format

### Campaign Configuration

```javascript
{
  campaign_id: "pt_cert_nov_2025",
  platform: "instantly.ai",

  sequence: {
    name: "PT Certification 7-Touch",
    touches: 7,
    duration_days: 21,

    emails: [
      {
        day: 1,
        subject_variants: ["A", "B", "C"],
        body_variant: "pain_focused",
        send_time: "9:00 AM",
        timezone_adjusted: true
      },
      // ... 6 more touches
    ]
  },

  targeting: {
    lpr_score_min: 40,
    awareness_level: [2, 3, 4],
    industry: "fitness",
    location: "Brooklyn, NY",
    radius_miles: 10
  },

  personalization: {
    tokens: ["firstName", "business", "city", "neighborhood"],
    dynamic_content: true,
    conditional_logic: true
  },

  deliverability: {
    warm_up: true,
    daily_limit_per_account: 50,
    accounts_used: 5,
    total_daily_capacity: 250
  },

  tracking: {
    open_tracking: true,
    click_tracking: true,
    reply_detection: true,
    analytics_webhook: "https://circuitos.com/api/email-analytics"
  },

  ab_testing: {
    enabled: true,
    test_subject_lines: true,
    test_send_times: true,
    sample_size_per_variant: 100
  }
}
```

---

## Best Practices

### DO:
- Warm up new domains/accounts (4-week protocol)
- Personalize every email (5+ tokens minimum)
- A/B test continuously (subject lines, body, times)
- Monitor deliverability daily (bounce, spam rates)
- Reply within 2 minutes (use DMN agent)
- Stop sequences on reply (immediately)
- Use single CTA per email
- Send from real person's name (not "info@")

### DON'T:
- Send from freshly created domains (<30 days old)
- Exceed 50 emails/day per account
- Use spam trigger words ("free money", "guarantee", "act now")
- Send on weekends (lower engagement)
- Use generic copy (no personalization)
- Continue sequence after reply (annoying)
- Use multiple CTAs (confusing)
- Send from "noreply@" addresses

---

## Skill Usage Checklist

- [ ] Instantly.ai account connected
- [ ] Domain DNS configured (SPF, DKIM, DMARC)
- [ ] Warm-up protocol started (4 weeks)
- [ ] Lead list imported from Virtual LPR
- [ ] Sequence selected based on LPR score
- [ ] Copy generated from ai-copywriting-agent
- [ ] Personalization tokens populated
- [ ] A/B test variants created
- [ ] Send times optimized (timezone adjusted)
- [ ] Reply detection rules configured
- [ ] Analytics tracking enabled
- [ ] Daily monitoring scheduled

---

**Created**: November 13, 2025
**Platform**: Instantly.ai Integration
**Status**: Production-Ready
**Priority**: CRITICAL - Fills Gap #2
