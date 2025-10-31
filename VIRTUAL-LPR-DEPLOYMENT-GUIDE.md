# Virtual LPR™ Deployment Guide
## Complete Setup for Lead Validation with FREE MCP Servers

**Version:** 2.0.0
**Date:** October 31, 2025
**Cost:** $0/month infrastructure + ~$0.01 per lead validation

---

## 🎯 What You Just Got

A **complete lead validation system** that:
- ✅ Validates leads using FREE MCP servers (Google Maps, Census Bureau)
- ✅ Scores leads 0-100 based on Fit + Intent + Timing
- ✅ Enriches with demographics (income, age, education)
- ✅ Calculates distance from your business
- ✅ Integrates with GoHighLevel workflows
- ✅ Costs $0/month infrastructure (only Claude API ~$0.01 per validation)

---

## 📁 What Was Created

```
Circuitos/
├── api/
│   ├── virtual-lpr.js              # Main lead validation endpoint
│   └── test-lead-validation.js     # Test console UI
├── lib/
│   └── mcps/
│       ├── google-maps.js          # Google Maps MCP integration
│       └── census-data.js          # Census Bureau MCP integration
├── .env.example                     # Environment variables template
└── VIRTUAL-LPR-DEPLOYMENT-GUIDE.md # This file
```

---

## 🚀 Quick Start (30 Minutes)

### Step 1: Get API Keys (15 minutes)

#### A. Claude API Key (REQUIRED)
```bash
# Get your key from: https://console.anthropic.com/
# Cost: ~$0.01 per lead validation

1. Go to https://console.anthropic.com/
2. Click "API Keys"
3. Create new key
4. Copy key (starts with sk-ant-api03-)
```

#### B. Google Maps API Key (OPTIONAL - for better distance calculation)
```bash
# Get FREE key from: https://console.cloud.google.com/
# Free tier: $200/month credit = ~28,000 API calls

1. Go to https://console.cloud.google.com/
2. Create new project: "CircuitOS Virtual LPR"
3. Enable APIs:
   - Maps JavaScript API
   - Places API
   - Distance Matrix API
   - Geocoding API
4. Create credentials → API key
5. Copy key (starts with AIza...)
```

**Note:** If you skip Google Maps API, the system will use Haversine formula (less accurate but FREE).

---

### Step 2: Set Environment Variables (5 minutes)

#### Option A: Using Vercel Dashboard (Recommended)

```bash
# 1. Go to your Vercel project dashboard
# 2. Settings → Environment Variables
# 3. Add these variables:

ANTHROPIC_API_KEY = sk-ant-api03-your-key-here
GOOGLE_MAPS_API_KEY = AIza-your-key-here (optional)

# Business configuration
BUSINESS_NAME = "MetroFlex Gym"
BUSINESS_LAT = 32.7357
BUSINESS_LNG = -97.1081
BUSINESS_CITY = "Arlington"
BUSINESS_STATE = "TX"
BUSINESS_TYPE = "Hardcore powerlifting/strongman gym"
BUSINESS_TARGET_RADIUS_MILES = 10
BUSINESS_MAX_DISTANCE_MILES = 25
```

#### Option B: Using .env File (Local Development)

```bash
# Copy template
cp .env.example .env

# Edit .env with your API keys
nano .env
```

---

### Step 3: Install Dependencies (2 minutes)

The API is designed to work with Vercel serverless functions, which auto-installs dependencies. However, if you want to test locally:

```bash
# Install Vercel CLI (if not already installed)
npm i -g vercel

# Install dependencies
npm install @anthropic-ai/sdk
```

---

### Step 4: Deploy to Vercel (5 minutes)

```bash
# If first time deploying
vercel deploy --prod

# If already deployed, just push to GitHub
git add .
git commit -m "Add: Virtual LPR lead validation system"
git push origin main
# Vercel will auto-deploy
```

---

### Step 5: Test the System (5 minutes)

#### A. Open Test Console

```bash
# After deployment, visit:
https://your-project.vercel.app/api/test-lead-validation
```

You'll see 3 test scenarios:
1. ✅ **High-Intent GMB** - User clicked directions (should qualify)
2. 📊 **Website Visit** - User browsed pricing (should qualify)
3. ❌ **Low Quality** - Far away, short visit (should NOT qualify)

