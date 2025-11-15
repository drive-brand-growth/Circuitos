# CircuitOS Docker Cheat Sheet

**Quick reference for daily Docker operations**

---

## 🚀 Getting Started

```bash
# Initial setup (one time)
cp .env.example .env
nano .env  # Add your OPENAI_API_KEY

# Start everything
docker-compose up -d

# Check status
docker-compose ps
```

---

## 📦 Service Management

```bash
# Start all services
docker-compose up -d

# Stop all services (keep data)
docker-compose down

# Stop and delete data (fresh start)
docker-compose down -v

# Restart specific service
docker-compose restart metroflex-ai

# Rebuild and restart
docker-compose up -d --build metroflex-ai

# Scale a service
docker-compose up -d --scale ml-api=3
```

---

## 🔍 Viewing Logs

```bash
# All logs (live)
docker-compose logs -f

# Specific service
docker-compose logs -f metroflex-ai

# Last 100 lines
docker-compose logs --tail=100 ml-api

# Multiple services
docker-compose logs -f metroflex-ai ml-api

# Search logs
docker-compose logs | grep -i error
```

---

## 🏥 Health Checks

```bash
# Check all services
docker-compose ps

# Test health endpoints
curl http://localhost:5001/health  # MetroFlex AI
curl http://localhost:5000/health  # ML API
curl http://localhost:8000/health  # Agentforce API

# Check container health
docker inspect --format='{{.State.Health.Status}}' metroflex-ai-agent

# Auto-restart unhealthy containers (built-in)
# Handled automatically by autoheal service
```

---

## 💾 Database Operations

```bash
# Connect to PostgreSQL
docker-compose exec postgres psql -U circuitos -d agentforce

# List databases
docker-compose exec postgres psql -U circuitos -c "\l"

# Run SQL file
docker-compose exec postgres psql -U circuitos -d agentforce -f /path/to/file.sql

# Backup database
docker-compose exec postgres pg_dump -U circuitos agentforce > backup.sql

# Restore database
cat backup.sql | docker-compose exec -T postgres psql -U circuitos -d agentforce

# Connect to Redis
docker-compose exec redis redis-cli

# Check Redis keys
docker-compose exec redis redis-cli KEYS '*'

# Clear Redis cache
docker-compose exec redis redis-cli FLUSHALL
```

---

## 🔧 Debugging

```bash
# Enter container shell
docker-compose exec metroflex-ai /bin/bash

# Run command in container
docker-compose exec metroflex-ai python --version

# Copy file from container
docker cp metroflex-ai-agent:/app/logs/error.log ./local-error.log

# Copy file to container
docker cp local-config.json metroflex-ai-agent:/app/config.json

# View container details
docker inspect metroflex-ai-agent

# View resource usage
docker stats

# View container processes
docker-compose top metroflex-ai
```

---

## 🌐 Network & Ports

```bash
# Check port mappings
docker-compose ps

# Test port connectivity
nc -zv localhost 5000  # ML API
nc -zv localhost 5001  # MetroFlex AI
nc -zv localhost 8000  # Agentforce API

# View network details
docker network inspect circuitos_circuitos-network

# Check what's using a port
lsof -i :5000
```

---

## 📊 Monitoring

```bash
# Open Grafana
open http://localhost:3002
# Login: admin / admin (or GRAFANA_PASSWORD from .env)

# Open Prometheus
open http://localhost:9090

# View metrics endpoint
curl http://localhost:5000/metrics  # ML API metrics

# Check Alertmanager
open http://localhost:9093
```

---

## 🛠 Development Workflow

```bash
# 1. Make code changes
nano Active/metroflex-ghl-website/AI_Agent/app.py

# 2. Rebuild service
docker-compose build metroflex-ai

# 3. Restart service
docker-compose up -d metroflex-ai

# 4. Watch logs
docker-compose logs -f metroflex-ai

# 5. Test changes
curl http://localhost:5001/health

# Quick restart without rebuild (if no dependency changes)
docker-compose restart metroflex-ai
```

---

## 🧹 Cleanup

```bash
# Remove stopped containers
docker-compose down

# Remove everything including volumes
docker-compose down -v

# Clean up Docker system
docker system prune -a

# Remove unused images
docker image prune -a

# Remove unused volumes
docker volume prune

# See disk usage
docker system df
```

---

## 🔄 Updates & Maintenance

```bash
# Pull latest images
docker-compose pull

# Rebuild all services
docker-compose build

# Update and restart
docker-compose up -d --build

# Rolling update (one service at a time)
docker-compose up -d --no-deps --build metroflex-ai
```

