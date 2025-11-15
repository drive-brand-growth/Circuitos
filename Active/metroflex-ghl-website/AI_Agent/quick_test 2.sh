#!/bin/bash

# Quick Test Script for MetroFlex Enhanced AI Agent
# Tests the agent with sample queries via curl

echo "🧪 Testing MetroFlex Enhanced AI Agent"
echo "=========================================="
echo ""

BASE_URL="http://localhost:5000"

# Test 1: Health Check
echo "Test 1: Health Check"
echo "---------------------"
curl -s "$BASE_URL/health" | python3 -m json.tool
echo ""
echo ""

# Test 2: Intent Classification Test
echo "Test 2: Intent Classification"
echo "------------------------------"
echo "Query: 'When is the next event?'"
curl -s -X POST "$BASE_URL/webhook/test-intent" \
  -H "Content-Type: application/json" \
  -d '{"query": "When is the next event?"}' | python3 -m json.tool
echo ""
echo ""

# Test 3: Date Query (datetime intent)
echo "Test 3: Chat - Date Query"
echo "--------------------------"
curl -s -X POST "$BASE_URL/webhook/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test_user",
    "message": "When is the Ronnie Coleman Classic?"
  }' | python3 -m json.tool
echo ""
echo ""

# Test 4: Sponsor Query (HIGH INTENT - should trigger lead capture)
echo "Test 4: Chat - Sponsor Query (HIGH INTENT)"
echo "--------------------------------------------"
curl -s -X POST "$BASE_URL/webhook/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test_sponsor",
    "message": "How much does sponsorship cost?"
  }' | python3 -m json.tool
echo ""
echo ""

# Test 5: Vendor Query (spray tan)
echo "Test 5: Chat - Vendor Query"
echo "----------------------------"
curl -s -X POST "$BASE_URL/webhook/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test_competitor",
    "message": "Where can I get spray tanned?"
  }' | python3 -m json.tool
echo ""
echo ""

echo "=========================================="
echo "✅ All tests complete!"
echo ""
echo "💡 What to look for:"
echo "  - health endpoint returns 'healthy' status"
echo "  - intent classification detects correct categories"
echo "  - date queries return event dates quickly"
echo "  - sponsor queries have 'high_intent_detected': true"
echo "  - vendor queries mention ProTan USA"
echo ""
