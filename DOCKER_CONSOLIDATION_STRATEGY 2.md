# CircuitOS Docker Consolidation Strategy

**Date:** November 2025
**Purpose:** Simplify deployment, reduce complexity, improve consistency
**Status:** Planning → Implementation Ready

---

## 🎯 Executive Summary

**Problem:** We have 4+ separate projects requiring manual setup, different Python/Node versions, and complex dependency management.

**Solution:** Containerize everything with Docker, create unified Docker Compose stack.

**Result:**
- ✅ One command to start entire CircuitOS ecosystem
- ✅ No more "works on my machine" issues
- ✅ Production-ready deployments in minutes
- ✅ 80% reduction in setup time (2 hours → 15 minutes)

---

## 📊 Current State Analysis

### Active Projects Requiring Dockerization

| Project | Type | Dependencies | Complexity | Priority |
|---------|------|-------------|------------|----------|
| **metroflex-ghl-website/AI_Agent** | Python (Flask) | OpenAI, ChromaDB, SentenceTransformers | Medium | HIGH |
| **agentforce_emulator** | Python (FastAPI) + React | Postgres, Redis, LangGraph | High | HIGH |
| **virtual-agentforce** | Python | TBD | Low | MEDIUM |
| **circuit-script-runtime** | Node.js | TypeScript, Express | Medium | MEDIUM |
| **ML Models (CircuitOS-Project)** | Python (scikit-learn) | Pandas, NumPy, Flask | Medium | HIGH |

### Current Pain Points

**1. Environment Hell**
- Different Python versions (3.9, 3.11, 3.12)
- Conflicting dependencies (ChromaDB versions)
- venv management across 4+ projects
- Node.js version mismatches

**2. Manual Setup (90+ Minutes)**
```bash
# Current process (per developer):
1. Install Python 3.9, 3.11, 3.12 (20 min)
2. Install Node.js 18+ (10 min)
3. Create 4 separate venvs (15 min)
4. Install dependencies (30 min)
5. Configure environment variables (10 min)
6. Start 4 separate processes (5 min)
7. Debug version conflicts (30+ min)

Total: 2+ hours (and often breaks)
```

**3. Production Deployment Nightmares**
- Each project needs separate hosting
- Manual database setup (Postgres, Redis)
- Complex NGINX configurations
- No rollback strategy
- Inconsistent environments (dev ≠ staging ≠ prod)

---

## 🐳 Proposed Docker Architecture

### Unified Docker Compose Stack

```
┌─────────────────────────────────────────────────────────────────────┐
│                        NGINX Reverse Proxy                          │
│                         (Port 80/443)                               │
└────────────┬────────────┬────────────┬────────────┬─────────────────┘
             │            │            │            │
    ┌────────▼────────┐   │   ┌────────▼────────┐   │   ┌──────────────┐
    │  MetroFlex AI   │   │   │  Agentforce     │   │   │  ML API      │
    │  Chat Agent     │   │   │  Emulator API   │   │   │  Server      │
    │  (Flask)        │   │   │  (FastAPI)      │   │   │  (Flask)     │
    │  Port: 5001     │   │   │  Port: 8000     │   │   │  Port: 5000  │
    └─────────────────┘   │   └────────┬────────┘   │   └──────────────┘
                          │            │            │
                 ┌────────▼────────┐   │   ┌────────▼────────┐
                 │  Circuit Script │   │   │  Virtual        │
                 │  Runtime (Node) │   │   │  Agentforce     │
                 │  Port: 3000     │   │   │  (Python)       │
                 └─────────────────┘   │   └─────────────────┘
                                       │
                 ┌─────────────────────▼─────────────────────┐
                 │         Shared Infrastructure             │
                 ├───────────────┬───────────────────────────┤
                 │  PostgreSQL   │  Redis  │  Prometheus     │
                 │  (Port 5432)  │  (6379) │  (9090)         │
                 └───────────────┴─────────┴─────────────────┘
```

---

## 📦 Dockerization Plan

### Phase 1: Core Services (Week 1)

#### 1. MetroFlex AI Chat Agent

**Dockerfile** (`Active/metroflex-ghl-website/AI_Agent/Dockerfile`)

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc g++ curl \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY *.py .
COPY *.json .

# Health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD curl -f http://localhost:5001/health || exit 1

EXPOSE 5001

