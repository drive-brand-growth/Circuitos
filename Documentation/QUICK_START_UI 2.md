# 🚀 CircuitOS Training UI - Quick Start

**Get Your Training Running in 30 Seconds**

---

## Option 1: Automatic (Recommended)

### Run Local Server

```bash
cd /Users/noelpena/Desktop/CircuitOS_Local_Complete_Package
./serve-local.sh
```

**Then open in your browser**:
```
http://localhost:8000/Docs/html/ghl-circuitos-complete-training.html
```

Press `Ctrl+C` when done to stop the server.

---

## Option 2: Manual

```bash
cd /Users/noelpena/Desktop/CircuitOS_Local_Complete_Package
python3 -m http.server 8000
```

**Open**: http://localhost:8000/Docs/html/ghl-circuitos-complete-training.html

---

## Option 3: Direct File Open

Just double-click:
```
/Users/noelpena/Desktop/CircuitOS_Local_Complete_Package/Docs/html/ghl-circuitos-complete-training.html
```

**Note**: Some features may not work without a server (like localStorage). Use Option 1 or 2 for full functionality.

---

## 🌐 Deploy to GitHub Pages

### One Command

```bash
cd /Users/noelpena/Desktop/CircuitOS_Local_Complete_Package
./deploy-github.sh
```

Follow the prompts. You'll need:
1. GitHub account
2. Repository URL (the script will ask for it)

After deployment, enable GitHub Pages:
1. Go to your repo on GitHub
2. Settings → Pages
3. Source: `main` branch, `/docs` folder
4. Save

**Live URL**: `https://[your-username].github.io/[repo-name]/`

---

## ✅ What You'll See

- ✅ **Interactive Training UI** - Full CircuitOS training system
- ✅ **Navigation Sidebar** - Jump between modules
- ✅ **Progress Tracking** - LocalStorage saves your progress
- ✅ **Checklists** - Track completed tasks
- ✅ **Dark Theme** - Metroflex red/steel branding
- ✅ **Mobile Responsive** - Works on all devices

---

## 🎨 Files Included

- `serve-local.sh` - One-click local server
- `deploy-github.sh` - One-click GitHub Pages deployment
- `DEPLOYMENT_GUIDE.md` - Complete deployment documentation
- `Docs/html/ghl-circuitos-complete-training.html` - The training UI

---

## 🆘 Troubleshooting

**Python not found?**
```bash
# Install Python 3
brew install python3  # Mac
# or download from python.org
```

**Port 8000 in use?**
```bash
python3 -m http.server 8080
# Open: http://localhost:8080/Docs/html/ghl-circuitos-complete-training.html
```

**GitHub deployment issues?**
See `DEPLOYMENT_GUIDE.md` for detailed troubleshooting.

---

## 📖 Full Documentation

For complete deployment guide with customization, analytics, custom domains, and more:

**Read**: `DEPLOYMENT_GUIDE.md`

---

**That's it! Your training UI is now running.** 🎉
