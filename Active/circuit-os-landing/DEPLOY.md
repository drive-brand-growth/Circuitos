# Deploy Circuit OS Landing Page to Railway

## Quick Deploy (From Your Phone)

### Option 1: Railway Dashboard (Easiest)

1. Open Railway: https://railway.app
2. Sign in to your account
3. Click **"New Project"**
4. Select **"Deploy from GitHub repo"**
5. Choose: `drive-brand-growth/Circuitos`
6. Select branch: `claude/circuit-os-landing-018FK9MAjqdY1sB545jwPShK`
7. Set **Root Directory**: `Active/circuit-os-landing`
8. Railway will auto-detect the Dockerfile and deploy!
9. Your site will be live at: `https://[your-app].railway.app`

### Option 2: Railway CLI (If you have it)

```bash
cd Active/circuit-os-landing
railway login
railway link
railway up
```

## What You'll Get

Once deployed, you'll have a live Circuit OS landing page with:

- ✅ Live animated metrics
- ✅ Interactive operator mode toggle
- ✅ Expandable revenue details
- ✅ Public HTTPS URL
- ✅ Auto-deployed from GitHub

## Files Ready for Deployment

```
Active/circuit-os-landing/
├── index.html           # Main landing page
├── Dockerfile           # Railway deployment config
├── railway.json         # Railway build settings
└── .railwayignore      # Files to exclude
```

## Environment Variables

No environment variables needed! This is a simple static site.

## Viewing Your Site

After deployment completes (usually ~2 minutes):
- Click the generated Railway URL
- Site opens in your phone's browser
- Watch the live metrics animate!

---

**Need help?** Check Railway logs in the dashboard or contact support.

**Cost:** Railway free tier includes 500 hours/month - more than enough for this demo.
