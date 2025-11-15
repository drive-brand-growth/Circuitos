# DOCKER SETUP GUIDE - METROFLEX EVENTS AI AGENT

## 🐳 Why Docker is Better for Your Use Case

### **Your Specific Advantages:**

| Feature | n8n Cloud | Docker Self-Hosted | Winner |
|---------|-----------|-------------------|--------|
| **Cost** | $20/mo | $12/mo (DigitalOcean) | ✅ Docker (40% cheaper) |
| **RAG Capabilities** | ❌ None | ✅ Qdrant vector DB | ✅ Docker |
| **Agent Organization** | Limited | ✅ Multiple containers | ✅ Docker |
| **File Management** | Basic | ✅ MinIO + shared volumes | ✅ Docker |
| **Audio Training Access** | Upload only | ✅ Direct mount | ✅ Docker |
| **Custom Code** | Limited | ✅ Full control | ✅ Docker |
| **Local Development** | ❌ Cloud only | ✅ Run locally | ✅ Docker |
| **Maintenance** | Zero | Some required | n8n Cloud |

**Verdict:** Docker is better for your complex, multi-agent setup with RAG and file management needs.

---

## 🏗️ WHAT YOU GET WITH THIS DOCKER SETUP

### **1. n8n (Workflow Automation)**
- Self-hosted n8n server
- PostgreSQL database (persistent storage)
- Same workflows as n8n Cloud
- Unlimited executions
- Save $96/year

### **2. Qdrant (Vector Database for RAG)**
- Store athlete profiles as vectors
- Semantic search ("find competitors similar to John Doe")
- Memory for AI agents
- Knowledge base for training data

### **3. Redis (Caching & Queues)**
- Cache frequently accessed data
- Queue management for background jobs
- Session storage
- Real-time data

### **4. MinIO (File Storage)**
- S3-compatible object storage
- Store audio training files (50+ MB)
- Organize documents, images, videos
- Accessible from all containers

### **5. AI Agent API (Custom Python Service)**
- FastAPI server for custom agents
- RAG integration (search athletes with context)
- Claude API wrapper
- Competitive intelligence endpoints

### **6. Nginx (Reverse Proxy)**
- SSL/HTTPS support
- Domain routing
- Load balancing
- Security layer

### **7. Portainer (Docker Management UI)**
- Visual dashboard for Docker
- Start/stop containers easily
- View logs
- Monitor resource usage

---

## 📁 PROJECT STRUCTURE

```
/home/user/Circuitos/
├── docker-compose.yml          # Main Docker configuration
├── .env                        # Environment variables (create from .env.example)
├── .env.example               # Template for environment variables
│
├── ai-agent-api/              # Custom AI Agent API
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── main.py                # FastAPI application with RAG
│   └── ...
│
├── nginx/                     # Nginx configuration
│   ├── conf.d/
│   │   └── default.conf
│   ├── ssl/                   # SSL certificates
│   └── logs/                  # Access logs
│
├── shared-files/              # Shared between containers
│   ├── athlete-data/
│   ├── event-documents/
│   └── exports/
│
├── audio-training/            # Your existing audio training files
│   ├── (read-only mount)
│   └── ...
│
└── qdrant-config/            # Qdrant configuration
    └── config.yaml
```

---

## 🚀 INSTALLATION GUIDE

### **Option 1: Local Development (Your MacBook/PC)**

**Step 1: Install Prerequisites**
```bash
# Install Docker Desktop
# Mac: https://docs.docker.com/desktop/install/mac-install/
# Windows: https://docs.docker.com/desktop/install/windows-install/
# Linux: https://docs.docker.com/engine/install/ubuntu/

# Verify installation
docker --version
docker-compose --version
```

**Step 2: Configure Environment**
```bash
cd /home/user/Circuitos

# Copy environment template
cp .env.example .env

# Edit .env file (add your API keys)
nano .env
# OR
code .env  # if using VS Code
```

**Step 3: Start Services**
```bash
# Start all containers
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

**Step 4: Access Services**
```
n8n:           http://localhost:5678
Qdrant:        http://localhost:6333/dashboard
Portainer:     http://localhost:9000
AI Agent API:  http://localhost:8080
MinIO:         http://localhost:9001
```

---

### **Option 2: Production Deployment (DigitalOcean/AWS/GCP)**

**Step 1: Create Server**

**DigitalOcean (Recommended):**
```bash
# Create a Droplet
# - Size: Basic ($12/mo, 2 GB RAM, 1 vCPU, 50 GB SSD)
# - Image: Docker on Ubuntu 22.04
# - Datacenter: Choose closest to Texas (New York 1)
# - Add SSH key

