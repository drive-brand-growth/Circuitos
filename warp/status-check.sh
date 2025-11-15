#!/bin/bash

# Warp Protocol Status Check
# Shows what's done and what needs to be done for CircuitOS MetroFlex deployment

set -e

# Color codes for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${BLUE}🚀 CircuitOS MetroFlex - Warp Protocol Status Check${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Section 1: GitHub Status
echo -e "${BLUE}📦 GITHUB REPOSITORY${NC}"
echo "─────────────────────────────────────────────────────────────────────────"

if [ -d ".git" ]; then
    CURRENT_BRANCH=$(git branch --show-current)
    COMMIT_COUNT=$(git rev-list --count HEAD)
    LAST_COMMIT=$(git log -1 --pretty=format:"%h - %s (%cr)")

    echo -e "${GREEN}✅ Repository initialized${NC}"
    echo "   Branch: $CURRENT_BRANCH"
    echo "   Commits: $COMMIT_COUNT"
    echo "   Latest: $LAST_COMMIT"

    # Check if there are uncommitted changes
    if [[ -n $(git status -s) ]]; then
        UNCOMMITTED=$(git status -s | wc -l | xargs)
        echo -e "${YELLOW}⚠️  $UNCOMMITTED uncommitted changes${NC}"
    else
        echo -e "${GREEN}✅ All changes committed${NC}"
    fi

    # Check remote
    if git remote -v | grep -q "github.com"; then
        REMOTE_URL=$(git remote get-url origin)
        echo -e "${GREEN}✅ GitHub remote configured${NC}"
        echo "   URL: $REMOTE_URL"
    else
        echo -e "${RED}❌ No GitHub remote configured${NC}"
    fi
else
    echo -e "${RED}❌ Not a git repository${NC}"
fi

echo ""

# Section 2: Local Infrastructure Status
echo -e "${BLUE}🏗️  LOCAL INFRASTRUCTURE${NC}"
echo "─────────────────────────────────────────────────────────────────────────"

if command -v docker-compose &> /dev/null || command -v docker &> /dev/null; then
    # Check if docker-compose-infrastructure.yml exists and get status
    if [ -f "docker-compose-infrastructure.yml" ]; then
        echo -e "${GREEN}✅ Infrastructure config found${NC}"
        echo ""

        # Get running services
        if docker-compose -f docker-compose-infrastructure.yml ps --services --filter "status=running" 2>/dev/null | grep -q .; then
            RUNNING_COUNT=$(docker-compose -f docker-compose-infrastructure.yml ps --services --filter "status=running" 2>/dev/null | wc -l | xargs)
            echo -e "${GREEN}✅ $RUNNING_COUNT services running${NC}"
            echo ""

            # Check each service
            for service in postgres redis prometheus grafana alertmanager promtail loki; do
                if docker-compose -f docker-compose-infrastructure.yml ps --services --filter "status=running" 2>/dev/null | grep -q "^${service}$"; then
                    PORT=""
                    case $service in
                        postgres) PORT="5432" ;;
                        redis) PORT="6379" ;;
                        prometheus) PORT="9090" ;;
                        grafana) PORT="3000" ;;
                        alertmanager) PORT="9093" ;;
                        loki) PORT="3100" ;;
                    esac
                    if [ -n "$PORT" ]; then
                        echo -e "${GREEN}   ✅ $service${NC} - Port $PORT"
                    else
                        echo -e "${GREEN}   ✅ $service${NC}"
                    fi
                else
                    echo -e "${RED}   ❌ $service${NC} - Not running"
                fi
            done

            echo ""
            echo -e "${BLUE}📊 Quick Links:${NC}"
            echo "   Grafana:    http://localhost:3000 (admin/admin)"
            echo "   Prometheus: http://localhost:9090"
        else
            echo -e "${YELLOW}⚠️  Infrastructure configured but not running${NC}"
            echo ""
            echo "   To start: docker-compose -f docker-compose-infrastructure.yml up -d"
        fi
    else
        echo -e "${RED}❌ Infrastructure config not found${NC}"
    fi
else
    echo -e "${RED}❌ Docker not installed or not running${NC}"
fi

echo ""

# Section 3: Dual RAG Knowledge Bases
echo -e "${BLUE}🧠 DUAL RAG KNOWLEDGE BASES${NC}"
echo "─────────────────────────────────────────────────────────────────────────"

EVENTS_KB="Active/metroflex-ghl-website/AI_Agent/METROFLEX_EVENTS_KB_V3_EVENTS_ONLY.json"
GYM_KB="Active/metroflex-ghl-website/METROFLEX_GYM_KB_V1.json"

if [ -f "$EVENTS_KB" ]; then
    EVENTS_SIZE=$(wc -c < "$EVENTS_KB" | xargs)
    echo -e "${GREEN}✅ Events RAG${NC} - $EVENTS_SIZE bytes"
    echo "   Covers: Competitions, Tickets, Vendors, Sponsors"
