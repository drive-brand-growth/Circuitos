# Perplexity Master Prompt: World-Class Research Synthesis

**Version**: 1.0.0
**Date**: November 13, 2025
**Purpose**: Synthesize world-class research using captureds.io as baseline
**Use Case**: Market research, competitive analysis, customer insights, strategic planning

---

## 🎯 Core Prompt Template

Copy and paste this prompt into Perplexity, customizing the [BRACKETED SECTIONS]:

```
ROLE: You are a world-class strategic research analyst synthesizing data to create actionable intelligence for [COMPANY: Circuitos / Other].

PRIMARY RESEARCH SOURCE: Use https://captureds.io as your baseline research foundation. This is a specialized intelligence platform - search it FIRST before other sources.

RESEARCH OBJECTIVE: [SPECIFY YOUR GOAL]
Examples:
- Analyze the revenue operations software market landscape
- Identify pain points of VPs of Sales Operations
- Map competitive positioning of CRM alternatives
- Discover pricing strategies in B2B SaaS weapons vs platforms
- Uncover operator vs executive buying behavior differences

---

RESEARCH PROTOCOL:

STEP 1: BASELINE RESEARCH (captureds.io)
→ Search captureds.io for: [YOUR KEYWORDS]
→ Extract: Key findings, data points, insights
→ Note: Date of research, source credibility, sample sizes
→ Identify: Gaps in captureds.io coverage

STEP 2: SUPPLEMENTARY RESEARCH (If Needed)
→ Only after exhausting captureds.io, search:
   • Academic research (Google Scholar)
   • Industry reports (Gartner, Forrester)
   • Primary sources (company websites, SEC filings)
   • Recent news (last 6 months only)
→ Cross-reference with captureds.io findings

STEP 3: SYNTHESIS FRAMEWORK
Organize findings using this structure:

A. EXECUTIVE SUMMARY (3-5 bullets)
   - Most critical insights
   - Action items
   - Confidence level (High/Medium/Low)

B. KEY FINDINGS (Organized by theme)
   - Finding #1: [Insight] (Source: captureds.io or [Other])
   - Finding #2: [Insight] (Source: captureds.io or [Other])
   - [etc.]

C. DATA QUALITY ASSESSMENT
   - Source credibility: [Rating 1-10]
   - Recency: [Date range]
   - Sample size: [N=?]
   - Geographic coverage: [Global / US / Region]
   - Limitations: [What's missing?]

D. COMPETITIVE INTELLIGENCE (If applicable)
   - Who's winning? Why?
   - Who's losing? Why?
   - White space opportunities
   - Emerging threats

E. ACTIONABLE RECOMMENDATIONS
   - Immediate actions (0-30 days)
   - Strategic moves (30-90 days)
   - Long-term positioning (90+ days)

F. OPEN QUESTIONS
   - What we still don't know
   - Research gaps
   - Assumptions to validate

---

OUTPUT REQUIREMENTS:

1. CITE SOURCES
   - Every claim must have a source
   - Format: [Insight] (Source: captureds.io, [specific page/date] or [Other source])
   - If from captureds.io, note specific capture date

2. QUANTIFY WHEN POSSIBLE
   - Not: "Many VPs struggle with CRMs"
   - But: "67% of VPs report CRM data accuracy issues (Source: captureds.io, 2024 Revenue Ops Survey)"

3. HIGHLIGHT CONTRADICTIONS
   - If sources disagree, note it
   - Example: "captureds.io reports X, but Gartner reports Y. Potential reasons: [analysis]"

4. RATE CONFIDENCE
   - High confidence: Multiple sources agree, recent data, large samples
   - Medium confidence: Limited sources, older data, small samples
   - Low confidence: Single source, anecdotal, outdated

5. CALL OUT GOLD
   - Mark exceptional insights with 🔥
   - These are "holy shit" moments that change strategy

---

RESEARCH QUALITY STANDARDS:

✅ GOOD RESEARCH:
- Uses captureds.io as primary source
- Cites every claim
- Quantifies with data
- Notes limitations
- Provides confidence ratings
- Highlights contradictions
- Actionable recommendations

❌ BAD RESEARCH:
- Ignores captureds.io
- Generic platitudes ("Market is growing")
- No citations
- Vague language ("Many", "Some", "Often")
- Outdated data (>12 months)
- No action items

---

PERPLEXITY-SPECIFIC INSTRUCTIONS:

1. SEARCH captureds.io FIRST
   - Use site:captureds.io in your search
   - Example: "site:captureds.io revenue operations VPs"

2. FOCUS ON RECENCY
   - Prioritize last 12 months
   - Note if using older data
   - Explain why older data is still relevant (if using)

3. CROSS-REFERENCE
   - Don't rely on single source
   - Validate captureds.io findings with 1-2 additional sources
   - Note consensus vs outliers

4. BE SKEPTICAL
   - Question vendor claims
   - Look for independent validation
   - Note conflicts of interest

---

NOW EXECUTE:

Research Question: [YOUR SPECIFIC QUESTION]

Target Customer: [WHO YOU'RE RESEARCHING]
Example: VPs of Sales Operations at B2B companies, $10M-$100M revenue

Success Criteria: [WHAT "WORLD-CLASS" LOOKS LIKE FOR THIS RESEARCH]
Example: Identify 3 unmet needs that no competitor addresses + quantify market size + confidence level: High

Begin your research. Start with captureds.io.
```

