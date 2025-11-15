# GHL Copy-Paste Setup Guide
## Zero-Coding Required - Just Copy & Paste

**Time to Complete:** 30-60 minutes
**Difficulty:** Beginner (No coding knowledge needed)
**Result:** Fully automated AI sales system

---

## 🎯 HOW THIS WORKS

Each AI Employee comes in **3 simple pieces:**

### Piece 1: System Prompt (Copy-Paste)
- Open the AI employee file (e.g., `01-Lead-Scorer.md`)
- Find section: **"SYSTEM PROMPT (Copy-Paste to GHL)"**
- Copy EVERYTHING inside the code block
- Paste into GHL AI Employee → System Prompt field
- **Done!**

### Piece 2: Input Variables (Click to Add)
- Same file, find section: **"Input Variables"**
- See list like: `{{contact.first_name}}`
- In GHL, click "Add Variable"
- Type or select each variable from list
- **Done!**

### Piece 3: Output Mapping (Point & Click)
- Same file, find section: **"Output Format"**
- See example like: `{"total_score": 78}`
- In GHL workflow, add "Update Contact" action
- Map: `total_score` → Custom Field: `lpr_score`
- **Done!**

---

## 📦 MODULAR STRUCTURE

Each AI Employee is **100% self-contained:**

```
01-Lead-Scorer.md
├── ✅ Complete System Prompt (ready to paste)
├── ✅ Input Variables List (copy names)
├── ✅ Output Format Example (see what you'll get)
├── ✅ Testing Data (verify it works)
├── ✅ GHL Configuration Screenshots (step-by-step)
└── ✅ Troubleshooting Guide (if something goes wrong)
```

**No dependencies:** Each employee works independently
**No coding:** Just copy-paste text
**No APIs to configure:** Everything uses GHL's built-in AI

---

## 🚀 EXAMPLE: Setting Up Lead Scorer (10 minutes)

### Step 1: Open GHL (1 min)
```
1. Log in to GoHighLevel
2. Settings → AI & Automations → AI Employees
3. Click "+ New AI Employee"
```

### Step 2: Copy Basic Info (1 min)
```
From: 01-Lead-Scorer.md → Section "CONFIGURATION"

Copy to GHL:
- Name: Lead Scorer
- Description: Scores leads 0-100 using BANT/MEDDIC/CHAMP frameworks
- Model: GPT-4
- Temperature: 0.3
```

### Step 3: Copy System Prompt (2 min)
```
From: 01-Lead-Scorer.md → Section "SYSTEM PROMPT"

1. Find the big code block that starts with:
   "You are the Lead Scorer for Circuit OS™..."

2. Copy ENTIRE block (includes full training)

3. Paste into GHL → "System Prompt" field

4. Click "Save"
```

**That's it for the AI Employee!**

### Step 4: Add Input Variables (3 min)
```
From: 01-Lead-Scorer.md → Section "Input Variables"

In GHL AI Employee Settings:
1. Click "Add Variable"
2. Type: contact.first_name (or select from dropdown)
3. Click "Add"
4. Repeat for:
   - contact.last_name
   - contact.email
   - contact.phone
   - contact.custom_fields.distance_miles
   - contact.custom_fields.neighborhood
   - ... (all listed in file)

OR

Use GHL's "Add All Contact Fields" button (easier!)
```

### Step 5: Test It (3 min)
```
From: 01-Lead-Scorer.md → Section "TESTING"

1. In GHL AI Employee → Click "Test"
2. Paste test data from file
3. Click "Run Test"
4. Verify output matches expected format
5. If good → Click "Publish"
```

**Done! Lead Scorer is live.**

---

## 📋 COMPLETE CHECKLIST (Do Once)

Before building AI employees, do these setup steps:

### ✅ One-Time Setup (20 min)

**1. Enable AI Unlimited ($97/mo)**
- [ ] Settings → Billing → Add-ons
- [ ] Find "AI Unlimited"
- [ ] Click "Enable"
- [ ] Confirm billing

**2. Add Custom Fields (15 min)**
- [ ] Open: `Custom-Fields/custom-fields-schema.csv`
- [ ] Settings → Custom Fields
- [ ] Click "+ New Custom Field" for each row
- [ ] OR import CSV if GHL supports it

