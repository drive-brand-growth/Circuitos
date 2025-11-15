# GitHub Deployment Instructions

Follow these steps to push the UMich CDAIO Mobile Training Platform to GitHub and enable GitHub Pages.

## Step 1: Create GitHub Repository

1. Go to [GitHub](https://github.com/new)
2. Repository name: `UMich-CDAIO-Mobile`
3. Description: `Mobile-optimized audio training platform for University of Michigan Chief Data & AI Officer Professional Certificate`
4. Visibility: **Public** (required for free GitHub Pages)
5. Do NOT initialize with README (we already have one)
6. Click "Create repository"

## Step 2: Push to GitHub

Run these commands in Terminal:

```bash
cd /Users/noelpena/Desktop/CircuitOS_Local_Complete_Package/UMich_CDAIO

# Add GitHub remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/UMich-CDAIO-Mobile.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Step 3: Enable GitHub Pages

1. Go to your repository on GitHub
2. Click "Settings" tab
3. Click "Pages" in the left sidebar
4. Under "Source":
   - Branch: **main**
   - Folder: **/ (root)**
5. Click "Save"

## Step 4: Wait for Deployment

- GitHub Pages will build your site (takes 1-2 minutes)
- Your site will be available at: `https://YOUR_USERNAME.github.io/UMich-CDAIO-Mobile/`
- You'll see a green checkmark when it's ready

## Step 5: Access on iPhone

### Option A: Safari Bookmark
1. Open the URL in Safari on your iPhone
2. Tap the "Share" button
3. Tap "Add to Home Screen"
4. Name it "UMich CDAIO Training"
5. The icon will appear on your home screen

### Option B: Direct Link
1. Open Safari on iPhone
2. Navigate to: `https://YOUR_USERNAME.github.io/UMich-CDAIO-Mobile/`
3. Bookmark for easy access

## Features on iPhone

- **Full-screen mode** when added to home screen
- **Offline support** after first load
- **Progress tracking** saves to device
- **Audio controls** optimized for touch
- **Responsive design** fits all screen sizes

## Updating the Platform

To make changes and update:

```bash
cd /Users/noelpena/Desktop/CircuitOS_Local_Complete_Package/UMich_CDAIO

# Make your changes to index.html or other files

# Commit and push
git add -A
git commit -m "Update: description of changes"
git push origin main
```

GitHub Pages will automatically rebuild and deploy within 1-2 minutes.

## Troubleshooting

### Pages not showing up
- Check Settings → Pages → Make sure it's enabled
- Verify branch is set to "main" and folder is "/ (root)"
- Wait 2-3 minutes for initial build

### 404 Error
- Ensure index.html is in the root directory (it is)
- Check that repository is public
- Clear browser cache

### Audio not working on iPhone
- Ensure you're using Safari (not Chrome)
- Tap play button (iOS requires user interaction)
- Check device is not on silent mode

## Current Repository Status

✅ Git repository initialized
✅ All files committed
✅ index.html in root directory (required for GitHub Pages)
✅ README.md included
✅ Ready to push to GitHub

**Next step:** Create the GitHub repository and run the push commands above!

---

**Questions?**
- GitHub Pages docs: https://docs.github.com/pages
- Contact support: support@github.com
