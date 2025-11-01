# GoHighLevel Interactive Setup Guide
**Dual-Path Lead System - Complete GHL Integration**

---

## 🎯 Overview

This guide walks you through setting up the Dual-Path Lead System inside GoHighLevel with exact click-by-click instructions.

**Time to Complete:** 60 minutes
**Difficulty:** Beginner-friendly
**Prerequisites:** GHL account, Vercel deployment complete

---

## 📋 Pre-Flight Checklist

Before starting, make sure you have:

- ✅ Your Vercel production URL (e.g., `https://your-project.vercel.app`)
- ✅ GHL admin access
- ✅ Test completed successfully on Vercel
- ✅ Claude API key configured in Vercel environment variables

---

## Part 1: Create Custom Fields (10 minutes)

### Step 1: Navigate to Custom Fields

1. Log in to GoHighLevel
2. Click **Settings** (gear icon in left sidebar)
3. Click **Custom Fields** in the settings menu
4. Click **+ Add Custom Field** button (top right)

### Step 2: Create Field #1 - lead_source

**Click "+ Add Custom Field" and enter:**

```
Field Name: lead_source
Field Type: Text (single line)
Placeholder: cold_email or website_traffic
Description: Source of the lead (cold_email or website_traffic)
```

**Settings:**
- [ ] Required: NO
- [ ] Show on contact: YES
- [ ] Show on form: NO

Click **Save**

### Step 3: Create Field #2 - vlpr_score

```
Field Name: vlpr_score
Field Type: Number
Placeholder: 0-100
Description: Virtual LPR qualification score (0-100)
```

**Settings:**
- [ ] Required: NO
- [ ] Show on contact: YES
- [ ] Show on form: NO

Click **Save**

### Step 4: Create Field #3 - vlpr_qualified

```
Field Name: vlpr_qualified
Field Type: Checkbox
Description: Lead passed Virtual LPR validation
```

**Settings:**
- [ ] Required: NO
- [ ] Show on contact: YES
- [ ] Show on form: NO

Click **Save**

### Step 5: Create Field #4 - distance_miles

```
Field Name: distance_miles
Field Type: Number
Placeholder: Distance in miles
Description: Distance from business location
```

**Settings:**
- [ ] Required: NO
- [ ] Show on contact: YES
- [ ] Show on form: NO

Click **Save**

### Step 6: Create Field #5 - median_income

```
Field Name: median_income
Field Type: Number
Placeholder: 50000
Description: Median household income (ZIP code)
```

**Settings:**
- [ ] Required: NO
- [ ] Show on contact: YES
- [ ] Show on form: NO

Click **Save**

### Step 7: Create Field #6 - awareness_level

```
Field Name: awareness_level
Field Type: Text (single line)
Placeholder: Problem Aware
Description: Schwartz awareness level (Unaware to Most Aware)
```

**Settings:**
- [ ] Required: NO
- [ ] Show on contact: YES
- [ ] Show on form: NO

Click **Save**

### Step 8: Create Field #7 - instantly_campaign_id

```
Field Name: instantly_campaign_id
Field Type: Text (single line)
Placeholder: camp_abc123
Description: Instantly.ai campaign ID
```

**Settings:**
- [ ] Required: NO
- [ ] Show on contact: YES
- [ ] Show on form: NO

Click **Save**

### Step 9: Create Field #8 - instantly_qualification

```
Field Name: instantly_qualification
Field Type: Text (single line)
Placeholder: positive
Description: Instantly reply qualification (positive/negative/neutral)
```

**Settings:**
- [ ] Required: NO
- [ ] Show on contact: YES
- [ ] Show on form: NO

Click **Save**

### ✅ Checkpoint: Verify Custom Fields

Go to **Settings → Custom Fields** and verify you see all 8 fields:

1. ✓ lead_source (Text)
2. ✓ vlpr_score (Number)
3. ✓ vlpr_qualified (Checkbox)
4. ✓ distance_miles (Number)
5. ✓ median_income (Number)
6. ✓ awareness_level (Text)
7. ✓ instantly_campaign_id (Text)
8. ✓ instantly_qualification (Text)

---

## Part 2: Build Workflow #1 - Website Traffic Path (30 minutes)

### Step 1: Create New Workflow

1. Go to **Automations** → **Workflows** in left sidebar
2. Click **+ Create Workflow** (top right)
3. Name: `Virtual LPR - Website Traffic`
4. Description: `Validates website leads and sends personalized copy`
5. Click **Create**

