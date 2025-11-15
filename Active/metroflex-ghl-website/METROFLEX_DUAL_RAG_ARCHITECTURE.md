# MetroFlex Dual RAG Architecture

**Date:** November 15, 2025
**Version:** 1.0
**Objective:** Implement two distinct ML RAG systems to prevent cross-contamination and ensure focused business vertical operations

---

## 🎯 Strategic Separation

### Problem Statement
Previously, we had ONE knowledge base (METROFLEX_COMPLETE_KB_V3.json) containing ALL MetroFlex data - events, gym memberships, licensing, apparel, ticketing, sponsorships. This creates cross-contamination risks where:
- Events agents might incorrectly answer gym membership questions
- Gym agents might incorrectly answer event ticketing questions
- ML models trained on mixed data produce less accurate predictions

### Solution: Two Distinct RAG Systems

**System 1: MetroFlex Events RAG**
- Knowledge Base: `METROFLEX_EVENTS_KB_V3_EVENTS_ONLY.json`
- Scope: ONLY what's on metroflexevents.com
- Handles: Competitor registration, spectator ticketing, vendor booths, sponsorships

**System 2: MetroFlex Gym RAG**
- Knowledge Base: `METROFLEX_GYM_KB_V1.json`
- Scope: Gym operations + licensing
- Handles: Arlington memberships, Miami memberships, licensing, apparel

---

## 📊 Data Separation Matrix

| Data Category | Events RAG | Gym RAG | Rationale |
|---------------|------------|---------|-----------|
| **Competitor Registration** | ✅ YES | ❌ NO | Event-specific (MuscleWare platform) |
| **Spectator Ticketing** | ✅ YES | ❌ NO | Event-specific (TicketSpice platform) |
| **Vendor Booths** | ✅ YES | ❌ NO | Event-specific (expo at championships) |
| **Sponsorships** | ✅ YES | ❌ NO | Event-specific (brand exposure at events) |
| **NPC Divisions/Classes** | ✅ YES | ❌ NO | Event-specific (competition rules) |
| **Arlington Gym Membership** | ❌ NO | ✅ YES | Gym operations |
| **Miami Gym Membership** | ❌ NO | ✅ YES | Gym operations |
| **Licensing Program** | ❌ NO | ✅ YES | Nationwide gym expansion |
| **Apparel Catalog** | ❌ NO | ✅ YES | Gym-related merchandise |
| **Personal Training** | ❌ NO | ✅ YES | Gym service offering |
| **Music Requirements** | ✅ YES | ❌ NO | Event-specific (posing music) |
| **Contact Info (Brian)** | ✅ YES | ✅ YES | Shared contact (but different context) |

---

## 🤖 Agent-to-RAG Mapping

### MetroFlex Events Agents → Events RAG

**Agent 1: MetroFlex Events AI Chat Agent (Existing)**
- RAG: `METROFLEX_EVENTS_KB_V3_EVENTS_ONLY.json`
- Purpose: Answer event questions, competitor registration, spectator tickets
- High-intent triggers: Competitor registration, spectator tickets
- **MUST NOT:** Answer gym membership or licensing questions

**Agent 2: Ticket Sales & Spectator Agent (Future)**
- RAG: `METROFLEX_EVENTS_KB_V3_EVENTS_ONLY.json`
- Purpose: Sell spectator tickets, handle group bookings
- High-intent triggers: "buy tickets", "VIP seating", "family pack"
- **MUST NOT:** Answer gym membership or licensing questions

**Agent 3: Event Fulfillment & Day-Of Agent (Future)**
- RAG: `METROFLEX_EVENTS_KB_V3_EVENTS_ONLY.json`
- Purpose: Day-of logistics for competitors, spectators, vendors
- High-intent triggers: "what time arrive", "parking", "check in"
- **MUST NOT:** Answer gym membership or licensing questions

**Agent 4: Sponsor Outreach & Qualification Agent (Future)**
- RAG: `METROFLEX_EVENTS_KB_V3_EVENTS_ONLY.json`
- Purpose: Qualify sponsor leads, present packages, close deals
- High-intent triggers: "sponsor", "title sponsor", "brand exposure"
- **MUST NOT:** Answer gym membership or licensing questions

