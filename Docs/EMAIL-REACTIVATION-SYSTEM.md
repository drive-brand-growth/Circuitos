# Email Reactivation & Deliverability System
## Reputation Management + List Re-warming with Claude

**Version:** 1.0
**Date:** 2025-11-11
**Status:** Production Ready

---

## Executive Summary

**Problem:** Cold email lists = destroyed sender reputation = spam folder death

**Solution:** Strategic re-warming system using Claude + Instantly AI + proper infrastructure

**Result:**
- Safely reactivate dormant lists
- Maintain 95%+ deliverability
- Protect sender reputation
- Scale to 10K+ emails/day

---

## Table of Contents

1. [Current State Assessment](#current-state-assessment)
2. [Email Infrastructure Stack](#email-infrastructure-stack)
3. [Instantly AI vs Alternatives](#instantly-ai-vs-alternatives)
4. [List Segmentation Strategy](#list-segmentation-strategy)
5. [Re-warming Protocol](#re-warming-protocol)
6. [Claude-Powered Email Generation](#claude-powered-email-generation)
7. [Batch Import & Processing](#batch-import--processing)
8. [Reputation Management](#reputation-management)
9. [Deliverability Optimization](#deliverability-optimization)
10. [Implementation Roadmap](#implementation-roadmap)

---

## Current State Assessment

### ⚠️ Risks of Cold Email on Dormant Lists

**If you haven't touched a list in 6+ months:**
- 20-40% hard bounces (dead emails)
- 30-50% spam complaints
- Instant domain blacklist
- Gmail/Outlook flagging
- Sender reputation destroyed

**Timeline to recovery:** 6-12 months (if recoverable at all)

**Cost:** Lost domain, lost email infrastructure, lost opportunities

---

## Email Infrastructure Stack

### Recommended Setup (Production-Grade)

```
┌────────────────────────────────────────────────┐
│ SENDING INFRASTRUCTURE                         │
├────────────────────────────────────────────────┤
│ Primary: Instantly AI (recommended)            │
│ - Unlimited warmup accounts                    │
│ - Auto-rotation across domains                 │
│ - Built-in deliverability monitoring           │
│ - Cost: $97-197/mo                            │
│                                                │
│ Alternatives:                                  │
│ - Smartlead ($99/mo)                          │
│ - Lemlist ($59-99/mo)                         │
│ - Apollo.io ($49-99/mo)                       │
└────────────────────────────────────────────────┘
         ↓
┌────────────────────────────────────────────────┐
│ EMAIL WARMING                                  │
├────────────────────────────────────────────────┤
│ Built into Instantly AI:                       │
│ - 30-45 day warm-up period                    │
│ - Gradual send volume increase                │
│ - Real inbox interactions                      │
│ - Spam folder monitoring                       │
│                                                │
│ Or separate: Mailreach ($25/mo per inbox)     │
└────────────────────────────────────────────────┘
         ↓
┌────────────────────────────────────────────────┐
│ REPUTATION MONITORING                          │
├────────────────────────────────────────────────┤
│ - Google Postmaster Tools (FREE)              │
│ - Microsoft SNDS (FREE)                        │
│ - MXToolbox (FREE tier)                        │
│ - GlockApps ($49/mo - optional)               │
└────────────────────────────────────────────────┘
         ↓
┌────────────────────────────────────────────────┐
│ CLAUDE-POWERED EMAIL GENERATION               │
├────────────────────────────────────────────────┤
│ - Batch process lists                          │
│ - Segment by engagement history                │
│ - Generate personalized re-activation emails   │
│ - Quality scoring (85+ threshold)              │
│ - A/B variant generation                       │
└────────────────────────────────────────────────┘
```

---

## Instantly AI vs Alternatives

### Why Instantly AI is Best for Your Use Case

| Feature | Instantly AI | Smartlead | Lemlist | Apollo |
|---------|--------------|-----------|---------|--------|
| **Unlimited warmup accounts** | ✅ | ❌ (limited) | ❌ | ❌ |
| **Auto domain rotation** | ✅ | ✅ | ❌ | ❌ |
| **Built-in deliverability** | ✅ | ✅ | ⚠️ | ⚠️ |
| **List cleaning** | ✅ | ✅ | ✅ | ✅ |
| **API access** | ✅ | ✅ | ✅ | ✅ |
| **Price (10K contacts)** | $97/mo | $99/mo | $99/mo | $49/mo |
| **Re-warming support** | ✅ Excellent | ✅ Good | ⚠️ Basic | ❌ |
| **Reputation monitoring** | ✅ | ✅ | ⚠️ | ❌ |

**Recommendation:** **Instantly AI** ($97/mo Growth plan)

**Why:**
- Unlimited warmup (critical for your dormant list)
- Auto-rotation protects main domain
- Built-in deliverability monitoring
- API for Claude integration
- Best reputation management tools

---

## List Segmentation Strategy

### Before Importing: Segment by Age & Engagement

```javascript
/**
 * Segment dormant list by risk level
 */

const LIST_SEGMENTS = {
  // Segment 1: SAFE (lowest risk)
  RECENTLY_ENGAGED: {
    criteria: 'Last engagement 0-6 months ago',
    riskLevel: 'LOW',
    warmupNeeded: false,
    sendVolume: 'Full speed (1000/day)',
    approach: 'Standard re-engagement campaign'
  },

  // Segment 2: CAUTION (medium risk)
  MODERATELY_STALE: {
    criteria: 'Last engagement 6-12 months ago',
    riskLevel: 'MEDIUM',
    warmupNeeded: true,
    warmupDays: 14,
    sendVolume: 'Start 50/day → ramp to 500/day',
    approach: 'Gentle re-activation with value offer'
  },

  // Segment 3: HIGH RISK
  VERY_STALE: {
    criteria: 'Last engagement 12-24 months ago',
    riskLevel: 'HIGH',
    warmupNeeded: true,
    warmupDays: 30,
    sendVolume: 'Start 20/day → ramp to 200/day',
    approach: 'Permission-based re-opt-in campaign'
  },

  // Segment 4: DANGER ZONE
  ANCIENT: {
    criteria: 'Last engagement 24+ months ago',
    riskLevel: 'CRITICAL',
    warmupNeeded: true,
    warmupDays: 45,
    sendVolume: 'Start 10/day → max 100/day',
    approach: 'Sunset campaign (clean or confirm interest)'
  }
};
```

### Segmentation Checklist

Before importing your list to Instantly AI:

- [ ] Export list with engagement dates
- [ ] Calculate days since last engagement
- [ ] Tag each contact with segment (SAFE/CAUTION/HIGH/CRITICAL)
- [ ] Remove hard bounces (emails that bounced before)
- [ ] Remove unsubscribes
- [ ] Remove spam complaints
- [ ] Verify email format validity
- [ ] Check for role emails (info@, admin@, etc.)

---

## Re-warming Protocol

### Phase 1: Infrastructure Setup (Week 1)

**Day 1-2: Domain Setup**
```bash
# DON'T use your main domain (drn.com)
# Buy 3-5 similar domains for cold email:

Examples:
- drnagency.com (main: drn.com)
- getdrn.com
- drnmarketing.com
- workwithdrn.com

Cost: $12/domain/year × 5 = $60/year
```

**Day 3-4: DNS Configuration**
```
For each domain:
1. SPF record
2. DKIM record
3. DMARC record
4. Custom tracking domain (click/open tracking)
5. MX records (if using custom email)

Instantly AI provides exact DNS records to add.
```

**Day 5-7: Connect to Instantly AI**
```
1. Add domains to Instantly AI
2. Create 5-10 email accounts per domain
   - john@drnagency.com
   - sarah@drnagency.com
   - mike@getdrn.com
   - etc.

3. Start warmup (automatically handled by Instantly)
```

### Phase 2: Warmup Period (Weeks 2-6)

**Week 2-3: Domain Warming (14-21 days)**
```
Day 1-7:   Send 10 emails/day per account
Day 8-14:  Send 20 emails/day per account
Day 15-21: Send 50 emails/day per account

Instantly AI handles this automatically via warmup pool.
```

**Week 4-6: Gradual Real Sends**
```
Week 4: Send to SAFE segment only (50/day total)
Week 5: Increase to 100/day, add CAUTION segment
Week 6: Increase to 200/day, monitor deliverability
```

### Phase 3: Full Send (Week 7+)

**Send Volume by Segment:**
```
SAFE (0-6 months):     1000/day
CAUTION (6-12 months): 500/day
HIGH (12-24 months):   200/day
CRITICAL (24+ months): 100/day (sunset campaign)
```

---

## Claude-Powered Email Generation

### Re-activation Email Strategy

```typescript
/**
 * Claude Skill: Email Reactivation Campaign Generator
 */

interface EmailReactivationInput {
  segment: 'SAFE' | 'CAUTION' | 'HIGH' | 'CRITICAL';
  contactData: {
    firstName: string;
    lastName: string;
    company?: string;
    lastEngagement?: string;
    lastTopic?: string;
    industry?: string;
  };
  campaignGoal: 'RE_ENGAGE' | 'RE_OPT_IN' | 'SUNSET';
}

interface EmailReactivationOutput {
  subject: string;
  preview: string;
  body: string;
  cta: string;
  qualityScore: number;        // 0-100
  personalization: number;     // 0-100
  spamRisk: number;           // 0-100 (lower is better)
  abVariants: Array<{
    subject: string;
    body: string;
    expectedOpenRate: number;
  }>;
}
```

### Claude Prompt for Re-activation Emails

**Create Claude Project: "Email Reactivation"**

**System Prompt:**
```
You are an email deliverability expert specializing in re-activating dormant lists without destroying sender reputation.

YOUR MISSION:
Generate re-activation emails that:
1. Get opens (avoid spam filters)
2. Get clicks (re-engage contacts)
3. Get responses (prove they're interested)
4. Protect sender reputation

SEGMENT-SPECIFIC APPROACHES:

SAFE (0-6 months dormant):
- Approach: "Hey, we have something new for you"
- Tone: Friendly, value-first
- CTA: Direct (book a call, download resource)
- Personalization: Medium

CAUTION (6-12 months dormant):
- Approach: "It's been a while, here's what you missed"
- Tone: Warm, non-pushy
- CTA: Soft (reply if interested, click to update preferences)
- Personalization: High

HIGH RISK (12-24 months dormant):
- Approach: "Should I keep you on my list?"
- Tone: Permission-based, respectful
- CTA: Re-opt-in (click to stay subscribed)
- Personalization: Very high

CRITICAL (24+ months dormant):
- Approach: "Last chance to stay connected"
- Tone: Sunset campaign, give option to unsubscribe
- CTA: Confirm interest or unsubscribe
- Personalization: Maximum

DELIVERABILITY RULES:
- NO spam trigger words (free, guarantee, urgent, act now, limited time)
- NO ALL CAPS
- NO excessive punctuation!!!
- NO misleading subject lines
- YES personalization tokens
- YES plain text or minimal HTML
- YES clear unsubscribe link
- YES sender name (not company name alone)

OUTPUT FORMAT (JSON):
{
  "subject": "<50 chars, no spam words>",
  "preview": "<130 chars, complements subject>",
  "body": "<plain text preferred, max 200 words>",
  "cta": "<clear, single call to action>",
  "qualityScore": <0-100>,
  "personalization": <0-100>,
  "spamRisk": <0-100, lower is better>,
  "abVariants": [
    {
      "subject": "<variant 1>",
      "body": "<variant 1>",
      "expectedOpenRate": <estimated %>
    },
    {
      "subject": "<variant 2>",
      "body": "<variant 2>",
      "expectedOpenRate": <estimated %>
    }
  ]
}

CRITICAL: Emails must pass spam filters. Quality score >85 required.
```

### Example Email Generation

**Input:**
```json
{
  "segment": "CAUTION",
  "contactData": {
    "firstName": "Sarah",
    "company": "TechStart Inc",
    "lastEngagement": "2024-05-15",
    "lastTopic": "Marketing automation"
  },
  "campaignGoal": "RE_ENGAGE"
}
```

**Claude Output:**
```json
{
  "subject": "Sarah, quick question about your marketing automation",
  "preview": "Been a while since we talked - wanted to share something that might help",
  "body": "Hey Sarah,\n\nIt's been about 6 months since we last connected about marketing automation for TechStart.\n\nI wanted to reach out because we just released something I think you'd find useful based on our last conversation.\n\nWould you be open to a quick 2-minute demo? No pressure - just want to make sure you're getting value from my emails.\n\nIf not interested, totally cool - just hit reply and let me know to take you off the list.\n\nCheers,\nMike",
  "cta": "Reply 'YES' for the demo or 'NO' to unsubscribe",
  "qualityScore": 92,
  "personalization": 88,
  "spamRisk": 12,
  "abVariants": [
    {
      "subject": "Sarah, following up on marketing automation",
      "body": "...",
      "expectedOpenRate": 28
    },
    {
      "subject": "Quick question for TechStart",
      "body": "...",
      "expectedOpenRate": 31
    }
  ]
}
```

---

## Batch Import & Processing

### Claude-Powered Batch Processing System

**Step 1: Export Your List**
```csv
email,first_name,last_name,company,last_engagement,segment
sarah@techstart.com,Sarah,Johnson,TechStart Inc,2024-05-15,CAUTION
john@acme.com,John,Smith,Acme Corp,2023-11-20,HIGH
...
```

**Step 2: Upload to Claude Project**

Create a file: `batch-email-generation.ts`

```typescript
import Anthropic from '@anthropic-ai/sdk';
import * as fs from 'fs';
import * as csv from 'csv-parser';

const client = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY });

interface Contact {
  email: string;
  firstName: string;
  lastName: string;
  company?: string;
  lastEngagement?: string;
  segment: 'SAFE' | 'CAUTION' | 'HIGH' | 'CRITICAL';
}

interface GeneratedEmail {
  contact: Contact;
  subject: string;
  body: string;
  qualityScore: number;
  spamRisk: number;
}

/**
 * Batch process list and generate personalized emails
 */
async function batchGenerateEmails(csvFilePath: string): Promise<GeneratedEmail[]> {
  const contacts: Contact[] = [];

  // Read CSV
  await new Promise((resolve) => {
    fs.createReadStream(csvFilePath)
      .pipe(csv())
      .on('data', (row) => {
        contacts.push({
          email: row.email,
          firstName: row.first_name,
          lastName: row.last_name,
          company: row.company,
          lastEngagement: row.last_engagement,
          segment: row.segment as any
        });
      })
      .on('end', resolve);
  });

  console.log(`Processing ${contacts.length} contacts...`);

  const results: GeneratedEmail[] = [];

  // Process in batches of 100 to manage API rate limits
  const batchSize = 100;
  for (let i = 0; i < contacts.length; i += batchSize) {
    const batch = contacts.slice(i, i + batchSize);

    console.log(`Processing batch ${Math.floor(i / batchSize) + 1}...`);

    const batchResults = await Promise.all(
      batch.map(contact => generateEmailForContact(contact))
    );

    results.push(...batchResults);

    // Rate limiting: wait 1 second between batches
    if (i + batchSize < contacts.length) {
      await new Promise(resolve => setTimeout(resolve, 1000));
    }
  }

  console.log(`✅ Generated ${results.length} personalized emails`);

  return results;
}

/**
 * Generate email for single contact using Claude
 */
async function generateEmailForContact(contact: Contact): Promise<GeneratedEmail> {
  const prompt = buildPrompt(contact);

  const response = await client.messages.create({
    model: 'claude-sonnet-4-5',
    max_tokens: 2048,
    temperature: 0.7,  // Slight creativity for email variation
    messages: [{ role: 'user', content: prompt }]
  });

  const rawOutput = response.content[0].text;
  const jsonMatch = rawOutput.match(/\{[\s\S]*\}/);

  if (!jsonMatch) {
    throw new Error(`No JSON found for ${contact.email}`);
  }

  const generated = JSON.parse(jsonMatch[0]);

  // Only return emails with quality score >85
  if (generated.qualityScore < 85) {
    console.warn(`⚠️ Low quality score (${generated.qualityScore}) for ${contact.email}, retrying...`);
    // Could implement retry logic here
  }

  return {
    contact,
    subject: generated.subject,
    body: generated.body,
    qualityScore: generated.qualityScore,
    spamRisk: generated.spamRisk
  };
}

/**
 * Build prompt for Claude
 */
function buildPrompt(contact: Contact): string {
  const segmentApproach = getSegmentApproach(contact.segment);

  return `Generate a re-activation email for this contact:

Contact Info:
- Name: ${contact.firstName} ${contact.lastName}
- Company: ${contact.company || 'Unknown'}
- Last Engagement: ${contact.lastEngagement || 'Unknown'}
- Segment: ${contact.segment}

Segment Approach:
${segmentApproach}

Generate email following the deliverability rules and return JSON only.`;
}

function getSegmentApproach(segment: string): string {
  const approaches = {
    SAFE: 'Friendly, value-first. Direct CTA.',
    CAUTION: 'Warm, non-pushy. Soft CTA asking if they want to stay connected.',
    HIGH: 'Permission-based. Re-opt-in required. Very respectful.',
    CRITICAL: 'Sunset campaign. Give option to unsubscribe cleanly.'
  };
  return approaches[segment as keyof typeof approaches];
}

/**
 * Export to CSV for Instantly AI import
 */
function exportToCSV(emails: GeneratedEmail[], outputPath: string) {
  const csvHeader = 'email,first_name,subject,body,quality_score,spam_risk\n';
  const csvRows = emails.map(e =>
    `${e.contact.email},"${e.contact.firstName}","${e.subject}","${e.body.replace(/"/g, '""')}",${e.qualityScore},${e.spamRisk}`
  ).join('\n');

  fs.writeFileSync(outputPath, csvHeader + csvRows);
  console.log(`✅ Exported to ${outputPath}`);
}

/**
 * Main execution
 */
async function main() {
  console.log('🚀 Starting batch email generation...\n');

  const emails = await batchGenerateEmails('./dormant-list.csv');

  // Filter: Only emails with quality >85 and spam risk <20
  const highQuality = emails.filter(e =>
    e.qualityScore >= 85 && e.spamRisk < 20
  );

  console.log(`\n📊 Results:`);
  console.log(`Total processed: ${emails.length}`);
  console.log(`High quality: ${highQuality.length}`);
  console.log(`Filtered out: ${emails.length - highQuality.length}`);

  // Export to CSV for Instantly AI import
  exportToCSV(highQuality, './instantly-import.csv');

  // Generate summary report
  const avgQuality = emails.reduce((sum, e) => sum + e.qualityScore, 0) / emails.length;
  const avgSpamRisk = emails.reduce((sum, e) => sum + e.spamRisk, 0) / emails.length;

  console.log(`\nAverage quality score: ${avgQuality.toFixed(2)}`);
  console.log(`Average spam risk: ${avgSpamRisk.toFixed(2)}`);
  console.log(`\n✅ Ready to import to Instantly AI!`);
}

// Run
main().catch(console.error);
```

**Step 3: Run Batch Processing**
```bash
npm install @anthropic-ai/sdk csv-parser

export ANTHROPIC_API_KEY="your-key"

node batch-email-generation.ts
```

**Step 4: Import to Instantly AI**
```
1. Log in to Instantly AI
2. Go to "Campaigns" → "New Campaign"
3. Import CSV: instantly-import.csv
4. Map fields:
   - Email → email
   - First Name → first_name
   - Subject → subject
   - Body → body
5. Set sending schedule (start slow!)
6. Launch campaign
```

---

## Reputation Management

### Daily Monitoring Checklist

**Setup (One-time):**
1. Google Postmaster Tools
   - Add your domains
   - Verify DNS
   - Monitor daily

2. Microsoft SNDS
   - Register sending IPs
   - Check reputation color (green = good)

3. MXToolbox
   - Check blacklist status
   - Monitor DNS health

**Daily Checks (5 minutes):**
```
- [ ] Google Postmaster: Domain reputation (HIGH/MEDIUM/LOW)
- [ ] Microsoft SNDS: IP reputation color
- [ ] Instantly AI: Deliverability score
- [ ] Bounce rate <2%
- [ ] Spam complaint rate <0.1%
- [ ] Unsubscribe rate <0.5%
```

**Red Flags (Stop sending immediately):**
- ⛔ Bounce rate >5%
- ⛔ Spam complaints >0.3%
- ⛔ Domain reputation drops to LOW
- ⛔ IP blacklisted
- ⛔ Deliverability drops below 85%

---

## Deliverability Optimization

### Technical Checklist

**DNS Configuration (Critical):**
```
SPF Record:
v=spf1 include:_spf.instantly.ai ~all

DKIM Record:
(Provided by Instantly AI - copy exact value)

DMARC Record:
v=DMARC1; p=quarantine; rua=mailto:dmarc@yourdomain.com

Custom Tracking Domain:
track.yourdomain.com → CNAME to Instantly AI
```

**Email Content Best Practices:**
- ✅ Plain text or minimal HTML
- ✅ Personalization tokens ({{firstName}}, {{company}})
- ✅ 1-2 links maximum
- ✅ Clear unsubscribe link
- ✅ Physical address in footer
- ✅ From name = person name (not company)
- ✅ Reply-to = real monitored email
- ❌ NO attachments
- ❌ NO URL shorteners
- ❌ NO  image-only emails
- ❌ NO spam trigger words

**Spam Trigger Words to Avoid:**
```
FREE, Guarantee, Limited Time, Act Now, Urgent, Click Here,
Buy Now, Order Now, Apply Now, Sign Up Free, Get Started Now,
Exclusive Deal, Special Promotion, No Obligation, Risk-Free,
Double Your Income, Make Money, Lose Weight, etc.
```

---

## Implementation Roadmap

### Week 1: Setup

**Day 1:**
- [ ] Sign up for Instantly AI ($97/mo Growth plan)
- [ ] Purchase 3-5 warm domains ($60 total)
- [ ] Set up DNS records

**Day 2-3:**
- [ ] Create 10-15 email accounts
- [ ] Connect to Instantly AI
- [ ] Start warmup (automatic)

**Day 4-5:**
- [ ] Set up Google Postmaster Tools
- [ ] Set up Microsoft SNDS
- [ ] Create monitoring dashboard

**Day 6-7:**
- [ ] Export dormant list
- [ ] Segment by engagement date
- [ ] Clean list (remove bounces, unsubscribes)

### Week 2-3: Warmup Period

**Automatically handled by Instantly AI:**
- Day 1-7: 10 emails/day per account
- Day 8-14: 20 emails/day
- Day 15-21: 50 emails/day

**Your action:**
- Monitor warmup progress
- Check deliverability scores
- Prepare email content with Claude

### Week 4: Claude Email Generation

**Day 1-2:**
- [ ] Create Claude Project "Email Reactivation"
- [ ] Add system prompt
- [ ] Test with 10 sample contacts

**Day 3-4:**
- [ ] Run batch processing on full list
- [ ] Review generated emails
- [ ] Filter by quality score (>85)

**Day 5:**
- [ ] Export to CSV
- [ ] Import to Instantly AI
- [ ] Set up campaign

### Week 5: Soft Launch

**SAFE Segment (0-6 months):**
- [ ] Send 50/day for 3 days
- [ ] Monitor: Open rate, click rate, bounce rate
- [ ] Adjust if needed

**If metrics look good:**
- Open rate >20%
- Bounce rate <2%
- Spam complaints <0.1%

→ Proceed to increase

### Week 6: Scale Up

**SAFE Segment:**
- Increase to 200/day

**CAUTION Segment (6-12 months):**
- Start at 50/day

**Monitor daily, adjust based on deliverability**

### Week 7+: Full Scale

**Send volumes:**
- SAFE: 1000/day
- CAUTION: 500/day
- HIGH: 200/day
- CRITICAL: 100/day (sunset)

**Ongoing optimization:**
- A/B test subject lines
- Refine personalization
- Clean bounces weekly
- Review spam complaints

---

## Cost Breakdown

### Infrastructure

| Item | Cost | Notes |
|------|------|-------|
| Instantly AI | $97/mo | Growth plan (unlimited warmup) |
| Warm domains (5x) | $60/year | One-time setup |
| Email accounts | $0 | Included in Instantly |
| Claude API | ~$50/mo | Batch email generation (10K emails) |
| **Total** | **~$150/mo** | **After initial $60 setup** |

### Cost per Email

**Email generation (Claude):**
- ~500 tokens per email
- $0.003 per 1K input tokens
- Cost: ~$0.0015 per email

**Sending (Instantly AI):**
- Unlimited sends on Growth plan
- Cost: $0 marginal per email

**Total cost per email:** ~$0.002 (1/5th of a cent)

**For 10,000 emails:** ~$20 (Claude) + $97 (Instantly) = **$117 total**

---

## Success Metrics

### Week 1 Targets
- Warmup started
- Deliverability score: 70%+ (warming up)
- Domains configured correctly

### Week 4 Targets
- Warmup complete
- Deliverability score: 90%+
- Claude batch processing tested

### Week 8 Targets
- SAFE segment fully sent
- Open rate: >25%
- Bounce rate: <2%
- Spam complaints: <0.1%
- Re-engagement rate: >10%

### Month 3 Targets
- All segments processed
- Deliverability maintained: 95%+
- List cleaned (20-30% removed/unsubscribed)
- Re-activated: 15-20% of list
- Ready for ongoing campaigns

---

## Next Steps

### Immediate (Today)
1. Sign up for Instantly AI
2. Purchase 3 warm domains
3. Review dormant list

### This Week
1. Set up DNS records
2. Connect domains to Instantly AI
3. Start warmup
4. Segment list by engagement date

### Next Week
1. Create Claude Project for email generation
2. Test batch processing
3. Monitor warmup progress

### Month 1
1. Generate emails with Claude
2. Import to Instantly AI
3. Launch soft campaign (SAFE segment)
4. Monitor and optimize

---

## Conclusion

**DON'T:**
- ❌ Blast cold emails to dormant list
- ❌ Use main domain
- ❌ Skip warmup period
- ❌ Ignore deliverability signals

**DO:**
- ✅ Use Instantly AI for proper warmup
- ✅ Segment by engagement age
- ✅ Generate personalized emails with Claude
- ✅ Start slow, ramp gradually
- ✅ Monitor reputation daily

**Result:**
- Safely reactivate dormant list
- Maintain 95%+ deliverability
- Re-engage 15-20% of list
- Protect sender reputation
- Scale to 10K+ emails/day

---

**Status:** ✅ Ready to implement
**Timeline:** 8 weeks to full scale
**Cost:** ~$150/mo operational
**ROI:** 15-20% list reactivation

