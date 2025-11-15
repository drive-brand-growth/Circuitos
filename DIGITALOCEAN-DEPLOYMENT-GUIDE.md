# 🚀 DigitalOcean Deployment Guide - Complete Stack

## Your Complete Metroflex AI System in 45 Minutes

This guide deploys:
- 3× n8n instances (Events, Gym, Circuit)
- Complete RAG system (Qdrant + NotebookLM)
- 6× MCP servers + Gateway
- All AI agent APIs
- PostgreSQL, Redis, MinIO
- Portainer management UI

**Total Cost: $48-68/mo**

---

## 📋 PREREQUISITES

### **1. DigitalOcean Account**
- Sign up at https://www.digitalocean.com
- Add payment method
- Get $200 free credit (60 days) with GitHub Student Pack or referral

### **2. Domain (Optional but Recommended)**
- Register domain (Namecheap, Cloudflare, etc.)
- Example: `metroflexai.com`
- You'll point this to your droplet

### **3. API Keys Ready**
```bash
# Have these ready to paste
CLAUDE_API_KEY=sk-ant-...
GOOGLE_MAPS_API_KEY=AIza...
OPENWEATHER_API_KEY=...
GHL_WEBHOOK_URL=https://...
```

---

## 🖥️ STEP 1: CREATE DROPLET (5 minutes)

### **1.1: Log into DigitalOcean**
- Go to https://cloud.digitalocean.com
- Click "Create" → "Droplets"

### **1.2: Choose Configuration**

**Choose an image:**
- Ubuntu 22.04 (LTS) x64

**Choose plan:**
- Click "Shared CPU" → "Regular"
- Select: **8 GB / 4 CPUs / 160 GB SSD / 5 TB transfer**
- Cost: **$48/month**

**Choose datacenter region:**
- New York 3 (closest to Texas for low latency)
- OR San Francisco 3 (if West Coast users)

**Authentication:**
- SSH Key (RECOMMENDED)
  - Click "New SSH Key"
  - Paste your public key (run `cat ~/.ssh/id_rsa.pub` on your Mac)
  - Name it "My Mac"
- OR Password (less secure)

**Hostname:**
- `metroflex-ai-stack`

**Click "Create Droplet"**

### **1.3: Wait 60 seconds**
- Droplet will be created and show public IP
- Copy the IP address (example: `159.89.123.45`)

---

## 🔧 STEP 2: INITIAL SERVER SETUP (10 minutes)

### **2.1: SSH into Server**
```bash
# From your terminal
ssh root@159.89.123.45
# (replace with your actual IP)

# Type 'yes' when asked about fingerprint
```

### **2.2: Update System**
```bash
apt update && apt upgrade -y
```

### **2.3: Install Docker**
```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Verify installation
docker --version
# Should show: Docker version 24.x.x

docker compose version
# Should show: Docker Compose version 2.x.x
```

### **2.4: Install Git**
```bash
apt install git -y
```

### **2.5: Create Swap File (Prevents OOM kills)**
```bash
# Create 4GB swap
fallocate -l 4G /swapfile
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile

# Make permanent
echo '/swapfile none swap sw 0 0' >> /etc/fstab

# Verify
free -h
# Should show 4GB swap
```

---

## 📦 STEP 3: DEPLOY YOUR STACK (15 minutes)

### **3.1: Clone Repository**
```bash
cd /root
git clone https://github.com/your-username/Circuitos.git
cd Circuitos
```

### **3.2: Create Environment File**
```bash
cp .env.example .env
nano .env
```

**Paste your configuration:**
```bash
# PostgreSQL
POSTGRES_USER=admin
POSTGRES_PASSWORD=CHANGE_THIS_STRONG_PASSWORD_123!

# n8n
N8N_USER=admin
N8N_PASSWORD=CHANGE_THIS_STRONG_PASSWORD_456!
N8N_ENCRYPTION_KEY=$(openssl rand -hex 32)
N8N_HOST=yourdomain.com
N8N_GYM_HOST=gym.yourdomain.com

# Claude API
CLAUDE_API_KEY=sk-ant-your-actual-key-here

# Google Services
GOOGLE_MAPS_API_KEY=AIzaYourActualKeyHere
GA4_PROPERTY_ID=123456789
GA4_CREDENTIALS_JSON={"type":"service_account"...}

# Google My Business
GMB_ACCOUNT_ID=your-gmb-account-id
GMB_LOCATION_ID=your-location-id
GMB_CREDENTIALS_JSON={"type":"service_account"...}

# OpenWeather
OPENWEATHER_API_KEY=your-openweather-key

# GoHighLevel
GHL_API_KEY=your-ghl-api-key
GHL_WEBHOOK_URL=https://hooks.gohighlevel.com/...

# MinIO
MINIO_ROOT_USER=minioadmin
MINIO_ROOT_PASSWORD=CHANGE_THIS_STRONG_PASSWORD_789!

# Timezone
TIMEZONE=America/Chicago
```

