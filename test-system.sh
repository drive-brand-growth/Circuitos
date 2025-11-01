#!/bin/bash

# System Validation Script
# Tests all API endpoints and verifies dual-path lead system

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default to localhost
BASE_URL="${1:-http://localhost:3000}"

echo -e "${BLUE}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║    Dual-Path Lead System - Validation Suite                   ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${YELLOW}Testing against: ${BASE_URL}${NC}"
echo ""

# Counter for passed/failed tests
PASSED=0
FAILED=0

# Test function
test_endpoint() {
    local test_name=$1
    local endpoint=$2
    local payload=$3
    local expected_key=$4

    echo -e "${YELLOW}Testing: ${test_name}${NC}"

    response=$(curl -s -X POST "${BASE_URL}${endpoint}" \
        -H "Content-Type: application/json" \
        -d "${payload}")

    # Check if response contains expected key
    if echo "$response" | grep -q "$expected_key"; then
        echo -e "${GREEN}✓ PASS${NC} - ${test_name}"
        ((PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC} - ${test_name}"
        echo "Response: $response"
        ((FAILED++))
        return 1
    fi
}

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Test 1: Virtual LPR - High Intent GMB Lead"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

test_endpoint \
    "Virtual LPR - GMB View" \
    "/api/virtual-lpr" \
    '{
        "signal_type": "gmb_view",
        "signal_data": {
            "phone": "8175551234",
            "zip_code": "76102"
        },
        "business": {
            "name": "MetroFlex Gym",
            "lat": 32.7357,
            "lng": -97.1081,
            "city": "Fort Worth",
            "state": "TX"
        }
    }' \
    "vlpr_score"

echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Test 2: Lead Router - Cold Email Detection"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

test_endpoint \
    "Lead Router - Cold Email" \
    "/api/lead-router" \
    '{
        "contact": {
            "email": "test@example.com",
            "first_name": "Marcus",
            "tags": ["Instantly Campaign"],
            "custom_fields": {
                "instantly_campaign_id": "camp_123"
            }
        }
    }' \
    "cold_email"

echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Test 3: Lead Router - Website Traffic Detection"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

test_endpoint \
    "Lead Router - Website Traffic" \
    "/api/lead-router" \
    '{
        "contact": {
            "email": "sarah@example.com",
            "first_name": "Sarah",
            "custom_fields": {
                "vlpr_source": "website_visit"
            }
        }
    }' \
    "website_traffic"

echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Test 4: Master Copywriter - Cold Email Tone"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

test_endpoint \
    "Copywriter - Cold Email (Humble Tone)" \
    "/api/copywriter" \
    '{
        "contact": {
            "first_name": "Marcus",
            "email": "marcus@example.com"
        },
        "channel": "email",
        "awareness_level": "Problem Aware",
        "lead_source": "cold_email",
        "business": {
            "name": "MetroFlex Gym",
            "city": "Fort Worth",
            "state": "TX"
        }
    }' \
    "variants"

echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Test 5: Master Copywriter - Website Traffic Tone"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

test_endpoint \
    "Copywriter - Website Traffic (Confident Tone)" \
    "/api/copywriter" \
    '{
        "contact": {
            "first_name": "Sarah",
            "email": "sarah@example.com"
        },
        "channel": "email",
        "awareness_level": "Product Aware",
        "lead_source": "website_traffic",
        "business": {
            "name": "MetroFlex Gym",
            "city": "Fort Worth",
            "state": "TX"
        }
    }' \
    "variants"

echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Test 6: Instantly Webhook - Positive Reply"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

test_endpoint \
    "Instantly Webhook - Qualified Reply" \
    "/api/instantly-webhook" \
    '{
        "event_type": "reply",
        "campaign_id": "camp_test123",
        "campaign_name": "Gym Owners Test Campaign",
        "lead_email": "interested@example.com",
        "lead_first_name": "Jake",
        "reply_text": "Yes, I am interested! Tell me more about pricing."
    }' \
    "qualified"

echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Test 7: Instantly Webhook - Negative Reply"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

test_endpoint \
    "Instantly Webhook - Unqualified Reply" \
    "/api/instantly-webhook" \
    '{
        "event_type": "reply",
        "campaign_id": "camp_test123",
        "campaign_name": "Gym Owners Test Campaign",
        "lead_email": "notinterested@example.com",
        "lead_first_name": "Bob",
        "reply_text": "Not interested, please remove me."
    }' \
    "negative"

echo ""
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "                          RESULTS SUMMARY"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo -e "Total Tests: $((PASSED + FAILED))"
echo -e "${GREEN}Passed: ${PASSED}${NC}"
echo -e "${RED}Failed: ${FAILED}${NC}"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}╔════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║    ✓ ALL TESTS PASSED - System is working correctly! 🎉       ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo "Next steps:"
    echo "1. Deploy to Vercel: vercel --prod"
    echo "2. Run this script against production:"
    echo "   ./test-system.sh https://your-project.vercel.app"
    echo "3. Set up GHL workflows (see COMPLETE-SETUP-GUIDE-STEP-BY-STEP.md)"
    exit 0
else
    echo -e "${RED}╔════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${RED}║    ✗ SOME TESTS FAILED - Check errors above                   ║${NC}"
    echo -e "${RED}╚════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo "Common fixes:"
    echo "1. Check ANTHROPIC_API_KEY in .env file"
    echo "2. Run 'npm install' to install dependencies"
    echo "3. Make sure 'vercel dev' is running on port 3000"
    echo "4. See QUICK-REFERENCE-CARD.md for troubleshooting"
    exit 1
fi
