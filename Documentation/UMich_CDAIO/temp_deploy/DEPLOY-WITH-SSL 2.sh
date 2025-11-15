#!/bin/bash

# Circuit OS - Deploy to GitHub with Automatic SSL
# This script pushes to GitHub and sets up HTTPS automatically

echo "🔒 Circuit OS - Secure Deployment to GitHub Pages"
echo "=================================================="
echo ""

# Check if gh CLI is installed
if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI not installed"
    echo ""
    echo "Please install it first:"
    echo "  brew install gh"
    echo ""
    echo "Or deploy manually:"
    echo "1. Create repo at: https://github.com/new"
    echo "2. Name: circuit-os-executive"
    echo "3. Set to PRIVATE"
    echo "4. Run:"
    echo "   git remote add origin https://github.com/YOUR-USERNAME/circuit-os-executive.git"
    echo "   git push -u origin main"
    echo "5. Enable GitHub Pages in Settings → Pages"
    echo "6. Check 'Enforce HTTPS' for SSL"
    exit 1
fi

# Login check
if ! gh auth status &> /dev/null; then
    echo "🔐 Logging into GitHub..."
    gh auth login
fi

echo "📦 Creating PRIVATE GitHub repository..."
echo ""

cd /Users/noelpena/Desktop/CircuitOS-DEPLOY-PACKAGE

# Create private repo and push
gh repo create circuit-os-executive \
    --private \
    --source=. \
    --remote=origin \
    --description="Circuit OS: Executive AI Platform with Vercel Design - PRIVATE" \
    --push

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Code pushed to GitHub!"
    echo ""
    echo "🔒 NEXT: Enable SSL/HTTPS"
    echo "=========================="
    echo ""
    echo "1. Go to repository settings:"
    echo "   https://github.com/$(gh api user --jq .login)/circuit-os-executive/settings/pages"
    echo ""
    echo "2. Under 'Source':"
    echo "   - Branch: main"
    echo "   - Folder: / (root)"
    echo "   - Click 'Save'"
    echo ""
    echo "3. Under 'Enforce HTTPS':"
    echo "   - Check the box: ✓ Enforce HTTPS"
    echo "   - SSL certificate issues automatically (2-3 minutes)"
    echo ""
    echo "4. Your HTTPS URLs will be:"
    echo "   https://$(gh api user --jq .login).github.io/circuit-os-executive/"
    echo "   https://$(gh api user --jq .login).github.io/circuit-os-executive/Dashboards/unified-demo-dashboard.html"
    echo ""
    echo "🔐 SSL Certificate: FREE Let's Encrypt (automatic renewal)"
    echo "🌍 Encryption: TLS 1.3, 256-bit"
    echo "🔒 Privacy: PRIVATE repository (only you can see code)"
    echo "🌐 Demo: PUBLIC (anyone can view via HTTPS URL)"
    echo ""
    echo "Want to open settings page now? (y/n)"
    read -r response
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        gh repo view --web
        echo ""
        echo "Navigate to: Settings → Pages → Enable & Enforce HTTPS"
    fi
else
    echo ""
    echo "❌ Failed to create repository"
    echo ""
    echo "Manual deployment steps:"
    echo "1. Go to: https://github.com/new"
    echo "2. Name: circuit-os-executive"
    echo "3. Set to PRIVATE"
    echo "4. Click 'Create repository'"
    echo "5. Run these commands:"
    echo ""
    echo "   git remote add origin https://github.com/YOUR-USERNAME/circuit-os-executive.git"
    echo "   git push -u origin main"
    echo ""
    echo "6. Enable GitHub Pages with HTTPS in Settings → Pages"
    echo ""
fi