else
    echo -e "${RED}❌ Events RAG not found${NC}"
fi

if [ -f "$GYM_KB" ]; then
    GYM_SIZE=$(wc -c < "$GYM_KB" | xargs)
    echo -e "${GREEN}✅ Gym RAG${NC} - $GYM_SIZE bytes"
    echo "   Covers: Memberships, Licensing, Apparel, Locations"
else
    echo -e "${RED}❌ Gym RAG not found${NC}"
fi

echo ""

# Section 4: Docker Services Configuration
echo -e "${BLUE}🐳 DOCKER SERVICES CONFIGURATION${NC}"
echo "─────────────────────────────────────────────────────────────────────────"

if [ -f "docker-compose.yml" ]; then
    SERVICE_COUNT=$(grep -c "^  [a-z]" docker-compose.yml || echo "0")
    echo -e "${GREEN}✅ docker-compose.yml found${NC}"
    echo "   Services configured: $SERVICE_COUNT"
else
    echo -e "${RED}❌ docker-compose.yml not found${NC}"
fi

# Check for Dockerfiles
DOCKERFILE_COUNT=$(find . -name "Dockerfile" -o -name "Dockerfile.*" 2>/dev/null | wc -l | xargs)
if [ "$DOCKERFILE_COUNT" -gt 0 ]; then
    echo -e "${GREEN}✅ $DOCKERFILE_COUNT Dockerfiles found${NC}"
else
    echo -e "${YELLOW}⚠️  No Dockerfiles found${NC}"
fi

echo ""

# Section 5: Railway Deployment Status
echo -e "${BLUE}🚂 RAILWAY DEPLOYMENT${NC}"
echo "─────────────────────────────────────────────────────────────────────────"

# Check if Railway CLI is installed
RAILWAY_CLI="$HOME/.npm-global/bin/railway"
if [ -f "$RAILWAY_CLI" ]; then
    echo -e "${GREEN}✅ Railway CLI installed${NC}"
    echo "   Path: $RAILWAY_CLI"
else
    echo -e "${RED}❌ Railway CLI not found${NC}"
    echo "   Install: npm install -g @railway/cli"
fi

# Check Railway config files
if [ -f "railway.json" ]; then
    echo -e "${GREEN}✅ railway.json configured${NC}"
else
    echo -e "${RED}❌ railway.json not found${NC}"
fi

if [ -f "railway.toml" ]; then
    echo -e "${GREEN}✅ railway.toml configured${NC}"
else
    echo -e "${RED}❌ railway.toml not found${NC}"
fi

# Check if Railway is logged in
if [ -f "$RAILWAY_CLI" ]; then
    if $RAILWAY_CLI whoami &>/dev/null; then
        RAILWAY_USER=$($RAILWAY_CLI whoami 2>/dev/null || echo "Unknown")
        echo -e "${GREEN}✅ Logged in to Railway${NC}"
        echo "   User: $RAILWAY_USER"
    else
        echo -e "${YELLOW}⚠️  Not logged in to Railway${NC}"
        echo "   Run: $RAILWAY_CLI login"
    fi
else
    echo -e "${YELLOW}⚠️  Railway CLI not available for login check${NC}"
fi

echo ""

# Section 6: Environment Variables
echo -e "${BLUE}🔐 ENVIRONMENT CONFIGURATION${NC}"
echo "─────────────────────────────────────────────────────────────────────────"

if [ -f ".env" ]; then
    echo -e "${GREEN}✅ .env file exists${NC}"

    # Check for critical environment variables (without showing values)
    if grep -q "OPENAI_API_KEY=" .env; then
        echo -e "${GREEN}   ✅ OPENAI_API_KEY set${NC}"
    else
        echo -e "${RED}   ❌ OPENAI_API_KEY missing${NC}"
    fi

    if grep -q "GHL_LEAD_CAPTURE_WEBHOOK=" .env; then
        echo -e "${GREEN}   ✅ GHL_LEAD_CAPTURE_WEBHOOK set${NC}"
    else
        echo -e "${YELLOW}   ⚠️  GHL_LEAD_CAPTURE_WEBHOOK not set${NC}"
    fi
else
    echo -e "${RED}❌ .env file not found${NC}"
fi

if [ -f ".env.example" ]; then
    echo -e "${GREEN}✅ .env.example template exists${NC}"
else
    echo -e "${YELLOW}⚠️  .env.example not found${NC}"
fi

echo ""

# Section 7: Documentation Status
echo -e "${BLUE}📚 DOCUMENTATION${NC}"
echo "─────────────────────────────────────────────────────────────────────────"

