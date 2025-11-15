# METROFLEX EVENTS AI AGENT - COMPLETE COST BREAKDOWN

## 💰 MONTHLY COST ANALYSIS

### **TIER 1: MVP - Core Competitor Scraping ($84-164/month)**

| Service | Plan | Cost/Month | Purpose | Required? |
|---------|------|------------|---------|-----------|
| **n8n Cloud** | Starter | $20 | Workflow automation engine | ✅ REQUIRED |
| **Apify** | Personal | $49 | Instagram/Facebook scraping | ✅ REQUIRED |
| **Claude API** | Pay-as-you-go | $15-50 | AI profile analysis | ✅ REQUIRED |
| **GoHighLevel** | (Existing) | $0* | CRM & outreach campaigns | ✅ REQUIRED |
| **SUBTOTAL** | | **$84-119/mo** | | |

*Assumes you already have GHL subscription ($97-297/mo depending on plan)

---

### **TIER 2: ENHANCED - Full Marketing Automation ($134-264/month)**

Add to Tier 1:

| Service | Plan | Cost/Month | Purpose | Required? |
|---------|------|------------|---------|-----------|
| **ManyChat** | Pro | $15 | Instagram DM automation | 🟡 OPTIONAL |
| **SendGrid** | Essentials | $20 | Transactional emails (if GHL insufficient) | 🟡 OPTIONAL |
| **Apify Extra Operations** | Add-on | $15-50 | If scraping >10K profiles/month | 🟡 OPTIONAL |
| **SUBTOTAL** | | **$134-204/mo** | | |

---

### **TIER 3: PREMIUM - Complete Intelligence System ($184-364/month)**

Add to Tier 2:

| Service | Plan | Cost/Month | Purpose | Required? |
|---------|------|------------|---------|-----------|
| **Octoparse** | Standard | $75 | Website scraping (NPC results, competitor sites) | 🟡 OPTIONAL |
| **Apollo.io** | Basic | $49 | Email/contact enrichment | 🟡 OPTIONAL |
| **Brand24** | Personal | $79 | Social media monitoring/sentiment | 🟡 OPTIONAL |
| **SUBTOTAL** | | **$287-427/mo** | | |

---

## 📊 DETAILED SERVICE BREAKDOWN

### **1. n8n Cloud - $20/month**

**What You Get:**
- 2,500 workflow executions/month
- Unlimited operations per execution
- Cloud hosting (99.9% uptime)
- Workflow editor with 400+ integrations
- Email support
- SSL/security included

**Your Usage Projection:**
- NPC scraping workflow: ~4 executions/month (weekly runs)
- Competitor monitoring: ~8 executions/month (twice weekly)
- Reputation management: ~30 executions/month (daily)
- Marketing automation: ~50 executions/month
- **TOTAL: ~100 executions/month (4% of limit)**

**Pricing Tiers:**
| Plan | Executions | Cost | When to Upgrade |
|------|------------|------|----------------|
| Starter | 2,500 | $20/mo | You're here (perfect fit) |
| Pro | 10,000 | $50/mo | If running 200+ workflows/month |
| Advanced | 25,000 | $100/mo | Enterprise scale only |

**Why n8n:**
- Fixed cost regardless of data volume
- Process 1,000 profiles in ONE execution
- No per-operation charges
- Export workflows (no lock-in)

---

### **2. Apify - $49/month**

**What You Get:**
- 10,000 platform credits/month
- Instagram scraper
- Facebook scraper
- Proxy rotation (avoid blocks)
- Residential IPs
- Webhook integrations
- Data storage (30 days)

**Credit Usage Calculator:**

