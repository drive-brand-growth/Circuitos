# METROFLEX EVENTS AI AGENT - WORKFLOW DIAGRAMS

## 🎨 MERMAID DIAGRAMS

### **DIAGRAM 1: COMPLETE SYSTEM ARCHITECTURE**

```mermaid
graph TB
    subgraph "DATA SOURCES"
        IG[Instagram<br/>#NPCTexas, #TexasBodybuilding]
        FB[Facebook<br/>Competitor Event Pages]
        NPC[NPC Website<br/>Results Pages]
    end

    subgraph "SCRAPING LAYER"
        APIFY[Apify Scrapers<br/>$49/mo]
    end

    subgraph "AUTOMATION ENGINE - n8n Cloud $20/mo"
        WEBHOOK[Webhook Trigger<br/>Receive from Apify]
        PARSE[Parse JSON Data<br/>Clean & Structure]
        LOOP[Loop Through Profiles<br/>Process 500x]
        BUILD[Build AI Prompt<br/>Personalized per athlete]
        CLAUDE[Call Claude API<br/>$0.01 per profile]
        ANALYZE[Parse AI Response<br/>Extract JSON data]
        FILTER{Filter<br/>Score > 40?}
        FORMAT[Format for GHL<br/>Map fields + tags]
        LOG[Log Rejected<br/>For analysis]
    end

    subgraph "AI ANALYSIS"
        CLAUDEAPI[Claude 3.5 Sonnet API<br/>Anthropic - $15-50/mo]
    end

    subgraph "CRM & OUTREACH"
        GHL[GoHighLevel CRM<br/>$97-297/mo]
        EMAIL[Email Campaigns<br/>5-7 touch sequence]
        SMS[SMS Campaigns<br/>Urgency triggers]
        DM[Instagram DMs<br/>ManyChat $15/mo optional]
    end

    subgraph "CONVERSION"
        REG[Athlete Registers<br/>RegFox/Web Connex]
        TIX[Spectators Buy Tickets<br/>Ticket Spice]
        REV[$$$<br/>Revenue Generated]
    end

    IG --> APIFY
    FB --> APIFY
    NPC --> APIFY

    APIFY -->|Webhook| WEBHOOK
    WEBHOOK --> PARSE
    PARSE --> LOOP
    LOOP --> BUILD
    BUILD --> CLAUDE
    CLAUDE -->|API Call| CLAUDEAPI
    CLAUDEAPI -->|Response| ANALYZE
    ANALYZE --> FILTER

    FILTER -->|YES<br/>Qualified| FORMAT
    FILTER -->|NO<br/>Rejected| LOG

    FORMAT --> GHL
    GHL --> EMAIL
    GHL --> SMS
    GHL --> DM

    EMAIL --> REG
    SMS --> REG
    DM --> REG

    EMAIL --> TIX
    SMS --> TIX

    REG --> REV
    TIX --> REV

    LOG -.->|Analytics| LOOP

    style APIFY fill:#FF6B6B,stroke:#333,stroke-width:2px,color:#fff
    style WEBHOOK fill:#4ECDC4,stroke:#333,stroke-width:2px,color:#fff
    style CLAUDEAPI fill:#FFE66D,stroke:#333,stroke-width:2px,color:#333
    style GHL fill:#A8E6CF,stroke:#333,stroke-width:2px,color:#333
    style REV fill:#95E1D3,stroke:#333,stroke-width:4px,color:#333
```

---

### **DIAGRAM 2: DETAILED n8n WORKFLOW**