---

## 🚨 Emergency Commands

```bash
# Stop everything immediately
docker-compose down

# Kill all containers
docker kill $(docker ps -q)

# Restart Docker daemon (Mac)
killall Docker && open /Applications/Docker.app

# View last crash logs
docker-compose logs --tail=100 metroflex-ai

# Restore from backup
cat backup.sql | docker-compose exec -T postgres psql -U circuitos

# Rollback to previous version
docker tag metroflex-ai:v1.1 metroflex-ai:old
docker tag metroflex-ai:v1.0 metroflex-ai:latest
docker-compose up -d metroflex-ai
```

---

## 🧪 Testing

```bash
# Test MetroFlex AI
curl -X POST http://localhost:5001/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What time should I arrive?"}'

# Test ML API
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"engagement_score": 87, "company_size": 550, "budget": 125000}'

# Test Agentforce API
curl http://localhost:8000/docs  # Swagger UI

# Load test (with hey)
hey -n 1000 -c 10 http://localhost:5000/health
```

---

## 📈 Performance

```bash
# Check resource usage
docker stats

# Limit resources (edit docker-compose.yml)
deploy:
  resources:
    limits:
      cpus: '2'
      memory: 2G

# Scale service
docker-compose up -d --scale ml-api=5

# Check scaled instances
docker-compose ps ml-api
```

---

## 🔒 Security

```bash
# Scan image for vulnerabilities
docker scan metroflex-ai:latest

# Check for security updates
docker-compose pull

# Rotate secrets
nano .env  # Change passwords
docker-compose down
docker-compose up -d

# View security logs
docker-compose logs | grep -i "unauthorized\|failed\|error"
```

---

## 📱 Quick Access URLs

| Service | URL | Purpose |
|---------|-----|---------|
| MetroFlex AI | http://localhost:5001 | Chat API |
| ML API | http://localhost:5000 | Lead scoring |
| Agentforce API | http://localhost:8000 | Lost opp agent |
| Agentforce UI | http://localhost:3001 | Control panel |
| Circuit Script | http://localhost:3000 | Script runtime |
| Grafana | http://localhost:3002 | Dashboards |
| Prometheus | http://localhost:9090 | Metrics |
| Alertmanager | http://localhost:9093 | Alerts |

---

## 🆘 Common Issues

**Issue:** Service won't start
```bash
# Check logs
docker-compose logs service-name
# Check if port is in use
lsof -i :5000
```

**Issue:** Database connection failed
```bash
# Check database is running
docker-compose ps postgres
# Wait for health check
docker-compose up -d && sleep 30
```

**Issue:** Out of memory
```bash
# Check usage
docker stats
# Increase Docker memory (Settings → Resources → 8GB)
```

**Issue:** Build failed
```bash
# Clean and rebuild
docker-compose down -v
docker system prune -a
docker-compose up -d --build
```

---

## 📚 Documentation Links

- [Full Guide](DOCKER_QUICKSTART.md)
- [Strategy Doc](DOCKER_CONSOLIDATION_STRATEGY.md)
- [ML Deployment](../CircuitOS-Project/CIRCUIT-ML-QUICKSTART.md)
- [Migration Summary](DOCKER_MIGRATION_SUMMARY.md)

---

## 💡 Pro Tips

**Tip 1:** Use aliases
```bash
alias dcup='docker-compose up -d'
alias dcdown='docker-compose down'
alias dclogs='docker-compose logs -f'
alias dcps='docker-compose ps'
```

**Tip 2:** Auto-restart on file changes (development)
```bash
# Use volumes for hot-reload
volumes:
  - ./Active/metroflex-ghl-website/AI_Agent:/app
```

**Tip 3:** Multi-environment setup
```bash
# Development
docker-compose up -d

# Staging
docker-compose -f docker-compose.yml -f docker-compose.staging.yml up -d

# Production
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

**Tip 4:** Quick logs for debugging
```bash
# Show only errors
docker-compose logs | grep -i error

# Show with timestamps
docker-compose logs -t

# Follow multiple services
docker-compose logs -f metroflex-ai ml-api
```

**Tip 5:** Health check all services
```bash
# One-liner health check
for port in 5000 5001 8000; do
  curl -s http://localhost:$port/health | jq
done
```

---

**Print this and keep it handy!** 📄

**Questions?** See [DOCKER_QUICKSTART.md](DOCKER_QUICKSTART.md)
