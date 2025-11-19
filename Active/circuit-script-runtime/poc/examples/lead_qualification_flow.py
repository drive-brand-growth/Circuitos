"""
Example: Lead Qualification Flow

Demonstrates Circuit Script orchestrating:
- DMN decision tables for business rules
- ML models for propensity scoring
- LLM for personalized outreach
- Workflow automation
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from circuit_script.runtime import CircuitScriptRuntime


# Circuit Script for Lead Qualification
LEAD_QUALIFICATION_SCRIPT = '''
@Trigger(event='Lead.Created')
public class LeadQualificationCircuit {
    public void execute(Lead lead) {
        // Step 1: Evaluate business rules with DMN
        DecisionResult qualification = DMN.evaluate('LeadQualification_v1', lead);

        // Step 2: Get ML propensity score
        Double propensityScore = ML.predict('LeadPropensity', lead);

        // Step 3: Classify lead intent
        IntentResult intent = ML.classify('LeadIntent', lead);

        // Step 4: Generate personalized outreach with LLM
        String outreach = LLM.generate('PersonalizedOutreach', {
            lead: lead,
            qualification: qualification,
            propensity: propensityScore,
            intent: intent
        });

        // Step 5: Take action based on qualification
        if (qualification.result == 'FAST_TRACK') {
            Workflow.trigger('HighValueLead', lead, outreach);
            System.log('Fast track lead - immediate callback scheduled');
        }

        if (qualification.result == 'QUALIFIED') {
            Workflow.trigger('NurtureSequence', lead, outreach);
            System.log('Qualified lead - nurture sequence started');
        }

        if (qualification.result == 'NURTURE') {
            Workflow.trigger('EducationalContent', lead, outreach);
            System.log('Nurture lead - educational content scheduled');
        }

        // Log completion
        System.debug(qualification);
    }
}
'''


def demo_lead_qualification():
    """Demonstrate the lead qualification flow"""

    print("=" * 60)
    print("CIRCUIT SCRIPT + DMN + ML + LLM INTEGRATION DEMO")
    print("Lead Qualification Flow")
    print("=" * 60)

    # Initialize runtime
    runtime = CircuitScriptRuntime()
    runtime.register_script(LEAD_QUALIFICATION_SCRIPT)

    # Test cases
    test_leads = [
        {
            "name": "ABC Transport Co",
            "timeInBusiness": 5,
            "vehicleCount": 20,
            "annualRevenue": 1000000,
            "hasExistingLicense": True,
            "inquiry": "I need commercial trucking licenses for my fleet"
        },
        {
            "name": "New Delivery LLC",
            "timeInBusiness": 1,
            "vehicleCount": 3,
            "annualRevenue": 150000,
            "hasExistingLicense": False,
            "inquiry": "How do I get started with delivery permits?"
        },
        {
            "name": "StartupHaul",
            "timeInBusiness": 0,
            "vehicleCount": 1,
            "annualRevenue": 40000,
            "hasExistingLicense": False,
            "inquiry": "What licenses do I need for a single truck?"
        }
    ]

    for i, lead in enumerate(test_leads, 1):
        print(f"\n{'='*60}")
        print(f"TEST CASE {i}: {lead['name']}")
        print(f"{'='*60}")

        print(f"\nInput Lead:")
        print(f"  - Time in Business: {lead['timeInBusiness']} years")
        print(f"  - Vehicle Count: {lead['vehicleCount']}")
        print(f"  - Annual Revenue: ${lead['annualRevenue']:,}")
        print(f"  - Has Existing License: {lead['hasExistingLicense']}")
        print(f"  - Inquiry: {lead['inquiry']}")

        # Execute the circuit
        result = runtime.execute(
            "LeadQualificationCircuit",
            "execute",
            {"lead": lead}
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
    print("  1. Circuit Script provides Apex-like syntax for business logic")
    print("  2. DMN decision tables handle qualification rules")
    print("  3. ML models predict lead propensity")
    print("  4. LLM generates personalized outreach")
    print("  5. Governor limits ensure resource control")


if __name__ == "__main__":
    demo_lead_qualification()