```mermaid
flowchart TD
    START([Apify Scraper Runs<br/>Weekly: Sunday 9am])
    START --> SCRAPE[Scrape Instagram<br/>Hashtags: #NPCTexas<br/>Results: 500 profiles]

    SCRAPE --> WEBHOOK[n8n Webhook Trigger<br/>Receives JSON payload]

    WEBHOOK --> PARSE[Parse Apify Data<br/>Extract: username, bio,<br/>followers, posts, location]

    PARSE --> LOOP{Split In Batches<br/>Process 1 at a time}

    LOOP --> PROFILE1[Profile #1]
    PROFILE1 --> PROMPT1[Build Claude Prompt<br/>Include: bio, followers,<br/>recent posts, location]

    PROMPT1 --> API1[HTTP Request<br/>POST to Claude API<br/>Model: claude-3.5-sonnet]

    API1 --> RESPONSE1[Claude Analyzes:<br/>- Is NPC competitor?<br/>- Division & experience<br/>- Recruitment score 0-100<br/>- Personalized message]

    RESPONSE1 --> PARSE_AI1[Parse JSON Response<br/>Extract all fields]

    PARSE_AI1 --> CHECK1{Recruitment<br/>Potential >= 40?}

    CHECK1 -->|YES| QUALIFIED1[Format for GHL<br/>Map to custom fields<br/>Add tags]
    CHECK1 -->|NO| REJECT1[Log as Rejected<br/>Store reason]

    QUALIFIED1 --> GHL1[Send to GHL Webhook<br/>Create/Update Contact]

    GHL1 --> CAMPAIGN1[GHL Auto-Triggers<br/>Email Campaign]

    REJECT1 --> NEXT1[Next Profile]
    CAMPAIGN1 --> NEXT1

    NEXT1 --> LOOP

    LOOP -->|All Done| SUMMARY[Workflow Summary<br/>Total: 500 processed<br/>Qualified: 180<br/>Rejected: 320]

    SUMMARY --> END([End - Wait for Next Week])

    style START fill:#667eea,stroke:#333,stroke-width:2px,color:#fff
    style SCRAPE fill:#f093fb,stroke:#333,stroke-width:2px,color:#fff
    style API1 fill:#fad961,stroke:#333,stroke-width:2px,color:#333
    style RESPONSE1 fill:#96e6a1,stroke:#333,stroke-width:2px,color:#333
    style GHL1 fill:#a8edea,stroke:#333,stroke-width:2px,color:#333
    style CAMPAIGN1 fill:#fed6e3,stroke:#333,stroke-width:2px,color:#333
    style SUMMARY fill:#c3cfe2,stroke:#333,stroke-width:2px,color:#333
    style END fill:#667eea,stroke:#333,stroke-width:2px,color:#fff
```

---

### **DIAGRAM 3: ATHLETE JOURNEY FLOW**

```mermaid
journey
    title Athlete Journey - From Scrape to Registration
    section Discovery
      Profile scraped from Instagram: 3: Apify
      AI analyzes profile: 5: Claude
      Scored as high potential: 5: n8n
      Added to GHL CRM: 5: GHL
    section Outreach
      Receives personalized email: 4: GHL
      Opens email (40% rate): 4: Athlete
      Clicks registration link: 4: Athlete
      Visits landing page: 3: Athlete
    section Consideration
      Reads event details: 3: Athlete
      Sees early bird discount: 4: GHL
      Receives SMS reminder: 4: GHL
      Checks competitor reviews: 2: Athlete
    section Conversion
      Decides to register: 5: Athlete
      Fills RegFox form: 3: Athlete
      Completes payment: 5: Athlete
      Receives confirmation: 5: GHL
    section Post-Registration
      Gets welcome sequence: 5: GHL
      Joins Facebook group: 4: Athlete
      Shares on Instagram: 5: Athlete
      Refers 2 friends: 5: Athlete
```

---

### **DIAGRAM 4: DATA FLOW & TRANSFORMATION**

