# CircuitOS Development Memory

This file captures key architectural decisions, patterns, and metrics for CircuitOS development.

---

## Core Architecture: Circuit Script + DMN + ML + LLM

### Overview

CircuitOS uses a unified orchestration layer where **Circuit Script** (Apex-like syntax) coordinates DMN business rules, ML models, and LLM agents.

```
┌─────────────────────────────────────────┐
│         CIRCUIT SCRIPT RUNTIME          │
│   (Apex-like syntax, Governor Limits)   │
└─────────────────┬───────────────────────┘
                  │
    ┌─────────────┼─────────────┐
    ▼             ▼             ▼
┌───────┐   ┌─────────┐   ┌─────────┐
│  DMN  │   │   ML    │   │   LLM   │
│ Rules │   │ Models  │   │ Agents  │
└───────┘   └─────────┘   └─────────┘
```

### Key Design Principles

1. **Apex-like syntax** - Familiar to Salesforce developers
2. **Governor limits** - Prevents runaway costs (30s CPU, 50 API calls, 100 queries)
3. **Declarative AI** - Business users write logic without knowing ML/LLM internals
4. **Unified data layer** - CircuitDB abstracts GHL + Salesforce + Supabase

---

## Component Specifications

### 1. DMN Decision Engine

**Purpose:** Version-controlled business rules that business analysts can modify

**Hit Policies:**
- `FIRST` - Return first matching rule (most common)
- `COLLECT` - Return all matching rules
- `UNIQUE` - Error if multiple rules match

**Current Decision Tables:**
- `LeadQualification_v1` - Qualification scoring (FAST_TRACK, QUALIFIED, NURTURE, NOT_QUALIFIED)
- `HandoffDecision_v1` - Conversation handoff rules

**Location:** `Active/circuit-script-runtime/poc/dmn/`

### 2. Circuit Script Parser

**Supported Syntax:**
- Class definitions with decorators (`@Trigger`, `@AgentFlow`)
- Method declarations with parameters
- Variable assignments
- Object literals `{ key: value }`
- Method chaining `object.method().property`
- If/else statements
- Service calls (DMN, ML, LLM, Workflow, DB)

**Location:** `Active/circuit-script-runtime/poc/circuit_script/parser.py`

### 3. Circuit Script Runtime

**Built-in Services:**
```apex
// Decision Management
DMN.evaluate(decisionId, inputs)           // Returns DecisionResult

// Machine Learning
ML.predict(modelId, features)              // Returns score (0-1)
ML.classify(modelId, text)                 // Returns classification

// Language Models
LLM.generate(promptId, context)            // Returns generated text
LLM.chat(messages)                         // Returns chat response

// Automation
Workflow.trigger(workflowId, data)         // Triggers n8n/GHL workflow

// Data
DB.query(soql)                             // Query CircuitDB
DB.insert(sobject, records)                // Insert records
DB.update(sobject, records)                // Update records

// Utilities
System.log(message)                        // Log to execution trace
System.debug(value)                        // Debug output
```

**Governor Limits:**
- CPU Time: 30,000ms
- API Calls: 50
- Queries: 100
- DML Statements: 150
- Heap Size: 128MB

**Location:** `Active/circuit-script-runtime/poc/circuit_script/runtime.py`

---

## Existing AI Agents

### Production Agents (5)

1. **MetroFlex Events Agent** (`metroflex_ai_agent_enhanced.py`)
   - RAG + intent classification + lead capture
   - Knowledge base: `METROFLEX_COMPLETE_KB_V3.json`

2. **Conversation Agent** (`ghl_conversation_agent.py`)
   - Real-time objection handling
   - Handoff scoring (75%+ = human transfer)

3. **Workflow Generator** (`GHL_Workflow_Generator_FIXED.py`)
   - Multi-channel nurture sequences (email, SMS, LinkedIn)

4. **Licensing Agent** (`licensing_qualification_agent.py`)
   - 4-band qualification: 85+=FAST_TRACK, 70-84=QUALIFIED, 50-69=NURTURE, <50=NOT_QUALIFIED

5. **Gym Member Agent** (`gym_member_agent.py`)
   - Founder's membership qualification

### LLM Configuration
- **Primary Model:** GPT-4o-mini (16x cheaper than GPT-4o)
- **RAG:** ChromaDB with sentence transformers

---

## Effectiveness Metrics

### Conversion Impact

| Area | Expected Improvement |
|------|---------------------|
| Lead Response Time | < 10ms (35-50% conversion lift) |
| Lead Scoring Accuracy | +20-30% better qualification |
| Personalization | +15-25% higher engagement |
| Handoff Timing | 40-60% reduction in churn |
| Follow-up Consistency | 2-3x more touchpoints |

### ROI Projections

**Cost Savings:**
- Manual qualification reduction: $30,000/year
- Recovered opportunities: $180,000/year
- LLM cost efficiency: $10,000+/year

**Revenue Gains:**
- Faster response: +$1,050,000/year
- Better qualification: +$360,000/year
- Reduced churn: +$96,000/year

### Key Metrics to Track

| Metric | Target |
|--------|--------|
| Lead Response Time | < 10 seconds |
| Qualification Accuracy | +25% |
| Conversion Rate | +30% |
| Handoff Satisfaction | +35% |
| Cost per Lead | -40% |

---

## Example Patterns

### Lead Qualification Flow

