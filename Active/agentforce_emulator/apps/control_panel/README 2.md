# Control Panel (Placeholder)

The control panel is a lightweight React/Next.js application for inspecting agent runs,
reviewing action outcomes, and replaying decision traces. Scaffold steps:

1. `npm create vite@latest control-panel -- --template react-ts` (or Next.js equivalent).
2. Configure `.env` with `VITE_AGENT_RUNTIME_URL=http://localhost:8002`.
3. Implement pages for:
   - Run history timeline
   - Opportunity drill-down (scores, signals, outcomes)
   - Telemetry dashboard embedding Grafana panels
4. Communicate with the runtime via `/api/v1/agents/lost-opportunity/run` and future `/runs` endpoints.

This README is a placeholder to reserve folder structure in version control.