```mermaid
graph LR
    subgraph "Stage 1: Raw Data"
        RAW[Instagram Profile<br/>Raw JSON from Apify]
    end

    subgraph "Stage 2: Cleaned Data"
        CLEAN[Cleaned Profile<br/>username: johnsmith_fitness<br/>followers: 5200<br/>bio: IFBB Pro Dallas TX<br/>posts: 847]
    end

    subgraph "Stage 3: AI Enrichment"
        ENRICH[AI-Enriched Profile<br/>isNPCCompetitor: true<br/>division: Men's Physique<br/>experienceLevel: Advanced<br/>location: Dallas, TX<br/>recruitmentPotential: 85<br/>personalizedMessage: Hey John...]
    end

    subgraph "Stage 4: GHL Format"
        GHL_DATA[GHL Contact<br/>firstName: John<br/>lastName: Smith<br/>customFields:<br/>  instagram_username<br/>  division<br/>  recruitment_score<br/>tags: NPC_Competitor,<br/>  Priority_High,<br/>  Location_Dallas]
    end

    subgraph "Stage 5: Campaign Data"
        CAMPAIGN[Campaign Variables<br/>{{ firstName }} = John<br/>{{ personalizedMessage }}<br/>{{ registrationLink }}<br/>{{ earlyBirdDiscount }}]
    end

    RAW -->|n8n Parse Node| CLEAN
    CLEAN -->|n8n + Claude API| ENRICH
    ENRICH -->|n8n Format Node| GHL_DATA
    GHL_DATA -->|GHL Workflow| CAMPAIGN

    style RAW fill:#ff9a9e,stroke:#333,stroke-width:2px
    style CLEAN fill:#fad0c4,stroke:#333,stroke-width:2px
    style ENRICH fill:#ffecd2,stroke:#333,stroke-width:2px
    style GHL_DATA fill:#a1c4fd,stroke:#333,stroke-width:2px
    style CAMPAIGN fill:#c2e9fb,stroke:#333,stroke-width:2px
```

---

### **DIAGRAM 5: COST vs VOLUME SCALING**

```mermaid
graph TD
    subgraph "Month 1-3: MVP"
        M1[500 profiles/month<br/>Cost: $84/mo<br/>Qualified: 150<br/>Registered: 10<br/>Revenue: $1,200<br/>ROI: 1,329%]
    end

    subgraph "Month 4-6: Scale"
        M4[2,000 profiles/month<br/>Cost: $134/mo<br/>Qualified: 600<br/>Registered: 30<br/>Revenue: $3,600<br/>ROI: 2,587%]
    end

    subgraph "Month 7-12: Optimize"
        M7[5,000 profiles/month<br/>Cost: $204/mo<br/>Qualified: 1,500<br/>Registered: 75<br/>Revenue: $9,000<br/>ROI: 4,312%]
    end

    M1 -->|Add ManyChat<br/>+$15/mo| M4
    M4 -->|Add Apify credits<br/>+$50/mo| M7

    style M1 fill:#ffeaa7,stroke:#333,stroke-width:2px
    style M4 fill:#fdcb6e,stroke:#333,stroke-width:2px
    style M7 fill:#e17055,stroke:#333,stroke-width:2px,color:#fff
```

---

### **DIAGRAM 6: DECISION TREE - ATHLETE QUALIFICATION**

```mermaid
graph TD
    START[Instagram Profile Scraped]

    START --> Q1{Bio mentions<br/>NPC, bodybuilding,<br/>or competing?}

    Q1 -->|NO| REJECT1[Reject: Not a competitor<br/>Score: 0-20]
    Q1 -->|YES| Q2{Location in<br/>Texas or<br/>nearby states?}

    Q2 -->|NO| REJECT2[Reject: Too far<br/>Score: 20-35]
    Q2 -->|YES| Q3{Follower count?}

    Q3 -->|<500| LOW[Low Influence<br/>Score: +10]
    Q3 -->|500-5K| MED[Medium Influence<br/>Score: +20]
    Q3 -->|>5K| HIGH[High Influence<br/>Score: +30]

    LOW --> Q4{Recent posts<br/>show prep or<br/>competition?}
    MED --> Q4
    HIGH --> Q4

    Q4 -->|NO| INACTIVE[Off-Season/Inactive<br/>Score: +5]
    Q4 -->|YES| ACTIVE[Active Competitor<br/>Score: +25]

    INACTIVE --> Q5{Division<br/>identified?}
    ACTIVE --> Q5

    Q5 -->|Unknown| FINAL1[Base Score Only]
    Q5 -->|Bikini/Physique| FINAL2[Popular Division<br/>Score: +10]
    Q5 -->|Bodybuilding| FINAL3[Core Division<br/>Score: +15]

    FINAL1 --> CALC[Calculate Total Score]
    FINAL2 --> CALC
    FINAL3 --> CALC

    CALC --> DECISION{Total Score?}

    DECISION -->|0-39| REJECT_FINAL[REJECT<br/>Log & Skip]
    DECISION -->|40-74| MEDIUM_PRI[MEDIUM PRIORITY<br/>Nurture Campaign]
    DECISION -->|75-100| HIGH_PRI[HIGH PRIORITY<br/>Immediate Outreach]

    REJECT1 --> LOG[Log to Analytics]
    REJECT2 --> LOG
    REJECT_FINAL --> LOG

    MEDIUM_PRI --> GHL[Send to GHL]
    HIGH_PRI --> GHL

    style START fill:#74b9ff,stroke:#333,stroke-width:2px,color:#333
    style REJECT_FINAL fill:#ff7675,stroke:#333,stroke-width:2px,color:#fff
    style MEDIUM_PRI fill:#ffeaa7,stroke:#333,stroke-width:2px,color:#333
    style HIGH_PRI fill:#55efc4,stroke:#333,stroke-width:2px,color:#333
    style GHL fill:#a29bfe,stroke:#333,stroke-width:2px,color:#fff
```

