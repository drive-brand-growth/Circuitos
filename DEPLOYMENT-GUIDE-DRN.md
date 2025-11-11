# Circuit OS Weapons - Deployment Guide for DRN Team

## Overview

This guide shows how to deploy all 4 Circuit OS weapons as:
1. **Claude Skills** (for use with Claude.ai Projects or API)
2. **Custom GPTs** (for use with ChatGPT Teams)

Both implementations use the same **Contract + Control Loop + Observability** patterns to ensure reliable, production-quality outputs.

---

## Table of Contents

1. [Available Weapons](#available-weapons)
2. [Option A: Deploy as Claude Skills](#option-a-deploy-as-claude-skills)
3. [Option B: Deploy as Custom GPTs](#option-b-deploy-as-custom-gpts)
4. [Usage Examples](#usage-examples)
5. [Team Rollout Strategy](#team-rollout-strategy)
6. [Success Metrics](#success-metrics)

---

## Available Weapons

| Weapon | Purpose | Use Case |
|--------|---------|----------|
| **Pipeline Truth Detector** | Expose stalled deals and truth gap | Weekly pipeline reviews |
| **Deal Defibrillator** | Revive dying deals | Rescue operations for at-risk deals |
| **Forecast Reality Check** | Compare forecast to reality | Before board calls and QBRs |
| **Quota Kill Switch** | Rep performance truth | Weekly 1-on-1s with reps |

All weapons return structured JSON output with tactical recommendations.

---

## Option A: Deploy as Claude Skills

### Prerequisites

- Claude.ai account (Pro or Team plan recommended)
- OR: Anthropic API key for programmatic access

### Deployment Steps

#### Method 1: Claude Projects (Web UI)

**For each weapon:**

1. **Go to Claude.ai**
2. **Click "Projects"** in left sidebar
3. **Click "Create Project"**
4. **Name the project:**
   - "Pipeline Truth Detector"
   - "Deal Defibrillator"
   - "Forecast Reality Check"
   - "Quota Kill Switch"
5. **Click "Project Settings"** → "Custom Instructions"
6. **Copy the entire contents** of the corresponding skill file:
   - `Claude-Skills/pipeline-truth-detector.md`
   - `Claude-Skills/deal-defibrillator.md`
   - `Claude-Skills/forecast-reality-check.md`
   - `Claude-Skills/quota-kill-switch.md`
7. **Paste into Custom Instructions**
8. **Save**

**Usage:**
- Open the project
- Upload CSV file or paste deal data
- Claude automatically analyzes and returns JSON

#### Method 2: API Integration (Programmatic)

**For programmatic access:**

```typescript
import Anthropic from '@anthropic-ai/sdk';
import * as fs from 'fs';

const client = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY
});

// Load skill as system prompt
const skillPrompt = fs.readFileSync(
  './Claude-Skills/pipeline-truth-detector.md',
  'utf-8'
);

// Execute weapon
const response = await client.messages.create({
  model: 'claude-sonnet-4-5',
  max_tokens: 4096,
  temperature: 0.0,
  system: [
    {
      type: "text",
      text: skillPrompt
    }
  ],
  messages: [
    {
      role: 'user',
      content: `Analyze this pipeline:\n\n${csvData}`
    }
  ]
});

const result = JSON.parse(response.content[0].text);
console.log(result);
```

**Cost Estimate:**
- Model: Claude Sonnet 4.5
- Average tokens: ~3,000 per analysis
- Cost: ~$0.02 per analysis
- Monthly (1000 analyses): ~$20

---

## Option B: Deploy as Custom GPTs

### Prerequisites

- ChatGPT Plus or ChatGPT Team account
- GPT builder access (available in Plus/Team)

### Deployment Steps

**For each weapon:**

1. **Go to ChatGPT**
2. **Click "Explore GPTs"** (left sidebar)
3. **Click "Create a GPT"** (top right)
4. **Switch to "Configure" tab**

5. **Fill in GPT Details:**

   **Name:** Copy from Custom GPT file (e.g., "Pipeline Truth Detector - DRN Edition")

   **Description:** Copy from Custom GPT file

   **Instructions:** Copy the entire instructions block from:
   - `Custom-GPTs/pipeline-truth-detector-gpt.md`
   - `Custom-GPTs/deal-defibrillator-gpt.md`
   - `Custom-GPTs/forecast-reality-check-gpt.md`
   - `Custom-GPTs/quota-kill-switch-gpt.md`

   **Conversation Starters:** Copy the 4 starters from the file

   **Knowledge:** (Optional) Upload sample CSV files

   **Capabilities:**
   - ✅ Enable "Code Interpreter"
   - ❌ Disable "DALL-E Image Generation"
   - ❌ Disable "Web Browsing"

   **Actions:** (Leave empty for now)

6. **Configure Access:**
   - Choose "Only people with a link" for DRN team sharing
   - OR "Anyone" for company-wide rollout

7. **Click "Create"**

8. **Copy the GPT link** and share with team

### Sharing GPTs with Team

**Option 1: Direct Link Sharing**
- Copy GPT link from builder
- Share in Slack/Teams channel
- Anyone with link can access

**Option 2: ChatGPT Team Workspace**
- If using ChatGPT Team plan
- GPTs are automatically available to workspace members
- No link sharing needed

**Cost Estimate:**
- ChatGPT Plus: $20/user/month
- ChatGPT Team: $25/user/month (min 2 users)

---

## Usage Examples

### Example 1: Pipeline Truth Detector

**Claude Project:**
```
1. Open "Pipeline Truth Detector" project
2. Upload pipeline.csv
3. Claude returns JSON with stalled deals
```

**Custom GPT:**
```
1. Open "Pipeline Truth Detector - DRN Edition" GPT
2. Click "Analyze my pipeline CSV"
3. Upload file
4. GPT returns JSON
```

**Sample Output:**
```json
{
  "totalPipeline": 2450000,
  "closeablePipeline": 1680000,
  "truthGap": 770000,
  "stalledDeals": [
    {
      "dealName": "Acme Corp Enterprise",
      "amount": 450000,
      "stage": "Negotiation",
      "daysSinceActivity": 52,
      "riskLevel": "CRITICAL"
    }
  ],
  "topProblems": [
    "31% of pipeline ($770K) is stalled over 30 days",
    "Top 2 deals worth $770K combined are both silent 30+ days"
  ],
  "recommendations": [
    "Mark Acme Corp as lost if no response by Friday",
    "Set 14-day activity alerts for Negotiation/Proposal stage"
  ],
  "generatedAt": "2025-11-11T14:30:00.000Z"
}
```

### Example 2: Deal Defibrillator

**Input:**
```
Deal: Acme Corp - Enterprise License
Value: $150,000
Stage: Negotiation
Days Since Activity: 42
Last Activity: Sent proposal, no response
Owner: John Smith
Context: Champion left company 2 weeks ago
```

**Output:**
```json
{
  "dealId": "Acme Corp - Enterprise License",
  "riskScore": 72,
  "rootCause": {
    "primary": "Champion departure killed internal advocacy",
    "evidence": [
      "42 days of silence after proposal sent",
      "Champion left 2 weeks ago"
    ]
  },
  "revivalStrategy": {
    "actions": [
      {
        "priority": 1,
        "description": "VP Sales call new VP of Operations (peer-to-peer)",
        "timeline": "immediate",
        "owner": "EXEC"
      }
    ],
    "urgencyLevel": "CRITICAL"
  },
  "verdict": "AT_RISK"
}
```

---

## Team Rollout Strategy

### Phase 1: Pilot (Week 1-2)

**Goal:** Test with 3-5 power users

**Steps:**
1. Deploy all 4 weapons as Claude Projects AND Custom GPTs
2. Invite sales managers and RevOps team
3. Have them test with real pipeline data
4. Collect feedback on accuracy and usefulness

**Success Criteria:**
- All weapons return valid JSON 90%+ of time
- User satisfaction >4/5
- At least 2 actionable insights per analysis

### Phase 2: Sales Team Rollout (Week 3-4)

**Goal:** Equip all AEs and managers

**Steps:**
1. Host 30-min training session
2. Show how to use each weapon
3. Share GPT/Project links in Slack
4. Create quick reference guide

**Training Outline:**
- **5 min:** Why we built these weapons
- **10 min:** Demo each weapon with live data
- **10 min:** Hands-on practice (upload your pipeline)
- **5 min:** Q&A

### Phase 3: Executive Adoption (Week 5-6)

**Goal:** CRO/VP Sales using for weekly reviews

**Steps:**
1. Create exec dashboard showing weapon usage
2. Integrate outputs into weekly pipeline reviews
3. Track impact on forecast accuracy and deal conversion

---

## Success Metrics

### Technical Metrics

Track these per weapon:

| Metric | Target | How to Measure |
|--------|--------|----------------|
| Valid JSON output rate | >90% | Manual spot checks |
| Response time | <10 seconds | User reported |
| Error rate | <5% | Support tickets |

### Business Metrics

Track these per team:

| Metric | Baseline | Target (3 months) | How to Measure |
|--------|----------|-------------------|----------------|
| Forecast accuracy | TBD | +10% improvement | Compare forecast to actuals |
| Stalled deals revived | 0 | 10+ deals/month | Track recommended actions taken |
| Time spent on pipeline analysis | TBD | -50% reduction | User survey |
| Rep quota attainment | TBD | +5% improvement | CRM reports |

### User Adoption Metrics

| Metric | Target | How to Measure |
|--------|--------|----------------|
| Weekly active users | 100% of sales team | Usage logs |
| Analyses per week per user | 2+ | Usage logs |
| User satisfaction | >4/5 | Quarterly survey |
| Recommendations acted upon | >60% | Follow-up survey |

---

## Troubleshooting

### Common Issues

**Issue: GPT returns prose instead of JSON**

**Solution:**
- Check that instructions were copied correctly
- Ensure "Code Interpreter" is enabled
- Remind user to ask for JSON explicitly if needed

**Issue: Claude Project doesn't seem to use custom instructions**

**Solution:**
- Verify instructions were saved in Project Settings
- Try starting a new conversation in the project
- Check that you're in the correct project

**Issue: JSON parsing errors**

**Solution:**
- Weapons should auto-retry with tighter prompts
- If persistent, check input data quality
- Report to team for prompt refinement

**Issue: Recommendations seem generic**

**Solution:**
- Provide more context in input (last activity details, etc.)
- Check that operating principles emphasize "tactical not theoretical"
- Report examples for prompt improvement

---

## Support & Feedback

### Getting Help

**Technical Issues:**
- Email: tech@drn.com
- Slack: #circuit-os-support

**Feature Requests:**
- Submit via GitHub issues
- Or post in #circuit-os-feedback Slack channel

### Providing Feedback

After each weapon usage, please share:
1. Was the output useful? (👍/👎)
2. Were recommendations actionable?
3. Any errors or issues?

This helps us improve the weapons over time.

---

## Cost Comparison

| Option | Setup Time | Monthly Cost (50 users) | Pros | Cons |
|--------|------------|------------------------|------|------|
| **Claude Projects** | 30 min | $1,000 (API) or $1,000 (50 x $20 Pro) | More reliable, better API | Requires training |
| **Custom GPTs** | 45 min | $1,000 (50 x $20 Plus) or $1,250 (50 x $25 Team) | Familiar interface | Less control |
| **Both** | 1.5 hours | $2,000 | Flexibility, redundancy | Higher cost |

**Recommendation:** Start with Custom GPTs for ease of adoption, add Claude Projects for power users who need API access.

---

## Next Steps

### Week 1: Immediate Actions

- [ ] Choose deployment option (Claude Skills vs Custom GPTs vs Both)
- [ ] Deploy all 4 weapons
- [ ] Identify 5 pilot users
- [ ] Schedule pilot kickoff

### Week 2-3: Pilot Phase

- [ ] Pilot users test all weapons
- [ ] Collect feedback
- [ ] Refine prompts based on feedback
- [ ] Measure success metrics

### Week 4-6: Full Rollout

- [ ] Host team training session
- [ ] Share weapon links with entire team
- [ ] Create quick reference guide
- [ ] Monitor adoption and usage

### Ongoing

- [ ] Weekly usage review
- [ ] Monthly accuracy assessment
- [ ] Quarterly prompt optimization
- [ ] Track ROI (forecast accuracy, deals saved, time saved)

---

## Resources

### File Locations

**Claude Skills:**
- `/Claude-Skills/pipeline-truth-detector.md`
- `/Claude-Skills/deal-defibrillator.md`
- `/Claude-Skills/forecast-reality-check.md`
- `/Claude-Skills/quota-kill-switch.md`

**Custom GPTs:**
- `/Custom-GPTs/pipeline-truth-detector-gpt.md`
- `/Custom-GPTs/deal-defibrillator-gpt.md`
- `/Custom-GPTs/forecast-reality-check-gpt.md`
- `/Custom-GPTs/quota-kill-switch-gpt.md`

**Documentation:**
- `/Docs/ADVANCED-PROMPT-ENGINEERING.md` - Technical implementation guide
- `/Docs/IMPLEMENTATION-EXAMPLE.ts` - Code reference
- `/Docs/LEVERAGE-VIDEO-INSIGHTS-SUMMARY.md` - Quick reference

---

## Version History

- **v1.0** (2025-11-11): Initial DRN deployment guide

---

## Questions?

Contact the Circuit OS team:
- Email: circuitos@drn.com
- Slack: #circuit-os

Let's turn sales pipeline chaos into revenue clarity! 🚀
