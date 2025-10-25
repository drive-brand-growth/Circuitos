#!/bin/bash

# Circuit OS - GitHub Push Script
# This script will push your code to GitHub

echo "🚀 Circuit OS - GitHub Push Script"
echo "===================================="
echo ""

# Ask for GitHub username
read -p "Enter your GitHub username: " GITHUB_USERNAME

if [ -z "$GITHUB_USERNAME" ]; then
    echo "❌ GitHub username required"
    exit 1
fi

echo ""
echo "GitHub username: $GITHUB_USERNAME"
echo "Repository will be created at: https://github.com/$GITHUB_USERNAME/CircuitOS"
echo ""

# Set git config
echo "Setting up git configuration..."
git config --global user.name "Noel Pena"
git config --global user.email "noel@circuitos.com"

# Navigate to project
cd /Users/noelpena/Desktop/CircuitOS-DEPLOY-PACKAGE

# Check current status
echo ""
echo "Current git status:"
git log --oneline -3
echo ""

# Option 1: Create repo via web, then push
echo "📋 OPTION 1: Manual GitHub Repo Creation (Recommended)"
echo "=================================================="
echo ""
echo "1. Go to: https://github.com/new"
echo "2. Repository name: CircuitOS"
echo "3. Description: Circuit OS - AI-Powered Lead Qualification Platform"
echo "4. Visibility: Private (or Public)"
echo "5. DO NOT initialize with README"
echo "6. Click 'Create repository'"
echo ""
read -p "Press ENTER after you've created the repository..."
echo ""

# Add remote
echo "Adding GitHub remote..."
git remote remove origin 2>/dev/null
git remote add origin https://github.com/$GITHUB_USERNAME/CircuitOS.git

if [ $? -ne 0 ]; then
    echo "❌ Failed to add remote"
    exit 1
fi

echo "✅ Remote added"
echo ""

# Push to GitHub
echo "🚀 Pushing to GitHub..."
echo "   (You may be prompted for your GitHub credentials)"
echo ""

git push -u origin main

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Push failed. This might be because:"
    echo "   1. Credentials needed (GitHub will prompt)"
    echo "   2. Repository doesn't exist yet"
    echo "   3. Branch name mismatch"
    echo ""
    echo "Try this command manually:"
    echo "   git push -u origin main"
    echo ""
    echo "Or if your default branch is 'master':"
    echo "   git branch -M main"
    echo "   git push -u origin main"
    exit 1
fi

echo ""
echo "✅ Successfully pushed to GitHub!"
echo ""
echo "🔗 Your repository: https://github.com/$GITHUB_USERNAME/CircuitOS"
echo ""
echo "📋 Next steps:"
echo "1. Visit your repo: https://github.com/$GITHUB_USERNAME/CircuitOS"
echo "2. Enable GitHub Pages (Settings → Pages → Source: main branch)"
echo "3. Your site will be live at: https://$GITHUB_USERNAME.github.io/CircuitOS/"
echo ""
echo "🎉 All done!"