#### B. Test Each Scenario

Click "Run Test" on each card and verify:
- High-intent leads score 70-100
- Medium leads score 40-69
- Low leads score 0-39

---

## 🔗 GHL Webhook Integration

### Step 1: Get Your Vercel API URL

```bash
# Your Virtual LPR endpoint URL:
https://your-project.vercel.app/api/virtual-lpr

# Example:
https://circuitos.vercel.app/api/virtual-lpr
```

### Step 2: Create GHL Workflow

**In GoHighLevel:**

1. **Automations → Workflows → + New Workflow**

2. **Name:** "Virtual LPR - Lead Validator"

3. **Trigger:** Choose one:
   - Contact Created (all new contacts)
   - Tag Added: "vLPR" (manual trigger)
   - Form Submitted (specific form)
   - Webhook Received (external signal)

4. **Add Action: Send Webhook**
   ```
   URL: https://your-project.vercel.app/api/virtual-lpr
   Method: POST
   Content-Type: application/json

   Body:
   {
     "signal_type": "website_visit",
     "signal_data": {
       "page_url": "{{contact.last_page_visited}}",
       "session_duration": 120,
       "location": {
         "city": "{{contact.city}}",
         "zip_code": "{{contact.postal_code}}",
         "lat": {{contact.latitude}},
         "lng": {{contact.longitude}}
       },
       "ip_address": "{{contact.ip_address}}",
       "timestamp": "{{current_timestamp}}"
     },
     "business": {
       "name": "MetroFlex Gym",
       "city": "Arlington",
       "state": "Texas",
       "lat": 32.7357,
       "lng": -97.1081,
       "type": "Hardcore powerlifting/strongman gym",
       "target_radius_miles": 10,
       "max_distance_miles": 25
     }
   }
   ```

5. **Add Action: Condition**
   ```
   IF: {{webhook_response.qualified}} equals true
   ```

6. **YES Branch: Update Contact**
   ```
   Add Tags: {{webhook_response.detection.initial_tags}}

   Update Custom Fields:
   - vlpr_source: {{webhook_response.ghl_integration.custom_fields.vlpr_source}}
   - vlpr_signal_strength: {{webhook_response.ghl_integration.custom_fields.vlpr_signal_strength}}
   - vlpr_score: {{webhook_response.ghl_integration.custom_fields.vlpr_score}}
   - distance_miles: {{webhook_response.ghl_integration.custom_fields.distance_miles}}
   - median_income: {{webhook_response.ghl_integration.custom_fields.median_income}}
   - zip_code: {{webhook_response.ghl_integration.custom_fields.zip_code}}
   ```

7. **YES Branch: Trigger Next Workflow**
   ```
   Workflow: "Lead Scorer" (your existing BANT/MEDDIC scorer)
   ```

8. **NO Branch: Add to Watch List**
   ```
   Add Tag: "Low Intent - Monitor"
   Add Note: "Virtual LPR score too low, monitoring for additional signals"
   ```

---

## 📊 API Reference

### Endpoint: POST /api/virtual-lpr

**Request Body:**
```json
{
  "signal_type": "website_visit" | "gmb_view" | "social_profile_view" | "email_open" | "location_proximity",
  "signal_data": {
    "page_url": "/pricing",
    "session_duration": 180,
    "location": {
      "city": "Arlington",
      "zip_code": "76011",
      "lat": 32.7450,
      "lng": -97.1180
    },
    "ip_address": "8.8.8.8"
  },
  "business": {
    "name": "MetroFlex Gym",
    "city": "Arlington",
    "state": "Texas",
    "lat": 32.7357,
    "lng": -97.1081,
    "type": "Hardcore powerlifting/strongman gym",
    "target_radius_miles": 10
  }
}
```

