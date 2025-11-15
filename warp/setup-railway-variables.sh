#!/bin/bash

# WARP PROTOCOL: Setup Railway Environment Variables
# ================================================

set -e

RAILWAY_CLI="/Users/noelpena/.npm-global/bin/railway"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🚀 WARP PROTOCOL: Railway Environment Variables Setup"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Check Railway CLI
if ! command -v $RAILWAY_CLI &> /dev/null; then
    echo "❌ Railway CLI not found"
    exit 1
fi

echo "[1/4] 📊 Checking current Railway status..."
$RAILWAY_CLI status
echo ""

echo "[2/4] 🔑 Environment variables to add:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "1. OPENAI_API_KEY"
echo "   Value: YOUR_OPENAI_API_KEY_HERE"
echo ""
echo "2. GHL_LEAD_CAPTURE_WEBHOOK"
echo "   Value: https://placeholder.com/webhook"
echo "   (Update this after creating GHL webhook)"
echo ""
echo "3. PORT"
echo "   Value: 5001"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo "[3/4] ⚙️  Railway variables cannot be set via CLI in non-interactive mode."
echo ""
echo "WARP SOLUTION: Copy-paste variables via Railway dashboard"
echo ""
echo "📋 Variables file created at:"
echo "   /tmp/railway_env_setup.txt"
echo ""
echo "You can also use Raw Editor in Railway:"
echo ""
echo "1. In Railway dashboard, click 'Raw Editor'"
echo "2. Paste this:"
echo ""
cat << 'ENVVARS'
OPENAI_API_KEY=YOUR_OPENAI_API_KEY_HERE
GHL_LEAD_CAPTURE_WEBHOOK=https://placeholder.com/webhook
PORT=5001
ENVVARS
echo ""
echo "3. Save and Railway will auto-restart"
echo ""

echo "[4/4] 🎯 After adding variables:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Railway will auto-restart (2-3 minutes)"
echo "✅ Check deployment: Railway dashboard → Deployments tab"
echo "✅ Get your URL: Railway dashboard → Settings → Domains"
echo "✅ Test health: curl https://your-url/health"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🚀 WARP PROTOCOL: Variables Ready to Add"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "USE RAW EDITOR (FASTEST):"
echo "1. Railway dashboard → Variables tab → Raw Editor"
echo "2. Copy the 3 lines above"
echo "3. Paste and save"
echo ""
echo "OR USE + NEW VARIABLE (ONE BY ONE):"
echo "1. Click + New Variable"
echo "2. Add each variable manually"
echo ""
echo "THEN:"
echo "⏳ Wait 2-3 minutes for restart"
echo "✅ Check Deployments tab for '✅ Success'"
echo "🌐 Get your public URL from Settings → Domains"
echo "🧪 Test: curl https://your-url/health"
echo ""
