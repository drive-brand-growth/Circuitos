# Webhook Retry Logic Handler - CircuitOS

## 🚨 CRITICAL - PREVENTS LOST LEADS

**Current Risk:** If webhook fails, hot lead reply is lost forever
**Impact:** Estimated 5-10% of webhook deliveries fail due to network issues
**Cost:** Lost revenue from missed replies (~$500-2000/month for avg business)
**Implementation Time:** 4 hours

---

## Problem Statement

**Webhooks that currently COULD fail:**
1. **Instantly.ai → GHL** (email replies from leads)
2. **GMB Reviews → GHL** (new reviews)
3. **Claude AI Employees → GHL** (AI responses)
4. **Virtual LPR Detection → GHL** (new lead detection)

**What happens now if webhook fails:**
- ❌ Lead reply never reaches GHL
- ❌ No workflow triggered
- ❌ No rep notification
- ❌ Lead goes cold (no follow-up)
- ❌ Revenue lost

**What we're building:**
- ✅ Automatic retry with exponential backoff
- ✅ Dead letter queue for failed webhooks
- ✅ Manual review process
- ✅ Alert system for critical failures
- ✅ Logging for debugging

---

## Architecture Overview

```
External Service (Instantly.ai, GMB, etc.)
   ↓
   POST webhook to Vercel Function (not directly to GHL)
   ↓
   Vercel Function: Webhook Relay with Retry Logic
   ↓
   TRY: Forward to GHL webhook URL
   ↓
   IF SUCCESS: Log success, return 200
   ↓
   IF FAILURE:
      → Retry 1 (wait 2s)
      → Retry 2 (wait 4s)
      → Retry 3 (wait 8s)
   ↓
   IF STILL FAILS:
      → Save to Supabase "failed_webhooks" table
      → Create GHL Task "Manual Review Required"
      → Send Slack/Email alert
      → Return 200 to external service (so they don't retry)
```

**Key insight:** Never return error to external service (Instantly, GMB) because:
- They might retry incorrectly or give up
- We handle retries ourselves with better logic
- We can manually recover from dead letter queue

---

## Part 1: Supabase Database Schema

### Create Failed Webhook Tracking Table

```sql
-- Table 1: Failed Webhooks (Dead Letter Queue)
CREATE TABLE failed_webhooks (
   id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
   source VARCHAR(100) NOT NULL, -- 'instantly', 'gmb', 'claude', 'virtual_lpr'
   webhook_type VARCHAR(100), -- 'email_reply', 'new_review', 'ai_response', 'lead_detected'
   payload JSONB NOT NULL, -- Full webhook payload
   ghl_webhook_url TEXT NOT NULL, -- Where it was supposed to go
   failure_reason TEXT, -- Error message
   retry_count INT DEFAULT 0,
   first_attempt_at TIMESTAMP DEFAULT NOW(),
   last_retry_at TIMESTAMP,
   status VARCHAR(50) DEFAULT 'pending', -- 'pending', 'retrying', 'failed', 'recovered', 'manual_review'
   manually_processed BOOLEAN DEFAULT false,
   processed_by VARCHAR(255), -- Staff member who manually fixed it
   processed_at TIMESTAMP,
   notes TEXT,
   created_at TIMESTAMP DEFAULT NOW()
);

-- Table 2: Webhook Success Log (for monitoring)
CREATE TABLE webhook_success_log (
   id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
   source VARCHAR(100) NOT NULL,
   webhook_type VARCHAR(100),
   response_time_ms INT, -- How long did GHL take to respond?
   ghl_response_status INT, -- HTTP status code
   retry_needed BOOLEAN DEFAULT false, -- Did it succeed on first try?
   retry_count INT DEFAULT 0,
   created_at TIMESTAMP DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_failed_webhooks_status ON failed_webhooks(status);
CREATE INDEX idx_failed_webhooks_source ON failed_webhooks(source);
CREATE INDEX idx_failed_webhooks_created ON failed_webhooks(created_at);
CREATE INDEX idx_webhook_success_source ON webhook_success_log(source);
CREATE INDEX idx_webhook_success_created ON webhook_success_log(created_at);
```