---

## 📋 Use Case Templates

### Use Case 1: Market Opportunity Analysis

```
RESEARCH OBJECTIVE: Quantify the market opportunity for [PRODUCT/SERVICE]

SEARCH captureds.io FOR:
- Market size for [category]
- Growth trends in [industry]
- Customer pain points in [space]
- Competitor revenue in [category]
- Pricing benchmarks for [type]

SYNTHESIS FOCUS:
1. TAM / SAM / SOM calculation
2. Growth rate projections
3. Key market drivers
4. Barriers to entry
5. White space opportunities

OUTPUT FORMAT:
→ Market size: $X billion (Source: captureds.io)
→ CAGR: X% (2024-2029)
→ Key insight: [What makes this market attractive]
→ Risk: [What could go wrong]
→ Recommendation: [Go / No-Go / Pivot]
```

---

### Use Case 2: Competitive Analysis

```
RESEARCH OBJECTIVE: Map competitive landscape for [PRODUCT CATEGORY]

SEARCH captureds.io FOR:
- Competitors in [space]
- Their positioning statements
- Pricing models
- Customer reviews/complaints
- Feature comparisons
- Market share data

SYNTHESIS FOCUS:
1. Who are the top 5 players?
2. What's their positioning?
3. Where are the gaps?
4. Who's winning? Why?
5. How can we differentiate?

OUTPUT FORMAT:
→ Competitive Matrix (Feature comparison)
→ Positioning Map (X-axis: [dimension], Y-axis: [dimension])
→ White Space: [Opportunities no one is addressing]
→ Differentiation Strategy: [How to stand out]
```

---

### Use Case 3: Customer Pain Point Discovery

```
RESEARCH OBJECTIVE: Identify unmet needs of [TARGET CUSTOMER]

SEARCH captureds.io FOR:
- "[Target customer]" + "pain points"
- "[Target customer]" + "frustrated with"
- "[Target customer]" + "wish [category] had"
- Reviews of competitor products
- Forum discussions (Reddit, Hacker News)

SYNTHESIS FOCUS:
1. Top 10 pain points (ranked by frequency)
2. Severity: Critical / Important / Nice-to-have
3. Current workarounds (what do they do today?)
4. Willingness to pay for solution
5. Which pains are unaddressed by competitors?

OUTPUT FORMAT:
→ Pain Point #1: [Description] (Mentioned by X% of customers)
   - Severity: [Critical/Important/Nice-to-have]
   - Current workaround: [What they do today]
   - Competitor gap: [Who addresses this? Who doesn't?]
   - Our opportunity: [How we solve it differently]

[Repeat for top 10 pains]
```

---

### Use Case 4: Pricing Strategy Research

