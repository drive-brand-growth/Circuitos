# GHL Webhook Setup Guide - Where to Build It

**Your Question:** "Should I create the webhook in MetroFlex Gym subaccount or MetroFlex Events subaccount?"

**Your Current Setup:**
- 📍 **MetroFlex Gym** subaccount (Arlington gym operations)
- 📍 **MetroFlex Events** subaccount (Competitions, vendor booths, sponsorships)

**Your AI Agents:**
1. **Licensing Agent** → $40k-60k deals (gym-related but new business)
2. **Gym Member Agent** → $2,500 Founder's memberships (gym operations)
3. **Events Agent** → Tickets, vendors, sponsors (event operations)

---

## 🎯 Recommended Approach: Create a THIRD Subaccount

### Option 1: MetroFlex AI Hub (Best Practice - Recommended)

**Create a NEW subaccount:** "MetroFlex AI Hub" or "MetroFlex Lead Center"

**Why this is BEST:**
✅ **Centralized Lead Management** - All AI-captured leads in one place
✅ **Cross-Business Intelligence** - See all opportunities together
✅ **Easier Routing** - Distribute leads to Gym or Events teams from one hub
✅ **Cleaner Reporting** - Unified AI performance metrics
✅ **Future-Proof** - Add more AI agents without restructuring
✅ **Brian's Dashboard** - One place for him to see all AI-generated opportunities

**How leads would flow:**
```
AI Agents (Licensing, Gym, Events)
         │
         ▼
   GHL Webhook
         │
         ▼
"MetroFlex AI Hub" Subaccount
         │
         ├─► IF Licensing Lead (score >= 70)
         │   → Tag: "Licensing - Hot Lead"
         │   → Assign to: Brian Dobson
         │   → Pipeline: "Licensing Opportunities"
         │   → Value: $40k-60k
         │
         ├─► IF Gym Member Lead
         │   → Tag: "Miami Gym - Prospect" or "Founder's"
         │   → Move to: MetroFlex Gym subaccount
         │   → Assign to: Brian or Sales Team
         │   → Pipeline: "Memberships"
         │
         └─► IF Events Lead
             → Tag: "Event Inquiry"
             → Move to: MetroFlex Events subaccount
             → Assign to: Events Team
             → Pipeline: "Event Sales"
```

