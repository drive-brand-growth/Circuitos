# Custom GPT Usage Guide - How to Use Your Circuit OS Weapons

## 🎯 Quick Answer: YES, It Analyzes Pipeline CSV!

All 4 Custom GPTs can analyze CSV files. Here's what you need to know:

---

## What You Need

### 1. ChatGPT Account
- **ChatGPT Plus** ($20/month) - Personal use
- **ChatGPT Team** ($25/user/month) - Team sharing
- **ChatGPT Enterprise** (custom pricing) - Large organizations

### 2. CSV Files
Your pipeline data exported from:
- Salesforce
- HubSpot
- Pipedrive
- GoHighLevel
- Excel/Google Sheets
- Any CRM that exports CSV

### 3. Required CSV Columns

**For Pipeline Truth Detector:**
- `deal_name` or `opportunity_name`
- `amount` or `value`
- `stage`
- `last_activity_date` or `last_activity`

**Optional but helpful:**
- `owner` or `rep_name`
- `close_date`
- `created_date`

**For other GPTs:**
- Similar columns plus probability, forecast amount, etc.

---

## Step-by-Step: Building Your First Custom GPT

### Step 1: Go to ChatGPT
1. Log in to ChatGPT
2. Click **"Explore GPTs"** (left sidebar)
3. Click **"Create a GPT"** (top right)

### Step 2: Configure GPT
1. Click **"Configure"** tab (not "Create")
2. Fill in:

**Name:**
```
Pipeline Truth Detector - Circuit OS
```

**Description:**
```
Expose stalled deals and calculate the "truth gap" between reported and closeable pipeline. Upload your CSV and get tactical recommendations in 90 seconds.
```

**Instructions:**
- Open `CUSTOM-GPT-BUILDER-INSTRUCTIONS.md`
- Copy ENTIRE "Instructions" section for Pipeline Truth Detector
- Paste into GPT Builder

**Conversation Starters:**
Add these 4:
```
1. Analyze my pipeline CSV
2. Show me stalled deals
3. Calculate my truth gap
4. What's killing my pipeline?
```

**Knowledge:**
- Leave empty (or upload sample CSVs for your team)

**Capabilities:**
- ✅ Enable **Code Interpreter**
- ❌ Disable **DALL-E Image Generation**
- ❌ Disable **Web Browsing**

**Actions:**
- Leave empty

### Step 3: Save & Test
1. Click **"Create"**
2. Choose access: **"Only people with a link"**
3. Click **"Save"**
4. Copy the GPT link
5. Test with sample CSV

### Step 4: Share with Team
1. Post link in Slack: `#sales-tools`
2. Add to team wiki/documentation
3. Train team on usage (15 min)

---

## How to Use Each GPT

### 🔍 GPT #1: Pipeline Truth Detector

**Best For:**
- Weekly pipeline reviews
- Preparing for forecast calls
- Identifying stalled deals quickly
- Cleaning up your CRM

**How to Use:**

**Option 1: Upload CSV File**
1. Open the GPT
2. Click **📎 attachment icon**
3. Upload `pipeline_export.csv`
4. GPT automatically analyzes and returns JSON

**Option 2: Paste CSV Text**
1. Open the GPT
2. Copy CSV from Excel/Sheets
3. Paste into chat
4. GPT analyzes immediately

**Example Conversation:**

```
YOU: [Upload pipeline.csv]

GPT: {
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
    },
    {
      "dealName": "TechStart Expansion",
      "amount": 320000,
      "stage": "Proposal",
      "daysSinceActivity": 38,
      "riskLevel": "HIGH"
    }
  ],
  "topProblems": [
    "31% of pipeline ($770K) is stalled over 30 days",
    "Top 2 deals worth $770K combined are both silent 30+ days",
    "Acme Corp in Negotiation for 52 days - deal is dead",
    "No large deals (>$100K) have closed in 45+ days",
    "Pipeline includes fantasy deals inflating forecast"
  ],
  "recommendations": [
    "Mark Acme Corp as lost if no response by Friday - stop wasting cycles",
    "TechStart needs exec call this week - offer discount to close",
    "Remove all deals stalled 60+ days from forecast immediately",
    "Set 14-day activity alerts for Negotiation/Proposal stage",
    "Weekly stalled deal review - 30+ days needs manager involvement"
  ],
  "generatedAt": "2025-11-11T14:30:00.000Z"
}

YOU: Can you explain the Acme Corp situation?

GPT: Acme Corp is CRITICAL because:
- $450K deal (your largest)
- 52 days of silence (almost 2 months)
- Stage: Negotiation (should close fast at this stage)

This deal is likely DEAD. Recommendation:
1. VP Sales calls their VP TODAY
2. If no response in 48 hours, mark as lost
3. Reallocate rep's time to closeable deals

Truth: Keeping dead deals in your pipeline creates false optimism and wastes time.
```

**Use Cases:**
✅ Monday morning pipeline review
✅ Before your weekly 1-on-1 with your boss
✅ Quarterly cleanup (find all stalled deals)
✅ Preparing forecast for board call