# OR use CLI:
doctl compute droplet create metroflex-ai \
  --image docker-20-04 \
  --size s-2vcpu-2gb \
  --region nyc1 \
  --ssh-keys YOUR_SSH_KEY_ID
```

**Step 2: Connect to Server**
```bash
ssh root@YOUR_SERVER_IP
```

**Step 3: Clone Your Repository**
```bash
# Install git if not installed
apt-get update && apt-get install -y git

# Clone your repo
git clone https://github.com/your-username/Circuitos.git
cd Circuitos
```

**Step 4: Configure Environment**
```bash
# Copy .env template
cp .env.example .env

# Edit with your production values
nano .env

# Generate secure passwords
openssl rand -hex 32  # Use for encryption keys
```

**Step 5: Set Up Domain (Optional but Recommended)**
```bash
# Point your domain to server IP
# Example: ai.metroflexevents.com → YOUR_SERVER_IP

# Update .env
N8N_HOST=ai.metroflexevents.com
```

**Step 6: Start Services**
```bash
# Start all containers
docker-compose up -d

# Check everything is running
docker-compose ps

# View logs
docker-compose logs -f n8n
```

**Step 7: Set Up SSL (Let's Encrypt)**
```bash
# Install Certbot
apt-get install -y certbot python3-certbot-nginx

# Get SSL certificate
certbot --nginx -d ai.metroflexevents.com

# Auto-renewal (already set up)
# Test with: certbot renew --dry-run
```

---

## 🔧 CONFIGURATION DETAILS

### **.env File Explained**

```bash
# n8n Authentication
N8N_USER=admin                     # Your admin username
N8N_PASSWORD=secure_password_123   # Strong password!
N8N_HOST=ai.metroflexevents.com   # Your domain (or localhost)

# Encryption Key (32+ characters)
N8N_ENCRYPTION_KEY=your_random_32_char_string_here_xyz123

# Database
POSTGRES_DB=n8n
POSTGRES_USER=n8n
POSTGRES_PASSWORD=another_secure_password

# API Keys
CLAUDE_API_KEY=sk-ant-your-key-here
GHL_WEBHOOK_URL=https://services.leadconnectorhq.com/hooks/...

# File Storage
MINIO_ROOT_USER=minioadmin
MINIO_ROOT_PASSWORD=minio_secure_password

# Timezone
TIMEZONE=America/Chicago
```

**Generate Secure Keys:**
```bash
# Linux/Mac
openssl rand -hex 32

# OR Python
python3 -c "import secrets; print(secrets.token_hex(32))"

# OR Node.js
node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"
```

---

## 📊 HOW RAG WORKS IN YOUR SETUP

### **Data Flow:**

```
┌─────────────────────────────────────────────────┐
│ 1. INGESTION                                    │
├─────────────────────────────────────────────────┤
│ Apify scrapes Instagram → sends to n8n         │
│ n8n processes athlete profile                   │
│ n8n calls AI Agent API: POST /athletes/add     │
│ AI Agent API creates embedding (vector)        │
│ Vector stored in Qdrant database               │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│ 2. RETRIEVAL                                    │
├─────────────────────────────────────────────────┤
│ Query: "Find experienced Men's Physique        │
│         competitors in Dallas"                  │
│ AI Agent API: POST /athletes/search            │
│ Convert query to embedding vector              │
│ Qdrant finds most similar vectors (cosine)     │
│ Returns top 5 matching athlete profiles        │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│ 3. AUGMENTED GENERATION                        │
├─────────────────────────────────────────────────┤
│ Retrieved athletes sent to Claude API          │
│ Claude analyzes: "These 5 athletes are ideal   │
│   for your event because..."                    │
│ Personalized outreach generated                │
│ Sent to GHL for campaign                       │
└─────────────────────────────────────────────────┘
```

### **Example RAG Query:**

**Via API:**
```bash
curl -X POST http://localhost:8080/athletes/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Find competitors who recently placed top 3 in Texas shows",
    "limit": 5,
    "use_claude": true
  }'
