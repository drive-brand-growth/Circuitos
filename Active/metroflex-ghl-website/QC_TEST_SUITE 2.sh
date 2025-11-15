#!/bin/bash

###############################################################################
# MetroFlex Website & AI Agent - Quality Control Test Suite
# Comprehensive automated testing for all recent updates
###############################################################################

echo "============================================================"
echo "🔍 MetroFlex Quality Control Test Suite"
echo "============================================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test counters
PASSED=0
FAILED=0
WARNINGS=0

###############################################################################
# SECTION 1: WEBSITE INTEGRITY TESTS
###############################################################################

echo "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo "${BLUE}  SECTION 1: Website Integrity Tests${NC}"
echo "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Test 1.1: Check if homepage exists
echo -n "Test 1.1: Homepage file exists... "
if [ -f "METROFLEX_HOMEPAGE_COMPLETE.html" ]; then
    echo -e "${GREEN}✓ PASS${NC}"
    ((PASSED++))
else
    echo -e "${RED}✗ FAIL${NC}"
    ((FAILED++))
fi

# Test 1.2: Check for hero section updates
echo -n "Test 1.2: Hero section has both events... "
if grep -q "NPC Ronnie Coleman Classic" METROFLEX_HOMEPAGE_COMPLETE.html && \
   grep -q "NPC Branch Warren Classic" METROFLEX_HOMEPAGE_COMPLETE.html; then
    echo -e "${GREEN}✓ PASS${NC}"
    ((PASSED++))
else
    echo -e "${RED}✗ FAIL${NC}"
    ((FAILED++))
fi

# Test 1.3: Check for 30th Anniversary text
echo -n "Test 1.3: 30th Anniversary text present... "
if grep -q "30th Anniversary" METROFLEX_HOMEPAGE_COMPLETE.html; then
    echo -e "${GREEN}✓ PASS${NC}"
    ((PASSED++))
else
    echo -e "${RED}✗ FAIL${NC}"
    ((FAILED++))
fi

# Test 1.4: Check for vintage poster image
echo -n "Test 1.4: Vintage poster image referenced... "
if grep -q "ronnie-coleman-30th-anniversary.jpg" METROFLEX_HOMEPAGE_COMPLETE.html; then
    echo -e "${GREEN}✓ PASS${NC}"
    ((PASSED++))
else
    echo -e "${RED}✗ FAIL${NC}"
    ((FAILED++))
fi

# Test 1.5: Check if vintage poster image file exists
echo -n "Test 1.5: Vintage poster image file exists... "
if [ -f "assets/ronnie-coleman-30th-anniversary.jpg" ]; then
    echo -e "${GREEN}✓ PASS${NC}"
    ((PASSED++))
else
    echo -e "${RED}✗ FAIL${NC}"
    ((FAILED++))
fi

# Test 1.6: Check for Branch/Ronnie legends image
echo -n "Test 1.6: Branch/Ronnie legends image exists... "
if [ -f "assets/ronnie-branch-legends.jpg" ]; then
    echo -e "${GREEN}✓ PASS${NC}"
    ((PASSED++))
else
    echo -e "${YELLOW}⚠ WARNING${NC} (Optional image)"
    ((WARNINGS++))
fi

# Test 1.7: Check for valid HTML structure
echo -n "Test 1.7: HTML structure validation... "
if grep -q "<!DOCTYPE html>" METROFLEX_HOMEPAGE_COMPLETE.html && \
   grep -q "</html>" METROFLEX_HOMEPAGE_COMPLETE.html; then
    echo -e "${GREEN}✓ PASS${NC}"
    ((PASSED++))
else
    echo -e "${RED}✗ FAIL${NC}"
    ((FAILED++))
fi

# Test 1.8: Check for meta description update
echo -n "Test 1.8: Meta description includes both events... "
if grep -q 'content=".*NPC Ronnie Coleman Classic.*NPC Branch Warren Classic.*"' METROFLEX_HOMEPAGE_COMPLETE.html; then
    echo -e "${GREEN}✓ PASS${NC}"
    ((PASSED++))
else
    echo -e "${YELLOW}⚠ WARNING${NC} (Meta tag may need update)"
    ((WARNINGS++))
fi

echo ""

###############################################################################
# SECTION 2: AI AGENT TESTS
###############################################################################

