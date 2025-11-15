# METROFLEX EVENTS AI AGENT - TOOLS & SETUP GUIDE

## 🛠️ COMPLETE TOOL SPECIFICATIONS

---

## **TOOL 1: n8n Cloud**

### **Overview:**
- **Type:** Workflow automation platform (like Zapier/Make.com but better)
- **Deployment:** Cloud-hosted (managed)
- **Purpose:** Orchestrate all automation between Apify → Claude → GHL

### **Sign Up & Setup:**

**Step 1: Create Account**
```
1. Go to: https://n8n.cloud
2. Click "Start Free Trial"
3. Enter email + password
4. Verify email
5. Choose plan: Starter ($20/mo after trial)
```

**Step 2: Create Your First Workflow**
```
1. Click "Create New Workflow"
2. Name it: "NPC Competitor Scraper"
3. Click "Import from File"
4. Upload: n8n-npc-competitor-scraper-workflow.json (provided)
5. Workflow loads with all nodes pre-configured
```

**Step 3: Configure Credentials**

You'll need to add 3 credentials:

**A. Claude API Key**
```
1. In n8n, click "Credentials" (left sidebar)
2. Click "Add Credential"
3. Search for "HTTP Header Auth"
4. Name: "Claude API Key"
5. Add header:
   - Name: x-api-key
   - Value: [YOUR_CLAUDE_API_KEY from console.anthropic.com]
6. Save
```

**B. GHL Webhook URL**
```
1. In n8n, go to workflow
2. Find "Send to GHL" node
3. Click to edit
4. In URL field, enter your GHL webhook URL
5. Get this from GHL:
   - Go to GHL → Automations → Workflows
   - Create "Incoming Webhook" trigger
   - Copy webhook URL
   - Paste into n8n
6. Save
```

**C. Environment Variables**
```
1. In n8n, click "Settings" → "Environment Variables"
2. Add:
   - Name: GHL_WEBHOOK_URL
   - Value: [Your GHL webhook URL]
3. Save
```

**Step 4: Test Workflow**
```
1. Click "Execute Workflow" button (top right)
2. Send test data via webhook (see Testing section below)
3. Check execution log for errors
4. Verify data appears in GHL
```

### **n8n Features You'll Use:**

| Feature | What It Does | How You'll Use It |
|---------|--------------|-------------------|
| **Webhook Node** | Receives data from external services | Apify sends scraped data here |
| **Code Node** | Run JavaScript to transform data | Parse JSON, build prompts, format data |
| **HTTP Request Node** | Call external APIs | Claude API, GHL webhook |
| **Split In Batches** | Loop through arrays | Process 500 profiles one-by-one |
| **IF Node** | Conditional logic | Filter qualified vs rejected athletes |
| **Error Handling** | Catch and log failures | Retry failed API calls, log errors |
| **Scheduler** | Run workflows on schedule | Weekly scraping jobs |

### **n8n Useful Tips:**

- **Execution Log:** See every workflow run (success/failure) for 30 days
- **Manual Testing:** Click nodes to see input/output data
- **Debugging:** Console.log() in Code nodes shows in execution log
- **Variables:** Use `{{ $json.fieldName }}` to access data from previous nodes
- **Error Retry:** HTTP nodes have built-in retry (3 attempts)

### **n8n Limits (Starter Plan):**

| Limit | Value | Your Usage | Headroom |
|-------|-------|------------|----------|
| Workflow executions/month | 2,500 | ~100 | 96% unused |
| Active workflows | 20 | ~5 | 75% unused |
| Workflow run time | 5 minutes | ~2 min | Safe |
| Data retention | 30 days | N/A | Sufficient |

---

## **TOOL 2: Apify**

### **Overview:**
- **Type:** Web scraping platform
- **Purpose:** Scrape Instagram, Facebook, TikTok, websites
- **Why:** Handles proxies, CAPTCHAs, rate limits professionally

### **Sign Up & Setup:**

