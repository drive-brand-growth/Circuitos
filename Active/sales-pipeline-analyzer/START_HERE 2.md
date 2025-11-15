# 🚀 Sales Pipeline Analyzer - START HERE

## What This Does

Analyzes your sales pipeline to identify:
- ✅ **Velocity issues**: Deals moving too slowly
- ✅ **Risk signals**: Stalled, ghosting, weak qualification
- ✅ **Health scores**: 0-100 for each opportunity
- ✅ **Coaching opportunities**: Specific actions tied to MEDDIC, SPIN, Gap Selling, etc.
- ✅ **Performance insights**: By rep, by stage, by age cohort
- ✅ **Forecast adjustments**: Reality-based projections

---

## Quick Setup (5 Minutes)

### Step 1: Create Gemini Gem
1. Go to https://gemini.google.com/
2. Click "Gems" → "New Gem"
3. Name: **"Sales Pipeline Analyzer"**

### Step 2: Paste Instructions
1. Open **GEMINI_INSTRUCTIONS.md**
2. Copy ENTIRE file
3. Paste into Gemini Gem "Instructions" field
4. Save

### Step 3: Upload Knowledge Base (2 files)
- `reference/velocity-risk-framework.md`
- `reference/coaching-playbook.md`

### Step 4: Test
Upload a CSV with your opportunities (see format below)

---

## CSV Format Required

### Minimum Fields:
```csv
opportunity_id,opportunity_name,created_date,stage,close_date,amount,owner
OPP-001,Acme Corp,2025-01-15,Proposal,2025-11-15,50000,John Smith
```

### Optional (Enhances Analysis):
- `last_activity_date`
- `probability`
- `stage_history` (format: "Stage1:Date1,Stage2:Date2")

---

## What You'll Get

**Executive Summary**:
- Health distribution (% Healthy, At Risk, Critical)
- Top 5 risks requiring immediate action
- Velocity trends (Rocket Ships, Stalled, Ghost Towns)

**Deal-by-Deal Analysis**:
- Health score (0-100)
- Velocity metrics (time in stage, age, momentum)
- Risk indicators (stall, slippage, qualification gaps)
- Coaching recommendations (framework-specific actions)

**Team Performance**:
- By rep (avg health, deals at risk)
- By stage (where deals get stuck)
- By age cohort (are older deals healthier or riskier?)

**Coaching Priorities**:
- Top 5 issues with specific actions
- Frameworks to apply (MEDDIC, SPIN, Sandler, etc.)

---

## Files Included

- **START_HERE.md** ← You are here
- **GEMINI_INSTRUCTIONS.md** ← Copy into Gem
- **reference/velocity-risk-framework.md** ← Upload to Gem
- **reference/coaching-playbook.md** ← Upload to Gem

---

## Ready?

1. Set up Gemini Gem (5 min)
2. Upload your pipeline CSV
3. Get world-class analysis in 2-3 minutes

**Let's optimize your pipeline!** 🚀
