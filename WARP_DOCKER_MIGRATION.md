# WARP Protocol: Docker Migration Session

**Session ID:** DOCKER-MIGRATION-001
**Date:** November 15, 2025
**Objective:** Complete CircuitOS Docker containerization in 4 hours
**Status:** ACTIVE

---

## 🎯 Mission Brief

**Goal:** Transform CircuitOS from fragmented manual setup → unified Docker stack

**Success Criteria:**
- ✅ All 6 services containerized
- ✅ docker-compose.yml fully functional
- ✅ Local testing successful (all health checks pass)
- ✅ Documentation complete
- ✅ Ready for production deployment

**Time Budget:** 4 hours (Warp speed)

---

## 📋 Warp Protocol Phases

### Phase 1: Foundation (45 min)
**Objective:** Create all Dockerfiles

**Tasks:**
1. [ ] MetroFlex AI Agent Dockerfile
2. [ ] ML API Server Dockerfile
3. [ ] Agentforce API Dockerfile
4. [ ] Agentforce Web Dockerfile
5. [ ] Virtual Agentforce Dockerfile
6. [ ] Circuit Script Runtime Dockerfile

**Warp Technique:** Parallel file creation, copy-paste optimization

---

### Phase 2: Infrastructure (30 min)
**Objective:** Set up supporting configs

**Tasks:**
1. [ ] NGINX configuration (nginx.conf)
2. [ ] PostgreSQL init script
3. [ ] Prometheus config
4. [ ] Grafana datasources
5. [ ] Loki config
6. [ ] Promtail config

**Warp Technique:** Use templates, minimal customization

---

### Phase 3: Testing (60 min)
**Objective:** Verify everything works

**Tasks:**
1. [ ] Build all images
2. [ ] Start stack (docker-compose up)
3. [ ] Health check all services
4. [ ] Integration tests
5. [ ] Fix any issues

**Warp Technique:** Automated testing scripts

---

### Phase 4: Documentation (45 min)
**Objective:** Make it reproducible

**Tasks:**
1. [ ] Update README files
2. [ ] Create troubleshooting guide
3. [ ] Record demo video
4. [ ] Write handoff docs

**Warp Technique:** AI-assisted documentation

---

## 🚀 Warp Commands

### Quick Start Sequence

```bash
# Phase 1: Create all Dockerfiles (Warp Mode)
./warp/create-dockerfiles.sh

# Phase 2: Generate configs (Warp Mode)
./warp/generate-configs.sh

# Phase 3: Test stack (Warp Mode)
./warp/test-stack.sh

# Phase 4: Generate docs (Warp Mode)
./warp/generate-docs.sh
```

---

## 📦 File Creation Matrix

| File | Location | Template | Status |
|------|----------|----------|--------|
| **Dockerfile** | Active/metroflex-ghl-website/AI_Agent/ | Python Flask | [ ] |
| **Dockerfile** | ../CircuitOS-Project/ | Python ML | [ ] |
| **Dockerfile.api** | Active/agentforce_emulator/ | Python FastAPI | [ ] |
| **Dockerfile.web** | Active/agentforce_emulator/ | Node React | [ ] |
| **Dockerfile** | Active/virtual-agentforce/ | Python | [ ] |
| **Dockerfile** | Active/circuit-script-runtime/ | Node.js | [ ] |
| **nginx.conf** | docker/ | NGINX template | [ ] |
| **postgres-init.sh** | docker/ | Bash script | [ ] |
| **prometheus.yml** | docker/ | YAML config | [ ] |
| **grafana-datasources.yml** | docker/ | YAML config | [ ] |
| **loki-config.yml** | docker/ | YAML config | [ ] |
| **promtail-config.yml** | docker/ | YAML config | [ ] |

---

## 🎬 Execution Plan

### Warp Phase 1: Dockerfiles (NOW)

**Let's create all 6 Dockerfiles in parallel:**

#### 1.1 MetroFlex AI Agent
**Location:** `Active/metroflex-ghl-website/AI_Agent/Dockerfile`
**Base:** Python 3.11-slim
**Dependencies:** Flask, OpenAI, ChromaDB, SentenceTransformers

