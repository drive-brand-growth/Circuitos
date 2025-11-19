# Circuitos Codebase Comprehensive Analysis

**Date:** November 19, 2025  
**Repository:** /home/user/Circuitos  
**Analysis Scope:** Circuit Script, DMN, ML Integrations, LLM implementations, and overall architecture

---

## Executive Summary

CircuitOS is a sophisticated multi-agent AI platform that combines:
- **Circuit Script Runtime**: Apex-equivalent execution environment (Cloudflare Workers + Deno)
- **Decision Engine**: Three-layer architecture (DMN + ML + LLM)
- **Multi-Agent System**: Specialized AI agents for different business workflows
- **RAG-Powered Assistants**: Knowledge-base driven conversational AI
- **Event-Driven Architecture**: Webhook-triggered, serverless execution model

---

## 1. CIRCUIT SCRIPT IMPLEMENTATION

### What It Is
Circuit Script is a **code execution runtime** that brings Salesforce Apex-level capabilities to CircuitOS. It's designed to replace scattered webhook handlers with a unified execution platform.

**Location:** `/home/user/Circuitos/Active/circuit-script-runtime/`

### Architecture Components

#### 1.1 API Gateway (Cloudflare Workers)
- **Technology:** Cloudflare Workers Edge Runtime
- **Purpose:** Webhook receiver and event router
- **Features:**
  - POST `/trigger/:objectType/:event` endpoint
  - API key validation (authentication layer)
  - Rate limiting (1000 req/min per customer)
  - Event routing (maps webhooks → trigger classes)
  - <10-50ms cold start latency (vs 200-500ms traditional serverless)

#### 1.2 Execution Sandbox (V8 Isolate)
- **Technology:** Deno Runtime with V8 Isolate
- **Isolation Level:** Complete JavaScript context isolation
- **Security Boundaries:**
  - No file system access
  - No direct network access (only via CircuitDB)
  - Transaction rollback on error
  - Sandboxed execution context per trigger

#### 1.3 Governor (Resource Management)
**Salesforce-style governor limits enforced at runtime:**
- Max execution time: 30 seconds (kills runaway code)
- Max memory: 128MB (prevents memory exhaustion)
- Max API calls: 50 (controls external API costs)
- Max DB queries: 100
- Max DML statements: 150

These are **enforced during execution**, not post-execution (preventing runaway costs).

#### 1.4 Trigger Framework
- **Pattern:** Decorator-based trigger registration (`@trigger` decorator)
- **Example:**
  ```javascript
  @trigger('Contact', ['afterInsert'])
  async scoreNewLeads(context) {
    const { newRecords } = context;
    const scores = await VirtualLPR.scoreLeads(newRecords);
    await CircuitDB.update('Contact', scores);
  }
  ```

#### 1.5 Logging & Observability
- **Primary Tool:** Axiom (structured logging)
- **Captures:**
  - Execution trace (start/end timestamps)
  - Resource usage tracking (API calls, memory, queries)
  - Error reporting (Sentry integration)
  - Audit logs (compliance)
- **Retention:** 30 days centralized logging

#### 1.6 CircuitDB - Unified Data Layer
**Single abstraction layer for all data operations:**
- GHL API (contacts, custom fields, workflows)
- Salesforce REST API (SOQL queries, DML operations)
- Supabase (ML feedback, analytics)
- Automatic bulkification (batch operations)
- Rate limiting aware (respects external API quotas)
- Connection pooling for performance

### Circuit Script vs Traditional Webhooks

| Feature | Traditional Webhooks | Circuit Script |
|---------|-------------------|----------------|
| **Execution** | Railway/Vercel functions | Cloudflare Workers (edge) |
| **Latency** | 200-500ms (cold start) | 10-50ms (instant) |
| **Logging** | Scattered across 5 platforms | Centralized (Axiom) |
| **Governor Limits** | None (runaway costs risk) | Enforced (30sec, 128MB, 50 API calls) |
| **Testing** | Manual (if you remember) | Mandatory (75% coverage) |
| **Deployment** | git push → hope it works | Tested → staged → production |
| **Rollback** | Fix forward (no rollback) | One-click rollback |
| **Cost** | $20-100/month per function | $5/month for ALL triggers |
| **Debugging** | Console.log hunting | Execution timeline + traces |