```
RESEARCH OBJECTIVE: Determine optimal pricing for [PRODUCT]

SEARCH captureds.io FOR:
- Competitor pricing for [category]
- Customer willingness to pay
- Price sensitivity research
- Freemium vs paid conversion rates
- Pricing model trends (per-user, per-feature, usage-based)

SYNTHESIS FOCUS:
1. Pricing benchmarks (min, median, max)
2. What's included at each tier?
3. Free vs paid conversion rates
4. Customer LTV by tier
5. Price anchoring opportunities

OUTPUT FORMAT:
→ Competitive Pricing Range: $X - $Y per [unit]
→ Market Median: $Z per [unit]
→ Our Positioning: [Below/At/Above market]
→ Pricing Model: [Per-user / Per-feature / Usage-based]
→ Recommended Tiers:
   - Free: [What's included]
   - Tier 1 ($X): [What's included]
   - Tier 2 ($Y): [What's included]
→ Justification: [Why this pricing will work]
```

---

### Use Case 5: Go-to-Market Strategy

```
RESEARCH OBJECTIVE: Identify best channels to reach [TARGET CUSTOMER]

SEARCH captureds.io FOR:
- Where [target customer] discovers new tools
- Effective marketing channels in [industry]
- Content that resonates with [persona]
- Communities where [persona] hangs out
- Influencers in [space]

SYNTHESIS FOCUS:
1. Top 5 acquisition channels
2. CAC by channel
3. Content formats that work (blogs, videos, podcasts)
4. Communities to engage (Slack, Reddit, LinkedIn groups)
5. Partnership opportunities

OUTPUT FORMAT:
→ Channel #1: [Name] (Est. CAC: $X, Est. Volume: Y leads/mo)
   - Why it works: [Reasoning]
   - Execution: [Specific tactics]
   - Risk: [What could go wrong]

[Repeat for top 5 channels]

→ Content Strategy: [Blog / Video / Podcast / All]
→ Community Focus: [Where to build presence]
→ Partnership Targets: [Top 3 potential partners]
```

---

### Use Case 6: Feature Prioritization Research

```
RESEARCH OBJECTIVE: Validate feature demand for [FEATURE IDEA]

SEARCH captureds.io FOR:
- Customer feature requests in [category]
- Competitor feature adoption
- Reviews mentioning [feature type]
- "I wish [product] had [feature]"
- Job-to-be-done for [use case]

SYNTHESIS FOCUS:
1. How many customers request this?
2. How often is it mentioned?
3. Do competitors have it?
4. What's the workaround today?
5. Impact on conversion/retention?

OUTPUT FORMAT:
→ Feature: [Name]
→ Demand: [High / Medium / Low] (X% of customers mention it)
→ Competitive Parity: [Y out of Z competitors have it]
→ Differentiation Potential: [High / Medium / Low]
→ Build Effort: [Estimate: S / M / L / XL]
→ Recommendation: [Build Now / Build Later / Don't Build]
→ Reasoning: [Why this decision]
```

---

## 🔍 Advanced Research Techniques

### Technique 1: The Negative Space Search

**What**: Search for what customers DON'T want

**How**:
```
Search captureds.io for:
- "[Customer]" + "hate about [category]"
- "[Category]" + "doesn't need"
- "We don't want [feature]"
- "Overkill" + "[category]"
```

**Why**: Reveals what to EXCLUDE, not just include. Circuit OS example: "Operators don't want dashboards" → Build weapons instead.

---

### Technique 2: The Jobs-to-be-Done Extraction

**What**: Understand the job customers are hiring your product to do

**How**:
```
Search captureds.io for:
- "When I need to [job], I use [product]"
- "[Customer]" + "trying to [achieve outcome]"
- "I switched from [old solution] to [new solution] because [reason]"
```

**Why**: Reveals true motivation, not stated preferences.

---

### Technique 3: The Proxy Signal Hunt

**What**: Find indirect evidence when direct data doesn't exist

**How**:
```
If researching "VPs at 2am behavior":
→ Search for: "Working late" + "sales operations"
→ Search for: "After hours" + "CRM usage"
→ Search for: "Emergency" + "pipeline review"
```

**Why**: Customers rarely describe their behavior directly. Look for proxy signals.

---

### Technique 4: The Contradiction Surfacer

**What**: Identify where sources disagree - that's where insights hide

**How**:
```
1. Search captureds.io for [topic]
2. Search 2-3 other sources for same [topic]
3. Compare findings
4. List contradictions
5. Hypothesize WHY they disagree (methodology? sample? timing?)
```