#### 1.2 ML API Server
**Location:** `../CircuitOS-Project/Dockerfile`
**Base:** Python 3.11-slim
**Dependencies:** scikit-learn, Flask, Gunicorn

#### 1.3 Agentforce API
**Location:** `Active/agentforce_emulator/Dockerfile.api`
**Base:** Python 3.12-slim
**Dependencies:** FastAPI, LangGraph, SQLAlchemy

#### 1.4 Agentforce Web
**Location:** `Active/agentforce_emulator/Dockerfile.web`
**Base:** Node 18-alpine
**Dependencies:** Vite, React

#### 1.5 Virtual Agentforce
**Location:** `Active/virtual-agentforce/Dockerfile`
**Base:** Python 3.11-slim
**Dependencies:** TBD (check requirements.txt)

#### 1.6 Circuit Script Runtime
**Location:** `Active/circuit-script-runtime/Dockerfile`
**Base:** Node 18-alpine
**Dependencies:** TypeScript, Express

---

## 🤖 Warp Automation Scripts

### Script 1: Create All Dockerfiles

```bash
#!/bin/bash
# warp/create-dockerfiles.sh

echo "🚀 WARP: Creating all Dockerfiles..."

# 1. MetroFlex AI
cat > Active/metroflex-ghl-website/AI_Agent/Dockerfile <<'EOF'
FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y gcc g++ curl && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY *.py .
COPY *.json .
EXPOSE 5001
HEALTHCHECK CMD curl -f http://localhost:5001/health || exit 1
CMD ["gunicorn", "--bind", "0.0.0.0:5001", "--workers", "2", "app:app"]
EOF

# 2. ML API
cat > ../CircuitOS-Project/Dockerfile <<'EOF'
FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y gcc g++ curl && rm -rf /var/lib/apt/lists/*
COPY requirements-production.txt .
RUN pip install --no-cache-dir -r requirements-production.txt
COPY *.py .
COPY trained_models/ ./trained_models/
EXPOSE 5000
HEALTHCHECK CMD curl -f http://localhost:5000/health || exit 1
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "3", "api_server:app"]
EOF

# 3. Agentforce API
cat > Active/agentforce_emulator/Dockerfile.api <<'EOF'
FROM python:3.12-slim
WORKDIR /app
RUN apt-get update && apt-get install -y gcc g++ postgresql-client curl && rm -rf /var/lib/apt/lists/*
RUN pip install uv
COPY pyproject.toml .
RUN uv pip install --system .
COPY services/ ./services/
COPY cli/ ./cli/
COPY configs/ ./configs/
EXPOSE 8000
HEALTHCHECK CMD curl -f http://localhost:8000/health || exit 1
CMD ["uvicorn", "services.agent_runtime.app:app", "--host", "0.0.0.0", "--port", "8000"]
EOF

# 4. Agentforce Web
cat > Active/agentforce_emulator/Dockerfile.web <<'EOF'
FROM node:18-alpine
WORKDIR /app
COPY apps/control_panel/package*.json ./
RUN npm ci
COPY apps/control_panel/ .
RUN npm run build
EXPOSE 3001
HEALTHCHECK CMD wget --quiet --tries=1 --spider http://localhost:3001 || exit 1
CMD ["npm", "run", "preview", "--", "--host", "0.0.0.0", "--port", "3001"]
EOF

# 5. Virtual Agentforce
cat > Active/virtual-agentforce/Dockerfile <<'EOF'
FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y gcc g++ curl && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY virtual_agentforce/ ./virtual_agentforce/
EXPOSE 8001
HEALTHCHECK CMD curl -f http://localhost:8001/health || exit 1
CMD ["python", "-m", "virtual_agentforce.main"]
EOF

# 6. Circuit Script Runtime
cat > Active/circuit-script-runtime/Dockerfile <<'EOF'
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build
EXPOSE 3000
HEALTHCHECK CMD wget --quiet --tries=1 --spider http://localhost:3000/health || exit 1
CMD ["npm", "start"]
EOF

echo "✅ All Dockerfiles created!"
```

### Script 2: Generate Infrastructure Configs