### Step 2: Configure Trigger

**Click the Trigger node:**

**Option A: Form Trigger**
1. Select: **Form Submitted**
2. Choose your website form
3. Click **Save**

**Option B: Tag Trigger**
1. Select: **Contact Tag Added**
2. Tag name: `Website Lead`
3. Click **Save**

**Recommended:** Use Tag trigger for flexibility

### Step 3: Add HTTP Request #1 - Virtual LPR

1. Click the **+** button below trigger
2. Select **Action**
3. Search for **Send HTTP Request** (not webhook)
4. Click to add

**Configure HTTP Request:**

**Request Name:** `Virtual LPR Validation`

**Method:** `POST`

**URL:**
```
https://your-project.vercel.app/api/virtual-lpr
```
⚠️ **IMPORTANT:** Replace `your-project.vercel.app` with your actual Vercel URL!

**Headers:**
```json
{
  "Content-Type": "application/json"
}
```

**Request Body (RAW JSON):**

```json
{
  "signal_type": "website_visit",
  "signal_data": {
    "phone": "{{contact.phone}}",
    "email": "{{contact.email}}",
    "zip_code": "{{contact.address.postal_code}}",
    "first_name": "{{contact.first_name}}",
    "last_name": "{{contact.last_name}}"
  },
  "business": {
    "name": "MetroFlex Gym",
    "lat": 32.7357,
    "lng": -97.1081,
    "city": "Fort Worth",
    "state": "TX",
    "zip": "76102"
  }
}
```

⚠️ **IMPORTANT:** Update the `business` object with YOUR business details:
- `name`: Your business name
- `lat`: Your latitude (get from Google Maps)
- `lng`: Your longitude (get from Google Maps)
- `city`, `state`, `zip`: Your location

**Save as Custom Values:**

Scroll down to **Save Response As** section and add these:

| Key Name | Value Path |
|----------|------------|
| `vlpr_score` | `{{custom_values.vlpr_score}}` |
| `vlpr_qualified` | `{{custom_values.qualified}}` |
| `distance_miles` | `{{custom_values.distance_miles}}` |
| `median_income` | `{{custom_values.median_income}}` |
| `awareness_level` | `{{custom_values.awareness_level}}` |
| `lead_source` | `website_traffic` |

**Advanced Settings:**
- Timeout: `30 seconds`
- Retry on failure: `Yes` (2 retries)

Click **Save**

### Step 4: Add Decision Node - Check Qualification

1. Click **+** below the HTTP Request
2. Select **Decision** (under Logic)
3. Click to add

**Configure Decision:**

**Decision Name:** `Check if Qualified`

**IF Condition:**
```
{{contact.custom_fields.vlpr_qualified}} equals Yes
```

