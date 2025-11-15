"""
Circuit OS Examples
Demonstrates how to build and execute circuits
"""

import asyncio
from circuit_engine import (
    Circuit,
    CircuitScriptEngine,
    CircuitContext,
    TriggerEvent,
    # Triggers
    SimpleTrigger,
    on_lead_created,
    on_hot_lead,
    # Actions
    GetLeadDataAction,
    ScrapeWebsiteAction,
    SearchNewsAction,
    RetrieveCompanyIntelAction,
    PredictLeadScoreAction,
    QueryCompetitorsAction,
    CreateOpportunityAction,
    SendSlackAlertAction,
    ConditionalAction,
    UpdateLeadAction,
    LogAction,
)


# ============================================================================
# EXAMPLE 1: Lead Processing Circuit (Full AI Pipeline)
# ============================================================================

def create_lead_processing_circuit() -> Circuit:
    """
    Complete lead processing workflow with AI

    This circuit demonstrates Circuit OS's competitive advantage:
    - Deterministic execution (like Apex)
    - ML predictions (Apex can't do this)
    - RAG retrieval (Apex can't do this)
    - Knowledge graph queries (Apex can't do this)
    - MCP integrations (Apex would need expensive APIs)
    """
    circuit = Circuit(
        name="lead_processing_ai",
        description="Process new leads with full AI enrichment"
    )

    # Trigger: When lead is created
    circuit.add_trigger(on_lead_created())

    # Action sequence
    circuit.add_action(LogAction("Processing lead: {lead_id}"))
    circuit.add_action(GetLeadDataAction())  # Get lead data (like SOQL)
    circuit.add_action(ScrapeWebsiteAction())  # Scrape company website (MCP)
    circuit.add_action(SearchNewsAction())  # Search recent news (MCP)
    circuit.add_action(RetrieveCompanyIntelAction())  # RAG retrieval
    circuit.add_action(PredictLeadScoreAction())  # ML prediction
    circuit.add_action(QueryCompetitorsAction())  # Knowledge graph

    # Conditional: Create opportunity if hot lead
    circuit.add_action(ConditionalAction(
        condition=lambda ctx: ctx.get("lead_score", 0) > 80,
        true_action=CreateOpportunityAction(),
        false_action=UpdateLeadAction({"status": "Nurture"})
    ))

    circuit.add_action(SendSlackAlertAction("#sales-alerts"))
    circuit.add_action(LogAction("Lead processing complete. Score: {lead_score}"))

    return circuit


# ============================================================================
# EXAMPLE 2: Hot Lead Alert Circuit
# ============================================================================

def create_hot_lead_alert_circuit() -> Circuit:
    """
    Immediate action on hot leads (score > 90)
    """
    circuit = Circuit(
        name="hot_lead_alert",
        description="Urgent alerts for hot leads"
    )

    # Trigger: High lead score detected
    circuit.add_trigger(on_hot_lead(score_threshold=90, priority=10))

    circuit.add_action(LogAction("🔥 HOT LEAD DETECTED! Score: {lead_score}"))
    circuit.add_action(GetLeadDataAction())
    circuit.add_action(CreateOpportunityAction())
    circuit.add_action(SendSlackAlertAction("#sales-urgent"))

    return circuit


# ============================================================================
# EXAMPLE 3: Competitor Intelligence Circuit
# ============================================================================

def create_competitor_intel_circuit() -> Circuit:
    """
    Monitor competitor mentions and gather intelligence
    """
    circuit = Circuit(
        name="competitor_monitoring",
        description="Track competitor activity"
    )

    # Trigger: When competitor is mentioned
    circuit.add_trigger(SimpleTrigger(
        TriggerEvent.COMPETITOR_MENTIONED,
        priority=8
    ))

    circuit.add_action(LogAction("Competitor mentioned: {competitor_name}"))
    circuit.add_action(SearchNewsAction())
    circuit.add_action(QueryCompetitorsAction())
    circuit.add_action(RetrieveCompanyIntelAction())
    circuit.add_action(SendSlackAlertAction("#competitive-intel"))

    return circuit


# ============================================================================
# EXAMPLE 4: Simple Data Circuit (Apex-equivalent)
# ============================================================================

def create_simple_data_circuit() -> Circuit:
    """
    Simple circuit using only data actions (Apex-equivalent)
    Demonstrates that Circuit OS can do everything Apex does
    """
    circuit = Circuit(
        name="simple_opportunity_creation",
        description="Basic opportunity creation (Apex-style)"
    )

    circuit.add_trigger(on_lead_created(
        conditions={"status": "Qualified"}
    ))

    circuit.add_action(GetLeadDataAction())
    circuit.add_action(CreateOpportunityAction())
    circuit.add_action(UpdateLeadAction({"status": "Converted"}))
    circuit.add_action(LogAction("Opportunity created for {company_name}"))

    return circuit


