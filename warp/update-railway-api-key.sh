#!/bin/bash

# WARP PROTOCOL: Update Railway OPENAI_API_KEY
# ==============================================

set -e

RAILWAY_CLI="/Users/noelpena/.npm-global/bin/railway"
NEW_API_KEY="YOUR_OPENAI_API_KEY_HERE"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔑 WARP PROTOCOL: Update Railway OpenAI API Key"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Check Railway CLI
if ! command -v $RAILWAY_CLI &> /dev/null; then
    echo "❌ Railway CLI not found at $RAILWAY_CLI"
    exit 1
fi

echo "[1/3] 📊 Current Railway status:"
$RAILWAY_CLI status
echo ""

echo "[2/3] 🔑 Updating OPENAI_API_KEY..."
echo ""
echo "⚠️  Railway CLI cannot set variables in non-interactive mode."
echo ""
echo "WARP SOLUTION: Copy-paste method"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📋 COPY THIS VALUE:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "$NEW_API_KEY"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo "[3/3] 📝 STEPS TO UPDATE IN RAILWAY DASHBOARD:"
echo ""
echo "1. Go to: https://railway.app/project/68f399d8-3794-4b03-b158-e77de07d3594"
echo ""
echo "2. Click 'Variables' tab"
echo ""
echo "3. Find 'OPENAI_API_KEY' in the list"
echo ""
echo "4. Click the Edit icon (pencil) next to OPENAI_API_KEY"
echo ""
echo "5. Paste the new key (copied above)"
echo ""
echo "6. Click 'Save' or press Enter"
echo ""
echo "7. Railway will auto-restart (takes ~30 seconds)"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ AFTER UPDATING:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Railway will automatically restart with the new API key."
echo ""
echo "Then test your agents:"
echo "  curl https://circuitos-production.up.railway.app/health"
echo ""
echo "Expected response:"
echo "  {\"status\": \"healthy\", \"agents\": {...}}"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔑 New API Key Ready to Paste"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
