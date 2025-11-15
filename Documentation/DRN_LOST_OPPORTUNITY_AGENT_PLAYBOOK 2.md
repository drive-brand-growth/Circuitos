# DRN LOST OPPORTUNITY REACTIVATION AGENT
## Salesforce Agentforce Implementation Playbook

**Created by:** Noel Pena
**Division:** Motorola Solutions - DRN (Digital Recognition Network)
**Platform:** Salesforce Agentforce
**POC Timeline:** 60 Days
**Agent Type:** Autonomous Reactivation Agent
**Methodology:** Autonomous Revenue Intelligence™ (ARI) - Layer 6 (Revenue Velocity Intelligence)

---

**© 2025 Noel Pena. Proprietary & Confidential.**
**Autonomous Revenue Intelligence™ is a trademark of Noel Pena.**

---

## EXECUTIVE SUMMARY

### The Business Problem

**Motorola DRN has $5M+ in dormant pipeline** sitting in "Closed-Lost" status:
- Lost deals from last 90-120 days with no follow-up
- Circumstances may have changed (funding, personnel, competitive failures)
- No systematic process for identifying reactivation opportunities
- Sales reps manually check (if at all) - inconsistent and time-consuming

**Traditional Approach:**
- Sales rep manually reviews lost deals quarterly (maybe)
- Sends generic "checking in" emails
- No intelligence about what changed
- Low response rate (<5%)

**ARI Approach (AI-Powered):**
- AI agent continuously monitors all lost opportunities
- Detects meaningful change signals automatically
- Scores reactivation probability (0-100)
- Generates personalized outreach referencing specific changes
- Expected response rate: 15-20%

### Expected Impact (60-Day POC)

**Conservative Estimates:**
- 200-300 lost opportunities analyzed
- 40-60 scored 80+ (reactivation recommended)
- 15-20% reactivated (sales conversations resumed)
- $2M-$3M in pipeline resurrected
- 3-5 expected to close within 90 days ($300K-$500K revenue)

**ROI:**
- POC Investment: $8,000 (Agentforce licenses + implementation time)
- Pipeline Value: $2.5M (midpoint)
- Assuming 30% close rate: $750K revenue
- Assuming 40% gross margin: $300K gross profit
- **ROI: 37.5x in 60 days**

---

## TABLE OF CONTENTS

