# Vercel Deployment Guide - 5 Minutes to Production
## Deploy Your Dual-Path Lead System to Vercel

**Time Required:** 5 minutes
**Cost:** $0/month (Hobby plan)
**Prerequisites:** GitHub account (you already have this)

---

## 🚀 Step 1: Create Vercel Account (2 minutes)

### A. Sign Up

1. **Go to:** https://vercel.com/signup
2. **Click:** "Continue with GitHub"
3. **Authorize:** Vercel to access your GitHub
4. **Done!** You're on the free Hobby plan

**What you get FREE:**
- ✅ 100GB bandwidth/month
- ✅ Unlimited serverless function executions
- ✅ Automatic HTTPS
- ✅ Custom domains (free)
- ✅ Edge network (global CDN)

---

## 🔗 Step 2: Import Your GitHub Repo (1 minute)

### A. Add New Project

1. **Vercel Dashboard:** Click "Add New..." → "Project"
2. **Import Git Repository:** Find `drive-brand-growth/Circuitos`
3. **Click:** "Import"

### B. Configure Project (Auto-detected)

Vercel will auto-detect:
- ✅ Framework: Node.js
- ✅ Build Command: (none needed)
- ✅ Output Directory: (none needed)
- ✅ Install Command: `npm install`

**Just click "Deploy"** (we'll add environment variables next)

⏳ **Wait 30-60 seconds** while Vercel builds...

### C. First Deployment

You'll see:
```
Building...
▲ Vercel
✓ Build completed
✓ Deployment ready
```

**Result:** Your APIs are live at:
```
https://circuitos-[random].vercel.app/api/virtual-lpr
https://circuitos-[random].vercel.app/api/copywriter
https://circuitos-[random].vercel.app/api/lead-router
https://circuitos-[random].vercel.app/api/instantly-webhook
https://circuitos-[random].vercel.app/api/test-lead-validation
```

**BUT** - It won't work yet (missing environment variables). Let's fix that!

---

## 🔐 Step 3: Add Environment Variables (2 minutes)

### A. Get Your Claude API Key

If you don't have one yet:
1. Go to: https://console.anthropic.com/
2. Settings → API Keys
3. Create Key → Copy it (starts with `sk-ant-api03-`)

### B. Add to Vercel

1. **Vercel Dashboard:** Your project → "Settings" tab
2. **Left sidebar:** Click "Environment Variables"
3. **Add each variable:**

#### Required Variables:

| Variable Name | Value | Where to Get It |
|--------------|-------|-----------------|
| `ANTHROPIC_API_KEY` | `sk-ant-api03-...` | https://console.anthropic.com/ |

#### Optional Variables (add these for better functionality):

| Variable Name | Example Value | Purpose |
|--------------|---------------|---------|
| `GOOGLE_MAPS_API_KEY` | `AIza...` | Distance calculation (optional, falls back to Haversine) |
| `BUSINESS_NAME` | `"MetroFlex Gym"` | Your business name |
| `BUSINESS_LAT` | `32.7357` | Your business latitude |
| `BUSINESS_LNG` | `-97.1081` | Your business longitude |
| `BUSINESS_CITY` | `"Arlington"` | Your city |
| `BUSINESS_STATE` | `"TX"` | Your state |
| `BUSINESS_TYPE` | `"Hardcore powerlifting gym"` | Business type |

### C. How to Add Variables

For each variable:
```
1. Click "Add New"
2. Name: ANTHROPIC_API_KEY
3. Value: sk-ant-api03-your-actual-key
4. Environment: Production (checked)
5. Click "Save"
```

**Repeat for all variables.**

---

## 🔄 Step 4: Redeploy with Environment Variables (30 seconds)

After adding variables:

1. **Go to:** "Deployments" tab
2. **Find:** Latest deployment (top of list)
3. **Click:** Three dots (...) → "Redeploy"
4. **Confirm:** "Redeploy"

⏳ **Wait 30 seconds...**

✅ **Done!** Your APIs are now live WITH environment variables!

---

## ✅ Step 5: Test Your Deployment (1 minute)

### A. Open Test Console

Go to: `https://your-project.vercel.app/api/test-lead-validation`

You should see a beautiful test console with 3 scenarios.

### B. Run Tests

**Test 1: High-Intent GMB**
- Click "Run Test"
- Should return: ✅ LEAD QUALIFIED, Score: 85+

**Test 2: Website Visit**
- Click "Run Test"
- Should return: ✅ LEAD QUALIFIED, Score: 60-80

**Test 3: Low Quality**
- Click "Run Test"
- Should return: ❌ LEAD NOT QUALIFIED, Score: <40

### C. If Tests Fail

**Check:**
1. Environment variables are set (Settings → Environment Variables)
2. ANTHROPIC_API_KEY is correct (no typos)
3. Redeployed after adding variables

**View Logs:**
1. Deployments → Latest → "Functions" tab
2. Click on a function (e.g., `api/virtual-lpr.js`)
3. See real-time logs

---

## 🎯 Your Live API Endpoints

After deployment, your endpoints are:

### 1. Virtual LPR (Lead Validation)
```
POST https://your-project.vercel.app/api/virtual-lpr

Body:
{
  "signal_type": "website_visit",
  "signal_data": { ... },
  "business": { ... }
}
```

### 2. Master Copywriter (Copy Generation)
```
POST https://your-project.vercel.app/api/copywriter

Body:
{
  "contact": { ... },
  "channel": "email",
  "awareness_level": "Product Aware",
  "lead_source": "website_traffic",
  "business": { ... }
}
```

### 3. Lead Router (Source Detection)
```
POST https://your-project.vercel.app/api/lead-router

Body:
{
  "contact": { ... },
  "source_data": { ... }
}
```

### 4. Instantly.ai Webhook (Reply Handler)
```
POST https://your-project.vercel.app/api/instantly-webhook

Body:
{
  "event_type": "reply",
  "lead_email": "...",
  "reply_text": "...",
  ...
}
```

### 5. Test Console (Interactive Testing)
```
GET https://your-project.vercel.app/api/test-lead-validation
```

---

## 🔗 Step 6: Configure Webhooks (5 minutes)

### A. Instantly.ai Webhook

1. **Instantly.ai Dashboard:** Settings → Webhooks
2. **Add Webhook URL:** `https://your-project.vercel.app/api/instantly-webhook`
3. **Select Events:**
   - ✅ Email Reply
   - ✅ Email Opened
   - ✅ Link Clicked
4. **Save**

**Test:**
- Send test email via Instantly
- Reply to it
- Check Vercel logs (should see webhook received)

### B. GoHighLevel Webhooks

**For Virtual LPR (Path 2):**

In GHL Workflow:
```
Action: Send Outbound Webhook
URL: https://your-project.vercel.app/api/virtual-lpr
Method: POST
Body: { signal_type, signal_data, business }
```

**For Master Copywriter:**

In GHL Workflow:
```
Action: Send Outbound Webhook
URL: https://your-project.vercel.app/api/copywriter
Method: POST
Body: { contact, channel, awareness_level, lead_source, business }
```

---

## 🎨 Step 7: Custom Domain (Optional - 2 minutes)

Want to use your own domain instead of `*.vercel.app`?

### A. Add Domain

1. **Settings → Domains**
2. **Add:** `api.yourdomain.com`
3. **Vercel gives you DNS records**
4. **Add records to your DNS provider** (Cloudflare, Namecheap, etc.)
5. **Wait 5 minutes** for DNS propagation

**Result:**
```
https://api.yourdomain.com/api/virtual-lpr
https://api.yourdomain.com/api/copywriter
```

### B. Update Webhooks

Update webhook URLs in:
- Instantly.ai → New domain
- GHL Workflows → New domain

---

## 📊 Step 8: Monitor Your APIs (Ongoing)

### A. View Analytics

**Vercel Dashboard → Analytics:**
- Request count per endpoint
- Response times
- Error rates
- Geographic distribution

### B. View Logs

**Deployments → Latest → Functions:**
- Real-time function logs
- See every API call
- Debug errors quickly

### C. View Performance

**Analytics → Functions:**
- Execution time per endpoint
- Cold start performance
- Bandwidth usage

---

## 🔄 Auto-Deploy on Git Push

**Already configured!** Now when you:

1. Make code changes locally
2. `git commit -m "Update..."`
3. `git push`

**Vercel automatically:**
1. Detects the push
2. Builds your project
3. Deploys to production
4. Updates all endpoints

**No manual deploy needed!**

### Preview Deployments

Every branch gets its own preview URL:
```
Branch: feature/new-copywriter
Preview: https://circuitos-git-feature-new-copywriter.vercel.app
```

**Perfect for testing before merging to main!**

---

## 🆘 Troubleshooting

### Issue 1: "Module not found: @anthropic-ai/sdk"

**Solution:**
```bash
# Locally run:
npm install

# Then commit and push:
git add package.json package-lock.json
git commit -m "Update dependencies"
git push

# Vercel will redeploy with correct dependencies
```

### Issue 2: "Environment variable undefined"

**Solution:**
1. Settings → Environment Variables
2. Check ANTHROPIC_API_KEY is set
3. Check it's enabled for "Production"
4. Redeploy

### Issue 3: API returns 500 error

**Solution:**
1. Deployments → Latest → Functions
2. Click on failing function
3. Read error logs
4. Usually: missing environment variable or typo in API key

### Issue 4: Webhook not receiving data

**Solution:**
1. Check webhook URL is correct (no typos)
2. Check Vercel logs (Deployments → Functions)
3. Test with Postman/curl first
4. Verify webhook source is sending correct format

---

## 💰 Cost Monitoring

### Free Tier Limits (Hobby Plan):

```
✅ 100GB Bandwidth/month
✅ 100GB-Hours Serverless Function Execution
✅ 1000 builds/month
✅ Unlimited requests
```

### When You'll Hit Limits:

**Bandwidth (100GB):**
- Average API response: 5KB
- 100GB = 20,000,000 API calls/month
- **You'll be fine for months**

**Function Execution (100GB-Hours):**
- Average execution: 500ms
- 100GB-hours = ~720,000 executions
- **You'll be fine**

### If You Hit Limits:

Upgrade to Pro ($20/mo):
- 1TB bandwidth
- 1000GB-hours execution
- Priority support

---

## ✅ Deployment Checklist

Before going live with real leads:

- [ ] Vercel account created
- [ ] GitHub repo connected
- [ ] Environment variables added (at least ANTHROPIC_API_KEY)
- [ ] Initial deployment successful
- [ ] Test console working (all 3 tests pass)
- [ ] Instantly.ai webhook configured
- [ ] GHL workflows updated with Vercel URLs
- [ ] Test cold email reply → webhook → GHL contact created
- [ ] Test website visitor → Virtual LPR → GHL contact created
- [ ] Custom domain configured (optional)
- [ ] Monitoring/alerts set up (optional)

---

## 🚀 You're Live!

Your production lead validation system is now running on Vercel:

✅ **Virtual LPR** - Validates 100+ leads/day with $0 infrastructure
✅ **Master Copywriter** - Generates world-class copy in 4 frameworks
✅ **Dual-Path Routing** - Cold vs Warm leads handled differently
✅ **Instantly.ai Integration** - Qualifies cold email replies
✅ **Auto-Scaling** - Handles 1000s of leads/day
✅ **99.9% Uptime** - Production-ready reliability

**Total Monthly Cost:** $0-10 (just Claude API usage)

---

## 📞 Next Steps

1. **Send test leads** through both paths (cold email + website)
2. **Monitor Vercel logs** for first week
3. **Adjust thresholds** if needed (qualification scores)
4. **Scale up** Instantly campaigns
5. **Track metrics** (qualification rate, conversion rate)

---

## 🎯 Quick Reference

**Your Vercel Project URL:**
```
https://your-project.vercel.app
```

**Test Console:**
```
https://your-project.vercel.app/api/test-lead-validation
```

**API Endpoints:**
```
/api/virtual-lpr
/api/copywriter
/api/lead-router
/api/instantly-webhook
```

**Dashboard:**
```
https://vercel.com/your-username/circuitos
```

---

**© 2025 CircuitOS™**
**Deployed on Vercel - Production Ready**
**Cost: $0/month infrastructure + ~$0.01 per lead validation**

🚀 **You're live!**