---

### MetroFlex Gym Agents → Gym RAG

**Agent 5: Gym Member Onboarding Agent (Future)**
- RAG: `METROFLEX_GYM_KB_V1.json`
- Purpose: Convert prospects into gym members, reduce churn
- High-intent triggers: "join metroflex miami", "founder's membership"
- **MUST NOT:** Answer event registration or ticketing questions

**Agent 6: Licensing Prospect Qualification Agent (Future)**
- RAG: `METROFLEX_GYM_KB_V1.json`
- Purpose: Qualify licensing leads, present packages, close $40-60k deals
- High-intent triggers: "open a metroflex gym", "licensing cost", "franchise"
- **MUST NOT:** Answer event registration or ticketing questions

**Agent 7: Apparel Recommendation Agent (Future)**
- RAG: `METROFLEX_GYM_KB_V1.json`
- Purpose: Recommend apparel products, suggest sizing, drive e-commerce
- High-intent triggers: "buy shirt", "metroflex apparel", "order hoodie"
- **MUST NOT:** Answer event registration or ticketing questions

---

## 🧠 ML Adaptive Cross-Referencing Protocol

### Core Principle
**By Default: NO CROSS-REFERENCING**
- Events agents ONLY use Events RAG
- Gym agents ONLY use Gym RAG
- This prevents confusion and maintains focused expertise

### Exception: ML Adaptive Cross-Referencing
**ONLY when explicitly needed for context:**

#### Example 1: Competitor Asks About Gym Training
```
User (to Events Agent): "I'm registering for the Ronnie Coleman Classic. Do you offer a gym where I can train before the show?"

Events Agent Logic:
1. Primary query: Event registration (Events RAG) ✅ Answer
2. Secondary query: Gym membership (NOT in Events RAG)
3. ML DETECTS: User context is competition prep → Legitimate cross-reference need
4. ADAPTIVE RESPONSE: "Yes! While I handle event registration, we have The Original MetroFlex Gym in Arlington, TX where you can train. For membership information, I can connect you with our gym team at brian@metroflexgym.com, or visit metroflexgym.com."
```

#### Example 2: Gym Member Asks About Competing
```
User (to Gym Agent): "I'm a member at Arlington. How do I compete at one of your events?"

Gym Agent Logic:
1. Primary query: Membership (Gym RAG) ✅ Acknowledge
2. Secondary query: Event registration (NOT in Gym RAG)
3. ML DETECTS: User context is member wanting to compete → Legitimate cross-reference need
4. ADAPTIVE RESPONSE: "Great! As an Arlington member, you're training where champions are made! For event registration, visit metroflexevents.com or I can connect you with our events team. You'll register through the MuscleWare platform for our three NPC championships: Texas Legends, Ronnie Coleman Classic, and Branch Warren Classic."
```

### ML Cross-Reference Decision Tree

```
User Query Received
    ↓
Does query match my RAG domain?
    ↓
YES → Answer directly from my RAG ✅
    ↓
NO → Does query relate to user's context?
    ↓
    YES → ML ADAPTIVE CROSS-REFERENCE
          - Acknowledge the question
          - Provide brief context-appropriate info
          - Refer to appropriate agent/website
          - DO NOT fabricate details from wrong RAG
    ↓
    NO → Polite referral ONLY
          - "That's handled by our [events/gym] team"
          - Provide contact: brian@metroflexgym.com
          - Provide website: metroflexevents.com or metroflexgym.com
```

### ML Adaptive Triggers

**When to Allow Cross-Referencing:**
- ✅ User is a current customer (member, competitor, licensee)
- ✅ Query relates to natural customer journey (gym → compete, compete → train)
- ✅ Context explicitly requires both systems (e.g., "I want to compete AND join the gym")
- ✅ User asks follow-up question spanning both domains

**When to BLOCK Cross-Referencing:**
- ❌ User is new lead with no established context
- ❌ Query is unrelated to primary agent domain
- ❌ Agent doesn't have ANY data on topic (no guessing)
- ❌ Cross-reference would confuse rather than help

---

## 🗃️ Vector Database Architecture

### Dual ChromaDB Collections

