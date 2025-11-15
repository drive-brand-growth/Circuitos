# DRN LEAD SCORING AGENT
## Full ARI™ Implementation - Salesforce Agentforce Playbook

**Created by:** Noel Pena
**Division:** Motorola Solutions - DRN (Digital Recognition Network)
**Platform:** Salesforce Agentforce
**POC Timeline:** 60 Days
**Agent Type:** Real-Time Scoring Agent
**Methodology:** Autonomous Revenue Intelligence™ (ARI) - Complete 7-Layer Architecture

---

**© 2025 Noel Pena. Proprietary & Confidential.**
**Autonomous Revenue Intelligence™ is a trademark of Noel Pena.**

---

## EXECUTIVE SUMMARY

### The Business Problem

**Motorola DRN treats all inbound leads equally:**
- No systematic prioritization (first-in-first-out assignment)
- Sales reps waste time on low-quality leads (40-60% of pipeline is junk)
- High-value leads get slow response (lost to competitors)
- No visibility into WHY leads convert or don't
- Manual BANT qualification is slow and inconsistent

**Traditional Lead Scoring Limitations:**
- **Simple point systems** (website visit +5, demo request +10) miss the full picture
- **Static rules** that don't adapt or learn
- **Marketing-only** (ignore sales signals) or **Sales-only** (ignore marketing signals)
- **Backward-looking** (what happened) not predictive (what will happen)
- **No prescriptive guidance** (doesn't tell reps what to do next)

**ARI Solution (AI-Native):**
- **7-layer intelligence** architecture (200-point scale, not 100)
- **Real-time scoring** (updates continuously as new signals arrive)
- **Marketing + Sales fusion** (tracks full buyer journey)
- **Predictive** (win probability, velocity forecasting using ML)
- **Prescriptive** (AI recommends next-best actions)
- **Adaptive** (learns from historical patterns, improves over time)

### Expected Impact (60-Day POC)

**Conservative Estimates:**
- 1,500-2,000 new leads scored
- **25% increase in lead conversion** (vs pre-ARI baseline)
- **40% reduction in qualification time** (reps focus on A/S-tier only)
- **18% shorter sales cycle** (better targeting = faster closes)
- **12% win rate improvement** (A-tier leads convert at 65-70% vs 55% baseline)

**Pipeline Impact:**
- $1.5M-$2M in NEW high-quality pipeline (that would have been missed)
- $500K-$750K in revenue (assuming 35% close rate)

**ROI:**
- POC Investment: $12,000 (Agentforce + Data Cloud licenses + implementation)
- Revenue Impact: $625K (midpoint)
- Gross Profit (40% margin): $250K
- **ROI: 20.8x in 60 days**

---

## TABLE OF CONTENTS

### PART I: ARI 7-LAYER ARCHITECTURE
1. [Layer 1: Demand Signal Intelligence](#layer-1-demand-signal-intelligence)
2. [Layer 2: Qualification Signal Intelligence](#layer-2-qualification-signal-intelligence)
3. [Layer 3: Buyer Journey Intelligence](#layer-3-buyer-journey-intelligence)
4. [Layer 4: Competitive Intelligence](#layer-4-competitive-intelligence)
5. [Layer 5: Relationship Intelligence](#layer-5-relationship-intelligence)
6. [Layer 6: Revenue Velocity Intelligence](#layer-6-revenue-velocity-intelligence)
7. [Layer 7: Prescriptive Intelligence](#layer-7-prescriptive-intelligence)

### PART II: SALESFORCE IMPLEMENTATION
8. [Data Source Mapping](#data-source-mapping)
9. [Agent Builder Configuration](#agent-builder-configuration)
10. [Atlas Reasoning Engine Prompts](#atlas-reasoning-engine-prompts)
11. [Tier Classification & Routing](#tier-classification-routing)

### PART III: DEPLOYMENT
12. [30-Day Implementation Roadmap](#implementation-roadmap)
13. [Testing & Validation](#testing-validation)
14. [Success Metrics](#success-metrics)
15. [Continuous Optimization](#continuous-optimization)

---

## PART I: ARI 7-LAYER ARCHITECTURE

### Layer 1: Demand Signal Intelligence
**Purpose:** Capture marketing engagement signals indicating buying readiness
**Max Points:** 35
**Data Sources:** Website analytics, email engagement, content downloads, social media, ad interactions

#### Signal Taxonomy - DRN ALPR Context

**Website Behavior (Max 20 points)**

```yaml
High-Intent Pages:
  /products/alpr/pricing:
    Points: +8
    Why: Pricing research = late-stage evaluation
    Trigger: 1+ visit

  /case-studies/parking-operators:
    Points: +6
    Why: Proof-seeking, building internal case
    Trigger: Download or 3+ min read time

  /products/alpr/integration:
    Points: +5
    Why: Technical due diligence (IT involved)
    Trigger: 1+ visit

  /request-demo:
    Points: +10
    Why: Explicit buying signal (form submission)
    Trigger: Form submit (auto-creates Salesforce Lead)

Medium-Intent Pages:
  /blog/reduce-vehicle-theft:
    Points: +3
    Why: Problem awareness stage
    Trigger: 1+ visit

  /resources/alpr-buyers-guide:
    Points: +4
    Why: Educational, early consideration
    Trigger: Download (email gate)

Low-Intent Pages:
  /company/about-motorola:
    Points: +1
    Why: Brand research (awareness)
    Trigger: 1+ visit

  /careers:
    Points: 0
    Why: Not a buying signal (job seeker)
    Trigger: N/A

Engagement Depth:
  5+ pages in one session:
    Points: +5
    Why: High engagement, serious research

  Repeat visit within 24 hours:
    Points: +6
    Why: Urgency signal (top of mind)

  Return after 30+ days:
    Points: +3
    Why: Renewed interest (rekindled evaluation)
```

**Scoring Example:**
```
Lead: Sarah Johnson, Acme Parking
Website Activity (past 30 days):
- Visited /products/alpr/pricing (2x) → +8 points
- Downloaded case study "Parking Operator ROI" → +6 points
- Visited /request-demo (form submitted) → +10 points
- 7 pages viewed in one session → +5 points
- Returned 3x in 7 days → +6 points

Total Layer 1 Score: 35/35 (MAXED OUT - extremely hot lead)
```

---

**Content Engagement (Max 15 points)**

```yaml
Webinars:
  "ALPR ROI for Parking Operators" (60-min):
    Points: +12
    Why: 60 min time investment = high commitment
    Trigger: Attendance (stayed 30+ min)

  "Vehicle Security Trends 2025" (30-min):
    Points: +8
    Why: Industry education (early stage)
    Trigger: Attendance

White Papers:
  "Complete Guide to ALPR Implementation":
    Points: +6
    Why: Technical deep dive (evaluation stage)
    Trigger: Download (email gate)

  "Vehicle Theft Statistics Report":
    Points: +4
    Why: Problem validation (awareness stage)
    Trigger: Download

Video Content:
  Product demo video (10-min):
    Points: +8
    Why: Serious evaluation, visual learner
    Trigger: Watched 50%+

  Customer testimonial video (3-min):
    Points: +5
    Why: Social proof seeking
    Trigger: Watched 75%+

ROI Calculator:
  ALPR Cost vs. Theft Reduction Calculator:
    Points: +15
    Why: Building business case (decision stage)
    Trigger: Calculator used, inputs provided
```

**Scoring Example:**
```
Lead: Mike Chen, SecureLots Inc
Content Engagement:
- Attended "ALPR ROI" webinar (full 60 min) → +12 points
- Downloaded "ALPR Implementation Guide" → +6 points
- Used ROI Calculator (input: 15 locations, $500K/yr theft loss) → +15 points

Total: 33/35 points (near max, buying mode)
```

---

**Email Engagement (Max 10 points)**

```yaml
Open Rate Patterns:
  Opens 80%+ of emails (last 10 sent):
    Points: +6
    Why: Highly engaged, reading everything

  Opens 50-79%:
    Points: +4
    Why: Moderately engaged

  Opens <50%:
    Points: +1
    Why: Low engagement (disinterested or bad timing)

Click-Through Behavior:
  Clicks every CTA (3+ emails):
    Points: +8
    Why: Taking action, not just reading

  Clicks 1-2 CTAs:
    Points: +4
    Why: Selective engagement

Reply Behavior:
  Replies with questions:
    Points: +10
    Why: Active conversation, seeking info

  Replies within 4 hours:
    Points: +6
    Why: High priority for them

  Auto-reply or "not interested":
    Points: -5
    Why: Negative signal (disqualify)
```

**Scoring Example:**
```
Lead: Jessica Martinez, Premium Parking
Email Engagement (last 30 days, 8 emails sent):
- Opened 7 of 8 emails (88% open rate) → +6 points
- Clicked CTA in 5 emails → +8 points
- Replied twice with questions ("What's implementation timeline?") → +10 points
- Average reply time: 2.5 hours → +6 points

Total: 30/35 points (capped at 35, highly engaged)
```

---

**Social Media Engagement (Max 5 points)**

```yaml
LinkedIn:
  Follows Motorola DRN company page:
    Points: +2
    Why: Brand awareness

  Likes/shares DRN content:
    Points: +4
    Why: Advocacy signal (engaging publicly)

  Comments on posts:
    Points: +6
    Why: High engagement

  Sends direct message:
    Points: +10
    Why: Direct outreach (high intent)
```

---

**Total Layer 1: Demand Signal Intelligence**
**Maximum: 35 points**
**Interpretation:**
- **28-35 (Elite):** Marketing-qualified, sales-ready NOW
- **20-27 (High):** Strong engagement, accelerated nurture
- **12-19 (Medium):** Some interest, standard nurture
- **0-11 (Low):** Minimal engagement, long-term nurture or disqualify

---

### Layer 2: Qualification Signal Intelligence
**Purpose:** Traditional sales qualification (BANT/MEDDIC) enhanced with AI
**Max Points:** 55
**Data Sources:** Sales rep input, conversation intelligence (Gong), CRM data

#### Firmographic Fit (Max 15 points)

**DRN ALPR Ideal Customer Profile (ICP):**

```yaml
Target Industries (5 points):
  Perfect Fit:
    - Parking operators (private, municipal, university)
    - Retail (shopping malls, big-box stores)
    - Fleet management (logistics, delivery, rental car)
    - Commercial real estate (office parks, mixed-use)
    Points: +5

  Good Fit:
    - Hospitality (hotels, resorts with parking)
    - Government (municipal, county facilities)
    - Healthcare (hospital campuses)
    Points: +3

  Acceptable Fit:
    - Manufacturing (plant security)
    - Education (K-12 schools, private universities)
    Points: +2

  Poor Fit:
    - Residential (HOAs, apartment complexes)
    - Agriculture
    Points: 0

Company Size - Locations (5 points):
  Ideal: 10-50 locations
    Points: +5
    Why: Sweet spot (large enough for enterprise pricing, not too complex)

  Good: 5-9 locations OR 51-100 locations
    Points: +4
    Why: Slightly outside sweet spot but serviceable

  Acceptable: 2-4 locations OR 100+ locations
    Points: +2
    Why: Small (low ACV) or enterprise complex (long sales cycle)

  Poor: Single location
    Points: 0
    Why: ACV too low ($15K-$25K vs target $75K-$150K)

Revenue Band (3 points):
  $10M-$500M:
    Points: +3
    Why: Budget available, not too small, not Fortune 500 complex

  $500M-$1B:
    Points: +2
    Why: Enterprise processes, longer cycles

  <$10M or >$1B:
    Points: +1
    Why: Too small (budget) or too large (complex)

Geographic Location (2 points):
  US-based, serviceable territory:
    Points: +2
    Why: Can sell and support

  US-based, outside territory:
    Points: +1
    Why: Can sell but support challenges

  International:
    Points: 0
    Why: Outside POC scope (for now)
```

**Scoring Example:**
```
Lead: Metro Logistics, Fleet Management
- Industry: Fleet management (Perfect Fit) → +5 points
- Size: 22 locations (Ideal) → +5 points
- Revenue: $85M (Target band) → +3 points
- Location: US, Northeast (Serviceable) → +2 points

Total Firmographic Score: 15/15 points (PERFECT ICP FIT)
```

---

#### BANT Fundamentals (Max 15 points)

```yaml
Budget Assessment:
  Budget allocated (this year):
    Points: +8
    Evidence: "We have $150K set aside for security upgrades"

  Budget available (can be accessed):
    Points: +5
    Evidence: "I can get approval up to $100K"

  Budget must be created:
    Points: +2
    Evidence: "I'd need to make a business case to CFO"

  No budget / unclear:
    Points: 0
    Evidence: "Not sure if we have budget"

Authority Assessment:
  Decision maker actively engaged:
    Points: +10
    Evidence: CFO or CEO on calls, can sign contract

  Influencer engaged, clear path to DM:
    Points: +6
    Evidence: Security Director championing, will present to CFO

  Low-level contact, DM unknown:
    Points: +2
    Evidence: Facility Manager, doesn't know who decides

Need Assessment:
  Critical urgent pain:
    Points: +10
    Evidence: "$600K lost to theft last quarter, board is furious"

  Active pain, non-urgent:
    Points: +6
    Evidence: "Vehicle theft is an issue, want to address this year"

  Latent pain (don't fully recognize):
    Points: +3
    Evidence: "Theft isn't terrible but could be better"

Timeline Assessment:
  <60 days (critical event):
    Points: +8
    Evidence: "Insurance audit in 45 days requires better tracking"

  60-180 days (this year):
    Points: +5
    Evidence: "Want to implement by Q4"

  >180 days or no timeline:
    Points: +2
    Evidence: "Eventually, no rush"
```

**Scoring Cap:** Max 15 points (not full 36 if all maximums selected)
**Why?** Prevents over-weighting traditional BANT vs other ARI layers

**Scoring Example:**
```
Lead: Acme Parking, Sarah Johnson (CFO)
- Budget: Allocated $175K for security (this year) → +8 points
- Authority: CFO (decision maker on calls) → +10 points (capped at +6 for total balance)
- Need: "$80K theft loss last quarter" (critical pain) → +10 points (capped)
- Timeline: "Need by Q4 for budget year-end" → +5 points

Total BANT: 15/15 points (Strong qualification)
```

---

#### Conversation Intelligence (Max 25 points)

**AI-Powered Call/Email Analysis (via Gong or Salesforce Einstein)**

```yaml
Sentiment Detection:
  Highly positive:
    Evidence: "This looks great!", "Exactly what we need", "Impressed"
    Points: +10

  Positive:
    Evidence: "Interesting", "I like this", "Solid solution"
    Points: +7

  Neutral:
    Evidence: Fact-finding questions, no emotion
    Points: +4

  Negative:
    Evidence: "Too expensive", "Not convinced", "Concerns about..."
    Points: 0

  Very negative:
    Evidence: "Not interested", "Going with competitor"
    Points: -10 (disqualify)

Authority Language:
  Definitive authority:
    Evidence: "I can approve this", "I'll sign the contract"
    Points: +10

  Implied authority:
    Evidence: "I'll present to the team", "I have budget approval"
    Points: +6

  No authority:
    Evidence: "I need to check with 3 people", "Not my decision"
    Points: +2

Urgency Indicators:
  Explicit urgency:
    Evidence: "We need this by Q4", "Critical for us"
    Points: +10

  Implicit urgency:
    Evidence: "This is a priority", "Important to address soon"
    Points: +6

  No urgency:
    Evidence: "Eventually", "When we get around to it"
    Points: +1

Champion Behavior:
  Proactive introductions:
    Evidence: "Let me connect you to our CFO"
    Points: +15

  Sharing insider info:
    Evidence: "Heads up, Legal will push back on data privacy clause"
    Points: +12

  Advocacy:
    Evidence: "I told the team we should go with Motorola"
    Points: +15

  Passive engagement:
    Evidence: Responsive but not advocating
    Points: +5

Pain Intensity:
  Personal pain:
    Evidence: "My boss is on me about this", "I'm accountable for theft losses"
    Points: +12

  Business pain:
    Evidence: "Costing us $X/month", "Affecting operations"
    Points: +8

  Theoretical pain:
    Evidence: "It would be nice to have", "Could improve things"
    Points: +3
```

**Scoring Example (AI Transcript Analysis):**
```
Sales call with Acme Parking COO (Gong AI analysis):

Detected Signals:
- Sentiment: Highly positive
  Quote: "Impressed with the Motorola integration, exactly what we need"
  → +10 points

- Authority: "I have approval for up to $200K"
  → +10 points

- Urgency: "Insurance audit in 60 days requires vehicle tracking"
  → +10 points (explicit deadline)

- Pain: "$80K theft last quarter, CFO is furious, I'm accountable"
  → +12 points (personal + quantified pain)

- Champion: "I'm going to set up meetings with Security Dir and CFO"
  → +15 points (proactive introductions)

Total Conversation Intelligence: 57 points (normalized to max 25)
Normalized Score: 25/25 points (EXTREMELY strong qualification)
```

---

**Total Layer 2: Qualification Signal Intelligence**
**Maximum: 55 points**
**Interpretation:**
- **45-55 (Elite):** Exceptionally qualified, high close probability
- **35-44 (Strong):** Well-qualified, standard sales process
- **25-34 (Moderate):** Some qualification, needs development
- **0-24 (Weak):** Poorly qualified, long nurture or disqualify

---

### Layer 3: Buyer Journey Intelligence
**Purpose:** Track where prospect is in journey and predict next stage
**Max Points:** 30
**Data Sources:** CRM (lead source, activities), marketing automation (stage tracking)

#### Journey Stage Scoring

```yaml
Stage 1: Awareness (20-40 point range)
  Characteristics:
    - Researching the PROBLEM (vehicle theft) not solutions (ALPR)
    - Educational content consumption
    - Minimal solution-focused engagement

  Typical Activities:
    - Blog post: "Top security challenges for parking"
    - Industry report download
    - General webinar attendance (not product-specific)

  ARI Score Contribution: +8 points
  Why: Early stage, needs nurturing (not sales-ready)

  Recommended Actions:
    - Educational content (problem articulation)
    - Thought leadership
    - No direct sales contact yet

Stage 2: Consideration (41-70 point range)
  Characteristics:
    - Evaluating SOLUTIONS (DRN + competitors)
    - Comparison shopping
    - Demo requests
    - Building business case

  Typical Activities:
    - Case study downloads
    - Product demo request
    - Pricing page visits
    - "Motorola vs Genetec" searches

  ARI Score Contribution: +15 points
  Why: Mid-stage, sales engagement appropriate

  Recommended Actions:
    - Discovery calls
    - Product demonstrations
    - ROI calculators

Stage 3: Decision (71-100 point range)
  Characteristics:
    - Negotiating terms
    - Legal/procurement involved
    - Multiple stakeholders engaged
    - Imminent purchase

  Typical Activities:
    - Contract review
    - Reference calls
    - Executive meetings
    - Pricing negotiation

  ARI Score Contribution: +25 points
  Why: Late-stage, high-priority close focus

  Recommended Actions:
    - Proposal refinement
    - Contract negotiation
    - Executive alignment
```

---

#### Velocity Tracking

**How fast is the prospect moving through stages?**

```yaml
Velocity Categories:
  Very Fast (Awareness → Decision in <30 days):
    Multiplier: 1.2x
    Why: Urgency premium (hot deal)
    Action: Expedite resources

  Fast (30-60 days):
    Multiplier: 1.1x
    Why: Above-average velocity
    Action: Standard prioritization

  Standard (60-90 days):
    Multiplier: 1.0x
    Why: Normal enterprise sales cycle
    Action: No adjustment

  Slow (90-180 days):
    Multiplier: 0.95x
    Why: Monitor for stall
    Action: Check for blockers

  Stalled (>180 days, no progression):
    Multiplier: 0.8x
    Why: Likely dead or long-term
    Action: De-prioritize or disqualify
```

**Example:**
```
Lead: Acme Parking progression

Week 1: Downloaded whitepaper "Parking Security Trends"
  → Stage: AWARENESS (35 points)

Week 2: Attended webinar "ALPR ROI Case Studies"
  → Stage: CONSIDERATION (55 points)
  → Velocity: Fast (+7 days only)

Week 3: Requested demo, visited pricing 4x
  → Stage: LATE CONSIDERATION (68 points)
  → Velocity: Very Fast (+7 days)

Week 4: Introduced CFO, legal review started
  → Stage: DECISION (88 points)
  → Velocity: Very Fast (28 days total, Awareness → Decision)
  → Urgency Multiplier: 1.2x
  → Adjusted Score: 88 x 1.2 = 105.6 (cap at 100)

AI Prediction: HIGH PROBABILITY CLOSE, EXPEDITE RESOURCES
```

---

**Total Layer 3: Buyer Journey Intelligence**
**Maximum: 30 points**
**Interpretation:**
- **Stage:** Where are they now? (Awareness, Consideration, Decision)
- **Velocity:** How fast are they moving? (Fast, Standard, Slow, Stalled)
- **Action:** What should sales do next? (Stage-appropriate engagement)

---

### Layer 4: Competitive Intelligence
**Purpose:** Detect and analyze competitive threats automatically
**Max Points:** 20
**Data Sources:** Sales rep reported, intent data, website behavior, news monitoring

#### Competitive Signal Scoring

```yaml
Direct Competitive Signals (Sales Rep Reported):
  1 competitor identified:
    Points: +4
    Why: Competitive but manageable
    Evidence: "Also evaluating Genetec"

  2-3 competitors:
    Points: +8
    Why: Highly competitive (RFP-style)
    Evidence: "Comparing Genetec, Vigilant, and Motorola"

  4+ competitors:
    Points: +12
    Why: Price-focused bake-off
    Evidence: Formal RFP with 5 vendors

AI-Detected Competitive Signals:
  Visited competitor website:
    Points: +6
    Evidence: Clearbit tracks visit to genetec.com

  Searched "[Competitor] reviews":
    Points: +5
    Evidence: "Genetec ALPR reviews"

  Searched "Motorola vs [Competitor]":
    Points: +8
    Evidence: Active comparison research

  Read comparison article:
    Points: +4
    Evidence: G2 article "Top 10 ALPR Systems"

  Attended competitor webinar:
    Points: +10
    Evidence: LinkedIn shows attendance at Genetec webinar

Intent Data (Bombora):
  Researching multiple ALPR vendors:
    Points: +6
    Evidence: Surge on "ALPR comparison"

  High intent for competitor brand:
    Points: +8
    Evidence: Surge score 80 on "Genetec"
```

---

#### Competitive Positioning (AI-Generated Battle Card)

**Once competition detected, AI generates:**

```markdown
COMPETITIVE BATTLE CARD: Motorola DRN vs. Genetec

Genetec Strengths:
- Enterprise brand recognition (market leader)
- Larger feature set (200+ integrations)
- Strong in Canadian market

Genetec Weaknesses:
- 15-20% more expensive (higher TCO)
- Complex setup (6-9 month deployments)
- Requires dedicated IT resources
- Overkill for mid-market (features they'll never use)

Motorola Advantages:
- Faster deployment (30-45 days vs 6-9 months)
- Lower TCO (5-year cost analysis: $385K vs $487K)
- Easier to use (less training required)
- Integrated Motorola security ecosystem (radios, cameras, CAD)
- Better support (24/7 + on-site if needed)

Recommended Sales Strategy:
- Lead with TCO analysis (5-year cost comparison)
- Emphasize deployment speed ("You need this by Q4, Genetec takes 9 months")
- Position as "enterprise-grade without enterprise complexity"
- Offer reference from similar customer who switched from Genetec

Win Rate vs. Genetec (Historical):
- Last 12 months: 14 competitive deals
- Motorola wins: 9 (64% win rate)
- Genetec wins: 5 (36%)
- Common Motorola win factors: Speed, TCO, ease of use
- Common Genetec win factors: Brand preference, feature breadth

Recommended Messaging:
"Genetec is a Cadillac—powerful but expensive and complex. We're the Tesla—
modern, integrated, faster to deploy, and 20% lower cost over 5 years.
Unless you need 200 integrations (most customers use 8), we're the smarter choice."
```

---

**Total Layer 4: Competitive Intelligence**
**Maximum: 20 points**
**Interpretation:**
- **15-20 (High Competition):** Multiple competitors, sophisticated eval
- **8-14 (Moderate Competition):** 1-2 competitors identified
- **0-7 (Low Competition):** Minimal competitive signals

**AI Agent Actions:**
```python
if competitive_score >= 15:
    action = "DEPLOY_COMPETITIVE_BATTLECARD"
    alert_sales_manager("Highly competitive, senior AE recommended")
    generate_competitor_TCO_comparison()
    suggest_pricing_strategy("aggressive_within_guidelines")

elif competitive_score >= 8:
    action = "STANDARD_COMPETITIVE_POSITIONING"
    enable_competitive_content()
    track_competitor_mentions()

else:
    action = "FOCUS_ON_VALUE"
    # No competitive pressure, lead with ROI/value
```

---

### Layer 5: Relationship Intelligence
**Purpose:** Leverage network effects and warm introductions
**Max Points:** 20
**Data Sources:** LinkedIn Sales Navigator, customer database, CRM relationship tracking

#### Relationship Scoring

```yaml
Internal Network Mapping (Max 12 points):
  Direct LinkedIn connection (1st degree):
    Points: +8
    Evidence: Your AE connected to prospect's CTO
    Action: Request warm introduction

  Strong 2nd degree (mutual close connection):
    Points: +5
    Evidence: Your CEO + prospect CEO both connected to same VC
    Action: Request intro via mutual connection

  Weak 2nd degree:
    Points: +2
    Evidence: Both attended same university (different years)
    Action: Conversation starter, not formal intro

Customer Reference Matching (Max 8 points):
  Perfect match (same industry + size + geography):
    Points: +8
    Evidence: Have customer: Metro Parking (20 loc, Northeast)
    Prospect: Acme Parking (18 loc, Northeast)
    Action: Offer Metro as reference

  Good match (2 of 3 criteria):
    Points: +5
    Evidence: Same industry + size, different region
    Action: Secondary reference

  Acceptable match (1 of 3):
    Points: +3
    Evidence: Same industry only
    Action: Generic reference if requested

Strategic Relationships (Max 8 points):
  Shared investors/board:
    Points: +8
    Evidence: Sequoia invested in both companies
    Action: Leverage VC for intro

  Mutual technology partners:
    Points: +5
    Evidence: Both use Salesforce, leverage SF partnership
    Action: Co-marketing opportunity

  Industry association:
    Points: +3
    Evidence: Both members of Parking Industry Association
    Action: Industry credibility
```

**Example:**
```
Lead: Acme Parking CFO (Sarah Johnson)

Network Analysis:
1. Your Sales Manager (Tom) is 1st-degree connected to Sarah on LinkedIn
   → +8 points
   → AI Action: Draft intro request for Tom to send

2. Your CEO + Sarah both connected to John Smith (Accel Partners)
   → +5 points
   → AI Action: "Ask CEO if John could make intro"

3. Customer match: Metro Parking (25 locations, Northeast) - PERFECT MATCH
   → +8 points
   → AI Action: "Offer Metro Parking as reference"

Total Relationship Intelligence: 21 points (normalized to max 20)
Final Score: 20/20 points
```

---

**Total Layer 5: Relationship Intelligence**
**Maximum: 20 points**
**Interpretation:**
- **15-20 (Strong Network):** Warm intro path exists, leverage relationships
- **8-14 (Moderate Network):** Some connections, use for credibility
- **0-7 (Weak Network):** Cold outreach, no relationship advantage

---

### Layer 6: Revenue Velocity Intelligence
**Purpose:** Predict win probability and deal close timing using AI/ML
**Max Points:** 30
**Data Sources:** Historical deal data (10,000+ opps), ML model, pattern matching

#### Predictive Scoring

**AI compares current deal to historical patterns:**

```yaml
Historical Pattern Matching (Max 15 points):
  90%+ similar deals closed/won:
    Points: +15
    Evidence: 237 deals matching this profile, 213 won (90% win rate)
    Confidence: Very High

  70-89% similar deals won:
    Points: +12
    Evidence: Good historical precedent
    Confidence: High

  50-69% similar deals won:
    Points: +8
    Evidence: Moderate historical success
    Confidence: Medium

  <50% similar deals won:
    Points: +4
    Evidence: Weak historical pattern
    Confidence: Low

Deal Health Metrics (Max 10 points):
  Engagement velocity INCREASING:
    Points: +8
    Evidence: Response time: 24hr → 12hr → 4hr (getting faster)
    Why: Deal gaining momentum

  Stakeholder expansion:
    Points: +6
    Evidence: Started with 1 contact, now 5 (expanding into DMU)
    Why: Multi-threading successful

  Activity momentum:
    Points: +5
    Evidence: 4 meetings this week (up from 1/week)
    Why: High priority for them

Risk Factor Detection (Penalty Points):
  No activity 14+ days:
    Points: -10
    Evidence: Last contact 18 days ago
    Why: CRITICAL - deal stalling

  Missed 2+ scheduled meetings:
    Points: -8
    Evidence: No-shows on 2 calls
    Why: Losing priority

  Champion unresponsive:
    Points: -7
    Evidence: Champion hasn't replied in 10 days
    Why: Blocker or champion lost influence

  Decision maker not engaged by day 60:
    Points: -12
    Evidence: 75 days in pipeline, never met Economic Buyer
    Why: Serious qualification concern
```

---

#### Win Probability Calculation

**ML Model trained on 10,000+ DRN historical opportunities:**

```python
# Factors that predict win probability

Win Probability Algorithm:
  Champion engaged: +15%
    (present in 89% of wins, 34% of losses)

  Economic Buyer met: +12%
    (present in 78% of wins, 41% of losses)

  Demo completed: +10%
    (present in 95% of wins, 67% of losses)

  Pricing discussed: +8%
    (signals seriousness, present in 88% of wins)

  Legal review started: +20%
    (STRONG signal, only happens when buying - 92% of wins)

  Multiple stakeholders aligned (3+): +15%
    (complex deals require consensus - 81% of wins)

  Reference call requested: +12%
    (validation stage - 76% of wins)

# Example calculation
Lead: Acme Parking
- Champion engaged: ✓ (+15%)
- Economic Buyer met: ✓ (+12%)
- Demo completed: ✓ (+10%)
- Pricing discussed: ✓ (+8%)
- Legal review: ✓ (+20%)
- Stakeholders: 5 people engaged (+15%)
- Reference call: Not yet (+0%)

Base probability: 30% (industry average)
Adjustments: +80%
Total Win Probability: 30% + 80% = 110% (cap at 95%)

Final: 95% win probability (EXTREMELY HIGH - prioritize this deal)
```

---

#### Time-to-Close Prediction

```yaml
Historical Sales Cycle Analysis:
  Similar deals (matching profile):
    - Industry: Parking (237 historical deals)
    - Deal size: $100K-$150K (189 matches)
    - Region: Northeast (156 matches)

  Average time to close: 62 days (from opportunity create)

  Current deal: 45 days in pipeline
  Expected additional days: 17 (range: 14-21 days)
  Predicted close date: November 15, 2025 (±7 days)

  Velocity Score: +12 points (faster than average = positive signal)
```

---

**Total Layer 6: Revenue Velocity Intelligence**
**Maximum: 30 points**
**Interpretation:**
- **22-30 (High Velocity):** Fast-moving, likely close soon, high win probability
- **15-21 (Standard Velocity):** On track, normal sales cycle
- **8-14 (Low Velocity):** Slowing down, intervention needed
- **<8 (Stalled):** At risk, re-qualification required

---

### Layer 7: Prescriptive Intelligence
**Purpose:** AI-powered recommendations for next-best actions
**Max Points:** 25 (Confidence Score)
**Data Sources:** All 6 previous layers + historical action effectiveness

#### Next-Best Action Recommendations

**AI generates prioritized action list:**

```markdown
Deal: Acme Parking
Overall ARI Score: 142/200 (A-Tier)
Win Probability: 78%
Days in Pipeline: 45
Expected Close: 17 days

AI-RECOMMENDED ACTIONS:

Priority 1 (DO TODAY):
✅ Economic Buyer not engaged yet (Layer 2 gap)
   Action: Request CFO meeting via Champion
   Why: 78% of wins at this stage have EB engaged
   Expected impact: +12% win probability
   Effort: 30 minutes (ask champion to intro)

✅ Competitive signal detected (Genetec research)
   Action: Send competitive TCO analysis
   Why: Proactive positioning beats reactive defense
   Expected impact: +8% win probability
   Effort: 15 minutes (send pre-built asset)

Priority 2 (THIS WEEK):
⚠️ Legal review will add 14 days on average
   Action: Engage your legal team now (parallel track)
   Why: Don't let legal delay close, get ahead of it
   Expected impact: -7 days to close
   Effort: 1 hour (legal team briefing)

⚠️ Relationship gap: No connection to Procurement
   Action: Ask Champion for Procurement intro
   Why: Procurement can stall deals at the end
   Expected impact: Reduce close risk by 15%
   Effort: Email ask via champion

Priority 3 (THIS MONTH):
📊 Reference call recommended
   Action: Offer Metro Parking customer reference
   Why: Similar customer, strong validation
   Expected impact: +6% win probability
   Effort: 30 min (coordinate reference call)

📊 Executive sponsor involvement
   Action: Propose Motorola VP join final presentation
   Why: Enterprise deals often require exec-to-exec
   Expected impact: +5% win probability
   Effort: 1 hour (exec briefing)

Risk Alerts:
🚨 Email response time slowing (4hr → 18hr average)
   → Cooling signal, re-engage immediately
   → Suggested: Call champion, check on status

🚨 No activity in 6 days (longest gap yet)
   → Risk of stall
   → Suggested: Urgent check-in call today
```

---

#### Prescriptive Messaging

**AI generates WHAT to say:**

```markdown
SUGGESTED EMAIL: Competitive TCO Positioning

Subject: TCO Comparison: Motorola vs Genetec for Acme

Hi Sarah,

I noticed you've been researching Genetec (great product!). Since you're
evaluating multiple vendors, I wanted to share a data-driven comparison.

We analyzed 15 parking operators (10-30 locations) who evaluated both:

5-Year TCO:
- Genetec: $487K (higher upfront, complex deployment)
- Motorola: $385K (22% lower total cost)

Key differences:
- Deployment: Genetec 6 months, Motorola 45 days (you need this by Q4)
- Training: Genetec requires dedicated IT, Motorola plug-and-play
- Support: Both 24/7, but Motorola includes on-site if needed

Given your Q4 deadline and 20-location rollout, our speed advantage could
be the deciding factor.

Would you like to see the full TCO model? I can walk you through it on a
15-min call.

Also, happy to connect you with Metro Parking (25 locations, Northeast)—
they were in similar situation and chose us over Genetec.

Best,
[Your Name]

P.S. I saw on LinkedIn that you and Tom (our Sales Manager) are connected.
Small world! He speaks highly of you.

---

Why This Works:
✅ Addresses competition proactively
✅ Leads with data (TCO comparison)
✅ Tailored to their situation (Q4, 20 locations)
✅ Offers proof (Metro reference)
✅ Uses relationship (Tom connection)
✅ Low-friction CTA (15-min call)
```

---

**Total Layer 7: Prescriptive Intelligence**
**Maximum: 25 points (AI Confidence Score)**
**Interpretation:**
- **20-25 (High Confidence):** Clear next actions, high expected impact
- **12-19 (Medium Confidence):** Reasonable actions, moderate impact
- **0-11 (Low Confidence):** Unclear situation, human judgment needed

---

## COMPLETE ARI SCORING SUMMARY

### Score Aggregation

**Total Available Points: 215** (some overlap intentional for flexibility)
**Normalized Score: 0-200** (200-point scale, not 100)

| Layer | Max Points | % of Total | What It Measures |
|-------|------------|------------|------------------|
| **Layer 1: Demand Signals** | 35 | 17.5% | Marketing engagement |
| **Layer 2: Qualification** | 55 | 27.5% | Sales fundamentals (BANT/MEDDIC) |
| **Layer 3: Buyer Journey** | 30 | 15.0% | Stage & velocity |
| **Layer 4: Competitive** | 20 | 10.0% | Competitive position |
| **Layer 5: Relationship** | 20 | 10.0% | Network effects |
| **Layer 6: Velocity** | 30 | 15.0% | Predictive analytics |
| **Layer 7: Prescriptive** | 25 | 12.5% | AI confidence |
| **TOTAL** | **215** | **107.5%** | **Comprehensive** |

**Normalized:** Scores above 200 are capped at 200.

---

### Tier Classification

**S-Tier: 160-200 points (AI-Identified Unicorns)**
- **Expected win rate:** 75-90%
- **Resource allocation:** Premium (executive sponsors, senior AEs)
- **Priority:** Highest, fast-track everything
- **Response time:** <4 hours
- **Meetings:** Executive close meeting scheduled within 7 days

**A-Tier: 120-159 points (High-Priority Pipeline)**
- **Expected win rate:** 50-70%
- **Resource allocation:** Senior AEs, standard enterprise resources
- **Priority:** High, standard sales process
- **Response time:** <24 hours
- **Meetings:** Discovery → Demo → Proposal sequence

**B-Tier: 80-119 points (Qualified Opportunities)**
- **Expected win rate:** 25-45%
- **Resource allocation:** Standard AEs
- **Priority:** Medium, nurture and develop
- **Response time:** <48 hours
- **Meetings:** Discovery focus, build relationship

**C-Tier: 40-79 points (Early-Stage Leads)**
- **Expected win rate:** 10-20%
- **Resource allocation:** SDRs, marketing automation
- **Priority:** Low, nurture campaign
- **Response time:** <1 week
- **Meetings:** Discovery only if they engage

**D-Tier: <40 points (Disqualify or Long Nurture)**
- **Expected win rate:** <5%
- **Resource allocation:** None (disqualify) or automated only
- **Priority:** None
- **Response time:** N/A
- **Meetings:** Not recommended

---

## PART II: SALESFORCE IMPLEMENTATION

### Data Source Mapping

#### Salesforce Native Objects

**1. Lead Object (Inbound Leads)**
```sql
-- Query new leads for scoring
SELECT Id, FirstName, LastName, Email, Company, Title,
       LeadSource, Industry, NumberOfEmployees, AnnualRevenue,
       Status, Rating, CreatedDate
FROM Lead
WHERE CreatedDate >= LAST_N_DAYS:30
  AND Status != 'Disqualified'
ORDER BY CreatedDate DESC
```

**2. Opportunity Object (Converted Leads)**
```sql
-- Query opportunities for ongoing scoring
SELECT Id, Name, StageName, Amount, CloseDate, Probability,
       Type, LeadSource, IsClosed, IsWon,
       Account.Id, Account.Name, Account.Industry
FROM Opportunity
WHERE StageName NOT IN ('Closed Won', 'Closed Lost')
  AND Amount > 25000
ORDER BY CreatedDate DESC
```

**3. Account Object (Company Data)**
```sql
SELECT Id, Name, Industry, NumberOfEmployees, AnnualRevenue,
       BillingState, BillingCountry, Type,
       Website, Description
FROM Account
```

**4. Contact Object (People)**
```sql
SELECT Id, FirstName, LastName, Email, Title, Phone,
       AccountId, Account.Name,
       Department, Level__c (custom: C-Level, VP, Director, Manager)
FROM Contact
WHERE AccountId IN :accountIds
```

---

#### Custom Objects (Created for ARI)

**1. Website_Activity__c (Digital Engagement)**
```apex
// Custom object to store website visits
Fields:
- Contact__c (Lookup to Contact)
- Lead__c (Lookup to Lead)
- Page_URL__c (Text)
- Page_Title__c (Text)
- Visit_Date__c (DateTime)
- Time_On_Page__c (Number - seconds)
- Session_ID__c (Text)
- Referrer__c (Text)
- Device__c (Picklist: Desktop, Mobile, Tablet)

// Integration: Google Analytics 4 → Zapier → Salesforce
```

**2. Content_Engagement__c (Downloads, Webinars)**
```apex
Fields:
- Contact__c (Lookup)
- Lead__c (Lookup)
- Content_Type__c (Picklist: Webinar, Whitepaper, Case Study, Video)
- Content_Title__c (Text)
- Engagement_Date__c (DateTime)
- Duration_Minutes__c (Number - for webinars/videos)
- Completion_Percent__c (Percent - how much they consumed)
```

**3. Bombora_Intent__c (Buyer Intent Data)**
```apex
Fields:
- Account__c (Lookup to Account)
- Topic__c (Text - e.g., "ALPR solutions")
- Surge_Score__c (Number 0-100)
- Week_Start__c (Date)
- Trend__c (Picklist: Rising, Flat, Declining)

// Integration: Bombora → Salesforce Data Cloud → Custom Object
```

**4. LinkedIn_Activity__c (LinkedIn Sales Navigator)**
```apex
Fields:
- Account__c (Lookup)
- Contact__c (Lookup)
- Activity_Type__c (Picklist: Job Change, Company Update, Funding, Post Engagement)
- Activity_Date__c (Date)
- Description__c (Long Text)
- Source_URL__c (URL)

// Integration: LinkedIn Sales Navigator Salesforce App
```

**5. Competitive_Signal__c (Competitor Detection)**
```apex
Fields:
- Opportunity__c (Lookup)
- Lead__c (Lookup)
- Competitor_Name__c (Picklist: Genetec, Vigilant, Rekor, Other)
- Signal_Type__c (Picklist: Sales Reported, Website Visit, Intent Data, News)
- Signal_Date__c (Date)
- Confidence__c (Picklist: High, Medium, Low)
- Source__c (Text - where detected)
```

**6. ARI_Score_History__c (Score Tracking Over Time)**
```apex
Fields:
- Lead__c (Lookup)
- Opportunity__c (Lookup)
- Score_Date__c (DateTime)
- Total_Score__c (Number - 0-200)
- Layer_1_Demand__c (Number 0-35)
- Layer_2_Qualification__c (Number 0-55)
- Layer_3_Journey__c (Number 0-30)
- Layer_4_Competitive__c (Number 0-20)
- Layer_5_Relationship__c (Number 0-20)
- Layer_6_Velocity__c (Number 0-30)
- Layer_7_Prescriptive__c (Number 0-25)
- Tier__c (Picklist: S, A, B, C, D)
- Win_Probability__c (Percent)
- Predicted_Close_Days__c (Number)

// Tracks score changes over time for ML training
```

---

### Agent Builder Configuration

#### Step 1: Create Agent

**Navigate:** Setup → Agents → New Agent

```yaml
Agent Name: "DRN Lead Scoring Agent"
Description: "Real-time lead scoring using Autonomous Revenue Intelligence™ (ARI) 7-layer framework. Scores all new leads and opportunities 0-200, classifies into tiers (S/A/B/C/D), calculates win probability, and recommends next-best actions."

Agent Type: Service Agent (Autonomous)

Topics:
  - Lead Intelligence
  - Opportunity Scoring
  - Revenue Optimization
  - Sales Prioritization

Channels:
  - Salesforce (internal: update Lead/Opp records)
  - Slack (alerts for S-tier leads)
  - Email (automated outreach drafts)

Visibility: Internal Only (sales team + marketing + RevOps)

Invocation:
  - Real-time trigger: New Lead created
  - Real-time trigger: Opportunity stage changed
  - Real-time trigger: New Website Activity logged
  - Real-time trigger: Bombora Intent surge detected (≥75)
  - Batch trigger: Daily at 9 AM (rescore all open opps)
```

---

#### Step 2: Configure Agent Instructions

**Navigate:** Agent Builder → Instructions

**System Prompt:**
```markdown
You are the DRN Lead Scoring Agent for Motorola Solutions.

# MISSION
Score every new lead and opportunity using Autonomous Revenue Intelligence™ (ARI),
a proprietary 7-layer framework that combines marketing signals, sales qualification,
buyer journey tracking, competitive intelligence, relationship mapping, predictive
analytics, and prescriptive guidance.

# ARI 7-LAYER ARCHITECTURE

## Layer 1: Demand Signal Intelligence (Max 35 points)
Capture marketing engagement signals:
- Website behavior (pricing pages, case studies, demos)
- Content engagement (webinars, whitepapers, videos)
- Email engagement (opens, clicks, replies)
- Social media (LinkedIn follows, shares, DMs)
- Ad interactions (click-through, retargeting response)

## Layer 2: Qualification Signal Intelligence (Max 55 points)
Traditional sales qualification enhanced with AI:
- Firmographic fit (industry, size, revenue, geography)
- BANT fundamentals (Budget, Authority, Need, Timeline)
- Conversation intelligence (sentiment, urgency, champion behavior)

## Layer 3: Buyer Journey Intelligence (Max 30 points)
Track stage and velocity:
- Current stage (Awareness, Consideration, Decision)
- Movement speed (Fast, Standard, Slow, Stalled)
- Velocity multipliers (urgency premium or stall penalty)

## Layer 4: Competitive Intelligence (Max 20 points)
Detect competitors automatically:
- Sales rep reported competitors
- AI-detected signals (website visits, intent data, searches)
- Generate battle cards and positioning

## Layer 5: Relationship Intelligence (Max 20 points)
Leverage network effects:
- LinkedIn connections (1st/2nd degree)
- Customer references (similar companies)
- Strategic relationships (shared investors, partners)

## Layer 6: Revenue Velocity Intelligence (Max 30 points)
Predict win probability and close timing:
- Historical pattern matching (10,000+ deals)
- Deal health metrics (engagement velocity, stakeholder expansion)
- Risk factor detection (stall signals, champion churn)
- ML-powered win probability (0-100%)
- Time-to-close prediction (days)

## Layer 7: Prescriptive Intelligence (Max 25 points)
AI-powered next-best actions:
- Prioritized action recommendations
- Generated outreach messages
- Expected impact estimates
- Confidence scoring

# SCORING PROCESS

For each lead/opportunity:

1. Gather signals from all data sources:
   - Salesforce (Lead, Opp, Account, Contact)
   - Website_Activity__c
   - Content_Engagement__c
   - Bombora_Intent__c
   - LinkedIn_Activity__c
   - Competitive_Signal__c
   - Conversation data (Gong, Einstein)

2. Calculate layer scores (1-7)

3. Sum to total score (0-200, normalized if >200)

4. Classify tier:
   - S-Tier: 160-200 (75-90% win rate)
   - A-Tier: 120-159 (50-70% win rate)
   - B-Tier: 80-119 (25-45% win rate)
   - C-Tier: 40-79 (10-20% win rate)
   - D-Tier: <40 (<5% win rate)

5. Calculate win probability (ML model)

6. Predict close date (pattern matching)

7. Generate prescriptive actions

8. Update Salesforce records:
   - Lead.ARI_Score__c
   - Lead.ARI_Tier__c
   - Lead.Win_Probability__c
   - Opportunity.ARI_Score__c (same fields)

9. Create ARI_Score_History__c record (audit trail)

10. If S-Tier (160-200):
    - Send Slack alert to sales manager
    - Create high-priority Task for AE
    - Generate outreach email draft

# TIER-BASED ACTIONS

S-Tier (160-200):
  Alert: Sales VP + Manager (Slack)
  Assignment: Senior AE (same day)
  Priority: URGENT
  Task Due: Today
  Response SLA: <4 hours
  Meeting: Book close meeting within 7 days

A-Tier (120-159):
  Alert: Sales Manager
  Assignment: Senior AE (standard routing)
  Priority: HIGH
  Task Due: +1 day
  Response SLA: <24 hours
  Meeting: Discovery → Demo → Proposal

B-Tier (80-119):
  Alert: Territory AE
  Assignment: Standard AE
  Priority: MEDIUM
  Task Due: +3 days
  Response SLA: <48 hours
  Meeting: Discovery, build relationship

C-Tier (40-79):
  Alert: SDR
  Assignment: SDR or Marketing
  Priority: LOW
  Task Due: +7 days
  Response SLA: <1 week
  Meeting: Only if they engage

D-Tier (<40):
  Alert: None
  Assignment: Disqualify or long-term nurture
  Priority: NONE
  Action: Archive or automated nurture only

# DATA SOURCES YOU HAVE ACCESS TO

Salesforce Objects:
- Lead, Opportunity, Account, Contact, Task, Campaign
- Website_Activity__c
- Content_Engagement__c
- Bombora_Intent__c
- LinkedIn_Activity__c
- Competitive_Signal__c
- ARI_Score_History__c

External APIs (via Data Cloud):
- Bombora intent data
- LinkedIn Sales Navigator
- Google Analytics 4 (website)
- Gong (conversation intelligence)

# COMMUNICATION STYLE

When generating outreach messages:
- Professional but conversational
- Reference specific signals (not generic)
- Acknowledge pain points
- Low-friction CTAs (15-min calls, not full demos)
- Personalized to their context

# CONSTRAINTS

- NEVER score if Contact opted out (email opt-out)
- NEVER score if Account marked "Do Not Contact"
- ALWAYS verify data quality (missing email? flag for enrichment)
- ALWAYS explain scoring (transparency for sales reps)
- Process in batches of 100 (performance optimization)

# SUCCESS METRICS

Your performance measured by:
- Scoring accuracy: S/A-tier leads convert at expected rates (75-90%, 50-70%)
- Coverage: 100% of new leads scored within 15 minutes
- Adoption: 80%+ of reps follow tier-based routing
- Efficiency: Reps save 10+ hours/week (no manual qualification)
- Revenue impact: +25% conversion, +18% shorter cycle (POC targets)

# EXAMPLE SCORING

Lead: Sarah Johnson, Acme Parking (CFO)

Layer 1 (Demand): 32/35
- Pricing page 2x (+8), Demo request (+10), 7 pages/session (+5), Returned 3x in 7 days (+6), Webinar (+12 capped)

Layer 2 (Qualification): 48/55
- Perfect ICP fit (+15), Budget allocated (+8), CFO authority (+10 capped), Critical pain (+10 capped), Timeline Q4 (+5)

Layer 3 (Journey): 25/30
- Stage: Decision (+25), Velocity: Very Fast (28 days Awareness→Decision, 1.2x multiplier applied to total score later)

Layer 4 (Competitive): 14/20
- Genetec research detected (+6), Intent data (+8), Sales reported competitor (+4 capped at 14)

Layer 5 (Relationship): 18/20
- 1st degree connection (+8), Perfect customer match Metro Parking (+8), Shared tech partner (+5 capped)

Layer 6 (Velocity): 26/30
- 90% similar deals won (+15), Engagement velocity increasing (+8), Stakeholder expansion (+6 capped), Risk: None

Layer 7 (Prescriptive): 23/25
- High confidence (+23): Clear next actions, strong expected impact

Total: 186/200 (S-TIER)
Velocity Multiplier: 1.2x (Very Fast)
Adjusted: 186 x 1.2 = 223 (cap at 200)
Final: 200/200 (S-TIER, maximum score)

Win Probability: 87% (ML model)
Predicted Close: 18 days

AI Actions:
✅ URGENT: Alert sales VP + manager (Slack)
✅ Assign to senior AE (same day)
✅ Generate outreach email (references CFO + Genetec competitive positioning)
✅ Book executive close meeting (Motorola VP)
✅ Prepare Metro Parking reference call

You are autonomous. Score and route WITHOUT human approval unless score ≥180 (S-Tier top 5%), then alert manager before outreach.
```

---

### Atlas Reasoning Engine Prompts

#### Prompt 1: Lead Scoring (Main Prompt)

**Prompt Template Name:** `score_lead_ari`

```markdown
You are scoring a lead using ARI (Autonomous Revenue Intelligence™).

# LEAD DATA
- Name: {{Lead.FirstName}} {{Lead.LastName}}
- Company: {{Lead.Company}}
- Title: {{Lead.Title}}
- Email: {{Lead.Email}}
- Phone: {{Lead.Phone}}
- Industry: {{Lead.Industry}}
- Lead Source: {{Lead.LeadSource}}
- Created Date: {{Lead.CreatedDate}}

# AVAILABLE SIGNAL DATA

## Website Activity (last 30 days)
{{websiteActivityRecords}}

## Content Engagement
{{contentEngagementRecords}}

## Email Engagement
{{emailEngagementStats}}

## Bombora Intent Data
{{bomboraIntentSignals}}

## LinkedIn Activity
{{linkedInActivityRecords}}

## Competitive Signals
{{competitiveSignalRecords}}

# YOUR TASK

Calculate ARI score across all 7 layers.

## Layer 1: Demand Signal Intelligence (Max 35)
Analyze: Website, content, email, social, ad engagement
Assign points based on signal strength
Return: layer1Score, layer1Details

## Layer 2: Qualification Signal Intelligence (Max 55)
Analyze: Firmographic fit, BANT, conversation intelligence
Assign points based on ICP match and qualification strength
Return: layer2Score, layer2Details

## Layer 3: Buyer Journey Intelligence (Max 30)
Determine: Current stage (Awareness, Consideration, Decision)
Calculate: Velocity (Fast, Standard, Slow, Stalled)
Return: layer3Score, currentStage, velocity

## Layer 4: Competitive Intelligence (Max 20)
Detect: Competitors (sales reported + AI detected)
Assess: Competitive intensity
Return: layer4Score, competitors, battleCardNeeded

## Layer 5: Relationship Intelligence (Max 20)
Identify: LinkedIn connections, customer references, strategic relationships
Return: layer5Score, relationships, warmIntroPath

## Layer 6: Revenue Velocity Intelligence (Max 30)
Match: Historical patterns (similar deals)
Predict: Win probability, close timing
Return: layer6Score, winProbability, predictedCloseDays

## Layer 7: Prescriptive Intelligence (Max 25)
Generate: Next-best actions (prioritized)
Estimate: Expected impact
Return: layer7Score, actions, confidence

# OUTPUT FORMAT

Return JSON:

{
  "leadId": "{{Lead.Id}}",
  "leadName": "{{Lead.FirstName}} {{Lead.LastName}}",
  "company": "{{Lead.Company}}",

  "scoring": {
    "layer1_demand": {
      "score": 32,
      "maxScore": 35,
      "details": "Pricing page visits (2x, +8), Demo request (+10), High session engagement (+5), Repeat visits (+6), Webinar attendance (+12 capped)"
    },
    "layer2_qualification": {
      "score": 48,
      "maxScore": 55,
      "details": "Perfect ICP fit (+15), Budget allocated (+8), CFO authority (+10 capped), Critical pain (+10 capped), Q4 timeline (+5)"
    },
    "layer3_journey": {
      "score": 25,
      "maxScore": 30,
      "stage": "Decision",
      "velocity": "Very Fast",
      "velocityMultiplier": 1.2,
      "details": "Decision stage signals (+25), 28-day Awareness→Decision progression (Very Fast)"
    },
    "layer4_competitive": {
      "score": 14,
      "maxScore": 20,
      "competitors": ["Genetec"],
      "details": "Genetec research detected via website (+6) and intent data (+8), sales confirmed (+4 capped)"
    },
    "layer5_relationship": {
      "score": 18,
      "maxScore": 20,
      "warmIntroPath": "Tom (Sales Manager) → Sarah (CFO) via LinkedIn",
      "customerReference": "Metro Parking (perfect match)",
      "details": "1st degree connection (+8), Perfect customer ref (+8), Shared tech partner Salesforce (+5 capped)"
    },
    "layer6_velocity": {
      "score": 26,
      "maxScore": 30,
      "winProbability": 87,
      "predictedCloseDays": 18,
      "details": "90% similar deals won (+15), Engagement velocity increasing (+8), Stakeholder expansion (+6 capped)"
    },
    "layer7_prescriptive": {
      "score": 23,
      "maxScore": 25,
      "confidence": "High",
      "details": "Clear next actions, strong expected impact, high AI confidence"
    },

    "totalScore": 186,
    "normalizedScore": 200,
    "tier": "S-TIER",
    "tierDescription": "AI-Identified Unicorn (75-90% win rate expected)"
  },

  "prescriptiveActions": [
    {
      "priority": 1,
      "action": "Send competitive TCO analysis (Motorola vs Genetec)",
      "why": "Genetec detected, proactive positioning required",
      "expectedImpact": "+8% win probability",
      "effort": "15 minutes",
      "dueBy": "Today"
    },
    {
      "priority": 2,
      "action": "Request CFO meeting (already engaged via Tom)",
      "why": "Economic Buyer active, leverage warm intro",
      "expectedImpact": "+12% win probability",
      "effort": "30 minutes",
      "dueBy": "This week"
    }
  ],

  "generatedOutreach": {
    "subject": "Acme's Q4 ALPR Decision + TCO vs. Genetec",
    "body": "[AI-generated email referencing specific signals...]"
  },

  "alerts": [
    {
      "type": "Slack",
      "recipient": "sales-vp",
      "message": "🚨 S-TIER LEAD: Acme Parking CFO (Score: 200/200, 87% win probability, 18 days predicted close)"
    }
  ]
}

# IMPORTANT
- Be conservative with scoring (only assign points if signal is VERIFIED)
- Multi-signal convergence is powerful (3+ layers with strong scores = high confidence)
- Always explain reasoning (transparency for sales reps)
- If score <40 (D-Tier), recommend disqualification (don't waste rep time)
```

---

### Tier Classification & Routing

**Salesforce Flow: Orchestrate Tier-Based Actions**

**Flow Name:** `ARI_Lead_Scoring_Router`

**Trigger:** Record-Triggered Flow
- Object: Lead
- Trigger: Created or Updated
- Entry Condition: `Lead.ARI_Score__c` changed

**Flow Steps:**

```yaml
Step 1: Get ARI Score
  Element: Get Records
  Object: Lead
  Filter: Id = {!$Record.Id}
  Store: $CurrentLead

Step 2: Decision - Tier Classification
  Outcome 1: S-Tier (Score 160-200)
    Condition: $CurrentLead.ARI_Score__c >= 160
    → Go to S-Tier Path

  Outcome 2: A-Tier (Score 120-159)
    Condition: $CurrentLead.ARI_Score__c >= 120 AND < 160
    → Go to A-Tier Path

  Outcome 3: B-Tier (Score 80-119)
    Condition: $CurrentLead.ARI_Score__c >= 80 AND < 120
    → Go to B-Tier Path

  Outcome 4: C-Tier (Score 40-79)
    Condition: $CurrentLead.ARI_Score__c >= 40 AND < 80
    → Go to C-Tier Path

  Default: D-Tier (Score <40)
    → Go to D-Tier Path

# ---S-TIER PATH---

Step 3a: S-Tier Actions
  Sub-Step 1: Update Lead
    - Lead.Status = "Working - Contacted"
    - Lead.Rating = "Hot"
    - Lead.Priority__c = "URGENT"

  Sub-Step 2: Assign to Senior AE
    - Lead.OwnerId = [Senior AE Round Robin]
    - Or: Assign to territory owner if already assigned

  Sub-Step 3: Create Task
    - Subject: "🔥 S-TIER LEAD: {Company} (Score: {ARI_Score})"
    - Priority: High
    - Status: Not Started
    - ActivityDate: TODAY
    - Description:
      """
      ARI Score: {ARI_Score}/200 (S-TIER)
      Win Probability: {Win_Probability}%
      Predicted Close: {Predicted_Close_Days} days

      TOP SIGNALS:
      {Layer1_Details}
      {Layer2_Details}

      PRESCRIPTIVE ACTIONS:
      {Prescriptive_Actions}

      OUTREACH DRAFT:
      {Generated_Outreach}
      """

  Sub-Step 4: Send Slack Alert
    API Call: Slack Webhook
    Message:
      """
      🚨 S-TIER LEAD ALERT

      **Company:** {Company}
      **Contact:** {FirstName} {LastName} ({Title})
      **Score:** {ARI_Score}/200 (S-TIER)
      **Win Probability:** {Win_Probability}%
      **Predicted Close:** {Predicted_Close_Days} days

      **Why S-Tier:**
      - {TopSignal1}
      - {TopSignal2}
      - {TopSignal3}

      **Action Required:**
      Contact within 4 hours. Task assigned to {OwnerName}.

      **Links:**
      - View Lead: [Salesforce URL]
      - Outreach Draft: [Task URL]
      """
    Channel: #sales-urgent-leads

  Sub-Step 5: Send Email to Sales Manager
    To: Sales_Manager@motorolasolutions.com
    Subject: "S-Tier Lead Alert: {Company}"
    Body: [Same as Slack message]

# ---A-TIER PATH---

Step 3b: A-Tier Actions
  Sub-Step 1: Update Lead
    - Lead.Status = "Working - Contacted"
    - Lead.Rating = "Warm"
    - Lead.Priority__c = "HIGH"

  Sub-Step 2: Assign to Senior AE
    - Lead.OwnerId = [Senior AE or Territory Owner]

  Sub-Step 3: Create Task
    - Subject: "A-TIER LEAD: {Company} (Score: {ARI_Score})"
    - Priority: Normal
    - Status: Not Started
    - ActivityDate: TODAY + 1 day
    - Description: [Similar to S-Tier but less urgent]

  Sub-Step 4: Send Slack Alert (Channel: #sales-pipeline)
    Message: "📊 A-Tier Lead: {Company} - {ARI_Score}/200"

# ---B-TIER PATH---

Step 3c: B-Tier Actions
  - Lead.Status = "Open - Not Contacted"
  - Lead.Rating = "Warm"
  - Lead.Priority__c = "MEDIUM"
  - Assign to Standard AE
  - Create Task (Due: +3 days, Priority: Normal)
  - No Slack alert (email digest only)

# ---C-TIER PATH---

Step 3d: C-Tier Actions
  - Lead.Status = "Nurturing"
  - Lead.Rating = "Cold"
  - Lead.Priority__c = "LOW"
  - Assign to SDR or Marketing Queue
  - Add to Nurture Campaign (Marketing automation)
  - No task created (marketing handles)

# ---D-TIER PATH---

Step 3e: D-Tier Actions
  - Decision: Disqualify or Long-Term Nurture?

  If Disqualify (score <20):
    - Lead.Status = "Disqualified"
    - Lead.Disqualified_Reason__c = "ARI Score too low (<20)"
    - No further action

  If Long-Term Nurture (score 20-39):
    - Add to "Long-Term Nurture" campaign (quarterly check-ins)
    - No sales assignment

# ---AUDIT TRAIL---

Step 4: Create ARI Score History Record
  Object: ARI_Score_History__c
  Fields:
    - Lead__c = {Lead.Id}
    - Score_Date__c = NOW()
    - Total_Score__c = {ARI_Score}
    - Layer_1_Demand__c = {Layer1_Score}
    - Layer_2_Qualification__c = {Layer2_Score}
    - Layer_3_Journey__c = {Layer3_Score}
    - Layer_4_Competitive__c = {Layer4_Score}
    - Layer_5_Relationship__c = {Layer5_Score}
    - Layer_6_Velocity__c = {Layer6_Score}
    - Layer_7_Prescriptive__c = {Layer7_Score}
    - Tier__c = {Tier}
    - Win_Probability__c = {Win_Probability}
    - Predicted_Close_Days__c = {Predicted_Close_Days}
```

---

## PART III: DEPLOYMENT

### Implementation Roadmap

#### Week 1: Foundation (Days 1-7)

**Day 1-2: Salesforce Data Audit**
- [ ] Audit Lead/Opportunity data quality
  - Are Industry, NumberOfEmployees, AnnualRevenue fields populated?
  - Are Lead Sources tracked correctly?
  - Test SOQL queries for new leads
- [ ] Create custom fields:
  - Lead.ARI_Score__c (Number 0-200)
  - Lead.ARI_Tier__c (Picklist: S, A, B, C, D)
  - Lead.Win_Probability__c (Percent)
  - Lead.Predicted_Close_Days__c (Number)
  - Lead.Layer_1_Demand__c through Layer_7_Prescriptive__c (Number fields)
  - Opportunity.ARI_Score__c (same fields)
- [ ] Create custom objects:
  - Website_Activity__c
  - Content_Engagement__c
  - Bombora_Intent__c
  - LinkedIn_Activity__c
  - Competitive_Signal__c
  - ARI_Score_History__c

**Day 3-4: External Integrations**
- [ ] Website Analytics:
  - Verify GA4 tracking on DRN website
  - Set up Zapier: GA4 → Website_Activity__c
  - Test: Visit /pricing, verify record created in Salesforce
- [ ] Marketing Automation:
  - HubSpot or Pardot → Content_Engagement__c sync
  - Map: Webinar attendance, whitepaper downloads
- [ ] Bombora Intent Data:
  - Install Bombora Salesforce connector (Data Cloud)
  - Configure intent topics (ALPR keywords)
  - Set surge threshold (≥75 = alert)
- [ ] LinkedIn Sales Navigator:
  - Install Salesforce app from AppExchange
  - Connect LinkedIn Sales Navigator accounts
  - Enable job change alerts

**Day 5-6: Agent Builder Setup**
- [ ] Create Agent: "DRN Lead Scoring Agent"
- [ ] Configure system prompt (copy from [Atlas Reasoning Engine Prompts](#atlas-reasoning-engine-prompts))
- [ ] Connect data sources (Lead, Opp, Account, Contact, custom objects)
- [ ] Build Apex actions (if needed):
  - `CalculateARIScoreAction.cls`
  - `GeneratePrescriptiveActionsAction.cls`

**Day 7: Salesforce Flow Configuration**
- [ ] Build `ARI_Lead_Scoring_Router` flow
- [ ] Configure tier-based routing logic
- [ ] Test with 10 sample leads (manual trigger)

---

#### Week 2: Testing & Calibration (Days 8-14)

**Day 8-10: Scoring Accuracy Testing**
- [ ] Historical backtest:
  - Select 50 closed-won opportunities (known outcomes)
  - Re-run ARI scoring using data from 30 days before close
  - Check: Did ARI score these as S/A-tier? (Target: 70%+ accuracy)
- [ ] Live test:
  - Score 100 new leads from last 30 days
  - Compare ARI tiers to sales rep intuition (survey reps)
  - Adjust scoring weights if needed

**Day 11-12: Flow & Automation Testing**
- [ ] Test tier routing:
  - Create test S-tier lead → Verify Slack alert + task created
  - Create test A-tier lead → Verify assignment + task
  - Create test D-tier lead → Verify disqualification
- [ ] Test edge cases:
  - Missing data (no email, no industry)
  - Duplicate leads
  - Opted-out contacts

**Day 13-14: Stakeholder Review**
- [ ] Demo to sales team:
  - Show sample scored leads (S/A/B/C/D)
  - Explain tier classification
  - Walk through generated outreach messages
- [ ] Gather feedback:
  - Are scores accurate?
  - Are outreach messages compelling?
  - Any false positives/negatives?
- [ ] Refine based on feedback

---

#### Week 3-4: Pilot Launch (Days 15-30)

**Day 15: Pilot Kickoff**
- [ ] Activate agent for pilot group (10-15 sales reps)
- [ ] Training session (1.5 hours):
  - How ARI works (7-layer framework)
  - How to interpret scores and tiers
  - How to act on S/A/B/C/D leads
  - How to provide feedback
- [ ] Enable real-time scoring (all new leads auto-scored)

**Days 16-30: Pilot Monitoring**
- [ ] Week 1 (Days 16-22):
  - Daily Slack check-ins with pilot reps
  - Monitor: Are scores accurate? Any issues?
  - Track: S-tier response rate, A-tier conversion
- [ ] Week 2 (Days 23-30):
  - Mid-pilot review meeting
  - Analyze results:
    - How many S-tier leads identified? (Target: 15-20)
    - How many reps contacted S-tier leads? (Target: 100%)
    - Response rate? (Target: 40%+ for S-tier)
  - Adjust scoring if needed (too strict? too lenient?)

**Day 30 Checkpoint:**
✅ Agent running autonomously
✅ 500+ leads scored
✅ 15-20 S-tier leads identified
✅ 40%+ S-tier response rate
✅ Reps trust scores (80%+ adoption)
✅ Stakeholder buy-in for full deployment

---

### Testing & Validation

#### Test 1: Scoring Accuracy (Precision & Recall)

**Goal:** Validate that S/A-tier scores predict actual conversions

**Method:**
1. Backtest on 100 closed opportunities (50 won, 50 lost)
2. Re-score using data from 30 days before close
3. Measure:
   - **Precision:** Of leads scored S/A-tier, what % actually won?
   - **Recall:** Of actual wins, what % were scored S/A-tier?

**Success Criteria:**
- Precision: >60% (S/A-tier leads should win at 60%+ rate)
- Recall: >70% (Agent should flag 70%+ of actual wins as S/A-tier)

---

#### Test 2: Tier Calibration

**Goal:** Ensure tiers match expected win rates

**Method:**
1. Score 200 new leads
2. Track conversions over 90 days
3. Compare actual win rates to tier targets:
   - S-Tier: 75-90% expected → Measure actual
   - A-Tier: 50-70% expected → Measure actual
   - B-Tier: 25-45% expected → Measure actual

**Success Criteria:**
- S-Tier actual win rate: 70%+ (within 5% of target)
- A-Tier actual win rate: 45%+ (within 10% of target)

---

#### Test 3: Sales Rep Adoption

**Goal:** Measure whether reps trust and use scores

**Method:**
1. Survey reps after 30 days:
   - "Do you trust ARI scores?" (1-10 scale)
   - "Do you follow tier-based prioritization?" (Yes/No)
   - "Are outreach messages helpful?" (Yes/No/Sometimes)
2. Measure behavior:
   - % of S-tier leads contacted within 4 hours (Target: 80%+)
   - % of S-tier tasks completed (Target: 95%+)

**Success Criteria:**
- Trust score: 7+/10
- Behavior compliance: 80%+

---

### Success Metrics

#### Primary Metrics (60-Day POC)

| Metric | Baseline (Pre-ARI) | Target (60 Days) | Stretch Goal |
|--------|-------------------|------------------|--------------|
| **Lead Conversion Rate** | 12% | 15% (+25%) | 18% (+50%) |
| **Qualification Time** | 25 min/lead | 15 min/lead (-40%) | 10 min/lead (-60%) |
| **Sales Cycle Length** | 68 days | 56 days (-18%) | 48 days (-29%) |
| **S-Tier Response Rate** | N/A | 40%+ | 60%+ |
| **A-Tier Win Rate** | N/A | 60%+ | 70%+ |
| **Pipeline Created** | $5M (60 days) | $6.5M (+30%) | $8M (+60%) |

---

#### Secondary Metrics (Efficiency)

| Metric | Target | Why It Matters |
|--------|--------|----------------|
| **Rep Time Saved** | 10 hours/week | Manual qualification eliminated |
| **Scoring Coverage** | 100% of leads | No lead left unscored |
| **Tier Accuracy** | 80%+ | Scores match outcomes |
| **Agent Uptime** | 99%+ | Reliability critical |

---

### Continuous Optimization

**How to improve ARI over time:**

#### Month 1-3: Baseline & Calibration
- Gather 90 days of conversion data
- Compare predicted vs actual win rates
- Adjust scoring weights if needed

#### Month 4-6: ML Model Training
- Train supervised ML model on 500+ scored leads
- Input features: All 7 layer scores + firmographic data
- Output: Win probability (0-100%)
- Replace rule-based Layer 6 with ML model

#### Month 7-12: Advanced Features
- Add: Propensity-to-buy scoring (when will they buy?)
- Add: Deal size prediction (how much will they spend?)
- Add: Churn risk (for existing customers, expansion opp scoring)

---

## CONCLUSION

**This playbook provides complete implementation of Autonomous Revenue Intelligence™ for Motorola DRN.**

**Key Differentiators vs. Traditional Lead Scoring:**
1. **7-layer architecture** (not simple point system)
2. **200-point scale** (not 100, allows multi-dimensional intelligence)
3. **Marketing + Sales fusion** (not siloed)
4. **Predictive + Prescriptive** (not just descriptive)
5. **Adaptive** (learns from outcomes, improves over time)

**Expected 60-Day POC Impact:**
- **1,500-2,000** leads scored
- **25%** increase in lead conversion
- **40%** reduction in qualification time
- **$1.5M-$2M** in new high-quality pipeline
- **20.8x ROI** (investment: $12K, return: $250K gross profit)

**This agent will validate the complete ARI framework and demonstrate AI-native revenue optimization to Motorola leadership.**

---

**Next Steps:**
1. Week 1: Foundation (data audit + integrations)
2. Week 2: Testing & calibration
3. Weeks 3-4: Pilot with 10-15 reps
4. Month 2: Full deployment (if successful)

**Questions? Refer to:**
- [ARI Framework Complete Documentation](ARI_FRAMEWORK_COMPLETE.md)
- [CAIO Training Master Curriculum](CAIO_TRAINING_MASTER_CURRICULUM.md)
- Salesforce Agentforce Docs: https://help.salesforce.com/agentforce

**Author:** Noel Pena
**Version:** 1.0
**Last Updated:** October 2025

---

**© 2025 Noel Pena. Proprietary & Confidential.**
**Autonomous Revenue Intelligence™ is a trademark of Noel Pena.**

**END OF PLAYBOOK**
