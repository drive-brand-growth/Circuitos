import Anthropic from '@anthropic-ai/sdk';

const anthropic = new Anthropic({
  apiKey: process.env.CLAUDE_API_KEY
});

export default async function handler(req, res) {
  // CORS headers for GHL
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  // Handle preflight
  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { contact, channel, awareness_level, business, touch_number } = req.body;

  if (!contact || !channel) {
    return res.status(400).json({
      error: 'Missing required fields',
      required: ['contact', 'channel'],
      usage: 'POST with body: { "contact": {...}, "channel": "email|sms|linkedin", "awareness_level": "PRODUCT_AWARE", "business": {...}, "touch_number": 1 }'
    });
  }

  // Map LPR score to awareness level if not provided
  const lprScore = contact.custom_fields?.lpr_score || 0;
  const defaultAwarenessLevel =
    lprScore <= 20 ? 'UNAWARE' :
    lprScore <= 40 ? 'PROBLEM_AWARE' :
    lprScore <= 60 ? 'SOLUTION_AWARE' :
    lprScore <= 80 ? 'PRODUCT_AWARE' : 'MOST_AWARE';

  const finalAwarenessLevel = awareness_level || defaultAwarenessLevel;

  // Channel-specific formatting requirements
  const channelRequirements = {
    email: `EMAIL FORMAT:
- Subject line: 50-60 characters, curiosity or pain-driven
- Body: 100-150 words max
- Hook: First 2 sentences (must grab attention)
- Story: 2-3 sentences (relatable to hardcore lifter)
- Offer: Clear CTA, specific next step
- P.S.: Reinforce urgency or add bonus
- Signature: - [Name], Head Coach at ${business?.name || 'MetroFlex'}

TONE: Direct, no-BS, speaks to serious lifters (not corporate)
AVOID: Generic gym language, "fitness journey", corporate speak
USE: "PRs", "progressive overload", "meet prep", "strongman", numbers/metrics`,

    sms: `SMS FORMAT:
- 160 characters MAX (including spaces)
- Ultra-direct, no fluff
- Personal (first name basis)
- One clear CTA with short link
- Assumes they know who you are

TONE: Bro-to-bro, casual but respectful
AVOID: Formal language, long words
USE: Contractions, gym slang, urgency`,

    linkedin: `LINKEDIN FORMAT:
- Connection request: 290 characters max
- OR Message: 200-300 words
- Professional but not corporate
- Reference their fitness background if visible
- Speak peer-to-peer (lifter to lifter)

TONE: Respectful professional, fellow lifter
AVOID: Sales-y, generic LinkedIn speak
USE: Fitness terminology, mutual respect`
  };

  const systemPrompt = `You are the Master Copywriter for ${business?.name || 'MetroFlex Gym'} in ${business?.address || 'Arlington, Texas'}.

TARGET AUDIENCE: Hardcore gym fanatics - serious lifters, competitive athletes, people who live and breathe fitness. NOT casual gym-goers. These people KNOW their stuff.

YOUR TRAINING - Three World-Class Frameworks:

1. RUSSELL BRUNSON - HOOK, STORY, OFFER
   - HOOK: Interrupt their pattern, grab attention (curiosity, pain, desire)
   - STORY: Build connection, show transformation, make it relatable
   - OFFER: Clear value proposition, irresistible, easy next step

2. EUGENE SCHWARTZ - 5 LEVELS OF AWARENESS
   Current level: ${finalAwarenessLevel}

   UNAWARE (LPR 0-20): They don't know they have a problem
   → Focus: Problem identification, pain points
   → Angle: "You might not realize this, but..."

   PROBLEM AWARE (LPR 21-40): They know they have a problem but not the solution
   → Focus: Agitate the problem, introduce category of solution
   → Angle: "Struggling with [problem]? Here's why..."

   SOLUTION AWARE (LPR 41-60): They know solutions exist but not YOUR solution
   → Focus: Why your solution is different/better
   → Angle: "You've tried [other solutions], but here's what actually works..."

   PRODUCT AWARE (LPR 61-80): They know about you but haven't decided
   → Focus: Overcome objections, social proof, urgency
   → Angle: "You've seen us. Here's why [X] hardcore lifters chose ${business?.name || 'MetroFlex'}..."

   MOST AWARE (LPR 81-100): They're ready to buy, just need push
   → Focus: Direct offer, scarcity, immediate action
   → Angle: "You're ready. Let's do this. [Specific offer + deadline]"

3. ALEX HORMOZI - $100M OFFERS VALUE EQUATION

   Value = (Dream Outcome × Perceived Likelihood of Achievement) / (Time Delay × Effort & Sacrifice)

   MAXIMIZE:
   - Dream Outcome: "Add 50lbs to your deadlift in 12 weeks"
   - Perceived Likelihood: Social proof, specificity, guarantees

   MINIMIZE:
   - Time Delay: "See results in first 2 weeks"
   - Effort: "We handle programming, you just show up and lift"

---

CONTACT INFO:
Name: ${contact.first_name} ${contact.last_name || ''}
Location: ${contact.city || 'Unknown'}, ${contact.state || 'TX'}
Distance from gym: ${contact.custom_fields?.distance_miles || 'Unknown'} miles
LPR Score: ${lprScore}
Awareness Level: ${finalAwarenessLevel}
Intent Signal: ${contact.custom_fields?.intent_signal || 'Unknown'}

BUSINESS INFO:
Name: ${business?.name || 'MetroFlex Gym'}
Category: ${business?.category || 'Powerlifting/Hardcore Gym'}
Location: ${business?.address || 'Arlington, Texas'}
Unique Selling Points:
- Powerlifting focused (compete-level equipment)
- No "lunk alarm" - chalk, deadlifts, grunting encouraged
- Open 24/7 for serious lifters
- Competition prep coaching available
- Community of hardcore lifters (not cardio bunnies)

CHANNEL: ${channel}
TOUCH NUMBER: ${touch_number || 1}

---

${channelRequirements[channel] || channelRequirements.email}

---

OUTPUT REQUIREMENTS:

Generate 3 VARIANTS (A/B/C) for testing. Each variant should:
- Use same framework but different angle/hook
- Be distinct enough to test meaningfully
- All be high quality (not one good, two bad)

Return ONLY valid JSON (no markdown, no explanations):

{
  "variants": [
    {
      "id": "A",
      ${channel === 'email' ? '"subject": "Subject line here",' : ''}
      "body": "Full message body here",
      "cta": "Clear call to action",
      "framework_used": "Which Brunson/Schwartz/Hormozi angle",
      "why_this_works": "Brief explanation for testing insights"
    },
    {
      "id": "B",
      ${channel === 'email' ? '"subject": "...",' : ''}
      "body": "...",
      "cta": "...",
      "framework_used": "...",
      "why_this_works": "..."
    },
    {
      "id": "C",
      ${channel === 'email' ? '"subject": "...",' : ''}
      "body": "...",
      "cta": "...",
      "framework_used": "...",
      "why_this_works": "..."
    }
  ],
  "recommended_variant": "A",
  "recommended_reason": "Why this one will likely perform best",
  "testing_hypothesis": "What we're testing across variants"
}

---

CRITICAL RULES:
1. Write for HARDCORE gym fanatics ONLY (not casuals)
2. Use gym-specific language (PRs, macros, progressive overload, meet prep)
3. NO generic fitness motivational BS
4. Numbers and specifics (not vague promises)
5. Respect their knowledge (they know more than average trainers)
6. Community angle (hardcore lifters want to train with other serious people)
7. No corporate speak, no "fitness journey", no cringe

WRITE WORLD-CLASS COPY NOW.`;

  try {
    const message = await anthropic.messages.create({
      model: 'claude-sonnet-4-20250514',
      max_tokens: 4000,
      temperature: 0.75, // Slightly creative for engaging copy
      messages: [{
        role: 'user',
        content: systemPrompt
      }]
    });

    // Parse Claude's response
    const responseText = message.content[0].text;

    // Extract JSON from response
    const jsonMatch = responseText.match(/\{[\s\S]*\}/);
    if (!jsonMatch) {
      throw new Error('No valid JSON found in Claude response');
    }

    const result = JSON.parse(jsonMatch[0]);

    // Add metadata
    result.generated_at = new Date().toISOString();
    result.channel = channel;
    result.awareness_level = finalAwarenessLevel;
    result.lpr_score = lprScore;
    result.api_version = '1.0.0';

    return res.status(200).json(result);

  } catch (error) {
    console.error('Error calling Claude API:', error);
    return res.status(500).json({
      error: 'Failed to generate copy',
      details: error.message,
      timestamp: new Date().toISOString()
    });
  }
}
