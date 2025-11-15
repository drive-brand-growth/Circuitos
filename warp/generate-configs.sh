#!/bin/bash
# WARP Protocol: Generate Infrastructure Configs
# Execution time: ~5 minutes
# Purpose: Generate production-ready configs for nginx, postgres, prometheus, grafana, loki, promtail

set -e  # Exit on error

echo "🚀 WARP PROTOCOL: Generating infrastructure configs..."
echo "================================================"

BASE_DIR="/Users/noelpena/Desktop/CircuitOS_Local_Complete_Package"
cd "$BASE_DIR"

# Create docker directory
mkdir -p docker

# 1. NGINX Config
echo "📦 [1/6] Creating NGINX configuration..."
cat > docker/nginx.conf <<'EOF'
events {
    worker_connections 1024;
}

http {
    upstream metroflex_events {
        server metroflex-events-agent:5001;
    }

    upstream metroflex_gym {
        server metroflex-gym-agent:5002;
    }

    upstream ml_api {
        server ml-api:5000;
    }

    upstream agentforce {
        server agentforce-api:8000;
    }

    server {
        listen 80;

        # Events API
        location /api/events/ {
            proxy_pass http://metroflex_events/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }

        # Gym API
        location /api/gym/ {
            proxy_pass http://metroflex_gym/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }

        # ML API
        location /ml/ {
            proxy_pass http://ml_api/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }

        # Agentforce
        location /agentforce/ {
            proxy_pass http://agentforce/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }

        # Health check
        location /health {
            access_log off;
            return 200 "healthy\n";
            add_header Content-Type text/plain;
        }
    }
}
EOF
echo "✅ NGINX config created"

# 2. PostgreSQL Init Script
echo "📦 [2/6] Creating PostgreSQL init script..."
cat > docker/postgres-init.sh <<'EOF'
#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    CREATE DATABASE agentforce;
    CREATE DATABASE ml_audit;
    CREATE DATABASE circuit_runtime;
    CREATE DATABASE metroflex_events;
    CREATE DATABASE metroflex_gym;

    GRANT ALL PRIVILEGES ON DATABASE agentforce TO $POSTGRES_USER;
    GRANT ALL PRIVILEGES ON DATABASE ml_audit TO $POSTGRES_USER;
    GRANT ALL PRIVILEGES ON DATABASE circuit_runtime TO $POSTGRES_USER;
    GRANT ALL PRIVILEGES ON DATABASE metroflex_events TO $POSTGRES_USER;
    GRANT ALL PRIVILEGES ON DATABASE metroflex_gym TO $POSTGRES_USER;
EOSQL

echo "✅ Databases created: agentforce, ml_audit, circuit_runtime, metroflex_events, metroflex_gym"
EOF
chmod +x docker/postgres-init.sh
echo "✅ PostgreSQL init script created"

# 3. Prometheus Config
echo "📦 [3/6] Creating Prometheus configuration..."
cat > docker/prometheus.yml <<'EOF'
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'metroflex-events-agent'
    static_configs:
      - targets: ['metroflex-events-agent:5001']

  - job_name: 'metroflex-gym-agent'
    static_configs:
      - targets: ['metroflex-gym-agent:5002']

  - job_name: 'ml-api'
    static_configs:
      - targets: ['ml-api:5000']

  - job_name: 'agentforce-api'
    static_configs:
      - targets: ['agentforce-api:8000']

  - job_name: 'postgres'
    static_configs:
      - targets: ['postgres:5432']

  - job_name: 'redis'
    static_configs:
      - targets: ['redis:6379']
EOF
echo "✅ Prometheus config created"

# 4. Grafana Datasources
echo "📦 [4/6] Creating Grafana datasources..."
cat > docker/grafana-datasources.yml <<'EOF'
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
    editable: true

  - name: Loki
    type: loki
    access: proxy
    url: http://loki:3100
    editable: true
EOF
echo "✅ Grafana datasources created"

# 5. Loki Config
echo "📦 [5/6] Creating Loki configuration..."
cat > docker/loki-config.yml <<'EOF'
auth_enabled: false

server:
  http_listen_port: 3100
  grpc_listen_port: 9096

common:
  path_prefix: /tmp/loki
  storage:
    filesystem:
      chunks_directory: /tmp/loki/chunks
      rules_directory: /tmp/loki/rules
  replication_factor: 1
  ring:
    instance_addr: 127.0.0.1
    kvstore:
      store: inmemory

schema_config:
  configs:
    - from: 2020-10-24
      store: boltdb-shipper
      object_store: filesystem
      schema: v11
      index:
        prefix: index_
        period: 24h

ruler:
  alertmanager_url: http://localhost:9093
EOF
echo "✅ Loki config created"

# 6. Promtail Config
echo "📦 [6/6] Creating Promtail configuration..."
cat > docker/promtail-config.yml <<'EOF'
server:
  http_listen_port: 9080
  grpc_listen_port: 0

positions:
  filename: /tmp/positions.yaml

clients:
  - url: http://loki:3100/loki/api/v1/push

scrape_configs:
  - job_name: docker
    docker_sd_configs:
      - host: unix:///var/run/docker.sock
        refresh_interval: 5s
    relabel_configs:
      - source_labels: ['__meta_docker_container_name']
        regex: '/(.*)'
        target_label: 'container'
      - source_labels: ['__meta_docker_container_log_stream']
        target_label: 'logstream'
      - source_labels: ['__meta_docker_container_label_logging_jobname']
        target_label: 'job'
EOF
echo "✅ Promtail config created"

echo ""
echo "================================================"
echo "✅ WARP COMPLETE: All infrastructure configs created!"
echo "================================================"
echo ""
echo "Created files:"
echo "  1. docker/nginx.conf"
echo "  2. docker/postgres-init.sh"
echo "  3. docker/prometheus.yml"
echo "  4. docker/grafana-datasources.yml"
echo "  5. docker/loki-config.yml"
echo "  6. docker/promtail-config.yml"
echo ""
echo "Next step: Create .env file and start Docker stack"
echo "  cp .env.example .env"
echo "  nano .env  # Add your OPENAI_API_KEY"
echo "  docker-compose up -d"
