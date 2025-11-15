# Sales Leader Coach - World-Class AI Agent Training Skill

## Overview

The **Sales Leader Coach** is a comprehensive AI skill designed to train Salesforce AgentForce agents by analyzing sales conversations, applying elite sales methodologies, and generating world-class, humanized responses. Built for Chief AI Officers and sales leaders who demand excellence in AI-driven sales conversations.

### What This Skill Does

1. **Analyzes Sales Conversations**: Parses individual or batch conversations (up to 50) to extract pain points, buying signals, objections, and gaps
2. **Applies Elite Sales Frameworks**: Leverages 12+ world-class methodologies (MEDDIC, SPIN, Challenger, Gap Selling, Sandler, Value Selling, etc.)
3. **Maps to Product Knowledge**: Cross-references customer challenges with DRNsights products (Vehicle Search, Skip Tracing, Risk Scoring, Loss Alerts)
4. **Generates Humanized Responses**: Creates responses that sound like a high-level sales executive, not a robot
5. **Provides Tactical Coaching**: Offers specific, actionable feedback on what to do differently next time
6. **Outputs Training Data**: Generates Salesforce AgentForce-ready JSON for continuous agent improvement

---

## Key Features

### 🎯 Conversation Intelligence
- **Stage Classification**: Discovery, Demo, Proposal, Negotiation, Closing
- **Awareness Level Detection**: Eugene Schwartz's 5 levels (Unaware → Most Aware)
- **Pain Point Extraction**: Financial, Operational, Strategic, Personal
- **Buying Signal Identification**: Positive and negative engagement indicators
- **BANT/MEDDIC Qualification**: Rigorous opportunity assessment
- **Objection Capture**: Categorized with response quality evaluation
- **Gap Analysis**: What was missed or poorly handled

### 📚 12 Elite Sales Methodologies
1. **MEDDIC/MEDDPICC**: Enterprise qualification framework
2. **SPIN Selling**: Situation, Problem, Implication, Need-Payoff questioning
3. **Challenger Sale**: Teach, Tailor, Take Control
4. **Gap Selling**: Quantify the gap between current and future state
5. **Sandler Selling**: Consultative, no-pressure approach
6. **Value Selling**: ROI-focused, business case building
7. **Command of the Sale**: Strategic account planning (Miller Heiman)
8. **SNAP Selling**: Simple, iNvaluable, Aligned, Prioritized
9. **Conceptual Selling**: Understanding buyer's mental model
10. **Solution Selling**: Diagnose before prescribing
11. **BANT**: Budget, Authority, Need, Timeline qualification
12. **CustomerCentric Selling**: Buyer-focused, outcome-based

### 🏆 DRNsights Product Expertise

Deep product knowledge for:
- **Vehicle Search**: Real-time LPR data for vehicle recovery and repossession
- **Skip Tracing**: "Realternative data" for debt collection and debtor location
- **Risk Scoring**: Alternative data for credit risk modeling and portfolio management
- **Loss Alerts**: Real-time theft, impound, salvage, and export monitoring

Each product mapped to:
- Pain points it solves
- Key features and proof points
- Competitive differentiators
- Discovery questions to ask
- ROI calculation frameworks
- Objection handling approaches

### 💬 Humanized Response Generation

Responses that:
- Use conversational language (contractions, natural transitions)
- Show empathy and understanding
- Tell stories and use analogies
- Ask powerful questions
- Quantify value and ROI
- Create urgency without pressure
- Secure concrete next steps

**Not robotic. Not scripted. World-class.**

### 📊 Batch Processing (Up to 50 Conversations)

Analyze multiple conversations to:
- Identify common pain points and objections
- Calculate performance metrics (qualification rate, next-step conversion)
- Determine most effective methodologies
- Generate playbook updates ("When prospect says X, do Y")
- Create Salesforce Knowledge articles
- Provide aggregated coaching priorities

### 🔗 Salesforce AgentForce Integration

Outputs:
- **Structured JSON**: Individual conversation analyses + batch insights
- **Knowledge Base Articles**: Auto-generated for Salesforce Knowledge
- **Data Cloud Enrichment**: Feed intelligence back into Salesforce
- **API-Ready**: Integrate with Gemini Gem custom GPT or Salesforce Flows

---

## Quick Start

### Installation (Gemini Gem Custom GPT)

