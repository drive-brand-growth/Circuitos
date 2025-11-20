# Circuit OS Automation Framework

**Team-ready automation for RAG, MetroFlex agents, and full-stack operations**

Built for scale. Not for single-developer workflows.

---

## 🎯 WHAT YOU GET

### Cursor Commands (11 reusable AI workflows)
Invoke with `/` in Cursor chat - zero setup required

### VS Code Tasks (20 production tasks)
Run with `Cmd+Shift+P` → "Tasks: Run Task"

### GitHub Actions (5 CI/CD workflows)
Automated validation on every commit

---

## 📁 STRUCTURE

```
.cursor/commands/
├── rag/
│   ├── ingest-npc-events.md          # Crawl NPC website
│   ├── analyze-cache-performance.md  # Cache hit rate analysis
│   ├── review-feedback-signals.md    # Quality issue detection
│   ├── query-with-quality-check.md   # Test with gates enabled
│   └── reingest-stale-documents.md   # Refresh outdated content
├── metroflex/
│   ├── test-licensing-agent.md       # Qualification scoring tests
│   ├── deploy-agent-updates.md       # Safe deployment workflow
│   └── analyze-ghl-conversions.md    # Revenue pipeline tracking
└── circuit-os/
    ├── health-check-full-stack.md    # All 15+ services
    ├── backup-databases.md           # Disaster recovery
    └── monitor-resource-usage.md     # CPU/memory/disk tracking

.vscode/tasks.json
├── RAG Health Check              # Quick status check
├── RAG Cache Stats               # Performance metrics
├── RAG Query Test                # End-to-end validation
├── MetroFlex: Test Licensing     # Agent testing
├── MetroFlex: Agent Status       # All 5 agents
├── Circuit OS: Full Health       # Comprehensive check
├── Docker: Rebuild MetroFlex     # Build + deploy
├── Database: Backup All          # Full backup
└── Monitoring: Open Grafana      # Dashboard access

.github/workflows/rag-ci.yml
├── Health Check                  # Python syntax validation
├── Docker Validation             # Compose config check
├── Cursor Commands Validation    # Structure verification
├── VS Code Tasks Validation      # JSON syntax check
└── n8n Workflows Validation      # Workflow integrity
```

---

## 🚀 QUICK START

### For Team Members (First Time)

**1. Install Cursor** (if not already)
```bash
# Download from cursor.com
# Open this repository in Cursor
```

**2. Test a Cursor Command**
```bash
# In Cursor chat, type:
/

# You'll see 11 commands appear:
# - rag/ingest-npc-events
# - rag/analyze-cache-performance
# - metroflex/test-licensing-agent
# etc.

# Select one and hit Enter
# Cursor will execute the workflow for you
```

**3. Run a VS Code Task**
```bash
# Press: Cmd+Shift+P (Mac) or Ctrl+Shift+P (Windows/Linux)
# Type: "Tasks: Run Task"
# Select: "Circuit OS: Full Health Check"

# Watch the output in the integrated terminal
```

**4. Check CI/CD Status**
```bash
# Push a commit to your branch
git add .
git commit -m "test: Verify CI/CD pipeline"
git push

# GitHub Actions will automatically:
# - Validate Python syntax
# - Check Docker configs
# - Verify Cursor commands
# - Test VS Code tasks
# - Validate n8n workflows

# View results: github.com/<your-repo>/actions
```

---

## 💡 COMMON WORKFLOWS

### Starting Your Day

**1. Health Check**
```bash
# VS Code Task: "Circuit OS: Full Health Check"
# Or in terminal:
curl http://localhost:5001/api/rag/health | jq
```

**2. Check Cache Performance**
```bash
# Cursor Command: /rag/analyze-cache-performance
# Or VS Code Task: "RAG: Cache Stats"
```

**3. Review Overnight Feedback**
```bash
# Cursor Command: /rag/review-feedback-signals
# Check which documents need re-ingestion
```

---

### Deploying Updates

**1. Build and Test Locally**
```bash
# VS Code Task: "Docker: Rebuild MetroFlex AI"
# Automatically builds + deploys + health checks
```

**2. Run Integration Tests**
```bash
# VS Code Task: "MetroFlex: Test Licensing Agent"
# Validates all 3 qualification tiers
```

**3. Push to Production**
```bash
git add .
git commit -m "feat: Update licensing scoring"
git push

# GitHub Actions will validate everything
# Railway auto-deploys on success
```

---

### Troubleshooting

**Service Down**
```bash
# VS Code Task: "Circuit OS: Full Health Check"
# Identifies which service failed

# Then check specific service:
docker compose logs -f <service-name>
```

