# Monitor Circuit OS Resource Usage

Track CPU, memory, disk, and network usage across all services.

## Quick Overview:

```bash
# Real-time stats for all containers
docker stats

# Top 5 CPU consumers
docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}" | sort -k2 -rn | head -6

# Top 5 memory consumers
docker stats --no-stream --format "table {{.Name}}\t{{.MemUsage}}" | sort -k2 -rn | head -6
```

## Detailed Analysis:

### CPU Usage
```bash
# CPU usage over 24 hours (Prometheus query)
curl -s 'http://localhost:9090/api/v1/query?query=rate(container_cpu_usage_seconds_total[5m])' | \
  jq '.data.result[] | {
    container: .metric.name,
    cpu_usage: .value[1]
  }'
```

Expected ranges:
- metroflex-ai: 5-15% (varies with query load)
- postgres: 2-10%
- redis: 1-5%
- prometheus: 2-8%

### Memory Usage
```bash
# Memory usage by container
docker stats --no-stream --format "{{.Name}}: {{.MemUsage}}" | sort

# Check for memory leaks (increasing trend)
docker stats --no-stream --format "{{.Name}}\t{{.MemPerc}}" | \
  awk '$2 > 80 {print "⚠️  HIGH: " $0} $2 <= 80 {print "✅ OK: " $0}'
```

Resource limits (from docker-compose.yml):
- ml-api: 2GB limit, 1GB reserved
- Other services: No hard limits (monitor for runaway processes)

### Disk Usage
```bash
# Docker volumes
docker system df -v

# PostgreSQL database sizes
docker exec circuitos-db psql -U circuitos -c "
SELECT
  datname,
  pg_size_pretty(pg_database_size(datname)) as size
FROM pg_database
WHERE datname IN ('agentforce', 'ml_audit', 'circuit_runtime')
ORDER BY pg_database_size(datname) DESC;
"

# Check disk space on host
df -h | grep -E "(Filesystem|/$)"
```

Critical thresholds:
- **Warning**: >70% disk usage
- **Critical**: >85% disk usage
- **Emergency**: >95% disk usage (services may crash)

### Network Usage
```bash
# Network stats per container
docker stats --no-stream --format "table {{.Name}}\t{{.NetIO}}"

# Check for abnormal traffic
docker stats --no-stream --format "{{.Name}}: RX={{.NetIO}}" | \
  awk -F'/' '{print $1}' | sort -k2 -rn
```

Red flags:
- Unexpected outbound traffic (potential security issue)
- Very high inbound to wrong service (DDoS attempt?)
- Zero network activity on active service (networking issue)

## Performance Benchmarks:

| Service | CPU (Avg) | Memory (Peak) | Disk I/O | Network |
|---------|-----------|---------------|----------|---------|
| metroflex-ai | 5-15% | 512MB | Low | Medium |
| postgres | 5-10% | 1GB | High | Low |
| redis | 1-5% | 256MB | Medium | High |
| prometheus | 5-8% | 800MB | Medium | Low |
| grafana | 2-5% | 400MB | Low | Low |

## Grafana Dashboards:

Access real-time metrics:
1. **System Overview**: http://localhost:3002/d/circuit-os-resources
   - CPU usage per container
   - Memory usage trends
   - Disk I/O rates
   - Network throughput

2. **Container Metrics**: http://localhost:3002/d/docker-containers
   - Per-container resource breakdown
   - Historical trends (7 days)
   - Anomaly detection alerts

3. **Database Performance**: http://localhost:3002/d/postgres-metrics
   - Query performance
   - Connection pool usage
   - Cache hit rates
   - Slow query log

## Automated Alerts:

AlertManager triggers notifications for:

**Critical (PagerDuty + Slack)**:
- CPU >90% for >5 minutes
- Memory >95% for >2 minutes
- Disk >95% usage
- Service health check failures

**Warning (Slack only)**:
- CPU >70% for >15 minutes
- Memory >80% for >10 minutes
- Disk >80% usage
- Slow database queries (>1s)

## Optimization Actions:

### If CPU is high:
1. Check Prometheus for which service
2. Review recent deployments (new code causing load?)
3. Scale horizontally (add more containers)
4. Profile slow code paths

### If memory is high:
1. Check for memory leaks (increasing trend over days)
2. Restart affected service: `docker compose restart <service>`
3. Review logs for OOM errors
4. Adjust memory limits in docker-compose.yml

### If disk is high:
1. Clean Docker images: `docker system prune -a`
2. Clean old logs: `docker compose logs --tail 100 > /dev/null`
3. Compress old backups
4. Purge old RAG chunks (documents >90 days with no feedback)

### If network is high:
1. Check if it's expected (large file transfers, backups)
2. Review NGINX access logs for traffic patterns
3. Enable rate limiting if DDoS suspected
4. Check for malicious actors in logs

## Weekly Maintenance:

```bash
# Run every Monday
docker system prune -f  # Clean unused images
docker volume prune -f  # Clean unused volumes
docker compose logs --tail 1000 > logs/archive-$(date +%Y-%m-%d).log  # Archive logs
# Compress old backups older than 30 days
find ./backups -name "*.sql.gz" -mtime +30 -exec gzip {} \;
```