```bash
#!/bin/bash
# warp/generate-configs.sh

echo "🚀 WARP: Generating infrastructure configs..."

# Create docker directory
mkdir -p docker

# 1. NGINX Config
cat > docker/nginx.conf <<'EOF'
events {
    worker_connections 1024;
}

http {
    upstream metroflex {
        server metroflex-ai:5001;
    }
    upstream ml_api {
        server ml-api:5000;
    }
    upstream agentforce {
        server agentforce-api:8000;
    }

    server {
        listen 80;

        location /metroflex/ {
            proxy_pass http://metroflex/;
        }

        location /ml/ {
            proxy_pass http://ml_api/;
        }

        location /agentforce/ {
            proxy_pass http://agentforce/;
        }

        location /health {
            access_log off;
            return 200 "healthy\n";
        }
    }
}
EOF

# 2. PostgreSQL Init Script
cat > docker/postgres-init.sh <<'EOF'
#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    CREATE DATABASE agentforce;
    CREATE DATABASE ml_audit;
    CREATE DATABASE circuit_runtime;
    CREATE DATABASE virtual_agentforce;
EOSQL
EOF
chmod +x docker/postgres-init.sh

# 3. Prometheus Config
cat > docker/prometheus.yml <<'EOF'
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'metroflex-ai'
    static_configs:
      - targets: ['metroflex-ai:5001']

  - job_name: 'ml-api'
    static_configs:
      - targets: ['ml-api:5000']

  - job_name: 'agentforce-api'
    static_configs:
      - targets: ['agentforce-api:8000']
EOF

# 4. Grafana Datasources
cat > docker/grafana-datasources.yml <<'EOF'
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true

  - name: Loki
    type: loki
    access: proxy
    url: http://loki:3100
EOF

# 5. Loki Config
cat > docker/loki-config.yml <<'EOF'
auth_enabled: false

server:
  http_listen_port: 3100

ingester:
  lifecycler:
    address: 127.0.0.1
    ring:
      kvstore:
        store: inmemory
      replication_factor: 1

schema_config:
  configs:
    - from: 2020-10-24
      store: boltdb-shipper
      object_store: filesystem
      schema: v11
      index:
        prefix: index_
        period: 24h

storage_config:
  boltdb_shipper:
    active_index_directory: /loki/boltdb-shipper-active
    cache_location: /loki/boltdb-shipper-cache
  filesystem:
    directory: /loki/chunks
EOF

# 6. Promtail Config
cat > docker/promtail-config.yml <<'EOF'
server:
  http_listen_port: 9080

positions:
  filename: /tmp/positions.yaml

clients:
  - url: http://loki:3100/loki/api/v1/push

scrape_configs:
  - job_name: docker
    docker_sd_configs:
      - host: unix:///var/run/docker.sock
    relabel_configs:
      - source_labels: ['__meta_docker_container_name']
        regex: '/(.*)'
        target_label: 'container'
EOF

echo "✅ All configs generated!"
```

### Script 3: Test Stack

```bash
#!/bin/bash
# warp/test-stack.sh

echo "🚀 WARP: Testing Docker stack..."

# Build all images
echo "Building images..."
docker-compose build

# Start stack
echo "Starting stack..."
docker-compose up -d

# Wait for services to be healthy
echo "Waiting for services..."
sleep 30

# Test health endpoints
echo "Testing health endpoints..."
services=(
    "http://localhost:5001/health"
    "http://localhost:5000/health"
    "http://localhost:8000/health"
    "http://localhost/health"
)

for url in "${services[@]}"; do
    echo "Testing $url..."
    if curl -f -s "$url" > /dev/null; then
        echo "✅ $url is healthy"
    else
        echo "❌ $url failed"
        docker-compose logs
        exit 1
    fi
done

echo "✅ All tests passed!"
```

### Script 4: Generate Documentation