**Save and exit:**
- Press `Ctrl+X`
- Press `Y`
- Press `Enter`

### **3.3: Generate Missing Keys**
```bash
# Generate n8n encryption key
echo "N8N_ENCRYPTION_KEY=$(openssl rand -hex 32)" >> .env
```

### **3.4: Create Required Directories**
```bash
mkdir -p shared-files
mkdir -p backups
mkdir -p documents
mkdir -p nginx/conf.d
mkdir -p nginx/ssl
mkdir -p nginx/logs
```

### **3.5: Deploy Stack**
```bash
# Start everything
docker compose -f docker-compose-with-mcp.yml up -d

# This will:
# - Pull all images (5-10 minutes first time)
# - Create networks
# - Start all 20+ containers
```

### **3.6: Monitor Startup**
```bash
# Watch logs
docker compose -f docker-compose-with-mcp.yml logs -f

# Press Ctrl+C to stop watching

# Check status
docker ps

# Should see 20+ containers running
```

---

## ✅ STEP 4: VERIFY DEPLOYMENT (5 minutes)

### **4.1: Check Container Health**
```bash
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

**Expected output:**
```
NAMES                    STATUS              PORTS
n8n-metroflex-events    Up 2 minutes        0.0.0.0:5678->5678/tcp
n8n-gym-operations      Up 2 minutes        0.0.0.0:5679->5678/tcp
qdrant-rag              Up 2 minutes        0.0.0.0:6333->6333/tcp
redis-cache             Up 2 minutes        0.0.0.0:6379->6379/tcp
postgres-main           Up 2 minutes        5432/tcp
mcp-gateway             Up 2 minutes        0.0.0.0:8089->8080/tcp
mcp-google-maps         Up 2 minutes        0.0.0.0:8090->8080/tcp
portainer-mgmt          Up 2 minutes        0.0.0.0:9000->9000/tcp
...
```

### **4.2: Test Services**

**Test Portainer (Docker Management UI):**
```bash
curl http://localhost:9000
# Should return HTML
```

Open in browser: `http://159.89.123.45:9000`
- Create admin account
- You'll see all containers

**Test n8n (Metroflex Events):**
```bash
curl http://localhost:5678
# Should return HTML
```

Open in browser: `http://159.89.123.45:5678`
- Login: admin / your-password-from-env
- You should see n8n interface

**Test Qdrant (RAG Vector DB):**
```bash
curl http://localhost:6333/collections
# Should return: {"result":{"collections":[]}}
```

**Test MCP Gateway:**
```bash
curl http://localhost:8089/health
# Should return: {"status":"healthy","mcp_servers":[...],"timestamp":"..."}
```

**Test MCP Geocoding:**
```bash
curl "http://localhost:8089/maps/geocode?address=Dallas,TX"
# Should return geocoding data
```

### **4.3: Check Logs for Errors**
```bash
# Check individual service
docker logs n8n-metroflex-events

# Check MCP gateway
docker logs mcp-gateway

# Check Qdrant
docker logs qdrant-rag
```

**If you see errors:** Most common issues:
- Missing API keys in `.env`
- Incorrect formatting of JSON credentials
- Database not ready (wait 30 seconds and restart)

---

## 🌐 STEP 5: SET UP DOMAIN & SSL (10 minutes)

### **5.1: Point Domain to Droplet**

**In your domain registrar (Namecheap, Cloudflare, etc.):**
```
Type: A Record
Name: @
Value: 159.89.123.45 (your droplet IP)
TTL: 300 (5 minutes)

Type: A Record
Name: n8n
Value: 159.89.123.45
TTL: 300

Type: A Record
Name: api
Value: 159.89.123.45
TTL: 300

Type: A Record
Name: qdrant
Value: 159.89.123.45
TTL: 300
```

**Wait 5-10 minutes for DNS propagation**

### **5.2: Install Certbot for SSL**
```bash
# Back on your droplet
apt install certbot python3-certbot-nginx -y
```