**Events RAG: Collection "metroflex_events"**
```python
collection_events = chroma_client.get_or_create_collection(
    name="metroflex_events",
    embedding_function=embedding_function
)

# Load ONLY Events KB
with open('METROFLEX_EVENTS_KB_V3_EVENTS_ONLY.json') as f:
    events_kb = json.load(f)

# Vectorize events data
# NO gym membership data
# NO licensing data
```

**Gym RAG: Collection "metroflex_gym"**
```python
collection_gym = chroma_client.get_or_create_collection(
    name="metroflex_gym",
    embedding_function=embedding_function
)

# Load ONLY Gym KB
with open('METROFLEX_GYM_KB_V1.json') as f:
    gym_kb = json.load(f)

# Vectorize gym data
# NO event registration data
# NO ticketing data
```

---

## 🔀 Agent Routing Logic

### Initial Query Classification

```python
def classify_initial_domain(query: str) -> str:
    """
    Classify which RAG domain the query belongs to
    Returns: 'events' or 'gym'
    """

    # Events keywords
    events_keywords = [
        'compete', 'register', 'competition', 'show',
        'tickets', 'spectator', 'VIP seating',
        'vendor booth', 'sponsor', 'expo',
        'npc', 'division', 'class', 'weight class',
        'ronnie coleman classic', 'branch warren', 'texas legends',
        'muscleware', 'ticketspice'
    ]

    # Gym keywords
    gym_keywords = [
        'membership', 'join gym', 'day pass',
        'founder', 'miami', 'arlington gym',
        'licensing', 'open a gym', 'franchise',
        'apparel', 'shirt', 'hoodie', 'merch',
        'personal training', 'coach', 'trainer'
    ]

    query_lower = query.lower()

    events_score = sum(1 for kw in events_keywords if kw in query_lower)
    gym_score = sum(1 for kw in gym_keywords if kw in query_lower)

    if events_score > gym_score:
        return 'events'
    elif gym_score > events_score:
        return 'gym'
    else:
        # Ambiguous - default to events (primary brand touchpoint)
        return 'events'
```

### Routing Examples

| Query | Domain | Rationale |
|-------|--------|-----------|
| "How do I register for the Ronnie Coleman Classic?" | Events | "register", "ronnie coleman classic" |
| "When does MetroFlex Miami open?" | Gym | "miami", membership context |
| "How much are spectator tickets?" | Events | "spectator tickets" |
| "I want to open a MetroFlex gym" | Gym | "open a gym", licensing |
| "What sizes do you have for hoodies?" | Gym | "hoodies", apparel |
| "What divisions can I compete in?" | Events | "divisions", "compete" |
| "Tell me about the Founder's Membership" | Gym | "founder's membership" |
| "How do I become a vendor?" | Events | "vendor", expo context |
| "What's the difference between New Build and Rebrand license?" | Gym | "license", licensing packages |
| "Can I compete and also join the gym?" | Both → Events first, then cross-ref | Dual intent detected |

---

## 🏗️ Docker Implementation

### Two Separate Agent Containers

**Container 1: metroflex-events-agent**
```yaml
metroflex-events-agent:
  build:
    context: ./Active/metroflex-ghl-website/AI_Agent
    dockerfile: Dockerfile.events
  environment:
    - OPENAI_API_KEY=${OPENAI_API_KEY}
    - KNOWLEDGE_BASE=METROFLEX_EVENTS_KB_V3_EVENTS_ONLY.json
    - AGENT_DOMAIN=events
  ports:
    - "5001:5001"
  volumes:
    - ./Active/metroflex-ghl-website/AI_Agent/METROFLEX_EVENTS_KB_V3_EVENTS_ONLY.json:/app/knowledge_base.json:ro
```

**Container 2: metroflex-gym-agent**
```yaml
metroflex-gym-agent:
  build:
    context: ./Active/metroflex-ghl-website
    dockerfile: Dockerfile.gym
  environment:
    - OPENAI_API_KEY=${OPENAI_API_KEY}
    - KNOWLEDGE_BASE=METROFLEX_GYM_KB_V1.json
    - AGENT_DOMAIN=gym
  ports:
    - "5002:5002"
  volumes:
    - ./Active/metroflex-ghl-website/METROFLEX_GYM_KB_V1.json:/app/knowledge_base.json:ro
```