```

**Response:**
```json
{
  "query": "Find competitors who recently placed top 3 in Texas shows",
  "results_count": 5,
  "athletes": [
    {
      "score": 0.89,
      "athlete": {
        "username": "johnsmith_npc",
        "display_name": "John Smith",
        "bio": "3rd Place Texas Shredder Classic 2024 | Men's Physique",
        "division": "Men's Physique",
        "location": "Dallas, TX"
      }
    },
    ...
  ],
  "claude_analysis": "These athletes are prime targets because they've demonstrated recent competitive success in Texas. John Smith's 3rd place finish shows he's actively competing and likely hungry to improve..."
}
```

---

## 🎯 INTEGRATING RAG WITH N8N WORKFLOW

### **Enhanced n8n Workflow with RAG:**

**New Node: "Check RAG for Similar Athletes"**

```json
{
  "name": "Check RAG for Similar Athletes",
  "type": "HTTP Request",
  "position": [1300, 300],
  "parameters": {
    "method": "POST",
    "url": "http://ai-agent-api:8080/athletes/search",
    "jsonBody": {
      "query": "={{ 'Find athletes similar to ' + $json.displayName + ' who compete in ' + $json.division }}",
      "limit": 3,
      "use_claude": false
    }
  }
}
```

**Use Cases:**

1. **Deduplication:** "Is this athlete already in our database?"
2. **Similar Athletes:** "Find 3 similar athletes to this one"
3. **Competitive Intelligence:** "Who from our database competed at [Competitor Show]?"
4. **Personalization:** "What do we know about this athlete's history?"

---

## 💾 FILE MANAGEMENT WITH MINIO

### **Why MinIO?**

- S3-compatible (use AWS SDK)
- Store large files (audio training: 50+ MB)
- Organize by buckets (events, athletes, audio, documents)
- Access from any container
- Built-in versioning and backup

### **Setup MinIO Buckets:**

**Via MinIO Console:**
```
1. Go to: http://localhost:9001
2. Login: minioadmin / your_minio_password
3. Click "Buckets" → "Create Bucket"
4. Create buckets:
   - metroflex-audio-training
   - metroflex-athlete-photos
   - metroflex-event-documents
   - metroflex-backups
```

**Via n8n (Automated):**

Add this node to your workflow to upload files:

```json
{
  "name": "Upload to MinIO",
  "type": "HTTP Request",
  "parameters": {
    "method": "PUT",
    "url": "http://minio:9002/metroflex-athletes/{{ $json.username }}.json",
    "authentication": "genericCredentialType",
    "genericAuthType": "httpBasicAuth",
    "sendBody": true,
    "bodyContentType": "json",
    "jsonBody": "={{ JSON.stringify($json) }}"
  }
}
```

### **Mount Your Audio Training Files:**

In `docker-compose.yml`, already configured:

```yaml
volumes:
  - ./audio-training:/audio-training:ro  # Read-only access
```

**Access from AI Agent API:**
```python
import os

# List audio files
audio_files = os.listdir("/audio-training")

# Load specific file
with open("/audio-training/module-01.mp3", "rb") as f:
    audio_data = f.read()
```

---

## 🔍 MONITORING & LOGGING

### **View Logs:**

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f n8n
docker-compose logs -f ai-agent-api
docker-compose logs -f qdrant

# Last 100 lines
docker-compose logs --tail=100 n8n
```

### **Portainer Dashboard:**

```
1. Go to: http://localhost:9000
2. Create admin account (first time)
3. Select "Local" Docker environment
4. View all containers, logs, stats
```

### **Resource Monitoring:**

```bash
# Resource usage
docker stats

# Specific container
docker stats metroflex-n8n
```

---

## 🛠️ COMMON OPERATIONS

### **Start/Stop Services:**

```bash
# Start all
docker-compose up -d

# Stop all
docker-compose down

# Restart specific service
docker-compose restart n8n

# Rebuild after code changes
docker-compose up -d --build ai-agent-api
```

### **Backup Data:**

```bash
# Backup volumes
docker run --rm \
  -v metroflex_postgres_data:/data \
  -v $(pwd)/backups:/backup \
  alpine tar czf /backup/postgres-$(date +%Y%m%d).tar.gz /data

# Backup Qdrant
docker run --rm \
  -v metroflex_qdrant_data:/data \
  -v $(pwd)/backups:/backup \
  alpine tar czf /backup/qdrant-$(date +%Y%m%d).tar.gz /data
```

### **Restore Data:**

```bash
# Restore PostgreSQL
docker-compose down
docker run --rm \
  -v metroflex_postgres_data:/data \
  -v $(pwd)/backups:/backup \
  alpine sh -c "cd /data && tar xzf /backup/postgres-20250115.tar.gz --strip 1"
docker-compose up -d
```

---

## 💰 COST COMPARISON