**Step 1: Create Account**
```
1. Go to: https://apify.com
2. Click "Sign Up Free"
3. Use email or Google account
4. Verify email
5. Choose plan: Personal ($49/mo after trial)
```

**Step 2: Find Instagram Scraper**
```
1. In Apify dashboard, click "Actors" (top menu)
2. Search: "Instagram Profile Scraper"
3. Recommended: "Instagram Profile Scraper" by Apify
4. Click "Try for free"
```

**Step 3: Configure Instagram Scraper**

**Basic Settings:**
```json
{
  "directUrls": [],
  "hashtags": [
    "NPCTexas",
    "TexasBodybuilding",
    "NPCBikini",
    "NPCMensPhysique",
    "DallasBodybuilding",
    "HoustonFitness"
  ],
  "locations": [],
  "resultsLimit": 500,
  "resultsType": "posts",
  "searchLimit": 100,
  "searchType": "hashtag",
  "addParentData": true,
  "enhanceUserSearchWithAge": false,
  "isUserTaggedFeedURL": false,
  "onlyPostsNewerThan": "",
  "proxy": {
    "useApifyProxy": true,
    "apifyProxyGroups": ["RESIDENTIAL"]
  }
}
```

**Advanced Settings:**
```json
{
  "extendOutputFunction": "",
  "extendScraperFunction": "",
  "customData": {},
  "pinnedPosts": false,
  "maxErrorCount": 3,
  "maxRequestRetries": 3
}
```

**Step 4: Set Up Webhook to n8n**

```
1. In Apify actor run settings, click "Webhooks"
2. Click "Add Webhook"
3. Event: "Actor run succeeded"
4. URL: [Your n8n webhook URL]
   - Get this from n8n: Open workflow → "Apify Webhook Trigger" node → Copy webhook URL
5. Payload template: "Default"
6. Save
```

**Step 5: Schedule Scraper**

```
1. In Apify, click "Schedules" (left sidebar)
2. Click "Create Schedule"
3. Name: "Weekly NPC Scraper"
4. Cron expression: "0 9 * * 0" (Every Sunday at 9am)
5. Actor: Instagram Profile Scraper
6. Input: Use config from Step 3
7. Save
```

### **Apify Scrapers You'll Use:**

| Scraper | Purpose | Credits/Run | Frequency |
|---------|---------|-------------|-----------|
| **Instagram Profile Scraper** | Scrape athlete profiles by hashtag | 500-1,000 | Weekly |
| **Instagram Hashtag Scraper** | Get posts for specific hashtags | 200-500 | Weekly |
| **Facebook Event Scraper** | Scrape competitor event attendee lists | 300-600 | Bi-weekly |
| **Web Scraper** (generic) | Scrape NPC results pages | 100-300 | Monthly |

### **Apify Best Practices:**

✅ **Use Residential Proxies:** Avoid Instagram blocks (already configured)
✅ **Limit Results:** Don't scrape more than you need (saves credits)
✅ **Schedule Off-Peak:** Run scrapers at night/weekends (less detection)
✅ **Monitor Credit Usage:** Check dashboard weekly
✅ **Save Datasets:** Download scraped data as backup (CSV export)

### **Apify Troubleshooting:**

| Issue | Solution |
|-------|----------|
| "Actor failed" | Check error log, usually rate limit or CAPTCHA |
| "No results" | Hashtag too niche, try broader tags |
| "Blocked by Instagram" | Reduce resultsLimit, add delay between requests |
| "Credits used too fast" | Lower resultsLimit or scrape less frequently |
| "Webhook not firing" | Check webhook URL is correct, test manually |

---

## **TOOL 3: Claude API (Anthropic)**

### **Overview:**
- **Type:** AI language model API
- **Purpose:** Analyze Instagram profiles, extract competitor intelligence
- **Model:** Claude 3.5 Sonnet (best quality/cost balance)

### **Sign Up & Setup:**

**Step 1: Create Anthropic Account**
```
1. Go to: https://console.anthropic.com
2. Click "Sign Up"
3. Enter email + password
4. Verify email
5. Add payment method (credit card)
```

