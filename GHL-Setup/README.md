# GoHighLevel Complete Setup Guide
## Two Systems Available

**Last Updated:** November 1, 2025

---

## 🔥 **NEW: Dual-Path Lead System** (Recommended)

**Version:** 2.0.0 | **Setup Time:** 2-3 hours | **Cost:** ~$0.03/lead

### Quick Start

**Interactive Guide (Recommended):**
```bash
open ../setup-guide.html
```
👉 **[Open Interactive Guide](file:///home/user/Circuitos/setup-guide.html)**

**Or use command line:**
```bash
cd ..
npm install
echo "ANTHROPIC_API_KEY=your-key-here" > .env
vercel dev
./test-system.sh
```

### What's Different

| Feature | Dual-Path (NEW) | AI Employees (Legacy) |
|---------|-----------------|----------------------|
| **Architecture** | Vercel serverless APIs | GHL AI Employees |
| **Cost per lead** | ~$0.03 | $97/mo unlimited |
| **Setup** | 2-3 hours | 4-6 hours |
| **Frameworks** | 4 (Brunson, Schwartz, Miller, Hormozi) | 3 frameworks |
| **Testing** | Automated test suite | Manual |
| **Lead Routing** | Dual-path (cold vs warm) | Single path |
| **Deployment** | Production-ready | Requires GHL config |

### Documentation

- **[setup-guide.html](../setup-guide.html)** - Interactive web guide
- **[README-DUAL-PATH-SYSTEM.md](../README-DUAL-PATH-SYSTEM.md)** - System overview
- **[QUICK-REFERENCE-CARD.md](../QUICK-REFERENCE-CARD.md)** - Commands cheat sheet
- **[GHL-INTERACTIVE-SETUP-GUIDE.md](../GHL-INTERACTIVE-SETUP-GUIDE.md)** - Detailed GHL integration

**Recommended:** Use the Dual-Path system for new deployments.

---

## 📦 **LEGACY: AI Employees System**

**Version:** 1.0.0
**Date:** October 25, 2025
**Plan Required:** GHL Unlimited + $97 AI Unlimited Add-On

### 📋 PREREQUISITES CHECKLIST

Before you begin, ensure you have:

### GoHighLevel Account
- [ ] GHL Account on Unlimited tier or higher
- [ ] $97/month AI Unlimited add-on enabled
- [ ] Admin access to create AI employees
- [ ] Admin access to create workflows
- [ ] Admin access to create custom fields

**How to verify:**
1. Log in to GHL
2. Go to Settings → Billing
3. Confirm "AI Unlimited" is active
4. Should show: "Unlimited AI Employee Conversations"

### Integration Accounts (Optional - Can add later)
- [ ] Instantly.ai account ($37/mo) - For cold email
- [ ] Claude API key (for testing) - Can use GHL's built-in AI first
- [ ] Google My Business access - For review monitoring
- [ ] Twilio account (if using SMS) - Can use GHL SMS

---

## 🎯 SETUP OVERVIEW

**Total Setup Time:** 2-4 hours (first time)
**Difficulty:** Intermediate
**Result:** Fully automated AI-powered sales system

### What You'll Build:

1. **7 AI Employees** (30-45 min)
   - Lead Scorer
   - Master Copywriter
   - Email Campaign Manager
   - Channel Router
   - Reputation Guardian
   - Content Creator
   - Search Optimizer

2. **5 Core Workflows** (45-60 min)
   - New Lead Processor
   - High-Intent Cold Email Sequence
   - Omnichannel Follow-Up
   - Review Response Handler
   - Content Publishing

3. **200+ Custom Fields** (15-20 min)
   - Virtual LPR attributes
   - Scoring data
   - Engagement history

4. **Webhooks & Integrations** (20-30 min)
   - Instantly.ai webhook
   - GMB review webhook
   - External API connections

---

## 📁 FILE STRUCTURE

All GHL configuration files are in this directory:

```
GHL-Setup/
├── README.md (this file)
├── AI-Employees/
│   ├── 01-Lead-Scorer.md
│   ├── 02-Master-Copywriter.md
│   ├── 03-Email-Campaign-Manager.md
│   ├── 04-Channel-Router.md
│   ├── 05-Reputation-Guardian.md
│   ├── 06-Content-Creator.md
│   └── 07-Search-Optimizer.md
├── Workflows/
│   ├── 01-New-Lead-Processor.md
│   ├── 02-High-Intent-Cold-Email.md
│   ├── 03-Omnichannel-Follow-Up.md
│   ├── 04-Review-Response-Handler.md
│   └── 05-Content-Publishing.md
├── Custom-Fields/
│   ├── custom-fields-schema.csv
│   ├── custom-fields-import-guide.md
│   └── field-descriptions.md
├── Webhooks/
│   ├── instantly-webhook-setup.md
│   ├── gmb-webhook-setup.md
│   └── webhook-testing-guide.md
└── Testing/
    ├── test-lead-data.json
    ├── testing-checklist.md
    └── troubleshooting-guide.md
```

---

## 🚀 QUICK START (Step-by-Step)

### Phase 1: Preparation (15 min)

#### Step 1: Verify GHL AI Unlimited
```
1. Log in to GoHighLevel
2. Settings → Billing
3. Verify: "AI Unlimited" shows "Active"
4. If not active:
   - Click "Add-ons"
   - Find "AI Unlimited - $97/mo"
   - Click "Enable"
   - Confirm billing
```

#### Step 2: Gather Test Business Info
You'll need this for first setup:
- Business name
- Industry/category
- Address (city, state, zip)
- Target customer profile
- Phone number
- Email address

**Example:**
- Name: MetroFlex Gym
- Industry: Fitness/Gym
- Address: 123 5th Ave, Brooklyn, NY 11215
- Target: Professionals age 28-45 in Park Slope
- Phone: (555) 123-4567
- Email: info@metroflexgym.com

#### Step 3: Create Sub-Account (If Agency)
If you're on Agency plan:
```
1. Settings → My Agency
2. Click "Add Location"
3. Enter business details
4. Save
5. Switch to new sub-account
```

If you're on Unlimited (single location):
```
Skip this step - work in your main account
```

---

### Phase 2: Custom Fields (20 min)

**Why First?** AI employees need these fields to store data.

#### Import Custom Fields

**Option A: Manual Import (Recommended First Time)**
1. Go to: Settings → Custom Fields
2. Click: "+ New Custom Field"
3. Use this template for each field:

**CORE FIELDS (Add these first):**

| Field Name | Type | Group | Description |
|------------|------|-------|-------------|
| `lpr_score` | Number | Scoring | Virtual LPR Score (0-100) |
| `fit_score` | Number | Scoring | Fit component (0-40) |
| `intent_score` | Number | Scoring | Intent component (0-40) |
| `timing_score` | Number | Scoring | Timing component (0-20) |
| `awareness_level` | Dropdown | Scoring | Unaware, Problem Aware, Solution Aware, Product Aware, Most Aware |
| `distance_miles` | Number | Location | Distance from business (miles) |
| `neighborhood` | Text | Location | Neighborhood name |
| `median_income` | Number | Demographics | Census median income for ZIP |
| `intent_signal` | Text | Behavior | Primary intent signal (called, visited, searched) |
| `last_action_date` | Date | Behavior | Most recent engagement |
| `email_variant_tested` | Dropdown | Campaigns | A, B, C |
| `sequence_status` | Dropdown | Campaigns | Active, Paused, Completed, Replied |
| `next_channel` | Dropdown | Campaigns | email, sms, linkedin, call |

**Quick Add Instructions:**
```
For each field:
1. Click "+ New Custom Field"
2. Field Name: [from table]
3. Field Type: [from table]
4. Group: [from table] (create new group if needed)
5. Description: [from table]
6. Click "Save"
7. Repeat for all fields
```

**Option B: Bulk Import (Advanced)**
1. Download: `Custom-Fields/custom-fields-schema.csv`
2. Go to: Settings → Custom Fields
3. Click: "Import" (if available)
4. Upload CSV
5. Map columns
6. Import

**Full field list:** See `Custom-Fields/field-descriptions.md` for all 200+ fields

---

### Phase 3: AI Employees (45 min)

**Create in this order** (each depends on previous):

#### 1. Lead Scorer (10 min)

**Navigation:**
```
Settings → AI & Automations → AI Employees → + New AI Employee
```

**Configuration:**
- Name: `Lead Scorer`
- Description: `Scores leads 0-100 using BANT/MEDDIC/CHAMP frameworks`
- Model: `GPT-4` (or best available in GHL)
- Temperature: `0.3` (lower = more consistent)

**System Prompt:**
```
Copy from: AI-Employees/01-Lead-Scorer.md
```

**Input Variables:**
- `{{contact.first_name}}`
- `{{contact.last_name}}`
- `{{contact.email}}`
- `{{contact.phone}}`
- `{{contact.address}}`
- `{{contact.custom_fields}}`

**Output Format:**
- JSON with: `{ score, fitScore, intentScore, timingScore, breakdown, confidence }`

**Save AI Employee**

---

#### 2. Master Copywriter (10 min)

**Configuration:**
- Name: `Master Copywriter`
- Description: `Generates world-class copy using Brunson/Schwartz/Hormozi frameworks`
- Model: `GPT-4`
- Temperature: `0.7` (higher = more creative)

**System Prompt:**
```
Copy from: AI-Employees/02-Master-Copywriter.md
```

**Input Variables:**
- `{{contact.first_name}}`
- `{{contact.custom_fields.lpr_score}}`
- `{{contact.custom_fields.awareness_level}}`
- `{{channel}}` (email, sms, linkedin)
- `{{business_name}}`
- `{{business_category}}`

**Output Format:**
- JSON with: `{ subject, body, cta, variant }`

---

#### 3-7. Repeat for Remaining Employees

Follow same process for:
- Email Campaign Manager (`AI-Employees/03-Email-Campaign-Manager.md`)
- Channel Router (`AI-Employees/04-Channel-Router.md`)
- Reputation Guardian (`AI-Employees/05-Reputation-Guardian.md`)
- Content Creator (`AI-Employees/06-Content-Creator.md`)
- Search Optimizer (`AI-Employees/07-Search-Optimizer.md`)

**Time estimate:** 5-7 minutes each

---

### Phase 4: Workflows (60 min)

#### Workflow 1: New Lead Processor (15 min)

**Purpose:** Score new leads and route to appropriate sequence

**Create Workflow:**
```
Automations → Workflows → + New Workflow
```

**Settings:**
- Name: `New Lead Processor`
- Trigger: `Contact Created` OR `Tag Added: "vLPR"`
- Description: `Scores leads using Lead Scorer AI employee and routes to sequence`

**Steps:**
```
See detailed steps in: Workflows/01-New-Lead-Processor.md
```

**Quick Overview:**
1. Trigger: Contact Created
2. Wait: 1 minute (let data settle)
3. AI Action: Call "Lead Scorer" employee
4. Update Contact: Set custom fields (lpr_score, fit_score, etc.)
5. Condition: IF lpr_score >= 70
   - YES → Add tag "High Intent" → Start "Cold Email Sequence"
   - NO → Check if >= 40
     - YES → Add tag "Medium Intent" → Start "Nurture Sequence"
     - NO → Add tag "Low Intent" → Start "Education Sequence"

---

#### Workflow 2: High-Intent Cold Email (20 min)

**Purpose:** 5-touch cold email sequence for hot leads

**Create Workflow:**
```
Automations → Workflows → + New Workflow
```

**Settings:**
- Name: `High-Intent Cold Email Sequence`
- Trigger: `Tag Added: "High Intent"`
- Description: `Aggressive 5-touch email sequence with Instantly integration`

**Steps:**
```
See detailed steps in: Workflows/02-High-Intent-Cold-Email.md
```

**Quick Overview:**
1. Trigger: Tag "High Intent" added
2. AI Action: Call "Master Copywriter" (channel: email, variant: A)
3. Store copy in custom fields
4. Wait: Check if Instantly connected
   - YES → Send via Instantly API
   - NO → Send via GHL email
5. Wait: 48 hours
6. Condition: Check if replied
   - YES → End workflow, mark "Replied"
   - NO → Continue to Follow-Up #2
7. Repeat for touches 2-5 with increasing delays

---

#### Workflow 3-5: Build Remaining Workflows

- Omnichannel Follow-Up (`Workflows/03-Omnichannel-Follow-Up.md`)
- Review Response Handler (`Workflows/04-Review-Response-Handler.md`)
- Content Publishing (`Workflows/05-Content-Publishing.md`)

**Time estimate:** 10-15 min each

---

### Phase 5: Webhooks & Integrations (30 min)

#### Instantly.ai Webhook (10 min)

**Purpose:** Receive reply notifications from Instantly

**Setup:**
```
See: Webhooks/instantly-webhook-setup.md
```

**Quick Steps:**
1. Settings → Integrations → Webhooks → + New Webhook
2. Name: `Instantly Reply Webhook`
3. URL: Auto-generated by GHL
4. Copy webhook URL
5. In Instantly.ai:
   - Settings → Integrations → Webhooks
   - Paste GHL webhook URL
   - Select events: "Email Reply"
   - Save

**Test:**
1. Send test email via Instantly
2. Reply to it
3. Check GHL → Contacts → Activity
4. Should see: "Webhook received: Instantly Reply"

---

#### Google My Business Webhook (10 min)

**Purpose:** Receive new review notifications

**Setup:**
```
See: Webhooks/gmb-webhook-setup.md
```

**Note:** GMB doesn't have native webhooks, so we'll use polling:
1. Create workflow: "Check GMB Reviews"
2. Trigger: Recurring (every 4 hours)
3. Action: Call external API (GMB API)
4. Parse response, find new reviews
5. If new review found → Trigger "Review Response Handler"

---

### Phase 6: Testing (30 min)

#### Test Lead Scoring

**Use test data:**
```
See: Testing/test-lead-data.json
```

**Steps:**
1. Contacts → + New Contact
2. Fill in test data:
   - First Name: John
   - Last Name: Doe
   - Email: john.doe.test@example.com
   - Phone: (555) 123-4567
   - Add Tag: "vLPR"
3. Watch workflow execute
4. Check Contact → Custom Fields
5. Verify: `lpr_score` populated (should be ~75-85 for test data)

**Expected Result:**
- Score calculated within 10 seconds
- Contact tagged "High Intent"
- Cold email sequence started

---

#### Test Copy Generation

**Steps:**
1. Find test contact from above
2. Manually trigger workflow: "High-Intent Cold Email"
3. Wait 30 seconds
4. Check Contact → Custom Fields
5. Verify: `email_variant_tested` = "A"
6. Check Contact → Activities
7. Verify: Email sent with personalized copy

**Review Generated Copy:**
- Should include contact's first name
- Should reference their location/neighborhood
- Should have clear Hook-Story-Offer structure
- Should match awareness level

---

#### Full System Test

**Complete testing checklist:**
```
See: Testing/testing-checklist.md
```

**Key tests:**
- [ ] New lead scored correctly
- [ ] High-intent leads get cold email
- [ ] Medium-intent leads get nurture sequence
- [ ] Low-intent leads get education sequence
- [ ] Email replies stop sequences
- [ ] Review responses generated correctly
- [ ] All custom fields populated

---

## 🎯 SUCCESS METRICS

After setup, track these in GHL:

### Week 1 (Testing)
- [ ] 5+ test contacts processed
- [ ] All workflows executing without errors
- [ ] AI employees responding in <30 seconds
- [ ] Custom fields populating correctly

### Week 2-4 (Beta)
- [ ] 10-50 real leads processed
- [ ] Lead scoring accuracy: >70% (compare predicted vs actual)
- [ ] Email deliverability: >95%
- [ ] Response rate: >5%

### Month 2+ (Production)
- [ ] Lead scoring F1 score: >0.75
- [ ] Email open rate: >45%
- [ ] Email reply rate: >8%
- [ ] Review response time: <4 hours
- [ ] Overall conversion rate: >3%

---

## 🆘 TROUBLESHOOTING

### AI Employee Not Responding

**Symptoms:**
- Workflow shows "Waiting for AI response"
- Stuck for >2 minutes

**Solutions:**
1. Check AI Unlimited is active (Settings → Billing)
2. Check system prompt length (<8,000 tokens recommended)
3. Try reducing temperature
4. Check input variables are populated
5. Test AI employee directly (AI Employees → Test)

---

### Workflow Not Triggering

**Symptoms:**
- Contact created but workflow doesn't start

**Solutions:**
1. Check trigger conditions (tag must match exactly)
2. Check workflow is published (not draft)
3. Check contact meets trigger criteria
4. View workflow history (Workflows → [Name] → History)

---

### Custom Fields Not Populating

**Symptoms:**
- AI employee runs but fields stay empty

**Solutions:**
1. Verify field names match exactly (case-sensitive)
2. Check "Update Contact" action in workflow
3. Verify AI output format is JSON
4. Check field type matches (Number vs Text)
5. Test with hardcoded value first

---

### More Issues?
See: `Testing/troubleshooting-guide.md`

---

## 📊 OPTIMIZATION TIPS

### After 1 Week of Use

**Review AI Employee Performance:**
1. AI Employees → [Name] → Analytics
2. Check: Avg response time (<30sec good, <10sec excellent)
3. Check: Error rate (<1% good)
4. Review: Sample conversations
5. Refine: System prompts based on output quality

**Review Workflow Performance:**
1. Workflows → [Name] → Analytics
2. Check: Completion rate (>95% good)
3. Check: Avg execution time
4. Identify: Bottlenecks (slow steps)
5. Optimize: Remove unnecessary waits

**Review Lead Scoring Accuracy:**
1. Export: Leads scored in past week
2. Check: Which scored >70 actually converted?
3. Calculate: Precision (% of high scores that converted)
4. Calculate: Recall (% of conversions that were high scored)
5. Adjust: Scoring thresholds if needed

---

## 💰 COST TRACKING

**With $97 AI Unlimited:**

**Month 1:**
- GHL Unlimited: (existing)
- AI Unlimited: $97
- Instantly.ai: $37
- **Total: $134/mo**

**Month 2+:**
- Same as Month 1
- **Average: $134/mo**

**Compare to traditional:**
- Claude API (1000 leads/day): ~$1,500/mo
- **Savings: $1,366/mo**

---

## 🚀 WHAT'S NEXT?

After completing this setup:

1. **Week 1:** Test with dummy data, refine prompts
2. **Week 2:** Onboard first real business (beta)
3. **Week 3:** Collect feedback, iterate
4. **Week 4:** Replicate to 5 businesses
5. **Month 2:** Scale to 20 businesses
6. **Month 3:** Scale to 50 businesses

**Each new business = 30 min setup** (once you have templates)

---

## 📞 SUPPORT

**Documentation:**
- All AI employee configs: `/AI-Employees/`
- All workflow configs: `/Workflows/`
- Custom fields: `/Custom-Fields/`
- Testing guides: `/Testing/`

**Troubleshooting:**
- See: `Testing/troubleshooting-guide.md`
- Common errors and solutions

**Updates:**
- This guide will be updated as GHL releases new features
- Check for updates monthly

---

## ✅ SETUP COMPLETE CHECKLIST

Before going live, confirm:

- [ ] GHL AI Unlimited active ($97/mo)
- [ ] 7 AI employees created and tested
- [ ] 5 core workflows built and published
- [ ] 200+ custom fields added
- [ ] Webhooks configured (Instantly, GMB)
- [ ] Test leads processed successfully
- [ ] All metrics tracking in place
- [ ] Team trained on system (if applicable)

**Estimated setup time: 2-4 hours**
**Expected ROI: $1,366/month savings vs traditional Claude API**

---

**© 2025 CircuitOS™**
**Optimized for GoHighLevel $97 AI Unlimited Plan**