---

### **DIAGRAM 7: COMPETITOR INTELLIGENCE WORKFLOW**

```mermaid
sequenceDiagram
    participant Apify as Apify Scraper
    participant n8n as n8n Workflow
    participant Competitor as Competitor Show<br/>Instagram/Facebook
    participant Claude as Claude AI
    participant DB as Database<br/>(GHL)
    participant Alert as Alert System

    Note over Apify,Competitor: Weekly Scraping Cycle

    Apify->>Competitor: Scrape event page<br/>Extract attendee list
    Competitor-->>Apify: Return 300 profiles

    Apify->>n8n: Send webhook<br/>with profile data

    loop For each profile
        n8n->>Claude: Analyze profile<br/>Is this our target?
        Claude-->>n8n: Yes: Score 85<br/>Division: Bikini<br/>Location: Dallas

        n8n->>DB: Check if already<br/>in our database

        alt New prospect
            n8n->>DB: Add new contact<br/>Tag: Competitor_Show_Attendee
            n8n->>Alert: Notify: New high-value<br/>competitor found
        else Existing contact
            n8n->>DB: Update: Attended<br/>competitor show
            n8n->>Alert: Notify: Our athlete<br/>went to competitor
        end
    end

    n8n->>DB: Generate report:<br/>Competitor intelligence
    DB-->>Alert: Send weekly digest
```

---

### **DIAGRAM 8: SYSTEM MONITORING DASHBOARD**

```mermaid
graph TB
    subgraph "Real-Time Metrics"
        M1[Profiles Scraped Today: 127]
        M2[Qualified Athletes: 38]
        M3[Added to GHL: 38]
        M4[Campaigns Triggered: 38]
    end

    subgraph "Weekly Performance"
        W1[Total Scraped: 489]
        W2[Qualification Rate: 37%]
        W3[Email Open Rate: 42%]
        W4[Click Rate: 18%]
        W5[Registration Rate: 3.2%]
    end

    subgraph "Cost Tracking"
        C1[n8n: $20/mo<br/>92% under limit]
        C2[Apify: $49/mo<br/>4,200/10,000 credits]
        C3[Claude: $18.43/mo<br/>2,147 profiles analyzed]
        C4[Total: $87.43/mo]
    end

    subgraph "ROI Metrics"
        R1[Athletes Registered: 16]
        R2[Revenue Generated: $1,920]
        R3[Cost Per Acquisition: $5.46]
        R4[ROI: 2,096%]
    end

    subgraph "Alerts"
        A1[⚠️ Competitor dropped<br/>prices by $20]
        A2[✅ All systems operational]
        A3[🎯 15 high-potential<br/>athletes this week]
    end

    M1 --> W1
    M2 --> W2
    W3 --> R1
    R1 --> R2
    C4 --> R3
    R2 --> R4

    style M1 fill:#00b894,stroke:#333,stroke-width:2px,color:#fff
    style M2 fill:#00b894,stroke:#333,stroke-width:2px,color:#fff
    style W2 fill:#fdcb6e,stroke:#333,stroke-width:2px
    style W3 fill:#fdcb6e,stroke:#333,stroke-width:2px
    style R4 fill:#55efc4,stroke:#333,stroke-width:3px,color:#333
    style A1 fill:#ff7675,stroke:#333,stroke-width:2px,color:#fff
    style A2 fill:#00b894,stroke:#333,stroke-width:2px,color:#fff
    style A3 fill:#74b9ff,stroke:#333,stroke-width:2px,color:#fff
```