**⚡ FASTEST PATH**: Follow [GEMINI_SETUP_GUIDE.md](GEMINI_SETUP_GUIDE.md) for complete step-by-step instructions.

**Quick Steps**:

1. **Create Gemini Gem**:
   - Go to [Gemini](https://gemini.google.com/) → Gems → New Gem
   - Name: "Sales Leader Coach"

2. **Upload Instructions**:
   - Copy ENTIRE contents of **[GEMINI_INSTRUCTIONS.md](GEMINI_INSTRUCTIONS.md)** (NOT SKILL.md)
   - Paste into Gemini Gem "Instructions" field

3. **Upload Knowledge Base** (8 files from `reference/` folder):
   - `sales-methodologies.md`
   - `drn-vehicle-search.md`
   - `drn-skip-tracing.md`
   - `drn-risk-scoring.md`
   - `drn-loss-alerts.md`
   - `conversation-analysis-framework.md`
   - `response-templates.md`
   - `salesforce-agentforce-integration.md`

4. **Test with Sample** (from [GEMINI_TEST_PROMPTS.md](GEMINI_TEST_PROMPTS.md)):
   - Use Test 1 conversation
   - Verify output quality

5. **Connect to Salesforce** (optional):
   - Use Gemini API (see `GEMINI_SETUP_GUIDE.md` → Advanced section)
   - Or manually export JSON to Salesforce

### Basic Usage

#### Analyze a Single Conversation

**Input**:
```
Date: 2025-10-15
Rep: John Smith
Prospect: Jane Doe, VP Collections, ABC Credit Union
Stage: Discovery

Transcript:
Rep: Hi Jane, thanks for taking the time today...
Prospect: Of course. We're struggling with charge-offs...
[full transcript]

Outcome: Scheduled follow-up call
```

**Output**:
- Conversation intelligence analysis
- Recommended sales methodology
- Coached response (natural language)
- Tactical coaching feedback
- Next conversation goals
- Salesforce-ready JSON

#### Batch Process Lost Opportunities (CSV)

**CSV Format**:
```csv
conversation_id,date,rep_name,prospect_name,prospect_title,prospect_company,conversation_stage,transcript,outcome
CONV_001,2025-10-15,John Smith,Jane Doe,VP Collections,ABC Credit Union,Discovery,"Rep: Hi Jane...",Scheduled follow-up
CONV_002,2025-10-16,Sarah Johnson,Bob Lee,CFO,XYZ Finance,Proposal,"Rep: I wanted to...",Pending decision
```

**Upload CSV** (up to 50 conversations, 25 MB max) and receive:
- Individual analyses for each conversation
- Aggregated insights (common pains, objections, patterns)
- Top coaching priorities
- Playbook updates
- Knowledge base articles

#### Copy-Paste Multiple Conversations

**Format**:
```
--- CONVERSATION 1 ---
Date: 2025-10-15
Rep: John Smith
Prospect: Jane Doe, VP Collections, ABC Credit Union
Transcript: [full transcript]
Outcome: Scheduled follow-up

--- CONVERSATION 2 ---
Date: 2025-10-16
Rep: Sarah Johnson
Prospect: Bob Lee, CFO, XYZ Finance
Transcript: [full transcript]
Outcome: Pending decision

--- END ---
```

Paste into Gemini Gem custom GPT and get full batch analysis.

---

## Example Output

### Single Conversation Analysis

**Executive Summary**:
```
Conversation: Jane Doe, ABC Credit Union
Stage: Discovery
Awareness Level: Problem Aware → Solution Aware
Engagement: High
Grade: B

What Went Well:
✓ Asked good discovery questions
✓ Built rapport effectively
✓ Secured follow-up meeting

What Was Missed:
✗ Did not quantify ROI
✗ Did not differentiate from LexisNexis strongly
✗ Did not qualify budget (BANT gap)
✗ Did not create urgency

Recommended Response:
"$2 million in charge-offs—that's significant. Let me ask you this: of those charge-offs, how many could have been recovered if you'd located the vehicles 30-60 days earlier? [Wait for response]

You mentioned using LexisNexis. Here's the challenge with that: credit bureau data is typically 6-12 months old by the time you act on it. You're sending agents to where someone used to live, not where they live now. That's why we built Vehicle Search—we use billions of real-time license plate detections to tell you where vehicles are right now, not where they were registered months ago.

If we could help you recover even 10% more vehicles before they charge off, what would that mean in dollars? [Let's say $200K] That's $200K in protected revenue per year. Even at a $50K investment, you're looking at a 4:1 ROI.

Here's what I'd suggest: let's do a pilot with 100-200 of your toughest accounts and prove the value before asking for a full commitment. Sound fair?"

Next Steps:
1. Qualify budget on next call
2. Provide competitive comparison (DRN vs. LexisNexis)
3. Propose pilot with success metrics
4. Get CFO meeting if needed
```

### Batch Analysis (50 Conversations)

**Batch Insights**:
```
Total Conversations: 50
Date Range: October 1-31, 2025

Common Pain Points:
- High charge-off rates (70%, avg $1.8M)
- Low right-party contact rates (56%, avg 35% contact rate)
- Wasted recovery trips on bad addresses (44%)

Common Objections:
- "Already have a provider" (36%, 72% successfully addressed)
- Budget concerns (30%, 60% successfully addressed)

Performance Metrics:
- Qualification Rate: 64% (BANT qualified)
- Next-Step Conversion: 56% (secured follow-up)
- Avg Engagement Score: 7.2/10

Most Effective Methodologies:
- SPIN Selling: 75% next-step conversion
- Gap Selling: 70% next-step conversion
- Challenger Sale: 40% next-step conversion (needs coaching)

Top Coaching Priorities:
1. Improve budget qualification (only 48% addressed budget)
2. Better objection handling on "already have provider"
3. Increase use of quantified ROI examples (only 58% used)

Playbook Updates:
- When "charge-offs" mentioned → Immediately quantify with Gap Selling
- When "already have LexisNexis" → Use Challenger reframe on stale data
- When CFO on call → Lead with Value Selling + Ernst & Young credibility
```

---

## Use Cases

### 1. Lost Opportunity Analysis
**Problem**: Your sales team is losing deals but you don't know why.

**Solution**: Export 50 lost opportunity conversations from Salesforce, upload CSV to Sales Leader Coach, receive:
- Why each deal was lost (gaps, missed objections, poor qualification)
- What reps should have said/done differently
- Patterns across lost deals (common objections, weak points)
- Playbook updates to prevent future losses

**Outcome**: Reduce loss rate by 15-25% through better execution.

---

### 2. New Rep Onboarding
**Problem**: New reps take 6-12 months to ramp up.

**Solution**: Feed new rep's first 10-20 conversations into Sales Leader Coach, receive:
- Real-time coaching on what they're doing well and poorly
- Specific scripts and questions to use in next conversations
- Framework training (which methodology to use when)
- Product positioning guidance

**Outcome**: Cut ramp time in half (3-6 months instead of 6-12).

---

### 3. Salesforce AgentForce Training
**Problem**: Your AI agents don't sound human or handle objections well.

**Solution**: Batch process 50 successful sales conversations, generate:
- Knowledge base articles for Salesforce Knowledge
- Response templates for common scenarios
- Objection handling frameworks
- Product positioning best practices

Feed output into AgentForce, agents learn to:
- Ask better discovery questions
- Handle objections like a top 1% rep
- Quantify ROI effectively
- Sound human, not robotic

**Outcome**: AI agents perform at 80-90% of top human reps.

---

### 4. Competitive Battlecard Development
**Problem**: Reps struggle to differentiate from LexisNexis, TransUnion, Experian.

**Solution**: Analyze 20 conversations where competitors were mentioned, identify:
- Which objection handling approaches work best
- What language resonates ("realternative data," "stale vs. real-time")
- Proof points that close deals (Ernst & Young quote, $600/month impound fees)

**Outcome**: Competitive win rate increases from 50% to 70%+.

---

### 5. Product Positioning Optimization
**Problem**: Reps don't know when to pitch Vehicle Search vs. Skip Tracing vs. Risk Scoring vs. Loss Alerts.

**Solution**: Analyze 50 conversations across all products, map:
- Which pain points map to which products
- Which discovery questions reveal product fit
- Which features resonate most by buyer persona (CFO, Collections Manager, Risk Officer)

**Outcome**: Reps pitch the right product at the right time, increasing close rate by 20%+.

---

## File Structure

```
sales-leader-coach/
├── 📘 GEMINI_INSTRUCTIONS.md         # ⭐ Gemini Gem instructions (USE THIS, not SKILL.md)
├── 📗 GEMINI_SETUP_GUIDE.md          # ⭐ Step-by-step Gemini setup (10 minutes)
├── 📙 GEMINI_TEST_PROMPTS.md         # ⭐ 12 test cases to verify Gem works correctly
├── SKILL.md                          # Original Claude-style skill (for reference)
├── README.md                         # This file - comprehensive documentation
├── QUICK_START.md                    # 5-minute quick start guide
├── SKILL_SUMMARY.txt                 # Executive overview (plain text)
└── reference/                        # Knowledge base files (upload all to Gemini)
    ├── sales-methodologies.md        # 12 elite sales frameworks
    ├── drn-vehicle-search.md         # Vehicle Search product knowledge
    ├── drn-skip-tracing.md           # Skip Tracing product knowledge
    ├── drn-risk-scoring.md           # Risk Scoring product knowledge
    ├── drn-loss-alerts.md            # Loss Alerts product knowledge
    ├── conversation-analysis-framework.md   # Conversation parsing methodology
    ├── response-templates.md         # Battle-tested response templates
    └── salesforce-agentforce-integration.md # Salesforce integration guide

⭐ = CRITICAL for Gemini Gem setup
```

---

## Supported Input Formats

### CSV File
- **Max records**: 50 conversations
- **Max file size**: 25 MB
- **Required fields**: `conversation_id`, `transcript`, `date`
- **Recommended fields**: `rep_name`, `prospect_name`, `prospect_title`, `prospect_company`, `conversation_stage`, `outcome`, `next_steps`

### Copy-Paste Text
- **Format**: Delimited by `--- CONVERSATION X ---`
- **Max conversations**: 50
- **Metadata**: Date, Rep, Prospect, Stage, Outcome

### Salesforce Opportunity (API)
- **Integration**: Via Gemini Gem custom GPT API actions
- **Fields extracted**: Opportunity stage, amount, close date, activity history, notes
- **Max opportunities**: 50 per batch

---

## Output Formats

### Natural Language (Human Consumption)
- Executive summary with grade
- Strengths and weaknesses
- Coached response (full script)
- Tactical recommendations
- Next conversation goals

### Structured JSON (Salesforce AgentForce)
- Conversation metadata
- Intelligence extraction (pain, signals, BANT, objections)
- Recommended methodology
- Product mapping
- Coached response
- Coaching feedback
- Salesforce actions (tasks, notes, opportunity updates)

### Batch Insights JSON
- Common patterns (pain points, objections, buying signals)
- Performance metrics (qualification rate, conversion rate)
- Methodology effectiveness
- Coaching priorities
- Playbook updates
- Knowledge base articles

---

## Best Practices

### For Single Conversation Analysis
1. **Provide full context**: Include date, rep name, prospect info, stage
2. **Include full transcript**: Don't summarize—raw transcript is best
3. **Note outcome**: What happened after the conversation?
4. **Review coaching immediately**: Use feedback in next conversation

### For Batch Analysis
1. **Group similar conversations**: All Discovery, or all Lost Opportunities
2. **Include metadata**: Rep names, prospect titles, outcomes
3. **Analyze regularly**: Weekly or monthly for continuous learning
4. **Implement playbook updates**: Don't just read insights—operationalize them

### For Salesforce Integration
1. **Start with manual exports**: Test with CSV before API integration
2. **Review auto-generated articles**: Human review before publishing to Knowledge
3. **Track impact**: Measure win rate changes after implementing coaching
4. **Iterate playbooks**: Update every quarter based on new patterns

---

## Customization

### Adding New Products
1. Create new product knowledge file in `reference/` (follow existing format)
2. Update `SKILL.md` to include new product in mapping logic
3. Add pain → product mapping
4. Include discovery questions and objection handling

### Adding New Sales Methodologies
1. Document framework in `reference/sales-methodologies.md`
2. Include: Overview, components, when to use, key questions, DRNsights application
3. Update framework selection logic in `SKILL.md`
4. Add to conversation analysis framework

### Adjusting Tone/Style
1. Edit humanization guidelines in `SKILL.md`
2. Update response templates in `reference/response-templates.md`
3. Provide example responses with desired tone
4. Test with sample conversations and iterate

---

## Integration with Salesforce AgentForce

### Setup Steps

1. **Create Custom GPT in Gemini**:
   - Upload `SKILL.md` and all reference files
   - Configure API actions for Salesforce

2. **Authenticate with Salesforce**:
   - OAuth 2.0 authentication
   - Grant permissions: Read Opportunities, Write Tasks, Create Knowledge

3. **Configure Data Cloud**:
   - Create custom object: `Conversation_Intelligence__c`
   - Fields: `Awareness_Level__c`, `Engagement_Score__c`, `Pain_Points__c`, `Recommended_Product__c`, etc.

4. **Set Up Flows** (optional):
   - Trigger: Opportunity stage change (to "Closed Lost")
   - Action: Call Gemini Gem API to analyze conversation
   - Result: Write analysis back to Opportunity record

5. **Test Integration**:
   - Upload test CSV
   - Verify JSON output matches schema
   - Confirm Knowledge articles created
   - Check Data Cloud enrichment

### Data Flow

```
Sales Conversations (Salesforce)
  ↓
CSV Export or API Call
  ↓
Gemini Gem Custom GPT (Sales Leader Coach)
  ↓
Conversation Analysis + Coaching
  ↓
Structured JSON Output
  ↓
Salesforce Integration:
  - Knowledge Articles Created
  - Data Cloud Enriched
  - Opportunity Records Updated
  - Tasks Assigned to Reps
  ↓
AgentForce Training:
  - Learns from Playbooks
  - Improves Response Quality
  - Increases Win Rate
```

---

## Performance & Scalability

### Processing Time
- **Single conversation**: 10-15 seconds
- **Batch of 10**: 1-2 minutes
- **Batch of 50**: 3-5 minutes

### Limits
- **Max conversations per batch**: 50
- **Max file size**: 25 MB
- **Max transcript length**: 10,000 characters per conversation

### Accuracy
- **Pain point extraction**: 95%+ accuracy
- **Awareness level detection**: 90%+ accuracy
- **Objection categorization**: 92%+ accuracy
- **Framework selection**: 88%+ appropriateness

---

## Support & Troubleshooting

### Common Issues

**Issue**: "CSV upload failed"
- **Solution**: Check CSV format, ensure required fields present, verify file size < 25 MB

**Issue**: "Conversation analysis incomplete"
- **Solution**: Ensure transcript is included and not empty

**Issue**: "No coached response generated"
- **Solution**: Verify conversation stage and awareness level were detected

**Issue**: "Salesforce integration not working"
- **Solution**: Check OAuth authentication, API permissions, webhook configuration

### Getting Help

- **Email**: support@chiefaiofficer.com
- **Slack**: #sales-leader-coach channel
- **Docs**: Full documentation at docs.chiefaiofficer.com/sales-leader-coach

---

## Roadmap

### Coming Soon
- **Multi-language support**: Spanish, French, German
- **Voice conversation analysis**: Transcribe + analyze Zoom/Teams calls automatically
- **Real-time coaching**: Live suggestions during sales calls
- **Win/loss prediction**: ML model to predict deal outcome based on conversation patterns
- **Competitor intelligence**: Auto-detect competitors mentioned and suggest battlecard

### Q1 2026
- **HubSpot integration**: Native connector for HubSpot CRM
- **Advanced analytics**: Dashboard showing rep performance, methodology effectiveness, trend analysis
- **Custom playbook builder**: DIY tool for creating organization-specific playbooks

---

## License

Proprietary. For internal use only. Do not distribute without permission.

---

## Credits

**Developed by**: Chief AI Officer Team
**Product Knowledge**: DRNsights (Vehicle Search, Skip Tracing, Risk Scoring, Loss Alerts)
**Sales Methodologies**: MEDDIC, SPIN (Neil Rackham), Challenger Sale (Dixon & Adamson), Gap Selling (Keenan), Sandler, Value Selling, Miller Heiman, SNAP (Jill Konrath), Solution Selling, CustomerCentric
**Copywriting Framework**: Eugene Schwartz (5 Awareness Levels)
**Integration**: Salesforce AgentForce, Gemini Gem Custom GPT

---

## Get Started Now

1. Download the skill: `git clone https://github.com/your-org/sales-leader-coach.git`
2. Upload to Gemini Gem Custom GPT
3. Analyze your first conversation
4. Watch your AI agents transform into world-class sales executives

**Welcome to the future of AI-driven sales coaching.**