### Implementation Status
- **Cores Runtime:** Designed, documented, architecture complete
- **Package:** `@circuitos/circuit-script` (v1.0.0)
- **Timeline:** 8-week MVP to production
- **Current Phase:** Specification and documentation complete; implementation pending

**Key Dependencies:**
```json
{
  "hono": "^4.0.0",  // Lightweight web framework
  "@cloudflare/workers-types": "^4.20240117.0",
  "typescript": "^5.3.3",
  "vitest": "^1.2.0",
  "wrangler": "^3.24.0"
}
```

---

## 2. DMN (DECISION MODEL AND NOTATION) INTEGRATION

### Current Implementation

The codebase implements a **three-layer intelligence architecture** combining DMN + ML + LLM:

#### 2.1 DMN - Business Rules Engine

**Not implemented as formal DMNX files** but rather as **encoded business logic** in:
- Scoring algorithms
- Decision thresholds
- Conditional routing logic

**Example: Lost Opportunity Agent Decision Logic**

Located in: `/home/user/Circuitos/Active/agentforce_emulator/services/agent_runtime/orchestrator.py`

```python
# Decision bands based on scoring thresholds
def _determine_band(self, score: float, thresholds: dict) -> str:
    urgent = thresholds.get("urgent", 80)
    high = thresholds.get("high", 60)
    
    if score >= urgent:
        return "urgent"  # → Create task, send Slack alert, draft email
    if score >= high:
        return "high"    # → Standard nurture sequence
    return "ignore"      # → No action
```

**Configuration-based rules:** `/home/user/Circuitos/Active/agentforce_emulator/configs/scoring_rules.yaml`
- Global thresholds
- Action plans per decision band
- Alert channels
- Task priorities
- Annotation rules

#### 2.2 DMN Rules in Different Agents

**1. Licensing Qualification Agent** (`licensing_agent.py`)
- Qualification scoring: 0-100 points
- Decision bands:
  - 85-100: FAST_TRACK (immediate phone call)
  - 70-84: QUALIFIED (standard process)
  - 50-69: NURTURE (educational sequence)
  - <50: NOT_QUALIFIED (refer to gym membership)
- Scoring factors:
  - Liquid capital: 40 points (>$150k = full)
  - Industry experience: 25 points (>3 years = full)
  - Existing gym: 15 points (bonus)
  - Passion score: 20 points (self-reported)

**2. Conversation Agent** (`ghl_conversation_agent.py`)
- **Objection Detection Framework:**
  - Price objections (35% frequency) → Value equation + ROI
  - Timing objections (25% frequency) → Cost of waiting
  - Authority objections (12% frequency) → Multi-stakeholder strategy
  - Trust objections (8% frequency) → Social proof
  - Comparison objections (5% frequency) → Differentiation

- **Handoff Decision Logic:**
  ```
  handoff_score = awareness_gap + objection_severity + sentiment_analysis
  if handoff_score >= 75: → Human sales rep handoff
  else: → Continue with AI response
  ```

**3. Intent Classification Engine** (`metroflex_ai_agent_enhanced.py`)
- Query intent classification to optimize RAG retrieval
- 10+ intent categories:
  - Datetime (event schedule) → prioritize event data
  - Registration (how to compete) → procedures + multi-turn flow
  - Division rules → division rules database
  - Sponsor queries → sponsor database + lead capture
  - Vendor services → vendor database
  - First-timer → guidance + onboarding flow
  - Tickets → spectator information

### DMN Future Roadmap
**Recommendation:** Formalize as DMNX (DMN XML) for:
- Business rule versioning
- Non-technical stakeholder management
- Compliance auditing
- Decision tree visualization
- Rules engine integration (Drools, IBM ODM)

