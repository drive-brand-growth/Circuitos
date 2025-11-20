# Deploy MetroFlex Agent Updates

Safely deploy updates to the MetroFlex AI agent stack.

## Pre-Deployment Checklist:
- [ ] All tests pass locally
- [ ] Knowledge base JSON files are validated
- [ ] Environment variables are set (.env file)
- [ ] Docker Compose config is up to date
- [ ] Database migrations completed (if any)

## Deployment Steps:

### 1. Build New Container
```bash
docker compose build metroflex-ai
```

### 2. Test Container Locally
```bash
# Start in detached mode
docker compose up -d metroflex-ai

# Watch logs for errors
docker compose logs -f metroflex-ai

# Test health endpoint
curl http://localhost:5001/health | jq
```

### 3. Verify Agent Status
```bash
curl http://localhost:5001/api/agents/status | jq
```

Expected agents:
- licensing (available: true)
- gym_member (available: true)
- events (available: true)
- workflow_generator (available: true)
- conversation_manager (available: true)
- **adaptive_rag** (available: true, endpoints: 4)

### 4. Run Integration Tests
```bash
# Test licensing agent
.cursor/commands/metroflex/test-licensing-agent.md

# Test gym member agent
curl -X POST http://localhost:5001/api/gym/chat \
  -d '{"query": "What are membership options?"}' | jq

# Test RAG endpoint
curl -X POST http://localhost:5001/api/rag/query \
  -d '{"query": "2026 event schedule"}' | jq
```

### 5. Monitor Performance (First 15 Minutes)
```bash
# Watch container stats
docker stats metroflex-ai-agent

# Monitor error logs
docker compose logs -f metroflex-ai | grep ERROR

# Check Prometheus metrics
curl http://localhost:9090/api/v1/query?query=up{job="metroflex-ai"}
```

### 6. Rollback Plan (If Issues Detected)
```bash
# Stop current container
docker compose stop metroflex-ai

# Rollback to previous image
docker compose up -d metroflex-ai --scale metroflex-ai=0
docker compose up -d metroflex-ai

# Verify rollback
curl http://localhost:5001/health
```

## Post-Deployment:
1. Update Grafana dashboards if metrics changed
2. Notify team in Slack: "#metroflex-deployments"
3. Monitor GHL webhook success rate for 24 hours
4. Review logs for any new error patterns

## Production Deployment (Railway):
```bash
# Push to Railway
git push railway main

# Monitor deployment
railway logs --tail

# Verify production health
curl https://metroflex-ai.railway.app/health
```