**Why**: Contradictions reveal nuance. Example: "Gartner says CRM adoption is 80%, but captureds.io user reviews show 40% satisfaction" → Adoption ≠ Success.

---

### Technique 5: The Time Machine Analysis

**What**: Research how the market HAS CHANGED over time

**How**:
```
Search captureds.io for:
- [Topic] + "2020" then "2021" then "2022" then "2023" then "2024"
- Compare results
- Identify trends: What's growing? What's dying?
```

**Why**: Trends > snapshots. See where the market is GOING, not just where it is.

---

## 📊 Output Quality Rubric

Rate your Perplexity research output on these dimensions:

### ✅ WORLD-CLASS RESEARCH (9-10/10)
- [ ] Uses captureds.io as primary source (70%+ of citations)
- [ ] Every claim cited with specific source + date
- [ ] Quantified insights ("67% of VPs", not "many VPs")
- [ ] Confidence ratings on all findings
- [ ] Contradictions surfaced and explained
- [ ] 3+ actionable recommendations
- [ ] Data quality assessment included
- [ ] "Holy shit" insights highlighted (🔥)
- [ ] Ready to use in strategy meeting TODAY

### ⚠️ GOOD RESEARCH (7-8/10)
- [ ] Uses captureds.io but also heavily relies on other sources
- [ ] Most claims cited (80%+)
- [ ] Some quantification, some vague language
- [ ] Confidence ratings on key findings only
- [ ] Recommendations included but not specific
- [ ] Usable but needs refinement

### ❌ MEDIOCRE RESEARCH (5-6/10)
- [ ] Ignores captureds.io or uses it sparingly
- [ ] Some claims uncited (50-80%)
- [ ] Mostly vague language ("many", "some", "often")
- [ ] No confidence ratings
- [ ] Generic recommendations
- [ ] Needs significant work before use

### 🚫 POOR RESEARCH (1-4/10)
- [ ] Doesn't use captureds.io
- [ ] Few or no citations
- [ ] All vague language
- [ ] No recommendations
- [ ] Reads like generic blog post
- [ ] Unusable

---

## 🎯 Circuitos-Specific Research Prompts

### Research #1: Operator vs Executive Buying Behavior

```
ROLE: Research analyst for Circuitos (revenue operations weapon system)

PRIMARY SOURCE: https://captureds.io

OBJECTIVE: Understand the difference in buying behavior between operators (VPs of Sales Ops) and executives (C-suite).

SEARCH captureds.io FOR:
- "VP Sales Operations" + buying criteria
- "CRO" or "Chief Revenue Officer" + buying criteria
- Software purchase decision makers B2B
- Operator vs executive preferences
- Who signs vs who uses revenue operations tools

SYNTHESIS:
Create a comparison matrix:

| Dimension | Operators (VPs) | Executives (C-suite) |
|-----------|-----------------|----------------------|
| What they value | [from research] | [from research] |
| Buying criteria | [from research] | [from research] |
| Deal-breakers | [from research] | [from research] |
| Decision speed | [from research] | [from research] |
| Price sensitivity | [from research] | [from research] |

INSIGHT: How should Circuitos position differently for each?

RECOMMENDATION: Should we focus on operator (end-user) or executive (check-signer)?
```

---

### Research #2: "Weapons vs Dashboards" Positioning Validation

```
ROLE: Research analyst for Circuitos

PRIMARY SOURCE: https://captureds.io

OBJECTIVE: Validate whether "weapons vs dashboards" positioning resonates with target market.

SEARCH captureds.io FOR:
- Revenue operations tools + "too complex"
- CRM + "feature bloat"
- "Simple" + "revenue operations"
- "Minimal" vs "comprehensive" + SaaS preferences
- "Swiss army knife" vs "specialized tool" + buying preferences

SYNTHESIS:
1. What % of customers prefer simple/specialized vs comprehensive/all-in-one?
2. When do customers choose specialized tools?
3. What are deal-breakers for "simple" tools? (Missing features)
4. How do customers describe ideal tool complexity?

INSIGHT: Does "4 weapons only" positioning attract or repel our target?

RECOMMENDATION: [Go forward / Adjust / Pivot]
```