# ============================================================================
# MAIN DEMO
# ============================================================================

async def demo():
    """
    Demonstrate Circuit OS capabilities
    """
    print("=" * 60)
    print("CIRCUIT OS DEMO")
    print("Salesforce Apex + AI Native Operations")
    print("=" * 60)
    print()

    # Initialize engine
    engine = CircuitScriptEngine()

    # Register circuits
    print("Registering circuits...")
    engine.register(create_lead_processing_circuit())
    engine.register(create_hot_lead_alert_circuit())
    engine.register(create_competitor_intel_circuit())
    engine.register(create_simple_data_circuit())

    print(f"✓ Registered {len(engine.list())} circuits")
    print()

    # List circuits
    print("Registered Circuits:")
    for circuit_info in engine.list_circuits():
        print(f"  - {circuit_info['name']}: {circuit_info['action_count']} actions")
    print()

    # ========================================================================
    # DEMO 1: Lead Processing with Full AI
    # ========================================================================
    print("\n" + "=" * 60)
    print("DEMO 1: Lead Processing Circuit (Full AI Pipeline)")
    print("=" * 60)

    lead_data = {
        "lead_id": "lead_12345",
        "status": "New"
    }

    print(f"\nExecuting: lead_processing_ai")
    print(f"Input: {lead_data}")
    print()

    context = await engine.execute_circuit("lead_processing_ai", lead_data)

    print("\n--- Results ---")
    print(f"Status: {context.get_metadata().get('status')}")
    print(f"Lead Score: {context.get('lead_score')}")
    print(f"Opportunity Created: {context.get('opportunity_id')}")
    print(f"Company Intelligence: {len(context.get('company_intelligence', []))} documents")
    print(f"Competitors Found: {len(context.get('competitors', []))}")
    print()

    # ========================================================================
    # DEMO 2: Hot Lead Alert
    # ========================================================================
    print("\n" + "=" * 60)
    print("DEMO 2: Hot Lead Alert Circuit")
    print("=" * 60)

    hot_lead_data = {
        "lead_id": "lead_99999",
        "lead_score": 95  # Very hot!
    }

    print(f"\nExecuting: hot_lead_alert")
    print(f"Input: {hot_lead_data}")
    print()

    context = await engine.execute_circuit("hot_lead_alert", hot_lead_data)

    print("\n--- Results ---")
    print(f"Status: {context.get_metadata().get('status')}")
    print(f"Slack Alert Sent: {context.get('slack_notification_sent')}")
    print()

    # ========================================================================
    # DEMO 3: Event-Driven Execution
    # ========================================================================
    print("\n" + "=" * 60)
    print("DEMO 3: Event-Driven Execution")
    print("=" * 60)

    print("\nPublishing LEAD_CREATED event...")
    triggered = await engine.publish_event(
        TriggerEvent.LEAD_CREATED,
        {"lead_id": "lead_auto_123", "status": "Qualified"}
    )

    print(f"✓ Triggered {len(triggered)} circuits: {', '.join(triggered)}")
    print()

    # Give queue time to process
    await asyncio.sleep(0.5)

    # ========================================================================
    # METRICS
    # ========================================================================
    print("\n" + "=" * 60)
    print("ENGINE METRICS")
    print("=" * 60)

    metrics = engine.get_metrics()
    print(f"\nTotal Executions: {metrics['total_executions']}")
    print(f"Successful: {metrics['successful_executions']}")
    print(f"Failed: {metrics['failed_executions']}")
    print(f"Success Rate: {metrics['success_rate']:.1%}")
    print(f"Average Duration: {metrics['average_duration']:.3f}s")
    print(f"Registered Circuits: {metrics['registered_circuits']}")
    print(f"Total Actions: {metrics['total_actions']}")
    print()

    # ========================================================================
    # COMPETITIVE ADVANTAGE SUMMARY
    # ========================================================================
    print("\n" + "=" * 60)
    print("COMPETITIVE ADVANTAGE vs SALESFORCE APEX")
    print("=" * 60)
    print()
    print("✓ Deterministic execution        (Apex has this)")
    print("✓ Data operations (SOQL/DML)     (Apex has this)")
    print("✓ Workflow automation            (Apex has this)")
    print()
    print("✓ ML predictions as native ops   (Apex CAN'T do this)")
    print("✓ RAG retrieval for context      (Apex CAN'T do this)")
    print("✓ Knowledge graph queries        (Apex CAN'T do this)")
    print("✓ MCP integrations (7 sources)   (Apex would need expensive APIs)")
    print("✓ Self-improving with AutoML     (Apex CAN'T do this)")
    print()
    print("Cost: $100/month vs $150K/year Salesforce")
    print("Gross Margin: 95% vs 70-80% industry")
    print()
    print("=" * 60)
    print()


if __name__ == "__main__":
    asyncio.run(demo())
