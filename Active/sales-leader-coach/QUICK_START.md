# Sales Leader Coach - Quick Start Guide

## 5-Minute Setup

### Step 1: Upload to Gemini Gem Custom GPT

1. Go to [Gemini](https://gemini.google.com/)
2. Click **"Create Custom GPT"**
3. Name it: **"Sales Leader Coach"**
4. Upload these files:
   - `SKILL.md` (primary instruction set)
   - All files from `reference/` folder (8 files total)
5. Click **"Create"**

### Step 2: Test with a Sample Conversation

Copy and paste this into your new custom GPT:

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

### Step 3: Review Output

You should receive:
- ✅ Conversation intelligence analysis
- ✅ Coached response (what rep should have said)
- ✅ Tactical feedback (what to improve)
- ✅ Next conversation goals
- ✅ Salesforce-ready JSON output

---

## Analyze Your First Real Conversation

### Option A: Single Conversation (Copy-Paste)

**Format**:
```
Date: YYYY-MM-DD
Rep: [Rep Name]
Prospect: [Name], [Title], [Company]
Stage: [Discovery | Demo | Proposal | Negotiation | Closing]

Transcript:
[Paste full conversation here]

Outcome: [What happened]
```

### Option B: Batch CSV Upload

**Create CSV** with these columns:
```csv
conversation_id,date,rep_name,prospect_name,prospect_title,prospect_company,conversation_stage,transcript,outcome
CONV_001,2025-10-15,John Smith,Jane Doe,VP Collections,ABC Bank,Discovery,"Rep: Hi Jane...",Scheduled follow-up
```

Upload CSV to custom GPT and wait 3-5 minutes for batch analysis.

---

## Common Use Cases

### 🔴 Lost Opportunity Analysis
**Goal**: Understand why deals were lost

**Process**:
1. Export 20-50 lost opportunity conversations from Salesforce
2. Format as CSV (see template above)
3. Upload to Sales Leader Coach
4. Review coaching feedback and playbook updates
5. Implement changes with sales team

**Expected Outcome**: 15-25% reduction in loss rate within 90 days

---

### 🟢 New Rep Onboarding
**Goal**: Accelerate rep ramp time

**Process**:
1. Have new rep record first 10 sales calls
2. Transcribe conversations (use Zoom/Teams auto-transcription)
3. Feed transcripts into Sales Leader Coach one at a time
4. Review coaching after each call
5. Use coached responses as scripts for next calls

**Expected Outcome**: Cut ramp time from 6-12 months to 3-6 months

---

### 🔵 AI Agent Training (Salesforce AgentForce)
**Goal**: Train AI agents to sound human and handle objections

**Process**:
1. Batch process 50 successful sales conversations
2. Export generated Knowledge Base articles
3. Import articles into Salesforce Knowledge
4. Configure AgentForce to reference new articles
5. Test agent responses and iterate

**Expected Outcome**: AI agents perform at 80-90% of top human reps

---

## Integrating with Salesforce AgentForce

### Prerequisites
- Salesforce org with AgentForce enabled
- Gemini Gem custom GPT set up
- OAuth 2.0 credentials for Salesforce API

### Integration Steps

1. **Authenticate Gemini GPT with Salesforce**:
   - In custom GPT settings, add Salesforce OAuth
   - Grant permissions: `Read Opportunities`, `Write Tasks`, `Create Knowledge`

2. **Configure API Actions**:
   - Add action: `analyzeConversations`
   - Input schema: Array of conversation objects (max 50)
   - Output schema: Batch analysis JSON (see `salesforce-agentforce-integration.md`)

3. **Create Salesforce Flow** (optional for automation):
   - Trigger: Opportunity stage changes to "Closed Lost"
   - Action: Call Gemini GPT API with opportunity data
   - Result: Write analysis to `Conversation_Intelligence__c` object

4. **Set Up Knowledge Base Sync**:
   - Auto-create Knowledge articles from batch insights
   - Publish to AgentForce-accessible categories
   - Schedule weekly updates

5. **Test End-to-End**:
   - Upload test CSV
   - Verify Knowledge articles created in Salesforce
   - Check Data Cloud enrichment
   - Confirm AgentForce can reference new content

**Full integration guide**: See `reference/salesforce-agentforce-integration.md`

---

## Tips for Best Results

### ✅ Do This
- **Include full transcripts**: Don't summarize—raw conversation is best
- **Provide context**: Date, rep name, prospect title, company, stage
- **Batch similar conversations**: All Discovery calls, or all Lost Opportunities
- **Implement coaching immediately**: Use feedback in next conversation
- **Review playbook updates monthly**: Operationalize insights

### ❌ Avoid This
- **Don't truncate transcripts**: Incomplete data = incomplete analysis
- **Don't skip metadata**: Context improves accuracy
- **Don't ignore coaching**: Reading insights without action = wasted effort
- **Don't batch 50+ conversations**: Overwhelming—start with 20-30
- **Don't forget to test**: Always validate output before relying on it

---

## Troubleshooting

### "CSV upload failed"
**Solution**: Check file format, ensure required fields (`conversation_id`, `transcript`, `date`), verify file < 25 MB

### "No coached response generated"
**Solution**: Ensure conversation stage and awareness level were detected (check transcript for pain points and engagement)

### "Analysis seems off"
**Solution**: Review transcript quality—typos, missing context, or unclear stage can affect accuracy

### "Salesforce integration not working"
**Solution**: Verify OAuth authentication, API permissions, webhook configuration (see `salesforce-agentforce-integration.md`)

---

## Next Steps

1. ✅ Analyze your first conversation (use sample above)
2. ✅ Upload 5-10 real conversations (CSV or copy-paste)
3. ✅ Review coaching feedback and implement changes
4. ✅ Set up Salesforce integration (optional)
5. ✅ Share results with sales team

---

## Support

- **Full Documentation**: See `README.md`
- **Integration Guide**: See `reference/salesforce-agentforce-integration.md`
- **Product Knowledge**: See `reference/drn-*.md` files
- **Sales Methodologies**: See `reference/sales-methodologies.md`
- **Response Templates**: See `reference/response-templates.md`

**Questions?** Email: support@chiefaiofficer.com

---

**You're now ready to transform your sales conversations with world-class AI coaching!**
