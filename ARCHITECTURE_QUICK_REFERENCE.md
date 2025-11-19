# CircuitOS Architecture Quick Reference

## System Layers

```
┌─────────────────────────────────────────────────────────────┐
│                    USER LAYER                                │
│  GHL Chat Widgets │ SMS │ Webhooks │ API Calls             │
└────────────────────────┬────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│            CIRCUIT SCRIPT RUNTIME (PLANNED)                  │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────────┐  │
│  │ API      │  │ Trigger  │  │ Governor │  │ Sandbox    │  │
│  │ Gateway  │  │ Manager  │  │ Limits   │  │ (V8)       │  │
│  └──────────┘  └──────────┘  └──────────┘  └────────────┘  │
└────────────────────────┬────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│              AI AGENT LAYER (IMPLEMENTED)                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐   │
│  │ MetroFlex    │  │ Conversation │  │ Workflow         │   │
│  │ Events       │  │ Agent        │  │ Generator        │   │
│  │ Agent (879)  │  │ (645 lines)  │  │ (827 lines)      │   │
│  └──────────────┘  └──────────────┘  └──────────────────┘   │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐                         │
│  │ Licensing    │  │ Gym Member   │                         │
│  │ Agent        │  │ Agent        │                         │
│  │ (328 lines)  │  │ (354 lines)  │                         │
│  └──────────────┘  └──────────────┘                         │
└────────────────────────┬────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│         INTELLIGENCE LAYER (DMN + ML + LLM)                 │
│  ┌─────────────┐  ┌─────────────┐  ┌──────────────────┐    │
│  │ Decision    │  │ Scoring &   │  │ LLM              │    │
│  │ Engine      │  │ Qualification│ │ (GPT-4o-mini)    │    │
│  │ (DMN Rules) │  │ (ML)        │  │ + RAG            │    │
│  └─────────────┘  └─────────────┘  └──────────────────┘    │
└────────────────────────┬────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│              DATA & INTEGRATION LAYER                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────────┐  │
│  │ GHL API  │  │ Salesforce│  │ Supabase │  │ ChromaDB   │  │
│  │ (CRM)    │  │ (SOQL)   │  │ (ML KB)  │  │ (Vector)   │  │
│  └──────────┘  └──────────┘  └──────────┘  └────────────┘  │
│                                                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                   │
│  │ Postgres │  │ Redis    │  │ n8n      │                   │
│  │ (Data)   │  │ (Cache)  │  │ (Flows)  │                   │
│  └──────────┘  └──────────┘  └──────────┘                   │
└────────────────────────┬────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│            OBSERVABILITY & MONITORING                        │
│  Axiom Logs │ Sentry Errors │ Prometheus Metrics │ Grafana  │
└─────────────────────────────────────────────────────────────┘
```

## Component Mapping

| Component | Technology | Files | Purpose |
|-----------|-----------|-------|---------|
| **Circuit Script** | Cloudflare Workers + Deno | circuit-script-runtime/ | Apex-equivalent runtime |
| **DMN Engine** | Python rules + YAML config | orchestrator.py, scoring_rules.yaml | Business decision logic |
| **ML Scoring** | Weighted algorithms | licensing_agent.py, *_agent.py | Lead qualification |
| **LLM Integration** | OpenAI GPT-4o-mini | metroflex_ai_agent*.py | Conversational AI |
| **RAG System** | ChromaDB + Embeddings | metroflex_ai_agent.py | Knowledge retrieval |
| **Workflow Engine** | n8n + JSON generation | ghl_workflow_agent.py | Multi-step automation |
| **Agent Orchestration** | LangGraph (planned) | orchestrator.py | Agent coordination |
| **Data Layer** | Postgres + SQLAlchemy | services/crm_api/ | Persistent storage |
| **Observability** | Axiom + Sentry | All services | Monitoring & logging |

## Data Flow Patterns

### Pattern 1: Intent → Classification → Response
```
User Input → Intent Classifier → RAG Search → LLM Call → Response → Lead Capture?
```

