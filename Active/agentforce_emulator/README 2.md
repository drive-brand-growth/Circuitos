# Agentforce Lost Opportunity Emulator

Local-first sandbox that emulates Salesforce Agentforce behaviors for the DRN Lost Opportunity agent. The stack runs entirely on a developer workstation or in a Docker Compose environment and mirrors the key Agentforce building blocks: CRM data access, enrichment signals, autonomous reasoning, and action routing.

## Capabilities

- Lightweight CRM/data-cloud API with Opportunity, Account, Contact, and enrichment signal objects.
- Atlas-inspired reasoning graph that scores lost opportunities and produces outreach/action plans.
- Configurable scoring model (`configs/scoring_rules.yaml`) aligned with DRN production logic.
- CLI, REST, and web UI triggers for weekly “lost opportunity” sweeps.
- Postgres-backed persistence (runs + actions), Redis event bus, OpenTelemetry traces, and structured audit logs.
- Seed datasets and synthetic signal generators for offline experimentation.

## Stack Overview

| Layer | Tech | Purpose |
| --- | --- | --- |
| API | FastAPI, Pydantic v2 | REST/GraphQL-style endpoints for CRM and agent runtime |
| Data | Postgres, SQLAlchemy, Alembic | Persistent storage for CRM objects and signals |
| Orchestration | LangGraph, LangChain, Redis | Planner/executor graph and tool routing |
| Messaging | Redis Streams | Event bus for agent actions and telemetry |
| Observability | OpenTelemetry, Grafana (optional) | Agent traces, metrics, audit trail |

## Repository Layout

```
agentforce_emulator/
├── apps/control_panel/        # Web dashboard (Vite + React)
├── cli/run_agent.py           # CLI trigger for emulator runs
├── configs/                   # Scoring rules, agent settings
├── docs/                      # High-level architecture + deployment notes
├── seed_data/                 # Synthetic CRM + signal CSVs
├── services/
│   ├── agent_runtime/         # Atlas-style reasoning service
│   └── crm_api/               # CRM + signal APIs
├── tests/                     # Integration and regression tests
├── docker-compose.local.yml   # Dev stack orchestration
└── pyproject.toml             # Python dependencies and tooling config
```

## Getting Started

1. **Install prerequisites**
   - Python 3.12+
   - uv or Poetry (for dependency management)
   - Docker Desktop (for Postgres/Redis)

2. **Clone & bootstrap**
   ```bash
   git clone <repo-url>
   cd agentforce_emulator
   uv sync  # or: poetry install
   cp .env.example .env
   ```

3. **Launch infrastructure**
   ```bash
   docker compose -f docker-compose.local.yml up -d
   ```

4. **Run services**
   ```bash
   uv run fastapi dev services/crm_api/app.py
   uv run fastapi dev services/agent_runtime/app.py
   ```

5. **Launch web control panel (optional)**
   ```bash
   cd apps/control_panel
   npm install
   npm run dev -- --host
   ```

6. **Trigger lost opportunity sweep**
   ```bash
   uv run python cli/run_agent.py --preset weekly
   ```

## Development Flow

- Update scoring logic in `configs/scoring_rules.yaml` and regenerate tests with `uv run pytest`.
- Extend CRM schema by adding SQLAlchemy models in `services/crm_api/models.py` and running Alembic migrations.
- Add new tools or actions in `services/agent_runtime/utils/tools.py` and register them inside the LangGraph workflow.
- Use the React control panel (scaffolded in `apps/control_panel`) for visual inspection and replay of agent decisions.

## Next Steps

- Flesh out integration tests in `tests/integration/` with real DRN anonymized datasets.
- Wire up Slack/webhook mocks in `services/agent_runtime/utils/actions.py` for full downstream automation rehearsals.
- Connect to enterprise LLM endpoints (Einstein GPT, OpenAI, Anthropic) via environment-based provider adapters.

---

For deep context on the production Agentforce implementation, review `docs/agentforce_overview.md` and the DRN architecture reference embedded in `CAIO_Training_Platform/modules/module3_agentforce/lessons/lesson3_1_agentforce_overview.json`.