---

## Part 2: Vercel Function - Webhook Relay with Retry

### File: `/api/webhook-relay/instantly-reply.js`

```javascript
/**
 * Webhook Relay: Instantly.ai Email Replies
 *
 * Purpose: Receive webhooks from Instantly.ai, forward to GHL with retry logic
 * Endpoint: https://your-vercel.com/api/webhook-relay/instantly-reply
 *
 * Setup in Instantly.ai:
 * Webhook URL: https://your-vercel.com/api/webhook-relay/instantly-reply
 * Trigger: When lead replies to campaign
 */

import { createClient } from "@supabase/supabase-js";
import * as Sentry from "@sentry/node";

const supabase = createClient(
  process.env.SUPABASE_URL,
  process.env.SUPABASE_KEY
);

Sentry.init({ dsn: process.env.SENTRY_DSN });

export default async function handler(req, res) {
  if (req.method !== "POST") {
    return res.status(405).json({ error: "Method not allowed" });
  }

  const payload = req.body;
  const source = "instantly";
  const webhookType = "email_reply";
  const ghlWebhookUrl = process.env.GHL_WEBHOOK_URL_INSTANTLY_REPLY;

  console.log(`[Webhook Relay] Received ${webhookType} from ${source}`);

  // ALWAYS return 200 to Instantly.ai (we handle retries ourselves)
  // This prevents Instantly from retrying incorrectly
  res.status(200).json({
    status: "received",
    message: "Webhook processing initiated"
  });

  // Process webhook asynchronously (don't block response)
  processWebhookWithRetry(payload, source, webhookType, ghlWebhookUrl);
}

async function processWebhookWithRetry(payload, source, webhookType, ghlWebhookUrl) {
  const maxRetries = 3;
  const retryDelays = [2000, 4000, 8000]; // Exponential backoff: 2s, 4s, 8s
  let retryCount = 0;
  let success = false;
  let lastError = null;

  const startTime = Date.now();

  // Attempt delivery with retries
  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      console.log(`[Webhook Relay] Attempt ${attempt + 1}/${maxRetries + 1} to forward to GHL`);

      const response = await fetch(ghlWebhookUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
        timeout: 10000, // 10 second timeout
      });

      if (response.ok) {
        // SUCCESS!
        const responseTime = Date.now() - startTime;
        console.log(`[Webhook Relay] ✅ Success on attempt ${attempt + 1} (${responseTime}ms)`);

        success = true;
        retryCount = attempt;

        // Log success
        await supabase.from("webhook_success_log").insert({
          source,
          webhook_type: webhookType,
          response_time_ms: responseTime,
          ghl_response_status: response.status,
          retry_needed: attempt > 0,
          retry_count: retryCount,
        });

        break; // Exit retry loop
      } else {
        // GHL returned error status
        lastError = `GHL returned status ${response.status}: ${await response.text()}`;
        console.error(`[Webhook Relay] ❌ Attempt ${attempt + 1} failed: ${lastError}`);
      }
    } catch (error) {
      // Network error, timeout, or other exception
      lastError = error.message;
      console.error(`[Webhook Relay] ❌ Attempt ${attempt + 1} failed: ${lastError}`);

      Sentry.captureException(error, {
        tags: {
          source,
          webhook_type: webhookType,
          attempt: attempt + 1,
        },
        extra: { payload },
      });
    }

    // If not last attempt, wait before retrying
    if (attempt < maxRetries) {
      const delay = retryDelays[attempt];
      console.log(`[Webhook Relay] Waiting ${delay}ms before retry...`);
      await sleep(delay);
    }
  }

  // If all retries failed, save to dead letter queue
  if (!success) {
    console.error(`[Webhook Relay] 🚨 All ${maxRetries + 1} attempts failed. Saving to dead letter queue.`);

    const { data: failedWebhook, error } = await supabase
      .from("failed_webhooks")
      .insert({
        source,
        webhook_type: webhookType,
        payload,
        ghl_webhook_url: ghlWebhookUrl,
        failure_reason: lastError,
        retry_count: maxRetries,
        last_retry_at: new Date(),
        status: "failed",
      })
      .select()
      .single();

    if (error) {
      console.error("[Webhook Relay] Failed to save to dead letter queue:", error);
      Sentry.captureException(error);
      return;
    }

    // Create GHL task for manual review
    await createGHLManualReviewTask(failedWebhook);

    // Send alert to team
    await sendFailureAlert(failedWebhook);
  }
}

async function createGHLManualReviewTask(failedWebhook) {
  const ghlApiKey = process.env.GHL_API_KEY;
  const ghlLocationId = process.env.GHL_LOCATION_ID;

  // Extract lead email from payload (Instantly.ai specific)
  const leadEmail = failedWebhook.payload.email || failedWebhook.payload.lead_email;

  try {
    const response = await fetch("https://rest.gohighlevel.com/v1/tasks/", {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${ghlApiKey}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        title: `🚨 URGENT: Webhook Failed - ${failedWebhook.webhook_type}`,
        body: `A webhook from ${failedWebhook.source} failed after ${failedWebhook.retry_count + 1} attempts.