**Step 2: Get API Key**
```
1. In console, click "API Keys" (left sidebar)
2. Click "Create Key"
3. Name: "Metroflex Events n8n"
4. Copy API key (starts with "sk-ant-...")
5. Save securely (you won't see it again)
```

**Step 3: Set Usage Limits (Optional but Recommended)**
```
1. In console, click "Settings" → "Billing"
2. Set monthly budget cap: $100
3. Set alert thresholds: $25, $50, $75
4. Add notification email
5. Save
```

**Step 4: Test API**

Using curl (command line):
```bash
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: YOUR_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{
    "model": "claude-3-5-sonnet-20241022",
    "max_tokens": 1024,
    "messages": [
      {"role": "user", "content": "Test message"}
    ]
  }'
```

Expected response:
```json
{
  "id": "msg_...",
  "type": "message",
  "role": "assistant",
  "content": [
    {
      "type": "text",
      "text": "This is Claude's response..."
    }
  ],
  "model": "claude-3-5-sonnet-20241022",
  "usage": {
    "input_tokens": 10,
    "output_tokens": 25
  }
}
```

### **Claude API Parameters (For n8n):**

Already configured in workflow, but here's what they mean:

```json
{
  "model": "claude-3-5-sonnet-20241022",
  // Options: claude-3-5-haiku (cheaper), claude-3-opus (premium)

  "max_tokens": 1024,
  // Maximum response length (1024 = ~750 words)
  // Lower = cheaper, but may truncate responses

  "temperature": 0.3,
  // Creativity (0-1). Lower = more consistent/factual
  // For data extraction, keep low (0.2-0.4)

  "messages": [
    {
      "role": "user",
      "content": "Your prompt here..."
    }
  ]
}
```

### **Claude Cost Optimization:**

| Strategy | Savings | Implementation |
|----------|---------|----------------|
| Use Haiku instead of Sonnet | 60% | Change model in n8n workflow |
| Reduce max_tokens to 512 | 20-30% | Adjust in workflow (if JSON fits) |
| Batch multiple profiles per call | 40% | Advanced: combine prompts |
| Cache system prompts | 50% on repeated text | Use prompt caching API |

**Recommended for MVP:** Stick with Sonnet, it's only $16/mo for 2,000 profiles

### **Claude API Limits:**

| Tier | Requests/Min | Tokens/Min | Cost |
|------|--------------|------------|------|
| Free Trial | 5 | 20,000 | $5 credit |
| Tier 1 (default) | 50 | 40,000 input / 40,000 output | Pay-as-you-go |
| Tier 2 (after $100 spent) | 1,000 | 80,000 input / 80,000 output | Pay-as-you-go |

**Your Usage:** ~10 requests/minute during workflow run (well under limit)

---

## **TOOL 4: GoHighLevel (GHL)**

### **Overview:**
- **Type:** All-in-one CRM & marketing automation
- **Purpose:** Store athlete contacts, run email/SMS campaigns
- **Plan Required:** Unlimited ($297/mo) or Agency

### **Setup Required:**

**Step 1: Create Custom Fields for Athletes**

```
1. Go to GHL → Settings → Custom Fields
2. Click "Add Custom Field"
3. Create these fields:

Contact Information:
- instagram_username (Text)
- instagram_url (URL)
- instagram_followers (Number)
- instagram_engagement_rate (Number)

NPC Competitor Data:
- npc_competitor (Dropdown: Yes/No)
- competitive_status (Dropdown: Active/Preparing/Off-Season/Retired/Unknown)
- division (Dropdown: Men's Physique/Classic/Bodybuilding/Bikini/Figure/Wellness)
- experience_level (Dropdown: Beginner/Intermediate/Advanced/Pro)

Location & Training:
- location (Text)
- gym (Text)
- coach (Text)

Shows:
- recent_shows (Long Text)
- upcoming_shows (Long Text)

AI Scoring:
- influence_score (Number 0-100)
- recruitment_potential (Number 0-100)
- recruitment_reason (Long Text)
- personalized_message (Long Text)
- priority (Dropdown: High/Medium/Low)

Meta:
- source (Text - default: "NPC_Competitor_Scraper")
- scraped_date (Date)
- profile_bio (Long Text)
```