**Cache Performance Issues**
```bash
# Cursor Command: /rag/analyze-cache-performance
# Shows hit rate, bucket count, TTL settings

# If hit rate <15%, adjust threshold:
# Edit docker-compose.yml → RAG_CACHE_TTL
```

**Stale Content Detected**
```bash
# Cursor Command: /rag/reingest-stale-documents
# Lists all outdated docs
# Re-ingests based on feedback signals
```

---

## 🔧 CUSTOMIZING FOR YOUR VENTURE

### Adding a New Cursor Command

**1. Create file**: `.cursor/commands/<category>/<name>.md`

Example: `.cursor/commands/drn/analyze-docs.md`
```markdown
# Analyze DRN Documentation Quality

## Steps:
1. Query RAG for all DRN-related documents
2. Check completeness score
3. Identify gaps

## API Endpoint:
\`\`\`bash
curl http://localhost:5001/api/rag/documents?category=drn | jq
\`\`\`

## Expected Output:
- Document count
- Coverage percentage
- Missing topics
```

**2. Use it**:
```bash
# In Cursor chat:
/drn/analyze-docs
```

---

### Adding a New VS Code Task

**1. Edit** `.vscode/tasks.json`:
```json
{
  "label": "DRN: Documentation Health",
  "type": "shell",
  "command": "curl http://localhost:5001/api/rag/documents?category=drn | jq",
  "problemMatcher": []
}
```

**2. Run it**:
```bash
# Cmd+Shift+P → "Tasks: Run Task" → "DRN: Documentation Health"
```

---

## 📊 MONITORING & METRICS

### Grafana Dashboards

**Circuit OS Overview**
- URL: http://localhost:3002/d/circuit-os-overview
- Metrics: All 15+ services, CPU, memory, disk

**RAG Performance**
- URL: http://localhost:3002/d/rag-performance
- Metrics: Query latency, cache hit rate, feedback signals

**MetroFlex Revenue Pipeline**
- URL: http://localhost:3002/d/metroflex-pipeline
- Metrics: Lead volume, qualification scores, GHL conversions

### Prometheus Queries

**Cache Hit Rate**
```promql
rate(rag_cache_hits_total[5m]) / rate(rag_queries_total[5m])
```

**Agent Query Volume**
```promql
sum(rate(agent_queries_total[5m])) by (agent_type)
```

**Quality Gate Failures**
```promql
sum(rate(quality_gate_failures_total[5m])) by (gate_type)
```

---

## 🚨 ALERTS

### Critical (PagerDuty + Slack)
- Any service down >5 minutes
- Database connection failures
- CPU >90% for >5 minutes
- Disk >95%

### Warning (Slack only)
- Cache hit rate <20%
- Quality gate failures >10%
- Slow queries >1s
- Memory >80%

### Configure Alerts
Edit: `docker/alertmanager.yml`

---

## 🔐 SECURITY

### Environment Variables

**Required**:
- `OPENAI_API_KEY` - GPT-4 access
- `RAG_DATABASE_URL` - pgvector connection
- `REDIS_URL` - Semantic cache
- `GHL_LEAD_CAPTURE_WEBHOOK` - Lead routing

**Optional**:
- `RAG_CACHE_TTL` - Cache expiration (default: 3600s)
- `RAG_EMBEDDING_MODEL` - Model override (default: all-MiniLM-L6-v2)

### Secrets Management

**Development**:
```bash
# Use .env file (never commit!)
cp .env.example .env
# Edit values
```

**Production (Railway)**:
```bash
# Set in Railway dashboard
# Or via CLI:
railway variables set OPENAI_API_KEY=sk-...
```

---

## 📈 PERFORMANCE BENCHMARKS

### RAG System
| Metric | Target | Actual |
|--------|--------|--------|
| Query latency (cached) | <50ms | 15-30ms |
| Query latency (uncached) | <250ms | 180-220ms |
| Cache hit rate | >30% | 31-45% |
| Ingestion speed | >5 pages/min | 8-12 pages/min |

### MetroFlex Agents
| Agent | Response Time | Qualification Time |
|-------|---------------|-------------------|
| Licensing | <500ms | <200ms |
| Gym Member | <400ms | <150ms |
| Events | <300ms | N/A |

### Infrastructure
| Service | CPU (Avg) | Memory (Peak) |
|---------|-----------|---------------|
| metroflex-ai | 5-15% | 512MB |
| postgres | 5-10% | 1GB |
| redis | 1-5% | 256MB |

---