### PART I: AGENT DESIGN
1. [Agent Architecture](#agent-architecture)
2. [ARI Layer 6 Integration](#ari-layer-6-integration)
3. [Signal Taxonomy](#signal-taxonomy)
4. [Scoring Model](#scoring-model)

### PART II: SALESFORCE IMPLEMENTATION
5. [Data Source Mapping](#data-source-mapping)
6. [Agent Builder Configuration](#agent-builder-configuration)
7. [Atlas Reasoning Engine Prompts](#atlas-reasoning-engine-prompts)
8. [Workflow Automation](#workflow-automation)

### PART III: DEPLOYMENT
9. [30-Day Implementation Roadmap](#implementation-roadmap)
10. [Testing & Validation](#testing-validation)
11. [Success Metrics](#success-metrics)
12. [Troubleshooting Guide](#troubleshooting-guide)

---

## PART I: AGENT DESIGN

### Agent Architecture

#### High-Level Flow

```
┌─────────────────────────────────────────────────────────┐
│         LOST OPPORTUNITY REACTIVATION AGENT             │
└─────────────────────────────────────────────────────────┘
                          │
                          ↓
┌─────────────────────────────────────────────────────────┐
│  STEP 1: IDENTIFY CANDIDATES                            │
│  - Opportunities with Status = "Closed-Lost"            │
│  - Closed Date: 90-120 days ago                         │
│  - Deal Size: >$50K (focus on high-value)               │
│  - Industry: Parking, Retail, Fleet, Commercial         │
└─────────────────────────────────────────────────────────┘
                          │
                          ↓
┌─────────────────────────────────────────────────────────┐
│  STEP 2: GATHER NEW SIGNALS                             │
│  - Company changes (funding, acquisitions, leadership)  │
│  - Personnel changes (new Security Dir, CFO, CEO)       │
│  - Competitive intel (competitor failures, news)        │
│  - Intent signals (researching ALPR again? Bombora)     │
│  - Firmographic changes (new locations, expansion)      │
└─────────────────────────────────────────────────────────┘
                          │
                          ↓
┌─────────────────────────────────────────────────────────┐
│  STEP 3: CALCULATE REACTIVATION SCORE (0-100)           │
│  - Apply ARI Layer 6 (Revenue Velocity Intelligence)    │
│  - Weight signals by predictive power                   │
│  - Compare to historical reactivation patterns          │
└─────────────────────────────────────────────────────────┘
                          │
                          ↓
┌─────────────────────────────────────────────────────────┐
│  STEP 4: GENERATE PERSONALIZED OUTREACH                 │
│  - Reference specific change signal                     │
│  - Address original objection (if known)                │
│  - Offer new value (new features, case studies)         │
│  - Low-friction CTA (15-min call, not full demo)        │
└─────────────────────────────────────────────────────────┘
                          │
                          ↓
┌─────────────────────────────────────────────────────────┐
│  STEP 5: ROUTE TO SALES REP                             │
│  - Score 80-100: IMMEDIATE (alert rep within 4 hours)  │
│  - Score 60-79: STANDARD (add to weekly review)        │
│  - Score 40-59: MONITOR (check again in 30 days)       │
│  - Score <40: DISQUALIFY (no reactivation opportunity) │
└─────────────────────────────────────────────────────────┘
                          │
                          ↓
┌─────────────────────────────────────────────────────────┐
│  STEP 6: TRACK & LEARN                                  │
│  - Did rep reach out? (execution tracking)              │
│  - Did prospect respond? (engagement tracking)          │
│  - Did deal reactivate? (conversion tracking)           │
│  - Feed data back to ML model (continuous learning)     │
└─────────────────────────────────────────────────────────┘
```

---

### ARI Layer 6 Integration

**Why Layer 6 (Revenue Velocity Intelligence)?**

Lost Opportunity Reactivation is fundamentally about **velocity**: detecting when a stalled deal can be **accelerated back into motion**.

**Traditional Method:**
- Rep manually checks lost deals
- Guesses "maybe they're ready now?"
- No data-driven approach

**ARI Layer 6 Approach:**
- Historical pattern matching: Which signals predict reactivation?
- Velocity scoring: How fast can this deal come back?
- Risk detection: What killed it before? Is that still present?

**ARI Layer 6 Components Used:**

#### 1. Historical Pattern Matching

```python
# AI analyzes 10,000+ historical opportunities

Similar reactivated deals (matching criteria):
- Industry: Parking/Security (28 reactivated wins)
- Deal size: $50K-$150K (19 reactivated wins)
- Region: Northeast US (12 reactivated wins)
- Original close reason: "Budget constraints" (8 reactivated wins)
- Days since close: 90-120 days (current analysis window)

Pattern Recognition:
- Reactivations with new personnel: 68% win rate (STRONG signal)
- Reactivations with funding event: 54% win rate (GOOD signal)
- Reactivations with competitor failure: 71% win rate (VERY STRONG)
- Reactivations with no change signals: 12% win rate (WEAK)

Recommendation: PRIORITIZE personnel changes and competitor failures
```

#### 2. Velocity Scoring

```python
# How fast can this deal come back?

Time to Reactivation Prediction:
- Days since close: 105 days
- Historical avg for this pattern: 120 days (we're 15 days early - good timing)
- Expected response time: 3-7 days (if we reach out now)
- Expected opportunity re-open: 14-21 days (after initial engagement)
- Expected new close date: 60-90 days (from reactivation)

Velocity Score: +18 points (faster than average = good signal)
```

#### 3. Deal Health Risk Detection

```python
# Why did it die before? Is that still present?

Original Close Reason: "Budget constraints - CFO rejected"
Risk Assessment:
- Company funding status: CHANGED (Series B raised 45 days ago) ✅
- CFO still there: NO (new CFO hired 30 days ago) ✅✅
- Original objection: LIKELY RESOLVED (new budget year + new CFO)

Risk Mitigation Score: +25 points (original blocker removed)
```

**Total ARI Layer 6 Contribution: 50 points (of 100 reactivation score)**

---

### Signal Taxonomy

**What signals indicate a lost opportunity can be reactivated?**

#### Category 1: Company Change Signals (Max 25 points)

**Funding Events:**
```
Series A/B/C raised: +15 points (CRITICAL: Budget now available)
Debt financing secured: +10 points (expansion capital)
IPO announcement: +12 points (enterprise-grade budget unlocked)
Acquisition (company acquired): +8 points (new parent may prioritize security)
Acquisition (company acquires another): +6 points (expansion = need for ALPR)
```

**Example:**
```
Acme Parking (Closed-Lost 102 days ago)
Original objection: "No budget this year"

NEW SIGNAL DETECTED:
- Acme Parking raised $12M Series B (announced 43 days ago)
- Press release mentions "expanding to 15 new cities in 2025"
→ Score: +15 points (funding) + 6 points (expansion)
→ Reactivation Recommendation: HIGH PRIORITY

Suggested Outreach:
"Hi [Contact], I saw the exciting news about your Series B and 15-city
expansion. Congrats! When we last spoke, timing wasn't right. Given your
growth plans, I'd love to revisit how DRN ALPR can scale with you across
all 15 locations. Quick 15-min call this week?"
```

**Strategic Changes:**
```
New CEO announcement: +12 points (new leadership = new priorities)
New locations opened: +10 points (expansion = new ALPR needs)
Market expansion (new geography): +8 points (scaling operations)
Rebranding/repositioning: +6 points (investing in business = budget)
```

---

#### Category 2: Personnel Change Signals (Max 30 points)

**Key Decision Maker Changes:**
```
New Security Director hired: +20 points (PRIMARY BUYER PERSONA)
New CFO hired: +15 points (budget authority changed)
New CEO hired: +12 points (new strategic priorities)
New CTO hired: +10 points (technology refresh initiatives)
New VP Operations: +10 points (operational efficiency focus)
```

**Why This Is CRITICAL:**
- Original decision maker may have rejected us
- New decision maker = clean slate, no prior bias
- Often hired specifically to "fix" issues (like vehicle theft)

**Example:**
```
Metro Parking (Closed-Lost 118 days ago)
Original objection: "Security Director prefers Genetec"

NEW SIGNAL DETECTED:
- Original Security Director left company 67 days ago (LinkedIn)
- NEW Security Director hired 28 days ago (LinkedIn + company announcement)
- New hire's background: 8 years at parking operator that USES DRN ALPR
→ Score: +20 points (new Security Dir) + 10 points (ALPR experience)
→ Reactivation Recommendation: URGENT - Contact within 24 hours

Suggested Outreach:
"Hi [New Security Director], welcome to Metro Parking! I noticed you
come from [Previous Company] where you used our DRN ALPR system. We
actually spoke with Metro last year but timing wasn't right. Given
your familiarity with our platform, I'd love to reconnect and see if
there's a fit now. Coffee this week?"
```

**Champion Departure (Negative Signal):**
```
Our champion left company: -15 points (lost internal advocate)
Economic buyer left: -10 points (restart qualification)
```

---

#### Category 3: Competitive Intelligence Signals (Max 25 points)

**Competitor Failures:**
```
Competitor implementation delayed/failed: +20 points (GOLDEN opportunity)
Competitor customer complaints (G2, Reddit, news): +12 points
Competitor price increase announced: +8 points (we're now competitive)
Competitor acquired (uncertainty): +10 points (customers re-evaluating)
```

**Example:**
```
Premium Parking (Closed-Lost 95 days ago)
Original outcome: "Went with Genetec"

NEW SIGNAL DETECTED:
- Reddit post from Premium Parking employee (verified via LinkedIn):
  "Our new Genetec ALPR system has been down 3x in 2 months. Management
  is furious. Anyone else have issues with Genetec reliability?"
- Posted 18 days ago, 47 upvotes, 23 comments (mostly negative about Genetec)
→ Score: +20 points (competitor failure documented publicly)
→ Reactivation Recommendation: IMMEDIATE

Suggested Outreach:
"Hi [Contact], I hope the Genetec implementation is going well. I saw
some discussion online about ALPR reliability challenges in the industry.
If you're experiencing any issues or want a backup plan, we'd love to
show you how DRN handles uptime differently. Our 99.7% uptime SLA is
backed by [proof]. Quick call?"
```

---

#### Category 4: Intent Signal Re-Emergence (Max 15 points)

**Digital Engagement (New Activity):**
```
Returned to DRN website (3+ pages): +10 points (renewed interest)
Downloaded new case study/whitepaper: +12 points (active research)
Attended DRN webinar: +15 points (HIGH intent)
Opened recent email campaign (3+ emails): +6 points (engaged)
```

**Third-Party Intent Data (Bombora, 6sense):**
```
Intent surge for "ALPR" or "License plate recognition": +12 points
Intent surge for "vehicle security" (category): +8 points
Intent surge for competitor keywords: +10 points (re-evaluating)
```

**Example:**
```
Secure Lots Inc (Closed-Lost 110 days ago)

NEW SIGNAL DETECTED:
- Bombora Intent Signal: "ALPR solutions"
  Surge Score: 82 (Very High - 4x above baseline)
- Website activity: Visited DRN pricing page 2x in last 14 days
- Email engagement: Opened 4 of last 5 emails (was 0 of 10 previously)
→ Score: +12 points (intent surge) + 10 points (website) + 6 points (email)
→ Reactivation Recommendation: HIGH PRIORITY

Suggested Outreach:
"Hi [Contact], I noticed you've been researching ALPR solutions again.
Last time we spoke, [original objection]. I wanted to share a new case
study from [similar company] that addressed exactly that concern. Would
a quick 15-min call make sense to see if things have changed on your end?"
```

---

#### Category 5: Firmographic Change Signals (Max 10 points)

**Business Growth Indicators:**
```
Headcount increase (20%+ growth): +8 points (business is thriving)
New locations added: +10 points (expansion needs)
Revenue growth (if public/reported): +6 points (budget availability)
Award/recognition (Best Places to Work, etc): +4 points (investing in business)
```

---

### Scoring Model

#### Reactivation Score Calculation (0-100)

**Formula:**
```
Reactivation Score =
  Company Changes (0-25) +
  Personnel Changes (0-30) +
  Competitive Intelligence (0-25) +
  Intent Signals (0-15) +
  Firmographic Changes (0-10) +
  ARI Layer 6 Adjustments (-10 to +15)

Maximum Possible: 110 points (normalized to 100)
```

**ARI Layer 6 Adjustments:**

**Positive Adjustments:**
```
+15: Original blocker removed (CFO who rejected is gone)
+10: Historical pattern match (90%+ similar deals reactivated)
+8: Velocity timing optimal (120 days = sweet spot for this pattern)
+5: Multiple signals present (3+ categories with points)
```

**Negative Adjustments:**
```
-10: Champion departed (lost internal advocate)
-8: Original objection still present (budget still tight, per 10-K filing)
-5: Too soon (<60 days since close - let them breathe)
-5: Too late (>180 days, probably moved on)
```

---

#### Tier Classification

**Tier 1: URGENT (Score 80-100)**
- **Action:** Immediate outreach within 24 hours
- **Assignment:** Senior AE who knows the account
- **Outreach:** Personalized email + LinkedIn message + phone call
- **CTA:** 15-min call this week (low friction)
- **Expected Response Rate:** 30-40%

**Tier 2: HIGH PRIORITY (Score 60-79)**
- **Action:** Outreach within 1 week
- **Assignment:** Original AE (or territory AE)
- **Outreach:** Personalized email
- **CTA:** "Worth a quick conversation?" (non-pushy)
- **Expected Response Rate:** 15-25%

**Tier 3: MONITOR (Score 40-59)**
- **Action:** Add to nurture campaign, check again in 30 days
- **Assignment:** Marketing automation (not direct sales)
- **Outreach:** Value-add content (new case studies, webinars)
- **CTA:** "Let us know if you want to chat"
- **Expected Response Rate:** 5-10%

**Tier 4: DISQUALIFY (Score <40)**
- **Action:** Remove from active list, archive
- **Assignment:** None
- **Outreach:** None (don't waste rep time)
- **Expected Response Rate:** <2% (not worth effort)

---

## PART II: SALESFORCE IMPLEMENTATION

### Data Source Mapping

**Where does the agent get signal data?**

#### Primary Data Sources (Salesforce Native)

**1. Opportunity Object (Core Data)**
```
Fields Required:
- Opportunity.Id
- Opportunity.Name
- Opportunity.StageName (filter: "Closed Lost")
- Opportunity.CloseDate (filter: 90-120 days ago)
- Opportunity.Amount (filter: >$50,000)
- Opportunity.Type (Industry: Parking, Retail, Fleet, Commercial)
- Opportunity.Loss_Reason__c (custom field: why did we lose?)
- Opportunity.Primary_Competitor__c (custom field: who won?)
- Account.Id (related account)
- Contact.Id (related contacts)
```

**SOQL Query:**
```sql
SELECT Id, Name, StageName, CloseDate, Amount, Type,
       Loss_Reason__c, Primary_Competitor__c,
       Account.Id, Account.Name, Account.Industry, Account.NumberOfEmployees
FROM Opportunity
WHERE StageName = 'Closed Lost'
  AND CloseDate >= LAST_N_DAYS:120
  AND CloseDate <= LAST_N_DAYS:90
  AND Amount > 50000
  AND Type IN ('Parking', 'Retail', 'Fleet', 'Commercial Security')
ORDER BY CloseDate DESC
```

**2. Account Object (Company Data)**
```
Fields Required:
- Account.Id
- Account.Name
- Account.Industry
- Account.NumberOfEmployees (track for growth)
- Account.AnnualRevenue (if available)
- Account.BillingState (geographic filter)
```

**3. Contact Object (Personnel Tracking)**
```
Fields Required:
- Contact.Id
- Contact.Name
- Contact.Title (track: Security Director, CFO, CEO, CTO)
- Contact.Email
- Contact.MobilePhone
- Contact.Role__c (custom: Champion, Economic Buyer, Influencer)
- Contact.Active__c (custom: still at company?)
```

---

#### External Data Sources (Integrations Required)

**1. LinkedIn Sales Navigator (Personnel Changes)**

**Integration: Salesforce AppExchange App**
- App: "LinkedIn Sales Navigator for Salesforce"
- Cost: Included with LinkedIn Sales Navigator Team ($99/user/month)

**Data Synced:**
```
New Contacts at Account:
- New Security Director hired → ALERT (20 points)
- New CFO hired → ALERT (15 points)
- Champion left company → ALERT (-15 points)

Company News:
- Funding announcements
- Leadership changes
- Office openings/expansion
```

**Setup Steps:**
1. Install LinkedIn Sales Navigator Salesforce app from AppExchange
2. Connect LinkedIn Sales Navigator Team account
3. Configure sync: Account → LinkedIn Company Page mapping
4. Enable alerts: New executive hires at target accounts

**Agent Access:**
```apex
// Access LinkedIn data via Salesforce
Account acct = [SELECT Id, LinkedIn_Company_Page__c FROM Account WHERE Id = :accountId];
List<LinkedIn_Update__c> updates = [
    SELECT Event_Type__c, Description__c, Date__c
    FROM LinkedIn_Update__c
    WHERE Account__c = :accountId
      AND Date__c >= :closeDate
    ORDER BY Date__c DESC
];
```

---

**2. Bombora Intent Data (Buying Signals)**

**Integration: Salesforce Data Cloud**
- Connector: Bombora Company Surge® for Salesforce
- Cost: ~$15K-$30K/year (enterprise)

**Data Synced:**
```
Intent Topics:
- "ALPR solutions" (surge score 0-100)
- "License plate recognition" (surge score 0-100)
- "Vehicle security systems" (surge score 0-100)
- "Parking security" (surge score 0-100)
- Competitor keywords: "Genetec", "Vigilant", etc.

Surge Scoring:
- 0-20: Baseline (no unusual activity)
- 21-50: Moderate (some research)
- 51-75: High (active evaluation)
- 76-100: Very High (imminent purchase)
```

**Setup Steps:**
1. Sign Bombora contract (contact Bombora sales)
2. Install Bombora Salesforce connector (Data Cloud)
3. Map Bombora company records to Salesforce Accounts (domain matching)
4. Configure intent topics (select relevant keywords)
5. Set surge threshold alerts (≥75 = agent notification)

**Agent Access:**
```apex
// Query Bombora intent data
List<Bombora_Intent__c> intentSignals = [
    SELECT Topic__c, Surge_Score__c, Week_Start__c
    FROM Bombora_Intent__c
    WHERE Account__c = :accountId
      AND Surge_Score__c >= 50
      AND Week_Start__c >= :closeDate
    ORDER BY Surge_Score__c DESC
];
```

---

**3. Website Analytics (Digital Engagement)**

**Integration: Google Analytics 4 → Salesforce (via Zapier or native connector)**

**Data Tracked:**
```
Page Visits (post-close):
- /products/alpr (pricing page): HIGH intent
- /case-studies (evaluation): MEDIUM intent
- /blog (awareness): LOW intent

Session Data:
- Number of visits since close
- Pages per session (engagement depth)
- Time on site (engagement quality)
- Form submissions (contact request)
```

**Setup Steps:**
1. Ensure GA4 tracking on DRN website
2. Create Salesforce custom object: `Website_Activity__c`
3. Use Zapier or Salesforce Marketing Cloud to push GA4 data
4. Match website visitors to Salesforce Contacts/Leads (email or cookie ID)

**Agent Access:**
```apex
List<Website_Activity__c> websiteVisits = [
    SELECT Page_URL__c, Visit_Date__c, Time_On_Page__c
    FROM Website_Activity__c
    WHERE Contact__c IN :relatedContacts
      AND Visit_Date__c >= :closeDate
    ORDER BY Visit_Date__c DESC
];
```

---

**4. News Monitoring (Competitive Intelligence)**

**Integration: Google Alerts + Zapier → Salesforce**

**Setup:**
1. Create Google Alerts for:
   - "[Account Name] funding"
   - "[Account Name] new hire"
   - "[Account Name] expansion"
   - "Genetec ALPR problems" (competitor negative news)
   - "Vigilant ALPR issues"
2. Configure Zapier:
   - Trigger: New Google Alert email
   - Action: Create Salesforce Task or Custom Object `News_Alert__c`
3. Link to Account (parse account name from alert)

**Agent Access:**
```apex
List<News_Alert__c> news = [
    SELECT Headline__c, Summary__c, URL__c, Published_Date__c
    FROM News_Alert__c
    WHERE Account__c = :accountId
      AND Published_Date__c >= :closeDate
    ORDER BY Published_Date__c DESC
];
```

---

**5. Crunchbase (Funding Data)**

**Integration: Crunchbase Enterprise API**
- Cost: ~$15K-$50K/year (enterprise API access)
- Alternative: Manual monitoring + Zapier

**Data Tracked:**
```
Funding Events:
- Series A/B/C announcements
- Amount raised
- Investors
- Date announced
```

**Setup Steps:**
1. Subscribe to Crunchbase Enterprise API
2. Build middleware to sync funding events to Salesforce (or use Zapier)
3. Create custom object: `Funding_Event__c`
4. Link to Account (company name matching)

**Agent Access:**
```apex
List<Funding_Event__c> fundingEvents = [
    SELECT Funding_Round__c, Amount__c, Announced_Date__c
    FROM Funding_Event__c
    WHERE Account__c = :accountId
      AND Announced_Date__c >= :closeDate
    ORDER BY Announced_Date__c DESC
];
```

---

### Agent Builder Configuration

**Salesforce Agentforce Setup (Step-by-Step)**

#### Step 1: Create Agent in Agent Builder

**Navigate:** Setup → Agents → New Agent

**Agent Configuration:**
```yaml
Agent Name: "Lost Opportunity Reactivation Agent"
Description: "Automatically identifies and scores lost opportunities that can be reactivated based on company changes, personnel changes, competitive intelligence, and intent signals."

Agent Type: Service Agent (Autonomous)

Topics:
  - Lost Opportunity Analysis
  - Revenue Reactivation
  - Pipeline Resurrection

Channels:
  - Slack (alerts to sales reps)
  - Email (automated outreach drafts)
  - Salesforce (internal actions: create tasks, update opps)

Visibility: Internal Only (sales team + RevOps)
```

---

#### Step 2: Configure Agent Instructions (Atlas Reasoning Engine)

**Instructions = "Brain" of the Agent**

Navigate to: Agent Builder → Instructions → System Prompt

**System Prompt:**
```markdown
You are the Lost Opportunity Reactivation Agent for Motorola Solutions DRN.

# MISSION
Your mission is to identify lost opportunities (Closed-Lost status, 90-120 days ago)
that have a HIGH PROBABILITY of reactivation based on NEW signals that emerged
since the opportunity closed.

# METHODOLOGY
You use Autonomous Revenue Intelligence™ (ARI) Layer 6 (Revenue Velocity Intelligence)
to score reactivation probability (0-100) based on 5 signal categories:

1. Company Change Signals (0-25 points): Funding, expansion, acquisitions
2. Personnel Change Signals (0-30 points): New Security Director, CFO, CEO
3. Competitive Intelligence (0-25 points): Competitor failures, price increases
4. Intent Signal Re-Emergence (0-15 points): Website visits, Bombora surge
5. Firmographic Changes (0-10 points): Headcount growth, new locations

Plus ARI Layer 6 Adjustments (-10 to +15 points):
- Original blocker removed: +15
- Champion departed: -10
- Historical pattern match: +10

Total Score: 0-110 (normalized to 0-100)

# TIER CLASSIFICATION
- URGENT (80-100): Contact within 24 hours
- HIGH PRIORITY (60-79): Contact within 1 week
- MONITOR (40-59): Nurture, check again in 30 days
- DISQUALIFY (<40): Archive, no action

# YOUR RESPONSIBILITIES
1. Query Salesforce for lost opportunities (90-120 days ago, >$50K)
2. For each opportunity, gather signals from:
   - LinkedIn (personnel changes)
   - Bombora (intent data)
   - Website analytics (digital engagement)
   - News alerts (company/competitive news)
   - Crunchbase (funding events)
3. Calculate reactivation score using ARI scoring model
4. Generate personalized outreach message referencing specific signals
5. Route to appropriate sales rep with priority level
6. Track outcomes (was contact made? did they respond? did deal reactivate?)

# COMMUNICATION STYLE
When drafting outreach messages:
- Professional but conversational (not robotic)
- Reference SPECIFIC signal (not generic "checking in")
- Acknowledge original objection (if known)
- Low-friction CTA (15-min call, not full demo)
- Tone: helpful, not pushy

# EXAMPLE GOOD OUTREACH
"Hi Sarah, I saw that Acme Parking raised $12M Series B last month - congrats!
When we last spoke in July, timing wasn't right due to budget constraints.
Given your expansion plans (15 new cities mentioned in the press release),
I'd love to revisit how DRN ALPR can scale with you. Quick 15-min call this week?"

# EXAMPLE BAD OUTREACH
"Hi, just checking in to see if you're interested in DRN ALPR yet."

# DATA SOURCES
You have access to:
- Salesforce Opportunity, Account, Contact objects
- LinkedIn Sales Navigator sync data
- Bombora intent data (Data Cloud)
- Website analytics (via custom object)
- News alerts (via custom object)
- Crunchbase funding events (via custom object)

# CONSTRAINTS
- NEVER reach out if champion explicitly requested "no contact"
- NEVER reach out if account is marked "Do Not Contact" (compliance)
- ALWAYS verify contact is still at company (LinkedIn)
- ALWAYS prioritize accounts with ACV >$100K (high value)
- Process opportunities in batches of 50 (every Monday)

# SUCCESS METRICS
Your performance is measured by:
- Reactivation Rate: % of URGENT/HIGH leads that respond (target: 20%)
- Conversion Rate: % of reactivated leads that re-open opportunity (target: 15%)
- Pipeline Value: Total $$ reactivated (target: $2M+ in 60 days)
- Efficiency: Time saved vs manual review (target: 10 hours/week per rep)

You are autonomous. You analyze, score, and recommend WITHOUT human approval
for scores <80. For scores 80-100 (URGENT), alert sales manager for review before outreach.
```

---

#### Step 3: Configure Data Sources (Agent → Salesforce Objects)

**Navigate:** Agent Builder → Data → Add Data Source

**Connected Objects:**

```yaml
Objects:
  - Opportunity (READ, WRITE)
  - Account (READ)
  - Contact (READ, WRITE)
  - LinkedIn_Update__c (READ) - custom object
  - Bombora_Intent__c (READ) - custom object via Data Cloud
  - Website_Activity__c (READ) - custom object
  - News_Alert__c (READ) - custom object
  - Funding_Event__c (READ) - custom object
  - Task (WRITE) - for creating sales rep tasks

Permissions:
  - Read all lost opportunities (Closed Lost, 90-120 days)
  - Read account and contact data
  - Read external signal data (LinkedIn, Bombora, etc.)
  - Write: Create Tasks, Update Opportunity.Reactivation_Score__c field
```

---

#### Step 4: Configure Actions (What the Agent Can Do)

**Navigate:** Agent Builder → Actions → Add Action

**Action 1: Analyze Lost Opportunities**
```yaml
Action Name: "Analyze_Lost_Opportunities"
Type: Apex Class
Description: "Query lost opportunities and gather all signal data"

Apex Class: AnalyzeLostOpportunitiesAction.cls

Input Parameters:
  - daysAgo: 90-120 (opportunity close date range)
  - minAmount: 50000 (filter for high-value deals)
  - maxBatchSize: 50 (process 50 at a time)

Output:
  - List<OpportunityWithSignals> (enriched opportunity data)
```

**Action 2: Calculate Reactivation Score**
```yaml
Action Name: "Calculate_Reactivation_Score"
Type: Apex Class
Description: "Apply ARI scoring model to calculate 0-100 score"

Apex Class: CalculateReactivationScoreAction.cls

Input Parameters:
  - opportunityId: Opportunity.Id
  - signals: OpportunitySignals object (all gathered signals)

Output:
  - score: Integer (0-100)
  - tier: String (URGENT, HIGH PRIORITY, MONITOR, DISQUALIFY)
  - reasoning: String (explanation of score for transparency)
```

**Action 3: Generate Outreach Message**
```yaml
Action Name: "Generate_Outreach_Message"
Type: LLM Prompt Template
Description: "Generate personalized reactivation email"

Prompt Template:
"""
Generate a personalized reactivation email for the following lost opportunity.

CONTEXT:
- Company: {{Account.Name}}
- Contact: {{Contact.Name}} ({{Contact.Title}})
- Opportunity: {{Opportunity.Name}}
- Amount: {{Opportunity.Amount}}
- Close Date: {{Opportunity.CloseDate}}
- Loss Reason: {{Opportunity.Loss_Reason__c}}
- Primary Competitor: {{Opportunity.Primary_Competitor__c}}

NEW SIGNALS (since close):
{{signals.summary}}

SCORING:
- Reactivation Score: {{score}}/100
- Top Signal: {{signals.topSignal}}
- Historical Pattern: {{signals.patternMatch}}

INSTRUCTIONS:
- Reference the TOP SIGNAL specifically (don't be generic)
- Acknowledge original objection if known: {{Opportunity.Loss_Reason__c}}
- Offer new value (case study, new features, pricing change)
- Low-friction CTA: 15-min call (not full demo)
- Professional but conversational tone
- Max 150 words

SUBJECT LINE:
[Generate 6-8 word subject line]

EMAIL BODY:
[Generate email]
"""

Output:
  - subject: String
  - body: String (email body text)
```

**Action 4: Create Sales Task**
```yaml
Action Name: "Create_Reactivation_Task"
Type: Standard Salesforce Action (Create Record)
Description: "Create task for sales rep to follow up"

Object: Task

Field Mapping:
  - Subject: "REACTIVATION OPPORTUNITY: {{Account.Name}} (Score: {{score}})"
  - Description: "{{outreachMessage.body}}\n\nReasoning: {{scoreReasoning}}"
  - Priority: {{tier}} (URGENT → High, HIGH PRIORITY → Normal, MONITOR → Low)
  - Status: "Not Started"
  - ActivityDate: {{calculateDueDate(tier)}} (URGENT: Today, HIGH: +7 days, MONITOR: +30 days)
  - WhoId: {{primaryContact.Id}}
  - WhatId: {{opportunity.Id}}
  - OwnerId: {{opportunity.OwnerId}} (assign to original AE)
```

**Action 5: Send Slack Alert (for URGENT leads)**
```yaml
Action Name: "Send_Slack_Alert"
Type: External Service (Slack API)
Description: "Alert sales rep on Slack for urgent leads (score 80-100)"

Slack Message Template:
"""
🚨 URGENT REACTIVATION OPPORTUNITY

**Account:** {{Account.Name}}
**Deal Size:** ${{Opportunity.Amount}}
**Score:** {{score}}/100 ({{tier}})

**Why Now:**
{{signals.topSignal}}

**Action Required:**
Contact within 24 hours.

Draft email: [Link to Salesforce Task]
Opportunity: [Link to Salesforce Opp]
"""

Trigger Condition: score >= 80
```

---

### Atlas Reasoning Engine Prompts

**The Atlas Reasoning Engine is Agentforce's LLM-powered "brain."**

Here's how to configure Atlas prompts for multi-step reasoning:

#### Prompt 1: Signal Gathering & Analysis

**Prompt Template Name:** `gather_reactivation_signals`

**Atlas Prompt:**
```markdown
You are analyzing a lost opportunity to determine if it can be reactivated.

# OPPORTUNITY DATA
- Company: {{Account.Name}}
- Industry: {{Account.Industry}}
- Opportunity: {{Opportunity.Name}}
- Amount: {{Opportunity.Amount}}
- Close Date: {{Opportunity.CloseDate}} ({{daysAgo}} days ago)
- Loss Reason: {{Opportunity.Loss_Reason__c}}
- Primary Competitor: {{Opportunity.Primary_Competitor__c}}

# YOUR TASK
Step 1: Identify all NEW signals that emerged since {{Opportunity.CloseDate}}.
Step 2: Categorize signals into 5 categories.
Step 3: Assign points to each signal based on ARI scoring model.
Step 4: Calculate total reactivation score (0-100).
Step 5: Determine tier (URGENT, HIGH PRIORITY, MONITOR, DISQUALIFY).
Step 6: Generate reasoning for the score (explain why this score was assigned).

# AVAILABLE DATA SOURCES

## LinkedIn Data
{{linkedInUpdates}}

## Bombora Intent Data
{{bomboraIntentSignals}}

## Website Activity
{{websiteActivityLogs}}

## News Alerts
{{newsAlerts}}

## Funding Events
{{fundingEvents}}

## Historical Patterns (from ML model)
{{historicalPatternMatch}}

# SCORING MODEL

## Category 1: Company Change Signals (0-25 points)
- Series A/B/C raised: +15
- Debt financing: +10
- IPO announced: +12
- Acquired by another company: +8
- Acquired another company: +6

## Category 2: Personnel Change Signals (0-30 points)
- New Security Director: +20 (PRIMARY BUYER)
- New CFO: +15
- New CEO: +12
- New CTO: +10
- New VP Operations: +10
- Champion left company: -15 (NEGATIVE)

## Category 3: Competitive Intelligence (0-25 points)
- Competitor implementation failed: +20
- Competitor customer complaints: +12
- Competitor price increase: +8
- Competitor acquired: +10

## Category 4: Intent Signal Re-Emergence (0-15 points)
- Returned to website (3+ pages): +10
- Downloaded case study: +12
- Attended webinar: +15
- Bombora intent surge (>75): +12

## Category 5: Firmographic Changes (0-10 points)
- Headcount growth 20%+: +8
- New locations added: +10
- Revenue growth reported: +6

## ARI Layer 6 Adjustments (-10 to +15)
- Original blocker removed (e.g., CFO who rejected left): +15
- Historical pattern match (90%+ similar deals reactivated): +10
- Optimal timing (120 days = sweet spot): +8
- Champion departed: -10
- Original objection still present: -8
- Too soon (<60 days): -5

# OUTPUT FORMAT

Return JSON:

{
  "accountName": "{{Account.Name}}",
  "opportunityId": "{{Opportunity.Id}}",
  "signalsDetected": [
    {
      "category": "Personnel Change",
      "signal": "New Security Director hired 28 days ago",
      "source": "LinkedIn",
      "points": 20,
      "importance": "CRITICAL"
    },
    {
      "category": "Company Change",
      "signal": "Series B funding $12M raised 43 days ago",
      "source": "Crunchbase",
      "points": 15,
      "importance": "HIGH"
    }
  ],
  "scoring": {
    "companyChangePoints": 15,
    "personnelChangePoints": 20,
    "competitiveIntelPoints": 0,
    "intentSignalPoints": 10,
    "firmographicPoints": 0,
    "ariLayer6Adjustments": 8,
    "totalScore": 53,
    "normalizedScore": 53,
    "tier": "HIGH PRIORITY"
  },
  "reasoning": "Score of 53 is driven primarily by new Security Director hire (20 points, CRITICAL signal as they are PRIMARY buyer persona) and Series B funding (15 points, removes original budget objection). Website activity shows renewed interest (10 points). Historical pattern match suggests 62% reactivation probability for similar deals. Recommend outreach within 7 days.",
  "topSignal": "New Security Director with ALPR experience hired 28 days ago",
  "recommendedAction": "Personalized outreach within 7 days referencing new Security Director and Series B funding",
  "historicalWinProbability": 62
}

# IMPORTANT
- Be conservative with scoring (only assign points if signal is VERIFIED and RELEVANT)
- Multi-signal convergence is powerful (3+ signals = higher confidence)
- Always explain reasoning (transparency for sales reps)
- If score <40, recommend DISQUALIFY (don't waste rep time)
```

---

#### Prompt 2: Outreach Message Generation

**Prompt Template Name:** `generate_reactivation_outreach`

**Atlas Prompt:**
```markdown
You are drafting a reactivation email for a lost opportunity.

# OPPORTUNITY CONTEXT
- Company: {{Account.Name}}
- Contact: {{Contact.FirstName}} {{Contact.LastName}}
- Title: {{Contact.Title}}
- Opportunity: {{Opportunity.Name}}
- Amount: ${{Opportunity.Amount}}
- Close Date: {{Opportunity.CloseDate}} ({{daysAgo}} days ago)
- Original Loss Reason: {{Opportunity.Loss_Reason__c}}
- Competitor (if known): {{Opportunity.Primary_Competitor__c}}

# NEW SIGNALS (Why we're reaching out now)
{{signals.summary}}

Top Signal: {{signals.topSignal}}

# REACTIVATION SCORE
Score: {{score}}/100 ({{tier}})

# YOUR TASK
Draft a personalized reactivation email that:

1. **References specific signal** (not generic "checking in")
   - Example: "I saw you raised Series B" or "I noticed you hired a new Security Director"

2. **Acknowledges original objection** (if known)
   - Example: "Last time we spoke, budget was a concern..."

3. **Offers new value**
   - New case study from similar company
   - New features/capabilities since last conversation
   - Limited-time offer or pricing change (if applicable)

4. **Low-friction CTA**
   - 15-minute call (not full demo)
   - Specific timing: "this week" or "next Tuesday"

5. **Professional but conversational tone**
   - Not robotic or salesy
   - Genuine interest in their business
   - Respectful of their time

# STYLE GUIDELINES

✅ DO:
- "I saw [specific news]..."
- "Given [specific change], I thought it might be worth reconnecting"
- "Quick 15-min call to see if things have changed?"
- "Congrats on [funding/expansion/new hire]"

❌ DON'T:
- "Just checking in..."
- "Wanted to follow up on our previous conversation"
- "Are you still interested?"
- "Let me know if you want to chat" (too vague)

# LENGTH
- Subject line: 6-8 words
- Email body: 100-150 words (3-4 short paragraphs)

# OUTPUT FORMAT

Return JSON:

{
  "subjectLine": "[Generate compelling 6-8 word subject line]",
  "emailBody": "[Generate email body]",
  "reasoning": "[Explain why this message will resonate]"
}

# EXAMPLE (DO NOT COPY, USE AS STYLE REFERENCE)

{
  "subjectLine": "Acme's Series B + ALPR for 15 cities",
  "emailBody": "Hi Sarah,\n\nI saw the exciting news about Acme's $12M Series B and your expansion into 15 new cities—congrats!\n\nWhen we last spoke in July, budget timing wasn't right. Given your growth plans and the vehicle theft challenges you mentioned, I'd love to revisit how DRN ALPR can scale with you across all locations.\n\nWe just published a case study from Metro Parking (similar 20-location setup) showing 68% reduction in theft within 90 days. I think you'd find it relevant.\n\nQuick 15-min call this week to see if there's a fit now?\n\nBest,\n[Your Name]",
  "reasoning": "This message works because: (1) References specific news (Series B + expansion), (2) Acknowledges original objection (budget), (3) Offers new proof (case study), (4) Low-friction CTA (15-min call). Conversational, not pushy."
}

# GENERATE EMAIL NOW
```

---

### Workflow Automation

**Salesforce Flow: Orchestrate Agent Actions**

#### Flow Name: `Lost_Opportunity_Reactivation_Workflow`

**Trigger:** Scheduled (Weekly, every Monday 9 AM)

**Flow Steps:**

```yaml
Step 1: Query Lost Opportunities
  Type: Get Records
  Object: Opportunity
  Filter:
    - StageName = "Closed Lost"
    - CloseDate >= LAST_N_DAYS:120
    - CloseDate <= LAST_N_DAYS:90
    - Amount > 50000
  Store in: $OpportunitiesList

Step 2: Loop Through Opportunities
  Type: Loop
  Collection: $OpportunitiesList
  Current Item: $CurrentOpportunity

  Step 2a: Call Agent Action "Analyze_Lost_Opportunities"
    Input:
      - opportunityId: $CurrentOpportunity.Id
    Output: $SignalsData

  Step 2b: Call Agent Action "Calculate_Reactivation_Score"
    Input:
      - opportunityId: $CurrentOpportunity.Id
      - signals: $SignalsData
    Output: $ScoringResult

  Step 2c: Decision - Check Tier
    Condition 1: $ScoringResult.tier = "URGENT"
      → Go to Step 2d (Urgent Path)

    Condition 2: $ScoringResult.tier = "HIGH PRIORITY"
      → Go to Step 2e (High Priority Path)

    Condition 3: $ScoringResult.tier = "MONITOR"
      → Go to Step 2f (Monitor Path)

    Default: $ScoringResult.tier = "DISQUALIFY"
      → Go to Step 2g (Disqualify Path)

  Step 2d: URGENT Path
    - Call Action: "Generate_Outreach_Message"
      Input: $ScoringResult, $SignalsData
      Output: $OutreachDraft

    - Call Action: "Send_Slack_Alert"
      Input: $CurrentOpportunity, $ScoringResult, $OutreachDraft

    - Call Action: "Create_Reactivation_Task"
      Input:
        - Priority: "High"
        - DueDate: TODAY
        - Subject: "URGENT REACTIVATION: {Account.Name} (Score: {score})"
        - Description: $OutreachDraft.emailBody

    - Update Opportunity:
        - Reactivation_Score__c = $ScoringResult.score
        - Reactivation_Tier__c = "URGENT"
        - Reactivation_Date__c = TODAY
        - Reactivation_Reasoning__c = $ScoringResult.reasoning

  Step 2e: HIGH PRIORITY Path
    - Call Action: "Generate_Outreach_Message"
      Input: $ScoringResult, $SignalsData
      Output: $OutreachDraft

    - Call Action: "Create_Reactivation_Task"
      Input:
        - Priority: "Normal"
        - DueDate: TODAY + 7 days
        - Subject: "HIGH PRIORITY REACTIVATION: {Account.Name}"
        - Description: $OutreachDraft.emailBody

    - Update Opportunity:
        - Reactivation_Score__c = $ScoringResult.score
        - Reactivation_Tier__c = "HIGH PRIORITY"
        - Reactivation_Date__c = TODAY

  Step 2f: MONITOR Path
    - Update Opportunity:
        - Reactivation_Score__c = $ScoringResult.score
        - Reactivation_Tier__c = "MONITOR"
        - Next_Review_Date__c = TODAY + 30 days

    - Add to Marketing Nurture Campaign:
        - Campaign: "Lost Opp Nurture - DRN"
        - Status: "Monitoring"

  Step 2g: DISQUALIFY Path
    - Update Opportunity:
        - Reactivation_Score__c = $ScoringResult.score
        - Reactivation_Tier__c = "DISQUALIFIED"
        - Reactivation_Notes__c = "No reactivation signals detected"

    - No action (archive)

Step 3: Send Summary Email to Sales Manager
  Type: Send Email
  To: Sales_Manager@motorolasolutions.com
  Subject: "Weekly Lost Opp Reactivation Report - {TODAY}"
  Body:
    """
    Weekly Lost Opportunity Reactivation Analysis Complete

    Opportunities Analyzed: {$OpportunitiesList.count}

    URGENT (Score 80-100): {$UrgentCount}
    → Action: Sales reps alerted via Slack + Task created (due today)

    HIGH PRIORITY (Score 60-79): {$HighPriorityCount}
    → Action: Task created (due within 7 days)

    MONITOR (Score 40-59): {$MonitorCount}
    → Action: Added to nurture campaign

    DISQUALIFIED (Score <40): {$DisqualifyCount}
    → Action: Archived

    Total Reactivation Potential: ${$TotalPipelineValue}

    View Report: [Link to Salesforce Dashboard]
    """
```

---

## PART III: DEPLOYMENT

### Implementation Roadmap

#### Week 1: Foundation (Days 1-7)

**Day 1-2: Data Audit & Preparation**
- [ ] Audit Opportunity data quality
  - Are Loss_Reason__c and Primary_Competitor__c fields populated?
  - Are CloseDate values accurate?
  - Test SOQL query for lost opps (90-120 days, >$50K)
- [ ] Audit Account/Contact data
  - Are key contacts still marked as Active?
  - Are Contact titles accurate?
- [ ] Create custom fields (if not exist):
  - Opportunity.Reactivation_Score__c (Number)
  - Opportunity.Reactivation_Tier__c (Picklist: URGENT, HIGH PRIORITY, MONITOR, DISQUALIFIED)
  - Opportunity.Reactivation_Date__c (Date)
  - Opportunity.Reactivation_Reasoning__c (Long Text)
  - Opportunity.Next_Review_Date__c (Date)

**Day 3-4: External Integrations Setup**
- [ ] LinkedIn Sales Navigator:
  - Install Salesforce app from AppExchange
  - Connect LinkedIn Sales Navigator Team account
  - Map Accounts to LinkedIn Company Pages
  - Enable alerts for executive changes
- [ ] Bombora Intent Data:
  - Install Bombora connector (Data Cloud)
  - Configure intent topics (ALPR, vehicle security, etc.)
  - Set surge threshold (≥75 = alert)
- [ ] Website Analytics:
  - Verify GA4 tracking on DRN website
  - Create custom object: `Website_Activity__c`
  - Set up Zapier: GA4 → Salesforce sync
- [ ] News Monitoring:
  - Create Google Alerts (account names + industry keywords)
  - Set up Zapier: Google Alerts → Salesforce Task
- [ ] Crunchbase (Optional for POC):
  - Subscribe to API or manual monitoring
  - Create custom object: `Funding_Event__c`

**Day 5-7: Agent Builder Configuration**
- [ ] Create Agent in Salesforce Agent Builder
  - Name: "Lost Opportunity Reactivation Agent"
  - Type: Service Agent (Autonomous)
- [ ] Configure Agent Instructions (Atlas system prompt)
  - Copy system prompt from [Atlas Reasoning Engine Prompts](#atlas-reasoning-engine-prompts)
  - Customize for DRN context (industry, buyer personas)
- [ ] Connect Data Sources
  - Add Opportunity, Account, Contact objects
  - Add custom objects (LinkedIn_Update__c, Bombora_Intent__c, etc.)
- [ ] Build Apex Actions (if needed):
  - `AnalyzeLostOpportunitiesAction.cls`
  - `CalculateReactivationScoreAction.cls`
- [ ] Configure Agent Actions
  - Analyze_Lost_Opportunities
  - Calculate_Reactivation_Score
  - Generate_Outreach_Message
  - Create_Reactivation_Task
  - Send_Slack_Alert

---

#### Week 2: Testing & Refinement (Days 8-14)

**Day 8-10: Manual Testing**
- [ ] Select 10 test opportunities (known lost deals from 90-120 days ago)
- [ ] Manually gather signals for each (LinkedIn, news, website)
- [ ] Run agent scoring for all 10
- [ ] Compare agent scores to manual assessment (accuracy check)
- [ ] Review generated outreach messages (quality check)
- [ ] Adjust scoring weights if needed

**Day 11-12: Automated Testing**
- [ ] Build Salesforce Flow: `Lost_Opportunity_Reactivation_Workflow`
- [ ] Test flow with 50 opportunities (batch test)
- [ ] Verify:
  - Opportunities scored correctly
  - Tasks created for URGENT/HIGH PRIORITY
  - Slack alerts sent for URGENT (score 80-100)
  - Nurture campaign adds for MONITOR
  - No action for DISQUALIFIED
- [ ] Check for errors in debug logs

**Day 13-14: Stakeholder Review**
- [ ] Present results to sales team (show scored opportunities)
- [ ] Demo: How reps receive alerts + tasks
- [ ] Gather feedback:
  - Are scores accurate? (do high scores match rep intuition?)
  - Are outreach messages compelling? (would reps send these?)
  - Any false positives/negatives?
- [ ] Refine based on feedback

---

#### Week 3-4: Pilot Launch (Days 15-30)

**Day 15: Pilot Kickoff**
- [ ] Select pilot group (5-10 sales reps, 1 sales manager)
- [ ] Training session (1 hour):
  - How agent works (scoring model, signal taxonomy)
  - How to interpret scores and tiers
  - How to act on URGENT vs HIGH PRIORITY tasks
  - How to provide feedback (this helps agent learn)
- [ ] Activate Flow: Schedule weekly run (every Monday 9 AM)

**Days 16-30: Pilot Monitoring**
- [ ] Week 1: Daily check-ins with pilot reps
  - Are alerts arriving?
  - Are scores making sense?
  - Any blockers?
- [ ] Week 2: Mid-pilot review
  - Analyze results:
    - How many URGENT leads identified?
    - How many reps contacted?
    - How many prospects responded?
  - Adjust scoring if needed (too strict? too lenient?)
- [ ] Week 3: Expansion planning
  - If pilot successful, plan full rollout
  - If issues, refine and extend pilot

**Day 30 Checkpoint:**
✅ Agent running autonomously (weekly)
✅ 100+ opportunities scored
✅ 10-20 URGENT leads identified
✅ 5-10 sales conversations resumed
✅ $500K-$1M pipeline reactivated
✅ Stakeholder buy-in for full deployment

---

### Testing & Validation

**How to validate agent accuracy:**

#### Test 1: Historical Validation (Backtesting)

**Goal:** Prove the agent would have predicted ACTUAL reactivations

**Method:**
1. Identify 20 opportunities that were:
   - Closed-Lost 6-12 months ago
   - Later reactivated and won (we have ground truth)
2. Re-run agent scoring using signals from 120 days post-close
3. Check: Did agent score these high (80-100)?

**Expected Result:**
- Agent should score 80-100 for 70%+ of actual reactivations (high recall)
- Agent should score <40 for opportunities that stayed lost (high precision)

**Success Criteria:**
- Precision: >60% (of URGENT leads, 60% should reactivate)
- Recall: >70% (of actual reactivations, agent should flag 70%)

---

#### Test 2: Sales Rep Validation (Human-in-the-Loop)

**Goal:** Validate that high scores match rep intuition

**Method:**
1. Agent scores 50 lost opportunities
2. Sort by score (highest to lowest)
3. Show TOP 10 to sales manager (blind - don't show scores)
4. Ask: "Which of these do you think could be reactivated?"
5. Compare manager picks to agent scores

**Expected Result:**
- Manager should pick 7-8 of the TOP 10 agent-scored opportunities
- If manager disagrees, investigate: What signal did agent miss? Or did manager have insider knowledge agent couldn't access?

**Success Criteria:**
- 70%+ agreement between agent and experienced sales manager

---

#### Test 3: A/B Testing (Gold Standard)

**Goal:** Prove agent-driven reactivation outperforms manual

**Method:**
1. Split 100 lost opportunities into 2 groups:
   - **Group A (Agent-Driven):** Use agent scoring, prioritize URGENT/HIGH
   - **Group B (Manual):** Reps review and prioritize themselves
2. Track results for 60 days:
   - Response rate (% who reply)
   - Reactivation rate (% who re-open opportunity)
   - Pipeline value reactivated

**Expected Result:**
- Agent-driven should have 2-3x higher response rate
- Agent-driven should have 2x higher reactivation rate

**Success Criteria:**
- Agent-driven Group A outperforms Manual Group B by 50%+

---

### Success Metrics

**How to measure POC success:**

#### Primary Metrics (60-Day POC)

| Metric | Target (Conservative) | Stretch Goal |
|--------|----------------------|--------------|
| **Opportunities Analyzed** | 200-300 | 400+ |
| **URGENT Leads (Score 80-100)** | 40-60 | 80+ |
| **Response Rate** | 15-20% | 25%+ |
| **Reactivation Rate** | 10-15% | 20%+ |
| **Pipeline Reactivated** | $2M-$3M | $5M+ |
| **Expected Closes (90 days)** | 3-5 deals | 8-10 deals |
| **Expected Revenue (90 days)** | $300K-$500K | $800K-$1M |

#### Secondary Metrics (Efficiency)

| Metric | Target | Calculation |
|--------|--------|-------------|
| **Rep Time Saved** | 10 hours/week | Manual review time - Agent time |
| **Lead Quality** | 3x improvement | Agent URGENT response rate ÷ Random lost opp response rate |
| **Forecast Accuracy** | +40% | Agent-predicted reactivations vs actual |

#### Tertiary Metrics (Learning)

| Metric | Target | Why It Matters |
|--------|--------|----------------|
| **Signal Accuracy** | 80%+ | Which signals truly predict reactivation? |
| **Score Calibration** | 90%+ | Are scores 80-100 actually reactivating at high rates? |
| **Agent Trust** | 70%+ | % of reps who follow agent recommendations |

---

### Troubleshooting Guide

**Common issues and solutions:**

#### Issue 1: Agent Scores Are Too Low (No URGENT leads)

**Symptoms:**
- All opportunities score <60
- No URGENT alerts generated

**Diagnosis:**
- Scoring model is too strict
- External data sources not connected (missing signals)

**Solutions:**
1. Check data integrations:
   - Is LinkedIn syncing? (verify LinkedIn_Update__c has records)
   - Is Bombora syncing? (verify Bombora_Intent__c has records)
2. Adjust scoring weights (lower thresholds):
   - Reduce required points for URGENT from 80 to 70
3. Add more signal sources:
   - Enable website tracking
   - Add news monitoring

---

#### Issue 2: Agent Scores Are Too High (Too many false positives)

**Symptoms:**
- 50%+ of opportunities score URGENT
- Reps say "these aren't actually good leads"

**Diagnosis:**
- Scoring model is too lenient
- Signals are not predictive (noise, not signal)

**Solutions:**
1. Tighten scoring:
   - Increase URGENT threshold from 80 to 85
   - Reduce points for weak signals (e.g., blog post visit = 0, was +2)
2. Add negative adjustments:
   - Champion left company: -15 points
   - Competitor contract signed: -20 points
3. Require multi-signal convergence:
   - URGENT tier requires 2+ categories with points (not just 1 big signal)

---

#### Issue 3: Outreach Messages Are Generic

**Symptoms:**
- Generated emails say "just checking in" (not specific)
- Reps rewrite every message (agent not saving time)

**Diagnosis:**
- Atlas prompt template is too vague
- Agent not accessing signal details (only summary)

**Solutions:**
1. Improve Atlas prompt:
   - Add examples of GOOD vs BAD messages
   - Require specific signal reference in first sentence
2. Pass more context to prompt:
   - Include full signal details (not just summary)
   - Include original loss reason (acknowledge objection)
3. Add message quality scoring:
   - Agent self-evaluates: "Does this message reference specific signal? Y/N"
   - If N, regenerate

---

#### Issue 4: Data Quality Issues

**Symptoms:**
- Agent can't find contacts (no email)
- Loss reasons are blank (can't address objection)

**Diagnosis:**
- Salesforce data incomplete

**Solutions:**
1. Data cleanup:
   - Backfill Loss_Reason__c for all lost opps (mandatory field going forward)
   - Backfill Contact emails (use ZoomInfo to enrich)
2. Prevent future gaps:
   - Make Loss_Reason__c required field on Opportunity close
   - Validation rule: "Must have 1+ Contact with email before closing opp"

---

#### Issue 5: Reps Aren't Acting on Alerts

**Symptoms:**
- URGENT tasks created but not completed
- Slack alerts ignored

**Diagnosis:**
- Reps don't trust agent yet (change management issue)
- Too many alerts (alert fatigue)

**Solutions:**
1. Executive sponsorship:
   - Sales VP sends email: "Trust the agent, these are high-quality leads"
   - Make task completion a KPI (tracked in weekly 1:1s)
2. Reduce alert volume:
   - Only alert for score 85+ (not 80+)
   - Only alert if 2+ signals present
3. Show proof:
   - Share wins: "Rep X contacted agent-flagged lead, closed $150K deal in 30 days"
   - Competitive pressure: Leaderboard of "agent-driven reactivations"

---

## CONCLUSION

**This playbook provides everything needed to deploy the Lost Opportunity Reactivation Agent at Motorola DRN within 30 days.**

**Key Success Factors:**
1. **Data Quality:** Agent is only as good as the data it receives (garbage in, garbage out)
2. **Integration Completeness:** Connect ALL signal sources (LinkedIn, Bombora, website, news)
3. **Scoring Calibration:** Adjust weights based on YOUR historical patterns (not generic)
4. **Change Management:** Get sales team buy-in (exec sponsorship critical)
5. **Continuous Learning:** Track outcomes, feed back to model, improve over time

**Expected 60-Day POC Impact:**
- **$2M-$3M** pipeline reactivated
- **15-20%** reactivation rate (3x manual baseline)
- **$300K-$500K** revenue (assuming 30% close rate)
- **37.5x ROI** (POC investment: $8K)

**Next Steps:**
1. Complete Week 1 setup (data audit + integrations)
2. Build and test agent (Week 2)
3. Pilot with 5-10 reps (Weeks 3-4)
4. Full deployment (if successful)

**This agent alone will validate ARI Layer 6 (Revenue Velocity Intelligence) and demonstrate AI-native revenue optimization to Motorola leadership.**

---

**Questions? Refer to:**
- [ARI Framework Complete Documentation](ARI_FRAMEWORK_COMPLETE.md)
- [CAIO Training Master Curriculum](CAIO_TRAINING_MASTER_CURRICULUM.md)
- Salesforce Agentforce Documentation: https://help.salesforce.com/agentforce

**Author:** Noel Pena
**Email:** [Your Email]
**Version:** 1.0
**Last Updated:** October 2025

---

**© 2025 Noel Pena. Proprietary & Confidential.**
**Autonomous Revenue Intelligence™ is a trademark of Noel Pena.**

**END OF PLAYBOOK**
