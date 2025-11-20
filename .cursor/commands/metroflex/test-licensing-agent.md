# Test MetroFlex Licensing Agent

Validate the licensing qualification agent with sample leads.

## Purpose:
Ensure the licensing agent correctly:
1. Qualifies leads based on capital, experience, and passion
2. Recommends appropriate packages (New Build $60k vs Rebrand $40k)
3. Sends qualified leads to GHL webhook
4. Calculates ROI and next steps

## Test Cases:

### High-Quality Lead (Should Score 85+)
```bash
curl -X POST http://localhost:5001/api/licensing/chat \
  -H "Content-Type: application/json" \
  -d '{
    "query": "I want to open a MetroFlex gym in Austin, Texas",
    "lead_data": {
      "name": "John Smith",
      "email": "john@example.com",
      "phone": "555-1234",
      "liquid_capital": 180000,
      "industry_experience_years": 5,
      "existing_gym": false,
      "existing_gym_sqft": 0,
      "location": "Austin, TX",
      "passion_score": 9
    }
  }' | jq
```

**Expected Output:**
- qualification_score.total_score: 85-100
- qualification_score.qualification_level: "FAST_TRACK"
- recommendation: "New Build License ($60,000)"
- ghl_sent: true

### Medium-Quality Lead (Should Score 70-84)
```bash
curl -X POST http://localhost:5001/api/licensing/chat \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are the licensing requirements?",
    "lead_data": {
      "name": "Sarah Johnson",
      "email": "sarah@example.com",
      "phone": "555-5678",
      "liquid_capital": 120000,
      "industry_experience_years": 2,
      "existing_gym": true,
      "existing_gym_sqft": 3500,
      "location": "Miami, FL",
      "passion_score": 7
    }
  }' | jq
```

**Expected Output:**
- qualification_score.total_score: 70-84
- qualification_score.qualification_level: "QUALIFIED"
- recommendation: "Rebrand License ($40,000)"
- ghl_sent: true

### Low-Quality Lead (Should Score <50)
```bash
curl -X POST http://localhost:5001/api/licensing/chat \
  -H "Content-Type: application/json" \
  -d '{
    "query": "How much does it cost?",
    "lead_data": {
      "name": "Mike Wilson",
      "email": "mike@example.com",
      "phone": "555-9999",
      "liquid_capital": 50000,
      "industry_experience_years": 0,
      "existing_gym": false,
      "existing_gym_sqft": 0,
      "location": "Dallas, TX",
      "passion_score": 5
    }
  }' | jq
```

**Expected Output:**
- qualification_score.total_score: <50
- qualification_score.qualification_level: "NOT_QUALIFIED"
- ghl_sent: false (don't waste sales team time)

## Validation Checklist:
- [ ] Capital scoring: $150k+ = 40 points, $100k-150k = 30 points
- [ ] Experience scoring: 5+ years = 25 points, 3-5 years = 20 points
- [ ] Existing gym bonus: 3000+ sqft = 15 points
- [ ] GHL webhook only fires for scores >=70
- [ ] Response includes MetroFlex legacy messaging
- [ ] ROI calculation shows breakeven timeline

## Troubleshooting:
If agent fails to initialize:
1. Check OPENAI_API_KEY is set in environment
2. Verify knowledge base file exists: `METROFLEX_EVENTS_KB_V3_EVENTS_ONLY.json`
3. Check Docker logs: `docker compose logs metroflex-ai`