**Type:** ${failedWebhook.webhook_type}
**Lead:** ${leadEmail}
**Error:** ${failedWebhook.failure_reason}
**Failed At:** ${new Date(failedWebhook.created_at).toLocaleString()}

**Action Required:**
1. Review failed webhook in Supabase: ID ${failedWebhook.id}
2. Manually process the webhook (see payload below)
3. Mark as resolved in dead letter queue

**Payload:**
\`\`\`json
${JSON.stringify(failedWebhook.payload, null, 2)}
\`\`\`

**Manual Recovery:**
- Update contact in GHL with reply information
- Trigger appropriate workflow
- Notify sales rep

**Mark Complete:** Update Supabase record status to 'recovered'
        `,
        dueDate: new Date(Date.now() + 3600000).toISOString(), // Due in 1 hour
        assignedTo: process.env.GHL_OWNER_USER_ID, // Assign to business owner
        contactId: null, // Can't link to contact if webhook failed
        locationId: ghlLocationId,
      }),
    });

    if (response.ok) {
      console.log("[Webhook Relay] ✅ Created GHL manual review task");
    } else {
      console.error("[Webhook Relay] Failed to create GHL task:", await response.text());
    }
  } catch (error) {
    console.error("[Webhook Relay] Error creating GHL task:", error);
    Sentry.captureException(error);
  }
}

async function sendFailureAlert(failedWebhook) {
  // Option 1: Slack alert (if configured)
  if (process.env.SLACK_WEBHOOK_URL) {
    try {
      await fetch(process.env.SLACK_WEBHOOK_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          text: `🚨 Webhook Failure Alert`,
          blocks: [
            {
              type: "header",
              text: {
                type: "plain_text",
                text: "🚨 Webhook Failed - Manual Review Required",
              },
            },
            {
              type: "section",
              fields: [
                {
                  type: "mrkdwn",
                  text: `*Source:*\n${failedWebhook.source}`,
                },
                {
                  type: "mrkdwn",
                  text: `*Type:*\n${failedWebhook.webhook_type}`,
                },
                {
                  type: "mrkdwn",
                  text: `*Retries:*\n${failedWebhook.retry_count + 1} attempts`,
                },
                {
                  type: "mrkdwn",
                  text: `*Error:*\n${failedWebhook.failure_reason}`,
                },
              ],
            },
            {
              type: "actions",
              elements: [
                {
                  type: "button",
                  text: {
                    type: "plain_text",
                    text: "View in Supabase",
                  },
                  url: `${process.env.SUPABASE_URL}/project/default/editor/${failedWebhook.id}`,
                },
                {
                  type: "button",
                  text: {
                    type: "plain_text",
                    text: "View in GHL",
                  },
                  url: process.env.GHL_DASHBOARD_URL,
                  style: "primary",
                },
              ],
            },
          ],
        }),
      });
      console.log("[Webhook Relay] ✅ Sent Slack alert");
    } catch (error) {
      console.error("[Webhook Relay] Failed to send Slack alert:", error);
    }
  }

  // Option 2: Email alert (fallback if no Slack)
  if (process.env.ALERT_EMAIL) {
    // Use SendGrid, AWS SES, or other email service
    // Implementation depends on your email provider
    console.log(`[Webhook Relay] Email alert would be sent to ${process.env.ALERT_EMAIL}`);
  }
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

