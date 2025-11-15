#!/bin/bash

# Quick Deploy Script for UMich CDAIO Mobile Platform
# Run this to push to GitHub and enable GitHub Pages

echo "🚀 UMich CDAIO - Quick Deploy to GitHub"
echo "========================================"
echo ""

# Check if we have a remote
if ! git remote | grep -q origin; then
    echo "📝 No GitHub remote found. Let's set it up..."
    echo ""
    echo "Please enter your GitHub username:"
    read github_username

    echo ""
    echo "Creating remote URL: https://github.com/$github_username/UMich-CDAIO-Mobile.git"
    git remote add origin "https://github.com/$github_username/UMich-CDAIO-Mobile.git"
    echo "✅ Remote added!"
else
    echo "✅ GitHub remote already configured"
fi

echo ""
echo "📤 Pushing to GitHub..."
git branch -M main
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Successfully pushed to GitHub!"
    echo ""
    echo "📱 Next steps:"
    echo "1. Go to your repository on GitHub"
    echo "2. Click 'Settings' → 'Pages'"
    echo "3. Set Source to: main branch, / (root) folder"
    echo "4. Click 'Save'"
    echo "5. Wait 1-2 minutes for deployment"
    echo "6. Your site will be live at:"
    echo "   https://$github_username.github.io/UMich-CDAIO-Mobile/"
    echo ""
    echo "📲 On your iPhone:"
    echo "1. Open that URL in Safari"
    echo "2. Tap Share → Add to Home Screen"
    echo "3. Launch from home screen"
    echo ""
    echo "🎓 Enjoy your mobile CDAIO training!"
else
    echo ""
    echo "❌ Push failed. You may need to:"
    echo "1. Create the repository on GitHub first"
    echo "2. Make sure you're logged in: gh auth login"
    echo "3. Or manually create at: https://github.com/new"
fi
