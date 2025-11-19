# Circuit Script + DMN + ML + LLM Integration PoC

This proof-of-concept demonstrates how Circuit Script (Apex-like syntax) integrates with DMN decision tables, ML models, and LLMs to create a unified business automation platform.

## Overview

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

## Quick Start

```bash
# Run all demos
cd poc

# Lead Qualification Demo
python examples/lead_qualification_flow.py

# Conversation Handoff Demo
python examples/conversation_handoff_flow.py

# Multi-Agent Orchestration Demo
python examples/multi_agent_orchestration.py
```

## Components

### 1. DMN Engine (`dmn/engine.py`)

Evaluates business rules defined in DMN decision tables:

```python
from dmn.engine import DMNEngine

engine = DMNEngine()
result = engine.evaluate('LeadQualification_v1', {
    'timeInBusiness': 5,
    'vehicleCount': 10,
    'annualRevenue': 500000
})

print(result.outputs)  # {'qualification': 'FAST_TRACK', 'score': 95, ...}
```

**Decision Tables Included:**
- `LeadQualification_v1` - Lead scoring and routing
- `HandoffDecision_v1` - Conversation handoff rules

### 2. Circuit Script Parser (`circuit_script/parser.py`)

Parses Apex-like syntax into an AST:

```python
from circuit_script.parser import parse_circuit_script

ast = parse_circuit_script('''
    @Trigger(event='Lead.Created')
    public class MyCircuit {
        public void execute(Lead lead) {
            DecisionResult result = DMN.evaluate('LeadQualification', lead);
        }
    }
''')
```

**Supported Syntax:**
- Class definitions with decorators
- Method declarations
- Variable assignments
- Object literals
- Method chaining
- If/else statements
- Service calls (DMN, ML, LLM, Workflow, DB)

### 3. Circuit Script Runtime (`circuit_script/runtime.py`)

Executes Circuit Scripts with integrated services:

```python
from circuit_script.runtime import CircuitScriptRuntime

runtime = CircuitScriptRuntime()
runtime.register_script(my_script)

result = runtime.execute('MyCircuit', 'execute', {'lead': lead_data})
```

**Built-in Services:**
- `DMN.evaluate()` - Evaluate decision tables
- `ML.predict()` - Get ML predictions
- `ML.classify()` - Classify text/data
- `LLM.generate()` - Generate LLM responses
- `Workflow.trigger()` - Trigger automation workflows
- `DB.query()` / `DB.insert()` - CircuitDB operations
- `System.log()` / `System.debug()` - Logging

**Governor Limits:**
- CPU Time: 30,000ms
- API Calls: 50
- Queries: 100
- DML Statements: 150
- Heap Size: 128MB

## Example Circuit Scripts

### Lead Qualification

```apex
@Trigger(event='Lead.Created')
public class LeadQualificationCircuit {
    public void execute(Lead lead) {
        // DMN decision
        DecisionResult eligibility = DMN.evaluate('LeadQualification_v1', lead);

        // ML scoring
        Double propensityScore = ML.predict('LeadPropensity', lead);

        // LLM personalization
        String outreach = LLM.generate('PersonalizedOutreach', {
            lead: lead,
            score: propensityScore,
            decision: eligibility
        });

        // Action
        if (eligibility.result == 'FAST_TRACK') {
            Workflow.trigger('HighValueLead', lead, outreach);
        }
    }
}
```

### Conversation Handoff

```apex
@Trigger(event='Conversation.MessageReceived')
public class ConversationHandoffCircuit {
    public void execute(Conversation conversation) {
        // Analyze sentiment
        SentimentResult sentiment = ML.classify('SentimentAnalysis', conversation);

        // Evaluate handoff rules
        DecisionResult decision = DMN.evaluate('HandoffDecision_v1', {
            handoffScore: conversation.score,
            sentiment: sentiment,
            objectionCount: conversation.objections
        });

        if (decision.action == 'IMMEDIATE_HANDOFF') {
            Workflow.trigger('ImmediateHandoff', conversation);
        }
    }
}
```

## Directory Structure

```
poc/
├── dmn/
│   ├── engine.py              # DMN decision engine
│   ├── lead_qualification.json # Lead scoring rules
│   └── handoff_decision.json   # Handoff rules
├── circuit_script/
│   ├── parser.py              # Apex-like parser
│   └── runtime.py             # Execution runtime
├── examples/
│   ├── lead_qualification_flow.py
│   ├── conversation_handoff_flow.py
│   └── multi_agent_orchestration.py
└── README.md
```

## Integration Points

### With Existing Agents

The Circuit Script runtime can wrap your existing AI agents:

```python
# In runtime.py, add to _register_services()
def licensing_agent(lead):
    # Import your existing agent
    from AI_Agent.licensing_qualification_agent import LicensingAgent
    agent = LicensingAgent()
    return agent.qualify(lead)

context.functions['Agent.licensing'] = licensing_agent
```

### With OpenAI

Replace LLM stubs with real OpenAI calls:

```python
def llm_generate(prompt_id: str, context_data: Any) -> str:
    from openai import OpenAI
    client = OpenAI()

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": build_prompt(prompt_id, context_data)}]
    )
    return response.choices[0].message.content
```

### With ChromaDB

Add RAG capabilities:

```python
def rag_search(query: str, collection: str) -> List[Dict]:
    import chromadb
    client = chromadb.Client()
    collection = client.get_collection(collection)
    results = collection.query(query_texts=[query], n_results=5)
    return results
```

## Next Steps

1. **Production Runtime**: Deploy to Cloudflare Workers with Deno V8 isolates
2. **Visual DMN Editor**: Create UI for business analysts to edit rules
3. **ML Pipeline**: Connect to real ML models (propensity, sentiment, etc.)
4. **Circuit Script Marketplace**: Pre-built templates for common flows
5. **Monitoring Dashboard**: Track governor usage, performance, costs

## Key Benefits

| Feature | Benefit |
|---------|---------|
| Apex-like Syntax | Familiar to Salesforce developers |
| Governor Limits | Prevents runaway processes |
| DMN Integration | Business analysts can modify rules |
| ML Abstraction | Simple API for complex models |
| LLM Integration | Consistent prompting patterns |
| Unified Data | CircuitDB for GHL + Salesforce + Supabase |

## Related Documentation

- [Circuit Script Specification](../README.md)
- [Architecture Diagrams](../ARCHITECTURE_DIAGRAMS.md)
- [2-Month Sprint Plan](../2_MONTH_SPRINT_PLAN.md)