**Step 2: Create Tags**

```
1. Go to GHL → Settings → Tags
2. Create tag categories:

Source Tags:
- NPC_Scraper
- Instagram_Scraper
- Facebook_Scraper
- Manual_Add

Competitor Tags:
- NPC_Competitor
- Fitness_Enthusiast
- First_Timer
- Experienced_Competitor

Division Tags:
- Division_Mens_Physique
- Division_Classic_Physique
- Division_Bodybuilding
- Division_Bikini
- Division_Figure
- Division_Wellness

Priority Tags:
- Priority_High
- Priority_Medium
- Priority_Low

Influence Tags:
- Influence_High (5K+ followers)
- Influence_Medium (1K-5K)
- Influence_Low (<1K)

Location Tags:
- Location_Dallas
- Location_Houston
- Location_Austin
- Location_San_Antonio
- Location_Texas
- Location_Oklahoma
- Location_Louisiana
```

**Step 3: Create Incoming Webhook**

```
1. Go to GHL → Automations → Workflows
2. Click "Create Workflow"
3. Name: "NPC Competitor Intake"
4. Trigger: "Incoming Webhook"
5. Copy webhook URL (save for n8n)
6. Add Actions:
   a. "Create/Update Contact"
      - Map fields from webhook to custom fields
      - Use email as unique identifier (or phone)
   b. "Add Tags"
      - Add tags from webhook data
   c. "Add to Campaign" (optional)
      - Trigger "New NPC Competitor" email sequence
7. Save & Activate
```

**Step 4: Create Outreach Campaigns**

**Campaign 1: High-Priority Athlete Outreach**
```
Trigger: Tag added "Priority_High"

Day 1: Email
Subject: "Compete at the Ronnie Coleman Classic?"
Body: {{ personalized_message }} (from custom field)
+ Registration link
+ Early bird discount

Day 3: SMS (if phone number available)
"Hey {{ firstName }}, did you see my email about Ronnie Coleman Classic? Would love to have you compete with us! [Link]"

Day 7: Follow-up Email
Subject: "Still interested in competing?"
Body: Testimonial from past athlete + urgency (early bird ends soon)

Day 14: Final touch
Email: "Last call - early bird closes Friday"
```

**Campaign 2: Medium-Priority Nurture**
```
Similar to above but longer timeline (14 days between touches)
```

### **GHL Webhook Payload Format:**

When n8n sends data to GHL, it should look like this:

```json
{
  "firstName": "John",
  "lastName": "Smith",
  "email": "",
  "phone": "",
  "customFields": {
    "instagram_username": "johnsmith_fitness",
    "instagram_url": "https://instagram.com/johnsmith_fitness",
    "instagram_followers": 5200,
    "instagram_engagement_rate": 4.5,
    "npc_competitor": "Yes",
    "competitive_status": "Active Competitor",
    "division": "Men's Physique",
    "experience_level": "Intermediate",
    "location": "Dallas, TX",
    "gym": "Metroflex Gym Arlington",
    "coach": "",
    "recent_shows": "Texas Shredder Classic 2024 (3rd place)",
    "upcoming_shows": "",
    "influence_score": 65,
    "recruitment_potential": 85,
    "recruitment_reason": "Active competitor in Dallas, good following, recently placed",
    "personalized_message": "Hey John! Saw your 3rd place finish at Texas Shredder - impressive! Would love to have you at Ronnie Coleman Classic...",
    "priority": "High",
    "source": "NPC_Competitor_Scraper",
    "scraped_date": "2024-01-15",
    "profile_bio": "IFBB Pro Men's Physique | Dallas, TX | Coach @..."
  },
  "tags": [
    "NPC_Scraper",
    "NPC_Competitor",
    "Division_Mens_Physique",
    "Experience_Intermediate",
    "Priority_High",
    "Influence_Medium",
    "Location_Dallas"
  ]
}
```

