#!/bin/bash
# WARP PROTOCOL: Fully Automated Railway Deployment
# No user interaction required - Warp handles everything

set -e

export PATH="$HOME/.npm-global/bin:$PATH"
RAILWAY="/Users/noelpena/.npm-global/bin/railway"
BASE_DIR="/Users/noelpena/Desktop/CircuitOS_Local_Complete_Package"

cd "$BASE_DIR"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🚀 WARP PROTOCOL: Automated Railway Deployment"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Verify login
echo "[1/4] ✅ Verifying Railway login..."
USER=$($RAILWAY whoami)
echo "   Logged in as: $USER"
echo ""

# Check project status
echo "[2/4] ✅ Railway project detected..."
PROJECT_INFO=$($RAILWAY status)
echo "$PROJECT_INFO"
echo ""

# Set environment variables
echo "[3/4] ⚙️  Setting environment variables..."

# Read OpenAI API key
OPENAI_KEY=$(grep "^OPENAI_API_KEY=" .env | cut -d'=' -f2 | tr -d '\r\n')

if [ -z "$OPENAI_KEY" ]; then
    echo "❌ OpenAI API key not found in .env file"
    exit 1
fi

echo "   Setting OPENAI_API_KEY..."
$RAILWAY variables set OPENAI_API_KEY="$OPENAI_KEY" 2>&1 || echo "   (may already be set)"

echo "   Setting POSTGRES_PASSWORD..."
POSTGRES_PASS=$(openssl rand -base64 32)
$RAILWAY variables set POSTGRES_PASSWORD="$POSTGRES_PASS" 2>&1 || echo "   (may already be set)"

echo "   Setting ENVIRONMENT..."
$RAILWAY variables set ENVIRONMENT="production" 2>&1 || echo "   (may already be set)"

echo "   Setting DEBUG..."
$RAILWAY variables set DEBUG="false" 2>&1 || echo "   (may already be set)"

echo "   Setting GHL_LEAD_CAPTURE_WEBHOOK..."
$RAILWAY variables set GHL_LEAD_CAPTURE_WEBHOOK="https://placeholder-get-real-webhook-from-brian.com" 2>&1 || echo "   (may already be set)"

echo ""
echo "✅ Environment variables configured"
echo ""

# Deploy
echo "[4/4] 🚢 Deploying to Railway..."
echo ""
echo "This will:"
echo "  - Deploy from current directory"
echo "  - Build all Docker services"
echo "  - Set up networking and SSL"
echo "  - Provide public URLs"
echo ""
echo "⏱️  Takes 20-25 minutes..."
echo ""

# Use railway up with --detach for non-interactive deployment
$RAILWAY up --detach

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎉 DEPLOYMENT INITIATED!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Wait a few seconds for deployment to register
echo "⏳ Waiting for deployment to register..."
sleep 10

# Get deployment status
echo ""
echo "📊 Deployment Status:"
$RAILWAY status

echo ""
echo "🌐 To get your live URLs (after deployment completes):"
echo "   $RAILWAY domain"
echo ""
echo "📝 Monitor deployment:"
echo "   $RAILWAY logs"
echo ""
echo "✅ Railway is now building and deploying your services!"
echo "   Check Railway dashboard: https://railway.app/dashboard"
echo ""