---

## 3. MACHINE LEARNING INTEGRATIONS

### 3.1 Current ML Implementations

**Location:** Embedded in agent logic, not separate ML pipeline yet

#### Lead Scoring & Qualification
**Files:**
- `licensing_agent.py` - Qualification score calculation
- `ghl_conversation_agent.py` - Handoff score calculation
- `metroflex_ai_agent_enhanced.py` - Intent classification

**Approach:** Rule-based ML (decision trees + weighted scoring)
- Not deep learning models
- Deterministic scoring algorithms
- Historical pattern recognition through thresholds

#### Example: Licensing Qualification ML
```python
score = 0
# Capital factor (40 points)
if liquid_capital >= 150000: score += 40
elif liquid_capital >= 100000: score += 30

# Experience factor (25 points)
if years_exp >= 5: score += 25
elif years_exp >= 3: score += 20

# Existing gym bonus (15 points)
if existing_gym and sqft >= 3000: score += 15

# Passion (20 points)
score += (passion_score / 10) * 20
```

### 3.2 ML Infrastructure

**Technologies Used:**
- **Sentence Transformers** (semantic embeddings)
  - Model: `all-MiniLM-L6-v2`
  - Purpose: Vector embeddings for RAG
  - File: `metroflex_ai_agent.py` line 44-45

- **ChromaDB** (vector database for RAG)
  - Stores embeddings from knowledge bases
  - Semantic search for document retrieval
  - In-memory collection management

- **Scoring Algorithms**
  - Weighted feature scoring
  - Threshold-based decision bands
  - Sensitivity analysis (confidence levels)

### 3.3 Future ML Opportunities

1. **Predictive Modeling:**
   - Reactivation probability (which lost deals will respond)
   - Conversion prediction (which leads → closed deals)
   - Churn prediction (which customers at risk)

2. **Clustering:**
   - Customer segment identification
   - Lead persona detection
   - Objection pattern clustering

3. **Deep Learning:**
   - NLP for sentiment analysis
   - Intent classification (transformer-based)
   - Response quality scoring

4. **Training Pipeline:**
   - Historical data labeling
   - Model training infrastructure
   - Cross-validation & evaluation
   - Model deployment & monitoring

---

## 4. LLM INTEGRATIONS

### 4.1 Primary LLM Provider: OpenAI

**Model:** GPT-4o-mini (cost-optimized)
- **Cost:** ~$0.0005 per chat (16x cheaper than GPT-4o)
- **Use Case:** Factual Q&A, knowledge base queries
- **Provider:** OpenAI API v1.0+

**Secondary Model Options Available:**
- OpenAI (gpt-4o-mini, gpt-4o)
- Anthropic Claude (from dependencies in virtual-agentforce)

### 4.2 LLM Integration Points

#### 1. RAG (Retrieval-Augmented Generation)
**Files:**
- `metroflex_ai_agent.py` (389 lines)
- `metroflex_ai_agent_enhanced.py` (879 lines)
- `ghl_conversation_agent.py` (645 lines)

**RAG Pipeline:**
```
User Query
    ↓
Intent Classification (routing)
    ↓
ChromaDB Semantic Search (vector retrieval)
    ↓
Top-K Documents Retrieved (context)
    ↓
System Prompt + Context + Query
    ↓
OpenAI API Call
    ↓
Response Generation
    ↓
Lead Capture (if high-intent signal)
    ↓
GHL Webhook
```

**Knowledge Bases Used:**
- `METROFLEX_COMPLETE_KB_V3.json` - Events, divisions, vendors, legacy
- `METROFLEX_GYM_KB_V1.json` - Gym membership info
- Custom licensing, events, procedural knowledge bases

#### 2. Conversation Agent
**File:** `ghl_conversation_agent.py`

**Capabilities:**
- Objection detection & response generation
- Multi-turn conversation management
- Awareness level assessment (Schwartz framework: levels 1-5)
- Handoff decision scoring
- Sales framework application (17-point judgment, value equation)

