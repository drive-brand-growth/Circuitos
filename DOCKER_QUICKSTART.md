# CircuitOS Docker Quick Start Guide

**Time to first deployment:** 15 minutes
**Prerequisites:** Docker Desktop installed

---

## 🚀 Quick Start (3 Steps)

### Step 1: Clone and Configure (5 minutes)

```bash
# 1. Navigate to project directory
cd CircuitOS_Local_Complete_Package

# 2. Create environment file
cp .env.example .env

# 3. Edit .env with your API keys
# Required: Add your OpenAI API key
# Optional: Add Anthropic API key, change passwords
nano .env  # or use any text editor
```

**Minimum required configuration:**
```bash
# .env
OPENAI_API_KEY=sk-proj-YOUR_ACTUAL_KEY_HERE
POSTGRES_PASSWORD=your_secure_password
```

---

### Step 2: Start Everything (5 minutes)

```bash
# Build and start all services
docker-compose up -d

# This will:
# - Build 6 Docker images (~3-5 minutes first time)
# - Start PostgreSQL, Redis, NGINX
# - Start all AI services
# - Start monitoring (Prometheus, Grafana)

# Watch the progress
docker-compose logs -f
```

**Expected output:**
```
✅ circuitos-db        ... started
✅ circuitos-redis     ... started
✅ metroflex-ai-agent  ... started
✅ ml-lead-qualifier   ... started
✅ agentforce-api      ... started
✅ agentforce-web      ... started
✅ circuit-script      ... started
✅ circuitos-proxy     ... started
✅ circuitos-metrics   ... started
✅ circuitos-dashboards... started
```

---

### Step 3: Verify and Use (5 minutes)

```bash
# Check all services are healthy
docker-compose ps

# Should show all services as "healthy" or "running"
```

**Access your services:**

| Service | URL | Purpose |
|---------|-----|---------|
| **MetroFlex AI Chat** | http://localhost:5001 | Event chatbot API |
| **ML Lead Qualifier** | http://localhost:5000 | Lead scoring API |
| **Agentforce API** | http://localhost:8000 | Lost opportunity agent |
| **Agentforce Dashboard** | http://localhost:3001 | Control panel UI |
| **Circuit Script Runtime** | http://localhost:3000 | Script execution engine |
| **Grafana Dashboards** | http://localhost:3002 | Metrics & monitoring |
| **Prometheus** | http://localhost:9090 | Raw metrics |
| **Main Proxy** | http://localhost | Unified entry point |

---

## 🧪 Test Your Setup

### Test 1: Health Checks

```bash
# Test all services
curl http://localhost:5001/health  # MetroFlex AI
curl http://localhost:5000/health  # ML API
curl http://localhost:8000/health  # Agentforce API
curl http://localhost:3000/health  # Circuit Script
curl http://localhost/health       # NGINX proxy

# All should return: {"status": "healthy"}
```

### Test 2: MetroFlex AI Chat

```bash
# Send a test query
curl -X POST http://localhost:5001/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What time should I arrive for the event?"
  }'

# Expected: AI response about arrival time
```

### Test 3: ML Lead Qualification

```bash
# Score a lead
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "engagement_score": 87,
    "company_size": 550,
    "budget": 125000,
    "industry": "Technology",
    "previous_purchases": 2
  }'

# Expected: {"prediction": "QUALIFIED", "confidence": 0.92, ...}
```

### Test 4: View Dashboards

```bash
# Open Grafana
open http://localhost:3002

# Login: admin / admin (or your GRAFANA_PASSWORD from .env)
# Navigate to: Dashboards → CircuitOS Overview
```

---

## 📊 What's Running?

### Core AI Services (6 containers)

```
1. metroflex-ai-agent     - MetroFlex event chatbot
2. ml-lead-qualifier      - ML-based lead scoring
3. agentforce-api         - Lost opportunity automation
4. agentforce-web         - Agentforce UI
5. virtual-agentforce     - Virtual agent runtime
6. circuit-script-runtime - Script execution engine
```

### Infrastructure (3 containers)

```
7. circuitos-db          - PostgreSQL (4 databases)
8. circuitos-redis       - Redis cache & pub/sub
9. circuitos-proxy       - NGINX reverse proxy
```

### Monitoring (4 containers)

```
10. circuitos-metrics    - Prometheus metrics
11. circuitos-dashboards - Grafana dashboards
12. circuitos-alerts     - Alertmanager
13. circuitos-logs       - Loki log aggregation
```