| Scraping Task | Credits | Frequency | Monthly Credits |
|---------------|---------|-----------|-----------------|
| Instagram hashtag (#NPCTexas) - 500 profiles | 500 | Weekly (4x) | 2,000 |
| Facebook event attendees - 300 profiles | 300 | Bi-weekly (2x) | 600 |
| Instagram profile details (deep scrape) | 1,000 | Monthly | 1,000 |
| Competitor social monitoring | 500 | Weekly (4x) | 2,000 |
| **TOTAL MONTHLY CREDITS NEEDED** | | | **5,600** |

**You'll Need:**
- Base plan (10,000 credits): $49/mo ✅ (covers usage with buffer)
- If scaling >10K credits: Add-ons at $10 per 1,000 credits

**Pricing Tiers:**
| Plan | Credits | Cost | Storage | When to Use |
|------|---------|------|---------|-------------|
| Free | 5 | $0 | 7 days | Testing only |
| Personal | 10,000 | $49/mo | 30 days | **Your tier** |
| Team | 30,000 | $149/mo | 60 days | If scraping 2,000+ profiles/week |

**Alternative to Apify:**
- **Phantom Buster**: $30-100/mo (similar features, may have fewer credits)
- **Octoparse**: $75/mo (visual scraper, less reliable for Instagram)
- **Custom Python scraper**: $0/mo (DIY, but higher risk of blocks)

**Why Apify:**
- Best Instagram scraper reliability
- Professional proxy rotation (won't get you banned)
- Webhook integration with n8n (seamless)
- Handles CAPTCHA challenges
- Regular updates when Instagram changes

---

### **3. Claude API (Anthropic) - $15-50/month**

**Pricing Model:** Pay per token (input + output)

| Model | Input (per 1M tokens) | Output (per 1M tokens) | Best For |
|-------|----------------------|------------------------|----------|
| Claude 3.5 Haiku | $0.80 | $4.00 | Simple analysis (cheaper) |
| Claude 3.5 Sonnet | $3.00 | $15.00 | **Recommended** (best quality/cost) |
| Claude 3 Opus | $15.00 | $75.00 | Premium (overkill for this) |

**Usage Calculator (Claude 3.5 Sonnet):**

```
Per Profile Analysis:
- Input prompt: ~800 tokens (profile data + instructions)
- Output response: ~400 tokens (JSON analysis)
- Total per profile: ~1,200 tokens

Cost per profile:
- Input: 800 tokens × $3.00 / 1M = $0.0024
- Output: 400 tokens × $15.00 / 1M = $0.0060
- TOTAL: $0.0084 per profile (~$0.01)

Monthly projection:
- 500 profiles/week × 4 weeks = 2,000 profiles/month
- 2,000 × $0.0084 = $16.80/month
```

**Conservative Estimate:** $15-25/month (2,000-3,000 profiles)
**Heavy Usage:** $40-50/month (5,000+ profiles)

**Billing Setup:**
- Create account at console.anthropic.com
- Add credit card (no monthly minimum)
- Set usage limit alerts ($50, $100, etc.)
- Pay only for what you use

**Cost Optimization Tips:**
- Use Haiku for simple tasks (60% cheaper)
- Batch multiple profiles in one API call (save on requests)
- Cache system prompts (reduce repeated tokens)
- Set max_tokens limit (prevent runaway costs)

---

### **4. GoHighLevel - $97-297/month** (Assuming you have this)

**Required Plan for This Use Case:**

| Plan | Cost | Contacts | AI Features | Workflows | Your Fit |
|------|------|----------|-------------|-----------|----------|
| Starter | $97/mo | 500 | Limited | 10 | ❌ Too small |
| Unlimited | $297/mo | Unlimited | Full | Unlimited | ✅ **Recommended** |
| Agency | $497+/mo | Unlimited | Full + White-label | Unlimited | 🟡 If reselling |

**What You're Using GHL For:**
- Contact database (2,000+ athletes, spectators, vendors)
- Custom fields (50+ fields for athlete data)
- Tags & segmentation (20+ tag categories)
- Email campaigns (10+ sequences)
- SMS campaigns (urgency triggers, reminders)
- Workflow automation (triggered campaigns)
- Calendars (event registration, check-in scheduling)
- Forms (registration forms embedded on website)
- Pipeline management (track athletes through funnel)
- Reporting & analytics

**GHL Built-in AI (Alternative to Claude API):**
- If you're on Unlimited plan, you get AI content generation
- Cost: $97/mo additional for unlimited AI requests
- **Could replace Claude API for simpler tasks**
- **Verdict:** Claude API is better quality for profile analysis, but GHL AI works for email copywriting

**GHL Alternatives (NOT Recommended):**
- HubSpot: $15-3,200/mo (more expensive, overkill)
- ActiveCampaign: $29-149/mo (lacks forms/calendar)
- Keap: $159-299/mo (similar to GHL but less features)
- **Stick with GHL** - it's purpose-built for this workflow

---

### **5. ManyChat - $15/month** (OPTIONAL)

**Purpose:** Instagram DM automation

**What You Get:**
- Send automated Instagram DMs
- Triggered by keywords, comments, story replies
- Drip sequences via DM
- 1,000 contacts included
- Pro growth tools

**Your Use Case:**
- Auto-respond when athletes DM you
- Send personalized DM sequences to scraped athletes
- Follow-up DMs for non-responders
- Lead qualification via DM

**Pricing:**
| Plan | Contacts | Cost | Features |
|------|----------|------|----------|
| Free | 50 | $0 | Basic automation |
| Pro | 1,000 | $15/mo | **Recommended** |
| Premium | 25,000+ | $45+ | Enterprise |

**Alternative:**
- **Manual DMs:** Free but time-consuming (20-30 DMs/day manually)
- **Mobile Monkey:** $19/mo (similar features)
- **Chatfuel:** $15-300/mo (more complex)

**Do You Need This?**
- 🟢 **YES** if: You want to automate Instagram outreach at scale
- 🔴 **NO** if: You're okay with manual DMs or email-only outreach

---

### **6. SendGrid - $0-20/month** (OPTIONAL)

**Purpose:** Transactional emails (if GHL email deliverability is poor)

**Pricing:**
| Plan | Emails/Month | Cost | When to Use |
|------|--------------|------|-------------|
| Free | 100/day | $0 | Testing |
| Essentials | 50,000/mo | $20/mo | If GHL bounces emails |
| Pro | 1.5M/mo | $90/mo | Enterprise only |

**Do You Need This?**
- 🔴 **NO** - GHL handles email already
- 🟡 **MAYBE** if: GHL emails land in spam consistently

**Alternatives:**
- Postmark: $15/mo (10K emails)
- Mailgun: $35/mo (50K emails)
- AWS SES: $0.10 per 1,000 emails (cheapest but technical)

---

### **7. Octoparse - $0-209/month** (OPTIONAL)

**Purpose:** Visual web scraper for NPC results pages, competitor websites

**What You Get:**
- No-code point-and-click scraper
- Scheduled scraping
- Cloud-based (no local software)
- Export to CSV, Excel, database

**Pricing:**
| Plan | Tasks | Cost | Cloud Run Time | Your Fit |
|------|-------|------|----------------|----------|
| Free | 10 | $0 | N/A (local only) | Testing |
| Standard | 20 | $75/mo | 10,000 min/mo | 🟡 If scraping 5+ websites |
| Professional | 100 | $209/mo | 100,000 min/mo | ❌ Overkill |

**Your Use Cases:**
- Scrape NPC official results pages (npcnewsonline.com)
- Scrape competitor show websites (rosters, results)
- Monitor competitor pricing pages
- Track venue availability

**Alternative:**
- **ParseHub:** $0-499/mo (similar to Octoparse)
- **Beautiful Soup + Python:** $0 (DIY coding)
- **n8n HTML node:** $0 (built into n8n, but limited)

**Do You Need This?**
- 🟡 **MAYBE** - Only if you want to scrape 5+ competitor websites regularly
- 🔴 **NO** if sticking to Instagram/Facebook only

---

### **8. Apollo.io - $0-149/month** (OPTIONAL)

**Purpose:** Enrich scraped profiles with email addresses and phone numbers

**What You Get:**
- B2B contact database (275M contacts)
- Email finder/verifier
- Phone number lookup
- Company data
- Chrome extension

**Pricing:**
| Plan | Credits/Month | Cost | Email Finder | Your Fit |
|------|---------------|------|--------------|----------|
| Free | 60 | $0 | 10/mo | Testing |
| Basic | 12,000 | $49/mo | Unlimited | 🟡 If need emails |
| Professional | 24,000 | $79/mo | Unlimited + Phone | 🟡 Premium |
| Organization | 48,000 | $149/mo | Advanced | ❌ Overkill |

**Your Use Case:**
- Find email addresses for scraped Instagram athletes
  - Input: Instagram username + name
  - Output: Email address (if found in Apollo database)
- Success rate: 30-50% (many athletes not in B2B databases)

**Alternative:**
- **Hunter.io:** $49-399/mo (email finder)
- **Clearbit:** $99-999/mo (expensive, overkill)
- **Manual email collection:** Free (check Instagram bio, website links)

**Do You Need This?**
- 🟡 **MAYBE** - Helpful for email outreach, but Instagram DMs may be more effective
- 🔴 **NO** if focusing on Instagram DMs + event registration forms for email capture

---

### **9. Brand24 - $79-399/month** (OPTIONAL)

**Purpose:** Social media monitoring, brand mentions, sentiment analysis

**What You Get:**
- Monitor keywords across social media (#NPCTexas, #RonnieColeman, competitor show names)
- Sentiment analysis (positive/negative/neutral)
- Influencer identification
- Real-time alerts
- Competitive analysis

**Pricing:**
| Plan | Mentions/Month | Cost | Keywords | Your Fit |
|------|----------------|------|----------|----------|
| Individual | 2,000 | $79/mo | 3 | 🟡 Basic monitoring |
| Team | 5,000 | $149/mo | 7 | 🟡 Recommended |
| Pro | 25,000 | $249/mo | 12 | ❌ Too much |
| Enterprise | 100,000 | $399/mo | 25 | ❌ Way too much |

**Your Use Cases:**
- Monitor #RonnieColeman Classic mentions
- Track competitor show hashtags
- Identify negative sentiment early
- Find influencers talking about NPC shows
- Real-time crisis alerts

**Alternative:**
- **Mention:** $29-99/mo (simpler, cheaper)
- **Hootsuite:** $99-739/mo (social management + monitoring)
- **Manual monitoring:** Free (search hashtags daily yourself)
- **Google Alerts:** Free (basic web monitoring)

**Do You Need This?**
- 🔴 **NO** for MVP - manual monitoring is sufficient early on
- 🟡 **MAYBE** once you're running 3+ events/year and need automated monitoring

---

## 🎯 RECOMMENDED STARTER STACK

### **Tier 1: MVP (START HERE) - $84-119/month**

```
┌─────────────────────────────────────┐
│ ESSENTIAL TOOLS ONLY                │
├─────────────────────────────────────┤
│ n8n Cloud        $20/mo  (automation)│
│ Apify            $49/mo  (scraping)  │
│ Claude API       $15-50  (AI)        │
│ GoHighLevel      (existing)          │
├─────────────────────────────────────┤
│ TOTAL:           $84-119/month       │
└─────────────────────────────────────┘

What You Can Do:
✅ Scrape 500-2,000 Instagram profiles/month
✅ AI analysis & scoring (recruitmentPotential)
✅ Auto-add qualified athletes to GHL
✅ Trigger email/SMS outreach campaigns
✅ Track conversions & ROI

Expected Results:
- 500 profiles scraped/month
- 150-200 qualified leads to GHL/month
- 10-20 new athlete registrations/month
- $1,200-2,400 revenue/month
- ROI: 1,010-2,757%
```

**After 3 Months Success, Add:**

### **Tier 2: Scale ($134-204/month)**

Add these when you're seeing ROI and want to scale:
- ManyChat ($15/mo) - Automate Instagram DMs
- Apify extra credits ($15-50/mo) - Scrape 5,000+ profiles/month

**Expected Results:**
- 2,000-5,000 profiles scraped/month
- 600-1,000 qualified leads/month
- 30-50 new athlete registrations/month
- $3,600-6,000 revenue/month
- ROI: 1,664-3,731%

---

## 💡 COST OPTIMIZATION STRATEGIES

### **How to Stay Under $100/month:**

1. **Use GHL AI Instead of Claude** ($97/mo additional vs $15-50)
   - ❌ Don't: Lower quality analysis
   - ✅ Consider: For email copy generation only

2. **Manual DMs Instead of ManyChat** (Save $15/mo)
   - ✅ Do: Send 20-30 manual DMs/day for first 3 months
   - Add ManyChat once overwhelmed

3. **Start with Instagram Only** (Apify covers this)
   - Skip Facebook scraping initially
   - Skip website scraping initially
   - Focus on highest ROI source first

4. **Use n8n Haiku Model** (60% cheaper than Sonnet)
   - Input: $0.25/1M tokens (vs $3)
   - Output: $1.25/1M tokens (vs $15)
   - Cost per profile: $0.003 vs $0.0084
   - Monthly savings: $10-15

5. **Batch Process Weekly Instead of Daily**
   - Reduce API calls
   - Lower Claude costs
   - Still effective for recruitment

**Optimized MVP Stack: $69-104/month**
- n8n: $20
- Apify: $49
- Claude (Haiku): $5-15
- GHL: (existing)
- Manual DMs: $0
- **TOTAL: $74-84/month**

---

## 📈 SCALING COST PROJECTION (12 Months)

| Month | Profiles/Mo | Tools Cost | Revenue Impact | ROI |
|-------|-------------|------------|----------------|-----|
| 1 | 500 | $84 | $1,200-2,400 | 1,329-2,757% |
| 2 | 1,000 | $94 | $2,400-4,800 | 2,453-5,006% |
| 3 | 1,500 | $104 | $3,600-7,200 | 3,362-6,823% |
| 4-6 | 2,000 | $134 | $4,800-9,600 | 3,482-7,064% |
| 7-9 | 3,000 | $164 | $7,200-14,400 | 4,290-8,683% |
| 10-12 | 5,000 | $204 | $12,000-24,000 | 5,782-11,665% |

**12-Month Total:**
- **Investment:** $1,600-1,800
- **Revenue Impact:** $50,000-100,000+
- **Net Gain:** $48,200-98,200
- **ROI:** 3,011-5,455%

---

## 🔒 WHAT'S NOT INCLUDED (Optional Add-Ons Later)

| Service | Cost | Purpose | When to Add |
|---------|------|---------|-------------|
| Video content tools (Synthesia) | $29-89/mo | AI video generation | Month 6+ |
| Advanced analytics (Mixpanel) | $0-899/mo | Deep data analysis | Month 12+ |
| Customer data platform (Segment) | $0-120/mo | Data unification | Enterprise |
| A/B testing (Optimizely) | $50-999/mo | Conversion optimization | Month 9+ |
| Live chat (Intercom) | $74-395/mo | Website chat | If high traffic |
| Review management (Podium) | $289+/mo | Automated review requests | If GHL insufficient |

**None of these are needed for MVP success.**

---

## ✅ FINAL RECOMMENDATION

### **Month 1-3: Start with $84-119/month**
- n8n Cloud
- Apify
- Claude API (Sonnet)
- GHL (existing)

### **Month 4-6: Scale to $134-204/month**
- Add ManyChat
- Increase Apify credits

### **Month 7-12: Optimize at $164-264/month**
- Add Octoparse (if needed)
- Add Apollo.io (if email needed)
- Maximize automation

### **Month 12+: Evaluate ROI**
- If crushing it: Add premium tools
- If profitable: Keep lean stack
- If struggling: Cut back to MVP

**The $84-119/month MVP stack will generate $50K-100K in year 1. Start there.**