**Response Generation:**
```python
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message}
    ],
    temperature=0.7,  # Some creativity for natural responses
    max_tokens=500
)
```

#### 3. Workflow Generator Agent
**File:** `ghl_workflow_agent.py` (827 lines)

**Generates:**
- Multi-step email sequences (Hook-Story-Offer framework)
- SMS messaging strategies
- Social media post copy
- Call scripts
- n8n workflow JSON

**LLM Role:**
- Applies marketing frameworks (Brunson, Hormozi, StoryBrand)
- Generates context-aware messaging
- Creates executable n8n workflows (JSON output)

#### 4. Intent Classification Engine
**File:** `metroflex_ai_agent_enhanced.py`

**Classification Strategy:**
```python
def classify_query_intent(self, query: str) -> Dict:
    # Keyword-based primary classification
    if any(word in query.lower() for word in ['register', 'sign up', 'compete']):
        return {
            "intent": "registration",
            "filter_category": "procedures",
            "sub_intent": "competitor_registration",
            "requires_structured_flow": True
        }
```

**17 Intent Categories:**
- datetime (event schedule)
- registration (compete/sign up)
- division_rules
- sponsor_inquiry
- vendor_services
- legacy/history
- first_timer
- tickets/spectators
- etc.

### 4.3 LLM System Prompts

**Pattern:** Comprehensive system prompts with embedded knowledge bases

Example structure:
```python
system_prompt = f"""You are the MetroFlex AI Agent.

KNOWLEDGE BASE:
{json.dumps(knowledge_base, indent=2)}

TONE: Professional, encouraging, legacy-focused

HIGH-INTENT SIGNALS: [list of signals triggering lead capture]

FRAMEWORKS APPLIED:
- Schwartz Awareness Levels (1-5)
- Hormozi Value Equation
- Brunson Hook-Story-Offer
- StoryBrand Framework
- 17-Point Judgment Framework

RESPONSE CONSTRAINTS:
- Max 500 tokens
- Avoid markdown formatting
- Use conversational tone
- Include specific details from knowledge base
"""
```

### 4.4 Lead Capture Integration

**GHL Webhook Integration:**
When high-intent signals detected:
```python
payload = {
    "contact": {
        "email": email,
        "phone": phone,
        "name": name,
        "source": "AI Chat Widget",
        "tags": [intent_type, lead_category, "ai_chat_lead"],
        "custom_fields": {
            "lead_source": "AI Chat Widget",
            "intent": intent_type,
            "lead_category": lead_category,
            "lead_quality_score": "high"  # For licensing: $40k-$60k deals
        }
    }
}
requests.post(ghl_webhook_url, json=payload)
```

---

## 5. ARCHITECTURE OVERVIEW

### 5.1 System Architecture Diagram

```
┌─────────────────────────────────────┐
│  External Event Sources              │
│  - GHL Webhooks (contact.created)    │
│  - Salesforce Events (apex triggers) │
│  - Scheduled Jobs (cron)             │
└────────────────┬────────────────────┘
                 ↓
┌─────────────────────────────────────┐
│  Circuit Script API Gateway          │
│  (Cloudflare Workers - Edge)         │
│  - Authentication (API key)          │
│  - Rate limiting (1000 req/min)      │
│  - Event routing                     │
└────────────────┬────────────────────┘
                 ↓
┌─────────────────────────────────────┐
│  Circuit Script Executor             │
│  - Trigger Manager                   │
│  - Governor (Resource Limits)        │
│  - V8 Isolate (Execution Sandbox)    │
│  - Axiom Logger                      │
└────────────────┬────────────────────┘
                 ↓
┌─────────────────────────────────────┐
│  CircuitDB (Unified Data Layer)      │
│  - GHL API                           │
│  - Salesforce REST API               │
│  - Supabase (ML feedback)            │
│  - Census API (enrichment)           │
│  - LinkedIn API (social)             │
└────────────────────────────────────┘
```