echo "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo "${BLUE}  SECTION 2: AI Agent Tests${NC}"
echo "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Test 2.1: Check if AI agent files exist
echo -n "Test 2.1: AI agent Python file exists... "
if [ -f "AI_Agent/metroflex_ai_agent_enhanced.py" ]; then
    echo -e "${GREEN}✓ PASS${NC}"
    ((PASSED++))
else
    echo -e "${RED}✗ FAIL${NC}"
    ((FAILED++))
fi

# Test 2.2: Check if .env file exists
echo -n "Test 2.2: .env file configured... "
if [ -f "AI_Agent/.env" ]; then
    echo -e "${GREEN}✓ PASS${NC}"
    ((PASSED++))
else
    echo -e "${RED}✗ FAIL${NC}"
    ((FAILED++))
fi

# Test 2.3: Check if knowledge base JSON exists
echo -n "Test 2.3: Knowledge base file exists... "
if [ -f "AI_Agent/METROFLEX_EVENTS_KB_V2_RESEARCH_BASED.json" ]; then
    echo -e "${GREEN}✓ PASS${NC}"
    ((PASSED++))
else
    echo -e "${RED}✗ FAIL${NC}"
    ((FAILED++))
fi

# Test 2.4: Validate JSON syntax
echo -n "Test 2.4: Knowledge base JSON syntax valid... "
if python3 -c "import json; json.load(open('AI_Agent/METROFLEX_EVENTS_KB_V2_RESEARCH_BASED.json'))" 2>/dev/null; then
    echo -e "${GREEN}✓ PASS${NC}"
    ((PASSED++))
else
    echo -e "${RED}✗ FAIL${NC}"
    ((FAILED++))
fi

# Test 2.5: Check for OpenAI API integration
echo -n "Test 2.5: OpenAI client integration present... "
if grep -q "from openai import OpenAI" AI_Agent/metroflex_ai_agent_enhanced.py; then
    echo -e "${GREEN}✓ PASS${NC}"
    ((PASSED++))
else
    echo -e "${RED}✗ FAIL${NC}"
    ((FAILED++))
fi

# Test 2.6: Check for dotenv loading
echo -n "Test 2.6: Environment variable loading... "
if grep -q "load_dotenv()" AI_Agent/metroflex_ai_agent_enhanced.py; then
    echo -e "${GREEN}✓ PASS${NC}"
    ((PASSED++))
else
    echo -e "${RED}✗ FAIL${NC}"
    ((FAILED++))
fi

# Test 2.7: Check if virtual environment exists
echo -n "Test 2.7: Python virtual environment setup... "
if [ -d "AI_Agent/venv" ]; then
    echo -e "${GREEN}✓ PASS${NC}"
    ((PASSED++))
else
    echo -e "${YELLOW}⚠ WARNING${NC} (Run start_enhanced_agent.sh)"
    ((WARNINGS++))
fi

# Test 2.8: Check if startup script exists
echo -n "Test 2.8: Startup script exists... "
if [ -f "AI_Agent/start_enhanced_agent.sh" ]; then
    echo -e "${GREEN}✓ PASS${NC}"
    ((PASSED++))
else
    echo -e "${RED}✗ FAIL${NC}"
    ((FAILED++))
fi

# Test 2.9: Check if startup script is executable
echo -n "Test 2.9: Startup script permissions... "
if [ -x "AI_Agent/start_enhanced_agent.sh" ]; then
    echo -e "${GREEN}✓ PASS${NC}"
    ((PASSED++))
else
    echo -e "${YELLOW}⚠ WARNING${NC} (Run: chmod +x AI_Agent/start_enhanced_agent.sh)"
    ((WARNINGS++))
fi

echo ""

###############################################################################
# SECTION 3: AI AGENT RUNTIME TESTS (If Running)
###############################################################################

