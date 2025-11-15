# ChatGPT Custom GPT Setup Guide
## UMich CDAIO Curriculum Analyzer

---

## 📋 WHAT YOU'LL CREATE

A Custom GPT that analyzes and designs executive education programs using the University of Michigan CDAIO methodology (9.5/10 quality score).

**What It Does**:
- ✅ Scores curriculum quality 0-10 using Bloom's Taxonomy
- ✅ Evaluates adult learning principles (Knowles' 5)
- ✅ Identifies 5-10 critical gaps with fixes
- ✅ Benchmarks against MIT, Stanford, Harvard
- ✅ Designs new programs from scratch
- ✅ Creates rubrics, budgets, and roadmaps

---

## 🚀 SETUP STEPS (5 Minutes)

### **Step 1: Open ChatGPT**
1. Go to https://chat.openai.com
2. Click your profile icon (bottom left)
3. Select **"My GPTs"**
4. Click **"Create a GPT"**

---

### **Step 2: Switch to Configure Tab**
1. Click **"Configure"** (top right)
2. You'll see fields for Name, Description, Instructions, etc.

---

### **Step 3: Fill in Basic Info**

**Name**:
```
UMich CDAIO Curriculum Analyzer
```

**Description** (copy this exactly):
```
World-class curriculum analyst using University of Michigan CDAIO methodology. Evaluates programs with Bloom's Taxonomy (37-point framework), adult learning principles, competitive benchmarking, and ROI analysis. Scores curriculum quality 0-10, identifies critical gaps, provides actionable fixes. Designs executive education programs from scratch.
```

---

### **Step 4: Copy Instructions**

1. Open the file: **CUSTOM_GPT_INSTRUCTIONS_COMPACT.txt**
2. **Copy the ENTIRE file** (Cmd+A, Cmd+C on Mac or Ctrl+A, Ctrl+C on Windows)
3. Paste into the **"Instructions"** field in ChatGPT

**Character count**: Should be ~7,900 characters (under 8,000 limit)

---

### **Step 5: Upload Knowledge File**

1. Scroll down to **"Knowledge"** section
2. Click **"Upload files"**
3. Select: **CUSTOM_GPT_KNOWLEDGE_BASE.md**
4. Wait for upload confirmation (green checkmark)

**This file contains**:
- Bloom's Taxonomy detailed guide
- Adult learning principles
- Rubric templates
- Competitive benchmarks
- UMich CDAIO case study (9.5/10)
- Gap analysis frameworks
- Implementation roadmaps

---

### **Step 6: Configure Capabilities**

In the **"Capabilities"** section:

- ✅ **Web Browsing**: **ON** (needed to analyze programs from URLs)
- ✅ **Code Interpreter**: **ON** (optional, for data analysis)
- ❌ **DALL-E Image Generation**: **OFF** (not needed)

---

### **Step 7: Add Conversation Starters**

In the **"Conversation starters"** section, add these 5:

```
1. Analyze this program: [URL]
```

```
2. Design a Chief AI Officer training program from scratch
```

```
3. Compare MIT AI program vs Stanford AI program
```

```
4. Score this learning objective and rewrite it
```

```
5. Build business case for executive AI bootcamp
```

---

### **Step 8: Save Your GPT**

1. Click **"Create"** (top right)
2. Choose visibility:
   - **"Only me"** (private, for testing)
   - **"Anyone with a link"** (shareable)
   - **"Public"** (listed in GPT store)

**Recommendation**: Start with "Only me" for testing

---

## ✅ TEST YOUR GPT

### **Test 1: Analyze UMich Program (Should Score 9.5/10)**

**Prompt**:
```
Analyze the University of Michigan CDAIO program. It has:
- 12 live sessions (90 min each) + 5-day immersion (40 hours)
- 85% of learning objectives at Evaluate/Create (Bloom's)
- All 5 adult learning principles met
- 10 pedagogical methods used (lectures, cases, labs, peer learning, capstone, speakers, site visits, etc.)
- Capstone project (35% of grade) with rubric
- Pricing: $16,000 for 20-30 students

Score the curriculum quality and identify any gaps.
```

**Expected Output**:
```markdown
# University of Michigan CDAIO - Analysis

## EXECUTIVE SUMMARY
**Quality Score**: 9.5/10 (Grade: A+)
**Bloom's**: 85% at Evaluate/Create ✅ (Target: 80%+)
**Adult Learning**: 5/5 principles met ✅
**Assessment Rigor**: 9/10 (missing formal quizzes)
**Recommendation**: World-class program - minor enhancements only

## CRITICAL GAP IDENTIFIED
🔴 **No Formal Quizzes**
- Fix: Add 10-question quiz per session (80% passing)
- Impact: +0.5 points (9.5 → 10/10)
```

✅ **If your GPT produces similar output, it's working correctly!**

---

### **Test 2: Score a Learning Objective**

**Prompt**:
```
Score this learning objective: "Understand AI strategy frameworks"
```

**Expected Output**:
```markdown
❌ **Bloom Level**: Understand (4/10 quality)

**Issues**:
- Uses weak verb "Understand" (not measurable)
- No business outcome
- Passive learning

✅ **IMPROVED VERSION**:
"Design AI transformation strategy for your organization using McKinsey 3-Horizon framework"

**Bloom Level**: Create (9/10 quality)
- Action verb "Design" ✅
- Specific framework ✅
- Business outcome ✅
- Deliverable: AI strategy 1-pager
```

✅ **If GPT rewrites objectives to Create/Evaluate level, it's working!**

---

### **Test 3: Design a New Program**

**Prompt**:
```
Design a 6-week AI Strategy Bootcamp for Fortune 500 executives. Target: 80%+ Evaluate/Create objectives.
```

**Expected Output**:
- Module structure (6 weeks, 2-3 sessions each)
- Learning objectives (at Create/Evaluate level)
- Assessment framework (quizzes, deliverables, capstone)
- Pricing and economics ($8-12K range)

✅ **If GPT produces structured curriculum with proper Bloom's levels, it's working!**

---

## 🎯 USING YOUR GPT

### **Use Case 1: Analyze Existing Program**

**Prompt Template**:
```
Analyze this program: [URL or paste syllabus]

Evaluate:
- Bloom's Taxonomy distribution
- Adult learning principles (Knowles' 5)
- Assessment rigor
- Critical gaps

Provide quality score (0-10) and recommendations.
```

---

### **Use Case 2: Design New Program**

**Prompt Template**:
```
Design a [DURATION]-week [TOPIC] program for [AUDIENCE].

Requirements:
- Target: 80%+ Evaluate/Create objectives
- Include assessment framework with rubrics
- Provide technology stack and budget
- Recommend pricing

Deliver full curriculum structure.
```

---

### **Use Case 3: Competitive Benchmarking**

**Prompt Template**:
```
Compare these programs:
1. [Program A details or URL]
2. [Program B details or URL]

Benchmark on:
- Curriculum quality
- Hands-on experience
- Faculty credentials
- Networking opportunities
- Pricing/value

Rank them and identify winner per dimension.
```

---

### **Use Case 4: Fix Weak Learning Objective**

**Prompt Template**:
```
Score this learning objective: "[PASTE OBJECTIVE]"

If weak (<7/10), rewrite to Evaluate or Create level with:
- Strong action verb
- Business outcome
- Measurable deliverable
```

---

### **Use Case 5: Create Rubric**

**Prompt Template**:
```
Create a 4-level rubric for this deliverable: "[DELIVERABLE NAME]"

Criteria:
1. [Criterion 1]
2. [Criterion 2]
3. [Criterion 3]

Levels: Below Expectations, Meets, Exceeds, Exceptional
```

---

## 🔧 TROUBLESHOOTING

### **Issue: GPT doesn't produce scores (0-10)**

**Fix**: Re-paste instructions, ensure this line is included:
```
1. **Always score quantitatively** (0-10, percentages, rankings)
```

---

### **Issue: GPT doesn't use Bloom's Taxonomy**

**Fix**: Check that **CUSTOM_GPT_KNOWLEDGE_BASE.md** is uploaded under "Knowledge"

---

### **Issue: GPT can't analyze URLs**

**Fix**: Ensure **Web Browsing** is enabled in Capabilities

---

### **Issue: GPT gives generic advice**

**Fix**: Prompt more specifically:
```
Analyze [program] using the UMich CDAIO framework. Score Bloom's distribution, adult learning (Knowles' 5), and assessment rigor (0-10). Identify 5 gaps with specific fixes.
```

---

### **Issue: Character limit exceeded when pasting instructions**

**Fix**: Use **CUSTOM_GPT_INSTRUCTIONS_COMPACT.txt** (already optimized to ~7,900 characters)

---

## 📊 SUCCESS CHECKLIST

Your GPT is working correctly if it:

- [ ] Produces 0-10 scores for curriculum quality
- [ ] Identifies Bloom's Taxonomy levels correctly
- [ ] Uses Knowles' 5 adult learning principles
- [ ] Identifies 3-7 gaps per program
- [ ] Provides specific, actionable fixes (not vague suggestions)
- [ ] Rewrites weak objectives to Create/Evaluate level
- [ ] Creates 4-level rubrics (Below/Meets/Exceeds/Exceptional)
- [ ] Benchmarks against MIT/Stanford/Harvard standards
- [ ] Builds financial models (pricing, margin, break-even)

---

## 🎓 REFERENCE FILES

You have 3 files:

1. **CUSTOM_GPT_INSTRUCTIONS_COMPACT.txt** (7,900 chars)
   - Copy this into ChatGPT "Instructions" field
   - Contains core methodology and response format

2. **CUSTOM_GPT_KNOWLEDGE_BASE.md** (30,000+ words)
   - Upload this as "Knowledge" file
   - Contains detailed frameworks, examples, rubrics, case studies

3. **SETUP_GUIDE_CHATGPT.md** (this file)
   - Step-by-step setup instructions
   - Test queries and troubleshooting

---

## 🚀 NEXT STEPS

### **After Setup**:

1. **Test with 3 queries** (see Test section above)
2. **Analyze a real program** from your industry
3. **Share with your team** (if useful)
4. **Iterate**: Add custom industry examples to Knowledge file

### **Advanced Customization**:

**Add Industry-Specific Content**:
- Create `Healthcare_AI_Programs.md` with healthcare-specific benchmarks
- Upload as additional Knowledge file
- GPT will use it automatically

**Add Your Own Case Studies**:
- Document your best programs in same format as UMich case study
- Add to Knowledge Base
- GPT will reference them in analyses

---

## 📧 SUPPORT

### **If You Get Stuck**:

1. Re-read this setup guide
2. Check that instructions were copied fully (all ~7,900 characters)
3. Verify Knowledge Base file uploaded successfully
4. Test with UMich benchmark query (Test 1 above)

### **Expected Results**:
- UMich CDAIO program should score **9.5/10**
- Weak objectives should be rewritten to **9-10/10**
- New programs should have **80%+ Evaluate/Create**

---

## ✅ FINAL CHECKLIST

Before using your GPT, confirm:

- [ ] Name: "UMich CDAIO Curriculum Analyzer"
- [ ] Description: [From Step 3 above]
- [ ] Instructions: CUSTOM_GPT_INSTRUCTIONS_COMPACT.txt pasted (full file)
- [ ] Knowledge: CUSTOM_GPT_KNOWLEDGE_BASE.md uploaded
- [ ] Web Browsing: Enabled
- [ ] Code Interpreter: Enabled (optional)
- [ ] DALL-E: Disabled
- [ ] Conversation starters: 5 examples added
- [ ] Test query run: UMich analysis = 9.5/10 ✅

---

## 🎯 YOU'RE READY!

**Your Custom GPT now replicates the world-class curriculum analysis methodology used for the University of Michigan CDAIO program.**

Start by analyzing a program you know well, then design something new!

**Example First Prompt**:
```
Analyze this program: [paste URL or syllabus]

Score:
- Bloom's Taxonomy (target: 80%+ Evaluate/Create)
- Adult learning principles (Knowles' 5)
- Assessment rigor (0-10)

Identify top 5 gaps and provide specific fixes.
```

---

**Built on the methodology that achieved 9.5/10 curriculum quality for UMich CDAIO.**