### Pattern 2: Lead Scoring → Decision → Action
```
Lead Data → ML Scoring → Decision Thresholds → Action Plan → Execution
```

### Pattern 3: Opportunity Reactivation
```
Closed-Lost Opportunity → Load Signals → Score (DMN Rules) 
→ Determine Band → Execute Actions → GHL Update
```

## Key Decision Points

| Decision | Scoring Range | Action | Agent |
|----------|--------------|--------|-------|
| Licensing Qualification | 85+ | Fast-track call | licensing_agent |
| Licensing Qualified | 70-84 | Standard process | licensing_agent |
| Licensing Nurture | 50-69 | Education sequence | licensing_agent |
| Objection Handoff | Score 75+ | Human rep | conversation_agent |
| Lost Opp Urgent | Score 80+ | Create task + alert | agentforce_emulator |
| Lost Opp High | Score 60+ | Nurture sequence | agentforce_emulator |

## Integration Points

```
GHL Webhooks ──→ AI Agents ──→ Decision Engine ──→ Actions
     ↓                          ↓                    ↓
  Contacts            Scoring Rules           GHL Updates
  Custom Fields       ML Qualification        Slack Alerts
  Workflows           Lead Capture            Task Creation
                      Email Generation        n8n Workflows
```

## File Organization

```
/home/user/Circuitos/
├── Active/
│   ├── circuit-script-runtime/          # Circuit Script (8-week MVP)
│   ├── metroflex-ghl-website/           
│   │   └── AI_Agent/                    # 5 AI Agents (implemented)
│   ├── agentforce_emulator/             # Lost Opportunity Agent
│   ├── virtual-agentforce/              # Salesforce simulation
│   └── ...
├── docker/                              # Infrastructure configs
├── n8n/workflows/                       # Automation workflows
├── Documentation/                       # Architecture & guides
└── CODEBASE_COMPREHENSIVE_ANALYSIS.md   # This analysis
```

## Technology Choices

| Layer | Choice | Why | Alternative |
|-------|--------|-----|-------------|
| LLM | OpenAI GPT-4o-mini | Cost-optimized (16x cheaper) | Claude, Gemini |
| Vector DB | ChromaDB | Simple, in-memory, embedded | Pinecone, Weaviate |
| Web Framework | FastAPI | Async-first, modern | Django, Flask |
| Orchestration | LangGraph (planned) | Multi-agent workflows | CrewAI, Autogen |
| Edge Runtime | Cloudflare Workers | Global latency (10-50ms) | AWS Lambda, Vercel |
| Database | Postgres | Production-ready | MySQL, MongoDB |
| Job Queue | Redis | Lightweight, built-in | RabbitMQ, Celery |

## Performance Metrics

| Metric | Target | Status |
|--------|--------|--------|
| API Latency | <100ms | Circuit Script: 10-50ms |
| Cold Start | <50ms | Cloudflare Workers achieves this |
| Logging Retention | 30 days | Axiom configured |
| Governor Timeout | 30 seconds | Hard limit enforced |
| API Calls/Run | <50 | Rate limiting via governor |
| Test Coverage | >75% | Required before deployment |

## Deployment Stack

```
GitHub Repo
    ↓
CI/CD Pipeline (GitHub Actions)
    ↓
Docker Build → Registry
    ↓
Railway.app / Fly.io
    ├─ MetroFlex Agents (FastAPI)
    ├─ Agentforce Emulator (FastAPI)
    ├─ Postgres Database
    ├─ Redis Cache
    └─ n8n Workflows
    ↓
Cloudflare Workers (Circuit Script - future)
    ↓
GHL Webhooks / Salesforce Events
```

## Next Priorities

1. **Immediate:** Formalize DMN rules as DMNX files
2. **Short-term:** Implement Circuit Script runtime (8 weeks)
3. **Medium-term:** Add deep learning models (sentiment, clustering)
4. **Long-term:** Full LangGraph integration with agent marketplace

---
Generated: November 19, 2025
