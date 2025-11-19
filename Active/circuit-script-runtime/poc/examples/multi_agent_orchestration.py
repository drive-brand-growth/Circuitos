"""
Example: Multi-Agent Orchestration Flow

Demonstrates Circuit Script orchestrating multiple AI agents:
- Intent classification to route to appropriate agent
- Agent chaining for complex workflows
- Unified data layer (CircuitDB)
- Governor limits across all agents
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from circuit_script.runtime import CircuitScriptRuntime


# Circuit Script for Multi-Agent Orchestration
MULTI_AGENT_SCRIPT = '''
@AgentFlow('FullLeadProcessing')
public class MultiAgentOrchestrator {
    public void execute(Request request) {
        // Step 1: Classify intent to route to appropriate agent
        IntentResult intent = ML.classify('IntentRouter', request);

        System.log('Intent classified');

        // Step 2: Route to domain-specific agent
        if (intent == 'licensing') {
            // Licensing Agent Flow
            DecisionResult qualification = DMN.evaluate('LeadQualification_v1', request);
            Double propensity = ML.predict('LicensingPropensity', request);

            String response = LLM.generate('LicensingResponse', {
                request: request,
                qualification: qualification,
                propensity: propensity
            });

            System.log('Licensing agent processed request');
        }

        if (intent == 'gym_membership') {
            // Gym Member Agent Flow
            DecisionResult membership = DMN.evaluate('MembershipQualification', request);

            String response = LLM.generate('GymMemberResponse', {
                request: request,
                membership: membership
            });

            System.log('Gym member agent processed request');
        }

        if (intent == 'general_inquiry') {
            // General RAG Agent Flow
            String response = LLM.generate('GeneralResponse', {
                request: request
            });

            System.log('General agent processed request');
        }

        // Step 3: Generate workflow based on agent response
        Workflow workflow = Workflow.trigger('FollowUpSequence', request);

        System.log('Workflow generated');

        // Step 4: Store interaction in CircuitDB
        DB.insert('Interaction', request);

        System.log('Interaction logged to CircuitDB');
    }
}
'''


def demo_multi_agent_orchestration():
    """Demonstrate multi-agent orchestration"""

    print("=" * 60)
    print("CIRCUIT SCRIPT MULTI-AGENT ORCHESTRATION DEMO")
    print("=" * 60)

    # Initialize runtime
    runtime = CircuitScriptRuntime()
    runtime.register_script(MULTI_AGENT_SCRIPT)

    # Test requests
    test_requests = [
        {
            "id": "req_001",
            "message": "I need commercial trucking licenses for my 10-truck fleet",
            "source": "website_chat",
            "contact": {
                "name": "John Smith",
                "email": "john@abctransport.com",
                "company": "ABC Transport"
            },
            "timeInBusiness": 5,
            "vehicleCount": 10,
            "annualRevenue": 500000
        },
        {
            "id": "req_002",
            "message": "I want to learn about the founder's membership at MetroFlex",
            "source": "instagram_dm",
            "contact": {
                "name": "Sarah Johnson",
                "email": "sarah@email.com"
            },
            "fitnessGoal": "strength_training",
            "experience": "intermediate"
        },
        {
            "id": "req_003",
            "message": "What are your business hours?",
            "source": "facebook_messenger",
            "contact": {
                "name": "Mike Brown",
                "email": "mike@email.com"
            }
        }
    ]

    for i, request in enumerate(test_requests, 1):
        print(f"\n{'='*60}")
        print(f"TEST CASE {i}: {request['id']}")
        print(f"{'='*60}")

        print(f"\nRequest Details:")
        print(f"  - Source: {request['source']}")
        print(f"  - Contact: {request['contact']['name']}")
        print(f"  - Message: \"{request['message']}\"")

        # Execute the circuit
        result = runtime.execute(
            "MultiAgentOrchestrator",
            "execute",
            {"request": request}
        )

        print(f"\nExecution Logs:")
        for log in result["logs"]:
            print(f"  → {log}")

        print(f"\nGovernor Limits:")
        gov = result["governor_usage"]
        print(f"  - CPU Time: {gov['cpu_time_ms']}ms / 30,000ms")
        print(f"  - API Calls: {gov['api_calls']} / 50")
        print(f"  - Queries: {gov['queries']} / 100")

    print(f"\n{'='*60}")
    print("DEMO COMPLETE")
    print("="*60)

    print("\n📊 KEY TAKEAWAYS:")
    print("  1. Single entry point routes to specialized agents")
    print("  2. Each agent uses DMN + ML + LLM as needed")
    print("  3. Unified CircuitDB stores all interactions")
    print("  4. Governor limits span entire flow")
    print("  5. Business users write Apex-like code without knowing internals")


if __name__ == "__main__":
    demo_multi_agent_orchestration()