**Response (Qualified Lead):**
```json
{
  "success": true,
  "qualified": true,
  "detection": {
    "qualified_lead": true,
    "signal_strength": 85,
    "predicted_lpr_score": 78,
    "reasoning": "High-intent action (directions clicked) from 2 miles away...",
    "awareness_level": "Product Aware",
    "initial_tags": ["Virtual LPR - High Intent", "Arlington ZIP 76011", "Within 5 miles"],
    "enrichment_summary": {
      "distance_miles": 1.8,
      "median_income": 65320,
      "median_age": 33,
      "zip_code": "76011"
    }
  },
  "ghl_integration": {
    "action": "create_contact",
    "initial_tags": ["Virtual LPR - High Intent", ...],
    "custom_fields": {
      "vlpr_source": "gmb_view",
      "vlpr_signal_strength": 85,
      "vlpr_score": 78,
      "distance_miles": 1.8,
      "median_income": 65320,
      "zip_code": "76011"
    },
    "next_workflow": "Lead Scorer"
  }
}
```

**Response (Not Qualified):**
```json
{
  "success": true,
  "qualified": false,
  "detection": {
    "qualified_lead": false,
    "signal_strength": 25,
    "reasoning": "Low engagement (10s visit) from 30 miles away, outside target radius",
    "recommended_action": "Ignore"
  }
}
```

---

## 💰 Cost Breakdown

### Infrastructure (All FREE)
- **Vercel Hosting:** FREE (100GB bandwidth)
- **Google Maps API:** FREE ($200/mo credit = 28K calls)
- **US Census API:** FREE (unlimited)
- **Google Analytics 4:** FREE (unlimited)

### Variable Costs
- **Claude API:** ~$0.01 per validation
- **Monthly estimate (100 leads/day):** ~$30/month

### vs. Traditional LPR
- **Hardware LPR System:** $10,000 - $50,000
- **Your Virtual LPR:** $30/month
- **Savings:** $49,970+ 🎉

---

## 🧪 Testing Checklist

Before going live, verify:

- [ ] Test console loads at `/api/test-lead-validation`
- [ ] High-intent test returns qualified=true, score 70+
- [ ] Website visit test returns qualified=true, score 40-69
- [ ] Low-quality test returns qualified=false, score <40
- [ ] Census data populates (median_income, median_age)
- [ ] Distance calculation works (or falls back to Haversine)
- [ ] GHL webhook receives response correctly
- [ ] Custom fields populate in GHL contact

---

## 🐛 Troubleshooting

### Error: "AI returned invalid JSON"
**Cause:** Claude API returned malformed JSON
**Fix:** Check your ANTHROPIC_API_KEY is valid, try again

### Error: "Census API failed"
**Cause:** Invalid ZIP code or Census API down
**Fix:** System will continue without Census data (graceful degradation)

### Error: "Google Maps API failed"
**Cause:** Invalid API key or exceeded quota
**Fix:** System falls back to Haversine formula (free but less accurate)

### GHL webhook not triggering
**Cause:** Firewall or wrong URL
**Fix:**
1. Test endpoint directly with Postman/curl
2. Check Vercel logs for errors
3. Verify webhook URL has no typos

---

## 🚀 What's Next?

### Week 1: Testing
- Process 10-20 test leads
- Verify scoring accuracy
- Adjust thresholds if needed

### Week 2: Production
- Connect to live GHL workflows
- Monitor qualification rate (target: 20-30% qualified)
- Track conversion rate (qualified → customer)

### Month 2: Optimization
- A/B test scoring thresholds (40 vs 50 vs 60)
- Add more signal sources (GA4, social media)
- Build ML feedback loop

---

## 📞 Support

**Documentation:**
- Main guide: `VIRTUAL-LPR-MCP-INTEGRATION.md`
- MCP integrations: `FREE-MCP-INTEGRATION-GUIDE.md`
- GHL setup: `GHL-Setup/README.md`

**Test Console:**
- https://your-project.vercel.app/api/test-lead-validation

**Need Help?**
- Check Vercel logs for errors
- Review API response in test console
- Verify environment variables are set

---

## ✅ Deployment Complete!

You now have:
- ✅ Virtual LPR API deployed to Vercel
- ✅ Test console for validation
- ✅ GHL integration ready
- ✅ FREE MCP servers configured
- ✅ $0/month infrastructure cost

**Next Step:** Open the test console and validate your first lead!

```bash
# Your test console:
https://your-project.vercel.app/api/test-lead-validation
```

---

**© 2025 CircuitOS™ - Virtual LPR™ Patent Pending**
