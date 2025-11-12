# How to Update Your AI Agents Without Touching GHL
## Code Updates vs Workflow Updates - What Lives Where

**TL;DR:** Most updates happen in code (GitHub → Vercel). GHL rarely needs changes.

---

## 🏗️ ARCHITECTURE: What Lives Where

### 1️⃣ **Code (GitHub + Vercel)** - YOU CONTROL THIS
**Location:** `/home/user/Circuitos/api/`

**What's here:**
- Claude Agent Memory API (`claude-agent-memory.js`)
- Memory Manager (`lib/memory-manager.js`)
- AI prompts and logic
- DMN Protocol system prompts
- Lead scoring algorithms
- Copy generation frameworks
- ML feedback processing

**How to update:**
```bash
# 1. Edit code in GitHub (via Claude Code or locally)
# 2. Commit changes
git add api/
git commit -m "Update: Improved lead scoring prompt"
git push

# 3. Deploy to Vercel (auto-deploys if connected, or manual)
npx vercel --prod

# 4. Done! GHL automatically uses new version
```

**GHL workflows don't need to change** because they just call the same API endpoint.

---

### 2️⃣ **Workflow Configuration (GHL)** - RARELY CHANGES
**Location:** GoHighLevel dashboard

**What's here:**
- Triggers (when workflow starts)
- Conditions (if/else logic)
- Webhook URLs (point to your Vercel API)
- Action sequences (send SMS, email, etc.)

**When you need to update GHL:**
- Change workflow structure (add new steps, change routing)
- Add new triggers or conditions
- Change webhook URL (if you move to different hosting)
- Modify SMS/email templates in GHL (if not using agent-generated)

**When you DON'T need to update GHL:**
- Improve AI prompts
- Change lead scoring logic
- Update agent behavior
- Add new features to the API
- Fix bugs in agent logic

---

## 🎯 EXAMPLES: What Can You Update Without Touching GHL?

### Example 1: Improve Lead Scoring Prompt

**Scenario:** You want lead scorer to be more aggressive with GMB directions clicks

**Update in Code (via Claude or GitHub):**
```javascript
// File: api/claude-agent-memory.js

const DMN_PROMPTS = {
  'Lead Scorer': `You are the Lead Scorer for Circuit OS™...

  // OLD:
  - GMB directions clicked: +10 intent points

  // NEW (just edit this):
  - GMB directions clicked: +15 intent points
  - If distance < 1 mile: +5 bonus points

  ...`
};
```

**Deploy:**
```bash
git add api/claude-agent-memory.js
git commit -m "Update: Increase GMB directions weight to +15 points"
git push
npx vercel --prod
```

**GHL Change Needed:** ❌ NONE

**Result:** Next time GHL calls the API, it automatically uses the new scoring logic!

---

### Example 2: Add New Agent Feature (Check Competitor Proximity)

**Scenario:** You want lead scorer to check if there are competitors nearby

**Update in Code:**
```javascript
// File: api/claude-agent-memory.js

async function scoreLead(req, res, contactId, businessId, data, useMemory) {
  const { contact, business } = data;

  // NEW: Add competitor analysis
  const competitorCount = await checkNearbyCompetitors(
    business.location,
    business.category,
    2 // within 2 miles
  );

  // Update prompt to include competitor context
  let userPrompt = `Score this lead...

  COMPETITOR ANALYSIS:
  - Competitors within 2 miles: ${competitorCount}
  - If 5+ competitors: Lower timing score by 5 points (high competition)
  - If 0-2 competitors: Increase timing score by 5 points (low competition)

  ...`;

  // Rest of code stays the same
}
```

**Deploy:**
```bash
git add api/claude-agent-memory.js
git commit -m "Add: Competitor proximity analysis to lead scoring"
git push
npx vercel --prod
```

**GHL Change Needed:** ❌ NONE

**Result:** Lead scoring now considers competitor density automatically!

---

### Example 3: Change Copywriter Framework

**Scenario:** You want to use a different copywriting framework for emails

**Update in Code:**
```javascript
// File: api/claude-agent-memory.js

const DMN_PROMPTS = {
  'Copywriter': `You are the Master Copywriter...

  // OLD:
  Your role: Generate copy using Russell Brunson's Hook-Story-Offer

  // NEW (just change the prompt):
  Your role: Generate copy using:
  - Gary Halbert's "Reason Why" framework
  - David Ogilvy's headline formulas
  - Clayton Makepeace's fascinations

  ...`
};
```