### 5.2 Multi-Agent Architecture

**5 Specialized AI Agents:**

1. **MetroFlex Events Agent** (879 lines)
   - Purpose: Event info, vendor services, sponsorship inquiries
   - Tech: RAG + intent classification + lead capture
   - Integration: GHL webhooks

2. **Conversation Agent** (645 lines)
   - Purpose: Real-time SMS/chat objection handling
   - Tech: Objection detection + sales frameworks + awareness assessment
   - Handoff trigger: Handoff score >= 75

3. **Workflow Generator** (827 lines)
   - Purpose: Multi-channel nurture sequence creation
   - Tech: Marketing framework application + n8n JSON generation
   - Output: Email, SMS, LinkedIn, calls

4. **Licensing Agent** (328 lines)
   - Purpose: High-value licensing qualification ($40k-$60k deals)
   - Tech: ML scoring + ROI calculation + application guidance
   - Score bands: FAST_TRACK (85+), QUALIFIED (70-84), NURTURE (50-69), NOT_QUALIFIED (<50)

5. **Gym Member Agent** (354 lines)
   - Purpose: Founder's membership ($2,500) qualification
   - Tech: Lead qualification + upsell detection

### 5.3 Agentforce Emulator (Salesforce Agentforce Simulation)

**Location:** `/home/user/Circuitos/Active/agentforce_emulator/`

**Technology Stack:**
- FastAPI (REST API)
- SQLAlchemy + Postgres (data persistence)
- LangGraph + LangChain (agent orchestration)
- Redis (event bus, caching)
- OpenTelemetry (observability)

**Key Components:**

1. **CRM API Service** (`services/crm_api/`)
   - Mock Salesforce objects (Opportunity, Account, Contact)
   - SOQL query parsing
   - REST endpoints for CRUD operations

2. **Agent Runtime Service** (`services/agent_runtime/`)
   - Lost Opportunity Orchestrator (main logic)
   - LangGraph workflow graph
   - Action executor (create tasks, send alerts, compose emails)
   - Scoring module (configurable scoring rules)

3. **Control Panel** (React UI)
   - Salesforce-style dashboard
   - Agent run management
   - Real-time execution traces
   - Decision visualization

**Example Run Flow:**
```
POST /api/v1/agents/lost-opportunity/run
  ↓
LostOpportunityOrchestrator.run()
  ↓
Fetch closed-lost opportunities
  ↓
For each opportunity:
  - Load signals (demographic, engagement, competitor, etc.)
  - Score (compute_score with configurable rules)
  - Determine decision band (urgent, high, ignore)
  - Execute actions (tasks, alerts, annotations, emails)
  ↓
Return AgentRunResponse with outcomes
  ↓
POST /api/v1/agents/runs/{run_id} to persist
```

### 5.4 Virtual AgentForce Environment

**Location:** `/home/user/Circuitos/Active/virtual-agentforce/`

**Purpose:** Local-first sandbox for Salesforce AgentForce simulation

**Key Features:**
- Mock Salesforce data layer (Account, Contact, Opportunity, Custom Objects)
- Atlas Reasoning Engine simulator (LLM integration)
- Agent Builder interface (configuration)
- Action framework (query, create, update, delete, tasks)
- Data source connectors (Data Cloud, Bombora, LinkedIn)
- Testing & validation tools

**Dependencies:**
```
fastapi==0.104.1
sqlalchemy==2.0.23
pydantic==2.5.0
openai==1.3.0
anthropic==0.7.8  # Multi-LLM support
```

### 5.5 n8n Workflow Integration

**Location:** `/home/user/Circuitos/n8n/workflows/`

**Workflows:**
- `licensing-high-value-lead.json` - Example workflow for licensing leads

**Purpose:** 
- Executes generated workflows from Workflow Generator Agent
- 14-day multi-channel nurture sequences
- Email → SMS → LinkedIn → Email → Call

**Integration:**
- Receives JSON from Workflow Generator LLM
- Deployed in Docker: `/home/user/Circuitos/n8n/Dockerfile`