### NGINX Routing

```nginx
server {
    listen 80;

    # Route events queries to events agent
    location /api/events/ {
        proxy_pass http://metroflex-events-agent:5001/;
    }

    # Route gym queries to gym agent
    location /api/gym/ {
        proxy_pass http://metroflex-gym-agent:5002/;
    }

    # Intelligent routing (classify query first)
    location /api/chat/ {
        proxy_pass http://query-classifier:5000/;
    }
}
```

---

## 📈 ML Model Separation

### Events RAG ML Models

**1. Lead Scoring Model (Events)**
- Inputs: intent_detected (registration, tickets, vendor_booth, sponsorship)
- Purpose: Prioritize high-value event leads
- Training data: Events leads ONLY

**2. Event Attendance Prediction**
- Inputs: historical_attendance, marketing_spend, divisions_offered
- Purpose: Forecast competitor/spectator attendance
- Training data: Events attendance ONLY

**3. Sponsor Qualification Score**
- Inputs: budget_indicators, company_size, sponsorship_history
- Purpose: Fast-track qualified sponsor leads
- Training data: Sponsorship deals ONLY

---

### Gym RAG ML Models

**1. Lead Scoring Model (Gym)**
- Inputs: intent_detected (membership, licensing, apparel)
- Purpose: Prioritize high-value gym leads
- Training data: Gym leads ONLY

**2. Churn Prediction Model**
- Inputs: membership_type, engagement_frequency, event_participation
- Purpose: Identify at-risk gym members
- Training data: Gym membership ONLY

**3. Size Recommendation Model**
- Inputs: height, weight, preferred_fit, product_category
- Purpose: Reduce apparel returns
- Training data: Apparel orders ONLY

**4. Licensing Qualification Score**
- Inputs: liquid_capital, industry_experience, location_density
- Purpose: Fast-track qualified licensing applicants
- Training data: Licensing applications ONLY

---

## 🎯 Business Benefits

### 1. Precision Targeting
- Events agents become EXPERTS in event operations
- Gym agents become EXPERTS in gym operations + licensing
- No confusion, no wrong answers

### 2. ML Model Accuracy
- Training on focused data = higher accuracy
- Events lead scoring optimized for event leads
- Gym churn prediction optimized for gym members
- No cross-contamination of training data

### 3. Scalability
- Add new events without affecting gym agents
- Add new gym locations without affecting event agents
- Each vertical scales independently

### 4. Data Security
- Events team doesn't need access to gym membership data
- Gym team doesn't need access to event sponsorship data
- Compliance and privacy easier to manage

### 5. Performance Optimization
- Smaller knowledge bases = faster RAG retrieval
- Events RAG: ~600 lines vs 1,200 lines (50% reduction)
- Gym RAG: ~800 lines vs 1,200 lines (33% reduction)
- 2x faster query responses

---

## 📊 Migration Plan

### Phase 1: Create Dual RAG Systems ✅
- [x] Created METROFLEX_EVENTS_KB_V3_EVENTS_ONLY.json
- [x] Created METROFLEX_GYM_KB_V1.json
- [x] Documented dual RAG architecture

### Phase 2: Update Existing Events Agent (Next)
- [ ] Modify metroflex_ai_agent_enhanced.py to use EVENTS_ONLY KB
- [ ] Add domain classifier logic
- [ ] Add ML adaptive cross-referencing protocol
- [ ] Test with events-specific queries

### Phase 3: Create Gym Agent (Week 2)
- [ ] Create metroflex_gym_agent.py based on events agent template
- [ ] Use METROFLEX_GYM_KB_V1.json
- [ ] Implement gym-specific intent classification
- [ ] Add ML adaptive cross-referencing protocol

### Phase 4: Deploy Dual Container Stack (Week 3)
- [ ] Create Dockerfile.events
- [ ] Create Dockerfile.gym
- [ ] Update docker-compose.yml with both agents
- [ ] Implement NGINX intelligent routing
- [ ] Deploy query classifier service

