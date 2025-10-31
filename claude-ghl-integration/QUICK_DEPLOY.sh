#!/bin/bash

# Claude GHL Integration - Quick Deploy Script
# This script helps you deploy to Vercel in minutes

set -e  # Exit on error

echo "🚀 Claude API + GHL Integration - Quick Deploy"
echo "================================================"
echo ""

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "📦 Vercel CLI not found. Installing..."
    npm install -g vercel
    echo "✅ Vercel CLI installed"
else
    echo "✅ Vercel CLI found"
fi

echo ""
echo "🔑 You'll need:"
echo "  1. Claude API key from: https://console.anthropic.com/settings/keys"
echo "  2. Vercel account (free): https://vercel.com/signup"
echo ""

read -p "Do you have your Claude API key ready? (y/n) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "⚠️  Please get your Claude API key first:"
    echo "   1. Go to https://console.anthropic.com"
    echo "   2. Sign up or log in"
    echo "   3. Navigate to Settings → API Keys"
    echo "   4. Create a new key"
    echo "   5. Run this script again"
    exit 1
fi

echo ""
echo "📤 Deploying to Vercel..."
echo ""

# Deploy to Vercel
vercel --prod

echo ""
echo "🔐 Now let's add your Claude API key..."
echo ""

# Add Claude API key
vercel env add CLAUDE_API_KEY production

echo ""
echo "🔄 Redeploying with environment variables..."
vercel --prod

echo ""
echo "✅ Deployment complete!"
echo ""
echo "📋 Next Steps:"
echo ""
echo "1. Copy your Vercel URL (shown above)"
echo "2. Test the API:"
echo ""
echo "   curl -X POST https://your-project.vercel.app/api/score-lead \\"
echo "     -H 'Content-Type: application/json' \\"
echo "     -d '{\"contact\": {\"first_name\": \"Test\"}}'"
echo ""
echo "3. Configure GHL Workflows (see README.md for details)"
echo ""
echo "4. Start sending leads to Claude API! 🎉"
echo ""
echo "📖 Full documentation: README.md"
echo "🔗 GHL Setup Guide: ../GHL-Setup/README.md"
echo ""