---

## 📊 DIAGRAM USAGE GUIDE

### **How to Use These Diagrams:**

1. **Diagram 1 - System Architecture**: Show to stakeholders for high-level overview
2. **Diagram 2 - n8n Workflow**: Technical reference for building/debugging
3. **Diagram 3 - Athlete Journey**: Understand user experience, optimize touchpoints
4. **Diagram 4 - Data Flow**: Understand data transformations at each stage
5. **Diagram 5 - Scaling**: Plan budget as you grow
6. **Diagram 6 - Decision Tree**: Understand AI qualification logic
7. **Diagram 7 - Competitor Intelligence**: Advanced feature for Phase 2
8. **Diagram 8 - Monitoring**: Build dashboard to track performance

### **Viewing Diagrams:**

These Mermaid diagrams render in:
- ✅ GitHub (native support)
- ✅ GitLab (native support)
- ✅ VS Code (with Mermaid extension)
- ✅ Notion (with /embed)
- ✅ Obsidian (native support)
- ✅ Mermaid Live Editor: https://mermaid.live

### **Exporting Diagrams:**

**As PNG/SVG:**
1. Copy diagram code
2. Go to https://mermaid.live
3. Paste code
4. Click "Export" → PNG or SVG
5. Use in presentations, documentation

**As PDF:**
1. Export as SVG first
2. Open in browser
3. Print to PDF

---

## 🎯 KEY TAKEAWAYS FROM DIAGRAMS

### **From System Architecture (Diagram 1):**
- 4 core tools: Apify → n8n → Claude → GHL
- Data flows one direction (scrape → analyze → store → outreach)
- Multiple revenue streams (athlete registration + ticket sales)
- Cost: $84-119/mo | Revenue: $1,200-2,400/mo

### **From n8n Workflow (Diagram 2):**
- Runs weekly (Sunday 9am)
- Processes 500 profiles in ~30 minutes
- Claude analyzes each profile ($0.01 per athlete)
- 30-40% qualify and go to GHL
- Automatic campaign triggering

### **From Athlete Journey (Diagram 3):**
- Discovery → Outreach → Consideration → Conversion
- Multiple touchpoints needed (email + SMS + DM)
- 40% open rate → 18% click rate → 3% conversion
- Post-registration advocacy (athlete shares & refers)

### **From Scaling (Diagram 5):**
- Start small: 500/mo ($84)
- Scale to 2,000/mo ($134) after 3 months
- Optimize to 5,000/mo ($204) by month 7
- ROI improves as you scale (1,329% → 4,312%)

---

## 📋 IMPLEMENTATION CHECKLIST

Using these diagrams as reference:

### **Phase 1: Setup (Week 1)**
- [ ] Sign up for all 4 tools (n8n, Apify, Claude, GHL)
- [ ] Import n8n workflow JSON
- [ ] Configure Apify Instagram scraper
- [ ] Set up GHL custom fields & tags
- [ ] Test end-to-end with 10 profiles

### **Phase 2: Launch (Week 2)**
- [ ] Schedule Apify scraper (weekly)
- [ ] Activate n8n workflow
- [ ] Monitor first batch (500 profiles)
- [ ] Verify GHL receives data correctly
- [ ] Check campaign triggers

### **Phase 3: Optimize (Weeks 3-4)**
- [ ] Analyze qualification rate (target: 30-40%)
- [ ] Review Claude scoring accuracy
- [ ] Adjust filters if needed
- [ ] Monitor costs vs projections
- [ ] Measure first conversions

### **Phase 4: Scale (Month 2-3)**
- [ ] Increase scraping frequency (bi-weekly)
- [ ] Add more hashtags/data sources
- [ ] Improve email copy based on results
- [ ] Add SMS sequences
- [ ] Consider ManyChat for DMs

**You're ready to build! Use these diagrams as your blueprint. 🚀**