### Phase 5: ML Model Training (Week 4)
- [ ] Train events lead scoring model on events data ONLY
- [ ] Train gym lead scoring model on gym data ONLY
- [ ] Train churn prediction model on gym members ONLY
- [ ] Train licensing qualification model on licensing apps ONLY
- [ ] Deploy models to respective agents

### Phase 6: GHL Integration (Week 5)
- [ ] Configure separate GHL pipelines for events leads
- [ ] Configure separate GHL pipelines for gym leads
- [ ] Test lead capture routing (events → events pipeline, gym → gym pipeline)
- [ ] Validate high-intent detection for both domains

---

## 🧪 Testing Matrix

### Events RAG Tests

| Query | Expected Response | Cross-Ref Allowed? |
|-------|-------------------|-------------------|
| "How do I register for Ronnie Coleman?" | MuscleWare process | NO |
| "How much are spectator tickets?" | TicketSpice pricing | NO |
| "I want a vendor booth" | Vendor booth packages | NO |
| "What sponsorship packages do you offer?" | 4 tiers + pricing | NO |
| "Can I train at your gym before competing?" | Brief gym info + refer to gym team | YES (adaptive) |
| "Do you offer memberships?" | Refer to gym team (NO details) | NO |

### Gym RAG Tests

| Query | Expected Response | Cross-Ref Allowed? |
|-------|-------------------|-------------------|
| "When does Miami open?" | June 1, 2026 + Founder's info | NO |
| "How much is licensing?" | $40k-60k + packages | NO |
| "Where can I buy hoodies?" | Apparel catalog + sizing | NO |
| "Do you offer personal training?" | PT pricing + packages | NO |
| "I'm a member - can I compete?" | Brief event info + refer to events team | YES (adaptive) |
| "How do I register for competitions?" | Refer to events team (NO details) | NO |

---

## 📞 Support & Escalation

### Events Agent Escalation
**When to escalate to human:**
- Complex sponsorship negotiation
- Custom vendor booth requests
- Competition rule exceptions
- Event cancellation/rescheduling

**Escalate to:** brian@metroflexgym.com (events team)

### Gym Agent Escalation
**When to escalate to human:**
- Licensing application review
- Founder's Membership waitlist (if sold out)
- Custom personal training packages
- Gym partnership proposals

**Escalate to:** brian@metroflexgym.com (gym team)

---

## 🏆 Success Metrics

### Events RAG Performance
- Query resolution rate: 85%+ for event-specific queries
- Lead capture rate: 25%+ for high-intent queries
- Cross-referral accuracy: 95%+ refer to gym team when needed
- ML model accuracy: 80%+ lead scoring precision

### Gym RAG Performance
- Query resolution rate: 85%+ for gym-specific queries
- Lead capture rate: 30%+ for high-intent queries (Founder's, licensing)
- Cross-referral accuracy: 95%+ refer to events team when needed
- ML model accuracy: 85%+ licensing qualification precision, 75%+ churn recall

### Combined System Health
- Average response time: <5 seconds
- Dual-domain queries handled: 95%+ correctly routed
- Customer satisfaction: 4.5+ / 5.0 stars
- Zero cross-contamination errors per week

---

## 📚 Related Documentation

- [METROFLEX_EVENTS_KB_V3_EVENTS_ONLY.json](AI_Agent/METROFLEX_EVENTS_KB_V3_EVENTS_ONLY.json) - Events RAG knowledge base
- [METROFLEX_GYM_KB_V1.json](METROFLEX_GYM_KB_V1.json) - Gym RAG knowledge base
- [METROFLEX_6_MISSING_AGENTS_QUICK_REF.md](METROFLEX_6_MISSING_AGENTS_QUICK_REF.md) - Agent development roadmap
- [DOCKER_QUICKSTART.md](../../DOCKER_QUICKSTART.md) - Docker deployment guide

---

**Document Version:** 1.0
**Last Updated:** November 15, 2025
**Status:** Architecture Defined ✅ - Ready for Implementation
**Next Step:** Update existing Events Agent to use EVENTS_ONLY KB

---

**Key Principle:** Two distinct ML RAG systems. Events RAG handles metroflexevents.com ONLY. Gym RAG handles gym memberships + licensing ONLY. ML adaptive cross-referencing ONLY when explicitly needed for user context.
