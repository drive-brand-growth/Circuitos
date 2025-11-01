# Quick Reference Card - Dual-Path Lead System
**Keep this open while following COMPLETE-SETUP-GUIDE-STEP-BY-STEP.md**

---

## 🚀 Quick Start Commands

### Local Development
```bash
# Install dependencies (one time)
npm install

# Start local server
vercel dev

# Test interactively
# Open browser: http://localhost:3000/api/test-lead-validation
```

### Deploy to Production
```bash
# Login to Vercel (one time)
npm install -g vercel
vercel login

# Deploy
vercel --prod
```

---

## 🔌 Your API Endpoints

### 1. Virtual LPR (Lead Validator)
**Endpoint:** `/api/virtual-lpr`
**Purpose:** Validates and scores leads 0-100 with demographics

**Test locally:**
```bash
curl -X POST http://localhost:3000/api/virtual-lpr \
  -H "Content-Type: application/json" \
  -d '{
    "signal_type": "gmb_view",
    "signal_data": {
      "phone": "8175551234",
      "zip_code": "76102"
    },
    "business": {
      "name": "MetroFlex Gym",
      "lat": 32.7357,
      "lng": -97.1081
    }
  }'
```

**Production URL:**
```
https://your-project.vercel.app/api/virtual-lpr
```

---

### 2. Lead Router (Source Detection)
**Endpoint:** `/api/lead-router`
**Purpose:** Detects if lead is cold email vs website traffic

**Test locally:**
```bash
# Test cold email detection
curl -X POST http://localhost:3000/api/lead-router \
  -H "Content-Type: application/json" \
  -d '{
    "contact": {
      "email": "test@example.com",
      "first_name": "John",
      "tags": ["Instantly Campaign"]
    }
  }'
```

---

### 3. Master Copywriter (4 Frameworks)
**Endpoint:** `/api/copywriter`
**Purpose:** Generates A/B/C variants using Brunson, Schwartz, StoryBrand, Hormozi

**Test locally:**
```bash
# Cold email tone (humble)
curl -X POST http://localhost:3000/api/copywriter \
  -H "Content-Type: application/json" \
  -d '{
    "contact": {
      "first_name": "Marcus",
      "email": "marcus@example.com"
    },
    "channel": "email",
    "awareness_level": "Problem Aware",
    "lead_source": "cold_email",
    "business": {
      "name": "MetroFlex Gym",
      "city": "Fort Worth",
      "state": "TX"
    }
  }'

# Website traffic tone (confident)
curl -X POST http://localhost:3000/api/copywriter \
  -H "Content-Type: application/json" \
  -d '{
    "contact": {
      "first_name": "Sarah",
      "email": "sarah@example.com"
    },
    "channel": "email",
    "awareness_level": "Product Aware",
    "lead_source": "website_traffic",
    "business": {
      "name": "MetroFlex Gym",
      "city": "Fort Worth",
      "state": "TX"
    }
  }'
```

---

### 4. Instantly Webhook
**Endpoint:** `/api/instantly-webhook`
**Purpose:** Receives Instantly.ai webhooks and qualifies replies

**Configure in Instantly.ai:**
```
Webhook URL: https://your-project.vercel.app/api/instantly-webhook
Events: Email Reply, Link Click, Email Opened
```

---

### 5. Test Console (Interactive)
**Endpoint:** `/api/test-lead-validation`
**Purpose:** Beautiful UI to test all 3 scenarios

**Access:**
```
Local: http://localhost:3000/api/test-lead-validation
Production: https://your-project.vercel.app/api/test-lead-validation
```

---

## 🎯 Framework Routing Logic

### By Awareness Level (Schwartz)
```
Unaware (0-20) → Problem identification (Brunson)
Problem Aware (21-40) → Agitate problem (Schwartz)
Solution Aware (41-60) → StoryBrand (build trust)
Product Aware (61-80) → Social proof (Schwartz)
Most Aware (81-100) → Direct value (Hormozi)
```

### By Lead Source
```
Cold Email → StoryBrand (humble, respectful)
Website Traffic → Hormozi/Brunson (confident, direct)
```

---

## 📊 GHL Custom Fields (Required)

Create these in GHL → Settings → Custom Fields:

```
Field Name                    Type        Example Value
──────────────────────────────────────────────────────────
lead_source                   Text        "cold_email" or "website_traffic"
vlpr_score                    Number      85
vlpr_qualified                Yes/No      Yes
distance_miles                Number      2.4
median_income                 Number      87500
awareness_level               Text        "Product Aware"
instantly_campaign_id         Text        "camp_abc123"
instantly_qualification       Text        "positive"
```

---

## 🔗 GHL Webhook Setup

### Workflow 1: Website Traffic (Virtual LPR)
```
Trigger: Form Submitted OR Tag Added: "Website Lead"

HTTP Request 1: Virtual LPR
  URL: https://your-project.vercel.app/api/virtual-lpr
  Method: POST
  Body:
  {
    "signal_type": "website_visit",
    "signal_data": {
      "phone": "{{contact.phone}}",
      "zip_code": "{{contact.postal_code}}"
    },
    "business": {
      "name": "MetroFlex Gym",
      "lat": 32.7357,
      "lng": -97.1081
    }
  }

Decision Node: Check if qualified
  IF vlpr_qualified = Yes → Continue
  ELSE → Archive

HTTP Request 2: Master Copywriter
  URL: https://your-project.vercel.app/api/copywriter
  Method: POST
  Body:
  {
    "contact": {
      "first_name": "{{contact.first_name}}",
      "email": "{{contact.email}}",
      "custom_fields": {
        "distance_miles": "{{contact.custom_fields.distance_miles}}",
        "median_income": "{{contact.custom_fields.median_income}}",
        "vlpr_score": "{{contact.custom_fields.vlpr_score}}"
      }
    },
    "channel": "email",
    "awareness_level": "{{contact.custom_fields.awareness_level}}",
    "lead_source": "website_traffic",
    "business": {
      "name": "MetroFlex Gym",
      "city": "Fort Worth",
      "state": "TX"
    }
  }

Email Action:
  To: {{contact.email}}
  Subject: {{custom_values.email_subject}}
  Body: {{custom_values.email_body}}
```

