# 🎯 GHL WEBHOOK SETUP - STEP BY STEP

## ✅ WHAT YOU'VE ALREADY DONE
- Created "MetroFlex AI Hub" subaccount in GHL
- Railway deployment is uploading (20-25 minutes to complete)

---

## 📍 STEP 1: CREATE WEBHOOK IN GHL (DO THIS NOW)

You're already in your GHL dashboard. Follow these exact steps:

### 1. Navigate to Webhooks
1. In the left sidebar, click **"Settings"** (gear icon)
2. Scroll down and click **"Webhooks"**
3. Click **"Create Webhook"** or **"Add Webhook"** button

### 2. Configure Webhook
Fill in these details:

**Webhook Name:**
```
AI Lead Capture
```

**Webhook Type:**
```
Inbound Webhook
```

**Events to Trigger:**
- ✅ Contact Created
- ✅ Opportunity Created (optional but recommended)
- ✅ Form Submitted (if you have forms)

### 3. Copy the Webhook URL
After creating the webhook, GHL will show you a URL that looks like:
```
https://services.leadconnectorhq.com/hooks/xxxxxxxxxxxxxxxxxx
```

**📋 COPY THIS URL** - You'll need it in Step 2

---

## 🚀 STEP 2: ADD WEBHOOK TO RAILWAY (WAIT 25 MIN)

⏳ **IMPORTANT:** Wait for Railway deployment to complete before doing this step.

Once Railway shows "Deployment Successful" (check: https://railway.app/dashboard), run:

```bash
/Users/noelpena/.npm-global/bin/railway variables
```

This will open Railway's variable editor. Add:

```
GHL_LEAD_CAPTURE_WEBHOOK=paste_your_webhook_url_here
```

Then restart the service:
```bash
/Users/noelpena/.npm-global/bin/railway service
```

Select your service, then:
```bash
/Users/noelpena/.npm-global/bin/railway up
```

---

## 📊 STEP 3: CREATE PIPELINES (OPTIONAL)

This helps organize leads in GHL. In "MetroFlex AI Hub" subaccount:

### Pipeline 1: Licensing Opportunities
1. Go to **Opportunities** → **Pipelines**
2. Create new pipeline: **"Licensing Opportunities"**
3. Add stages:
   - 🔥 Fast-Track (Score 85+)
   - ✅ Qualified (Score 70-84)
   - 🌱 Nurture (Score 50-69)
   - ❌ Not Qualified (Score <50)

### Pipeline 2: Gym Memberships
1. Create pipeline: **"Gym Memberships"**
2. Add stages:
   - 💎 Founder's Membership Interest
   - 📅 Monthly Membership Interest
   - 🎟️ Day Pass Interest
   - ✅ Member Onboarded

### Pipeline 3: Event Leads
1. Create pipeline: **"Event Leads"**
2. Add stages:
   - 🎪 Vendor Interest
   - 🏆 Competitor Interest
   - 🎟️ Ticket Sales
   - 💼 Sponsorship Interest

---

## 🧪 STEP 4: TEST THE SYSTEM

### Get Your Railway URL
Once deployment completes:
```bash
/Users/noelpena/.npm-global/bin/railway domain
```

This will show your live URL (e.g., `https://metroflex-ai-production.up.railway.app`)

### Test the AI Agent
Send a test message via your website chat widget:

**Test Message:**
```
I'm interested in opening a MetroFlex gym in Austin, Texas. I have about $200k in capital and 5 years of fitness industry experience.
```

**Expected Result:**
- AI responds with licensing qualification questions
- Lead appears in GHL "MetroFlex AI Hub" with:
  - Tag: "Licensing Lead"
  - Qualification Score: 85+ (Fast-Track)
  - Opportunity in "Licensing Opportunities" pipeline

### Check GHL
1. Go to **Contacts** in "MetroFlex AI Hub"
2. Look for the test contact
3. Verify tags and qualification score
4. Check if opportunity was created

---

## 🎉 WHAT HAPPENS NEXT

Once this is set up, here's the automated flow:

### Licensing Leads
1. Someone asks about licensing on your website
2. AI qualifies them (0-100 score)
3. Lead sent to GHL "AI Hub" with score + tags
4. If score 85+: Brian gets Slack alert (once n8n is added)
5. If score 70-84: Standard qualification sequence
6. If score 50-69: Education nurture sequence
7. If score <50: Referred to gym membership

### Gym Leads
1. Someone asks about memberships
2. AI recommends best tier (Founder's, Monthly, Day Pass)
3. Lead sent to GHL with tier recommendation
4. Founder's leads: FOMO urgency messaging
5. Automated booking link for gym tour

### Event Leads
1. Someone asks about vendor booth, competitor registration, etc.
2. AI answers questions from Events knowledge base
3. Lead sent to GHL with event interest tag
4. Automated follow-up with registration links

---

## 📞 NEED HELP?

If you get stuck on any step, let me know exactly where and I'll help troubleshoot!

## 🚨 CURRENT STATUS

✅ GitHub pushed (350 files)
✅ Railway deployment uploading (25 min ETA)
✅ GHL "MetroFlex AI Hub" created
⏳ Webhook creation (YOU'RE HERE - Step 1)
⏳ Webhook URL to Railway (Step 2 - after deployment)
⏳ Test system (Step 4 - final verification)