### **5.3: Get SSL Certificates**
```bash
# Replace with your actual domains
certbot --nginx -d metroflexai.com -d www.metroflexai.com -d n8n.metroflexai.com -d api.metroflexai.com

# Follow prompts:
# - Enter email
# - Agree to terms
# - Choose: Redirect HTTP to HTTPS
```

### **5.4: Configure Nginx**
```bash
nano /root/Circuitos/nginx/conf.d/default.conf
```

**Paste this configuration:**
```nginx
# n8n Metroflex Events
server {
    listen 80;
    server_name n8n.metroflexai.com;

    location / {
        proxy_pass http://n8n-metroflex:5678;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# MCP Gateway API
server {
    listen 80;
    server_name api.metroflexai.com;

    location / {
        proxy_pass http://mcp-gateway:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

# Qdrant Admin UI
server {
    listen 80;
    server_name qdrant.metroflexai.com;

    location / {
        proxy_pass http://qdrant:6333;
        proxy_set_header Host $host;
    }
}
```

**Restart Nginx:**
```bash
cd /root/Circuitos
docker compose -f docker-compose-with-mcp.yml restart nginx
```

### **5.5: Test HTTPS**
Open in browser:
- `https://n8n.metroflexai.com` → n8n interface
- `https://api.metroflexai.com/health` → MCP gateway health
- `https://qdrant.metroflexai.com` → Qdrant dashboard

**You now have SSL! 🎉**

---

## 🎯 STEP 6: IMPORT N8N WORKFLOW (5 minutes)

### **6.1: Access n8n**
- Go to `https://n8n.metroflexai.com`
- Login with credentials from `.env`

### **6.2: Import NPC Competitor Scraper**
1. Click "Workflows" in left sidebar
2. Click "Add Workflow" → "Import from File"
3. Upload: `/root/Circuitos/n8n-npc-competitor-scraper-workflow.json`
4. Workflow appears with all nodes

### **6.3: Configure Credentials**
1. Click on "Claude AI" node
2. Create credential → Paste your `CLAUDE_API_KEY`
3. Click on "HTTP Request" node (GHL webhook)
4. Update URL to your actual GHL webhook

### **6.4: Activate Workflow**
1. Click toggle switch in top-right to "Active"
2. Copy the webhook URL (shown in "Webhook" node)
3. Use this URL in your Apify scraper

---

## 📊 STEP 7: SET UP RAG KNOWLEDGE BASES (Optional)

### **7.1: Scrape NPC Texas Website**
```bash
# From your droplet
docker exec -it rag-ingestor python website-scraper.py \
  --url "https://npc-texas.com" \
  --collection "npc_texas" \
  --max-pages 50

# Scrapes 50 pages → chunks → stores in Qdrant
```

### **7.2: Verify Collection Created**
```bash
curl http://localhost:6333/collections
# Should show: "npc_texas" collection
```

### **7.3: Query Your Knowledge Base**
```bash
curl -X POST http://localhost:8084/query \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What are the upcoming NPC Texas shows?",
    "collection": "npc_texas",
    "top_k": 5
  }'

# Returns answer with citations!
```

---

## 🔐 STEP 8: SECURE YOUR SYSTEM (5 minutes)

### **8.1: Set Up Firewall**
```bash
# Install UFW
apt install ufw -y

# Allow SSH
ufw allow 22/tcp

# Allow HTTP/HTTPS
ufw allow 80/tcp
ufw allow 443/tcp

# Allow n8n (if you want direct IP access)
ufw allow 5678/tcp
ufw allow 5679/tcp

# Allow Portainer
ufw allow 9000/tcp

# Enable firewall
ufw enable

# Check status
ufw status
```

### **8.2: Change Default Ports (Optional)**
**For extra security, change exposed ports:**
```bash
nano /root/Circuitos/docker-compose-with-mcp.yml

# Change:
# - "5678:5678"  →  - "15678:5678"
# - "9000:9000"  →  - "19000:9000"

# Then restart
docker compose -f docker-compose-with-mcp.yml down
docker compose -f docker-compose-with-mcp.yml up -d
```

### **8.3: Enable Automatic Backups**
**Already included!** The backup service runs daily at 2am.

**Check backups:**
```bash
ls -lh /root/Circuitos/backups/
# Should see: circuit-os-20250115.tar.gz (daily)
```

**Restore from backup:**
```bash
cd /root/Circuitos
docker compose -f docker-compose-with-mcp.yml down
tar -xzf backups/circuit-os-20250115.tar.gz
docker compose -f docker-compose-with-mcp.yml up -d
```

---

## 🎉 SUCCESS! YOUR STACK IS LIVE