```bash
#!/bin/bash
# warp/generate-docs.sh

echo "🚀 WARP: Generating documentation..."

# Create README for docker directory
cat > docker/README.md <<'EOF'
# CircuitOS Docker Infrastructure

This directory contains all Docker infrastructure configurations.

## Files

- `nginx.conf` - NGINX reverse proxy configuration
- `postgres-init.sh` - PostgreSQL database initialization
- `prometheus.yml` - Prometheus metrics collection
- `grafana-datasources.yml` - Grafana data sources
- `loki-config.yml` - Loki log aggregation
- `promtail-config.yml` - Promtail log shipping

## Usage

All configs are automatically loaded by docker-compose.yml.
No manual configuration required.

## Customization

Edit these files to customize your infrastructure.
Restart services after changes:

```bash
docker-compose restart <service-name>
```
EOF

echo "✅ Documentation generated!"
```

---

## ⚡ Execute Warp Protocol

**Ready to execute? Run these commands in sequence:**

```bash
# Step 1: Create warp scripts directory
mkdir -p warp

# Step 2: Make scripts executable
chmod +x warp/*.sh

# Step 3: WARP SPEED - Execute all phases
./warp/create-dockerfiles.sh
./warp/generate-configs.sh
./warp/test-stack.sh
./warp/generate-docs.sh
```

**Total time:** 45 minutes (vs 8 hours manual)

---

## 🎯 Success Metrics

Track progress in real-time:

```bash
# Check what's created
find . -name "Dockerfile*" -o -name "*.yml" -o -name "*.sh" | grep -E "(Dockerfile|docker/)"

# Count completed tasks
grep -r "✅" WARP_DOCKER_MIGRATION.md | wc -l

# Test coverage
docker-compose config --services | wc -l  # Should be 16
```

---

## 🐛 Warp Debugging

**If something fails:**

```bash
# Quick diagnostics
docker-compose ps              # Check service status
docker-compose logs <service>  # View logs
docker system df              # Check disk space

# Quick fixes
docker-compose down -v         # Reset everything
docker system prune -a         # Clean Docker
./warp/create-dockerfiles.sh   # Re-create files
```

---

## 📊 Warp Protocol Status

### Phase 1: Dockerfiles
- [ ] MetroFlex AI (5 min)
- [ ] ML API (5 min)
- [ ] Agentforce API (5 min)
- [ ] Agentforce Web (5 min)
- [ ] Virtual Agentforce (5 min)
- [ ] Circuit Script (5 min)

**Total:** 30 min (parallel execution: 10 min actual)

### Phase 2: Infrastructure
- [ ] NGINX (5 min)
- [ ] PostgreSQL init (5 min)
- [ ] Prometheus (5 min)
- [ ] Grafana (5 min)
- [ ] Loki (5 min)
- [ ] Promtail (5 min)

**Total:** 30 min (parallel execution: 10 min actual)

### Phase 3: Testing
- [ ] Build images (15 min)
- [ ] Start stack (5 min)
- [ ] Health checks (5 min)
- [ ] Integration tests (10 min)
- [ ] Fix issues (25 min buffer)

**Total:** 60 min

### Phase 4: Documentation
- [ ] Update READMEs (15 min)
- [ ] Troubleshooting guide (15 min)
- [ ] Demo recording (10 min)
- [ ] Handoff docs (5 min)

**Total:** 45 min

**Grand Total:** 2 hours 25 minutes (vs 8 hours manual)

---

## 🎓 Warp Protocol Principles

**1. Parallel Execution**
- Create all Dockerfiles simultaneously
- Use templates, not custom code
- Automate everything

**2. Fail Fast**
- Test immediately after creation
- Automated health checks
- Quick rollback

**3. Documentation as Code**
- Auto-generate from templates
- Keep in sync with configs
- Version control everything

**4. Measure Everything**
- Track time per phase
- Count completed tasks
- Monitor success rate

---

## 🚀 Ready to Launch?

**Execute Warp Protocol NOW:**

```bash
# One command to rule them all
cd /Users/noelpena/Desktop/CircuitOS_Local_Complete_Package
./warp/create-dockerfiles.sh && \
./warp/generate-configs.sh && \
./warp/test-stack.sh && \
./warp/generate-docs.sh

# Expected result: Fully functional Docker stack in < 3 hours
```

---

**Session Started:** November 15, 2025
**Expected Completion:** November 15, 2025 (same day!)
**Warp Factor:** 8/10 (Near light speed)

**ENGAGE! 🚀**
