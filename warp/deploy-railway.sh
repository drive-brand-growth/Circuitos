#!/bin/bash
# WARP PROTOCOL: Deploy to Railway
# Execution time: ~30 minutes (mostly Railway build time)
# Purpose: Automated Railway deployment with all services

set -e  # Exit on error

# Add Railway CLI to PATH
export PATH="$HOME/.npm-global/bin:/usr/local/bin:$PATH"
RAILWAY_CLI="$HOME/.npm-global/bin/railway"

echo "🚀 WARP PROTOCOL: Railway Deployment"
echo "================================================"
echo ""

BASE_DIR="/Users/noelpena/Desktop/CircuitOS_Local_Complete_Package"
cd "$BASE_DIR"

# Step 1: Check if Railway CLI is installed
echo "📦 [1/7] Checking Railway CLI..."
if [ ! -f "$RAILWAY_CLI" ]; then
    echo "❌ Railway CLI not found. Installing..."
    npm install -g @railway/cli
    echo "✅ Railway CLI installed"
else
    echo "✅ Railway CLI already installed"
fi
echo ""

# Step 2: Check Railway authentication
echo "🔐 [2/7] Checking Railway authentication..."
if $RAILWAY_CLI whoami &> /dev/null; then
    echo "✅ Already authenticated to Railway"
    $RAILWAY_CLI whoami
else
    echo "🔑 Opening Railway login..."
    $RAILWAY_CLI login
    echo "✅ Railway authentication complete"
fi
echo ""

# Step 3: Check if project exists or create new one
echo "📂 [3/7] Setting up Railway project..."
if $RAILWAY_CLI status &> /dev/null; then
    echo "✅ Already linked to Railway project"
    $RAILWAY_CLI status
else
    echo "🆕 Creating new Railway project..."
    $RAILWAY_CLI init
    echo "✅ Railway project created"
fi
echo ""

# Step 4: Link to GitHub repository
echo "🔗 [4/7] Linking to GitHub repository..."
echo "Repository: https://github.com/drive-brand-growth/Circuitos"
echo "This will deploy from your GitHub main branch"
$RAILWAY_CLI link
echo "✅ GitHub repository linked"
echo ""

# Step 5: Set environment variables
echo "⚙️  [5/7] Setting environment variables..."

# Read OpenAI API key from .env file
OPENAI_KEY=$(grep "^OPENAI_API_KEY=" .env | cut -d'=' -f2)

if [ -z "$OPENAI_KEY" ]; then
    echo "❌ OpenAI API key not found in .env file"
    exit 1
fi

echo "Setting OPENAI_API_KEY..."
$RAILWAY_CLI variables set OPENAI_API_KEY="$OPENAI_KEY"

echo "Setting POSTGRES_PASSWORD..."
$RAILWAY_CLI variables set POSTGRES_PASSWORD="$(openssl rand -base64 32)"

echo "Setting ENVIRONMENT..."
$RAILWAY_CLI variables set ENVIRONMENT="production"

echo "Setting DEBUG..."
$RAILWAY_CLI variables set DEBUG="false"

echo "Setting GHL_LEAD_CAPTURE_WEBHOOK (placeholder)..."
$RAILWAY_CLI variables set GHL_LEAD_CAPTURE_WEBHOOK="https://placeholder-get-from-brian.webhook.office.com"

echo "✅ Environment variables set"
echo ""

# Step 6: Deploy to Railway
echo "🚢 [6/7] Deploying to Railway..."
echo "This will:"
echo "  - Build all Docker images (AI agents + infrastructure)"
echo "  - Deploy 16 services"
echo "  - Set up networking and SSL"
echo "  - Provide public URLs"
echo ""
echo "⏱️  This takes 15-25 minutes. Railway handles everything."
echo ""
$RAILWAY_CLI up --detach

echo "✅ Deployment initiated"
echo ""

# Step 7: Get deployment status and URL
echo "🌐 [7/7] Getting deployment information..."
sleep 5  # Wait for deployment to register

echo ""
echo "================================================"
echo "✅ WARP COMPLETE: Railway Deployment Started!"
echo "================================================"
echo ""

echo "📊 Deployment Status:"
$RAILWAY_CLI status

echo ""
echo "🔗 Your URLs:"
echo "Run this to get your live URLs once deployment completes:"
echo "  railway status"
echo ""

echo "📝 Next Steps:"
echo "  1. Wait 15-25 minutes for Railway to build and deploy"
echo "  2. Monitor deployment: railway logs"
echo "  3. Get your URL: railway domain"
echo "  4. Test your endpoints: curl https://your-url.railway.app/health"
echo "  5. Update GHL webhook with your Railway URL"
echo ""

echo "💡 Useful Commands:"
echo "  railway logs              # View deployment logs"
echo "  railway logs -f           # Follow logs in real-time"
echo "  railway domain            # Get your public URL"
echo "  railway status            # Check deployment status"
echo "  railway variables         # View environment variables"
echo ""

echo "🎯 Once deployed, you'll have:"
echo "  ✅ All 16 services running"
echo "  ✅ Public HTTPS URLs"
echo "  ✅ SSL certificates (automatic)"
echo "  ✅ Monitoring dashboards"
echo "  ✅ Dual RAG system (Events + Gym)"
echo ""

echo "📚 Documentation:"
echo "  - QUICK_DEPLOY.md - Complete Railway guide"
echo "  - WHERE_WE_ARE.md - Project status"
echo "  - LOCAL_INFRASTRUCTURE_SUCCESS.md - Local testing"
echo ""
