# Analyze GHL Conversion Rates

Review MetroFlex agent performance and GHL webhook success rates.

## Purpose:
Track the AI agent's impact on lead conversion and revenue pipeline.

## Key Metrics to Monitor:

### 1. Agent Query Volume
```sql
-- Query logs from application database
SELECT
  DATE(timestamp) as date,
  COUNT(*) as total_queries,
  COUNT(CASE WHEN high_intent_detected = true THEN 1 END) as high_intent_queries,
  COUNT(CASE WHEN ghl_sent = true THEN 1 END) as leads_sent_to_ghl
FROM agent_logs
WHERE timestamp > NOW() - INTERVAL '30 days'
GROUP BY DATE(timestamp)
ORDER BY date DESC;
```

### 2. Conversion Funnel
```
Total Queries → High Intent Detection → GHL Webhook → Qualified Lead → Closed Deal

Example:
1000 queries
↓ 15% high-intent detection
150 high-intent queries
↓ 90% GHL webhook success
135 leads in GHL
↓ 12% qualification rate
16 qualified leads
↓ 25% close rate
4 closed deals

Revenue Impact: 4 deals × $50k avg = $200k
```

### 3. Agent Performance by Type
```bash
curl http://localhost:5001/api/agents/status | jq '.agents | to_entries | map({
  agent: .key,
  available: .value.available,
  revenue_potential: .value.revenue_potential
})'
```

### 4. GHL Webhook Success Rate
```bash
# Check Docker logs for webhook failures
docker compose logs metroflex-ai | grep "GHL webhook" | grep -c "✅"
docker compose logs metroflex-ai | grep "GHL webhook" | grep -c "❌"

# Calculate success rate
SUCCESS=$(docker compose logs metroflex-ai | grep "GHL webhook" | grep -c "✅")
FAILED=$(docker compose logs metroflex-ai | grep "GHL webhook" | grep -c "❌")
TOTAL=$((SUCCESS + FAILED))
echo "GHL Webhook Success Rate: $(echo "scale=2; $SUCCESS / $TOTAL * 100" | bc)%"
```

## Performance Benchmarks:

| Metric | Target | Current | Status |
|--------|--------|---------|--------|
| High-Intent Detection Rate | 15-20% | Check logs | 🟡 |
| GHL Webhook Success | >95% | Check logs | 🟡 |
| Licensing Qualification | >70 score | Check DB | 🟡 |
| Gym Member Conversion | 12-18% | Check GHL | 🟡 |

## Grafana Dashboards:
1. **Agent Performance**: http://localhost:3002/d/metroflex-agents
2. **GHL Integration**: http://localhost:3002/d/ghl-webhooks
3. **Revenue Pipeline**: http://localhost:3002/d/revenue-funnel

## Optimization Actions:

If high-intent detection is low (<10%):
- Review intent classification keywords in `metroflex_ai_agent_enhanced.py:99-194`
- Adjust sensitivity thresholds
- Add more high-intent signals

If GHL webhook success rate is low (<90%):
- Check `GHL_LEAD_CAPTURE_WEBHOOK` environment variable
- Verify webhook URL is active (test in GHL dashboard)
- Review payload format matches GHL expectations

If qualification scores are too low:
- Adjust scoring weights in `licensing_agent.py:67-152`
- Lower capital requirement threshold (currently $150k)
- Review passion score impact (currently 20% weight)

## Monthly Reporting Template:
```markdown
## MetroFlex AI Agent Performance - [Month]

### Overview
- Total Queries: X
- High-Intent Queries: X (X%)
- Leads Sent to GHL: X (X% success)
- Qualified Leads: X
- Revenue Pipeline: $X

### Agent Breakdown
- Licensing: X queries, X leads, $X pipeline
- Gym Member: X queries, X leads, $X pipeline
- Events: X queries, X leads

### Key Wins
- [Notable conversion story]
- [Performance improvement]

### Action Items
- [Optimization needed]
- [Follow-up required]
```
