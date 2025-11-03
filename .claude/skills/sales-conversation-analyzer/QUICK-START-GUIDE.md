# Quick Start Guide - Gemini Sales Conversation Analyzer GPT

## Setup (5 Minutes)

### Step 1: Create Custom GPT

1. Go to **Gemini** (or ChatGPT Plus)
2. Click **"Explore GPTs"** → **"Create a GPT"**
3. Name it: **"Sales Conversation Analyzer"**
4. Description: **"Analyzes sales conversations across Auto Finance, Insurance, Repo, and Retail verticals to identify winning patterns and train AI agents"**

### Step 2: Add Instructions

1. Open file: `GEMINI-GPT-PROMPT.txt`
2. **Copy the ENTIRE contents**
3. Paste into the **"Instructions"** field in your GPT
4. **Enable**: "Code Interpreter" (for CSV processing)
5. **Enable**: "File Upload"
6. Click **"Save"**

### Step 3: Prepare Your Data

**Option A: Use Provided Templates**

Use the template CSVs in the `/templates` folder:
- `won_auto_finance.csv`
- `won_insurance.csv`
- `won_repo.csv`
- `won_retail.csv`

Replace the example data with your actual conversations.

**Option B: Export from Your CRM**

Export conversations with these columns:

**Required:**
- `conversation_id` (or `id`)
- `transcript` (or `conversation`)

**Optional (but recommended):**
- `outcome` (closed, booked, lost)
- `deal_value`
- `duration` (seconds)
- `customer_name`
- `date`
- `agent_name`

**File naming:**
- Won deals: `won_[vertical].csv`
  - `won_auto_finance.csv`
  - `won_insurance.csv`
  - `won_repo.csv`
  - `won_retail.csv`

- Lost deals: `lost_[vertical].csv`
  - `lost_auto_finance.csv`
  - `lost_insurance.csv`
  - `lost_repo.csv`
  - `lost_retail.csv`

## Usage

### Example 1: Analyze Won Auto Finance Deals

1. Start conversation with GPT
2. When prompted, type: **"1"** or **"Auto Finance"**
3. Upload: `won_auto_finance.csv`
4. Wait for analysis (~30 seconds for 50 conversations)
5. Review:
   - Consistent buying signals (3-7 identified)
   - World-class patterns to replicate
   - Framework recommendations
   - Training protocols

### Example 2: Analyze Lost Insurance Deals

1. Start conversation
2. Select: **"2"** or **"Insurance"**
3. Upload: `lost_insurance.csv`
4. Get analysis of:
   - Why deals were lost
   - Preventable vs unpreventable
   - Prevention strategies
   - Coaching priorities

### Example 3: Compare Won vs Lost (Repo)

1. Start conversation
2. Select: **"3"** or **"Repo"** or **"Forwarding"**
3. Upload BOTH: `won_repo.csv` AND `lost_repo.csv`
4. Get comparative analysis:
   - Critical success factors
   - What separates won from lost
   - Action plan for improvement

### Example 4: Generate AI Agent Training

1. After analysis complete, ask:
   **"Generate AI agent training prompts"**
2. GPT will output:
   - Copy-paste prompt enhancements
   - Few-shot training examples
   - Signal detection instructions
   - Framework priorities

### Example 5: Create Rep Playbook

1. After analysis, ask:
   **"Create rep playbook"**
2. GPT will output:
   - Training modules by framework
   - Buyer signal recognition guide
   - Objection handling scripts
   - Practice exercises

## What You'll Get

### For Won Deals:

✅ **3-7 Consistent Buying Signals**
- Each mapped to supporting frameworks
- Strength and confidence scores
- Real examples from your data
- Frequency across conversations

✅ **World-Class Patterns**
- Top 5 techniques that worked
- Effectiveness scores
- Success rates
- Direct quotes
- Why they work

✅ **Framework Rankings**
- Which of the 12 frameworks performed best
- Effectiveness scores by framework
- Usage frequency

✅ **Training Protocols**
- Specific recommendations for reps
- AI agent prompt enhancements
- Practice scenarios

### For Lost Deals:

❌ **Root Causes**
- 9 categories analyzed
- Severity levels
- Preventable vs unpreventable
- Frequency and impact

❌ **Prevention Strategies**
- Specific tactics by category
- Frameworks to apply
- Expected impact
- Implementation examples

❌ **Coaching Priorities**
- Critical, High, Medium priorities
- Specific skill gaps
- Development plans

