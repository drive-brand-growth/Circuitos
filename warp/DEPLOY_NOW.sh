#!/bin/bash
# WARP PROTOCOL: One-Command Railway Deployment
# Run this in your terminal: ./warp/DEPLOY_NOW.sh

set -e

export PATH="$HOME/.npm-global/bin:/usr/local/bin:$PATH"
RAILWAY_CLI="$HOME/.npm-global/bin/railway"

cd /Users/noelpena/Desktop/CircuitOS_Local_Complete_Package

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🚀 WARP PROTOCOL: Railway Deployment"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "This script will deploy your CircuitOS MetroFlex system to Railway."
echo "Total time: ~40 minutes"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Command 1: Login
echo "[1/5] 🔐 Login to Railway"
echo "────────────────────────────────────────────────────────────────────────"
echo ""
echo "Copy and paste this command in your terminal:"
echo ""
echo "  $RAILWAY_CLI login"
echo ""
echo "This will open your browser. Login with GitHub or email."
echo ""
echo "After logging in, press ENTER to continue..."
read -r

# Verify login
if ! $RAILWAY_CLI whoami &> /dev/null; then
    echo "❌ Not logged in. Please run the login command above first."
    exit 1
fi

USER=$($RAILWAY_CLI whoami)
echo "✅ Logged in as: $USER"
echo ""

# Command 2: Create project
echo "[2/5] 📂 Create Railway Project"
echo "────────────────────────────────────────────────────────────────────────"
echo ""

if $RAILWAY_CLI status &> /dev/null; then
    echo "✅ Already linked to a Railway project"
    $RAILWAY_CLI status
else
    echo "Running: $RAILWAY_CLI init"
    echo ""
    echo "When prompted:"
    echo "  - Project name: circuitos-metroflex (or press Enter)"
    echo "  - Template: Empty Project"
    echo ""

    $RAILWAY_CLI init

    echo "✅ Project created"
fi
echo ""

# Command 3: Link GitHub
echo "[3/5] 🔗 Link to GitHub Repository"
echo "────────────────────────────────────────────────────────────────────────"
echo ""
echo "Running: $RAILWAY_CLI link"
echo ""
echo "When prompted:"
echo "  - Repository: drive-brand-growth/Circuitos"
echo "  - Branch: main"
echo ""

$RAILWAY_CLI link

echo "✅ GitHub linked"
echo ""

# Command 4: Set environment variables
echo "[4/5] ⚙️  Set Environment Variables"
echo "────────────────────────────────────────────────────────────────────────"
echo ""

OPENAI_KEY=$(grep "^OPENAI_API_KEY=" .env | cut -d'=' -f2)

if [ -z "$OPENAI_KEY" ]; then
    echo "❌ OpenAI API key not found in .env file"
    exit 1
fi

echo "Setting 5 environment variables..."
echo ""

$RAILWAY_CLI variables set OPENAI_API_KEY="$OPENAI_KEY"
echo "✅ OPENAI_API_KEY set"

$RAILWAY_CLI variables set POSTGRES_PASSWORD="$(openssl rand -base64 32)"
echo "✅ POSTGRES_PASSWORD set"

$RAILWAY_CLI variables set ENVIRONMENT="production"
echo "✅ ENVIRONMENT set"

$RAILWAY_CLI variables set DEBUG="false"
echo "✅ DEBUG set"

$RAILWAY_CLI variables set GHL_LEAD_CAPTURE_WEBHOOK="https://placeholder-get-real-webhook-from-brian.com"
echo "✅ GHL_LEAD_CAPTURE_WEBHOOK set"

echo ""
echo "✅ All environment variables configured"
echo ""

# Command 5: Deploy
echo "[5/5] 🚢 Deploy to Railway"
echo "────────────────────────────────────────────────────────────────────────"
echo ""
echo "Running: $RAILWAY_CLI up"
echo ""
echo "This will:"
echo "  - Pull code from GitHub"
echo "  - Build all 16 Docker services"
echo "  - Deploy to production"
echo "  - Set up SSL and public URLs"
echo ""
echo "⏱️  Takes 20-25 minutes..."
echo ""

$RAILWAY_CLI up

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎉 DEPLOYMENT COMPLETE!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo "📊 Deployment Status:"
$RAILWAY_CLI status

echo ""
echo "🌐 Get your URLs:"
echo "  $RAILWAY_CLI domain"
echo ""

echo "📝 Next Steps:"
echo ""
echo "1. Test Events AI:"
echo "   curl -X POST https://your-url/api/events/chat -H 'Content-Type: application/json' -d '{\"query\":\"When is next event?\"}'"
echo ""
echo "2. Test Gym AI:"
echo "   curl -X POST https://your-url/api/gym/chat -H 'Content-Type: application/json' -d '{\"query\":\"Membership info?\"}'"
echo ""
echo "3. Access Grafana:"
echo "   https://your-url/grafana (admin/admin)"
echo ""
echo "4. Update GHL webhook:"
echo "   $RAILWAY_CLI variables set GHL_LEAD_CAPTURE_WEBHOOK='brian_webhook_url'"
echo ""
echo "✅ You're LIVE in production!"
echo ""