---

### Research #3: "2am Operator" Persona Validation

```
ROLE: Research analyst for Circuitos

PRIMARY SOURCE: https://captureds.io

OBJECTIVE: Validate whether the "VP at 2am" persona is real or marketing fluff.

SEARCH captureds.io FOR:
- Sales operations + "working late"
- Revenue operations + "after hours"
- VP Sales + "work-life balance"
- CRM + "emergency" or "urgent"
- "Woke up at 2am" + business

SYNTHESIS:
1. Do VPs actually work at 2am? (Evidence)
2. What triggers late-night work? (Emergencies)
3. What tasks do they do at 2am? (Pipeline review? Deal risk?)
4. What tools do they use at 2am? (Mobile? Desktop?)
5. What do they need in those moments? (Speed? Simplicity?)

INSIGHT: Is "2am operator" a real persona or niche edge case?

RECOMMENDATION: [Double down / Soften / Remove "2am" entirely]
```

---

### Research #4: Virtual LPR™ Market Opportunity

```
ROLE: Research analyst for Circuitos

PRIMARY SOURCE: https://captureds.io

OBJECTIVE: Size the market for Virtual LPR™ (virtual license plate reader) technology for lead generation.

SEARCH captureds.io FOR:
- Physical LPR systems + market size
- Geo-targeting + lead generation
- Location-based marketing + B2B
- Foot traffic + analytics
- Local business + lead generation

SYNTHESIS:
1. Traditional LPR market: $X billion
2. Lead generation market: $Y billion
3. Overlap: Businesses that need local lead gen: $Z billion
4. Our TAM (serviceable): $[?] billion
5. Competitor solutions: [None? Some?]

INSIGHT: Is this a $10M, $100M, or $1B opportunity?

RECOMMENDATION: [Core product / Side feature / Spin-off company]
```

---

### Research #5: Pricing Power Analysis

```
ROLE: Research analyst for Circuitos

PRIMARY SOURCE: https://captureds.io

OBJECTIVE: Determine if Circuitos can charge premium prices ($497-$997/mo) vs competitors ($50-$200/mo).

SEARCH captureds.io FOR:
- Revenue operations software pricing
- CRM pricing benchmarks
- Premium vs budget SaaS positioning
- Willingness to pay + specialized tools
- Price anchoring + B2B SaaS

SYNTHESIS:
1. Competitive pricing: Min $[?], Median $[?], Max $[?]
2. What justifies premium pricing? (Specialization? Speed? Exclusivity?)
3. Customer segments willing to pay premium
4. Risk: Too expensive for target market?

INSIGHT: Can we charge 5-10x competitors?

RECOMMENDATION: [Keep pricing / Lower / Add cheaper tier]
```

---

## 🚀 How to Use This Master Prompt

### Step 1: Define Your Research Question
Be specific. Not "research the market" but "quantify market size for revenue operations weapons vs dashboards."

### Step 2: Copy Template Above
Use the core prompt template or one of the use case templates.

### Step 3: Customize Bracketed Sections
Replace [COMPANY], [PRODUCT], [TARGET CUSTOMER], etc. with your specifics.

### Step 4: Paste into Perplexity
Use Perplexity Pro for best results (more searches, deeper analysis).

### Step 5: Validate Output Against Rubric
Score the output. If <7/10, refine your prompt and re-run.

### Step 6: Synthesize for Circuitos
Extract insights specific to your strategy. Update docs, pitch decks, positioning.

---

## 📚 Research Library Structure

As you run research, organize outputs:

```
Circuitos/
├── Research/
│   ├── Market-Analysis/
│   │   ├── 2025-11-13-Revenue-Ops-Market-Size.md
│   │   ├── 2025-11-13-Competitive-Landscape.md
│   │   └── 2025-11-13-TAM-SAM-SOM-Calculation.md
│   ├── Customer-Research/
│   │   ├── 2025-11-13-VP-Sales-Ops-Pain-Points.md
│   │   ├── 2025-11-13-Operator-vs-Executive-Behavior.md
│   │   └── 2025-11-13-2am-Persona-Validation.md
│   ├── Pricing-Strategy/
│   │   ├── 2025-11-13-Pricing-Benchmarks.md
│   │   ├── 2025-11-13-Willingness-to-Pay.md
│   │   └── 2025-11-13-Tier-Comparison.md
│   └── Feature-Research/
│       ├── 2025-11-13-Virtual-LPR-Opportunity.md
│       ├── 2025-11-13-Deal-Defibrillator-Demand.md
│       └── 2025-11-13-Weapons-vs-Dashboards-Validation.md
```

