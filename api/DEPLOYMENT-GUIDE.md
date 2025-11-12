# Claude Agent Memory - Deployment Guide
## ADK-Level Intelligence Without the Framework

**Time to Deploy:** 30-45 minutes
**Cost:** $0/month infrastructure + Claude API usage (~$50-300/mo)

---

## 🚀 QUICK START

### Prerequisites
- Claude API key (https://console.anthropic.com)
- Supabase account (https://supabase.com) - FREE tier
- Vercel account (https://vercel.com) - FREE tier
- Node.js 18+ installed locally

---

## STEP 1: Setup Supabase (10 minutes)

### 1.1 Create Supabase Project
```bash
# Go to https://supabase.com
# Click "New Project"
# Name: circuitos-memory
# Database Password: [generate strong password]
# Region: Choose closest to your users
# Click "Create new project"
```

### 1.2 Run Database Schema
```bash
# In Supabase Dashboard:
# 1. Go to "SQL Editor"
# 2. Click "New Query"
# 3. Copy contents of api/supabase-schema.sql
# 4. Paste and click "Run"
# 5. Verify tables created: conversation_history, agent_feedback, ml_retraining_queue
```

### 1.3 Get Supabase Credentials
```bash
# In Supabase Dashboard:
# 1. Go to "Settings" → "API"
# 2. Copy "Project URL" (looks like: https://xxxxx.supabase.co)
# 3. Copy "service_role" key (NOT anon key - we need full access)
# 4. Save these for Step 2
```

---

## STEP 2: Deploy to Vercel (15 minutes)

### 2.1 Install Dependencies
```bash
cd /home/user/Circuitos/api
npm install
```

### 2.2 Test Locally (Optional)
```bash
# Create .env.local for testing
cat > .env.local << 'EOF'
CLAUDE_API_KEY=sk-ant-api03-xxxxx
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.xxxxx
EOF

# Test locally
vercel dev

# In another terminal, test the API:
curl -X POST http://localhost:3000/api/claude-agent-memory \
  -H "Content-Type: application/json" \
  -d '{
    "action": "score-lead",
    "contactId": "test-123",
    "businessId": "biz-456",
    "useMemory": true,
    "data": {
      "contact": {
        "first_name": "John",
        "last_name": "Doe",
        "city": "Brooklyn",
        "custom_fields": {
          "distance_miles": "1.2",
          "intent_signal": "GMB_CALL"
        }
      },
      "business": {
        "name": "MetroFlex Gym",
        "category": "Fitness"
      }
    }
  }'
```

### 2.3 Deploy to Vercel Production
```bash
# Login to Vercel
npx vercel login

# Deploy
npx vercel --prod

# You'll get a URL like: https://your-project.vercel.app
```

### 2.4 Add Environment Variables to Vercel
```bash
# Add Claude API key
npx vercel env add CLAUDE_API_KEY production
# Paste your Claude API key when prompted

# Add Supabase URL
npx vercel env add SUPABASE_URL production
# Paste your Supabase URL

# Add Supabase service_role key
npx vercel env add SUPABASE_KEY production
# Paste your Supabase service_role key

# Redeploy with environment variables
npx vercel --prod
```

---

## STEP 3: Test the Deployment (5 minutes)

### 3.1 Test Lead Scoring with Memory
```bash
# Replace YOUR_VERCEL_URL with your actual URL
curl -X POST https://YOUR_VERCEL_URL/api/claude-agent-memory \
  -H "Content-Type: application/json" \
  -d '{
    "action": "score-lead",
    "contactId": "contact-abc123",
    "businessId": "business-xyz789",
    "useMemory": true,
    "data": {
      "contact": {
        "first_name": "Sarah",
        "last_name": "Johnson",
        "email": "sarah@example.com",
        "city": "Brooklyn",
        "custom_fields": {
          "distance_miles": "0.8",
          "median_income": "85000",
          "intent_signal": "GMB_DIRECTIONS_CLICKED"
        }
      },
      "business": {
        "name": "CrossFit Brooklyn",
        "category": "Fitness",
        "location": "123 Main St, Brooklyn NY"
      }
    }
  }'
```

**Expected Response:**
```json
{
  "total_score": 82,
  "breakdown": {
    "fit": 32,
    "intent": 34,
    "timing": 16
  },
  "grade": "A",
  "priority": "HIGH",
  "next_action": "IMMEDIATE_COLD_EMAIL",
  "confidence": "VERY_HIGH",
  "missing_data": [],
  "detailed_attribution": {
    "fit_reasons": [
      "Distance: 0.8mi (EXCELLENT - within 1 mile)",
      "Income: $85K (strong fit for $150/mo membership)"
    ],
    "intent_reasons": [
      "GMB directions clicked (HIGH INTENT - ready to visit)",
      "Active search behavior"
    ],
    "timing_reasons": [
      "Recent activity signals urgency"
    ]
  },
  "metadata": {
    "agent": "Lead Scorer",
    "model": "claude-sonnet-4-5-20250929",
    "conversationTurns": 1,
    "usedMemory": true,
    "tokens": {
      "input": 487,
      "output": 312,
      "total": 799
    }
  }
}
```

### 3.2 Test Multi-Agent Collaboration
```bash
# Now call Copywriter agent with SAME contactId
# Copywriter will see Lead Scorer's analysis in conversation history!
curl -X POST https://YOUR_VERCEL_URL/api/claude-agent-memory \
  -H "Content-Type: application/json" \
  -d '{
    "action": "generate-copy",
    "contactId": "contact-abc123",
    "businessId": "business-xyz789",
    "useMemory": true,
    "data": {
      "contact": {
        "first_name": "Sarah",
        "last_name": "Johnson",
        "city": "Brooklyn"
      },
      "channel": "EMAIL",
      "awareness_level": "Solution Aware",
      "business": {
        "name": "CrossFit Brooklyn",
        "category": "Fitness"
      }
    }
  }'
```

**Expected:** Copywriter generates copy that references the high intent score from Lead Scorer!

### 3.3 Verify Memory in Supabase
```sql
-- Go to Supabase SQL Editor and run:
SELECT
  contact_id,
  agent_name,
  role,
  LEFT(content, 100) as content_preview,
  created_at
FROM conversation_history
WHERE contact_id = 'contact-abc123'
ORDER BY created_at ASC;

-- You should see:
-- 1. Lead Scorer user message
-- 2. Lead Scorer assistant response (score: 82)
-- 3. Copywriter user message
-- 4. Copywriter assistant response (email variants)
```

---

## STEP 4: Connect to GoHighLevel (10 minutes)

### 4.1 Update GHL Workflow - Lead Scoring

In your GHL workflow, **replace the old one-shot API call** with the new memory-enabled version:

**OLD (No Memory):**
```json
{
  "action": "score-lead",
  "data": {
    "contact": {...},
    "business": {...}
  }
}
```

**NEW (With Memory):**
```json
{
  "action": "score-lead",
  "contactId": "{{contact.id}}",
  "businessId": "{{business.id}}",
  "useMemory": true,
  "data": {
    "contact": {
      "first_name": "{{contact.first_name}}",
      "last_name": "{{contact.last_name}}",
      "email": "{{contact.email}}",
      "city": "{{contact.city}}",
      "custom_fields": {
        "distance_miles": "{{contact.custom_fields.distance_miles}}",
        "median_income": "{{contact.custom_fields.median_income}}",
        "intent_signal": "{{contact.custom_fields.intent_signal}}"
      }
    },
    "business": {
      "name": "{{business.name}}",
      "category": "{{business.category}}",
      "location": "{{business.address}}"
    }
  }
}
```

**Webhook URL:** `https://YOUR_VERCEL_URL/api/claude-agent-memory`

### 4.2 Store Response in GHL Custom Fields

Map webhook response to custom fields:

```
{{webhook_response.total_score}} → custom_fields.lpr_score
{{webhook_response.breakdown.fit}} → custom_fields.fit_score
{{webhook_response.breakdown.intent}} → custom_fields.intent_score
{{webhook_response.breakdown.timing}} → custom_fields.timing_score
{{webhook_response.next_action}} → custom_fields.next_action
{{webhook_response.metadata.conversationTurns}} → custom_fields.agent_turns
```

### 4.3 Create Multi-Agent Workflow

**Workflow Structure:**
```
1. TRIGGER: New contact created
2. ACTION: Score lead (Lead Scorer agent with memory)
3. CONDITION: If lpr_score >= 70
4. ACTION: Generate copy (Copywriter agent with memory - sees Lead Scorer's work!)
5. ACTION: Send email using generated copy
6. WAIT: 24 hours
7. ACTION: Record feedback (did they respond? convert?)
```

---

## STEP 5: Enable ML Feedback Loop (5 minutes)

### 5.1 Record Feedback After Outreach

Add this to your GHL workflow **24 hours after sending email**:

```json
{
  "action": "record-feedback",
  "contactId": "{{contact.id}}",
  "data": {
    "conversationId": "{{webhook_response.metadata.conversationId}}",
    "predicted": "HIGH_INTENT",
    "actual": "{{contact.custom_fields.outcome}}",
    "learnedPatterns": {
      "signals": ["GMB_CALL", "PROXIMITY_<1MI"],
      "worked": "{{contact.custom_fields.converted}}",
      "industry": "{{business.category}}"
    }
  }
}
```

### 5.2 View ML Feedback Dashboard

In Supabase SQL Editor:

```sql
-- Get ML feedback summary
SELECT * FROM get_ml_feedback_summary();

-- See which agents are most accurate
SELECT * FROM agent_accuracy;

-- View conversations flagged for retraining
SELECT
  conversation_id,
  error_delta,
  priority,
  status,
  created_at
FROM ml_retraining_queue
WHERE status = 'PENDING'
ORDER BY priority DESC, created_at ASC;
```

---

## 🎉 YOU'RE DONE!

### What You Now Have:

✅ **Conversational Memory** - Agents remember all past interactions
✅ **Multi-Agent Collaboration** - Lead Scorer → Copywriter with shared context
✅ **ML Feedback Loop** - System learns from actual outcomes
✅ **Zero Infrastructure Cost** - Supabase + Vercel free tiers
✅ **ADK-Level Intelligence** - Without Google framework overhead
✅ **Production-Ready** - Deployed and integrated with GHL

---

## 📊 COST BREAKDOWN

| Item | Cost |
|------|------|
| Vercel hosting | **$0/mo** (free tier: 100GB bandwidth) |
| Supabase database | **$0/mo** (free tier: 500MB, 50K rows) |
| Claude API (1000 leads/mo) | **$80-120/mo** (usage-based) |
| **Total** | **$80-120/mo** |

**vs Google ADK:** Same or lower cost, more control, no vendor lock-in

---

## 🔧 TROUBLESHOOTING

### Issue: "Cannot connect to Supabase"
**Fix:** Verify environment variables are set correctly in Vercel:
```bash
npx vercel env ls
# Should show SUPABASE_URL and SUPABASE_KEY
```

### Issue: "Conversation history not loading"
**Fix:** Check Supabase RLS policies - ensure service_role key is used (not anon key)

### Issue: "Memory not persisting"
**Fix:** Verify tables were created:
```sql
SELECT table_name FROM information_schema.tables
WHERE table_schema = 'public';
```

### Issue: "High token usage"
**Fix:** Limit conversation history to recent turns:
```javascript
// In memory-manager.js
async getConversationHistory(contactId, maxTurns = 10) // Reduce from 20 to 10
```

---

## STEP 6: Enable Observability Features (15 minutes)

### 6.1 Deploy Observability Schema to Supabase

```bash
# In Supabase Dashboard:
# 1. Go to "SQL Editor"
# 2. Click "New Query"
# 3. Copy contents of api/supabase-observability-schema.sql
# 4. Paste and click "Run"
# 5. Verify tables created: error_log, executions, scheduled_jobs
```

### 6.2 Deploy Dashboard UIs

The observability UIs are static HTML files in `/public`:

```bash
# These are automatically deployed with your Vercel project:
# - /public/test.html → Test Interface
# - /public/errors.html → Error Dashboard
# - /public/executions.html → Execution History

# Access them at:
# https://YOUR_VERCEL_URL/test.html
# https://YOUR_VERCEL_URL/errors.html
# https://YOUR_VERCEL_URL/executions.html
```

### 6.3 Access Observability Dashboards

**🧪 Test Interface** - `https://YOUR_VERCEL_URL/test.html`
- Dry-run mode (no API cost)
- Step-by-step execution tracking
- Mock responses for testing
- Input validation
- Use this to test agents without triggering full GHL workflows!

**🚨 Error Dashboard** - `https://YOUR_VERCEL_URL/errors.html`
- View all errors with severity classification (CRITICAL/HIGH/MEDIUM/LOW)
- Filter by severity, context, resolution status
- Automatic retry tracking
- Critical error alerts
- Mark errors as resolved

**📊 Execution History** - `https://YOUR_VERCEL_URL/executions.html`
- View all API executions with full input/output
- Performance metrics by action
- Success rate tracking
- Token usage analytics
- Replay executions for debugging

### 6.4 Configure Slack Notifications (Optional)

For critical error alerts, add Slack webhook to Vercel:

```bash
# Add Slack webhook URL
npx vercel env add SLACK_WEBHOOK_URL production
# Paste your Slack webhook URL when prompted

# Redeploy
npx vercel --prod
```

To create a Slack webhook:
1. Go to https://api.slack.com/apps
2. Create new app → "From scratch"
3. Add "Incoming Webhooks" feature
4. Create webhook for your channel
5. Copy webhook URL

**What you'll get:** Automatic Slack messages for CRITICAL errors with full context.

### 6.5 Enable Error Tracking in Your API

The error tracking is **automatically integrated** into the memory API. No code changes needed!

**What's tracked:**
- ✅ All API errors with severity classification
- ✅ Retry attempts with exponential backoff
- ✅ Full error context (contact ID, business ID, stack traces)
- ✅ Slack notifications for CRITICAL errors
- ✅ Resolution tracking

**What's logged:**
- ✅ All API executions with full input/output
- ✅ Duration and token usage per execution
- ✅ Success/failure status
- ✅ Performance metrics by action
- ✅ Replay capability for debugging

### 6.6 Test Observability Features

**Test the Test Interface:**
```bash
# Visit https://YOUR_VERCEL_URL/test.html
# 1. Select "Score Lead" action
# 2. Enable "Dry Run" and "Use Mock Response"
# 3. Click "Run Test"
# 4. You should see step-by-step execution without API cost
```

**Test Error Tracking:**
```bash
# Trigger an error intentionally:
curl -X POST https://YOUR_VERCEL_URL/api/claude-agent-memory \
  -H "Content-Type: application/json" \
  -d '{"action": "invalid-action"}'

# Then visit https://YOUR_VERCEL_URL/errors.html
# You should see the error logged with MEDIUM severity
```

**Test Execution Tracking:**
```bash
# Run any valid API call (e.g., score-lead from Step 3)
# Then visit https://YOUR_VERCEL_URL/executions.html
# You should see the execution with full input/output data
```

### 6.7 Monitor Performance

**Key Metrics to Watch:**

1. **Success Rate** - Should be >95% for production
2. **Average Duration** - <3000ms for Lead Scorer, <5000ms for Copywriter
3. **Token Usage** - Track costs in Execution History dashboard
4. **Error Rate by Severity:**
   - CRITICAL: Should be 0 (if >0, investigate immediately)
   - HIGH: <1% (API failures, rate limits)
   - MEDIUM: <5% (network issues, timeouts)
   - LOW: <10% (validation errors)

---

## 📚 NEXT STEPS

1. **Monitor Usage:** Track Claude API costs in Anthropic Console + Execution History dashboard
2. **Tune Memory:** Adjust `maxTurns` based on conversation complexity
3. **Add Agents:** Create more agents (Channel Router, Content Creator, etc.)
4. **ML Training:** Build retraining pipeline using `ml_retraining_queue`
5. **Scale Up:** When you exceed free tiers, upgrade (still cheap!)
6. **Review Errors:** Check Error Dashboard weekly, resolve unresolved errors
7. **Optimize Performance:** Use Execution History to identify slow agents

---

## 🎯 COMPARISON: Before vs After

### BEFORE (One-Shot API Calls)
- ❌ No memory - agents forget everything
- ❌ No collaboration - each call independent
- ❌ Static - no learning from outcomes
- ❌ Simple - single-turn only

### AFTER (Memory-Enhanced Agents)
- ✅ Full memory - agents remember all interactions
- ✅ Multi-agent collaboration - shared context
- ✅ Self-improving - ML feedback loop
- ✅ ADK-level - multi-turn conversations

**Result:** Your Claude agents now match or exceed Google ADK capabilities!

---

**Questions?** Check the code comments or review the architecture doc.

**Ready to deploy?** Run through Steps 1-5 above.

**© 2025 Circuit OS™**
**Powered by Claude Sonnet 4.5 with Conversational Memory**