### **n8n Cloud vs Docker Self-Hosted (12 Months):**

| Service | n8n Cloud | Docker (DigitalOcean) |
|---------|-----------|----------------------|
| **n8n** | $240/year | $0 (included in droplet) |
| **Server** | $0 (included) | $144/year ($12/mo droplet) |
| **PostgreSQL** | $0 (included) | $0 (included in droplet) |
| **Qdrant** | ❌ Not available | $0 (included in droplet) |
| **Redis** | ❌ Not available | $0 (included in droplet) |
| **MinIO** | ❌ Not available | $0 (included in droplet) |
| **AI Agent API** | ❌ Not available | $0 (included in droplet) |
| **TOTAL YEAR 1** | **$240** | **$144** |

**Savings:** $96/year (40% cheaper) + WAY more functionality

**If you need more resources:**
- $24/mo droplet (4GB RAM): Better for production
- Total: $288/year (still better value than n8n Cloud alone)

---

## 🚨 TROUBLESHOOTING

| Issue | Solution |
|-------|----------|
| "Port 5678 already in use" | Change port in docker-compose.yml: "5679:5678" |
| "Cannot connect to Qdrant" | Check: `docker-compose logs qdrant` |
| "n8n won't start" | Check .env file has all required variables |
| "Out of disk space" | Clean: `docker system prune -a` |
| "Can't access via domain" | Check DNS, check Nginx config |
| "SSL certificate fails" | Ensure port 80/443 open, domain points to server |

### **Reset Everything:**

```bash
# DANGER: This deletes all data
docker-compose down -v
docker-compose up -d
```

---

## 📋 MIGRATION FROM N8N CLOUD

### **Step 1: Export Workflows from n8n Cloud**
```
1. Log into n8n Cloud
2. Go to each workflow
3. Click "..." → "Export"
4. Save as JSON files
```

### **Step 2: Import to Self-Hosted n8n**
```
1. Access your self-hosted n8n: http://YOUR_DOMAIN:5678
2. Create account (first time)
3. Go to Workflows
4. Click "Import from File"
5. Upload each JSON file
6. Update credentials (API keys) in self-hosted version
```

### **Step 3: Update Apify Webhooks**
```
1. Go to Apify dashboard
2. Update webhook URL from n8n Cloud to your new domain
3. Test webhook
```

### **Step 4: Cancel n8n Cloud**
```
Once verified working, cancel n8n Cloud subscription
```

---

## ✅ QUICK START CHECKLIST

**Prerequisites:**
- [ ] Docker installed
- [ ] Docker Compose installed
- [ ] Domain name (optional but recommended)
- [ ] Server/droplet created (if production)

**Setup (30-60 minutes):**
- [ ] Clone repository
- [ ] Copy .env.example to .env
- [ ] Fill in all API keys in .env
- [ ] Generate encryption keys
- [ ] Run `docker-compose up -d`
- [ ] Access n8n at http://localhost:5678
- [ ] Create n8n admin account
- [ ] Import workflows from JSON files
- [ ] Test Qdrant: http://localhost:6333/dashboard
- [ ] Test AI Agent API: http://localhost:8080/health
- [ ] Configure GHL webhooks
- [ ] Test end-to-end workflow

**Production Only:**
- [ ] Point domain to server IP
- [ ] Set up SSL with Let's Encrypt
- [ ] Configure firewall (UFW)
- [ ] Set up automated backups
- [ ] Configure monitoring/alerts

---

## 🎓 LEARNING RESOURCES

**Docker:**
- Official docs: https://docs.docker.com
- Docker Compose: https://docs.docker.com/compose/
- Awesome Docker: https://github.com/veggiemonk/awesome-docker

**n8n:**
- Self-hosting: https://docs.n8n.io/hosting/
- Docker setup: https://docs.n8n.io/hosting/installation/docker/

**Qdrant:**
- Docs: https://qdrant.tech/documentation/
- Quick start: https://qdrant.tech/documentation/quick-start/

**FastAPI:**
- Docs: https://fastapi.tiangolo.com
- Tutorial: https://fastapi.tiangolo.com/tutorial/

---

## 🎯 NEXT STEPS

1. ✅ Review this guide
2. ✅ Decide: Local development or production deployment
3. ✅ Set up Docker environment
4. ✅ Configure .env file
5. ✅ Start services with `docker-compose up -d`
6. ✅ Import n8n workflows
7. ✅ Test RAG functionality
8. ✅ Integrate with existing Metroflex systems

**You're ready to build with Docker! 🚀**