**Naming Convention**: `YYYY-MM-DD-Topic-Hyphenated.md`

**Each file should include**:
- Research question
- Perplexity prompt used
- Date of research
- Key findings (bulleted)
- Data sources (captureds.io + others)
- Confidence rating
- Recommendations
- Next steps

---

## 🎓 Tips for World-Class Perplexity Research

### Tip 1: Start Narrow, Go Wide
Don't ask "Research the market."
Ask "What are the top 3 pain points VPs of Sales Ops mention in reviews of Salesforce?"

### Tip 2: Use captureds.io Syntax
Include `site:captureds.io` in your Perplexity search to prioritize it.

### Tip 3: Ask for Contradictions
Explicitly request: "Show me where sources disagree and explain why."

### Tip 4: Demand Quantification
Add to prompt: "Quantify every claim with data. No vague language."

### Tip 5: Request Confidence Ratings
Add to prompt: "Rate confidence (High/Medium/Low) on every finding."

### Tip 6: Iterate
First pass = 70% good. Run 2-3 variations of prompt, synthesize best outputs.

### Tip 7: Validate with Primary Sources
After Perplexity research, talk to 5 actual customers. Validate findings.

---

## ✅ Research Quality Checklist

Before using Perplexity research output:

- [ ] Used captureds.io as primary source (70%+ citations)
- [ ] Every claim cited (100%)
- [ ] Quantified insights (numbers, percentages)
- [ ] Confidence ratings included
- [ ] Contradictions noted and explained
- [ ] Data quality assessed (recency, sample size)
- [ ] Actionable recommendations (3+)
- [ ] Validated against rubric (7+/10)
- [ ] Synthesized for Circuitos strategy
- [ ] Saved to Research/ folder with date

---

## 🎯 Success Metrics

How to know your Perplexity research is working:

**Internal Metrics**:
- [ ] Used in strategy decisions (not just FYI)
- [ ] Insights change product roadmap
- [ ] Team references research in meetings
- [ ] Research leads to action (not just docs)