---

## 6. KEY FILES & THEIR PURPOSES

### Circuit Script Core
| File | Lines | Purpose |
|------|-------|---------|
| `circuit-script-runtime/package.json` | 32 | Package definition, npm scripts |
| `circuit-script-runtime/tsconfig.json` | 20 | TypeScript configuration |
| `circuit-script-runtime/wrangler.toml` | 20 | Cloudflare Workers config |
| `circuit-script-runtime/README.md` | 585 | Complete specification & examples |
| `circuit-script-runtime/ARCHITECTURE_DIAGRAMS.md` | 150+ | System architecture documentation |

### MetroFlex AI Agents
| File | Lines | Purpose |
|------|-------|---------|
| `metroflex_ai_agent_enhanced.py` | 879 | RAG agent with intent classification, lead capture |
| `ghl_conversation_agent.py` | 645 | Objection handling, handoff scoring |
| `ghl_workflow_agent.py` | 827 | Multi-channel nurture sequence generation |
| `licensing_agent.py` | 328 | Licensing qualification scoring |
| `gym_member_agent.py` | 354 | Gym membership qualification |
| `METROFLEX_COMPLETE_KB_V3.json` | Large | Knowledge base (events, vendors, legacy) |
| `requirements.txt` | 19 | Python dependencies (openai, chromadb, flask) |

### Agentforce Emulator
| File | Purpose |
|------|---------|
| `orchestrator.py` | Lost opportunity agent logic, scoring, decisions |
| `services/agent_runtime/app.py` | FastAPI application setup |
| `services/crm_api/app.py` | Mock Salesforce data API |
| `services/agent_runtime/models.py` | SQLAlchemy ORM models |
| `pyproject.toml` | Python dependencies (LangGraph, LangChain) |
| `apps/control_panel/src/App.tsx` | React control panel UI |

### Documentation
| File | Purpose |
|------|---------|
| `SYSTEM_ARCHITECTURE_DIAGRAMS.md` | Complete MetroFlex system architecture |
| `CIRCUITOS_COMPLETE_TECH_STACK_GUIDE.md` | Tech stack overview |
| `EXECUTIVE_SUMMARY_DMN_ML_LLM.md` | Three-layer intelligence architecture |
| `Documentation/EXECUTIVE_SUMMARY_DMN_ML_LLM.md` | DMN + ML + LLM implementation guide |

---

## 7. COMPONENT INTERACTIONS

### Data Flow: Lead Capture Example

```
User Message (SMS/Chat)
    ↓
MetroFlex Events Agent
    ├─ Intent Classification
    │  └─ Detect intent type (sponsor, registration, etc.)
    ├─ High-Intent Detection
    │  └─ Check for signals like "sponsor", "how much"
    ├─ RAG Retrieval
    │  └─ ChromaDB semantic search for context
    └─ LLM Generation
       └─ OpenAI generates response
    ↓
High-Intent Signal Detected?
    ├─ YES → GHL Lead Capture
    │  ├─ Create GHL contact record
    │  ├─ Add tags (intent_type, lead_category)
    │  ├─ Set custom fields (lead_source, quality_score)
    │  └─ Trigger GHL workflows
    └─ NO → Send AI response only
    ↓
Conversation History
    └─ Store in agent state for multi-turn context
```

### Orchestration: Agentforce Emulator Run

```
POST /api/v1/agents/lost-opportunity/run
    ↓
LostOpportunityOrchestrator.run()
    ├─ Fetch closed-lost opportunities (CRM API)
    ├─ Load scoring configuration
    └─ For each opportunity:
       ├─ Load signals (CRM API)
       ├─ Compute score (scoring rules)
       ├─ Determine band (DMN thresholds)
       ├─ Execute actions (if score >= threshold)
       │  ├─ Create task (action registry)
       │  ├─ Send Slack alert
       │  ├─ Compose email (LLM generated)
       │  └─ Record annotation
       └─ Persist run & actions (PostgreSQL)
    ↓
Return AgentRunResponse
    └─ run_id, evaluated count, acted count, outcomes
```