**Alternative IF syntax** (if above doesn't work):
```
{{custom_values.qualified}} equals true
```

This creates TWO paths:
- **YES** path (qualified) → Continue
- **NO** path (not qualified) → Stop

Click **Save**

### Step 5: Update Contact Fields (YES path)

On the **YES** path:

1. Click **+** button
2. Select **Action**
3. Search for **Update Contact**
4. Click to add

**Configure Update Contact:**

**Fields to Update:**

| Field | Value |
|-------|-------|
| `lead_source` | `website_traffic` |
| `vlpr_score` | `{{custom_values.vlpr_score}}` |
| `vlpr_qualified` | `Yes` |
| `distance_miles` | `{{custom_values.distance_miles}}` |
| `median_income` | `{{custom_values.median_income}}` |
| `awareness_level` | `{{custom_values.awareness_level}}` |

Click **Save**

### Step 6: Add HTTP Request #2 - Master Copywriter (YES path)

1. Click **+** below Update Contact
2. Select **Action**
3. Search for **Send HTTP Request**
4. Click to add

**Configure HTTP Request:**

**Request Name:** `Master Copywriter`

**Method:** `POST`

**URL:**
```
https://your-project.vercel.app/api/copywriter
```

**Headers:**
```json
{
  "Content-Type": "application/json"
}
```

**Request Body (RAW JSON):**

```json
{
  "contact": {
    "first_name": "{{contact.first_name}}",
    "last_name": "{{contact.last_name}}",
    "email": "{{contact.email}}",
    "phone": "{{contact.phone}}",
    "city": "{{contact.address.city}}",
    "state": "{{contact.address.state}}",
    "custom_fields": {
      "distance_miles": "{{contact.custom_fields.distance_miles}}",
      "median_income": "{{contact.custom_fields.median_income}}",
      "vlpr_score": "{{contact.custom_fields.vlpr_score}}"
    }
  },
  "channel": "email",
  "awareness_level": "{{contact.custom_fields.awareness_level}}",
  "lead_source": "website_traffic",
  "business": {
    "name": "MetroFlex Gym",
    "city": "Fort Worth",
    "state": "TX",
    "phone": "(817) 555-0100",
    "website": "https://metroflexgym.com"
  }
}
```

⚠️ **IMPORTANT:** Update the `business` object with YOUR business details!

**Save as Custom Values:**

| Key Name | Value Path |
|----------|------------|
| `email_subject` | `{{custom_values.variants.variant_a.subject}}` |
| `email_body` | `{{custom_values.variants.variant_a.body}}` |
| `framework_used` | `{{custom_values.framework_selected}}` |

**Advanced Settings:**
- Timeout: `30 seconds`
- Retry on failure: `Yes` (2 retries)

Click **Save**

### Step 7: Add Email Action (YES path)

1. Click **+** below Master Copywriter HTTP Request
2. Select **Action**
3. Search for **Send Email**
4. Click to add

**Configure Email:**

**From Name:** `Your Business Name`

**From Email:** `hello@yourdomain.com` (or your GHL email)

**To:** `{{contact.email}}`

**Subject:** `{{custom_values.email_subject}}`

**Body Type:** HTML

**Email Body:**
```html
{{custom_values.email_body}}

<br><br>

<p style="color: #666; font-size: 12px;">
Powered by Virtual LPR™ | Framework: {{custom_values.framework_used}}
</p>
```

**Advanced:**
- Track opens: YES
- Track clicks: YES

Click **Save**

### Step 8: Configure NO Path (Not Qualified)

On the **NO** path from the Decision node:

1. Click **+** button
2. Select **Action**
3. Search for **Add Tag**
4. Click to add

**Tag to Add:** `Virtual LPR - Not Qualified`

This tags unqualified leads for follow-up or removal.

Click **Save**

### Step 9: Activate Workflow

1. Click **Publish** button (top right)
2. Toggle **Active** switch to ON
3. Workflow is now live!

### ✅ Checkpoint: Test Workflow

**Test with a real contact:**

1. Go to **Contacts** → **+ Add Contact**
2. Create test contact:
   - First Name: `Test`
   - Last Name: `Lead`
   - Email: `test@example.com`
   - Phone: `(817) 555-1234`
   - ZIP: `76102`
3. Add tag: `Website Lead`
4. Go to **Automations** → **Workflows**
5. Click your workflow name
6. Click **History** tab
7. Watch it execute in real-time

**Expected Results:**
- ✓ HTTP Request #1 completes (Virtual LPR)
- ✓ Decision evaluates to YES or NO
- ✓ If YES: Contact fields update
- ✓ If YES: HTTP Request #2 completes (Copywriter)
- ✓ If YES: Email sends to contact

**Verify in Contact:**
1. Go back to your test contact
2. Check custom fields populated:
   - `vlpr_score`: Should be 0-100
   - `vlpr_qualified`: Should be Yes or No
   - `awareness_level`: Should be set
   - `distance_miles`: Should show distance
3. Check **Activity** tab for sent email

---

## Part 3: Build Workflow #2 - Cold Email Path (20 minutes)

### Step 1: Create New Workflow

1. Go to **Automations** → **Workflows**
2. Click **+ Create Workflow**
3. Name: `Cold Email Reply Handler`
4. Description: `Qualifies cold email replies and sends nurture sequence`
5. Click **Create**

### Step 2: Configure Webhook Trigger

**Click the Trigger node:**

1. Select: **Webhook**
2. Copy the webhook URL that appears
3. Save this URL for Instantly.ai configuration

**Example webhook URL:**
```
https://services.leadconnectorhq.com/hooks/abc123xyz/webhook-trigger/xyz789abc
```

Click **Save**

### Step 3: Add HTTP Request - Instantly Webhook Handler

1. Click **+** below trigger
2. Select **Action**
3. Search for **Send HTTP Request**
4. Click to add

**Request Name:** `Instantly Reply Qualification`

**Method:** `POST`

**URL:**
```
https://your-project.vercel.app/api/instantly-webhook
```

**Headers:**
```json
{
  "Content-Type": "application/json"
}
```

**Request Body (RAW JSON):**

```json
{
  "event_type": "reply",
  "campaign_id": "{{webhook.campaign_id}}",
  "campaign_name": "{{webhook.campaign_name}}",
  "lead_email": "{{webhook.lead_email}}",
  "lead_first_name": "{{webhook.first_name}}",
  "lead_last_name": "{{webhook.last_name}}",
  "reply_text": "{{webhook.reply_text}}",
  "reply_date": "{{webhook.reply_date}}"
}
```

**Save as Custom Values:**

| Key Name | Value Path |
|----------|------------|
| `qualified` | `{{custom_values.qualified}}` |
| `intent` | `{{custom_values.intent}}` |
| `instantly_campaign_id` | `{{webhook.campaign_id}}` |

Click **Save**

### Step 4: Add Decision Node - Check Intent

1. Click **+** below HTTP Request
2. Select **Decision**
3. Click to add

**Decision Name:** `Check Reply Intent`

**IF Condition:**
```
{{custom_values.qualified}} equals true
```

**Alternative:**
```
{{custom_values.intent}} equals positive
```

Click **Save**

### Step 5: Create/Update Contact (YES path - Qualified)

On the **YES** path:

1. Click **+** button
2. Select **Action**
3. Search for **Create/Update Contact**
4. Click to add

**Email:** `{{webhook.lead_email}}`

**Fields:**

| Field | Value |
|-------|-------|
| First Name | `{{webhook.first_name}}` |
| Last Name | `{{webhook.last_name}}` |
| `lead_source` | `cold_email` |
| `instantly_campaign_id` | `{{webhook.campaign_id}}` |
| `instantly_qualification` | `{{custom_values.intent}}` |

**Tags to Add:** `Cold Email - Qualified`

Click **Save**

### Step 6: Add Master Copywriter (YES path)

1. Click **+** below Create/Update Contact
2. Select **Action**
3. Search for **Send HTTP Request**
4. Click to add

**Request Name:** `Master Copywriter - Cold Email`

**Method:** `POST`

**URL:**
```
https://your-project.vercel.app/api/copywriter
```

**Headers:**
```json
{
  "Content-Type": "application/json"
}
```

**Request Body:**

```json
{
  "contact": {
    "first_name": "{{contact.first_name}}",
    "email": "{{contact.email}}"
  },
  "channel": "email",
  "awareness_level": "Problem Aware",
  "lead_source": "cold_email",
  "business": {
    "name": "MetroFlex Gym",
    "city": "Fort Worth",
    "state": "TX"
  },
  "context": {
    "reply_text": "{{webhook.reply_text}}"
  }
}
```

**Save as Custom Values:**

| Key Name | Value Path |
|----------|------------|
| `email_subject` | `{{custom_values.variants.variant_a.subject}}` |
| `email_body` | `{{custom_values.variants.variant_a.body}}` |

Click **Save**

### Step 7: Send Follow-Up Email (YES path)

1. Click **+** below Master Copywriter
2. Select **Action**
3. Search for **Send Email**
4. Click to add

**From Name:** Your name or business name

**From Email:** Your email

**To:** `{{contact.email}}`

**Subject:** `{{custom_values.email_subject}}`

**Body:**
```html
{{custom_values.email_body}}

<br><br>

<p style="color: #666; font-size: 12px;">
Thanks for your interest!
</p>
```

Click **Save**

### Step 8: Handle Negative Responses (NO path)

On the **NO** path:

1. Click **+** button
2. Select **Action**
3. Search for **Create/Update Contact**
4. Click to add

**Email:** `{{webhook.lead_email}}`

**Tags to Add:** `Cold Email - Not Interested`

**Workflow:** Optionally add to suppression list

Click **Save**

### Step 9: Activate Workflow

1. Click **Publish**
2. Toggle **Active** to ON
3. Copy the webhook URL from Step 2

### ✅ Checkpoint: Configure Instantly.ai

**In Instantly.ai dashboard:**

1. Go to **Settings** → **Webhooks**
2. Click **+ Add Webhook**
3. **Webhook URL:** Paste the GHL webhook URL from Step 2
4. **Events to Track:**
   - ✓ Email Reply
   - ✓ Email Opened (optional)
   - ✓ Link Clicked (optional)
5. **Active:** ON
6. Click **Save**

**Test:**
1. Send a test campaign from Instantly
2. Reply to the email from your test account
3. Check GHL workflow history
4. Verify contact was created with correct tags

---

## Part 4: Testing & Verification (15 minutes)

### Test Scenario 1: Website Traffic Lead

**Setup:**
1. Create contact: `sarah@test.com`
2. First name: `Sarah`
3. ZIP: `76102`
4. Add tag: `Website Lead`

**Expected Results:**
- ✓ Workflow triggers
- ✓ Virtual LPR validates (score 60-80)
- ✓ Custom fields populate
- ✓ Email sends with confident tone
- ✓ Subject mentions "noticed you" or "saw you"

**Verify Tone:**
- Should NOT say "Thanks for replying"
- SHOULD say "Saw you on our website" or similar

### Test Scenario 2: Cold Email Reply (Positive)

**Setup:**
1. Send test webhook to Cold Email workflow with:
```json
{
  "lead_email": "marcus@test.com",
  "first_name": "Marcus",
  "reply_text": "Yes, I'm interested. Tell me more about pricing."
}
```

**Expected Results:**
- ✓ Workflow triggers
- ✓ Contact created/updated
- ✓ Tag: "Cold Email - Qualified"
- ✓ Email sends with humble tone
- ✓ Subject is respectful, not pushy

**Verify Tone:**
- SHOULD say "Thanks for replying"
- Should NOT be overly aggressive

### Test Scenario 3: Cold Email Reply (Negative)

**Setup:**
1. Send test webhook with:
```json
{
  "lead_email": "nope@test.com",
  "reply_text": "Not interested, please remove me."
}
```

**Expected Results:**
- ✓ Workflow triggers
- ✓ Qualification fails
- ✓ Tag: "Cold Email - Not Interested"
- ✓ NO email sent
- ✓ Contact marked for suppression

### Test Scenario 4: Compare Frameworks

**Test Different Awareness Levels:**

| Awareness Level | Expected Framework | Key Phrase to Look For |
|-----------------|-------------------|------------------------|
| Unaware | Brunson | "Let me tell you a story..." |
| Problem Aware | Schwartz | "Tired of..." or "Struggling with..." |
| Solution Aware | StoryBrand | "guide" or "plan" |
| Most Aware | Hormozi | "Here's what you get" or value equation |

**How to Test:**
1. Manually set `awareness_level` custom field on contact
2. Re-trigger workflow
3. Check email body for framework-specific language

---

## Part 5: Going Live

### Connect Real Traffic Sources

**Website Forms:**
1. Your form already triggers workflows via GHL forms
2. Just make sure forms have ZIP code field
3. Ensure form submission triggers "Website Lead" tag

**Google My Business:**
1. Go to **Settings** → **Integrations** → **Google My Business**
2. Connect your GMB account
3. Create automation: GMB lead → Add tag "Website Lead"

**Facebook Lead Ads:**
1. Go to **Settings** → **Integrations** → **Facebook**
2. Connect Facebook Ads account
3. Map form fields to GHL contact fields
4. Add trigger to workflow: "Facebook Lead"

**Instantly.ai:**
1. Already configured via webhook
2. Make sure webhook is active
3. Test with small campaign first

### Monitor Performance

**Key Metrics Dashboard:**

Go to **Analytics** → Create Custom Report:

**Metrics to Track:**

| Metric | Formula | Target |
|--------|---------|--------|
| Qualification Rate | (vlpr_qualified = Yes) / Total Leads | >60% |
| Email Open Rate | Emails Opened / Emails Sent | >45% |
| Reply Rate | Replies / Emails Sent | >8% |
| Booking Rate | Appointments / Qualified Leads | >15% |

**Create Smart Lists:**

1. **High-Value Leads**
   - `vlpr_score` > 80
   - `median_income` > 70000
   - `distance_miles` < 5

2. **Qualified Cold Leads**
   - `lead_source` = "cold_email"
   - `instantly_qualification` = "positive"

3. **Not Qualified - Follow Up**
   - `vlpr_score` 40-60
   - No appointment booked
   - Last contacted > 7 days

---

## Troubleshooting

### Issue: Workflow Doesn't Trigger

**Check:**
1. Workflow is **Active** (toggle ON)
2. Trigger conditions match (correct tag, form, etc.)
3. Contact has email + phone fields populated

### Issue: HTTP Request Times Out

**Check:**
1. Vercel URL is correct and includes `https://`
2. Vercel environment variables include `ANTHROPIC_API_KEY`
3. Increase timeout to 30 seconds in HTTP Request advanced settings

### Issue: Custom Fields Don't Populate

**Check:**
1. Field names match EXACTLY (case-sensitive)
   - ✓ `vlpr_score` (correct)
   - ✗ `VLPR_Score` (wrong)
   - ✗ `vlpr score` (wrong - no spaces)
2. Custom value mapping in HTTP Request is correct
3. API response is successful (check workflow history)

### Issue: Wrong Copy Tone (Cold Sounds Pushy)

**Check:**
1. `lead_source` field is set to EXACTLY `"cold_email"`
2. Not `"cold"`, `"email"`, or anything else
3. Check Master Copywriter HTTP Request body has correct `lead_source`

### Issue: Framework Not Routing Correctly

**Check:**
1. `awareness_level` is one of the 5 exact values:
   - "Unaware"
   - "Problem Aware"
   - "Solution Aware"
   - "Product Aware"
   - "Most Aware"
2. Case matters! "problem aware" won't work
3. Virtual LPR is setting this field correctly

### Issue: No Email Sent

**Check:**
1. Contact has valid email address
2. Email action is on the YES path (after decision node)
3. `{{custom_values.email_body}}` is populated
4. Check GHL email sending limits (may need to verify domain)

---

## Advanced Customization

### Add SMS Follow-Up

After email sends:

1. Click **+** below Email action
2. Select **Send SMS**
3. **To:** `{{contact.phone}}`
4. **Message:**
```
Hi {{contact.first_name}}, just sent you an email about [topic].
Check your inbox! - [Your Name]
```

### Add Internal Notification

For high-score leads:

1. After Update Contact action
2. Add **Decision** node
3. **IF:** `{{contact.custom_fields.vlpr_score}}` > 80
4. Add **Send Internal Notification** action
5. Alert sales team of hot lead

### A/B Test Frameworks

Create 3 parallel paths after Master Copywriter:

**Path A:** Send Variant A (Brunson)
**Path B:** Send Variant B (Schwartz)
**Path C:** Send Variant C (Hormozi)

Use **Random Split** node to distribute evenly.

Track which variant performs best!

---

## ✅ Final Checklist

### Custom Fields
- [ ] All 8 custom fields created
- [ ] Field names match exactly
- [ ] Visible on contact record

### Workflow 1: Website Traffic
- [ ] Created and active
- [ ] Trigger configured (tag or form)
- [ ] HTTP Request #1 (Virtual LPR) with correct URL
- [ ] Decision node checks qualification
- [ ] Update Contact action populates fields
- [ ] HTTP Request #2 (Copywriter) with correct URL
- [ ] Email action sends with dynamic content
- [ ] Tested with real contact

### Workflow 2: Cold Email
- [ ] Created and active
- [ ] Webhook trigger configured
- [ ] HTTP Request (Instantly webhook) with correct URL
- [ ] Decision node checks intent
- [ ] Create/Update Contact on YES path
- [ ] Master Copywriter generates humble copy
- [ ] Email sends follow-up
- [ ] Webhook URL added to Instantly.ai

### Testing
- [ ] Website lead test passed
- [ ] Cold email (positive) test passed
- [ ] Cold email (negative) test passed
- [ ] Tone difference verified
- [ ] Framework routing verified

### Live
- [ ] Real lead sources connected
- [ ] Monitoring dashboard created
- [ ] Team notified of new system
- [ ] Backup/export workflows

---

## 🎉 You're Done!

Your Dual-Path Lead System is now live in GoHighLevel!

**What happens now:**
1. Leads come in from website/GMB → Virtual LPR validates → Personalized email sends
2. Cold email replies → Sentiment analysis → Qualified leads get follow-up
3. All lead data tracked in custom fields
4. Framework selection happens automatically
5. Tone adapts based on lead source

**Monitor for 48 hours:**
- Check workflow history for any errors
- Verify emails are sending
- Watch custom fields populate
- Review lead qualification accuracy

**Optimize after 1 week:**
- A/B test different frameworks
- Adjust awareness level thresholds
- Refine copy templates
- Add more automation steps

---

**Need help?** Check [QUICK-REFERENCE-CARD.md](./QUICK-REFERENCE-CARD.md) for troubleshooting.

**© 2025 CircuitOS™ - Virtual LPR™ Technology**
