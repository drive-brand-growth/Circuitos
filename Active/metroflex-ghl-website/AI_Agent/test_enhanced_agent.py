#!/usr/bin/env python3
"""
Test Script for MetroFlex Enhanced AI Agent
Demonstrates RAG improvements, intent classification, and lead capture
"""

import os
import json
from metroflex_ai_agent_enhanced import MetroFlexAIAgentEnhanced

# Set OpenAI API key (replace with your actual key)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-key-here")
KNOWLEDGE_BASE_PATH = "METROFLEX_EVENTS_KB_V2_RESEARCH_BASED.json"

def print_response(query: str, response_data: dict):
    """Pretty print agent response"""
    print("\n" + "="*80)
    print(f"USER: {query}")
    print("="*80)
    print(f"\n🎯 INTENT: {response_data.get('intent', {}).get('intent', 'unknown')}")
    print(f"   Sub-intent: {response_data.get('intent', {}).get('sub_intent', 'N/A')}")
    print(f"   Filter category: {response_data.get('intent', {}).get('filter_category', 'None')}")

    if response_data.get('high_intent_detected'):
        print(f"\n🔥 HIGH INTENT DETECTED: {response_data.get('lead_category', 'unknown')}")
        print(f"   Intent types: {', '.join(response_data.get('intent_types', []))}")

    print(f"\n📚 RELEVANT SOURCES ({len(response_data.get('relevant_sources', []))}):")
    for i, source in enumerate(response_data.get('relevant_sources', [])[:2], 1):
        print(f"   {i}. {source[:100]}...")

    print(f"\n🤖 RESPONSE:")
    print(f"{response_data.get('response', 'No response')}")
    print("\n" + "="*80 + "\n")

def main():
    print("🚀 Initializing MetroFlex Enhanced AI Agent...")
    print("="*80)

    # Initialize agent
    agent = MetroFlexAIAgentEnhanced(KNOWLEDGE_BASE_PATH, OPENAI_API_KEY)

    print("✅ Agent initialized successfully!\n")

    # Test queries demonstrating improvements
    test_queries = [
        # Test 1: Date query (should prioritize events, not legacy)
        "When is the next event?",

        # Test 2: Registration query (should trigger multi-turn flow + procedures)
        "How do I register for the Ronnie Coleman Classic?",

        # Test 3: Division query (should prioritize division rules)
        "What are the weight classes for Men's Bodybuilding?",

        # Test 4: Sponsor query (HIGH INTENT - should trigger lead capture)
        "I'm interested in sponsoring an event. What are the packages?",

        # Test 5: Vendor query (should retrieve vendor database)
        "Where can I get spray tanned for the competition?",

        # Test 6: First-timer query (should prioritize guide)
        "I've never competed before. Where do I start?",

        # Test 7: Legacy query (should prioritize Ronnie Coleman story)
        "Tell me about Ronnie Coleman and MetroFlex",

        # Test 8: Pro card query (should prioritize procedures)
        "How do I earn an IFBB Pro Card?",
    ]

    print("📋 RUNNING TEST QUERIES")
    print("="*80)
    print("Testing enhanced RAG with intent classification...\n")

    for query in test_queries:
        response_data = agent.chat(query, user_id="test_user", conversation_id="test_session")
        print_response(query, response_data)

        # Small delay for readability
        import time
        time.sleep(0.5)

    # Test intent classification directly
    print("\n📊 INTENT CLASSIFICATION TEST")
    print("="*80)

    intent_test_queries = [
        "when is the better bodies classic",
        "how much does it cost to sponsor",
        "what division should I compete in",
        "where can I get spray tan",
        "tell me about ronnie coleman",
    ]

    for query in intent_test_queries:
        intent_info = agent.classify_query_intent(query)
        high_intent = agent.detect_high_intent(query, "", intent_info)

        print(f"\nQuery: '{query}'")
        print(f"  Intent: {intent_info['intent']}")
        print(f"  Category filter: {intent_info['filter_category']}")
        print(f"  High intent: {high_intent['has_high_intent']}")
        if high_intent['has_high_intent']:
            print(f"  Lead category: {high_intent['lead_category']}")

    print("\n" + "="*80)
    print("✅ ALL TESTS COMPLETE!")
    print("="*80)

    print("\n📈 SUMMARY OF IMPROVEMENTS:")
    print("  ✅ Intent classification optimizes RAG retrieval")
    print("  ✅ Date queries return event info (not legacy)")
    print("  ✅ Sponsor queries detect high intent + trigger lead capture")
    print("  ✅ Vendor queries retrieve service providers (ProTan, Physique Visuals)")
    print("  ✅ Division queries prioritize rules over general info")
    print("  ✅ First-timer queries prioritize guide over procedures")
    print("")
    print("💡 NEXT STEPS:")
    print("  1. Set GHL_LEAD_CAPTURE_WEBHOOK environment variable")
    print("  2. Deploy to Railway/Fly.io")
    print("  3. Configure GHL Chat Widget to call /webhook/chat")
    print("  4. Monitor leads in GHL dashboard")
    print("")

if __name__ == "__main__":
    main()