**Total:** 13 containers, all orchestrated automatically

---

## 🛠 Common Commands

### Start/Stop

```bash
# Start everything
docker-compose up -d

# Stop everything (keeps data)
docker-compose down

# Stop and delete all data (fresh start)
docker-compose down -v

# Restart a specific service
docker-compose restart metroflex-ai

# Rebuild and restart after code changes
docker-compose up -d --build metroflex-ai
```

### Logs & Debugging

```bash
# View all logs
docker-compose logs -f

# View logs for specific service
docker-compose logs -f metroflex-ai

# View last 100 lines
docker-compose logs --tail=100 ml-api

# Follow logs from multiple services
docker-compose logs -f metroflex-ai ml-api
```

### Check Status

```bash
# Show all containers
docker-compose ps

# Show resource usage
docker stats

# Check service health
docker inspect --format='{{.State.Health.Status}}' metroflex-ai-agent
```

### Database Access

```bash
# Connect to PostgreSQL
docker-compose exec postgres psql -U circuitos -d agentforce

# List all databases
docker-compose exec postgres psql -U circuitos -c "\l"

# Connect to Redis
docker-compose exec redis redis-cli

# Check Redis keys
docker-compose exec redis redis-cli KEYS '*'
```

### Scaling

```bash
# Scale ML API to 3 instances
docker-compose up -d --scale ml-api=3

# Check scaled instances
docker-compose ps ml-api
```

---

## 🔧 Troubleshooting

### Problem: Services won't start

**Solution 1: Check Docker is running**
```bash
docker info
# If error: Start Docker Desktop
```

**Solution 2: Check ports are available**
```bash
# Check if ports 80, 443, 5000, 5001, 8000 are in use
lsof -i :80
lsof -i :5000

# If port is in use, either:
# - Stop the conflicting service
# - Change port in docker-compose.yml
```

**Solution 3: Check logs for errors**
```bash
docker-compose logs | grep -i error
```

---

### Problem: "Permission denied" errors

**Solution:**
```bash
# Fix log directory permissions
mkdir -p logs
chmod -R 777 logs

# Restart services
docker-compose restart
```

---

### Problem: Database connection errors

**Solution:**
```bash
# Check PostgreSQL is healthy
docker-compose ps postgres

# View PostgreSQL logs
docker-compose logs postgres

# Restart database
docker-compose restart postgres

# Wait for health check
docker-compose ps | grep healthy
```

---

### Problem: Out of memory errors

**Solution:**
```bash
# Check Docker resources
docker info | grep -i memory

# Increase Docker Desktop memory:
# Docker Desktop → Settings → Resources → Memory → 8GB minimum

# Restart Docker Desktop
```

---

### Problem: Build fails

**Solution 1: Clean build cache**
```bash
# Remove all images and rebuild
docker-compose down -v
docker system prune -a
docker-compose up -d --build
```

**Solution 2: Check Dockerfile exists**
```bash
# Verify Dockerfiles are in place
ls Active/metroflex-ghl-website/AI_Agent/Dockerfile
ls ../CircuitOS-Project/Dockerfile
ls Active/agentforce_emulator/Dockerfile.api
```

---

### Problem: Service keeps restarting

**Solution:**
```bash
# Check why it's failing
docker-compose logs --tail=50 <service-name>

# Common causes:
# 1. Missing environment variable (check .env)
# 2. Database not ready (wait 30 seconds)
# 3. Port conflict (change port in docker-compose.yml)
# 4. Missing dependency (rebuild image)
```

---

## 🎯 Development Workflow

### Making Code Changes

```bash
# 1. Edit code in your IDE
nano Active/metroflex-ghl-website/AI_Agent/app.py

# 2. Rebuild and restart the service
docker-compose up -d --build metroflex-ai

# 3. Watch logs
docker-compose logs -f metroflex-ai

# 4. Test changes
curl http://localhost:5001/health
```

### Adding New Dependencies

```bash
# 1. Update requirements.txt
echo "new-package==1.0.0" >> Active/metroflex-ghl-website/AI_Agent/requirements.txt

# 2. Rebuild image
docker-compose build metroflex-ai

# 3. Restart service
docker-compose up -d metroflex-ai
```

### Database Migrations