// Export config for Vercel
export const config = {
  api: {
    bodyParser: true,
    externalResolver: true,
  },
};
```

---

## Part 3: Additional Webhook Relays

### Duplicate the above function for each webhook type:

**File:** `/api/webhook-relay/gmb-review.js`
- Source: `gmb`
- Webhook Type: `new_review`
- GHL URL: `process.env.GHL_WEBHOOK_URL_GMB_REVIEW`

**File:** `/api/webhook-relay/virtual-lpr.js`
- Source: `virtual_lpr`
- Webhook Type: `lead_detected`
- GHL URL: `process.env.GHL_WEBHOOK_URL_VIRTUAL_LPR`

**File:** `/api/webhook-relay/claude-ai.js`
- Source: `claude`
- Webhook Type: `ai_response`
- GHL URL: `process.env.GHL_WEBHOOK_URL_AI_RESPONSE`

---

## Part 4: Dead Letter Queue Recovery Workflow

### GHL Workflow: "Retry Failed Webhooks" (Daily Cron)

**Trigger:** Scheduled - Daily at 9:00 AM

**Step 1: Query Failed Webhooks**
```javascript
API Call to Vercel:
GET https://your-vercel.com/api/webhook-recovery/get-failed

Returns: List of failed webhooks from last 7 days with status='failed'
```

**Step 2: For Each Failed Webhook, Attempt Manual Recovery**
```javascript
API Call to Vercel:
POST https://your-vercel.com/api/webhook-recovery/retry
Body: {
   "webhook_id": "{{failed_webhook.id}}"
}

This will:
1. Fetch webhook from Supabase
2. Attempt delivery to GHL (1 more time)
3. IF success:
      - Update status = 'recovered'
      - Close GHL task
      - Send success notification
4. IF still fails:
      - Increment retry_count
      - Update status = 'manual_review'
      - Keep GHL task open
```

**Step 3: Daily Report to Owner**
```
Send Email:
Subject: Daily Webhook Health Report

Body:
Hi {{owner.first_name}},

Here's yesterday's webhook performance:

✅ Successful webhooks: {{success_count}}
⚠️ Required retry: {{retry_success_count}} ({{retry_rate}}%)
🚨 Failed (manual review): {{failed_count}}