**Deploy:**
```bash
git add api/claude-agent-memory.js
git commit -m "Update: Switch to Halbert + Ogilvy copywriting framework"
git push
npx vercel --prod
```

**GHL Change Needed:** ❌ NONE

**Result:** All new emails use the updated copywriting approach!

---

### Example 4: Fix a Bug in Memory Retrieval

**Scenario:** Memory manager is loading too many old messages, slowing down API

**Update in Code:**
```javascript
// File: api/lib/memory-manager.js

async getConversationHistory(contactId, maxTurns = 20) {
  // OLD: Load 20 turns (40 messages)
  // NEW: Load only 10 recent turns (20 messages)

  const { data, error } = await supabase
    .from('conversation_history')
    .select('role, content, agent_name, metadata, created_at')
    .eq('contact_id', contactId)
    .order('created_at', { ascending: true })
    .limit(10 * 2); // Changed from 20 * 2

  // Rest stays the same
}
```

**Deploy:**
```bash
git add api/lib/memory-manager.js
git commit -m "Fix: Reduce memory retrieval to 10 turns for speed"
git push
npx vercel --prod
```

**GHL Change Needed:** ❌ NONE

**Result:** API responses are faster, GHL workflows work exactly the same!

---

## 🔄 THE WORKFLOW: How to Update Code via Claude Code (Me!)

### Option 1: Ask Me to Make Changes (Easiest)

**Just tell me what you want:**

> "Claude, update the lead scorer to give GMB directions clicks a higher weight"

> "Claude, change the copywriter to use Gary Halbert's framework instead"

> "Claude, add competitor analysis to the scoring algorithm"

**I'll:**
1. Edit the code files
2. Commit to GitHub
3. Tell you to deploy to Vercel (`npx vercel --prod`)
4. Done! GHL uses new version automatically

### Option 2: Edit Code Locally (If You Prefer)

```bash
# 1. Pull latest code
cd /home/user/Circuitos
git pull

# 2. Edit files in your IDE
# (api/claude-agent-memory.js, api/lib/memory-manager.js, etc.)

# 3. Commit and push
git add .
git commit -m "Your changes"
git push

# 4. Deploy to Vercel
npx vercel --prod
```

---

## ⚠️ WHEN YOU *DO* NEED TO UPDATE GHL

### Scenario 1: Add New Workflow Step

**Example:** You want to add a "Wait 4 hours" between SMS and email (instead of 2 hours)

**Where to change:** GHL Workflows UI
- Open workflow
- Find "Wait for Engagement" action
- Change duration from "2 hours" to "4 hours"
- Save

**Code change needed:** ❌ NONE

---

### Scenario 2: Change Webhook URL

**Example:** You move from Vercel to AWS Lambda

**Where to change:** GHL Workflows UI
- Open workflow
- Find all "Webhook" actions
- Update URL from `https://old-vercel.app/api/...` to `https://new-aws.com/api/...`
- Save

**Code change:** You'd deploy the same code to AWS instead of Vercel

---

### Scenario 3: Add New Custom Field

**Example:** You want to track "competitor_count" in GHL

**Where to change:**
1. **GHL Settings:** Create custom field `competitor_count`
2. **GHL Workflow:** Add action to store `{{webhook_response.competitor_count}}` in custom field
3. **Code:** Update API to return `competitor_count` in response

**Both GHL and code need updates** for this one.

---

## 📊 COMPARISON: Code Updates vs GHL Updates

| What You Want to Change | Update Code? | Update GHL? | Time Required |
|--------------------------|--------------|-------------|---------------|
| Improve AI prompts | ✅ | ❌ | 5 minutes |
| Change lead scoring logic | ✅ | ❌ | 10 minutes |
| Add new agent features | ✅ | ❌ | 15-30 minutes |
| Fix bugs in agent code | ✅ | ❌ | 5-15 minutes |
| Change copywriting framework | ✅ | ❌ | 5 minutes |
| Adjust memory retention | ✅ | ❌ | 5 minutes |
| Update ML feedback logic | ✅ | ❌ | 10 minutes |
| **Add new workflow step** | ❌ | ✅ | 10 minutes |
| **Change SMS/email timing** | ❌ | ✅ | 5 minutes |
| **Add new trigger** | ❌ | ✅ | 10 minutes |
| **Change webhook URL** | ❌ | ✅ | 5 minutes |
| **Add new custom field** | ✅ | ✅ | 15 minutes |

**Key insight:** 80% of improvements = code updates only (no GHL changes needed!)

---

## 🎯 REAL-WORLD UPDATE SCENARIO

