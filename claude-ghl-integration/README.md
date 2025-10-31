# Claude API Integration for GoHighLevel
## World-Class AI Employees Powered by Claude Sonnet 4.5

This project provides serverless API endpoints that connect GoHighLevel workflows to Claude API, enabling world-class AI capabilities (10/10 quality) instead of GHL's built-in AI (7/10 quality).

---

## 🎯 What This Gives You

**7 World-Class AI Employees:**

1. **Lead Scorer** (`/api/score-lead`) - BANT/MEDDIC/CHAMP enterprise scoring
2. **Master Copywriter** (`/api/copywriter`) - Russell Brunson + Eugene Schwartz + Alex Hormozi frameworks
3. **Email Campaign Manager** (`/api/email-campaign`) - Instantly.ai integration with deliverability optimization
4. **Channel Router** (`/api/channel-router`) - Omnichannel orchestration (Email → LinkedIn → SMS → Call)
5. **Reputation Guardian** (`/api/reputation`) - Review monitoring and response generation
6. **Content Creator** (`/api/content-creator`) - Hyperlocal SEO-optimized content
7. **Search Optimizer** (`/api/search-optimizer`) - AI search engine optimization (ChatGPT, Perplexity, etc.)

**Cost:** ~$50-150/month (Claude API usage) + $0 hosting (Vercel free tier)

**Quality Upgrade:** 7/10 (GHL AI) → 10/10 (Claude Sonnet 4.5)

---

## 🚀 Quick Start (15 Minutes)

### Step 1: Get Claude API Key