```apex
@Trigger(event='Lead.Created')
public class LeadQualificationCircuit {
    public void execute(Lead lead) {
        // DMN decision
        DecisionResult qualification = DMN.evaluate('LeadQualification_v1', lead);

        // ML scoring
        Double propensityScore = ML.predict('LeadPropensity', lead);

        // LLM personalization
        String outreach = LLM.generate('PersonalizedOutreach', {
            lead: lead,
            score: propensityScore,
            decision: qualification
        });

        // Action based on qualification
        if (qualification.result == 'FAST_TRACK') {
            Workflow.trigger('HighValueLead', lead, outreach);
        }
    }
}
```

### Conversation Handoff Flow

```apex
@Trigger(event='Conversation.MessageReceived')
public class ConversationHandoffCircuit {
    public void execute(Conversation conversation) {
        // Analyze sentiment
        SentimentResult sentiment = ML.classify('SentimentAnalysis', conversation);

        // Evaluate handoff rules
        DecisionResult decision = DMN.evaluate('HandoffDecision_v1', {
            handoffScore: conversation.score,
            sentiment: sentiment.label,
            objectionCount: conversation.objections
        });

        if (decision.action == 'IMMEDIATE_HANDOFF') {
            Workflow.trigger('ImmediateHandoff', conversation);
        }
    }
}
```

### Multi-Agent Orchestration

```apex
@AgentFlow('FullLeadProcessing')
public class MultiAgentOrchestrator {
    public void execute(Request request) {
        // Intent classification routes to appropriate agent
        IntentResult intent = ML.classify('IntentRouter', request);

        if (intent.domain == 'licensing') {
            // Licensing agent flow
            DecisionResult qualification = DMN.evaluate('LeadQualification_v1', request);
            String response = LLM.generate('LicensingResponse', { request: request, qualification: qualification });
        }

        if (intent.domain == 'gym_membership') {
            // Gym member agent flow
            String response = LLM.generate('GymMemberResponse', { request: request });
        }

        // Store interaction
        DB.insert('Interaction', request);
    }
}
```

---

## Development Roadmap

### Phase 1: Foundation (Weeks 1-2)
- [x] DMN decision tables (JSON format)
- [x] Circuit Script parser
- [x] Runtime with governor limits
- [ ] Formalize DMNX files for business rule management

### Phase 2: ML Pipeline (Weeks 3-4)
- [ ] Feature store for lead data
- [ ] Propensity model training
- [ ] MLflow integration
- [ ] Sentiment analysis model

### Phase 3: Circuit Runtime (Weeks 5-8)
- [ ] Cloudflare Workers deployment
- [ ] Deno V8 isolate runtime
- [ ] CircuitDB bindings (GHL + Salesforce + Supabase)
- [ ] Centralized logging (Axiom)

### Phase 4: Agent Orchestration (Weeks 9-10)
- [ ] LangGraph integration
- [ ] Multi-agent flows
- [ ] Agent marketplace

### Phase 5: Production (Weeks 11-12)
- [ ] Visual DMN editor
- [ ] Monitoring dashboard
- [ ] Circuit Script marketplace

---

## File Structure

```
Circuitos/
├── Active/
│   ├── circuit-script-runtime/
│   │   ├── poc/                          # Proof of concept
│   │   │   ├── dmn/
│   │   │   │   ├── engine.py             # DMN decision engine
│   │   │   │   ├── lead_qualification.json
│   │   │   │   └── handoff_decision.json
│   │   │   ├── circuit_script/
│   │   │   │   ├── parser.py             # Apex-like parser
│   │   │   │   └── runtime.py            # Execution runtime
│   │   │   └── examples/
│   │   │       ├── lead_qualification_flow.py
│   │   │       ├── conversation_handoff_flow.py
│   │   │       └── multi_agent_orchestration.py
│   │   ├── README.md                     # Full specification
│   │   └── ARCHITECTURE_DIAGRAMS.md
│   ├── metroflex-ghl-website/
│   │   └── AI_Agent/                     # Production agents
│   └── agentforce_emulator/              # Salesforce emulation
├── CODEBASE_COMPREHENSIVE_ANALYSIS.md
├── ARCHITECTURE_QUICK_REFERENCE.md
└── CLAUDE.md                             # This file
```

---

## Quick Commands

```bash
# Run PoC demos
cd Active/circuit-script-runtime/poc
python examples/lead_qualification_flow.py
python examples/conversation_handoff_flow.py
python examples/multi_agent_orchestration.py

# Test DMN engine directly
python -m dmn.engine

# Test parser
python -m circuit_script.parser
```

---

## Key Decisions Log

| Date | Decision | Rationale |
|------|----------|-----------|
| 2025-11-19 | Use JSON for DMN tables (not XML) | Easier to read/edit, works with existing tooling |
| 2025-11-19 | Governor limits match Salesforce | Familiar to developers, proven limits |
| 2025-11-19 | GPT-4o-mini as default LLM | 16x cost savings, sufficient quality |
| 2025-11-19 | Python PoC before Cloudflare | Faster iteration, integrates with existing agents |

---

## Notes for Future Sessions

1. **When modifying DMN rules:** Update both the JSON file and test in examples
2. **When adding new services:** Register in `runtime.py` `_register_services()` method
3. **When extending parser:** Add token types in `TokenType` enum, handle in `_parse_*` methods
4. **Performance target:** < 10ms for Circuit Script execution (excluding LLM calls)

---

*Last updated: 2025-11-19*
