#!/bin/bash
# WARP PROTOCOL: Interactive Railway Deployment
# This script guides you through Railway deployment step-by-step

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Railway CLI path
export PATH="$HOME/.npm-global/bin:/usr/local/bin:$PATH"
RAILWAY_CLI="$HOME/.npm-global/bin/railway"

BASE_DIR="/Users/noelpena/Desktop/CircuitOS_Local_Complete_Package"
cd "$BASE_DIR"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${BLUE}🚀 WARP PROTOCOL: Interactive Railway Deployment${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo -e "${YELLOW}This will deploy your CircuitOS MetroFlex system to Railway.${NC}"
echo -e "${YELLOW}Total time: ~40 minutes${NC}"
echo ""

# Function to wait for user confirmation
wait_for_user() {
    echo ""
    echo -e "${YELLOW}Press ENTER when ready to continue...${NC}"
    read -r
}

# Step 1: Check Railway CLI
echo -e "${BLUE}[STEP 1/5] Checking Railway CLI${NC}"
echo "─────────────────────────────────────────────────────────────────────────"
if [ ! -f "$RAILWAY_CLI" ]; then
    echo -e "${RED}❌ Railway CLI not found${NC}"
    echo "Installing Railway CLI..."
    npm install -g @railway/cli
    echo -e "${GREEN}✅ Railway CLI installed${NC}"
else
    echo -e "${GREEN}✅ Railway CLI found${NC}"
    echo "   Path: $RAILWAY_CLI"
fi
echo ""

# Step 2: Login to Railway
echo -e "${BLUE}[STEP 2/5] Login to Railway${NC}"
echo "─────────────────────────────────────────────────────────────────────────"

if $RAILWAY_CLI whoami &> /dev/null; then
    USER=$($RAILWAY_CLI whoami)
    echo -e "${GREEN}✅ Already logged in to Railway${NC}"
    echo "   User: $USER"
else
    echo -e "${YELLOW}⚠️  Not logged in to Railway${NC}"
    echo ""
    echo "I will now open Railway login in your browser."
    echo ""
    echo "What to do:"
    echo "  1. A browser window will open"
    echo "  2. Login with GitHub or email"
    echo "  3. Come back to this terminal"
    echo ""
    wait_for_user

    echo "Opening Railway login..."
    $RAILWAY_CLI login

    echo ""
    echo -e "${GREEN}✅ Railway login complete${NC}"
fi
echo ""

# Step 3: Create or link Railway project
echo -e "${BLUE}[STEP 3/5] Create Railway Project${NC}"
echo "─────────────────────────────────────────────────────────────────────────"

if $RAILWAY_CLI status &> /dev/null; then
    echo -e "${GREEN}✅ Already linked to a Railway project${NC}"
    $RAILWAY_CLI status
else
    echo "Creating new Railway project..."
    echo ""
    echo "What to do when prompted:"
    echo "  - Project name: Type 'circuitos-metroflex' (or press Enter)"
    echo "  - Template: Select 'Empty Project'"
    echo ""
    wait_for_user

    $RAILWAY_CLI init

    echo ""
    echo -e "${GREEN}✅ Railway project created${NC}"
fi
echo ""

# Step 4: Link to GitHub
echo -e "${BLUE}[STEP 4/5] Link to GitHub Repository${NC}"
echo "─────────────────────────────────────────────────────────────────────────"
echo "Repository: https://github.com/drive-brand-growth/Circuitos"
echo ""
echo "What to do when prompted:"
echo "  - Select repository: drive-brand-growth/Circuitos"
echo "  - Branch: main"
echo ""
wait_for_user

$RAILWAY_CLI link

echo ""
echo -e "${GREEN}✅ GitHub repository linked${NC}"
echo ""

# Step 5: Set environment variables
echo -e "${BLUE}[STEP 5/5] Set Environment Variables${NC}"
echo "─────────────────────────────────────────────────────────────────────────"

# Read OpenAI API key from .env
OPENAI_KEY=$(grep "^OPENAI_API_KEY=" .env | cut -d'=' -f2)

if [ -z "$OPENAI_KEY" ]; then
    echo -e "${RED}❌ OpenAI API key not found in .env file${NC}"
    exit 1
fi

echo "Setting environment variables..."
echo ""

echo "1/5 Setting OPENAI_API_KEY..."
$RAILWAY_CLI variables set OPENAI_API_KEY="$OPENAI_KEY"
echo -e "${GREEN}   ✅ OPENAI_API_KEY set${NC}"

echo "2/5 Setting POSTGRES_PASSWORD..."
POSTGRES_PASS=$(openssl rand -base64 32)
$RAILWAY_CLI variables set POSTGRES_PASSWORD="$POSTGRES_PASS"
echo -e "${GREEN}   ✅ POSTGRES_PASSWORD set${NC}"

echo "3/5 Setting ENVIRONMENT..."
$RAILWAY_CLI variables set ENVIRONMENT="production"
echo -e "${GREEN}   ✅ ENVIRONMENT set${NC}"

echo "4/5 Setting DEBUG..."
$RAILWAY_CLI variables set DEBUG="false"
echo -e "${GREEN}   ✅ DEBUG set${NC}"

echo "5/5 Setting GHL_LEAD_CAPTURE_WEBHOOK..."
$RAILWAY_CLI variables set GHL_LEAD_CAPTURE_WEBHOOK="https://placeholder-get-real-webhook-from-brian.com"
echo -e "${GREEN}   ✅ GHL_LEAD_CAPTURE_WEBHOOK set${NC}"

echo ""
echo -e "${GREEN}✅ All environment variables configured${NC}"
echo ""

# Final confirmation before deployment
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${BLUE}🚢 Ready to Deploy!${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "What will happen next:"
echo "  - Railway will pull your code from GitHub"
echo "  - Railway will build all 16 Docker services"
echo "  - Railway will deploy to production"
echo "  - Railway will provide public HTTPS URLs"
echo ""
echo -e "${YELLOW}⏱️  This takes 20-25 minutes${NC}"
echo -e "${GREEN}💰 Monthly cost: \$45-65${NC}"
echo ""
echo "Do you want to deploy now? (y/n)"
read -r DEPLOY_CONFIRM

if [ "$DEPLOY_CONFIRM" != "y" ] && [ "$DEPLOY_CONFIRM" != "Y" ]; then
    echo ""
    echo -e "${YELLOW}Deployment cancelled. Run this script again when ready.${NC}"
    exit 0
fi

echo ""
echo -e "${BLUE}Starting deployment...${NC}"
echo ""

$RAILWAY_CLI up

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${GREEN}🎉 DEPLOYMENT COMPLETE!${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Get deployment status
echo "Getting your deployment information..."
echo ""
$RAILWAY_CLI status

echo ""
echo -e "${BLUE}📋 Next Steps:${NC}"
echo ""
echo "1. Get your live URLs:"
echo "   $RAILWAY_CLI domain"
echo ""
echo "2. Test your Events AI agent:"
echo "   curl -X POST https://your-url.railway.app/api/events/chat \\"
echo "     -H \"Content-Type: application/json\" \\"
echo "     -d '{\"query\": \"When is the next MetroFlex event?\"}'"
echo ""
echo "3. Test your Gym AI agent:"
echo "   curl -X POST https://your-url.railway.app/api/gym/chat \\"
echo "     -H \"Content-Type: application/json\" \\"
echo "     -d '{\"query\": \"How much is membership?\"}'"
echo ""
echo "4. Access Grafana monitoring:"
echo "   https://your-url.railway.app/grafana"
echo "   Login: admin / admin (change on first login)"
echo ""
echo "5. Update GHL webhook (get Brian's real URL):"
echo "   $RAILWAY_CLI variables set GHL_LEAD_CAPTURE_WEBHOOK=\"brians_real_webhook\""
echo ""
echo -e "${GREEN}✅ You're now LIVE in production!${NC}"
echo ""