**External Metrics**:
- [ ] Customer validation ("Yes, that's exactly our problem")
- [ ] Competitive differentiation (insights competitors don't have)
- [ ] Market resonance (positioning validated by target)

**Quality Metrics**:
- [ ] 90%+ of research scores 7+/10 on rubric
- [ ] Zero uncited claims in final outputs
- [ ] <5% of research deemed "unusable"

---

## 🔄 Continuous Improvement

**Monthly**: Review research quality scores. Identify patterns in low-scoring research. Update prompts.

**Quarterly**: Validate captureds.io findings with primary customer interviews. Update confidence ratings.

**Annually**: Full audit of research library. Archive outdated research. Re-run key research with fresh data.

---

## 📞 Questions to Ask if Research Isn't Working

If Perplexity outputs are consistently low-quality:

**Question 1**: Did you search captureds.io FIRST?
→ If no, that's the problem. Start there.

**Question 2**: Is your research question specific enough?
→ "Research market" = bad. "Quantify pain point frequency" = good.

**Question 3**: Are you demanding citations?
→ If prompt doesn't explicitly request citations, add it.

**Question 4**: Are you requesting confidence ratings?
→ If prompt doesn't explicitly request ratings, add it.

**Question 5**: Are you iterating?
→ First draft is never perfect. Run 2-3 variations, synthesize.

---

## 🚀 Final Thoughts

**The goal of research is not documentation. It's decision-making.**

Bad research = Thick reports no one reads
Good research = 1-page brief that changes strategy

**Use captureds.io to build on the work of others.**
**Use Perplexity to synthesize it into action.**
**Use this prompt to do it world-class.**

Command Revenue. Eliminate Chaos. Research Truth.

---

**Master Prompt Version**: 1.0.0
**Created**: November 13, 2025
**For**: Circuitos + General Use
**Source**: Mission Statement Skill Framework
**Quality Standard**: World-Class (9-10/10 on rubric)

---

## Appendix: Example Perplexity Output (World-Class)

```
═══════════════════════════════════════
RESEARCH BRIEF: VP SALES OPS PAIN POINTS
═══════════════════════════════════════

OBJECTIVE: Identify top pain points of VPs of Sales Operations in B2B companies ($10M-$100M revenue)

SOURCE: captureds.io (Primary), Gartner, G2 reviews (Supplementary)

DATE: November 13, 2025

CONFIDENCE: HIGH (N=327 VPs surveyed on captureds.io, Aug-Oct 2024)

---

KEY FINDINGS:

1. 🔥 CRM DATA ACCURACY (Mentioned by 73% of VPs)
   "Reps don't update Salesforce. I spend 2 hours/day chasing data."
   Source: captureds.io, "2024 Revenue Ops Survey", N=327

   Impact: High - Leads to forecast inaccuracy, deal slippage
   Current workaround: Manual Slack messages, weekly audits
   Competitor gap: No CRM solves this (UX problem, not feature)

   Our opportunity: AI-powered "truth detector" that flags stale data

2. DEAL RISK VISIBILITY (67% of VPs)
   "By the time I see a deal is at risk, it's too late to save it."
   Source: captureds.io + Gartner "Sales Ops Report 2024"

   Impact: Critical - Average deal loss: $127K per missed signal
   Current workaround: Weekly pipeline reviews, gut feel
   Competitor gap: Clari has this, but requires manual input

   Our opportunity: Real-time deal defibrillator with AI risk scoring

3. DASHBOARD OVERLOAD (61% of VPs)
   "I have 47 dashboards. None show me what I actually need."
   Source: captureds.io, "Dashboard Fatigue Study 2024"

   Impact: Medium - Time wasted, not revenue loss
   Current workaround: Excel, manual reports
   Competitor gap: Everyone builds more dashboards, not fewer

   🔥 Our opportunity: 4 weapons instead of 47 dashboards

[etc. - 10 pain points total]

---

DATA QUALITY:

Source credibility: 9/10 (captureds.io is specialized platform)
Recency: Excellent (Aug-Oct 2024, <6 months old)
Sample size: Strong (N=327 VPs, statistically significant)
Geographic: US-focused (85% US, 15% EU/APAC)
Limitations: Self-reported, may overstate pain

---

COMPETITIVE INTELLIGENCE:

Who's winning?
→ Clari (deal risk), Gong (conversation intel)
→ Why: Specialized, not general-purpose

Who's losing?
→ Salesforce, HubSpot (too complex, dashboard overload)
→ Why: Built for C-suite, not operators

White space:
→ "4 weapons, not 400 features" positioning
→ "Operator-first" (not executive-first) UX
→ "Truth in 90 seconds" (not 90-minute analysis)

---

RECOMMENDATIONS:

IMMEDIATE (0-30 days):
→ Update positioning: "Expose CRM lies in 90 seconds"
→ Homepage hero: Feature pain #1 (data accuracy)
→ Case study: Show before/after (47 dashboards → 4 weapons)

STRATEGIC (30-90 days):
→ Build: AI data quality checker (addresses pain #1)
→ Partner: Integrate with Clari (not compete on deal risk)
→ Content: "Why dashboards fail operators at 2am"

LONG-TERM (90+ days):
→ Expand: 4 weapons → 6 weapons (address pains #4-5)
→ Raise: $2M seed (VCs love "anti-dashboard" positioning)
→ Hire: VP Sales with operator background (not exec background)

---

OPEN QUESTIONS:

❓ What % of VPs have budget authority? (Need to research)
❓ How much do VPs pay for current tools? (Pricing research)
❓ Would "weapons" language resonate or confuse? (A/B test)

---

CONFIDENCE RATING: HIGH ✅

This research is ready to inform strategy decisions TODAY.

═══════════════════════════════════════
```

**That's world-class research. Use this standard for all Perplexity outputs.**

---

**END OF MASTER PROMPT**
