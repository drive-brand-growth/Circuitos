# Virtual Salesforce AgentForce Environment

A local testing environment that simulates Salesforce AgentForce functionality, allowing you to design, test, and iterate on agents without requiring Salesforce access or licenses.

## Features

- **Mock Salesforce Data Layer** - Simulates Salesforce objects (Opportunity, Account, Contact, Custom Objects)
- **Atlas Reasoning Engine Simulator** - LLM integration for reasoning and prompt testing
- **Agent Builder Interface** - Configuration interface for agent instructions, actions, and data sources
- **Action Framework** - Simulates agent actions (query records, create tasks, send alerts)
- **Data Source Connectors** - Mock integrations for Data Cloud, external APIs (Bombora, LinkedIn)
- **Testing & Validation Tools** - Test agent logic, validate prompts, measure accuracy

## Quick Start

### Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
# Create .env file with your API keys:
# OPENAI_API_KEY=sk-...
# ANTHROPIC_API_KEY=sk-ant-...
# LLM_PROVIDER=openai  # or anthropic

# Initialize database
python -m virtual_agentforce.data.init_db

# Create sample data (optional)
python -m virtual_agentforce.data.init_db --sample-data

# Run the server
uvicorn virtual_agentforce.main:app --reload

# Or test installation
python scripts/quick_test.py
```

### Create Your First Agent

```python
from virtual_agentforce.core.agent import Agent
from virtual_agentforce.core.atlas import AtlasEngine

# Create an agent configuration
agent_config = {
    "name": "Lost Opp Reactivation Agent",
    "instructions": "Analyze lost opportunities and identify reactivation signals...",
    "data_sources": ["Opportunity", "Account", "Contact"],
    "actions": ["query", "update", "create_task"]
}

agent = Agent.from_config(agent_config)
results = await agent.execute()
```

## Project Structure

```
virtual-agentforce/
├── virtual_agentforce/       # Main package
│   ├── core/                 # Core agent framework
│   │   ├── agent.py         # Agent execution engine
│   │   ├── atlas.py         # Atlas Reasoning Engine simulator
│   │   └── actions.py       # Action framework
│   ├── data/                 # Mock Salesforce data layer
│   │   ├── models.py        # SQLAlchemy models
│   │   ├── soql.py          # SOQL query parser/simulator
│   │   └── init_db.py       # Database initialization
│   ├── integrations/        # Mock external integrations
│   │   ├── bombora.py       # Bombora connector
│   │   ├── linkedin.py        # LinkedIn connector
│   │   └── slack.py         # Slack connector
│   ├── agents/               # Agent configurations
│   └── examples/            # Example agent configs
│       └── lost_opp_reactivation/  # Lost Opp Reactivation Agent
├── tests/                    # Test suites
└── requirements.txt         # Python dependencies
```

## Usage Examples

See `/examples` directory for complete agent configurations including:
- Lost Opportunity Reactivation Agent
- Lead Scoring Agent
- Customer Health Agent

## Documentation

- [Usage Guide](./USAGE_GUIDE.md) - Complete usage instructions
- [Example Agents](./virtual_agentforce/examples/README.md) - Example configurations
- [Validation Tools](./virtual_agentforce/validation/README.md) - Backtest and validation tools

## Features Implemented

✅ Mock Salesforce Data Layer (Account, Contact, Opportunity, Custom Objects)  
✅ SOQL Query Parser and Simulator  
✅ Atlas Reasoning Engine (OpenAI/Anthropic LLM integration)  
✅ Agent Configuration and Execution Framework  
✅ Action Framework (Query, Create, Update, Delete, Tasks, Email)  
✅ Mock Data Cloud Connectors (Bombora, LinkedIn)  
✅ Slack Integration (Mock)  
✅ FastAPI REST API  
✅ Lost Opp Reactivation Agent Example  
✅ Validation & Backtest Tools (Historical testing, accuracy metrics)  

## Architecture

The Virtual AgentForce environment simulates:
- **Salesforce Objects**: Standard (Account, Contact, Opportunity) and Custom (Bombora_Intent__c, LinkedIn_Activity__c, etc.)
- **SOQL Queries**: Parses and executes SOQL queries against mock data
- **Atlas Reasoning Engine**: Chain-of-thought reasoning using LLM APIs
- **Agent Framework**: Configuration-based agent execution
- **Actions**: Query, Create, Update, Delete, Tasks, Email, API calls
- **Integrations**: Mock connectors for Bombora, LinkedIn, Slack

## Next Steps

1. Set up your environment variables (`.env` file)
2. Initialize database: `python -m virtual_agentforce.data.init_db --sample-data`
3. Test installation: `python scripts/quick_test.py`
4. Start API: `uvicorn virtual_agentforce.main:app --reload`
5. Try the example agent: See `USAGE_GUIDE.md`

For detailed usage, see [USAGE_GUIDE.md](./USAGE_GUIDE.md).