**Setup in GHL:**
1. Create new subaccount: "MetroFlex AI Hub"
2. Create pipelines:
   - "Licensing Opportunities" (stages: Qualification → Application → Contract → Closed)
   - "Gym Memberships" (stages: Inquiry → Consultation → Founder's → Member)
   - "Event Inquiries" (stages: Interest → Quote → Booked)
3. Create webhook: "AI Lead Capture"
4. Set up automations to route leads to respective subaccounts

**Cost:** Same (subaccounts are free in GHL)

---

## Option 2: MetroFlex Gym Subaccount (Second Best)

**Use existing:** MetroFlex Gym subaccount

**Why this works:**
✅ No new subaccount needed
✅ Licensing is gym-related business
✅ Gym memberships already here
✅ Brian probably checks this one most

**Downsides:**
⚠️ Events leads mixed with gym operations
⚠️ Harder to separate AI performance from manual leads
⚠️ May clutter gym team's pipeline

**How leads would flow:**
```
All AI Agents → MetroFlex Gym Subaccount
                      │
                      ├─► Licensing: "Licensing Pipeline"
                      ├─► Gym: "Membership Pipeline"
                      └─► Events: "Event Inquiries Pipeline"
```

**Setup in GHL:**
1. Go to MetroFlex Gym subaccount
2. Settings → Webhooks → Create "AI Lead Capture"
3. Create new pipelines for Licensing and Events
4. Tag all AI leads with "AI-Generated"

---

## Option 3: MetroFlex Events Subaccount (Least Recommended)

**Use existing:** MetroFlex Events subaccount

**Why this could work:**
✅ Events are high-volume
✅ Already have event infrastructure

**Downsides:**
❌ Licensing and Gym leads don't belong in Events
❌ Wrong context for Brian's gym licensing deals
❌ Confusing for events team

**Only use this if:** You're ONLY using the Events AI agent (not Licensing or Gym agents)

---

## 🎯 My Strong Recommendation

### Create "MetroFlex AI Hub" Subaccount

**Here's exactly how to set it up:**

### Step 1: Create New Subaccount (5 min)
1. Login to GHL main account
2. Settings → Sub-Accounts
3. Click "Add Sub-Account"
4. Name: **"MetroFlex AI Hub"**
5. Purpose: **AI Lead Management & Routing**

### Step 2: Create Pipelines (10 min)

**Pipeline 1: Licensing Opportunities**
- Stage 1: "Qualification" (AI scored, waiting review)
- Stage 2: "Application Sent" (Brian sent application)
- Stage 3: "Under Review" (Reviewing docs)
- Stage 4: "Contract Negotiation" (Discussing terms)
- Stage 5: "Closed Won" ($40k-60k!)
- Stage 6: "Closed Lost" (Not qualified or passed)

**Pipeline 2: Gym Memberships**
- Stage 1: "AI Inquiry" (AI detected interest)
- Stage 2: "Consultation Scheduled" (Call booked)
- Stage 3: "Founder's Offer Made" ($2,500)
- Stage 4: "Payment Pending"
- Stage 5: "Active Member"
- Stage 6: "Lost"

**Pipeline 3: Event Leads**
- Stage 1: "Event Inquiry" (AI captured)
- Stage 2: "Quote Sent"
- Stage 3: "Negotiation"
- Stage 4: "Booked"
- Stage 5: "Closed Lost"

### Step 3: Create Webhook (2 min)
1. In AI Hub subaccount → Settings → Webhooks
2. Click "Create Webhook"
3. Name: **"AI Lead Capture"**
4. Type: **Inbound Webhook**
5. Copy the webhook URL (looks like: `https://services.leadconnectorhq.com/hooks/xxx`)

**This URL is what you'll add to Railway**

### Step 4: Set Up Tags
Create these tags in AI Hub:
- `AI-Generated` (all AI leads)
- `Licensing - Hot Lead` (score >= 85)
- `Licensing - Qualified` (score >= 70)
- `Licensing - Nurture` (score 50-69)
- `Founder's - Hot Lead` (high commitment, $2500 budget)
- `Miami Gym - Prospect`
- `Event Inquiry`
- `High-Intent` (all high-intent detections)

### Step 5: Create Automation (Optional - 15 min)
**Automation 1: Route Licensing Leads**
```
Trigger: Contact created via AI webhook
Condition: Tag contains "Licensing"
Actions:
  1. Add to "Licensing Opportunities" pipeline (Stage: Qualification)
  2. Assign to: Brian Dobson
  3. Send internal notification to Brian (Email/SMS)
  4. IF tag = "Licensing - Hot Lead":
     → Send urgent notification: "🚨 $60k opportunity!"
     → Create task: "Call within 24 hours"
```

**Automation 2: Route Gym Leads**
```
Trigger: Contact created via AI webhook
Condition: Tag contains "Gym" or "Founder's"
Actions:
  1. Add to "Gym Memberships" pipeline
  2. Assign to: Brian or Gym Sales Team
  3. IF tag = "Founder's - Hot Lead":
     → Send urgency email: "Limited Founder's spots!"
     → Add to Founder's nurture sequence
```

**Automation 3: Route Event Leads**
```
Trigger: Contact created via AI webhook
Condition: Tag contains "Event"
Actions:
  1. Add to "Event Leads" pipeline
  2. Assign to: Events Team
  3. Send to event inquiry follow-up sequence
```

---

## 🔄 Alternative: Multi-Webhook Strategy

**If you want leads to go directly to respective subaccounts:**

**Create 3 separate webhooks:**
1. **Licensing Webhook** → MetroFlex Gym subaccount
2. **Gym Membership Webhook** → MetroFlex Gym subaccount
3. **Events Webhook** → MetroFlex Events subaccount

**Update Railway with 3 variables:**
```bash
railway variables set LICENSING_WEBHOOK="url_from_gym_subaccount"
railway variables set GYM_WEBHOOK="url_from_gym_subaccount"
railway variables set EVENTS_WEBHOOK="url_from_events_subaccount"
```

**Then update the AI agents to use respective webhooks.**

**Pros:**
✅ Leads automatically sorted
✅ Each team sees only their leads

**Cons:**
❌ More complex setup
❌ Harder to see unified AI performance
❌ Brian can't see all opportunities in one place

---

## 💡 My Implementation Recommendation

**Best Practice Setup (30 min total):**

1. **Create "MetroFlex AI Hub" subaccount** (5 min)
   - Centralized AI lead management
   - Brian's main dashboard

2. **Create 3 pipelines in AI Hub** (10 min)
   - Licensing Opportunities
   - Gym Memberships
   - Event Leads

3. **Create single webhook in AI Hub** (2 min)
   - Captures all AI leads
   - Easier to manage

4. **Set up routing automations** (15 min)
   - Auto-assign based on lead type
   - Send to respective teams
   - Alert Brian for high-value opportunities

5. **Add webhook URL to Railway** (1 min)
   ```bash
   railway variables set GHL_LEAD_CAPTURE_WEBHOOK="your_ai_hub_webhook_url"
   railway restart
   ```

**Result:**
- All AI leads funnel through one hub
- Automatically routed to right teams
- Brian sees everything in one dashboard
- Clean reporting on AI performance
- Easy to scale (add more agents later)

---

## 🎯 Quick Decision Matrix

| Where to Create Webhook | Best For | Complexity | My Rating |
|-------------------------|----------|------------|-----------|
| **NEW: MetroFlex AI Hub** | Clean organization, Brian's dashboard | Medium | ⭐⭐⭐⭐⭐ **BEST** |
| **Existing: MetroFlex Gym** | Quick setup, gym-focused | Low | ⭐⭐⭐ Good |
| **Existing: MetroFlex Events** | Only using events agent | Low | ⭐⭐ OK |
| **Multi-Webhook (3 separate)** | Advanced users, team separation | High | ⭐⭐⭐⭐ Advanced |

---

## ✅ What Should You Do Right Now?

**I recommend:** Create the "MetroFlex AI Hub" subaccount

**Steps:**
1. Create AI Hub subaccount (5 min)
2. Create webhook in AI Hub (2 min)
3. Give me the webhook URL
4. I'll add it to Railway
5. Test with a sample lead

**Want me to walk you through creating the AI Hub subaccount step-by-step?**

Or if you prefer simpler:
**Just use MetroFlex Gym subaccount for now**, and we can migrate to AI Hub later if needed.

**Your call - what works best for your workflow?** 🚀