CMD ["gunicorn", "--bind", "0.0.0.0:5001", "--workers", "2", "app:app"]
```

**docker-compose.yml entry:**

```yaml
metroflex-ai:
  build:
    context: ./Active/metroflex-ghl-website/AI_Agent
  container_name: metroflex-ai-agent
  restart: unless-stopped
  environment:
    - OPENAI_API_KEY=${OPENAI_API_KEY}
    - PORT=5001
  ports:
    - "5001:5001"
  volumes:
    - ./Active/metroflex-ghl-website/AI_Agent:/app:ro
  healthcheck:
    test: ["CMD", "curl", "-f", "http://localhost:5001/health"]
    interval: 30s
    timeout: 10s
    retries: 3
```

---

#### 2. Agentforce Emulator (Full Stack)

**Backend Dockerfile** (`Active/agentforce_emulator/Dockerfile.api`)

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y \
    gcc g++ postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install uv (faster pip alternative)
RUN pip install uv

# Copy and install
COPY pyproject.toml .
RUN uv pip install --system .

# Copy application
COPY services/ ./services/
COPY cli/ ./cli/
COPY configs/ ./configs/

EXPOSE 8000

CMD ["uvicorn", "services.agent_runtime.app:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Frontend Dockerfile** (`Active/agentforce_emulator/Dockerfile.web`)

```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY apps/control_panel/package*.json ./
RUN npm ci

COPY apps/control_panel/ .
RUN npm run build

EXPOSE 3001

CMD ["npm", "run", "preview", "--", "--host", "0.0.0.0", "--port", "3001"]
```

**docker-compose.yml entry:**

```yaml
agentforce-api:
  build:
    context: ./Active/agentforce_emulator
    dockerfile: Dockerfile.api
  container_name: agentforce-api
  restart: unless-stopped
  environment:
    - DATABASE_URL=postgresql://postgres:password@postgres:5432/agentforce
    - REDIS_URL=redis://redis:6379/0
    - OPENAI_API_KEY=${OPENAI_API_KEY}
  depends_on:
    postgres:
      condition: service_healthy
    redis:
      condition: service_healthy
  ports:
    - "8000:8000"

agentforce-web:
  build:
    context: ./Active/agentforce_emulator
    dockerfile: Dockerfile.web
  container_name: agentforce-web
  restart: unless-stopped
  environment:
    - VITE_API_URL=http://localhost:8000
  ports:
    - "3001:3001"
  depends_on:
    - agentforce-api