### **Access Your Services:**
```
Portainer (Management):         https://159.89.123.45:9000
n8n (Metroflex Events):         https://n8n.metroflexai.com
n8n (Gym Operations):           http://159.89.123.45:5679
Qdrant Dashboard:               https://qdrant.metroflexai.com
MCP Gateway API:                https://api.metroflexai.com
NotebookLM Query Interface:     http://159.89.123.45:8084
```

### **Test MCP Gateway:**
```bash
# Geocode
curl "https://api.metroflexai.com/maps/geocode?address=Arlington,TX"

# Demographics
curl "https://api.metroflexai.com/census/demographics?zip=76010"

# Location Intelligence (composite)
curl "https://api.metroflexai.com/composite/location-intelligence?address=Dallas,TX"
```

### **Next Steps:**
1. ✅ Import NPC competitor scraper workflow
2. ✅ Set up Apify scraper for Instagram/Facebook
3. ✅ Build RAG knowledge bases (NPC sites, competitor shows)
4. ✅ Test athlete recruitment automation
5. ✅ Monitor costs and performance

---

## 🆘 TROUBLESHOOTING

### **Container won't start:**
```bash
# Check logs
docker logs container-name

# Restart specific container
docker restart container-name

# Recreate container
docker compose -f docker-compose-with-mcp.yml up -d --force-recreate container-name
```

### **Out of memory:**
```bash
# Check memory usage
free -h

# Check which container is using most memory
docker stats

# Restart memory-hungry container
docker restart container-name
```

### **Can't access service:**
```bash
# Check if port is open
netstat -tulpn | grep 5678

# Check firewall
ufw status

# Check Nginx
docker logs nginx-proxy
```

### **Database connection error:**
```bash
# Check PostgreSQL is running
docker ps | grep postgres

# Check database logs
docker logs postgres-main

# Restart PostgreSQL
docker restart postgres-main

# Wait 10 seconds, then restart dependent services
docker restart n8n-metroflex-events
```

### **MCP server not responding:**
```bash
# Check MCP gateway logs
docker logs mcp-gateway

# Check individual MCP server
docker logs mcp-google-maps

# Test health
curl http://localhost:8089/health
```

---

## 💰 COST MONITORING

### **Check Your DigitalOcean Bill:**
1. Go to https://cloud.digitalocean.com/account/billing
2. Monitor usage
3. Set billing alerts

**Expected monthly:**
```
Droplet (8GB):           $48.00
Block Storage (optional): $10.00
Bandwidth (included):     $0.00
────────────────────────────────
TOTAL:                   $48-58/mo
```

### **Monitor API Costs:**
```bash
# Check Claude API usage
# Go to: https://console.anthropic.com/settings/billing

# Check Google Maps API usage
# Go to: https://console.cloud.google.com/billing

# Set up budget alerts!
```

---

## 📚 USEFUL COMMANDS

### **Manage Containers:**
```bash
# View all containers
docker ps -a

# View logs
docker logs -f container-name

# Restart all
docker compose -f docker-compose-with-mcp.yml restart

# Stop all
docker compose -f docker-compose-with-mcp.yml down

# Start all
docker compose -f docker-compose-with-mcp.yml up -d

# Update all images
docker compose -f docker-compose-with-mcp.yml pull
docker compose -f docker-compose-with-mcp.yml up -d
```

### **System Maintenance:**
```bash
# Check disk usage
df -h

# Clean up old Docker images
docker system prune -a

# Check memory
free -h

# Check CPU
top
```

### **Backup Manually:**
```bash
cd /root/Circuitos
tar -czf backups/manual-backup-$(date +%Y%m%d).tar.gz \
  -C /var/lib/docker/volumes/ \
  postgres_data qdrant_data n8n_metroflex_data
```

---

## ✅ DEPLOYMENT COMPLETE!

**You now have:**
- ✅ Complete AI agent infrastructure
- ✅ 3 n8n instances for automation
- ✅ RAG system with Qdrant
- ✅ 6 MCP servers for data enrichment
- ✅ Automatic backups
- ✅ SSL encryption
- ✅ Monitoring via Portainer
- ✅ Cost: $48-68/mo (vs $150-300/mo cloud services)

**Time to start building! 💪**

**Questions? Check:**
- Portainer logs (visual UI)
- `/root/Circuitos/README.md` for architecture
- `ULTIMATE-RAG-GUIDE.md` for RAG usage
- `MCP-RAG-INTEGRATION-GUIDE.md` for MCP examples

**Ready to scrape those NPC competitors and recruit athletes! 🏋️**