---

## ✅ Testing Checklist

### Local Testing (Before Deploy)
- [ ] `vercel dev` starts without errors
- [ ] http://localhost:3000/api/test-lead-validation loads
- [ ] Test 1 (High Intent GMB) scores 85+
- [ ] Test 2 (Website Visit) scores 60-75
- [ ] Test 3 (Low Quality) scores <40
- [ ] Cold email copy uses "Thanks for replying..."
- [ ] Website traffic copy uses "Saw you on our site..."

### Production Testing (After Deploy)
- [ ] All endpoints return 200 status
- [ ] Test console accessible online
- [ ] GHL webhook receives response in <2 seconds
- [ ] Custom fields populate correctly
- [ ] Email variants (A/B/C) are distinct

### End-to-End Testing
- [ ] Create test contact in GHL
- [ ] Add tag "Website Lead"
- [ ] Workflow triggers
- [ ] vlpr_score populates
- [ ] Email sends with personalized copy
- [ ] Test cold email path separately

---

## ❌ Common Issues & Fixes

### Issue: "ANTHROPIC_API_KEY is required"
**Fix:** Add API key to .env (local) or Vercel (production)
```bash
# Local
echo "ANTHROPIC_API_KEY=sk-ant-api03-YOUR-KEY-HERE" >> .env

# Production
# Vercel Dashboard → Settings → Environment Variables → Add
```

### Issue: "Module not found: @anthropic-ai/sdk"
**Fix:** Install dependencies
```bash
npm install
```

### Issue: Webhook times out (504)
**Fix:** Check Claude API key is valid, or increase timeout in GHL
```
GHL Workflow → HTTP Request → Advanced → Timeout: 30 seconds
```

### Issue: Wrong framework being used
**Fix:** Check awareness_level is being passed correctly
```javascript
// Should be one of:
"Unaware"
"Problem Aware"
"Solution Aware"
"Product Aware"
"Most Aware"
```

### Issue: Copy tone is wrong (cold email sounds pushy)
**Fix:** Verify lead_source is set correctly
```javascript
// Should be EXACTLY:
"cold_email"  // NOT "cold", "email", "instantly"
"website_traffic"  // NOT "website", "web", "organic"
```

---

## 📖 Documentation Links

**Start here:**
1. COMPLETE-SETUP-GUIDE-STEP-BY-STEP.md (You are here)
2. QUICK-REFERENCE-CARD.md (This file)

**Deep dives:**
- DUAL-PATH-LEAD-SYSTEM.md - Complete system architecture
- FRAMEWORK-ROUTING-GUIDE.md - When to use each framework
- VERCEL-DEPLOYMENT-GUIDE.md - Deployment walkthrough
- VIRTUAL-LPR-DEPLOYMENT-GUIDE.md - Lead validation details

---

## 🔥 Most Common Commands (Copy-Paste Ready)

```bash
# Start local development
vercel dev

# Test Virtual LPR locally
curl -X POST http://localhost:3000/api/virtual-lpr \
  -H "Content-Type: application/json" \
  -d '{"signal_type":"gmb_view","signal_data":{"phone":"8175551234","zip_code":"76102"},"business":{"name":"MetroFlex Gym","lat":32.7357,"lng":-97.1081}}'

# Test Master Copywriter (cold email)
curl -X POST http://localhost:3000/api/copywriter \
  -H "Content-Type: application/json" \
  -d '{"contact":{"first_name":"Marcus","email":"marcus@example.com"},"channel":"email","awareness_level":"Problem Aware","lead_source":"cold_email","business":{"name":"MetroFlex Gym","city":"Fort Worth","state":"TX"}}'

# Test Master Copywriter (website traffic)
curl -X POST http://localhost:3000/api/copywriter \
  -H "Content-Type: application/json" \
  -d '{"contact":{"first_name":"Sarah","email":"sarah@example.com"},"channel":"email","awareness_level":"Product Aware","lead_source":"website_traffic","business":{"name":"MetroFlex Gym","city":"Fort Worth","state":"TX"}}'

# Deploy to production
vercel --prod

# View logs
vercel logs
```

---

## 🎓 Key Concepts Reminder

**Virtual LPR™** = Detects "virtual passersby" using online signals (website visits, GMB views)

**Dual-Path Routing** = Different workflows for cold vs warm leads

**Framework Routing** = AI picks best copywriting style (Brunson, Schwartz, StoryBrand, Hormozi)

**Awareness Levels** = Schwartz's 5 stages: Unaware → Problem → Solution → Product → Most Aware

**Lead Source Matters** = Cold email = humble tone, Website traffic = confident tone

---

**Need help?** Open the full guide: COMPLETE-SETUP-GUIDE-STEP-BY-STEP.md
