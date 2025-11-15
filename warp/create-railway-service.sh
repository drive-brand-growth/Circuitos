#!/bin/bash

# WARP PROTOCOL: Create Railway Service
# ================================================

set -e

RAILWAY_CLI="/Users/noelpena/.npm-global/bin/railway"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🚀 WARP PROTOCOL: Railway Service Setup"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Step 1: Check Railway status
echo "[1/3] 📊 Checking Railway project..."
$RAILWAY_CLI status
echo ""

# Step 2: Create service via Railway dashboard instructions
echo "[2/3] 🎯 Creating Railway service..."
echo ""
echo "⚠️  Railway service creation requires the dashboard:"
echo ""
echo "1. Open: https://railway.app/project/d53017e3-f123-4cb0-86f3-c649455b9495"
echo "2. Click '+ New Service'"
echo "3. Select 'Empty Service'"
echo "4. Name it: 'metroflex-ai-agent'"
echo "5. Click 'Deploy'"
echo ""
echo "Once created, the deployment will automatically build from your latest push."
echo ""
read -p "Press ENTER after you've created the service in Railway dashboard..."
echo ""

# Step 3: Link the service locally
echo "[3/3] 🔗 Link service locally..."
echo ""
echo "Run this command to link your local project:"
echo ""
echo "  cd /Users/noelpena/Desktop/CircuitOS_Local_Complete_Package"
echo "  $RAILWAY_CLI link"
echo ""
echo "Select:"
echo "  - Project: remarkable-manifestation"
echo "  - Environment: production"
echo "  - Service: metroflex-ai-agent"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ SERVICE SETUP COMPLETE!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🎉 Next steps:"
echo "   1. Wait for deployment to complete (20-25 min)"
echo "   2. Get your live URL: $RAILWAY_CLI domain"
echo "   3. Set up GHL webhook (see GHL_WEBHOOK_SETUP_NOW.md)"
echo ""
