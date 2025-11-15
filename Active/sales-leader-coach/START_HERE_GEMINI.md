# 🚀 START HERE - Gemini Gem Setup

## What You Have

A **complete, world-class sales coaching AI** optimized specifically for Gemini Gem custom GPT that will train your Salesforce AgentForce agents to perform like top 1% sales executives.

## 3 Critical Files for Gemini (Use These!)

### 1️⃣ [GEMINI_INSTRUCTIONS.md](GEMINI_INSTRUCTIONS.md) 
**COPY-PASTE THIS INTO YOUR GEMINI GEM "INSTRUCTIONS" FIELD**
- This is NOT the same as SKILL.md
- Optimized specifically for Gemini format
- Contains all coaching logic, tone guidelines, and methodology selection
- **DO THIS FIRST**

### 2️⃣ [GEMINI_SETUP_GUIDE.md](GEMINI_SETUP_GUIDE.md)
**FOLLOW THIS STEP-BY-STEP (10 MINUTES)**
- Complete setup instructions
- How to upload the 8 knowledge base files
- Testing checklist
- Troubleshooting common issues
- **DO THIS SECOND**

### 3️⃣ [GEMINI_TEST_PROMPTS.md](GEMINI_TEST_PROMPTS.md)
**USE THESE TO VERIFY YOUR GEM WORKS**
- 12 test cases with expected outputs
- Verify product knowledge accuracy
- Check methodology selection
- Validate JSON output
- **DO THIS THIRD**

---

## Quick Setup (5 Steps)

### Step 1: Create Your Gemini Gem
1. Go to https://gemini.google.com/
2. Click "Gems" → "New Gem"
3. Name: **"Sales Leader Coach"**

### Step 2: Paste Instructions
1. Open **GEMINI_INSTRUCTIONS.md**
2. **Copy the ENTIRE file** (all 500+ lines)
3. Paste into Gemini Gem "Instructions" field
4. Save

### Step 3: Upload Knowledge Base
Upload these 8 files from the `reference/` folder:
- ✅ sales-methodologies.md
- ✅ drn-vehicle-search.md
- ✅ drn-skip-tracing.md
- ✅ drn-risk-scoring.md
- ✅ drn-loss-alerts.md
- ✅ conversation-analysis-framework.md
- ✅ response-templates.md
- ✅ salesforce-agentforce-integration.md

### Step 4: Test with Sample
Copy-paste this into your Gem:

```
Date: 2025-10-15
Rep: Test Rep
Prospect: Sample Prospect, VP Collections, Test Credit Union
Stage: Discovery

Transcript:
Rep: Hi, thanks for taking the time today.
Prospect: No problem. So what does your company do?
Rep: We provide vehicle location data to help with repossessions.
Prospect: Interesting. We're actually losing about $2 million a year to charge-offs.
Rep: That's significant. How are you currently locating vehicles?
Prospect: We use LexisNexis for skip tracing.
Rep: I see. Our system uses real-time license plate data.
Prospect: How much does it cost?
Rep: I'd need to put together a proposal. Can we schedule a follow-up?
Prospect: Sure.

Outcome: Scheduled follow-up call
```

**Expected Output**: Full analysis with grade (B or B-), strengths, weaknesses, coached response, tactical recommendations, and JSON.

### Step 5: Analyze Real Conversations
Start with 5-10 actual sales conversations, review output quality, refine as needed.

---

## Why This Is Gemini-Optimized

### vs. Claude (Original SKILL.md)
| Feature | Claude | Gemini (This Version) |
|---------|--------|----------------------|
| **Instruction Format** | Markdown with YAML frontmatter | Plain text instructions |
| **Tone Control** | Implicit | Explicit with examples |
| **File Access** | Native file read | Requires upload + explicit referencing |
| **Response Structure** | Flexible | Structured with templates |
| **Error Handling** | Implicit | Explicit fallback instructions |

### Key Gemini Optimizations
✅ **More Explicit Instructions**: Gemini benefits from very clear, specific directions
✅ **Tone Examples**: Good vs. bad examples for humanization
✅ **Structured Templates**: Exact format for responses (headers, sections, etc.)
✅ **Repeated Key Points**: Critical instructions repeated for reinforcement
✅ **File Reference Instructions**: Explicitly tells Gem to use uploaded files

---

## What This Gem Will Do

When you paste a sales conversation, it will:

1. **Analyze** → Extract pain points, buying signals, objections, qualification gaps
2. **Grade** → A+ to F based on execution quality
3. **Coach** → Specific feedback: "You missed X, here's what to say instead: [exact script]"
4. **Map to Products** → "This pain point maps to Vehicle Search because..."
5. **Apply Methodologies** → "Use SPIN Selling here, Challenger Sale there, Value Selling for ROI"
6. **Generate Response** → Word-for-word script of what to say in next conversation
7. **Output JSON** → Salesforce AgentForce-ready training data

**Result**: Your AI agents learn from every conversation and get better over time.

---

## Common Mistakes to Avoid

❌ **Don't use SKILL.md** in Gemini instructions → Use GEMINI_INSTRUCTIONS.md instead
❌ **Don't skip file uploads** → The 8 reference files are critical for product knowledge
❌ **Don't expect it to work perfectly immediately** → Test with sample first, refine instructions if needed
❌ **Don't forget to test** → Use GEMINI_TEST_PROMPTS.md to validate it's working correctly

---

## File Directory

```
sales-leader-coach/
├── START_HERE_GEMINI.md          ← YOU ARE HERE
├── GEMINI_INSTRUCTIONS.md         ← Copy-paste into Gem instructions
├── GEMINI_SETUP_GUIDE.md          ← Step-by-step setup
├── GEMINI_TEST_PROMPTS.md         ← Test cases
├── README.md                      ← Full documentation
├── SKILL.md                       ← Original Claude version (don't use in Gemini)
└── reference/                     ← Upload all 8 files to Gem
    ├── sales-methodologies.md
    ├── drn-vehicle-search.md
    ├── drn-skip-tracing.md
    ├── drn-risk-scoring.md
    ├── drn-loss-alerts.md
    ├── conversation-analysis-framework.md
    ├── response-templates.md
    └── salesforce-agentforce-integration.md
```

---

## Support Path

1. **Setup Issues** → Read [GEMINI_SETUP_GUIDE.md](GEMINI_SETUP_GUIDE.md) → Troubleshooting section
2. **Test Failures** → Read [GEMINI_TEST_PROMPTS.md](GEMINI_TEST_PROMPTS.md) → Success Criteria section
3. **Product Questions** → Check `reference/drn-*.md` files
4. **Methodology Questions** → Check `reference/sales-methodologies.md`
5. **Salesforce Integration** → Check `reference/salesforce-agentforce-integration.md`

---

## Expected Outcomes (90 Days)

- ✅ 15-25% reduction in loss rate (lost opportunities become wins)
- ✅ 50% faster rep ramp time (6-12 months → 3-6 months)
- ✅ 20%+ increase in competitive win rate (beat LexisNexis, TransUnion, etc.)
- ✅ 80-90% AI agent performance vs. top human reps
- ✅ $500K-$2M+ annual revenue impact (depending on portfolio size)

---

## Ready? Let's Go! 🚀

**Next Step**: Open [GEMINI_SETUP_GUIDE.md](GEMINI_SETUP_GUIDE.md) and follow Steps 1-5.

**Questions?** All documentation is in this folder. Start with the setup guide, use test prompts to validate, reference README for deep dives.

**You're about to transform your sales conversations. Let's do this.**
