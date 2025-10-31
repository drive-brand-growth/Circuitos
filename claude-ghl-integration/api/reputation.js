import Anthropic from '@anthropic-ai/sdk';

const anthropic = new Anthropic({
  apiKey: process.env.CLAUDE_API_KEY
});

const SYSTEM_PROMPT = `You are the Reputation Guardian for Circuit OS™, managing online reviews and reputation.

YOUR ROLE:
1. Generate authentic, personalized review responses
2. Match tone to review sentiment (5★ grateful, 1★ empathetic)
3. Handle negative reviews with offline resolution offers
4. Identify happy customers for review requests

RESPONSE FRAMEWORKS:

5-STAR REVIEWS:
- Personal greeting (use their name if provided)
- Reference specific detail from their review
- Reinforce community/brand values
- Future invitation or engagement

4-STAR REVIEWS:
- Thank them for honest feedback
- Address any mentioned concerns
- Invite them to discuss how to make it 5★
- Show continuous improvement commitment

1-3 STAR REVIEWS:
- Empathetic opening (never defensive)
- Acknowledge their specific issue
- Offer immediate offline resolution (call/email)
- Provide direct contact (owner/manager)
- Move conversation off public platform

TONE RULES:
- Authentic, human voice (not robotic)
- Match business personality (hardcore gym = direct, not corporate)
- Avoid generic phrases ("Thank you for your feedback" ❌)
- Show genuine care + specific details (proves we read it)

OUTPUT: Generate response that passes "Turing test" (sounds human)`;

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { review, business, action } = req.body;

  if (!review) {
    return res.status(400).json({
      error: 'Missing review data',
      usage: 'POST with: { "review": {...}, "business": {...}, "action": "respond|request" }'
    });
  }

  const actionType = action || 'respond';

  try {
    let prompt = '';

    if (actionType === 'respond') {
      prompt = `${SYSTEM_PROMPT}

REVIEW TO RESPOND TO:
Platform: ${review.platform || 'Google'}
Rating: ${review.rating}★
Reviewer: ${review.author_name || 'Anonymous'}
Review Text: "${review.text}"
Date: ${review.date || 'Recent'}

BUSINESS INFO:
${JSON.stringify(business, null, 2)}

Generate an authentic response. Return JSON:
{
  "response_text": "Full response here...",
  "tone": "grateful|empathetic|apologetic|celebratory",
  "urgency": "immediate|standard|routine",
  "follow_up_action": "call_customer|send_email|none",
  "sentiment_shift_prediction": "likely_positive|neutral|needs_escalation"
}`;
    } else if (actionType === 'request') {
      prompt = `You are generating a review request message for a happy customer.

CUSTOMER INFO:
${JSON.stringify(review, null, 2)}

BUSINESS INFO:
${JSON.stringify(business, null, 2)}

Create a personalized review request. Return JSON:
{
  "message_text": "SMS/Email message requesting review...",
  "platform_links": {
    "google": "https://g.page/...",
    "facebook": "https://fb.com/..."
  },
  "incentive": "none|discount|entry",
  "expected_conversion_rate": 0.40
}`;
    }

    const message = await anthropic.messages.create({
      model: 'claude-sonnet-4-20250514',
      max_tokens: 1500,
      temperature: 0.75,
      messages: [{
        role: 'user',
        content: prompt
      }]
    });

    const responseText = message.content[0].text;
    const jsonMatch = responseText.match(/\{[\s\S]*\}/);

    if (!jsonMatch) {
      throw new Error('No valid JSON in response');
    }

    const result = JSON.parse(jsonMatch[0]);
    result.generated_at = new Date().toISOString();
    result.action_type = actionType;
    result.api_version = '1.0.0';

    return res.status(200).json(result);

  } catch (error) {
    console.error('Error:', error);
    return res.status(500).json({
      error: 'Failed to process review',
      details: error.message
    });
  }
}
