#!/bin/bash

# Circuit OS - Push to GitHub Script
# This will create a PRIVATE repository and push your code

echo "🚀 Circuit OS - GitHub Deployment"
echo "=================================="
echo ""

# Check if gh CLI is installed
if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI not installed"
    echo ""
    echo "Please install it first:"
    echo "  brew install gh"
    echo ""
    echo "Or manually create repo at: https://github.com/new"
    echo "Then run:"
    echo "  git remote add origin https://github.com/YOUR-USERNAME/circuit-os-executive.git"
    echo "  git push -u origin main"
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

# Create private repo
gh repo create circuit-os-executive \
    --private \
    --source=. \
    --remote=origin \
    --description="Circuit OS: Dark Knight Executive AI Platform - PRIVATE" \
    --push

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ SUCCESS! Your code is now on GitHub (PRIVATE)"
    echo ""
    echo "📍 Repository URL:"
    gh repo view --web
    echo ""
    echo "🔒 Privacy: PRIVATE (only you can see it)"
    echo ""
else
    echo ""
    echo "❌ Failed to create repository"
    echo ""
    echo "Manual steps:"
    echo "1. Go to: https://github.com/new"
    echo "2. Name: circuit-os-executive"
    echo "3. Set to PRIVATE"
    echo "4. Click 'Create repository'"
    echo "5. Run these commands:"
    echo ""
    echo "   git remote add origin https://github.com/YOUR-USERNAME/circuit-os-executive.git"
    echo "   git push -u origin main"
    echo ""
fi
