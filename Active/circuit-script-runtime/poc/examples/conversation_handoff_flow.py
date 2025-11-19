"""
Example: Conversation Handoff Flow

Demonstrates Circuit Script orchestrating:
- Real-time conversation analysis
- DMN rules for handoff decisions
- ML sentiment analysis
- LLM response generation
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from circuit_script.runtime import CircuitScriptRuntime


# Circuit Script for Conversation Handling
CONVERSATION_HANDOFF_SCRIPT = '''
@Trigger(event='Conversation.MessageReceived')
public class ConversationHandoffCircuit {
    public void execute(Conversation conversation) {
        // Step 1: Analyze sentiment
        SentimentResult sentiment = ML.classify('SentimentAnalysis', conversation);

        // Step 2: Calculate handoff score
        Double handoffScore = ML.predict('HandoffScore', conversation);

        // Step 3: Evaluate handoff decision with DMN
        DecisionResult handoffDecision = DMN.evaluate('HandoffDecision_v1', {
            handoffScore: handoffScore,
            sentiment: sentiment,
            objectionCount: conversation,
            conversationLength: conversation
        });

        // Step 4: Take action based on decision
        if (handoffDecision.action == 'IMMEDIATE_HANDOFF') {
            Workflow.trigger('ImmediateHandoff', conversation);
            System.log('Immediate handoff triggered - human agent alerted');
        }

        if (handoffDecision.action == 'QUEUE_HANDOFF') {
            Workflow.trigger('QueueHandoff', conversation);
            System.log('Handoff queued - agent will join shortly');
        }

        if (handoffDecision.action == 'CONTINUE_AI') {
            // Generate AI response
            String response = LLM.generate('ConversationResponse', {
                conversation: conversation,
                sentiment: sentiment
            });
            System.log('AI continuing conversation');
        }

        System.debug(handoffDecision);
    }
}
'''


def demo_conversation_handoff():
    """Demonstrate the conversation handoff flow"""

    print("=" * 60)
    print("CIRCUIT SCRIPT + DMN + ML + LLM INTEGRATION DEMO")
    print("Conversation Handoff Flow")
    print("=" * 60)

    # Initialize runtime
    runtime = CircuitScriptRuntime()
    runtime.register_script(CONVERSATION_HANDOFF_SCRIPT)

    # Test conversations
    test_conversations = [
        {
            "id": "conv_001",
            "handoffScore": 92,
            "sentiment": "frustrated",
            "objectionCount": 4,
            "conversationLength": 12,
            "lastMessage": "This is ridiculous! I've been waiting for days!"
        },
        {
            "id": "conv_002",
            "handoffScore": 65,
            "sentiment": "neutral",
            "objectionCount": 2,
            "conversationLength": 8,
            "lastMessage": "Can you clarify the pricing structure?"
        },
        {
            "id": "conv_003",
            "handoffScore": 30,
            "sentiment": "positive",
            "objectionCount": 0,
            "conversationLength": 3,
            "lastMessage": "Great! How do I get started?"
        }
    ]

    for i, conv in enumerate(test_conversations, 1):
        print(f"\n{'='*60}")
        print(f"TEST CASE {i}: {conv['id']}")
        print(f"{'='*60}")

        print(f"\nConversation State:")
        print(f"  - Handoff Score: {conv['handoffScore']}")
        print(f"  - Sentiment: {conv['sentiment']}")
        print(f"  - Objection Count: {conv['objectionCount']}")
        print(f"  - Conversation Length: {conv['conversationLength']} messages")
        print(f"  - Last Message: \"{conv['lastMessage']}\"")

        # Execute the circuit
        result = runtime.execute(
            "ConversationHandoffCircuit",
            "execute",
            {"conversation": conv}
        )

        print(f"\nExecution Logs:")
        for log in result["logs"]:
            print(f"  → {log}")

        print(f"\nGovernor Limits:")
        gov = result["governor_usage"]
        print(f"  - CPU Time: {gov['cpu_time_ms']}ms / 30,000ms")
        print(f"  - API Calls: {gov['api_calls']} / 50")

    print(f"\n{'='*60}")
    print("DEMO COMPLETE")
    print("="*60)

    print("\n📊 KEY TAKEAWAYS:")
    print("  1. Real-time sentiment analysis via ML")
    print("  2. DMN rules determine handoff urgency")
    print("  3. Automatic routing to human agents when needed")
    print("  4. LLM continues conversation when AI is appropriate")


if __name__ == "__main__":
    demo_conversation_handoff()