### For Comparison (Won + Lost):

🔄 **Critical Success Factors**
- What separates winners from losers
- Specific behavioral differences
- Quantified gaps

🔄 **Action Plans**
- This week priorities
- This month goals
- This quarter objectives

## Tips for Best Results

### 1. Quality Data

**Good:**
```csv
conversation_id,transcript,outcome,deal_value
conv_001,"Agent: Hi John... [full conversation]...",closed,25000
```

**Bad:**
```csv
id,notes
1,"Customer interested in financing"
```

**Need full conversations, not summaries!**

### 2. Consistent Formatting

- Use same column names across files
- Keep vertical in filename (won_**auto_finance**.csv)
- One conversation per row

### 3. Enough Data

**Minimum:** 10 conversations per file
**Recommended:** 30-50+ conversations
**Ideal:** 100+ conversations

More data = better pattern detection

### 4. Actual Conversations

Include:
- ✅ Full back-and-forth dialogue
- ✅ Both agent and customer messages
- ✅ Complete conversations (start to close/loss)

Avoid:
- ❌ Summaries or notes
- ❌ One-sided transcripts
- ❌ Partial conversations

### 5. Ask Follow-Up Questions

After analysis, you can ask:
- "Which framework should we focus training on?"
- "What's the #1 pattern to teach new reps?"
- "Create an AI agent prompt for this vertical"
- "What's the biggest difference between won and lost?"
- "Generate role-play scenarios for these patterns"

## Troubleshooting

### "No data found in CSV"

**Solution:** Check that you have columns named:
- `conversation_id` or `id`
- `transcript` or `conversation`

### "Only found X conversations"

**Solution:** Make sure each conversation is on its own row (not split across multiple rows)

### "Unable to detect vertical"

**Solution:** Make sure you selected a vertical (1-4) when prompted at the start

### "Analysis seems generic"

**Solution:**
- Upload more conversations (need 30+ for good patterns)
- Ensure transcripts are complete dialogues, not summaries
- Check that the vertical selected matches the data

## Advanced Usage

### Multiple Verticals

Run separate analyses for each vertical:

1. **Session 1:** Auto Finance won + lost
2. **Session 2:** Insurance won + lost
3. **Session 3:** Repo won + lost
4. **Session 4:** Retail won + lost

Each gets vertical-specific insights.

### Time-Based Comparison

Upload CSVs from different time periods:

- `won_auto_finance_q1.csv` (Jan-Mar)
- `won_auto_finance_q2.csv` (Apr-Jun)

Compare to track improvement over time.

### Agent Performance

Add `agent_name` column to CSVs, then ask:

**"Compare performance by agent"**

GPT will show which agents use which patterns most effectively.

### Custom Frameworks

Ask GPT to look for specific patterns:

**"Also analyze for [Your Custom Framework]"**

GPT will adapt analysis to include your proprietary techniques.

## Export Options

After analysis, ask for:

1. **"Export as JSON"** - Structured data for systems integration
2. **"Export as training examples"** - Few-shot learning format
3. **"Create AI agent prompt"** - Copy-paste ready prompt
4. **"Generate PDF playbook"** - Training document for reps

## Support

**Questions?**
1. Check the full instructions: `GEMINI-GPT-INSTRUCTIONS.md`
2. Review example conversations in `/templates`
3. Try with template data first to see expected output

**Tips:**
- Start with won deals only (easier to see patterns)
- Add lost deals after understanding won patterns
- Use comparative analysis to identify biggest gaps
- Generate training materials after each analysis

---

## Example Full Workflow

```
1. Create GPT with GEMINI-GPT-PROMPT.txt instructions
2. Upload won_auto_finance.csv (50 conversations)
3. Review 5 consistent buying signals identified
4. Note top 3 world-class patterns
5. Ask: "Generate AI agent training prompts"
6. Copy AI prompts to your AI agent system
7. Ask: "Create rep playbook"
8. Share playbook with sales team
9. Upload lost_auto_finance.csv
10. Review prevention strategies
11. Ask: "Compare won vs lost - what's the #1 difference?"
12. Implement that difference in training
```

**Time investment:** 15 minutes
**Value:** World-class training protocols based on YOUR data

---

## Ready to Start?

1. ✅ Created GPT with instructions
2. ✅ Prepared CSV file(s)
3. ✅ Opened GPT
4. ✅ Selected vertical
5. ✅ Uploaded file

**Go analyze!** 🚀