1. Go to [console.anthropic.com](https://console.anthropic.com)
2. Sign up or log in
3. Navigate to **Settings → API Keys**
4. Click **Create Key**
5. Copy your API key (starts with `sk-ant-...`)

### Step 2: Deploy to Vercel

```bash
# Clone or navigate to this directory
cd claude-ghl-integration

# Install Vercel CLI (if not installed)
npm install -g vercel

# Deploy
vercel

# Follow prompts:
# - Set up and deploy? Yes
# - Which scope? [Your account]
# - Link to existing project? No
# - Project name? claude-ghl-integration
# - Directory? ./
# - Override settings? No

# Add Claude API key as environment variable
vercel env add CLAUDE_API_KEY

# Paste your API key when prompted
# Select: Production, Preview, Development (all three)

# Redeploy with environment variable
vercel --prod
```

**You'll get a URL:** `https://claude-ghl-integration-[random].vercel.app`

### Step 3: Test the API

```bash
# Test Lead Scorer endpoint
curl -X POST https://your-project.vercel.app/api/score-lead \
  -H "Content-Type: application/json" \
  -d '{
    "contact": {
      "first_name": "John",
      "last_name": "Doe",
      "email": "john@example.com",
      "city": "Brooklyn",
      "state": "NY",
      "custom_fields": {
        "distance_miles": 1.2,
        "lpr_score": 78,
        "intent_signal": "Called business"
      }
    },
    "business": {
      "name": "MetroFlex Gym",
      "category": "Fitness",
      "address": "Arlington, TX"
    }
  }'
```

If you get a JSON response with a score, it's working! 🎉

---

## 🔧 GoHighLevel Integration

### Configure GHL Workflow to Call Claude API

**Example: Lead Scoring Workflow**

1. **Open GHL** → Automations → Workflows
2. **Create New Workflow** or edit existing
3. **Add Trigger:** "Contact Created" or "Tag Added"
4. **Add Action:** Webhook
5. **Configure Webhook:**
   - **URL:** `https://your-project.vercel.app/api/score-lead`
   - **Method:** POST
   - **Headers:**
     ```json
     {
       "Content-Type": "application/json"
     }
     ```
   - **Body:**
     ```json
     {
       "contact": {
         "first_name": "{{contact.first_name}}",
         "last_name": "{{contact.last_name}}",
         "email": "{{contact.email}}",
         "city": "{{contact.city}}",
         "state": "{{contact.state}}",
         "custom_fields": {
           "distance_miles": "{{contact.custom_fields.distance_miles}}",
           "lpr_score": "{{contact.custom_fields.lpr_score}}",
           "intent_signal": "{{contact.custom_fields.intent_signal}}"
         }
       },
       "business": {
         "name": "Your Business Name",
         "category": "Your Category",
         "address": "Your City, State"
       }
     }
     ```

6. **Store Response in Custom Fields:**
   - Create custom fields in GHL:
     - `lpr_score` (Number)
     - `fit_score` (Number)
     - `intent_score` (Number)
     - `timing_score` (Number)
     - `score_confidence` (Text)
     - `next_action` (Dropdown: IMMEDIATE_COLD_EMAIL, NURTURE_SEQUENCE, EDUCATION_SEQUENCE)

   - Map webhook response to custom fields:
     - `{{webhook.response.total_score}}` → `lpr_score`
     - `{{webhook.response.breakdown.fit}}` → `fit_score`
     - `{{webhook.response.breakdown.intent}}` → `intent_score`
     - `{{webhook.response.breakdown.timing}}` → `timing_score`
     - `{{webhook.response.confidence}}` → `score_confidence`
     - `{{webhook.response.next_action}}` → `next_action`

7. **Add Conditional Logic:**
   - IF `lpr_score >= 70` → Tag: "High Intent - Cold Email"
   - IF `lpr_score 40-69` → Tag: "Medium Intent - Nurture"
   - IF `lpr_score < 40` → Tag: "Low Intent - Education"

---

## 📊 API Endpoints Reference

### 1. Lead Scorer (`POST /api/score-lead`)

**Input:**
```json
{
  "contact": {
    "first_name": "string",
    "last_name": "string",
    "email": "string",
    "city": "string",
    "state": "string",
    "custom_fields": {
      "distance_miles": number,
      "lpr_score": number,
      "intent_signal": "string"
    }
  },
  "business": {
    "name": "string",
    "category": "string",
    "address": "string"
  }
}
```

**Output:**
```json
{
  "total_score": 78,
  "grade": "A",
  "priority": "HIGH",
  "breakdown": {
    "fit": 26,
    "intent": 36,
    "timing": 16
  },
  "confidence": "VERY_HIGH",
  "next_action": "IMMEDIATE_COLD_EMAIL",
  "estimated_ltv": 4800
}
```

### 2. Master Copywriter (`POST /api/copywriter`)

**Input:**
```json
{
  "contact": { ... },
  "channel": "email|sms|linkedin",
  "awareness_level": "PRODUCT_AWARE",
  "business": { ... },
  "touch_number": 1
}
```

**Output:**
```json
{
  "variants": [
    {
      "id": "A",
      "subject": "Subject line",
      "body": "Email body",
      "cta": "Call to action",
      "framework_used": "Brunson Hook-Story-Offer"
    }
  ],
  "recommended_variant": "A"
}
```

### 3. Email Campaign Manager (`POST /api/email-campaign`)

Creates 5-touch email sequences optimized for deliverability.

### 4. Channel Router (`POST /api/channel-router`)

Determines optimal next channel based on engagement history.

### 5. Reputation Guardian (`POST /api/reputation`)

Generates authentic review responses or review request messages.

### 6. Content Creator (`POST /api/content-creator`)

Creates SEO-optimized content (blog posts, GMB posts, service pages).

### 7. Search Optimizer (`POST /api/search-optimizer`)

Optimizes content for AI search engines (ChatGPT, Perplexity, Claude).

---

## 💰 Cost Analysis

### Claude API Pricing (as of 2025)

- **Input tokens:** $3 per million tokens (~$0.003 per 1K tokens)
- **Output tokens:** $15 per million tokens (~$0.015 per 1K tokens)

### Estimated Costs Per Endpoint

| Endpoint | Input Tokens | Output Tokens | Cost Per Call | Use Case |
|----------|-------------|---------------|---------------|----------|
| Lead Scorer | ~2,000 | ~2,000 | ~$0.04 | Every new lead |
| Copywriter | ~2,000 | ~1,500 | ~$0.03 | 3x per lead (email, SMS, LinkedIn) |
| Email Campaign | ~2,000 | ~4,000 | ~$0.07 | Once per campaign setup |
| Channel Router | ~1,500 | ~500 | ~$0.01 | Every engagement check |
| Reputation | ~500 | ~300 | ~$0.006 | Per review response |
| Content Creator | ~1,000 | ~6,000 | ~$0.10 | Per content piece |
| Search Optimizer | ~3,000 | ~4,000 | ~$0.07 | Per optimization |

### Monthly Cost Examples

**Small Business (100 leads/month):**
- Lead scoring: 100 × $0.04 = $4
- Copywriting: 100 × 3 × $0.03 = $9
- Channel routing: 100 × 5 × $0.01 = $5
- **Total: ~$20/month**

**Growing Business (1,000 leads/month):**
- Lead scoring: 1,000 × $0.04 = $40
- Copywriting: 1,000 × 3 × $0.03 = $90
- Channel routing: 1,000 × 5 × $0.01 = $50
- Review responses: 50 × $0.006 = $0.30
- **Total: ~$180/month**

**Vercel Hosting:** FREE (up to 100GB bandwidth/month)

---

## 🔒 Security Best Practices

1. **Never commit `.env` file** - API keys should stay local
2. **Use Vercel environment variables** - Keys stored securely in production
3. **Rotate API keys periodically** - Every 90 days recommended
4. **Monitor usage** - Set up billing alerts in Anthropic console
5. **Rate limiting** - Implement in GHL workflows (avoid spam)

---

## 🐛 Troubleshooting

### Error: "Missing CLAUDE_API_KEY"

**Solution:** Add environment variable to Vercel:
```bash
vercel env add CLAUDE_API_KEY
# Paste your API key
vercel --prod  # Redeploy
```

### Error: "Method not allowed"

**Solution:** Ensure you're using POST requests (not GET):
```bash
curl -X POST https://your-url/api/score-lead ...
```

### Error: "No valid JSON found in Claude response"

**Solution:** Claude occasionally wraps JSON in markdown. The code handles this automatically. If it persists, check Claude API status at status.anthropic.com.

### GHL Workflow Not Triggering

**Checklist:**
1. Webhook URL is correct (no typos)
2. Method is POST
3. Content-Type header is set
4. Body has correct variable syntax: `{{contact.field}}`
5. Webhook action is placed after contact data is available

---

## 📈 Performance Monitoring

### Track These Metrics in GHL

1. **Lead Scoring Accuracy**
   - Compare predicted LPR score to actual conversion
   - Goal: 85%+ accuracy

2. **Email Reply Rates**
   - Track reply rate per copywriter variant
   - Goal: 8%+ reply rate (vs 3% industry average)

3. **Channel Conversion Rates**
   - Track which channel routes convert best
   - Goal: 4%+ conversion rate (vs 1.2% industry average)

4. **Review Response Rate**
   - Track % of reviews responded to within 24 hours
   - Goal: 90%+ response rate

---

## 🔄 Updating the Code

```bash
# Make changes to api/*.js files

# Test locally
vercel dev

# Deploy updates
vercel --prod
```

---

## 📚 Additional Resources

- **Claude API Docs:** [docs.anthropic.com](https://docs.anthropic.com)
- **Vercel Docs:** [vercel.com/docs](https://vercel.com/docs)
- **GHL Webhook Guide:** [help.gohighlevel.com](https://help.gohighlevel.com)
- **Full AI Employee Documentation:** See `GHL-Setup/AI-Employees/` folder

---

## 🆘 Support

If you encounter issues:

1. Check Vercel deployment logs: `vercel logs`
2. Check GHL workflow execution history
3. Verify Claude API key is valid: [console.anthropic.com](https://console.anthropic.com)
4. Check API usage/limits in Anthropic console

---

## 📄 License

**Proprietary** - Circuit OS™ 2025

This integration is part of the Circuit OS Virtual LPR™ system. See `PROPRIETARY-TECHNOLOGY-EXPLAINED.md` for details on IP protection.

---

**© 2025 Circuit OS™**
**World-Class AI Integration for GoHighLevel**