---

## **TOOL 5: ManyChat (OPTIONAL)**

### **Overview:**
- **Type:** Instagram DM automation
- **Purpose:** Auto-send DMs to scraped athletes
- **Plan:** Pro ($15/mo)

### **Setup:**

**Step 1: Connect Instagram**
```
1. Go to: https://manychat.com
2. Sign up with Facebook account
3. Click "Add Channel" → Instagram
4. Connect your Metroflex Events Instagram account
5. Grant permissions (DMs, comments, story replies)
```

**Step 2: Create DM Flow**

```
1. Click "Automation" → "New Flow"
2. Name: "NPC Competitor Outreach"
3. Trigger: "Manual" (you'll send via n8n webhook)
4. Add action: "Send Message"
5. Message template:

"Hey {{first_name}}! 👋

{{custom_message}}

We're hosting the Ronnie Coleman Classic in [City] on [Date] and would love to have you compete!

Interested? Reply YES for details or visit: [link]"

6. Add quick replies:
   - "YES, tell me more" → Trigger "More Info" flow
   - "Not interested" → End conversation
7. Save flow
```

**Step 3: Get ManyChat API Key**
```
1. Go to Settings → API
2. Generate API key
3. Copy for n8n integration
```

**Step 4: Integrate with n8n (Advanced)**

Add this node after "Filter Qualified Athletes" in n8n:

```json
{
  "type": "HTTP Request",
  "url": "https://api.manychat.com/fb/sending/sendContent",
  "method": "POST",
  "headers": {
    "Authorization": "Bearer YOUR_MANYCHAT_API_KEY",
    "Content-Type": "application/json"
  },
  "body": {
    "subscriber_id": "{{ $json.instagram_username }}",
    "data": {
      "version": "v2",
      "content": {
        "messages": [
          {
            "type": "text",
            "text": "{{ $json.personalizedOutreach }}"
          }
        ]
      }
    }
  }
}
```

### **ManyChat Limits:**

| Plan | Contacts | Cost | DMs/Day |
|------|----------|------|---------|
| Free | 50 | $0 | 50 |
| Pro | 1,000 | $15/mo | 1,000 |

---

## **INTEGRATION ARCHITECTURE**

```
┌─────────────────────────────────────────────────────────┐
│                     DATA FLOW                           │
└─────────────────────────────────────────────────────────┘

Step 1: SCRAPING
┌──────────┐
│  Apify   │ Scrapes Instagram hashtags (#NPCTexas)
│  Actor   │ Finds 500 athlete profiles
└────┬─────┘
     │ Webhook
     ▼

Step 2: AUTOMATION ENGINE
┌──────────┐
│   n8n    │ Receives scraped profiles (JSON)
│  Cloud   │ Loops through each profile (500x)
└────┬─────┘
     │
     ▼

Step 3: AI ANALYSIS
┌──────────┐
│  Claude  │ Analyzes each profile
│   API    │ Returns: isCompetitor, division, score
└────┬─────┘
     │
     ▼

Step 4: FILTERING
┌──────────┐
│   n8n    │ Filters: recruitmentPotential > 40?
│  Filter  │ YES → Continue | NO → Reject & log
└────┬─────┘
     │
     ▼ (200 qualified)

Step 5: CRM
┌──────────┐
│   GHL    │ Creates/updates contact
│   CRM    │ Adds tags, custom fields
└────┬─────┘
     │
     ▼

Step 6: OUTREACH
┌──────────┐
│   GHL    │ Triggers email/SMS campaign
│ Campaign │ Sends personalized outreach
└────┬─────┘
     │
     ▼

Step 7: CONVERSION
┌──────────┐
│ Athletes │ Click link → Register
│ Register │ Revenue generated
└──────────┘
```

---

## **TESTING CHECKLIST**

Before going live, test each component:

### **Test 1: Apify Scraper**
```
□ Run Instagram scraper manually
□ Verify 10-50 profiles scraped
□ Check JSON structure is correct
□ Confirm webhook fires to n8n
□ Execution time: <5 minutes
```