Failed Webhooks Requiring Attention:
{{#each failed_webhooks}}
   - {{source}} / {{webhook_type}} ({{retry_count}} attempts)
     Error: {{failure_reason}}
     [View in GHL]({{ghl_task_url}})
{{/each}}

Average response time: {{avg_response_time}}ms
Reliability: {{(success_count / total_webhooks * 100)}}%

Dashboard: [View Supabase Dashboard]

Regards,
CircuitOS Monitoring System
```

---

## Part 5: Vercel Function - Webhook Recovery Endpoints

### File: `/api/webhook-recovery/get-failed.js`

```javascript
import { createClient } from "@supabase/supabase-js";

const supabase = createClient(
  process.env.SUPABASE_URL,
  process.env.SUPABASE_KEY
);

export default async function handler(req, res) {
  if (req.method !== "GET") {
    return res.status(405).json({ error: "Method not allowed" });
  }

  const sevenDaysAgo = new Date(Date.now() - 7 * 24 * 60 * 60 * 1000);

  const { data: failedWebhooks, error } = await supabase
    .from("failed_webhooks")
    .select("*")
    .in("status", ["failed", "manual_review"])
    .gte("created_at", sevenDaysAgo.toISOString())
    .order("created_at", { ascending: false });

  if (error) {
    return res.status(500).json({ error: error.message });
  }

  return res.status(200).json({
    count: failedWebhooks.length,
    webhooks: failedWebhooks,
  });
}
```

### File: `/api/webhook-recovery/retry.js`

```javascript
import { createClient } from "@supabase/supabase-js";

const supabase = createClient(
  process.env.SUPABASE_URL,
  process.env.SUPABASE_KEY
);

export default async function handler(req, res) {
  if (req.method !== "POST") {
    return res.status(405).json({ error: "Method not allowed" });
  }

  const { webhook_id } = req.body;

  // Fetch failed webhook
  const { data: webhook, error } = await supabase
    .from("failed_webhooks")
    .select("*")
    .eq("id", webhook_id)
    .single();

  if (error || !webhook) {
    return res.status(404).json({ error: "Webhook not found" });
  }

  // Attempt delivery one more time
  try {
    const response = await fetch(webhook.ghl_webhook_url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(webhook.payload),
      timeout: 10000,
    });

    if (response.ok) {
      // SUCCESS! Update status
      await supabase
        .from("failed_webhooks")
        .update({
          status: "recovered",
          manually_processed: true,
          processed_at: new Date(),
          notes: "Auto-recovered via daily retry job",
        })
        .eq("id", webhook_id);

      return res.status(200).json({
        success: true,
        message: "Webhook recovered successfully",
      });
    } else {
      // Still failing
      await supabase
        .from("failed_webhooks")
        .update({
          status: "manual_review",
          retry_count: webhook.retry_count + 1,
          last_retry_at: new Date(),
          failure_reason: `Retry failed: ${response.status} ${await response.text()}`,
        })
        .eq("id", webhook_id);

      return res.status(500).json({
        success: false,
        message: "Webhook still failing - manual review required",
      });
    }
  } catch (error) {
    return res.status(500).json({
      success: false,
      error: error.message,
    });
  }
}
```

---

## Part 6: Environment Variables (Vercel)

### Add to Vercel Project Settings → Environment Variables

```bash
# GHL Webhook URLs (where to forward webhooks)
GHL_WEBHOOK_URL_INSTANTLY_REPLY=https://hooks.gohighlevel.com/v1/your-webhook-id-1
GHL_WEBHOOK_URL_GMB_REVIEW=https://hooks.gohighlevel.com/v1/your-webhook-id-2
GHL_WEBHOOK_URL_VIRTUAL_LPR=https://hooks.gohighlevel.com/v1/your-webhook-id-3
GHL_WEBHOOK_URL_AI_RESPONSE=https://hooks.gohighlevel.com/v1/your-webhook-id-4

# GHL API Credentials
GHL_API_KEY=your-ghl-api-key
GHL_LOCATION_ID=your-ghl-location-id
GHL_OWNER_USER_ID=your-ghl-owner-user-id
GHL_DASHBOARD_URL=https://app.gohighlevel.com/v2/location/your-location-id

# Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-supabase-anon-key

# Error Tracking
SENTRY_DSN=https://your-sentry-dsn

# Alerts
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK
ALERT_EMAIL=alerts@yourbusiness.com
```

---

## Part 7: External Service Configuration

### Update Webhook URLs in External Services

**Instantly.ai:**
```
Dashboard → Settings → Webhooks
Event: Lead Replied
OLD: https://hooks.gohighlevel.com/v1/your-webhook-id
NEW: https://your-vercel.com/api/webhook-relay/instantly-reply
```

**GMB (if using polling service):**
```
Webhook destination:
NEW: https://your-vercel.com/api/webhook-relay/gmb-review
```

**Virtual LPR Detection:**
```
Update detection script to POST to:
NEW: https://your-vercel.com/api/webhook-relay/virtual-lpr
```

---

## Part 8: Monitoring Dashboard (Supabase)

### Create Dashboard View in Supabase

```sql
-- View: Webhook Health Summary
CREATE VIEW webhook_health_summary AS
SELECT
   DATE(created_at) as date,
   source,
   COUNT(*) as total_deliveries,
   SUM(CASE WHEN retry_needed = false THEN 1 ELSE 0 END) as first_attempt_success,
   SUM(CASE WHEN retry_needed = true THEN 1 ELSE 0 END) as required_retry,
   AVG(response_time_ms) as avg_response_time,
   MAX(response_time_ms) as max_response_time
FROM webhook_success_log
GROUP BY DATE(created_at), source
ORDER BY date DESC;

-- View: Failed Webhooks Summary
CREATE VIEW failed_webhooks_summary AS
SELECT
   DATE(created_at) as date,
   source,
   webhook_type,
   status,
   COUNT(*) as count
FROM failed_webhooks
GROUP BY DATE(created_at), source, webhook_type, status
ORDER BY date DESC;
```

---

## Implementation Checklist

### Day 1: Database Setup

- [ ] Create Supabase tables (failed_webhooks, webhook_success_log)
- [ ] Create monitoring views (webhook_health_summary, failed_webhooks_summary)
- [ ] Test Supabase connection from Vercel

### Day 2: Vercel Functions

- [ ] Deploy `/api/webhook-relay/instantly-reply.js`
- [ ] Deploy `/api/webhook-relay/gmb-review.js`
- [ ] Deploy `/api/webhook-relay/virtual-lpr.js`
- [ ] Deploy `/api/webhook-recovery/get-failed.js`
- [ ] Deploy `/api/webhook-recovery/retry.js`
- [ ] Configure environment variables in Vercel

### Day 3: External Service Updates

- [ ] Update Instantly.ai webhook URL to Vercel endpoint
- [ ] Update GMB webhook URL (if applicable)
- [ ] Update Virtual LPR to post to Vercel endpoint
- [ ] Test each webhook with live data

### Day 4: GHL Workflows

- [ ] Create "Retry Failed Webhooks" scheduled workflow
- [ ] Test daily recovery job
- [ ] Set up Slack/email alerts

### Day 5: Testing & Validation

- [ ] Simulate webhook failure (disconnect GHL temporarily)
- [ ] Verify retry logic works (3 attempts, exponential backoff)
- [ ] Verify dead letter queue saves failed webhooks
- [ ] Verify GHL task creation for manual review
- [ ] Verify daily recovery job processes failed webhooks

---

## Expected Results

**Before Implementation:**
- ❌ Webhook failure rate: ~5-10%
- ❌ Lost leads: ~10-20 per month
- ❌ No visibility into failures
- ❌ No recovery mechanism

**After Implementation:**
- ✅ Webhook failure rate: <0.1% (99.9% reliability)
- ✅ Automatic recovery: 95% of failures recovered via retry
- ✅ Manual recovery: 5% require manual intervention (tracked in dead letter queue)
- ✅ Full visibility: Dashboard shows all webhook health metrics
- ✅ Alert system: Team notified within seconds of critical failures

**ROI:**
- Lost revenue prevented: ~$500-2000/month
- Implementation cost: ~4 hours × $100/hr = $400
- Payback period: <1 month
- Ongoing cost: $0 (uses existing infrastructure)

---

## Support

**Troubleshooting:**
- Check Vercel logs: `vercel logs`
- Check Supabase logs: SQL Editor → Query failed_webhooks table
- Check Sentry for error tracking
- Review GHL tasks created for manual review

**Common Issues:**
- **High retry rate:** GHL may be slow (optimize workflows)
- **Persistent failures:** Check GHL webhook URL is correct
- **No alerts:** Verify Slack webhook URL or email configured

---

**DEPLOY THIS IMMEDIATELY** to prevent losing hot leads from webhook failures.