**Example fields to add:**
```
Field Name          | Type    | Group
--------------------|---------|----------
lpr_score           | Number  | Scoring
fit_score           | Number  | Scoring
intent_score        | Number  | Scoring
timing_score        | Number  | Scoring
awareness_level     | Dropdown| Scoring (options: Unaware, Problem Aware, Solution Aware, Product Aware, Most Aware)
distance_miles      | Number  | Location
neighborhood        | Text    | Location
median_income       | Number  | Demographics
intent_signal       | Text    | Behavior
last_action_date    | Date    | Behavior
```

**3. Create Field Groups (5 min)**
- [ ] In Custom Fields, create groups:
  - Scoring
  - Location
  - Demographics
  - Behavior
  - Campaigns

This organizes your fields neatly.

---

## 🎨 VISUAL GUIDE (What You'll See)

### In GHL, You'll Fill Out Forms Like This:

**AI Employee Setup Screen:**
```
┌─────────────────────────────────────────┐
│ Create AI Employee                       │
├─────────────────────────────────────────┤
│                                          │
│ Name: [Lead Scorer]                     │
│                                          │
│ Description:                             │
│ [Scores leads 0-100 using BANT/MEDDIC/  │
│  CHAMP frameworks]                       │
│                                          │
│ Model: [GPT-4 ▼]                        │
│                                          │
│ Temperature: [0.3]                       │
│                                          │
│ System Prompt:                           │
│ ┌─────────────────────────────────────┐ │
│ │ You are the Lead Scorer for         │ │
│ │ Circuit OS™, the world's most...    │ │
│ │                                      │ │
│ │ [PASTE ENTIRE PROMPT HERE]          │ │
│ │                                      │ │
│ │ (Will be 500-1000 lines)            │ │
│ └─────────────────────────────────────┘ │
│                                          │
│ Input Variables:                         │
│ [+ Add Variable]                         │
│   ✓ contact.first_name                  │
│   ✓ contact.email                       │
│   ✓ contact.custom_fields.lpr_score    │
│                                          │
│ [Save & Test]  [Publish]                │
└─────────────────────────────────────────┘
```

**That's it!** No code, no complexity.

---

## 📚 ALL 7 AI EMPLOYEES (Same Easy Process)

Each one takes **5-10 minutes** to set up:

### Employee 1: Lead Scorer
**File:** `01-Lead-Scorer.md`
**Purpose:** Score all new leads 0-100
**Setup Time:** 10 min (your first one, includes learning)

