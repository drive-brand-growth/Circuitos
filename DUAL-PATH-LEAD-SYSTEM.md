# Dual-Path Lead System Documentation
## Path 1: Cold Emails (Instantly.ai) vs Path 2: Website Traffic (Virtual LPR)

**Version:** 1.0.0
**Date:** November 1, 2025
**Status:** Production Ready

---

## 🎯 Overview

Your lead system now has **TWO distinct paths** based on lead source:

### Path 1: **Cold Emails** (Instantly.ai)
- Leads from outbound cold email campaigns
- Qualify FIRST via Instantly.ai
- Hand-off to GHL only if qualified
- Respectful, humble tone (they don't know you yet)

### Path 2: **Website Traffic** (Virtual LPR)
- Leads from website, GMB, organic search
- Validate immediately with Virtual LPR
- Engage aggressively (they found YOU)
- Confident, direct tone (they already know you)

---

## 🔀 Complete Flow Diagram

```
                    NEW LEAD ENTERS
                          │
                          ▼
              ┌───────────────────────┐
              │   LEAD ROUTER API     │
              │  /api/lead-router.js  │
              │                       │
              │  Detects source:      │
              │  - Instantly tag?     │
              │  - Virtual LPR data?  │
              │  - Form submission?   │
              │  - GA4 tracking?      │
              └───────────┬───────────┘
                          │
            ┌─────────────┴─────────────┐
            │                           │
    ┌───────▼────────┐         ┌───────▼────────┐
    │  PATH 1:       │         │  PATH 2:       │
    │  COLD EMAIL    │         │  WEBSITE       │
    │  (Instantly)   │         │  TRAFFIC       │
    └───────┬────────┘         └───────┬────────┘
            │                           │
            ▼                           ▼
┌──────────────────────┐    ┌──────────────────────┐
│ INSTANTLY.AI         │    │ VIRTUAL LPR API      │
│ - Qualification      │    │ - Distance check     │
│ - Reply analysis     │    │ - Demographics       │
│ - Intent scoring     │    │ - Census data        │
└──────────┬───────────┘    └──────────┬───────────┘
           │                           │
           │                           │
    IF QUALIFIED                IF VALIDATED
           │                           │
           │                           │
           └─────────┬─────────────────┘
                     │
                     ▼
            ┌────────────────┐
            │  LEAD SCORER   │
            │ BANT/MEDDIC    │
            │ Awareness Level│
            └────────┬───────┘
                     │
                     ▼
            ┌────────────────┐
            │ MASTER         │
            │ COPYWRITER     │◄────── Routes framework based on:
            │                │        - Awareness (Schwartz)
            │ Routes between:│        - Demographics
            │ - Brunson      │        - Lead source
            │ - Schwartz     │        - Psychographics
            │ - Hormozi      │
            └────────┬───────┘
                     │
                     ▼
            ┌────────────────┐
            │ EMAIL CAMPAIGN │
            │ MANAGER        │
            │ (Instantly.ai) │
            └────────┬───────┘
                     │
                     ▼
            ┌────────────────┐
            │ CHANNEL ROUTER │
            │ Omnichannel    │
            │ Email→LinkedIn │
            │ →SMS→Call      │
            └────────────────┘
```

---

## 📋 PATH 1: Cold Emails (Instantly.ai)

### Workflow Name: "Cold Email Reply Handler"

### Trigger:
```
Webhook Received from Instantly.ai
URL: https://your-project.vercel.app/api/instantly-webhook
```

---

### Step-by-Step Flow:

#### **STEP 1: Instantly.ai Sends Webhook**

**When:**
- Lead replies to cold email
- Lead clicks link in email
- Lead opens email (tracked)

**Webhook Payload Example:**
```json
{
  "event_type": "reply",
  "campaign_id": "abc123",
  "campaign_name": "MetroFlex Q4 Campaign",
  "lead_email": "john@example.com",
  "lead_first_name": "John",
  "lead_last_name": "Doe",
  "reply_text": "Yes, interested. Tell me more about your gym.",
  "replied_at": "2025-11-01T10:30:00Z"
}
```

---

#### **STEP 2: Qualification (Automatic)**

**Our API analyzes reply intent:**

```javascript
// Positive signals:
"interested", "tell me more", "yes", "how much", "pricing", questions

// Negative signals:
"not interested", "remove me", "unsubscribe", "stop"

// Neutral:
Short replies ("OK", "Thanks"), no clear intent
```

**Qualification Results:**
- **Positive/Curious (70-90 score)** → Qualified ✅ → Send to GHL
- **Negative (0 score)** → Not qualified ❌ → Archive, add DNC tag
- **Neutral (30 score)** → Monitor only, continue Instantly campaign

---

#### **STEP 3: Create/Update Contact in GHL**

**If Qualified:**

**Action:** Create Contact (or update if exists)

**Data to populate:**
```json
{
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "tags": [
    "Lead Source - Cold Email",
    "Instantly Campaign - MetroFlex Q4",
    "Reply Intent - Positive"
  ],
  "custom_fields": {
    "lead_source": "cold_email",
    "instantly_campaign_id": "abc123",
    "instantly_reply_text": "Yes, interested...",
    "instantly_qualification": "positive",
    "instantly_qualification_score": 85,
    "lead_temperature": "cold"
  }
}
```

---

#### **STEP 4: Route to Lead Scorer**

**Trigger:** Lead Scorer workflow

**Input:**
- Contact data from Step 3
- Source = "cold_email"

**Output:**
- LPR Score (0-100)
- Awareness Level (Schwartz: Unaware → Most Aware)
- Fit, Intent, Timing scores

---

#### **STEP 5: Master Copywriter (Cold Email Mode)**

**Endpoint:** POST `/api/copywriter`

**Request:**
```json
{
  "contact": {
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "custom_fields": {
      "lpr_score": 75,
      "awareness_level": "Solution Aware"
    }
  },
  "channel": "email",
  "awareness_level": "Solution Aware",
  "lead_source": "cold_email",  // ← KEY FIELD
  "business": {
    "name": "MetroFlex Gym",
    "city": "Arlington",
    "state": "Texas"
  },
  "touch_number": 1
}
```

**AI Behavior (Cold Email Mode):**
```
✅ Acknowledges they replied to cold email
✅ Builds credibility fast (social proof, numbers)
✅ Respectful, humble tone ("Thanks for replying...")
✅ Assumes they're comparing options
✅ Makes next step EASY (low friction)

❌ Doesn't act overly familiar
❌ Doesn't assume they know who you are
❌ Not aggressive or pushy
```

**Example Output:**
```
Subject: John - Quick intro to MetroFlex

John,

Thanks for replying! Quick intro:

We're a hardcore powerlifting gym in Arlington (2.3 miles from you).
No lunk alarms, no cardio bunnies - just serious lifters.

47 guys who pull 500+ train here. Last month, 3 members hit PRs at
USAPL Raw Nationals.

First week free - see if the vibe fits.

[Book Your Free Week]

- Jake, Head Coach
MetroFlex Arlington

P.S. Open 24/7. Deadlift at 2am if that's your thing.
```

---

#### **STEP 6: Send Email via Instantly.ai**

**Action:** Email Campaign Manager sends follow-up

**Integration:** Instantly.ai API

**Sequence:**
- Touch 1: Reply acknowledgment + intro (generated by Copywriter)
- Touch 2 (48 hours later): Social proof + transformation stories
- Touch 3 (5 days later): Limited offer + urgency

---

#### **STEP 7: Channel Router Monitors Engagement**

**If:** Email opened + clicked → Route to LinkedIn
**If:** No response after 3 touches → Archive for 90 days
**If:** Positive reply → Schedule call immediately

---

## 📋 PATH 2: Website Traffic (Virtual LPR)

### Workflow Name: "Virtual LPR - Lead Validator"

### Trigger:
```
- Contact Created (from website form)
- Tag Added: "vLPR"
- GMB action (direction clicked, phone call)
- GA4 webhook (website visitor tracked)
```

---

### Step-by-Step Flow:

#### **STEP 1: Virtual LPR Validation**

**Endpoint:** POST `/api/virtual-lpr`

**Request:**
```json
{
  "signal_type": "website_visit",
  "signal_data": {
    "page_url": "/pricing",
    "session_duration": 180,
    "location": {
      "city": "Arlington",
      "zip_code": "76011",
      "lat": 32.7450,
      "lng": -97.1180
    },
    "ip_address": "8.8.8.8"
  },
  "business": {
    "name": "MetroFlex Gym",
    "lat": 32.7357,
    "lng": -97.1081,
    "target_radius_miles": 10
  }
}
```

**AI Validation:**
- Calculates distance (Google Maps or Haversine)
- Fetches Census demographics (income, age)
- Scores signal strength (0-100)
- Determines if qualified

**Output:**
```json
{
  "qualified": true,
  "signal_strength": 85,
  "predicted_lpr_score": 78,
  "enrichment_summary": {
    "distance_miles": 1.8,
    "median_income": 65320,
    "median_age": 33
  }
}
```

---

#### **STEP 2: Create Contact in GHL**

**Data populated:**
```json
{
  "tags": [
    "Lead Source - Website",
    "Virtual LPR - High Intent",
    "Within 5 miles"
  ],
  "custom_fields": {
    "lead_source": "website_traffic",
    "vlpr_source": "website_visit",
    "vlpr_score": 78,
    "distance_miles": 1.8,
    "median_income": 65320,
    "lead_temperature": "warm"
  }
}
```

---

#### **STEP 3: Lead Scorer**

**Same as Path 1** - runs BANT/MEDDIC scoring

---

#### **STEP 4: Master Copywriter (Website Traffic Mode)**

**Request:**
```json
{
  "contact": {
    "first_name": "Sarah",
    "custom_fields": {
      "lpr_score": 82,
      "distance_miles": 1.8
    }
  },
  "channel": "email",
  "awareness_level": "Product Aware",
  "lead_source": "website_traffic",  // ← KEY FIELD
  "business": { ... }
}
```

**AI Behavior (Website Traffic Mode):**
```
✅ Leverages their existing knowledge
✅ References what they viewed ("Saw you checked pricing...")
✅ Confident, direct tone
✅ Higher urgency (they're shopping NOW)
✅ More aggressive CTAs

❌ Doesn't over-explain who you are
❌ Not overly cautious or humble
```

**Example Output:**
```
Subject: Sarah - saw you checking out MetroFlex pricing

Sarah,

Noticed you were on our site looking at pricing. You're 1.8 miles away.

Quick answer: $60/mo, no contract, 24/7 access.

But here's what makes us different:

→ 47 guys who pull 500+ train here (you'll level up FAST)
→ Last month: 3 members hit PRs at nationals
→ Actual powerlifting equipment (Rogue, Eleiko, not machines)

First week free. Train with us Monday - see if you fit.

[Book Free Week - 2 spots left this week]

You ready?

- Jake
MetroFlex Arlington

P.S. If you're thinking about competing, we've got 4 people prepping
for USAPL nationals. Jump in now.
```

---

#### **STEP 5: Send via Email Campaign Manager**

**Same as Path 1** - uses Instantly.ai

---

#### **STEP 6: Channel Router**

**Same as Path 1** - omnichannel follow-up

---

## 🔧 GHL Workflow Setup

### Workflow 1: "Cold Email Reply Handler" (Path 1)

```
TRIGGER: Webhook Received
URL: /api/instantly-webhook

↓

STEP 1: Condition
IF {{webhook_response.qualified}} = true

↓ YES

STEP 2: Create/Update Contact
Email: {{webhook_response.ghl_action.contact.email}}
Tags: {{webhook_response.ghl_action.contact.tags}}
Custom Fields: {{webhook_response.ghl_action.contact.custom_fields}}

↓

STEP 3: Send Webhook (Lead Scorer)
URL: /api/lead-scorer
Body: { contact: {...}, source: "cold_email" }

↓

STEP 4: Send Webhook (Master Copywriter)
URL: /api/copywriter
Body: {
  contact: {...},
  channel: "email",
  awareness_level: "{{contact.custom_fields.awareness_level}}",
  lead_source: "cold_email",
  business: {...}
}

↓

STEP 5: Update Contact
Custom Fields:
- email_variant_a_subject: {{webhook_response.copy.variants.0.subject}}
- email_variant_a_body: {{webhook_response.copy.variants.0.body}}
- recommended_variant: {{webhook_response.copy.recommended_variant}}

↓

STEP 6: Send Email (Instantly.ai)
Subject: {{contact.custom_fields.email_variant_a_subject}}
Body: {{contact.custom_fields.email_variant_a_body}}

↓

STEP 7: Wait 48 hours

↓

STEP 8: Trigger Workflow: "Channel Router"
```

---

### Workflow 2: "Virtual LPR - Lead Validator" (Path 2)

```
TRIGGER: Contact Created OR Tag Added: "vLPR"

↓

STEP 1: Send Webhook (Virtual LPR)
URL: /api/virtual-lpr
Body: { signal_type, signal_data, business }

↓

STEP 2: Condition
IF {{webhook_response.qualified}} = true

↓ YES

STEP 3: Update Contact
Tags: {{webhook_response.detection.initial_tags}}
Custom Fields: {
  vlpr_score: {{webhook_response.ghl_integration.custom_fields.vlpr_score}},
  distance_miles: {{webhook_response.ghl_integration.custom_fields.distance_miles}},
  median_income: {{webhook_response.ghl_integration.custom_fields.median_income}}
}

↓

STEP 4: Send Webhook (Lead Scorer)
URL: /api/lead-scorer
Body: { contact: {...}, source: "website_traffic" }

↓

STEP 5: Send Webhook (Master Copywriter)
URL: /api/copywriter
Body: {
  contact: {...},
  channel: "email",
  awareness_level: "{{contact.custom_fields.awareness_level}}",
  lead_source: "website_traffic",  // ← IMPORTANT
  business: {...}
}

↓

STEP 6-8: Same as Path 1
```

---

## 📊 Key Differences Summary

| Aspect | Path 1: Cold Email | Path 2: Website Traffic |
|--------|-------------------|------------------------|
| **Lead Quality** | Unknown (cold) | Higher (they found you) |
| **Qualification** | Via Instantly.ai first | Via Virtual LPR |
| **Copy Tone** | Humble, respectful | Confident, direct |
| **Speed** | Slower, gentle nurture | Faster, aggressive |
| **Acknowledgment** | "Thanks for replying..." | "Saw you on our site..." |
| **Credibility** | Build from scratch | Leverage existing |
| **CTA** | Low friction, easy | Urgent, specific |
| **Example** | "Quick intro: We're..." | "You're 1.8 miles away..." |

---

## 🚀 Deployment Checklist

### API Endpoints:
- [ ] `/api/lead-router.js` - Deployed
- [ ] `/api/copywriter.js` - Deployed
- [ ] `/api/instantly-webhook.js` - Deployed
- [ ] `/api/virtual-lpr.js` - Deployed (already done)
- [ ] Environment variables set (ANTHROPIC_API_KEY)

### GHL Workflows:
- [ ] "Cold Email Reply Handler" - Created
- [ ] "Virtual LPR - Lead Validator" - Created
- [ ] "Lead Scorer" - Created
- [ ] "Channel Router" - Created

### Instantly.ai:
- [ ] Webhook configured to point to `/api/instantly-webhook`
- [ ] Test campaign running
- [ ] Reply received and processed successfully

### GHL Custom Fields:
- [ ] `lead_source` (Dropdown: cold_email, website_traffic)
- [ ] `lead_temperature` (Dropdown: cold, warm, hot)
- [ ] `instantly_campaign_id` (Text)
- [ ] `instantly_qualification` (Dropdown: positive, negative, neutral)
- [ ] `instantly_qualification_score` (Number)
- [ ] `vlpr_source` (Text)
- [ ] `vlpr_score` (Number)

---

## 🧪 Testing

### Test Path 1 (Cold Email):
1. Send test email via Instantly.ai
2. Reply with "Yes, interested"
3. Verify webhook received at `/api/instantly-webhook`
4. Check GHL contact created with correct tags
5. Verify Master Copywriter used "cold_email" tone
6. Check copy says "Thanks for replying..."

### Test Path 2 (Website Traffic):
1. Submit website form OR add tag "vLPR" to contact
2. Verify Virtual LPR validation runs
3. Check GHL contact has distance/demographics
4. Verify Master Copywriter used "website_traffic" tone
5. Check copy says "Saw you on our site..."

---

## ✅ Success Criteria

**Path 1 (Cold Email):**
- Instantly.ai replies qualify correctly (>80% accuracy)
- Only positive/curious replies go to GHL
- Copy tone is respectful, not pushy
- Conversion rate: 3-5% (reply → booking)

**Path 2 (Website Traffic):**
- Virtual LPR validates correctly (>90% accuracy)
- Only leads within target radius get engaged
- Copy tone is confident, direct
- Conversion rate: 8-12% (visitor → booking)

---

**© 2025 CircuitOS™**
**Dual-Path Lead System - Production Ready**