DOCS=(
    "DEPLOY_NOW_APPROVED.md:Deployment commands (APPROVED)"
    "APPROVAL_NEEDED.md:Deployment approval guide"
    "DEPLOYMENT_COMPLETE_STATUS.md:System status"
    "RAILWAY_DEPLOY_NOW.md:Railway deployment guide"
    "WHERE_WE_ARE.md:Project overview"
)

DOC_COUNT=0
for doc_info in "${DOCS[@]}"; do
    DOC_FILE="${doc_info%%:*}"
    DOC_DESC="${doc_info#*:}"
    if [ -f "$DOC_FILE" ]; then
        echo -e "${GREEN}✅ $DOC_FILE${NC}"
        echo "   $DOC_DESC"
        ((DOC_COUNT++))
    fi
done

echo ""
echo "   Total: $DOC_COUNT/5 key documents found"

echo ""

# Section 8: Overall Progress
echo -e "${BLUE}📊 OVERALL PROGRESS${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

TOTAL_CHECKS=0
PASSED_CHECKS=0

# GitHub checks
((TOTAL_CHECKS++))
[ -d ".git" ] && ((PASSED_CHECKS++))

# Infrastructure checks
((TOTAL_CHECKS++))
[ -f "docker-compose-infrastructure.yml" ] && ((PASSED_CHECKS++))

# RAG checks
((TOTAL_CHECKS+=2))
[ -f "$EVENTS_KB" ] && ((PASSED_CHECKS++))
[ -f "$GYM_KB" ] && ((PASSED_CHECKS++))

# Docker checks
((TOTAL_CHECKS++))
[ -f "docker-compose.yml" ] && ((PASSED_CHECKS++))

# Railway checks
((TOTAL_CHECKS+=2))
[ -f "railway.json" ] && ((PASSED_CHECKS++))
[ -f "railway.toml" ] && ((PASSED_CHECKS++))

# Environment checks
((TOTAL_CHECKS++))
[ -f ".env" ] && ((PASSED_CHECKS++))

# Documentation checks
((TOTAL_CHECKS++))
[ -f "DEPLOY_NOW_APPROVED.md" ] && ((PASSED_CHECKS++))

PERCENTAGE=$((PASSED_CHECKS * 100 / TOTAL_CHECKS))

echo ""
echo -e "   Completion: ${GREEN}$PASSED_CHECKS/$TOTAL_CHECKS checks passed ($PERCENTAGE%)${NC}"
echo ""

if [ $PERCENTAGE -ge 90 ]; then
    echo -e "${GREEN}   🎉 SYSTEM READY FOR DEPLOYMENT!${NC}"
elif [ $PERCENTAGE -ge 70 ]; then
    echo -e "${YELLOW}   ⚠️  Almost ready - few items remaining${NC}"
else
    echo -e "${RED}   ❌ More setup needed before deployment${NC}"
fi

echo ""

# Section 9: Next Steps
echo -e "${BLUE}🎯 NEXT STEPS${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

if [ -f "DEPLOY_NOW_APPROVED.md" ]; then
    echo -e "${GREEN}✅ Deployment APPROVED - Ready to execute!${NC}"
    echo ""
    echo "Execute these 5 commands to deploy to Railway:"
    echo ""
    echo -e "${BLUE}1. Login to Railway:${NC}"
    echo "   $HOME/.npm-global/bin/railway login"
    echo ""
    echo -e "${BLUE}2. Create Railway project:${NC}"
    echo "   cd /Users/noelpena/Desktop/CircuitOS_Local_Complete_Package && $HOME/.npm-global/bin/railway init"
    echo ""
    echo -e "${BLUE}3. Link to GitHub:${NC}"
    echo "   $HOME/.npm-global/bin/railway link"
    echo ""
    echo -e "${BLUE}4. Set environment variables:${NC}"
    echo "   $HOME/.npm-global/bin/railway variables set OPENAI_API_KEY=\"\$(grep '^OPENAI_API_KEY=' .env | cut -d'=' -f2)\""
    echo "   $HOME/.npm-global/bin/railway variables set POSTGRES_PASSWORD=\"\$(openssl rand -base64 32)\""
    echo "   $HOME/.npm-global/bin/railway variables set ENVIRONMENT=\"production\""
    echo "   $HOME/.npm-global/bin/railway variables set DEBUG=\"false\""
    echo ""
    echo -e "${BLUE}5. Deploy to Railway:${NC}"
    echo "   $HOME/.npm-global/bin/railway up"
    echo ""
    echo -e "${YELLOW}⏱️  Total time: ~40 minutes${NC}"
    echo -e "${GREEN}💰 Monthly cost: \$45-65${NC}"
    echo ""
else
    echo "Review APPROVAL_NEEDED.md for deployment options"
fi

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${BLUE}📖 Full details: See DEPLOY_NOW_APPROVED.md${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
