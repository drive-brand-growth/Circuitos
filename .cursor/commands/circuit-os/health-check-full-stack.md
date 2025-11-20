# Circuit OS Full Stack Health Check

Comprehensive health check across all 15+ Docker services.

## Services to Check:

### Core AI Services (5)
1. **metroflex-ai** (Port 5001)
2. **ml-api** (Port 5000)
3. **agentforce-api** (Port 8000)
4. **agentforce-web** (Port 3001)
5. **virtual-agentforce** (Port 8001)
6. **circuit-script** (Port 3000)

### Infrastructure (3)
7. **postgres** (Port 5432)
8. **redis** (Port 6379)
9. **nginx** (Port 80/443)

### Monitoring Stack (5)
10. **prometheus** (Port 9090)
11. **grafana** (Port 3002)
12. **alertmanager** (Port 9093)
13. **loki** (Port 3100)
14. **promtail** (logs shipper)

### Utilities (2)
15. **backup** (database backups)
16. **healthcheck-ui** (autoheal)

## Quick Health Check Script:

```bash
#!/bin/bash
echo "=== Circuit OS Health Check ==="
echo ""

# Docker Compose Status
echo "📦 Docker Services Status:"
docker compose ps | grep -E "(Up|running)" | wc -l
echo "/16 services running"
echo ""

# Core AI Services
echo "🤖 AI Services:"
curl -s http://localhost:5001/health | jq -r '.status' && echo "✅ MetroFlex AI"
curl -s http://localhost:5000/health | jq -r '.status' && echo "✅ ML API"
curl -s http://localhost:8000/health | jq -r '.status' && echo "✅ Agentforce API"
curl -s http://localhost:3000/health | jq -r '.status' && echo "✅ Circuit Script"
echo ""

# RAG System
echo "🔍 RAG System:"
curl -s http://localhost:5001/api/rag/health | jq '{
  status,
  documents,
  chunks,
  features
}'
echo ""

# Infrastructure
echo "🗄️  Infrastructure:"
docker exec circuitos-db pg_isready && echo "✅ PostgreSQL"
docker exec circuitos-redis redis-cli ping && echo "✅ Redis"
curl -s http://localhost:80/health && echo "✅ NGINX"
echo ""

# Monitoring
echo "📊 Monitoring Stack:"
curl -s http://localhost:9090/-/healthy && echo "✅ Prometheus"
curl -s http://localhost:3002/api/health | jq -r '.database' && echo "✅ Grafana"
curl -s http://localhost:3100/ready && echo "✅ Loki"
echo ""

# Resource Usage
echo "💾 Resource Usage:"
docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}" | head -n 10
echo ""

echo "=== Health Check Complete ==="
```

## Detailed Checks:

### Database Health
```bash
# Check all databases
docker exec circuitos-db psql -U circuitos -c "\l" | grep -E "(agentforce|ml_audit|circuit_runtime)"

# Check pgvector extension
docker exec circuitos-db psql -U circuitos -d agentforce -c "\dx vector"

# Check table sizes
docker exec circuitos-db psql -U circuitos -d agentforce -c "
SELECT
  schemaname,
  tablename,
  pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC
LIMIT 10;
"
```

### Redis Health
```bash
# Check Redis info
docker exec circuitos-redis redis-cli INFO | grep -E "(uptime_in_seconds|used_memory_human|connected_clients)"

# Check RAG cache
docker exec circuitos-redis redis-cli KEYS "rag:cache:*" | wc -l
```

## Alerts to Monitor:

Critical (Immediate Action):
- Any service status != "Up"
- PostgreSQL down
- Redis down
- Disk usage >90%

Warning (Monitor):
- High memory usage (>80%)
- Slow response times (>500ms)
- Cache hit rate <20%

## Automated Health Checks:

This health check runs automatically:
1. **Docker healthchecks**: Every 30 seconds per service
2. **Prometheus scrapes**: Every 15 seconds
3. **AlertManager notifications**: Slack #circuit-os-alerts
4. **Grafana dashboards**: Real-time visualization

Access dashboards:
- Overview: http://localhost:3002/d/circuit-os-overview
- Services: http://localhost:3002/d/circuit-os-services
- Infrastructure: http://localhost:3002/d/circuit-os-infra
