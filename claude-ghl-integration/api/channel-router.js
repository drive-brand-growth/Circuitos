import Anthropic from '@anthropic-ai/sdk';

const anthropic = new Anthropic({
  apiKey: process.env.CLAUDE_API_KEY
});

const SYSTEM_PROMPT = `You are the Channel Router for Circuit OS™, making intelligent omnichannel escalation decisions.

YOUR ROLE:
Analyze engagement patterns and determine optimal next channel: Email → LinkedIn → SMS → Call

DECISION LOGIC:

IF Email (2+ opens, 1+ click, no reply):
→ Escalate to LinkedIn connection request

IF LinkedIn (connection accepted):
→ Send personalized LinkedIn DM

IF LinkedIn (engaged but no meeting):
→ Escalate to SMS follow-up

IF SMS (positive reply):
→ Schedule phone call

IF SMS (ignored):
→ Wait 7 days, retry email with new angle

IF No engagement after 14 days:
→ Archive for 90-day re-engagement

COMPLIANCE:
- Email: Implicit opt-in (business inquiry)
- SMS/Call: Explicit opt-in required
- Honor unsubscribe across ALL channels
- CAN-SPAM, TCPA, LinkedIn ToS compliant

TIMING OPTIMIZATION:
- Don't SMS after 9pm or before 8am local time
- Don't call on Sundays
- Wait 3-7 days between channel switches (avoid fatigue)
- Accelerate if high engagement velocity

OUTPUT: Return JSON with next channel, timing, and reasoning`;

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { contact, engagement_history } = req.body;

  if (!contact || !engagement_history) {
    return res.status(400).json({
      error: 'Missing required data',
      usage: 'POST with: { "contact": {...}, "engagement_history": {...} }'
    });
  }

  try {
    const message = await anthropic.messages.create({
      model: 'claude-sonnet-4-20250514',
      max_tokens: 2000,
      temperature: 0.3,
      messages: [{
        role: 'user',
        content: `${SYSTEM_PROMPT}

CONTACT DATA:
${JSON.stringify(contact, null, 2)}

ENGAGEMENT HISTORY:
${JSON.stringify(engagement_history, null, 2)}

Analyze the engagement and determine the next best channel. Return JSON:
{
  "next_channel": "email|linkedin|sms|call|archive",
  "recommended_delay_hours": 72,
  "reasoning": "Detailed explanation of decision",
  "message_angle": "Suggested messaging approach",
  "compliance_status": {
    "email_opted_in": true,
    "sms_opted_in": false,
    "can_contact": true
  },
  "engagement_velocity": "high|medium|low|none",
  "predicted_conversion_probability": 0.35,
  "alternative_channel_if_fails": "email"
}`
      }]
    });

    const responseText = message.content[0].text;
    const jsonMatch = responseText.match(/\{[\s\S]*\}/);

    if (!jsonMatch) {
      throw new Error('No valid JSON in response');
    }

    const result = JSON.parse(jsonMatch[0]);
    result.routed_at = new Date().toISOString();
    result.api_version = '1.0.0';

    return res.status(200).json(result);

  } catch (error) {
    console.error('Error:', error);
    return res.status(500).json({
      error: 'Failed to route channel',
      details: error.message
    });
  }
}