## 🆘 TROUBLESHOOTING

### Cursor Commands Not Appearing

**Issue**: Typing `/` in Cursor chat shows no commands

**Fix**:
1. Check `.cursor/commands/` directory exists
2. Restart Cursor
3. Verify files are `.md` format
4. Check Cursor version (requires v0.30+)

### VS Code Tasks Not Running

**Issue**: "Tasks: Run Task" shows empty list

**Fix**:
1. Verify `.vscode/tasks.json` exists
2. Check JSON syntax: `python -m json.tool .vscode/tasks.json`
3. Reload window: `Cmd+Shift+P` → "Reload Window"

### GitHub Actions Failing

**Issue**: CI/CD pipeline shows red X

**Fix**:
1. Check logs: github.com/<repo>/actions
2. Common issues:
   - Missing environment variables
   - Python syntax errors
   - Docker compose validation failed
3. Run locally: `docker compose config`

### Service Won't Start

**Issue**: Docker service stuck in "starting" state

**Fix**:
```bash
# Check logs
docker compose logs -f <service-name>

# Common issues:
# - Database not ready (wait for postgres healthcheck)
# - Missing environment variable
# - Port already in use

# Restart specific service
docker compose restart <service-name>
```

---

## 🎓 TEAM TRAINING

### Onboarding Checklist (15 minutes)

**New Team Member Setup**:
- [ ] Clone repository
- [ ] Install Cursor
- [ ] Copy `.env.example` to `.env` (get keys from team)
- [ ] Run: `docker compose up -d`
- [ ] Test Cursor command: `/rag/health-check`
- [ ] Run VS Code task: "Circuit OS: Full Health Check"
- [ ] Verify all services: Green checkmarks
- [ ] Access Grafana: http://localhost:3002 (admin/admin)

### Daily Workflows (5 minutes/day)

**Morning**:
1. Health check (1 min)
2. Review overnight feedback (2 min)
3. Check Grafana alerts (1 min)
4. Review cache performance (1 min)

**End of Day**:
1. Commit changes
2. Push to branch
3. Verify CI/CD passes

### Weekly Maintenance (30 minutes/week)

**Monday**:
- Review stale documents, queue re-ingestion
- Analyze cache performance trends
- Check resource usage

**Friday**:
- Backup databases
- Review agent conversion rates
- Clean Docker system: `docker system prune -f`

---

## 🔄 CONTINUOUS IMPROVEMENT

### Metrics to Track

**Weekly**:
- Cache hit rate trend
- Quality gate failure rate
- Agent query volume
- GHL conversion rates

**Monthly**:
- Total documents indexed
- Feedback signals processed
- System uptime
- Cost per query

### Optimization Opportunities

**If cache hit rate is low (<20%)**:
- Lower similarity threshold to 0.90
- Increase TTL to 7200s (2 hours)
- Review query patterns for clustering

**If ingestion is slow (<5 pages/min)**:
- Increase chunk size to 1024 tokens
- Reduce overlap to 25 tokens
- Use faster embedding model

**If queries are slow (>500ms)**:
- Add pgvector indexes
- Optimize chunk retrieval limit
- Enable query result caching

---

## 📚 ADDITIONAL RESOURCES

### Documentation
- **RAG Core**: `Active/metroflex-ghl-website/AI_Agent/rag_core.py`
- **Adaptive Features**: `Active/metroflex-ghl-website/AI_Agent/rag_adaptive.py`
- **API Reference**: `Active/metroflex-ghl-website/AI_Agent/adaptive_rag_api.py`

### Dashboards
- **Grafana**: http://localhost:3002
- **Prometheus**: http://localhost:9090
- **n8n**: http://localhost:5678

### Support Channels
- **Slack**: #circuit-os-support
- **GitHub Issues**: github.com/<repo>/issues
- **Team Wiki**: notion.so/<workspace>/circuit-os

---

## ✅ SUCCESS CRITERIA

**System is production-ready when**:
- [ ] All health checks pass
- [ ] Cache hit rate >30%
- [ ] Query latency <250ms (p95)
- [ ] All agents respond <500ms
- [ ] Zero downtime in 7 days
- [ ] Team can deploy without assistance
- [ ] Monitoring shows green across all services

**Team is onboarded when**:
- [ ] Can run health checks independently
- [ ] Can deploy updates safely
- [ ] Can troubleshoot common issues
- [ ] Can interpret Grafana dashboards
- [ ] Can add new Cursor commands
- [ ] Can modify VS Code tasks

---

**Built for scale. Ready for your team.**

Version 1.0.0 | January 2025
