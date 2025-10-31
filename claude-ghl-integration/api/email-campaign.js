import Anthropic from '@anthropic-ai/sdk';

const anthropic = new Anthropic({
  apiKey: process.env.CLAUDE_API_KEY
});

const SYSTEM_PROMPT = `You are the Email Campaign Manager for Circuit OS™, managing cold email campaigns via Instantly.ai.

YOUR ROLE:
1. Design 5-touch email sequences with optimal timing
2. Optimize deliverability (sender reputation, spam avoidance)
3. Create A/B test variants (subject, hook, CTA)
4. Monitor performance and adjust sequences dynamically

SEQUENCE STRATEGY:
- Touch 1 (Day 0): Intro + Value Prop
- Touch 2 (Day 3): Social proof + Case study
- Touch 3 (Day 6): Address objections
- Touch 4 (Day 10): Urgency + Scarcity
- Touch 5 (Day 14): Final breakup email

DELIVERABILITY RULES:
- Never exceed 50 emails/day per domain
- Monitor bounce rate (<5%), spam rate (<0.1%)
- Rotate sending domains for high volume
- Personalize every email (200+ attributes)

ENGAGEMENT LOGIC:
- IF opened 2+ times, no reply → Escalate to LinkedIn
- IF clicked link → Escalate to SMS
- IF replied → Mark hot, route to sales
- IF no opens after 3 touches → Pause campaign

OUTPUT FORMAT: Return JSON with campaign configuration for Instantly.ai`;

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { contact, campaign_type, business } = req.body;

  if (!contact) {
    return res.status(400).json({
      error: 'Missing contact data',
      usage: 'POST with: { "contact": {...}, "campaign_type": "cold_outreach", "business": {...} }'
    });
  }

  try {
    const message = await anthropic.messages.create({
      model: 'claude-sonnet-4-20250514',
      max_tokens: 6000,
      temperature: 0.7,
      messages: [{
        role: 'user',
        content: `${SYSTEM_PROMPT}

CONTACT DATA:
${JSON.stringify(contact, null, 2)}

BUSINESS DATA:
${JSON.stringify(business, null, 2)}

CAMPAIGN TYPE: ${campaign_type || 'cold_outreach'}

Create a 5-touch email sequence for this lead. Return JSON with:
{
  "campaign_name": "...",
  "sequence": [
    {
      "touch_number": 1,
      "day": 0,
      "subject_variants": ["A", "B", "C"],
      "body_variants": ["A", "B", "C"],
      "send_time": "10:00 AM local",
      "personalization_tokens": {...}
    }
  ],
  "deliverability_settings": {
    "daily_send_limit": 50,
    "warmup_mode": false,
    "sender_rotation": true
  },
  "success_metrics": {
    "target_open_rate": 0.45,
    "target_reply_rate": 0.08
  },
  "escalation_rules": {
    "email_opens_no_reply": "linkedin",
    "link_clicked": "sms",
    "replied": "hot_lead"
  }
}`
      }]
    });

    const responseText = message.content[0].text;
    const jsonMatch = responseText.match(/\{[\s\S]*\}/);

    if (!jsonMatch) {
      throw new Error('No valid JSON in response');
    }

    const result = JSON.parse(jsonMatch[0]);
    result.created_at = new Date().toISOString();
    result.api_version = '1.0.0';

    return res.status(200).json(result);

  } catch (error) {
    console.error('Error:', error);
    return res.status(500).json({
      error: 'Failed to create campaign',
      details: error.message
    });
  }
}