---

## 8. DEPLOYMENT & INFRASTRUCTURE

### Containerization
**Location:** `/home/user/Circuitos/docker-compose.yml`

**Services Orchestrated:**
- Circuit Script API (Cloudflare Workers equivalent)
- MetroFlex AI Agents (FastAPI)
- Agentforce Emulator (CRM API + Agent Runtime)
- n8n (workflow automation)
- Postgres (data persistence)
- Redis (caching, event bus)
- ChromaDB (vector database)
- Axiom (logging)
- Grafana (monitoring)
- Prometheus (metrics)

### Deployment Platforms
- **Primary:** Railway.app (current)
- **Alternative:** Fly.io, Heroku
- **Edge:** Cloudflare Workers (Circuit Script)

---

## 9. CURRENT STATUS & GAPS

### Implemented
✅ MetroFlex RAG agents (5 specialized agents)  
✅ Conversation agent with objection handling  
✅ Intent classification & lead capture  
✅ Licensing qualification scoring  
✅ Agentforce emulator (Lost Opportunity Agent)  
✅ Virtual AgentForce environment  
✅ Docker containerization  
✅ n8n workflow generation  
✅ Comprehensive documentation  

### Partially Implemented
⚠️ Circuit Script (specification complete, runtime pending)  
⚠️ DMN (encoded as business rules, not formal DMNX)  
⚠️ ML (rule-based scoring, not deep learning)  

### Not Implemented
❌ Formal DMN (DMNX) files  
❌ Deep learning models (NLP, sentiment, clustering)  
❌ LangGraph graph definition in agent runtime  
❌ Production ML training pipeline  
❌ Advanced observability (full OpenTelemetry)  

---

## 10. TECHNOLOGY STACK SUMMARY

### Backend
- **Python 3.12+** - AI agents, API services
- **FastAPI** - REST API frameworks
- **SQLAlchemy** - ORM
- **Postgres** - Primary database
- **Redis** - Caching, event bus
- **LangChain/LangGraph** - Agent orchestration (planned)

### LLM & AI
- **OpenAI GPT-4o-mini** - Primary LLM
- **Anthropic Claude** - Secondary option
- **Sentence Transformers** - Embeddings
- **ChromaDB** - Vector database

### Frontend
- **React + TypeScript** - Web UI
- **Vite** - Build tool
- **Salesforce Design System** - UI components

### DevOps
- **Docker** - Containerization
- **Cloudflare Workers** - Edge runtime
- **Wrangler** - Workers CLI
- **GitHub** - Version control
- **Railway/Fly.io** - Hosting

### Monitoring
- **Axiom** - Logs
- **Sentry** - Error tracking
- **Prometheus** - Metrics
- **Grafana** - Dashboards
- **OpenTelemetry** - Tracing

---

## 11. RECOMMENDED NEXT STEPS

### Phase 1: Circuit Script Production (8 weeks)
1. Implement Cloudflare Workers gateway
2. Build execution sandbox with governor limits
3. Create trigger framework with decorators
4. Deploy logging infrastructure (Axiom)
5. Migrate Virtual LPR to Circuit Script

### Phase 2: Formalize DMN
1. Create DMNX files for decision rules
2. Integrate DMN engine (Drools or similar)
3. Add business rule UI for non-technical users
4. Enable rule versioning & audit trails

### Phase 3: Advanced ML
1. Train predictive models (reactivation, conversion)
2. Set up ML training pipeline
3. Implement model evaluation & testing
4. Deploy model monitoring

### Phase 4: LangGraph Integration
1. Define agent workflow graphs explicitly
2. Implement state management
3. Add conditional routing
4. Enable complex multi-step workflows

---

**Document Generated:** November 19, 2025  
**Repository:** /home/user/Circuitos  
**Branch:** claude/circuit-script-ai-integration-016nSibTEmHsc9iCgLvJiRQP
