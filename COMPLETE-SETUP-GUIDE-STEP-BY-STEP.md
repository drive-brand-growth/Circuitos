# Complete Setup Guide - From Zero to Production
## Dual-Path Lead System with GHL Integration

**For:** Someone with basic GHL knowledge (not an expert)
**Time:** 2-3 hours total
**Difficulty:** Beginner-friendly with checkpoints
**What You'll Build:** Complete lead validation system with dual-path routing

---

## 🎯 What You're Building (Overview)

By the end of this guide, you'll have:

1. **Local Development Environment** - Test everything on your computer first
2. **API Endpoints** - 5 working APIs that validate leads and generate copy
3. **Vercel Production Deployment** - Live system accessible worldwide
4. **GHL Integration** - 2 workflows that use your APIs
5. **End-to-End Testing** - Verify both cold email and website traffic paths work

**Path 1 (Cold Email):**
```
Instantly.ai sends email → Lead replies → Your API qualifies → Creates GHL contact → Sends personalized follow-up
```

**Path 2 (Website Traffic):**
```
Lead visits website → Your API validates → Creates GHL contact → Sends personalized email immediately
```

---

## 📋 Pre-Requirements Checklist

Before starting, make sure you have:

### ✅ Accounts You Need:

- [ ] **GitHub account** - You have this (your code is there)
- [ ] **Anthropic account** - For Claude API (we'll get key in Step 1)
- [ ] **GoHighLevel account** - For creating workflows
- [ ] **Instantly.ai account** (optional for now - Path 1 only)
- [ ] **Computer with terminal access** - Mac/Linux/Windows with Git Bash

### ✅ Software Installed:

Check if you have these installed. Open terminal and run:

```bash
# Check Node.js (need v18+)
node --version
# Should show: v18.x.x or higher

# Check npm
npm --version
# Should show: 9.x.x or higher

# Check git
git --version
# Should show: git version 2.x.x
```

**Don't have Node.js?**
- Go to: https://nodejs.org/
- Download LTS version
- Install
- Restart terminal

---

## 🚀 PHASE 1: Local Development Setup (30 minutes)

**Goal:** Get everything running on your computer first so you can test before deploying.

---

### STEP 1: Get Your Claude API Key (5 minutes)

**What this is:** Your authentication to use Claude AI for lead validation and copy generation.

**Cost:** Pay-per-use (~$0.01 per lead validation)

#### 1.1 Create Anthropic Account

1. Go to: https://console.anthropic.com/
2. Click "Sign Up" (top right)
3. Sign up with email or Google
4. Verify your email

#### 1.2 Add Payment Method

1. After login, click your profile (top right)
2. Click "Billing"
3. Click "Add Payment Method"
4. Add credit card (won't be charged until you use API)
5. **Note:** First $5 is usually free credits

#### 1.3 Create API Key

1. Click "API Keys" in left sidebar
2. Click "Create Key"
3. Name it: `CircuitOS Local Dev`
4. **COPY THE KEY NOW** - it starts with `sk-ant-api03-`
5. Save it somewhere safe (you'll need it in next step)

**✅ CHECKPOINT:** You should have a key that looks like:
```
sk-ant-api03-ABcdEFghIJklMNopQRstUVwxYZ1234567890...
```

---

### STEP 2: Clone Your Repository Locally (3 minutes)

**What this does:** Downloads your code to your computer so you can run it locally.

#### 2.1 Open Terminal

- **Mac:** Applications → Utilities → Terminal
- **Windows:** Search "Git Bash" (if you have Git installed)
- **Linux:** Ctrl+Alt+T

#### 2.2 Navigate to Where You Want the Code

```bash
# Example: Go to Desktop
cd ~/Desktop

# Or create a projects folder
mkdir ~/projects
cd ~/projects
```

#### 2.3 Clone the Repository

```bash
git clone https://github.com/drive-brand-growth/Circuitos.git
cd Circuitos
```

**What you'll see:**
```
Cloning into 'Circuitos'...
remote: Enumerating objects: 150, done.
remote: Counting objects: 100% (150/150), done.
remote: Compressing objects: 100% (100/100), done.
Receiving objects: 100% (150/150), 500 KB | 2 MB/s, done.
```

#### 2.4 Verify You Have the Code

```bash
ls
```

**You should see:**
```
api/
lib/
GHL-Setup/
package.json
vercel.json
DUAL-PATH-LEAD-SYSTEM.md
... (other files)
```

**✅ CHECKPOINT:** You're now in the `Circuitos` directory with all the code.

---

### STEP 3: Install Dependencies (2 minutes)

**What this does:** Downloads the libraries your code needs (like Claude AI SDK).

#### 3.1 Install Node Modules

```bash
npm install
```

**What you'll see:**
```
npm WARN deprecated ...
added 50 packages, and audited 51 packages in 5s
```

**Wait for it to finish** (30-60 seconds).

#### 3.2 Verify Installation

```bash
ls node_modules
```

**You should see:**
```
@anthropic-ai/
... (many folders)
```

**✅ CHECKPOINT:** `node_modules` folder exists with ~50 packages installed.

---

### STEP 4: Create Environment Variables File (3 minutes)

**What this is:** Secret configuration (like your API keys) that won't be committed to GitHub.

#### 4.1 Create .env File

```bash
# Copy the example
cp .env.example .env
```

#### 4.2 Edit .env File

**Option A: Using nano (terminal editor):**
```bash
nano .env
```

**Option B: Using VS Code:**
```bash
code .env
```

**Option C: Using any text editor:**
- Open `.env` file in your favorite editor

#### 4.3 Add Your API Key

**Find this line:**
```
ANTHROPIC_API_KEY=sk-ant-api03-your-key-here
```

**Replace with your actual key from Step 1:**
```
ANTHROPIC_API_KEY=sk-ant-api03-ABcdEFghIJklMNopQRstUVwxYZ1234567890...
```

#### 4.4 Add Your Business Info (Optional but Recommended)

**Update these lines with your actual business:**
```bash
BUSINESS_NAME="MetroFlex Gym"
BUSINESS_LAT=32.7357
BUSINESS_LNG=-97.1081
BUSINESS_CITY="Arlington"
BUSINESS_STATE="TX"
BUSINESS_TYPE="Hardcore powerlifting gym"
```

**Don't know your lat/lng?**
- Google "my coordinates"
- Or go to: https://www.latlong.net/

#### 4.5 Save the File

- **nano:** Press `Ctrl+O`, Enter, then `Ctrl+X`
- **VS Code:** Press `Cmd+S` (Mac) or `Ctrl+S` (Windows)

**✅ CHECKPOINT:** Run this command to verify:
```bash
cat .env | grep ANTHROPIC_API_KEY
```

**You should see:**
```
ANTHROPIC_API_KEY=sk-ant-api03-ABcd... (your key)
```

**🔒 IMPORTANT:** Never commit `.env` to GitHub (it's in `.gitignore` so you're safe).

---

### STEP 5: Test Locally with Vercel Dev (10 minutes)

**What this does:** Runs your API endpoints on your computer so you can test them.

#### 5.1 Install Vercel CLI

```bash
npm install -g vercel
```

**What you'll see:**
```
added 1 package in 3s
```

#### 5.2 Start Local Development Server

```bash
vercel dev
```

**What you'll see:**
```
Vercel CLI 33.0.0
? Set up and develop "~/projects/Circuitos"? [Y/n] y
? Which scope should contain your project?
? Link to existing project? [y/N] n
? What's your project's name? circuitos
? In which directory is your code located? ./

🔗  Linked to your-username/circuitos
> Ready! Available at http://localhost:3000
```

**Answer the questions:**
- Set up project? **y** (yes)
- Link to existing? **n** (no, new project)
- Project name? **circuitos** (or whatever you want)
- Directory? **./** (current directory, press Enter)

**Wait for "Ready! Available at..."**

#### 5.3 Test Your First API Endpoint

**Open a NEW terminal window** (keep the first one running).

**Test Virtual LPR:**

```bash
curl -X POST http://localhost:3000/api/virtual-lpr \
  -H "Content-Type: application/json" \
  -d '{
    "signal_type": "website_visit",
    "signal_data": {
      "page_url": "/pricing",
      "location": {
        "city": "Arlington",
        "zip_code": "76011",
        "lat": 32.7450,
        "lng": -97.1180
      }
    },
    "business": {
      "name": "MetroFlex Gym",
      "city": "Arlington",
      "state": "Texas",
      "lat": 32.7357,
      "lng": -97.1081,
      "target_radius_miles": 10
    }
  }'
```

**What you should see:**
```json
{
  "success": true,
  "qualified": true,
  "detection": {
    "signal_strength": 85,
    "predicted_lpr_score": 78,
    "reasoning": "High-intent action from 1.8 miles away...",
    ...
  }
}
```

**✅ CHECKPOINT:** If you see `"success": true` and `"qualified": true`, it's working!

**❌ ERROR: "ANTHROPIC_API_KEY not found"**
- Go back to Step 4
- Make sure `.env` file has your key
- Restart `vercel dev` (Ctrl+C, then run again)

**❌ ERROR: "Invalid API key"**
- Check Step 1.3 - make sure you copied the full key
- Key should start with `sk-ant-api03-`

---

### STEP 6: Test the Interactive Test Console (5 minutes)

**What this is:** A beautiful web interface to test all your APIs visually.

#### 6.1 Open Test Console in Browser

With `vercel dev` still running, open:

```
http://localhost:3000/api/test-lead-validation
```

**What you should see:**
- Beautiful purple/gradient page
- Title: "Virtual LPR™ Test Console"
- 3 test cards:
  - ✅ Test 1: High-Intent GMB
  - 📊 Test 2: Website Visit
  - ❌ Test 3: Low Quality Lead

#### 6.2 Run Test 1 (High-Intent GMB)

1. **Click:** "Run Test" button on first card
2. **Wait:** ~2 seconds (you'll see a spinner)
3. **Result:** Should show:
   ```
   ✅ LEAD QUALIFIED
   Signal Score: 85
   LPR Score: 78
   Distance: 1.8 mi
   ```

#### 6.3 Run Test 2 (Website Visit)

1. **Click:** "Run Test" on second card
2. **Result:** Should show:
   ```
   ✅ LEAD QUALIFIED
   Signal Score: 70
   LPR Score: 65
   Distance: 7.0 mi
   ```

#### 6.4 Run Test 3 (Low Quality)

1. **Click:** "Run Test" on third card
2. **Result:** Should show:
   ```
   ❌ LEAD NOT QUALIFIED
   Signal Score: 25
   Reasoning: Low engagement from 30 miles away...
   ```

**✅ CHECKPOINT:** All 3 tests should complete with results showing.

**📸 SCREENSHOT:** Take a screenshot of the test results - you'll want this later!

---

### STEP 7: Test the Master Copywriter (5 minutes)

**What this does:** Tests the AI copywriting with 4 frameworks (Brunson, Schwartz, StoryBrand, Hormozi).

#### 7.1 Test Cold Email Copy Generation

In your second terminal window:

```bash
curl -X POST http://localhost:3000/api/copywriter \
  -H "Content-Type: application/json" \
  -d '{
    "contact": {
      "first_name": "John",
      "last_name": "Doe",
      "city": "Arlington",
      "custom_fields": {
        "lpr_score": 75,
        "distance_miles": 2.3
      }
    },
    "channel": "email",
    "awareness_level": "Solution Aware",
    "lead_source": "cold_email",
    "business": {
      "name": "MetroFlex Gym",
      "city": "Arlington",
      "state": "Texas",
      "type": "Hardcore powerlifting gym"
    }
  }'
```

**What you should see:**
```json
{
  "success": true,
  "copy": {
    "variants": [
      {
        "id": "A",
        "subject": "John - for serious lifters only",
        "body": "John,\n\nThanks for replying!...",
        "framework_used": "StoryBrand (build trust)",
        ...
      },
      {
        "id": "B",
        "subject": "...",
        "body": "...",
        ...
      },
      {
        "id": "C",
        "subject": "...",
        "body": "...",
        ...
      }
    ],
    "recommended_variant": "A"
  }
}
```

**✅ CHECKPOINT:** You should see 3 variants (A, B, C) with different subject lines and bodies.

#### 7.2 Compare: Cold vs Warm Copy

**Now test with warm traffic (website visitor):**

```bash
curl -X POST http://localhost:3000/api/copywriter \
  -H "Content-Type: application/json" \
  -d '{
    "contact": {
      "first_name": "Sarah",
      "custom_fields": {
        "lpr_score": 82,
        "distance_miles": 1.8
      }
    },
    "channel": "email",
    "awareness_level": "Product Aware",
    "lead_source": "website_traffic",
    "business": {
      "name": "MetroFlex Gym",
      "city": "Arlington",
      "state": "Texas"
    }
  }'
```

**Notice the difference:**
- **Cold email** body starts with: "Thanks for replying..." (humble, respectful)
- **Website traffic** body starts with: "Saw you on our site..." (confident, direct)

**✅ CHECKPOINT:** Tone should be noticeably different between cold and warm.

---

### STEP 8: Understand What You Just Tested (5 minutes)

**Let's break down what's happening:**

#### 8.1 The Flow You Just Tested

```
1. Lead signal comes in (website visit, GMB action, email reply)
   ↓
2. Virtual LPR API (/api/virtual-lpr)
   - Validates: Is this lead qualified?
   - Enriches: Distance, demographics (Census data)
   - Scores: 0-100 based on fit, intent, timing
   ↓
3. Lead Router API (/api/lead-router)
   - Detects: Cold email or website traffic?
   - Routes: Path 1 (cold) or Path 2 (warm)
   ↓
4. Master Copywriter API (/api/copywriter)
   - Selects framework: Brunson, Schwartz, StoryBrand, or Hormozi
   - Adapts tone: Humble (cold) or confident (warm)
   - Generates: 3 A/B/C variants
   ↓
5. Result: Personalized copy ready to send
```

#### 8.2 The 4 Copywriting Frameworks

Your system automatically chooses:

| Framework | When Used | Example |
|-----------|-----------|---------|
| **Brunson** | Product Aware (61-80 LPR) | Hook-Story-Offer: "Tired of gyms where..." |
| **Schwartz** | Any awareness level | Awareness-based: "You might not know..." |
| **StoryBrand** | Cold emails, Solution Aware | Hero's journey: "You're a serious lifter..." |
| **Hormozi** | Most Aware (81-100 LPR) | Value equation: "$60/mo, PR in 30 days..." |

**✅ CHECKPOINT:** You understand the flow from lead signal → validation → copy generation.

---

## 🎯 PHASE 2: Deploy to Production (20 minutes)

**Goal:** Make your APIs accessible on the internet so GHL and Instantly can use them.

---

### STEP 9: Deploy to Vercel (10 minutes)

**What this does:** Puts your code on Vercel's servers so it's available 24/7.

#### 9.1 Create Vercel Account

1. Go to: https://vercel.com/signup
2. Click "Continue with GitHub"
3. Authorize Vercel

**✅ CHECKPOINT:** You're logged into Vercel dashboard.

#### 9.2 Import Your Repository

1. Click "Add New..." → "Project"
2. Find `drive-brand-growth/Circuitos` in the list
3. Click "Import"

**Configuration screen:**
- Framework Preset: **Other** (auto-detected)
- Root Directory: **./** (leave default)
- Build Command: (leave blank)
- Output Directory: (leave blank)

4. Click "Deploy"

**⏳ Wait 30-60 seconds...**

**✅ CHECKPOINT:** You see "Congratulations! Your project is deployed."

**Your production URL:**
```
https://circuitos-abc123.vercel.app
```

**COPY THIS URL** - you'll need it!

---

### STEP 10: Add Environment Variables to Vercel (5 minutes)

**What this does:** Adds your Claude API key to production so your deployed APIs work.

#### 10.1 Go to Settings

1. Click on project name (top left)
2. Click "Settings" tab
3. Click "Environment Variables" (left sidebar)

#### 10.2 Add API Key

**Add variable:**
- Name: `ANTHROPIC_API_KEY`
- Value: `sk-ant-api03-your-key` (from Step 1)
- Environment: ✅ Production (checked)
- Click "Save"

#### 10.3 Add Business Variables (Optional)

Add these same as in local `.env`:
- `BUSINESS_NAME`
- `BUSINESS_LAT`
- `BUSINESS_LNG`
- `BUSINESS_CITY`
- `BUSINESS_STATE`

#### 10.4 Redeploy

**IMPORTANT:** Variables don't take effect until you redeploy!

1. Click "Deployments" tab
2. Click three dots (...) on latest deployment
3. Click "Redeploy"
4. Confirm "Redeploy"

**⏳ Wait 30 seconds...**

**✅ CHECKPOINT:** Deployment shows "Ready" status.

---

### STEP 11: Test Production Deployment (5 minutes)

**What this does:** Verifies your production APIs work before connecting to GHL.

#### 11.1 Open Production Test Console

Go to:
```
https://your-vercel-url.vercel.app/api/test-lead-validation
```

**Replace `your-vercel-url` with your actual URL from Step 9.**

#### 11.2 Run All 3 Tests

Same as Step 6, but now on production:

- Test 1: Should show ✅ LEAD QUALIFIED
- Test 2: Should show ✅ LEAD QUALIFIED
- Test 3: Should show ❌ LEAD NOT QUALIFIED

**✅ CHECKPOINT:** All tests pass in production (same as local).

**❌ ERROR: "Failed to generate"**
- Check Step 10 - make sure you added ANTHROPIC_API_KEY
- Check you redeployed after adding variables
- View logs: Deployments → Latest → Functions → Click function name

---

## 🔗 PHASE 3: GHL Integration (45 minutes)

**Goal:** Connect your APIs to GoHighLevel so leads automatically get validated and personalized copy.

---

### STEP 12: Understand GHL Workflow Structure (5 minutes - READ THIS)

**Before we build, understand what you're creating:**

#### Path 1: Cold Email Leads (Instantly.ai)
```
Instantly sends email
  ↓
Lead replies
  ↓
Instantly webhook → /api/instantly-webhook
  ↓
IF qualified → Create GHL contact
  ↓
GHL Workflow: "Cold Email Reply Handler"
  ↓
Calls /api/copywriter (lead_source: cold_email)
  ↓
Sends personalized follow-up
```

#### Path 2: Website Traffic Leads
```
Lead visits website/GMB
  ↓
GHL Workflow: "Virtual LPR - Lead Validator"
  ↓
Calls /api/virtual-lpr
  ↓
IF qualified → Update GHL contact
  ↓
Calls /api/copywriter (lead_source: website_traffic)
  ↓
Sends personalized email
```

**Key Difference:**
- **Path 1:** Humble, builds trust ("Thanks for replying...")
- **Path 2:** Confident, direct ("Saw you on our site...")

**✅ CHECKPOINT:** You understand we're building 2 separate workflows.

---

### STEP 13: Create GHL Custom Fields (10 minutes)

**What this does:** Creates places to store lead data (scores, distance, demographics).

#### 13.1 Log into GoHighLevel

1. Go to your GHL account
2. Make sure you're in the right sub-account (if agency)

#### 13.2 Navigate to Custom Fields

**Navigation:**
```
Settings (gear icon) → Custom Fields → Contacts
```

#### 13.3 Create Required Fields

**Click "+ New Field" for each:**

| Field Name | Field Type | Group | Description |
|------------|------------|-------|-------------|
| `lead_source` | Dropdown | Source | cold_email or website_traffic |
| `lead_temperature` | Dropdown | Source | cold, warm, hot |
| `vlpr_score` | Number | Scoring | Virtual LPR score (0-100) |
| `vlpr_signal_strength` | Number | Scoring | Signal strength (0-100) |
| `distance_miles` | Number | Demographics | Miles from business |
| `median_income` | Number | Demographics | ZIP code median income |
| `median_age` | Number | Demographics | ZIP code median age |
| `awareness_level` | Dropdown | Scoring | Schwartz awareness level |

**For dropdown fields, add options:**

`lead_source`:
- cold_email
- website_traffic

`lead_temperature`:
- cold
- warm
- hot

`awareness_level`:
- Unaware
- Problem Aware
- Solution Aware
- Product Aware
- Most Aware

#### 13.4 Verify Fields Created

**Navigation:**
```
Settings → Custom Fields → Contacts
```

**You should see 8 new fields in the list.**

**✅ CHECKPOINT:** All 8 custom fields exist and appear in the list.

**📸 SCREENSHOT:** Take a screenshot of your custom fields list.

---

### STEP 14: Create Workflow #1 - Website Traffic (Path 2) (15 minutes)

**Why Path 2 first?** It's simpler to test (no Instantly.ai needed).

#### 14.1 Create New Workflow

**Navigation:**
```
Marketing → Workflows → + Create Workflow
```

**Settings:**
- Name: `Virtual LPR - Lead Validator`
- Folder: (create new) `CircuitOS - Lead System`
- Status: Draft (we'll publish after testing)

**Click "Create"**

#### 14.2 Set Trigger

**Click "+ Add Trigger"**

**Choose:** Contact Tag Applied

**Settings:**
- Tag: `vLPR` (create new tag)
- **Explanation:** We'll manually add this tag to test contacts

**Click "Save"**

**✅ CHECKPOINT:** Trigger shows "When contact tag applied: vLPR"

#### 14.3 Add Action: Send Webhook (Virtual LPR)

**Click "+Add Action" below trigger**

**Choose:** Webhook → Send Outbound Webhook

**Settings:**

**Webhook URL:**
```
https://your-vercel-url.vercel.app/api/virtual-lpr
```
*(Replace with your actual Vercel URL)*

**Method:** POST

**Headers:**
```
Content-Type: application/json
```

**Body (Request Data):**
```json
{
  "signal_type": "website_visit",
  "signal_data": {
    "page_url": "{{contact.website}}",
    "location": {
      "city": "{{contact.city}}",
      "zip_code": "{{contact.postal_code}}",
      "lat": null,
      "lng": null
    },
    "ip_address": "{{contact.source_ip}}"
  },
  "business": {
    "name": "MetroFlex Gym",
    "city": "Arlington",
    "state": "Texas",
    "lat": 32.7357,
    "lng": -97.1081,
    "target_radius_miles": 10,
    "max_distance_miles": 25
  }
}
```

**Update the business section with YOUR business details!**

**Click "Save"**

**✅ CHECKPOINT:** Webhook action shows URL and method POST.

#### 14.4 Add Condition: Check if Qualified

**Click "+ Add Action"**

**Choose:** Conditions → IF/ELSE

**Condition:**
- Field: `Custom Value`
- Operator: `equals`
- Value: `{{webhook_response.qualified}}`
- Comparison: `true`

**Click "Save"**

**✅ CHECKPOINT:** You see an IF/ELSE split in the workflow.

#### 14.5 YES Branch: Update Contact

**Under "YES" branch, click "+ Add Action"**

**Choose:** CRM → Update Contact

**Fields to update:**

| Field | Value |
|-------|-------|
| `vlpr_score` | `{{webhook_response.ghl_integration.custom_fields.vlpr_score}}` |
| `vlpr_signal_strength` | `{{webhook_response.ghl_integration.custom_fields.vlpr_signal_strength}}` |
| `distance_miles` | `{{webhook_response.ghl_integration.custom_fields.distance_miles}}` |
| `median_income` | `{{webhook_response.ghl_integration.custom_fields.median_income}}` |
| `lead_source` | `website_traffic` |
| `lead_temperature` | `warm` |

**Tags to add:**
- `Virtual LPR - Qualified`
- `Lead Source - Website`

**Click "Save"**

**✅ CHECKPOINT:** Update Contact action shows 6 custom fields being set.

#### 14.6 NO Branch: Add Note

**Under "NO" branch, click "+ Add Action"**

**Choose:** CRM → Add Note

**Note:**
```
Virtual LPR Qualification Failed

Score: {{webhook_response.detection.signal_strength}}/100
Reason: {{webhook_response.detection.reasoning}}

Recommended: {{webhook_response.recommended_action}}
```

**Click "Save"**

**✅ CHECKPOINT:** Both YES and NO branches have actions.

#### 14.7 Save and Publish Workflow

**Click "Save" (top right)**

**Click "Publish"**

**✅ CHECKPOINT:** Workflow status shows "Published" with green dot.

---

### STEP 15: Test Workflow #1 with Real Contact (10 minutes)

**What this does:** Verifies your workflow actually works with a real test contact.

#### 15.1 Create Test Contact

**Navigation:**
```
Contacts → + New Contact
```

**Fill in:**
- First Name: `Test`
- Last Name: `User`
- Email: `test@example.com`
- Phone: `555-555-5555`
- City: `Arlington`
- Postal Code: `76011`

**Click "Save"**

**✅ CHECKPOINT:** Test contact appears in contacts list.

#### 15.2 Add vLPR Tag to Trigger Workflow

**On the contact page:**

1. Find "Tags" section
2. Click in tag field
3. Type: `vLPR`
4. Select "vLPR" from dropdown (or create it)
5. Tag gets added

**⏳ WORKFLOW WILL NOW RUN (takes 5-10 seconds)**

#### 15.3 Watch Workflow Execute

**Navigate to:**
```
Workflows → Virtual LPR - Lead Validator → History tab
```

**You should see:**
- New workflow execution
- Status: "Running..." then "Completed"
- Click on it to see details

**✅ CHECKPOINT:** Workflow shows "Completed" status.

#### 15.4 Verify Contact Was Updated

**Go back to your test contact:**

**Check Custom Fields section:**
- `vlpr_score` should have a number (e.g., 75)
- `distance_miles` should have a number (e.g., 2.3)
- `median_income` should have a number (e.g., 65320)
- `lead_source` should show "website_traffic"

**Check Tags:**
- Should have "Virtual LPR - Qualified"
- Should have "Lead Source - Website"

**✅ CHECKPOINT:** All custom fields populated and tags added!

**🎉 SUCCESS! Path 2 (Website Traffic) is working!**

**❌ TROUBLESHOOTING:**

**If workflow shows "Failed":**
1. Click on failed execution
2. Look for error message
3. Common issues:
   - Webhook URL has typo → Fix in workflow
   - Environment variable not set → Check Vercel Settings
   - Custom fields don't exist → Go back to Step 13

**If custom fields are empty:**
1. Check workflow execution details
2. Look at webhook response
3. Make sure field names match exactly (case-sensitive)

---

### STEP 16: Add Master Copywriter to Workflow (10 minutes)

**What this does:** Now that validation works, add copy generation.

#### 16.1 Edit Workflow

**Navigate to:**
```
Workflows → Virtual LPR - Lead Validator → Edit (pencil icon)
```

#### 16.2 Add Action After "Update Contact"

**In the YES branch, after "Update Contact", click "+ Add Action"**

**Choose:** Webhook → Send Outbound Webhook

**Settings:**

**Webhook URL:**
```
https://your-vercel-url.vercel.app/api/copywriter
```

**Method:** POST

**Body:**
```json
{
  "contact": {
    "first_name": "{{contact.first_name}}",
    "last_name": "{{contact.last_name}}",
    "email": "{{contact.email}}",
    "city": "{{contact.city}}",
    "state": "{{contact.state}}",
    "custom_fields": {
      "lpr_score": "{{contact.custom_fields.vlpr_score}}",
      "distance_miles": "{{contact.custom_fields.distance_miles}}",
      "vlpr_source": "website_visit"
    }
  },
  "channel": "email",
  "awareness_level": "Product Aware",
  "lead_source": "website_traffic",
  "touch_number": 1,
  "business": {
    "name": "MetroFlex Gym",
    "city": "Arlington",
    "state": "Texas",
    "type": "Hardcore powerlifting gym"
  }
}
```

**Update with YOUR business info!**

**Click "Save"**

#### 16.3 Store Generated Copy in Custom Fields

**Click "+ Add Action" after copywriter webhook**

**Choose:** CRM → Update Contact

**Create 3 new custom fields first (if you haven't):**
- `email_subject_a` (Text)
- `email_body_a` (Text Long)
- `recommended_variant` (Text)

**Then update:**

| Field | Value |
|-------|-------|
| `email_subject_a` | `{{webhook_response.copy.variants.0.subject}}` |
| `email_body_a` | `{{webhook_response.copy.variants.0.body}}` |
| `recommended_variant` | `{{webhook_response.copy.recommended_variant}}` |

**Click "Save"**

#### 16.4 Save and Re-Publish

**Click "Save" → "Publish"**

**✅ CHECKPOINT:** Workflow now has 3 actions in YES branch.

---

### STEP 17: Test Complete Flow (5 minutes)

#### 17.1 Create New Test Contact

**Why new contact?** To test from scratch.

**Create contact:**
- First Name: `Sarah`
- Last Name: `Martinez`
- Email: `sarah@example.com`
- City: `Arlington`
- Postal Code: `76011`

**Add tag:** `vLPR`

**⏳ Wait 10 seconds...**

#### 17.2 Check Results

**Go to contact, check custom fields:**

**From Virtual LPR:**
- ✅ `vlpr_score` (should be 60-80)
- ✅ `distance_miles` (should be ~2-5)
- ✅ `median_income` (should be ~60000-70000)

**From Copywriter:**
- ✅ `email_subject_a` (should have email subject)
- ✅ `email_body_a` (should have email body)
- ✅ Check if body mentions "Saw you on our site" or similar (website traffic tone)

**✅ CHECKPOINT:** All fields populated, copy sounds confident/direct.

**📸 SCREENSHOT:** Screenshot the custom fields section with all values filled.

**🎉 COMPLETE PATH 2 WORKING!**

---

## 🧪 PHASE 4: Testing & Verification (20 minutes)

**Goal:** Make sure everything works correctly before going live.

---

### STEP 18: Test Different Scenarios (10 minutes)

**Test these scenarios to verify your system adapts:**

#### Scenario 1: Close Lead (High Score)

**Create contact:**
- Name: Marcus Johnson
- City: Arlington
- ZIP: 76011 (same city as business)

**Add tag:** `vLPR`

**Expected Result:**
- `vlpr_score`: 75-85
- `distance_miles`: <3
- Copy tone: Urgent, mentions distance

#### Scenario 2: Far Lead (Lower Score)

**Create contact:**
- Name: David Chen
- City: Dallas
- ZIP: 75201 (30 miles away)

**Add tag:** `vLPR`

**Expected Result:**
- `vlpr_score`: 40-50 (or NOT qualified)
- `distance_miles`: ~30
- If qualified: Copy emphasizes "worth the drive"

#### Scenario 3: Different Income Area

**Create contact:**
- Name: Lisa Wong
- ZIP: 76002 (different income demographics)

**Add tag:** `vLPR`

**Expected Result:**
- `median_income`: Different from first test
- Copy should adapt slightly (if implemented)

**✅ CHECKPOINT:** System gives different scores based on location.

---

### STEP 19: Verify Framework Routing (5 minutes)

**Test that different awareness levels use different frameworks:**

#### Test: Solution Aware (Should use StoryBrand)

In your workflow, temporarily change this line in copywriter webhook:
```json
"awareness_level": "Solution Aware"
```

**Run workflow, check copy:**
- Should have hero's journey elements
- Should position business as "guide"
- Should have empathy statements

#### Test: Most Aware (Should use Hormozi)

Change to:
```json
"awareness_level": "Most Aware"
```

**Run workflow, check copy:**
- Should be very direct
- Should emphasize value equation
- Should have urgency/scarcity

**✅ CHECKPOINT:** Copy tone and structure changes with awareness level.

---

### STEP 20: Monitor and Debug (5 minutes)

**Learn how to see what's happening:**

#### 20.1 View GHL Workflow History

**Navigation:**
```
Workflows → Your Workflow → History tab
```

**You see:**
- All executions
- Success/failure status
- Execution time
- Click to see details

#### 20.2 View Vercel Function Logs

1. Go to: https://vercel.com/dashboard
2. Click your project
3. Click "Deployments" tab
4. Click latest deployment
5. Click "Functions" tab
6. Click function name (e.g., `api/virtual-lpr.js`)
7. See real-time logs

**What logs show:**
```
[Virtual LPR] Processing signal: website_visit
[Virtual LPR] Enriching with Census data for ZIP: 76011
[Virtual LPR] ✓ Lead QUALIFIED - Score: 85
```

**✅ CHECKPOINT:** You know how to view logs in both GHL and Vercel.

---

## 📋 PHASE 5: Going Live (Optional - When Ready)

**Do this when you're ready for real leads:**

---

### STEP 21: Connect to Real Lead Sources

#### Option A: Website Form

In your website form submission handler:
- Add tag `vLPR` to new contacts
- Workflow will auto-run

#### Option B: GMB Webhook

Set up GMB webhook to call your API directly:
```
https://your-url.vercel.app/api/virtual-lpr
```

#### Option C: Manual Testing

Add `vLPR` tag manually to real contacts to test before automation.

---

### STEP 22: Monitor Performance (Ongoing)

**First Week:**
- Check workflow execution rate: 90%+ success
- Check qualification rate: ~20-30% qualified (normal)
- Review generated copy quality
- Adjust awareness levels if needed

**Metrics to Track:**
```
Total leads → Virtual LPR → Qualified → Copy generated → Sent → Replied
```

**Target Performance:**
- Qualification rate: 20-30%
- Copy generation success: 99%+
- Email open rate: 45-55%
- Reply rate: 8-12%

---

## ✅ Final Checklist

**Before going fully live, verify:**

### Local Development:
- [ ] Code cloned locally
- [ ] Dependencies installed (`npm install`)
- [ ] `.env` file created with API key
- [ ] `vercel dev` runs successfully
- [ ] Local tests pass (curl commands work)
- [ ] Test console works locally

### Production Deployment:
- [ ] Vercel account created
- [ ] Repository imported to Vercel
- [ ] Environment variables added
- [ ] Redeployed after adding variables
- [ ] Production test console works
- [ ] All 3 tests pass in production

### GHL Integration:
- [ ] Custom fields created (8 fields)
- [ ] Workflow #1 created (Virtual LPR)
- [ ] Workflow published and tested
- [ ] Test contact validated successfully
- [ ] Master Copywriter added to workflow
- [ ] Generated copy stored in fields
- [ ] Complete flow tested end-to-end

### Verification:
- [ ] Different scenarios tested (close/far leads)
- [ ] Framework routing verified (awareness levels)
- [ ] Know how to view GHL workflow history
- [ ] Know how to view Vercel function logs
- [ ] Screenshots saved for reference

---

## 🆘 Common Issues & Solutions

### Issue: "Webhook returned 500 error"

**Check:**
1. Vercel logs (Deployments → Functions)
2. Error message usually says what's wrong
3. Common: ANTHROPIC_API_KEY not set or invalid

**Fix:**
1. Settings → Environment Variables
2. Verify key is correct
3. Redeploy

### Issue: "Custom fields not populating"

**Check:**
1. Field names match exactly (case-sensitive)
2. GHL workflow shows webhook response
3. Response has the data you're trying to map

**Fix:**
1. Test webhook manually first (Step 7)
2. Copy exact field names from response
3. Use `{{webhook_response.detection.field_name}}`

### Issue: "Workflow not triggering"

**Check:**
1. Workflow is Published (not Draft)
2. Tag name matches exactly
3. Contact has the tag applied

**Fix:**
1. Check workflow status (top right)
2. Verify trigger settings
3. Try removing and re-adding tag

### Issue: "Copy sounds wrong for lead source"

**Check:**
1. `lead_source` field in copywriter webhook body
2. Should be "cold_email" or "website_traffic"

**Fix:**
1. Edit workflow
2. Update copywriter webhook body
3. Ensure `lead_source` matches the path

---

## 📞 Next Steps

**You now have a working system!**

**Recommended progression:**

**Week 1: Testing**
- Run 20-30 test leads through system
- Verify all custom fields populate
- Review generated copy quality
- Adjust awareness levels if needed

**Week 2: Soft Launch**
- Connect to one real lead source (e.g., website form)
- Monitor 50-100 real leads
- Track qualification rate
- Fine-tune thresholds

**Week 3: Full Launch**
- Connect all lead sources
- Set up Instantly.ai webhook (Path 1)
- Monitor metrics daily
- Optimize based on data

**Month 2: Scale**
- A/B test copy variants
- Adjust framework routing
- Track conversion rates
- Scale up volume

---

## 🎓 What You Learned

Throughout this guide, you:

✅ Set up local development environment
✅ Tested APIs locally before deploying
✅ Deployed to Vercel production
✅ Created GHL custom fields
✅ Built complete workflow with webhooks
✅ Tested different scenarios
✅ Learned to monitor and debug

**You now have:**
- Production-ready lead validation system
- AI-powered copywriting with 4 frameworks
- Dual-path routing (cold vs warm)
- Complete GHL integration
- $0/month infrastructure cost

---

**© 2025 CircuitOS™**
**Complete Setup Guide - Local to Production**

**Questions?** Check VERCEL-DEPLOYMENT-GUIDE.md for more details.
**Issues?** Check logs in Vercel and GHL workflow history.

🚀 **You're ready to validate leads at scale!**
