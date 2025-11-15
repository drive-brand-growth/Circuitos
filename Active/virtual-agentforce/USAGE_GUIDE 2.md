# Usage Guide

Complete guide to using the Virtual Salesforce AgentForce environment.

## Quick Start

### 1. Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
# Create .env file with your API keys (see .env.example)
```

### 2. Initialize Database

```bash
# Initialize database schema
python -m virtual_agentforce.data.init_db

# Create sample test data
python -m virtual_agentforce.data.init_db --sample-data
```

### 3. Run Server

```bash
uvicorn virtual_agentforce.main:app --reload
```

The API will be available at `http://localhost:8000`

## Using the API

### Execute SOQL Query

```bash
curl -X POST "http://localhost:8000/soql/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "SELECT Id, Name, StageName FROM Opportunity WHERE StageName = '\''Closed Lost'\'' LIMIT 10"
  }'
```

### Execute Agent

```bash
curl -X POST "http://localhost:8000/agents/execute" \
  -H "Content-Type: application/json" \
  -d '{
    "config": {
      "name": "Test Agent",
      "instructions": "You are a helpful AI agent.",
      "data_sources": ["Opportunity"],
      "actions": ["query", "create"]
    },
    "task": "Find all lost opportunities",
    "context": {}
  }'
```

### Use Atlas Reasoning Engine

```bash
curl -X POST "http://localhost:8000/atlas/reason" \
  -H "Content-Type: application/json" \
  -d '{
    "system_prompt": "You are an AI reasoning agent.",
    "user_prompt": "Should we reactivate this lost opportunity?",
    "context": {
      "opportunity_id": "006XXXXXX",
      "loss_reason": "Budget"
    }
  }'
```

## Using the Python API

### Basic Agent Execution

```python
from virtual_agentforce.core.agent import Agent, AgentConfig
from virtual_agentforce.data.database import SessionLocal

# Create agent configuration
config = AgentConfig(
    name="My Agent",
    instructions="You are a helpful AI agent that analyzes sales opportunities.",
    data_sources=["Opportunity", "Account"],
    actions=["query", "create", "update"]
)

# Create session and agent
session = SessionLocal()
agent = Agent(config, session)

# Execute agent
result = await agent.execute(
    task="Find all opportunities with Amount > 100000",
    context={}
)

print(result.reasoning)
print(result.results)
```

### Lost Opp Reactivation Agent

```python
from virtual_agentforce.examples.lost_opp_reactivation import get_lost_opp_agent_config
from virtual_agentforce.core.agent import Agent
from virtual_agentforce.data.database import SessionLocal

# Load pre-configured agent
config = get_lost_opp_agent_config()
session = SessionLocal()
agent = Agent.from_config(config, session)

# Execute analysis
result = await agent.execute(
    task="Analyze lost opportunities from the last 90-120 days for reactivation signals",
    context={}
)

if result.success:
    print("✅ Agent executed successfully")
    print(f"Actions executed: {len(result.actions_executed)}")
    print(f"Reasoning: {result.reasoning}")
else:
    print(f"❌ Error: {result.error}")
```

### Query Data Directly

```python
from virtual_agentforce.data.soql import execute_soql
from virtual_agentforce.data.database import SessionLocal

session = SessionLocal()

# Execute SOQL query
results = execute_soql(
    session,
    "SELECT Id, Name, StageName, Amount FROM Opportunity WHERE Amount > 50000 LIMIT 10"
)

for record in results:
    print(f"{record['Name']}: ${record['Amount']}")
```

### Use Integrations

```python
from virtual_agentforce.integrations import BomboraConnector, LinkedInConnector
from virtual_agentforce.data.database import SessionLocal

session = SessionLocal()

# Get Bombora intent data
bombora = BomboraConnector(session)
intent_data = bombora.get_intent_data(
    account_id="001XXXXXX",
    topics=["ALPR solutions"],
    days_back=30
)

# Get LinkedIn activities
linkedin = LinkedInConnector(session)
activities = linkedin.get_activities(
    account_id="001XXXXXX",
    activity_types=["Job Change", "Company Update"],
    days_back=120
)

# Send Slack alert
from virtual_agentforce.integrations import SlackConnector

slack = SlackConnector()
slack.send_alert(
    channel="#sales-urgent-leads",
    title="S-Tier Lead Identified",
    message="ABC Credit Union scored 87/100",
    priority="urgent",
    fields=[
        {"title": "Account", "value": "ABC Credit Union"},
        {"title": "Score", "value": "87 (S-Tier)"},
    ]
)
```

## Creating Custom Agents

### 1. Define Agent Configuration

```python
my_agent_config = {
    "name": "Custom Lead Scoring Agent",
    "instructions": """
    You are a lead scoring agent.
    Analyze leads and assign scores based on:
    - Industry fit
    - Company size
    - Engagement level
    """,
    "data_sources": ["Lead", "Account", "Contact"],
    "actions": ["query", "update", "create_task"],
    "invocation_trigger": "on_lead_creation",
}
```

### 2. Create and Execute

```python
from virtual_agentforce.core.agent import Agent
from virtual_agentforce.data.database import SessionLocal

session = SessionLocal()
agent = Agent.from_config(my_agent_config, session)

result = await agent.execute(
    task="Score all new leads created today",
    context={"date": "2025-01-15"}
)
```

## Testing

### Run Tests

```bash
pytest tests/
```

### Test Agent Execution

```python
import pytest
from virtual_agentforce.core.agent import Agent, AgentConfig
from virtual_agentforce.data.database import SessionLocal, init_database

@pytest.mark.asyncio
async def test_agent_execution():
    init_database()
    session = SessionLocal()
    
    config = AgentConfig(
        name="Test Agent",
        instructions="Test instructions",
        data_sources=["Opportunity"],
        actions=["query"]
    )
    
    agent = Agent(config, session)
    result = await agent.execute("Test task")
    
    assert result.success
    assert result.agent_name == "Test Agent"
```

## Troubleshooting

### Database Issues

If you encounter database errors:

```bash
# Reinitialize database
rm virtual_agentforce.db  # Remove existing database
python -m virtual_agentforce.data.init_db
```

### LLM API Issues

Ensure your API keys are set in `.env`:

```bash
OPENAI_API_KEY=sk-...
# OR
ANTHROPIC_API_KEY=sk-ant-...
```

### SOQL Query Errors

The SOQL parser supports:
- SELECT fields FROM object
- WHERE conditions (=, !=, >, <, >=, <=, LIKE, IN)
- ORDER BY
- LIMIT

Complex queries may need simplification.

## Next Steps

- See `examples/` for more agent configurations
- Check `docs/` for detailed architecture documentation
- Review `tests/` for testing patterns











