# Circuit OS Weapons - Quick Reference Card

## 🎯 4 Weapons, 4 Use Cases

| Weapon | When to Use | Input | Output |
|--------|-------------|-------|--------|
| **Pipeline Truth Detector** | Weekly pipeline review | CSV with deals | Stalled deals + truth gap |
| **Deal Defibrillator** | Deal at risk | Deal details | Revival strategy |
| **Forecast Reality Check** | Before board call | Forecast + pipeline | Drift analysis |
| **Quota Kill Switch** | Weekly rep 1-on-1 | Rep performance data | On/off track verdict |

---

## 📊 Pipeline Truth Detector

**Use:** Find stalled deals killing your pipeline

**Input:**
```csv
deal_name,amount,stage,last_activity_date
Acme Corp,150000,Negotiation,2025-10-01
TechStart,25000,Discovery,2025-11-08
```

**Output:** JSON with:
- Total pipeline vs closeable pipeline
- Truth gap ($)
- Stalled deals with risk levels
- Top 5 problems
- Top 5 tactical recommendations

**Quick Access:**
- Claude: Project "Pipeline Truth Detector"
- GPT: "Pipeline Truth Detector - DRN Edition"

---

## 💊 Deal Defibrillator

**Use:** Save a dying deal before it's lost

**Input:**
```
Deal: Acme Corp - $150K
Stage: Negotiation
Days Silent: 42
Context: Champion left company
```

**Output:** JSON with:
- Risk score (0-100)
- Root cause analysis
- 3-5 revival actions (priority, owner, timeline)
- Verdict: RECOVERABLE, AT_RISK, CRITICAL, UNRECOVERABLE

**Quick Access:**
- Claude: Project "Deal Defibrillator"
- GPT: "Deal Defibrillator - DRN Edition"

---

## 📈 Forecast Reality Check

**Use:** Compare reported forecast to reality

**Input:**
```
Reported Forecast: $2.5M
Pipeline data: deals with probabilities
```

**Output:** JSON with:
- Actual forecast vs reported
- Drift amount and %
- At-risk deals in forecast
- Safe deals
- Recommendations to close gap

**Quick Access:**
- Claude: Project "Forecast Reality Check"
- GPT: "Forecast Reality Check - DRN Edition"

---

## ⚡ Quota Kill Switch

**Use:** Check if rep will hit quota

**Input:**
```
Rep: John Smith
Quota: $500K
Current: $180K
Days Left: 45
Pipeline: $580K
```

**Output:** JSON with:
- Progress % and gap
- Required daily close rate
- Pipeline coverage (xX)
- Verdict: ON_TRACK, AT_RISK, CRITICAL, UNRECOVERABLE
- Next action

**Quick Access:**
- Claude: Project "Quota Kill Switch"
- GPT: "Quota Kill Switch - DRN Edition"

---

## 🚀 How to Use

### Claude Projects
1. Open project
2. Upload CSV or paste data
3. Get JSON output

### Custom GPTs
1. Open GPT
2. Click conversation starter or upload file
3. Get JSON output

---

## ✅ Output Format

**All weapons return structured JSON:**
- No prose
- Strict schema
- Tactical recommendations (<200 chars each)
- ISO timestamps

---

## 📏 Success Criteria

| Risk Level | Criteria |
|------------|----------|
| **LOW** | 0-14 days since activity |
| **MEDIUM** | 15-30 days |
| **HIGH** | 31-60 days |
| **CRITICAL** | 60+ days OR >$100K with 45+ day gap |

---

## 💰 Cost

**Claude API:** ~$0.02 per analysis
**Claude Projects:** $20/user/month (Pro plan)
**Custom GPTs:** $20/user/month (Plus) or $25/user/month (Team)

---

## 📞 Support

**Slack:** #circuit-os-support
**Email:** circuitos@drn.com
**Docs:** `/Docs/` folder

---

## 🎓 Training

**30-min session covers:**
1. Why these weapons exist (5 min)
2. Demo each weapon (10 min)
3. Hands-on practice (10 min)
4. Q&A (5 min)

---

## 📈 Track These Metrics

**Weekly:**
- Weapons used
- Valid JSON rate
- User feedback (👍/👎)

**Monthly:**
- Forecast accuracy improvement
- Deals revived
- Time saved

---

## 🔥 Pro Tips

1. **Upload CSV directly** - faster than pasting
2. **Include context** - more context = better recommendations
3. **Act on recommendations** - these are tactical, not theoretical
4. **Share wins** - post in #circuit-os-wins when a weapon saves a deal
5. **Provide feedback** - helps us improve the prompts

---

**Print this card or save to desktop for quick reference!**

**Version:** 1.0 | **Date:** 2025-11-11