### **Test 2: n8n Workflow**
```
□ Import workflow JSON
□ Add all credentials (Claude, GHL)
□ Send test webhook with sample data
□ Verify each node executes successfully
□ Check Claude returns valid JSON
□ Confirm GHL receives data
□ Review execution log for errors
```

### **Test 3: Claude API**
```
□ Test API key with curl
□ Verify response format
□ Check token usage (~1,200 tokens/profile)
□ Confirm billing dashboard shows usage
```

### **Test 4: GHL Integration**
```
□ Send test contact via webhook
□ Verify contact created in GHL
□ Check custom fields populated
□ Confirm tags applied
□ Test campaign triggers correctly
```

### **Test 5: End-to-End**
```
□ Run full workflow with 10 test profiles
□ Verify all 10 process successfully
□ Check 5-7 qualify and go to GHL
□ Confirm outreach emails sent
□ Monitor for 24 hours for issues
```

---

## **MONITORING & MAINTENANCE**

### **Daily (5 minutes):**
- Check n8n execution log (any failures?)
- Monitor GHL new contacts (athletes added?)
- Review email campaign performance (open rates?)

### **Weekly (15 minutes):**
- Verify Apify scraper ran successfully
- Check Claude API usage vs budget
- Review qualified athlete count (trending up?)
- Analyze outreach response rates

### **Monthly (1 hour):**
- Review total costs vs budget
- Analyze ROI (athletes registered from scraping?)
- Optimize Claude prompts (improve accuracy?)
- Adjust filters (lower/raise recruitmentPotential threshold?)
- Update hashtags in Apify (new trending tags?)

---

## **TROUBLESHOOTING GUIDE**

| Issue | Likely Cause | Solution |
|-------|--------------|----------|
| n8n workflow fails | Missing API key | Check credentials are saved |
| Claude returns invalid JSON | Prompt unclear | Refine prompt, add "ONLY JSON" |
| GHL doesn't receive data | Webhook URL wrong | Verify GHL webhook URL |
| Apify scrapes 0 profiles | Hashtag too specific | Try broader hashtags |
| Too many low-quality leads | Filter too loose | Increase recruitmentPotential threshold to 50+ |
| API costs too high | Processing too many | Reduce Apify resultsLimit |
| Emails not sending | Campaign not triggered | Check GHL workflow trigger |

---

## **SECURITY BEST PRACTICES**

✅ **API Keys:**
- Never commit to Git
- Store in n8n credentials (encrypted)
- Rotate every 90 days
- Use separate keys for prod/test

✅ **Webhooks:**
- Use HTTPS only
- Add authentication headers (optional)
- Validate webhook source
- Rate limit incoming requests

✅ **Data Privacy:**
- Only scrape public profiles
- Don't store sensitive data
- Have privacy policy on website
- Allow opt-out from communications

✅ **Access Control:**
- Limit n8n access to 2-3 people
- Use 2FA on all accounts
- Don't share credentials via email

---

## **QUICK REFERENCE - ALL ACCOUNTS YOU NEED**

| Service | URL | Username | Purpose |
|---------|-----|----------|---------|
| n8n Cloud | n8n.cloud | [Your email] | Automation |
| Apify | apify.com | [Your email] | Scraping |
| Anthropic | console.anthropic.com | [Your email] | AI API |
| GoHighLevel | app.gohighlevel.com | [Your email] | CRM |
| ManyChat (optional) | manychat.com | [Facebook] | DM automation |

**Backup Credentials:** Store all API keys in password manager (1Password, LastPass, Bitwarden)

---

## **NEXT STEPS AFTER SETUP**

1. ✅ Run test workflow with 10 profiles
2. ✅ Verify data quality in GHL
3. ✅ Send 5-10 manual test emails
4. ✅ Monitor for 48 hours
5. ✅ Go live with weekly scraping
6. ✅ Measure results for 30 days
7. ✅ Optimize based on data

**You're ready to build! 🚀**