---

### 💊 GPT #2: Deal Defibrillator

**Best For:**
- Rescuing specific stalled deals
- Getting tactical revival strategies
- Preparing for "save this deal" meetings
- Training reps on deal rescue

**How to Use:**

**Input Format (paste as text):**
```
Deal: Acme Corp - Enterprise License
Value: $150,000
Stage: Negotiation
Days Since Activity: 42
Last Activity: Sent proposal, no response
Owner: John Smith
Context: Champion left company 2 weeks ago, new contact hasn't responded
```

**Example Output:**
```json
{
  "dealId": "Acme Corp - Enterprise License",
  "riskScore": 72,
  "rootCause": {
    "primary": "Champion departure killed internal advocacy - no one fighting for this deal",
    "secondary": "New contact doesn't have context or relationship with us",
    "evidence": [
      "42 days of silence after proposal sent",
      "Champion left 2 weeks ago (day 28 of silence)",
      "New contact not responding to outreach"
    ]
  },
  "revivalStrategy": {
    "actions": [
      {
        "priority": 1,
        "description": "VP Sales call new VP of Operations (peer-to-peer) - rebuild relationship at exec level",
        "timeline": "immediate",
        "owner": "EXEC"
      },
      {
        "priority": 2,
        "description": "Send new contact case study from their industry + offer 30-min demo reset call",
        "timeline": "24h",
        "owner": "REP"
      },
      {
        "priority": 3,
        "description": "Connect with former champion on LinkedIn - ask for warm intro to replacement",
        "timeline": "24h",
        "owner": "REP"
      }
    ],
    "urgencyLevel": "CRITICAL",
    "estimatedTimeToRevive": "1-2 weeks with exec involvement"
  },
  "verdict": "AT_RISK",
  "nextCheckIn": "2025-11-14T09:00:00.000Z"
}
```

**Use Cases:**
✅ Big deal has gone silent
✅ Deal stuck in same stage for 30+ days
✅ Champion left company
✅ Competitor entered the picture
✅ Preparing for internal "save this deal" meeting

---

### 📈 GPT #3: Forecast Reality Check

**Best For:**
- Before QBR (Quarterly Business Review)
- Before board calls
- Weekly forecast accuracy checks
- Calling out sandbagging/over-optimism

**How to Use:**

**Input Format:**
```
Reported Forecast: $2,500,000

Pipeline Data:
[paste CSV with: deal_name, amount, stage, close_date, probability, rep_name]
```