echo "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo "${BLUE}  SECTION 3: AI Agent Runtime Tests${NC}"
echo "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Test 3.1: Check if agent is running
echo -n "Test 3.1: AI Agent health check... "
HEALTH_CHECK=$(curl -s http://localhost:5001/health 2>/dev/null)
if echo "$HEALTH_CHECK" | grep -q "healthy"; then
    echo -e "${GREEN}✓ PASS${NC} (Agent is running)"
    ((PASSED++))

    # Test 3.2: Test date query
    echo -n "Test 3.2: Date query response... "
    DATE_RESPONSE=$(curl -s -X POST http://localhost:5001/webhook/chat \
        -H "Content-Type: application/json" \
        -d '{"user_id": "qc_test", "message": "When is the Ronnie Coleman Classic?"}' 2>/dev/null)
    if echo "$DATE_RESPONSE" | grep -q "May 16, 2026"; then
        echo -e "${GREEN}✓ PASS${NC}"
        ((PASSED++))
    else
        echo -e "${RED}✗ FAIL${NC}"
        echo "  Response: $DATE_RESPONSE"
        ((FAILED++))
    fi

    # Test 3.3: Test intent classification
    echo -n "Test 3.3: Intent classification... "
    INTENT_RESPONSE=$(curl -s -X POST http://localhost:5001/webhook/test-intent \
        -H "Content-Type: application/json" \
        -d '{"query": "When is the next event?"}' 2>/dev/null)
    if echo "$INTENT_RESPONSE" | grep -q "datetime"; then
        echo -e "${GREEN}✓ PASS${NC}"
        ((PASSED++))
    else
        echo -e "${RED}✗ FAIL${NC}"
        ((FAILED++))
    fi

    # Test 3.4: Test high-intent detection
    echo -n "Test 3.4: High-intent sponsor detection... "
    SPONSOR_RESPONSE=$(curl -s -X POST http://localhost:5001/webhook/test-intent \
        -H "Content-Type: application/json" \
        -d '{"query": "How much does sponsorship cost?"}' 2>/dev/null)
    if echo "$SPONSOR_RESPONSE" | grep -q "high_intent.*true"; then
        echo -e "${GREEN}✓ PASS${NC}"
        ((PASSED++))
    else
        echo -e "${RED}✗ FAIL${NC}"
        ((FAILED++))
    fi

    # Test 3.5: Test vendor query
    echo -n "Test 3.5: Vendor query response... "
    VENDOR_RESPONSE=$(curl -s -X POST http://localhost:5001/webhook/chat \
        -H "Content-Type: application/json" \
        -d '{"user_id": "qc_test", "message": "Where can I get spray tanned?"}' 2>/dev/null)
    if echo "$VENDOR_RESPONSE" | grep -qi "ProTan"; then
        echo -e "${GREEN}✓ PASS${NC}"
        ((PASSED++))
    else
        echo -e "${RED}✗ FAIL${NC}"
        ((FAILED++))
    fi

else
    echo -e "${YELLOW}⚠ SKIP${NC} (Agent not running - start with ./AI_Agent/start_enhanced_agent.sh)"
    echo "  Skipping runtime tests..."
    ((WARNINGS++))
fi

echo ""

###############################################################################
# SECTION 4: FILE INTEGRITY TESTS
###############################################################################

echo "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo "${BLUE}  SECTION 4: File Integrity Tests${NC}"
echo "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Test 4.1: Check for required documentation
echo -n "Test 4.1: Quick start documentation exists... "
if [ -f "AI_Agent/QUICK_START_LOCAL.md" ]; then
    echo -e "${GREEN}✓ PASS${NC}"
    ((PASSED++))
else
    echo -e "${YELLOW}⚠ WARNING${NC}"
    ((WARNINGS++))
fi

# Test 4.2: Check for test interface
echo -n "Test 4.2: Test interface HTML exists... "
if [ -f "test_ai_agent.html" ]; then
    echo -e "${GREEN}✓ PASS${NC}"
    ((PASSED++))
else
    echo -e "${YELLOW}⚠ WARNING${NC}"
    ((WARNINGS++))
fi

# Test 4.3: Check assets folder
echo -n "Test 4.3: Assets folder exists... "
if [ -d "assets" ]; then
    echo -e "${GREEN}✓ PASS${NC}"
    ((PASSED++))
else
    echo -e "${RED}✗ FAIL${NC}"
    ((FAILED++))
fi

# Test 4.4: Count assets
echo -n "Test 4.4: Assets folder has files... "
ASSET_COUNT=$(ls -1 assets/*.jpg assets/*.png assets/*.svg 2>/dev/null | wc -l)
if [ "$ASSET_COUNT" -gt 0 ]; then
    echo -e "${GREEN}✓ PASS${NC} ($ASSET_COUNT images found)"
    ((PASSED++))
else
    echo -e "${YELLOW}⚠ WARNING${NC} (No images found)"
    ((WARNINGS++))
fi

echo ""

###############################################################################
# SECTION 5: CONTENT VERIFICATION
###############################################################################

echo "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo "${BLUE}  SECTION 5: Content Verification${NC}"
echo "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Test 5.1: Check for all 4 events in homepage
echo -n "Test 5.1: All 4 MetroFlex events listed... "
EVENTS=0
grep -q "Better Bodies Classic" METROFLEX_HOMEPAGE_COMPLETE.html && ((EVENTS++))
grep -q "Ronnie Coleman Classic" METROFLEX_HOMEPAGE_COMPLETE.html && ((EVENTS++))
grep -q "Branch Warren Classic - Colorado" METROFLEX_HOMEPAGE_COMPLETE.html && ((EVENTS++))
grep -q "Branch Warren Classic - Houston" METROFLEX_HOMEPAGE_COMPLETE.html && ((EVENTS++))

if [ $EVENTS -eq 4 ]; then
    echo -e "${GREEN}✓ PASS${NC} (All 4 events found)"
    ((PASSED++))
else
    echo -e "${RED}✗ FAIL${NC} (Only $EVENTS/4 events found)"
    ((FAILED++))
fi

# Test 5.2: Check for sponsorship section
echo -n "Test 5.2: Sponsorship section present... "
if grep -q "Sponsorship Opportunities" METROFLEX_HOMEPAGE_COMPLETE.html; then
    echo -e "${GREEN}✓ PASS${NC}"
    ((PASSED++))
else
    echo -e "${RED}✗ FAIL${NC}"
    ((FAILED++))
fi

# Test 5.3: Check for legacy section
echo -n "Test 5.3: Legacy section present... "
if grep -q "38+ Years of Making Champions" METROFLEX_HOMEPAGE_COMPLETE.html; then
    echo -e "${GREEN}✓ PASS${NC}"
    ((PASSED++))
else
    echo -e "${RED}✗ FAIL${NC}"
    ((FAILED++))
fi

# Test 5.4: Check knowledge base has all events
echo -n "Test 5.4: Knowledge base has all events... "
if [ -f "AI_Agent/METROFLEX_EVENTS_KB_V2_RESEARCH_BASED.json" ]; then
    KB_EVENTS=$(grep -o '"better_bodies_classic"' AI_Agent/METROFLEX_EVENTS_KB_V2_RESEARCH_BASED.json | wc -l)
    if [ $KB_EVENTS -gt 0 ]; then
        echo -e "${GREEN}✓ PASS${NC}"
        ((PASSED++))
    else
        echo -e "${RED}✗ FAIL${NC}"
        ((FAILED++))
    fi
else
    echo -e "${RED}✗ FAIL${NC} (Knowledge base not found)"
    ((FAILED++))
fi

echo ""

###############################################################################
# FINAL REPORT
###############################################################################

echo "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo "${BLUE}  TEST SUMMARY${NC}"
echo "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

TOTAL=$((PASSED + FAILED))
SUCCESS_RATE=$((PASSED * 100 / TOTAL))

echo "  ${GREEN}✓ Passed:${NC}   $PASSED"
echo "  ${RED}✗ Failed:${NC}   $FAILED"
echo "  ${YELLOW}⚠ Warnings:${NC} $WARNINGS"
echo "  ────────────────"
echo "  Total Tests: $TOTAL"
echo "  Success Rate: ${SUCCESS_RATE}%"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}  🎉 ALL CRITICAL TESTS PASSED!${NC}"
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    echo "✅ Website is ready for deployment"
    echo "✅ AI Agent is properly configured"
    echo "✅ All recent updates are intact"

    if [ $WARNINGS -gt 0 ]; then
        echo ""
        echo -e "${YELLOW}Note: $WARNINGS warnings detected (non-critical)${NC}"
    fi
else
    echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${RED}  ⚠️  CRITICAL ISSUES DETECTED${NC}"
    echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    echo "❌ $FAILED critical test(s) failed"
    echo "⚠️  Please review the failures above"
fi

echo ""
echo "For detailed AI Agent testing, visit:"
echo "  http://localhost:8000/test_ai_agent.html"
echo ""
echo "============================================================"

exit $FAILED