```bash
# 1. Create migration SQL
cat > docker/migrations/001_add_table.sql <<EOF
CREATE TABLE new_table (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100)
);
EOF

# 2. Run migration
docker-compose exec postgres psql -U circuitos -d agentforce -f /migrations/001_add_table.sql

# 3. Verify
docker-compose exec postgres psql -U circuitos -d agentforce -c "\dt"
```

---

## 📈 Monitoring

### Grafana Dashboards

```bash
# Open Grafana
open http://localhost:3002

# Default login: admin / admin

# Pre-configured dashboards:
# - CircuitOS Overview (all services)
# - ML Model Performance
# - Database Health
# - API Response Times
```

### Prometheus Queries

```bash
# Open Prometheus
open http://localhost:9090

# Example queries:
# - Requests per second: rate(http_requests_total[1m])
# - Error rate: rate(http_requests_total{status=~"5.."}[1m])
# - P95 latency: histogram_quantile(0.95, http_request_duration_seconds)
```

### Logs with Loki

```bash
# View in Grafana Explore
# 1. Open Grafana → Explore
# 2. Select Loki data source
# 3. Query: {container_name="metroflex-ai-agent"}
# 4. See real-time logs
```

---

## 🚀 Production Deployment

### Deploy to Server

```bash
# 1. Copy project to server
rsync -avz CircuitOS_Local_Complete_Package/ user@server:/opt/circuitos/

# 2. SSH to server
ssh user@server

# 3. Start services
cd /opt/circuitos
docker-compose up -d

# 4. Configure firewall
ufw allow 80/tcp
ufw allow 443/tcp

# 5. Set up SSL
# (see SSL_SETUP_GUIDE.md)
```

### Environment-Specific Configs

```bash
# Development
ENVIRONMENT=development docker-compose up -d

# Staging
ENVIRONMENT=staging docker-compose -f docker-compose.yml -f docker-compose.staging.yml up -d

# Production
ENVIRONMENT=production docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

---

## 💾 Backup & Restore

### Automated Backups

Backups run automatically daily at midnight (configured in docker-compose.yml).

**Location:** `docker/postgres-backup/`

**Retention:**
- Daily: 7 days
- Weekly: 4 weeks
- Monthly: 6 months

### Manual Backup

```bash
# Backup all databases
docker-compose exec postgres pg_dumpall -U circuitos > backup_$(date +%Y%m%d).sql

# Backup specific database
docker-compose exec postgres pg_dump -U circuitos agentforce > agentforce_backup.sql
```

### Restore from Backup

```bash
# Stop services
docker-compose down

# Restore database
cat backup_20251115.sql | docker-compose exec -T postgres psql -U circuitos

# Start services
docker-compose up -d
```

---

## 🔒 Security Checklist

Before deploying to production:

- [ ] Changed default passwords in .env
- [ ] Generated SSL certificates
- [ ] Enabled firewall (only ports 80, 443)
- [ ] Set up automated backups
- [ ] Configured monitoring alerts
- [ ] Reviewed logs for errors
- [ ] Tested rollback procedure
- [ ] Documented access credentials (securely)

---

## 📚 Next Steps

### Week 1: Get Familiar
- [ ] Start stack locally
- [ ] Test all services
- [ ] Review Grafana dashboards
- [ ] Make a code change and redeploy

### Week 2: Customize
- [ ] Update environment variables for your use case
- [ ] Configure GHL webhooks
- [ ] Set up Slack alerts
- [ ] Add custom Grafana dashboards

### Week 3: Production Deploy
- [ ] Deploy to staging server
- [ ] Load test (see LOAD_TESTING.md)
- [ ] Security audit (see SECURITY_CHECKLIST.md)
- [ ] Deploy to production

---

## 🆘 Getting Help

**Documentation:**
- [Full Docker Strategy](DOCKER_CONSOLIDATION_STRATEGY.md)
- [ML Deployment Guide](../CircuitOS-Project/CIRCUIT-ML-QUICKSTART.md)
- [Architecture Overview](Documentation/PROJECT-OVERVIEW.md)

**Common Issues:**
- Check [TROUBLESHOOTING.md](docker/TROUBLESHOOTING.md)
- Search GitHub Issues
- Review Docker logs

**Support:**
- GitHub Issues: Tag with `docker`
- Slack: #circuitos-docker
- Email: support@circuitos.com

---

**Built by:** CircuitOS DevOps Team
**Last Updated:** November 2025
**Version:** 1.0

**Questions?** Open an issue or ping @devops-team on Slack.