**Output:**
Shows you:
- Actual forecast vs reported
- Which deals are at risk (shouldn't be in forecast)
- Which deals are safe
- Drift trend
- Recommendations

**Use Cases:**
✅ Sunday night before Monday forecast call
✅ Friday before QBR
✅ When CFO asks "Are we hitting the number?"
✅ Identifying which reps are sandbagging/over-forecasting

---

### ⚡ GPT #4: Quota Kill Switch

**Best For:**
- Weekly 1-on-1s with reps
- End of month/quarter check-ins
- PIP (Performance Improvement Plan) decisions
- Territory planning

**How to Use:**

**Input Format:**
```
Rep: John Smith
Quota: $500,000
Current Progress: $180,000
Days Remaining: 45
Pipeline: $580,000
Historical Close Rate: 35%
```

**Output:**
Shows you:
- On track? (yes/no)
- Gap to quota
- Required daily close rate
- Pipeline coverage
- Verdict (ON_TRACK, AT_RISK, CRITICAL, UNRECOVERABLE)
- Specific next actions

**Use Cases:**
✅ Monday morning rep performance review
✅ Friday check-in: "Will we hit the number?"
✅ Deciding who needs help this week
✅ PIP/termination decisions (data-driven, not gut feel)

---

## Best Practices

### 📊 Data Quality Tips

**DO:**
✅ Export fresh data (not stale snapshots)
✅ Include all required columns
✅ Use consistent date formats (YYYY-MM-DD)
✅ Clean up blank rows before uploading

**DON'T:**
❌ Upload files >10MB (paginate if needed)
❌ Mix different deal types in one CSV
❌ Include sensitive data (GPT stores conversations)
❌ Use special characters in deal names

### 🎯 Getting Better Results

**Be Specific with Context:**
```
BAD:  "Analyze this deal"
GOOD: "Deal: Acme Corp, $150K, 42 days silent, champion left - is this savable?"
```

**Ask Follow-ups:**
```
GPT: [Returns JSON analysis]

YOU: "What's the highest priority action for Acme Corp?"
GPT: "VP Sales call their VP TODAY. If no response in 48 hours, mark as lost."
```

**Iterate:**
```
YOU: "Can you give me a different revival strategy that doesn't require exec involvement?"
GPT: [Returns alternative approach]
```

### 🔄 Weekly Workflow

**Monday Morning:**
1. Export pipeline from CRM → CSV
2. Upload to Pipeline Truth Detector
3. Review stalled deals
4. Pick top 3 to revive
5. Use Deal Defibrillator for each

**Friday Afternoon:**
1. Update pipeline
2. Run Forecast Reality Check
3. Prepare for Monday forecast call
4. Flag at-risk deals

**End of Month:**
1. Export rep performance data
2. Run Quota Kill Switch for each rep
3. Prepare 1-on-1 talking points
4. Identify who needs help

---

## Advanced Use Cases

### 🔥 Emergency Triage

**Scenario:** "I have 20 stalled deals. Which 3 should I focus on?"

**Solution:**
1. Upload all 20 to Pipeline Truth Detector
2. GPT ranks by risk level
3. Focus on CRITICAL deals first
4. Use Deal Defibrillator on top 3

### 📉 Forecast Forensics

**Scenario:** "We missed forecast by 30%. Why?"

**Solution:**
1. Upload deals that were forecasted to close
2. Use Forecast Reality Check
3. Identify patterns (stage duration, rep accuracy, etc.)
4. Use insights to improve next quarter

### 🎓 Training New Reps

**Scenario:** "New rep needs to learn deal rescue"

**Solution:**
1. Take their stalled deal
2. Run through Deal Defibrillator together
3. Show them the revival strategy
4. Have them execute actions
5. Review outcomes next week

---

## Troubleshooting

### Issue: GPT Returns Prose Instead of JSON

**Fix:**
- Check that "Code Interpreter" is enabled
- Remind GPT: "Return only JSON, no prose"
- Re-paste instructions if needed

### Issue: CSV Parse Errors

**Fix:**
- Ensure file is .csv (not .xlsx)
- Check for special characters
- Try pasting as text instead of uploading

### Issue: Missing Columns

**Fix:**
- Export required columns from CRM
- Or rename columns in CSV to match expected names

### Issue: Results Not Helpful

**Fix:**
- Add more context in your question
- Include last activity details
- Specify what outcome you want

---

## What Else You Can Do

### 🔧 Customize for Your Business

**Add your own rules:**
```
YOU: "In our business, any deal in Negotiation for >21 days (not 30) is CRITICAL"

GPT: "Understood. I'll adjust the stalled deal criteria for you."
```

**Add your stages:**
```
YOU: "Our stages are: Discovery, Demo, Trial, Negotiation, Closed Won"

GPT: "Got it. I'll use those exact stage names."
```

### 📊 Create Custom Views

**Example:**
```
YOU: "Show me only deals >$100K that are CRITICAL"

GPT: [Filters and shows subset]
```

### 🤝 Team Calibration

**Use Case:** Get your whole team on the same page

**Process:**
1. Run same CSV through GPT
2. Share results in team meeting
3. Discuss: Do we agree with risk levels?
4. Calibrate definitions if needed

---

## ROI Tracking

### Time Saved

**Before Custom GPT:**
- Manual pipeline analysis: 2-3 hours/week
- Stalled deal identification: 1 hour/week
- Forecast prep: 2 hours/week
- Total: **5-6 hours/week**

**After Custom GPT:**
- Upload CSV, get analysis: 2 minutes
- Review results, take action: 30 minutes
- Total: **~30 minutes/week**

**Time Saved:** **4.5-5.5 hours/week per person**

### Value Created

**For a sales team of 10:**
- Time saved: 45-55 hours/week
- Cost saved: ~$2,500/week (at $50/hr)
- Annual savings: **~$130,000**

**Plus:**
- Faster deal closure (less time stalled)
- Higher forecast accuracy
- Better pipeline hygiene
- More time selling

---

## Next Steps

### Immediate (Today)
1. Build your first Custom GPT (15 min)
2. Export pipeline CSV from CRM
3. Test with Pipeline Truth Detector
4. Share results with your team

### This Week
1. Build all 4 Custom GPTs
2. Train team on usage (30 min)
3. Add to weekly workflow
4. Track time saved

### This Month
1. Measure forecast accuracy improvement
2. Track deals revived
3. Document ROI
4. Expand to more team members

---

## Support

**Questions?**
- Check `DEPLOYMENT-GUIDE-DRN.md` for detailed setup
- Review `QUICK-REFERENCE-CARD.md` for quick tips
- All docs in `/Circuitos/Docs/` and `/Custom-GPTs/`

**Issues?**
- Re-copy instructions from `CUSTOM-GPT-BUILDER-INSTRUCTIONS.md`
- Verify "Code Interpreter" is enabled
- Check CSV format matches requirements

---

## Summary

### ✅ YES, It Analyzes Pipeline CSV!

**What you need:**
1. ChatGPT Plus/Team account ($20-25/month)
2. CSV files from your CRM
3. 15 minutes to build each GPT

**What you get:**
1. Pipeline Truth Detector - Find stalled deals in 90 seconds
2. Deal Defibrillator - Get revival strategies
3. Forecast Reality Check - Compare forecast to reality
4. Quota Kill Switch - Check who's on/off track

**Time to value:** **<30 minutes** from start to first insight

**ROI:** **4-5 hours saved per week** + better pipeline management

---

**Ready to build?** Open `CUSTOM-GPT-BUILDER-INSTRUCTIONS.md` and copy-paste to get started! 🚀