### Employee 2: Master Copywriter
**File:** `02-Master-Copywriter.md`
**Purpose:** Generate email/SMS/LinkedIn copy
**Setup Time:** 7 min (you'll be faster now)

### Employee 3: Email Campaign Manager
**File:** `03-Email-Campaign-Manager.md`
**Purpose:** Manage Instantly.ai sequences
**Setup Time:** 7 min

### Employee 4: Channel Router
**File:** `04-Channel-Router.md`
**Purpose:** Decide: Email → LinkedIn → SMS → Call
**Setup Time:** 5 min

### Employee 5: Reputation Guardian
**File:** `05-Reputation-Guardian.md`
**Purpose:** Respond to reviews automatically
**Setup Time:** 7 min

### Employee 6: Content Creator
**File:** `06-Content-Creator.md`
**Purpose:** Write blog posts, GMB posts
**Setup Time:** 7 min

### Employee 7: Search Optimizer
**File:** `07-Search-Optimizer.md`
**Purpose:** Optimize for ChatGPT/Perplexity
**Setup Time:** 5 min

**Total Setup Time: 48 minutes** (all 7 employees)

---

## 🔄 WORKFLOW SETUP (Also Copy-Paste)

After AI employees are built, you'll create workflows:

### Workflow Template Structure:

**Each workflow file has:**
```markdown
## WORKFLOW NAME: New Lead Processor

### Trigger (Copy This)
- Trigger Type: Contact Created
- Filter: Tag = "vLPR"

### Step 1 (Copy This)
- Action: Wait
- Duration: 1 minute

### Step 2 (Copy This)
- Action: AI Employee
- Select: "Lead Scorer"
- Input: {{contact}}
- Store Output In: custom_fields.lpr_score

### Step 3 (Copy This)
- Action: Condition
- IF: {{custom_fields.lpr_score}} >= 70
- THEN: Add Tag "High Intent"
- ELSE: Go to Step 4

... (etc)
```

**You just:**
1. Read the step
2. Click the buttons in GHL that match
3. Copy-paste any text needed
4. Move to next step

**No thinking required!**

---

## 🎯 SIMPLIFIED WORKFLOW BUILDER

**GHL's visual workflow builder looks like:**

```
┌─────────────────────────────────────────┐
│ New Lead Processor                       │
├─────────────────────────────────────────┤
│                                          │
│  [Trigger: Contact Created]              │
│          ↓                               │
│  [Wait: 1 minute]                        │
│          ↓                               │
│  [AI Action: Lead Scorer]                │
│          ↓                               │
│  [Update Contact: lpr_score]             │
│          ↓                               │
│  ╔═══════╗                               │
│  ║ IF    ║ score >= 70?                 │
│  ╚═══════╝                               │
│     ↙         ↘                          │
│  YES          NO                         │
│    ↓           ↓                         │
│ [Add Tag]  [Add Tag]                     │
│ "High"     "Medium"                      │
│                                          │
└─────────────────────────────────────────┘
```

**You build this by:**
1. Drag boxes onto canvas
2. Connect them with arrows
3. Fill in values from our template
4. Click "Save"

**Total time per workflow: 10-15 minutes**

---

## 🛠️ TROUBLESHOOTING (Copy-Paste Solutions)

### Problem: AI Employee returns error

**Solution in file:**
```
See: Testing/troubleshooting-guide.md

Common Error: "Invalid JSON output"
Fix: Check system prompt, ensure it says:
     "Return ONLY valid JSON, no extra text"

Quick Fix (copy-paste):
Add to end of system prompt:
"CRITICAL: Your response must be ONLY valid JSON.
No explanations, no markdown, just pure JSON."
```

### Problem: Custom field not updating

**Solution in file:**
```
See: Workflows/common-issues.md

Issue: Output not mapping to field
Fix:
1. Check field name matches exactly (case-sensitive)
2. Field type matches output (Number vs Text)
3. Workflow has "Update Contact" action after AI call

Quick Fix Template:
Action: Update Contact
Field: custom_fields.lpr_score
Value: {{ai_response.total_score}}
```

---

## ✅ SUCCESS CHECKLIST

After setup, verify these:

**AI Employees (7 total):**
- [ ] Lead Scorer - Status: Published
- [ ] Master Copywriter - Status: Published
- [ ] Email Campaign Manager - Status: Published
- [ ] Channel Router - Status: Published
- [ ] Reputation Guardian - Status: Published
- [ ] Content Creator - Status: Published
- [ ] Search Optimizer - Status: Published

**Custom Fields (~50 core fields):**
- [ ] All "Scoring" fields added
- [ ] All "Location" fields added
- [ ] All "Demographics" fields added
- [ ] All "Behavior" fields added
- [ ] All "Campaign" fields added

**Workflows (5 core workflows):**
- [ ] New Lead Processor - Status: Active
- [ ] High-Intent Cold Email - Status: Active
- [ ] Omnichannel Follow-Up - Status: Active
- [ ] Review Response Handler - Status: Active
- [ ] Content Publishing - Status: Active

**Testing:**
- [ ] Test lead created
- [ ] Test lead scored (check custom fields)
- [ ] Test email generated
- [ ] All workflows executed without errors

---

## 🎉 THAT'S IT!

**No coding. No APIs. No complexity.**

**Just:**
1. Open file
2. Copy section
3. Paste into GHL
4. Repeat for each employee/workflow

**Time investment: 2-3 hours total**
**Result: World-class AI sales system**

---

**Next Step:** I'll build the remaining 6 AI employees in this exact format.

Each will have:
- ✅ Copy-paste system prompt
- ✅ Clear input variables list
- ✅ Output format example
- ✅ Testing data
- ✅ Step-by-step GHL setup guide
- ✅ Screenshots (when helpful)
- ✅ Troubleshooting section

**You'll literally just copy-paste and click buttons.**

---

**© 2025 CircuitOS™**
**GHL Copy-Paste Setup - Zero Coding Required**