**Month 1:** You launch with basic lead scoring

**Month 2:** You notice GMB directions leads convert 20% better than expected

**What you want:** Increase LPR score weight for GMB directions from 10 → 15 points

**How to update:**

**Via Claude Code (ask me):**
> "Claude, increase the GMB directions weight in lead scoring from 10 to 15 points"

**I do:**
```bash
# 1. Edit api/claude-agent-memory.js
# 2. Change scoring logic
# 3. Commit to git
git commit -m "Update: GMB directions weight +15 (was +10)"
# 4. Push to GitHub
git push
```

**You do:**
```bash
# Just redeploy to Vercel
npx vercel --prod
```

**Time:** 2 minutes total

**GHL changes:** ZERO

**Result:** All future leads get the improved scoring automatically!

---

## 🚀 CONTINUOUS IMPROVEMENT WORKFLOW

### The Beautiful Part:

```
You spot improvement → Tell me what to change → I update code → You deploy
    ↓
GHL workflows keep working exactly the same
    ↓
Leads get better AI immediately
    ↓
Repeat weekly/monthly as you learn what works
```

**No GHL reconfiguration. No workflow rebuilding. Just code updates.**

---

## 💡 PRO TIPS

### 1. Use Git Branches for Experiments

**Test new scoring logic without affecting production:**

```bash
# Create experiment branch
git checkout -b experiment/new-scoring-logic

# I update the code with new logic
git commit -m "Experiment: New scoring algorithm"
git push

# Deploy to Vercel preview (not production)
npx vercel

# You get a preview URL: https://preview-xyz.vercel.app
# Test it in GHL by temporarily changing webhook URL
# If it works, merge to main and deploy to production
```

### 2. Version Your Prompts

**Track prompt changes over time:**

```javascript
// api/claude-agent-memory.js

const DMN_PROMPTS = {
  'Lead Scorer': `
    VERSION: 2.1.0
    LAST UPDATED: 2025-01-15
    CHANGES: Increased GMB directions weight to +15

    You are the Lead Scorer...
  `
};
```

### 3. Use Environment Variables for Quick Tweaks

**Change scoring weights without code changes:**

```javascript
// In Vercel dashboard: Settings → Environment Variables
GMB_DIRECTIONS_WEIGHT=15
PROXIMITY_BONUS=5

// In code:
const gmbWeight = parseInt(process.env.GMB_DIRECTIONS_WEIGHT) || 10;
const proximityBonus = parseInt(process.env.PROXIMITY_BONUS) || 0;
```

**Update weight:** Vercel dashboard → Change env var → Redeploy
**No code commit needed!**

---

## 📚 SUMMARY

### ✅ What You CAN Update Without Touching GHL:
- AI prompts (scoring, copywriting, review responses)
- Agent logic and decision-making
- Memory retrieval settings
- ML feedback processing
- Bug fixes
- New features in the API
- Response format changes (as long as GHL expects same fields)

### ⚠️ What Requires GHL Updates:
- Workflow structure (add/remove steps)
- Timing changes (wait durations)
- New triggers or conditions
- Webhook URLs (if you change hosting)
- New custom fields (must create in GHL + map in workflow)

### 🎯 The 80/20 Rule:
**80% of improvements = code updates only**
**20% of changes = require GHL configuration**

---

## 🔄 UPDATE WORKFLOW (Step-by-Step)

### When You Want to Improve Something:

**Step 1:** Tell me what you want to change
> "Claude, make lead scoring more aggressive for high-intent signals"

**Step 2:** I update the code and commit to git
> "✅ Updated lead scorer prompt. Committed to git."

**Step 3:** You deploy to Vercel
```bash
npx vercel --prod
```

**Step 4:** Test in GHL
> Trigger workflow with test lead → Verify new behavior

**Step 5:** Monitor results
> Check Supabase `agent_feedback` table after 50 leads → Adjust as needed

**Step 6:** Repeat!

---

## ✅ CONCLUSION

**Yes, you can control and update AI logic entirely through code (GitHub/Claude Code) without touching GHL!**

**The separation is:**
- **Code (you control via Git):** AI intelligence, prompts, logic, features
- **GHL (you configure once):** Workflow structure, triggers, routing

**This means:**
- Fast iteration on AI quality
- Version-controlled improvements
- No workflow reconfiguration headaches
- Easy rollback if something breaks

**Ask me anytime to update agent prompts, scoring logic, or features. I'll handle the code, you just redeploy!**

---

**© 2025 Circuit OS™**
**Update AI Intelligence, Not Workflows**
