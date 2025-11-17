# Circuit OS Landing Page - Live Access 🚀

## Your Circuit OS Landing Page is Ready!

The landing page has been integrated into your Flask server and is ready to deploy.

---

## Access From Your Phone 📱

### If You Have an Existing Railway Deployment:

1. **Find your Railway URL:**
   - Go to: https://railway.app
   - Sign in
   - Open your `Circuitos` or `MetroFlex` project
   - Look for your service domain (something like `your-app.up.railway.app`)

2. **Access Circuit OS:**
   ```
   https://your-railway-url.railway.app/circuit-os
   ```

3. **That's it!** The landing page will load with live metrics.

### If You DON'T Have a Railway Deployment Yet:

#### Option A: Quick Deploy via Railway Dashboard (Easiest - 5 minutes)

1. **Open Railway:** https://railway.app (on your phone)
2. **Create New Project** → **Deploy from GitHub**
3. **Select:**
   - Repo: `drive-brand-growth/Circuitos`
   - Branch: `claude/circuit-os-landing-018FK9MAjqdY1sB545jwPShK`
4. **Railway will auto-detect the Dockerfile and deploy!**
5. **Get your URL:**
   - Click on your deployment
   - Find the domain/URL
   - Add `/circuit-os` to the end
6. **Access:** `https://[your-url].railway.app/circuit-os`

#### Option B: Deploy Main Branch (Production Ready)

1. First, merge this branch to main (or deploy from this branch)
2. Railway will rebuild and deploy
3. Your Circuit OS page will be at: `/circuit-os`

---

## What You'll See

When you open the URL in your phone's browser:

✅ **Live Animated Metrics:**
- Pipeline Activated: 0% → 92%
- Meetings Booked: 0 → 18
- Revenue Recovered: $0 → $482,900

✅ **Interactive Features:**
- "Deploy Quick Switch" button
- "Enter Operator Mode" button (toggles signal green ↔ red)
- Expandable revenue details dropdown

✅ **Dark Industrial Theme:**
- Sleek operator interface
- Glowing signal indicators
- Smooth animations

---

## Endpoints Available

Once deployed, your server will have:

```
GET  /                    - API navigation/status
GET  /circuit-os          - Circuit OS Landing Page ⭐
GET  /health              - Health check
GET  /api/agents/status   - All AI agents status
POST /api/licensing/chat  - Licensing AI agent
POST /api/gym/chat        - Gym membership AI agent
POST /api/events/chat     - Events AI agent
```

---

## Environment Variables Needed

For Railway deployment, set these in your Railway dashboard:

**Required:**
```bash
OPENAI_API_KEY=your_openai_api_key_here
PORT=5001
```

**Optional:**
```bash
GHL_LEAD_CAPTURE_WEBHOOK=your_ghl_webhook_url
ENVIRONMENT=production
DEBUG=false
```

Railway will automatically set the `PORT` variable, but the app defaults to 5001 if not set.

---

## Deployment Status

✅ Code committed and pushed to branch: `claude/circuit-os-landing-018FK9MAjqdY1sB545jwPShK`

✅ Files ready:
- `/Active/metroflex-ghl-website/AI_Agent/circuit-os-landing.html`
- `/Active/metroflex-ghl-website/AI_Agent/unified_api_server.py` (updated)
- `/Dockerfile` (ready for Railway)

✅ Flask routes added:
- `GET /circuit-os` - Serves the landing page
- `GET /` - Navigation help

---

## Quick Test (If Deployed)

Once Railway is live, test in your phone browser:

```
1. Open: https://your-url.railway.app
   → Should show API navigation

2. Open: https://your-url.railway.app/circuit-os
   → Should show Circuit OS landing page with live metrics

3. Tap "Enter Operator Mode" button
   → Signal should turn from green to red

4. Tap "Show recovered revenue details"
   → Should expand to show breakdown
```

---

## Next Steps

### To Go Live Now:

1. **Via Railway Dashboard (Easiest):**
   - https://railway.app
   - New Project → GitHub repo
   - Select this branch
   - Deploy!
   - Access at: `https://[generated-url]/circuit-os`

2. **Via Railway CLI:**
   ```bash
   railway login
   railway link
   railway up
   railway domain  # Get your URL
   ```
   Then access: `https://[your-url]/circuit-os`

### To Merge to Production:

```bash
# Create PR from this branch to main
# Merge when ready
# Railway auto-deploys main branch
```

---

## Troubleshooting

**"Page not found" error:**
- Check Railway deployment logs
- Verify the service is running
- Make sure you added `/circuit-os` to the URL

**"File not found" error:**
- Verify `circuit-os-landing.html` is in the deployment
- Check Railway build logs
- Ensure Dockerfile copied AI_Agent directory

**Metrics not animating:**
- This is normal - check JavaScript console
- Try refreshing the page
- Works best on modern browsers

---

## Files You Can Download

If you want to test locally on your computer (not phone):

1. Download: `Active/circuit-os-landing/circuit-os-landing.html`
2. Open directly in any browser
3. No server needed!

---

## Support

- **Railway Docs:** https://docs.railway.app
- **Railway Dashboard:** https://railway.app
- **GitHub Repo:** https://github.com/drive-brand-growth/Circuitos

---

**Ready to go live?** Just deploy to Railway and access `/circuit-os` from your phone! 🎉