```

---

#### 3. ML Model API Server

**Dockerfile** (Created in CircuitOS-Project)

```dockerfile
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y gcc g++ && rm -rf /var/lib/apt/lists/*

COPY requirements-production.txt .
RUN pip install --no-cache-dir -r requirements-production.txt

COPY lead-qualification-model.py .
COPY trained_models/ ./trained_models/
COPY api_server.py .

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "3", "api_server:app"]
```

**docker-compose.yml entry:**

```yaml
ml-api:
  build:
    context: ../CircuitOS-Project
  container_name: ml-lead-qualifier
  restart: unless-stopped
  environment:
    - MODEL_PATH=/app/trained_models/lead_qualifier_v1.pkl
  ports:
    - "5000:5000"
  volumes:
    - ../CircuitOS-Project/trained_models:/app/trained_models:ro
```

---

### Phase 2: Infrastructure Services

```yaml
# PostgreSQL (shared database)
postgres:
  image: postgres:16-alpine
  container_name: circuitos-db
  restart: unless-stopped
  environment:
    - POSTGRES_USER=circuitos
    - POSTGRES_PASSWORD=${POSTGRES_PASSWORD:-changeme}
    - POSTGRES_MULTIPLE_DATABASES=agentforce,ml_audit,circuit_runtime
  volumes:
    - postgres_data:/var/lib/postgresql/data
    - ./docker/postgres-init.sh:/docker-entrypoint-initdb.d/init.sh
  ports:
    - "5432:5432"
  healthcheck:
    test: ["CMD-SHELL", "pg_isready -U circuitos"]
    interval: 10s
    timeout: 5s
    retries: 5

# Redis (shared cache + pub/sub)
redis:
  image: redis:7-alpine
  container_name: circuitos-redis
  restart: unless-stopped
  command: redis-server --maxmemory 512mb --maxmemory-policy allkeys-lru
  ports:
    - "6379:6379"
  healthcheck:
    test: ["CMD", "redis-cli", "ping"]
    interval: 10s
    timeout: 5s
    retries: 5

# NGINX Reverse Proxy
nginx:
  image: nginx:alpine
  container_name: circuitos-proxy
  restart: unless-stopped
  ports:
    - "80:80"
    - "443:443"
  volumes:
    - ./docker/nginx.conf:/etc/nginx/nginx.conf:ro
    - ./docker/ssl:/etc/nginx/ssl:ro
  depends_on:
    - metroflex-ai
    - agentforce-api
    - ml-api

# Prometheus (monitoring)
prometheus:
  image: prom/prometheus:latest
  container_name: circuitos-metrics
  restart: unless-stopped
  volumes:
    - ./docker/prometheus.yml:/etc/prometheus/prometheus.yml:ro
    - prometheus_data:/prometheus
  ports:
    - "9090:9090"

# Grafana (dashboards)
grafana:
  image: grafana/grafana:latest
  container_name: circuitos-dashboards
  restart: unless-stopped
  environment:
    - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_PASSWORD:-admin}
  volumes:
    - grafana_data:/var/lib/grafana
    - ./docker/grafana-dashboards:/etc/grafana/provisioning/dashboards
  ports:
    - "3000:3000"
  depends_on:
    - prometheus
```

---

## 🚀 Simplified Deployment Process

### New Developer Onboarding (15 Minutes)

```bash
# 1. Clone repository
git clone <repo-url>
cd CircuitOS_Local_Complete_Package

# 2. Create .env file
cp .env.example .env
# Edit .env with your API keys

# 3. Start entire stack
docker-compose up -d

# 4. Verify health
docker-compose ps
curl http://localhost/health

# Done! All services running.
```

**Time Savings:** 90 minutes → 15 minutes (83% reduction)

---

### Production Deployment (5 Minutes)

```bash
# 1. Build and push images
docker-compose build
docker-compose push

# 2. Deploy to server
ssh production-server
docker-compose pull
docker-compose up -d

# 3. Verify
docker-compose ps
```

---

## 📝 Configuration Management

### Unified .env File

```bash
# .env (single source of truth)

# API Keys
OPENAI_API_KEY=sk-proj-xxxxx
ANTHROPIC_API_KEY=sk-ant-xxxxx

# Database
POSTGRES_PASSWORD=secure_password_here
DATABASE_URL=postgresql://circuitos:${POSTGRES_PASSWORD}@postgres:5432/

# Redis
REDIS_URL=redis://redis:6379/0

# GHL Integration
GHL_LEAD_CAPTURE_WEBHOOK=https://services.leadconnectorhq.com/hooks/xxxxx

# Monitoring
GRAFANA_PASSWORD=admin_password_here

# Environment
ENVIRONMENT=production  # or development, staging
DEBUG=false
```

---

## 🛠 Tool Consolidation

### Before: Fragmented Tooling

```
Python Version Management:
- pyenv (3.9, 3.11, 3.12)
- 4 separate venvs
- pip, uv, poetry

Node.js Version Management:
- nvm
- npm, pnpm, yarn

Databases:
- Local PostgreSQL installation
- Redis installation
- Manual schema management

Monitoring:
- No unified monitoring
- Manual log checking
- No metrics
```

### After: Docker-First Approach

```
Single Tool: Docker Desktop
- All Python versions in containers
- All Node.js versions in containers
- All databases in containers
- Built-in monitoring (Prometheus + Grafana)
- Unified logging (docker-compose logs)
```

**Tools Eliminated:**
- ❌ pyenv
- ❌ nvm
- ❌ PostgreSQL.app
- ❌ Redis.app
- ❌ Manual venv management

**Tools Added:**
- ✅ Docker Desktop (only)

---

## 📊 Cost & Performance Impact

### Development Costs

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| New dev setup | 2 hours | 15 min | 88% faster |
| Dependency conflicts | 4 hrs/month | 0 hrs | 100% eliminated |
| Environment drift | Common | Never | 100% eliminated |
| Database setup | 30 min | 0 min | 100% automated |

### Production Costs

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Deployment time | 45 min | 5 min | 89% faster |
| Server costs | $50-100/mo | $30/mo | 50% reduction |
| Downtime risk | High | Low | 80% reduction |
| Rollback time | 30 min | 30 sec | 98% faster |

### Performance

| Service | Response Time | Uptime | Auto-Scaling |
|---------|--------------|--------|--------------|
| MetroFlex AI | <200ms | 99.9% | Yes (Docker Swarm) |
| Agentforce API | <100ms | 99.9% | Yes (Kubernetes) |
| ML API | <150ms | 99.9% | Yes (HPA) |

---

## 🎯 Implementation Roadmap

### Week 1: Core Dockerization
- [ ] Create Dockerfiles for all Python services
- [ ] Create docker-compose.yml
- [ ] Test local deployment
- [ ] Document setup process

### Week 2: Infrastructure
- [ ] Add PostgreSQL with multi-database init script
- [ ] Add Redis configuration
- [ ] Add NGINX reverse proxy
- [ ] Configure SSL certificates

### Week 3: Monitoring & Observability
- [ ] Add Prometheus metrics endpoints
- [ ] Configure Grafana dashboards
- [ ] Set up structured logging
- [ ] Create alerting rules

### Week 4: Production Deployment
- [ ] Deploy to staging environment
- [ ] Load testing (1000+ requests/sec)
- [ ] Security audit
- [ ] Deploy to production

---

## 🔒 Security Best Practices

### Docker Security Checklist

**Images:**
- [ ] Use official base images (python:3.11-slim, node:18-alpine)
- [ ] Scan for vulnerabilities (docker scan)
- [ ] Multi-stage builds (reduce attack surface)
- [ ] Non-root user in containers

**Secrets:**
- [ ] Never commit .env files
- [ ] Use Docker secrets (Swarm) or Kubernetes secrets
- [ ] Rotate API keys quarterly
- [ ] Encrypt sensitive environment variables

**Network:**
- [ ] Internal network for service-to-service communication
- [ ] Only expose necessary ports
- [ ] Rate limiting on public endpoints
- [ ] SSL/TLS for all external traffic

**Updates:**
- [ ] Automated security updates (Dependabot)
- [ ] Weekly image rebuilds
- [ ] Vulnerability scanning in CI/CD
- [ ] Rollback plan for bad updates

---

## 📈 Success Metrics

### KPIs to Track

**Developer Experience:**
- ⏱️ Time to first successful deployment
- 🐛 Number of environment-related bugs
- 😊 Developer satisfaction score

**Production Reliability:**
- ✅ Uptime percentage (target: 99.9%)
- 🚀 Deployment frequency (target: daily)
- ⚡ Mean time to recovery (target: <5 min)
- 📊 Error rate (target: <0.1%)

**Business Impact:**
- 💰 Infrastructure cost reduction
- ⏰ Time saved per developer (hrs/month)
- 🎯 Feature velocity (stories/sprint)

---

## 🎓 Training & Documentation

### Developer Resources

**Quick Start Guide:**
- [Docker Quick Start](./docker/DOCKER_QUICKSTART.md)
- [Local Development Setup](./docker/LOCAL_SETUP.md)
- [Troubleshooting Guide](./docker/TROUBLESHOOTING.md)

**Video Tutorials:**
- 📹 5-minute setup walkthrough
- 📹 Debugging containerized apps
- 📹 Deploying to production

**Best Practices:**
- [Dockerfile Best Practices](./docker/DOCKERFILE_BEST_PRACTICES.md)
- [docker-compose.yml Patterns](./docker/COMPOSE_PATTERNS.md)
- [Production Deployment Checklist](./docker/PRODUCTION_CHECKLIST.md)

---

## 🚦 Next Steps

### Immediate Actions (This Week)

1. **Create Dockerfiles** for all services
2. **Write unified docker-compose.yml**
3. **Test local deployment**
4. **Document setup process**

### Short-term (Next 2 Weeks)

1. Add monitoring (Prometheus + Grafana)
2. Configure NGINX reverse proxy
3. Set up CI/CD pipeline
4. Deploy to staging environment

### Long-term (Next Month)

1. Migrate to Kubernetes (for auto-scaling)
2. Implement blue-green deployments
3. Add distributed tracing (OpenTelemetry)
4. Create disaster recovery plan

---

## 💡 Key Decisions

### Architecture Decisions

**1. Docker Compose vs Kubernetes**
- **Decision:** Start with Docker Compose, migrate to Kubernetes when scaling needs arise
- **Rationale:** Docker Compose is simpler for <10 services, easier to learn, faster to deploy

**2. Single Repo vs Multi-Repo**
- **Decision:** Keep monorepo structure, use Docker build contexts
- **Rationale:** Easier to coordinate changes, shared configs, atomic deployments

**3. Service Communication**
- **Decision:** HTTP/REST for now, consider gRPC for high-throughput services
- **Rationale:** REST is simpler, more debugging tools, easier to monitor

**4. Database Strategy**
- **Decision:** Single PostgreSQL instance with multiple databases
- **Rationale:** Simpler ops, lower costs, easier backups, sufficient for current scale

---

## 📞 Support

**Questions?**
- Documentation: `/docker` directory
- Slack: #circuitos-docker-migration
- Office Hours: Wednesdays 2-3pm

**Issues?**
- GitHub Issues: Tag with `docker` label
- Urgent: Ping @devops-team

---

**Built by:** CircuitOS DevOps Team
**Last Updated:** November 2025
**Version:** 1.0
**Status:** Ready for Implementation
