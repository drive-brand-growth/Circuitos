/**
 * Master Copywriter API - World-Class Copy Generation
 * © 2025 CircuitOS™
 *
 * Routes between copywriting frameworks based on:
 * - Awareness level (Schwartz)
 * - Demographics (age, income, distance)
 * - Psychographics (intent signals, LPR score)
 * - Channel (Email, SMS, LinkedIn)
 * - Weather context (NEW - hyper-personalization) ✅
 *
 * Frameworks:
 * 1. Russell Brunson - Hook, Story, Offer
 * 2. Eugene Schwartz - 5 Levels of Awareness
 * 3. Donald Miller - StoryBrand
 * 4. Alex Hormozi - $100M Offers Value Equation
 */

import Anthropic from '@anthropic-ai/sdk';
import { getWeatherCopySuggestions } from '../lib/mcps/openweather.js';

const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY
});

export default async function handler(req, res) {
  // CORS
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const {
    contact,
    channel,
    awareness_level,
    business,
    touch_number,
    lead_source // "cold_email" or "website_traffic"
  } = req.body;

  // Validate required fields
  if (!contact || !channel || !business) {
    return res.status(400).json({
      error: 'Missing required fields',
      required: ['contact', 'channel', 'business']
    });
  }

  try {
    console.log('[Copywriter] Generating copy for:', contact.first_name, 'Channel:', channel);

    const message = await anthropic.messages.create({
      model: 'claude-sonnet-4-20250514',
      max_tokens: 3000,
      temperature: 0.75, // Slightly creative for engaging copy
      messages: [{
        role: 'user',
        content: `You are the Master Copywriter for ${business.name}.

TARGET AUDIENCE: ${business.target_audience || 'Hardcore gym fanatics - serious lifters, competitive athletes, people who live and breathe fitness. NOT casual gym-goers.'}

YOUR TRAINING - Four World-Class Frameworks:

1. RUSSELL BRUNSON - HOOK, STORY, OFFER
   - HOOK: Interrupt their pattern, grab attention (curiosity, pain, desire)
   - STORY: Build connection, show transformation, make it relatable
   - OFFER: Clear value proposition, irresistible, easy next step

2. EUGENE SCHWARTZ - 5 LEVELS OF AWARENESS
   Current level: ${awareness_level || 'UNKNOWN'}

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
   → Angle: "You've seen us. Here's why [X] hardcore lifters chose ${business.name}..."

   MOST AWARE (LPR 81-100): They're ready to buy, just need push
   → Focus: Direct offer, scarcity, immediate action
   → Angle: "You're ready. Let's do this. [Specific offer + deadline]"

3. DONALD MILLER - STORYBRAND (7-Part Framework)

   The hero's journey positioning YOU as the guide:

   1. A CHARACTER (The Hero = Your Customer)
      → "You're a serious lifter who's tired of commercial gyms..."

   2. HAS A PROBLEM (External, Internal, Philosophical)
      → External: Need a gym with real equipment
      → Internal: Feel judged at commercial gyms, need community
      → Philosophical: Believe serious training deserves serious environment

   3. MEETS A GUIDE (You = Yoda, not Luke)
      → "We've trained 100+ competitive lifters..."
      → Show empathy: "We get it - commercial gyms don't understand..."
      → Show authority: "47 guys who pull 500+ train here"

   4. WHO GIVES THEM A PLAN (3 simple steps)
      → Step 1: Book free week
      → Step 2: Train with us, meet the community
      → Step 3: Decide if you fit (no pressure)

   5. AND CALLS THEM TO ACTION (Direct + Transitional)
      → Direct: "Book Your Free Week"
      → Transitional: "Download our lifting program guide"

   6. THAT HELPS THEM AVOID FAILURE (Stakes)
      → "Don't waste another year in a gym that doesn't get you..."
      → "Stop training alone when you could be hitting PRs with the pack..."

   7. AND ENDS IN SUCCESS (Vision)
      → "Imagine hitting a new PR every month..."
      → "Picture yourself competing at nationals with your training partners..."

   **When to use StoryBrand:**
   - Solution Aware (41-60 LPR) - They need to see YOU as the guide
   - Educational content (not hard sell)
   - Building trust and positioning
   - Longer-form copy (200-300 words)
   - Cold leads who need nurturing

4. ALEX HORMOZI - $100M OFFERS VALUE EQUATION

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
Location: ${contact.city || 'Unknown'}, ${contact.state || ''}
Distance from business: ${contact.custom_fields?.distance_miles || 'Unknown'} miles
LPR Score: ${contact.custom_fields?.lpr_score || contact.custom_fields?.vlpr_score || 'Unknown'}
Awareness Level: ${awareness_level || 'Unknown'}
Intent Signal: ${contact.custom_fields?.intent_signal || contact.custom_fields?.vlpr_source || 'Unknown'}
Median Income (ZIP): $${contact.custom_fields?.median_income || 'Unknown'}
Lead Source: ${lead_source || 'Unknown'}

BUSINESS INFO:
Name: ${business.name}
Category: ${business.category || business.type}
Location: ${business.city}, ${business.state}
Unique Selling Points:
${business.usp || `
- Powerlifting focused (compete-level equipment)
- No "lunk alarm" - chalk, deadlifts, grunting encouraged
- Open 24/7 for serious lifters
- Competition prep coaching available
- Community of hardcore lifters (not cardio bunnies)
`}

CHANNEL: ${channel}
TOUCH NUMBER: ${touch_number || 1}
LEAD SOURCE: ${lead_source || 'website_traffic'}

---

LEAD SOURCE ROUTING:

${lead_source === 'cold_email' ? `
**COLD EMAIL LEAD (Instantly.ai)**

This lead came from a cold email campaign via Instantly.ai. They:
- Did NOT visit your website first
- May not know who you are yet
- Responded to an outbound email (POSITIVE signal!)

YOUR APPROACH:
- Acknowledge they don't know you yet
- Build credibility FAST (social proof, numbers, specifics)
- Assume they're comparing you to competitors
- Make it EASY to take next step (low friction)
- Respect that they replied (they're interested, but cautious)

TONE: Respectful, humble, grateful they replied. Not presumptuous.
AVOID: Acting like they know who you are, over-familiar tone
USE: "Thanks for replying", "Quick intro", "Here's what we do"
` : ''}

${lead_source === 'website_traffic' ? `
**WEBSITE TRAFFIC LEAD (Warm)**

This lead came from your website/GMB/organic search. They:
- Actively searched for you or found you organically
- Showed INTENT by visiting website/GMB
- Already know something about you

YOUR APPROACH:
- Leverage their existing knowledge
- Reference what they viewed ("Saw you checked out our pricing...")
- Higher urgency (they're shopping NOW)
- More direct/aggressive (they expect it)

TONE: Confident, direct, peer-to-peer
AVOID: Over-explaining who you are (they know)
USE: "Saw you visited...", "You checked out...", "Ready when you are"
` : ''}

${contact.custom_fields?.weather_temp || contact.weather ? `
---

**WEATHER CONTEXT (Hyper-Personalization)**

Current weather in ${contact.city || business.city}:
- Temperature: ${contact.custom_fields?.weather_temp || contact.weather?.temp}°F
- Condition: ${contact.custom_fields?.weather_condition || contact.weather?.condition}

WEATHER-BASED MESSAGING:
${getWeatherContext(contact.custom_fields?.weather_temp || contact.weather?.temp, contact.custom_fields?.weather_condition || contact.weather?.condition, business.type)}

` : ''}

---

CHANNEL-SPECIFIC REQUIREMENTS:

${channel === 'email' ? `
EMAIL FORMAT:
- Subject line: 50-60 characters, curiosity or pain-driven
- Body: 100-150 words max
- Hook: First 2 sentences (must grab attention)
- Story: 2-3 sentences (relatable to target audience)
- Offer: Clear CTA, specific next step
- P.S.: Reinforce urgency or add bonus
- Signature: - [Name], ${business.signature || 'Head Coach'}

TONE: Direct, no-BS, speaks to target audience (not corporate)
AVOID: Generic language, "journey" speak, corporate jargon
USE: Specific numbers, metrics, industry terminology
` : ''}

${channel === 'sms' ? `
SMS FORMAT:
- 160 characters MAX (including spaces)
- Ultra-direct, no fluff
- Personal (first name basis)
- One clear CTA with short link
- Assumes they know who you are

TONE: Casual but respectful, peer-to-peer
AVOID: Formal language, long words
USE: Contractions, industry slang, urgency
` : ''}

${channel === 'linkedin' ? `
LINKEDIN FORMAT:
- Connection request: 290 characters max
- OR Message: 200-300 words
- Professional but not corporate
- Reference their background if visible
- Speak peer-to-peer

TONE: Respectful professional, fellow professional
AVOID: Sales-y, generic LinkedIn speak
USE: Industry terminology, mutual respect
` : ''}

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
      "subject": "Subject line here"${channel !== 'email' ? ' // Omit if not email' : ''},
      "body": "Full message body here",
      "cta": "Clear call to action",
      "framework_used": "Which Brunson/Schwartz/Hormozi angle",
      "why_this_works": "Brief explanation for testing insights"
    },
    {
      "id": "B",
      "subject": "...",
      "body": "...",
      "cta": "...",
      "framework_used": "...",
      "why_this_works": "..."
    },
    {
      "id": "C",
      "subject": "...",
      "body": "...",
      "cta": "...",
      "framework_used": "...",
      "why_this_works": "..."
    }
  ],
  "recommended_variant": "A",
  "recommended_reason": "Why this one will likely perform best",
  "testing_hypothesis": "What we're testing across variants",
  "lead_source_adapted": "${lead_source || 'website_traffic'}",
  "awareness_level_used": "${awareness_level || 'UNKNOWN'}"
}

---

CRITICAL RULES:
1. Write for TARGET AUDIENCE ONLY (respect their sophistication)
2. Use industry-specific language (show you understand their world)
3. NO generic motivational BS
4. Numbers and specifics (not vague promises)
5. Respect their intelligence and knowledge
6. Community angle (people want to be around similar people)
7. No corporate speak, no cringe
8. ${lead_source === 'cold_email' ? 'ACKNOWLEDGE they replied to cold email - be grateful' : 'LEVERAGE that they found you - they want you'}

WRITE WORLD-CLASS COPY NOW.`
      }]
    });

    const result = JSON.parse(message.content[0].text);

    console.log('[Copywriter] ✓ Generated', result.variants.length, 'variants');

    return res.status(200).json({
      success: true,
      copy: result,
      metadata: {
        lead_source: lead_source || 'website_traffic',
        awareness_level: awareness_level || 'UNKNOWN',
        channel,
        contact_name: contact.first_name
      }
    });

  } catch (error) {
    console.error('[Copywriter] Error:', error);
    return res.status(500).json({
      success: false,
      error: 'Failed to generate copy',
      message: error.message
    });
  }
}

/**
 * Generate weather-based copy suggestions
 * Adds hyper-personalization based on current weather
 */
function getWeatherContext(temp, condition, businessType = 'gym') {
  if (!temp || !condition) return '';

  let context = '';

  // Hot weather
  if (temp > 85) {
    context = `🔥 HOT WEATHER (${temp}°F):
- Hook: "With temps hitting ${temp}°F today..."
- Pain: "scorching heat," "brutal temperatures," "heat wave"
- Solution angle: "${businessType === 'gym' ? 'climate-controlled facility' : 'air-conditioned comfort'}"
- Benefit: "beat the heat," "stay cool while crushing goals"
- Urgency: "perfect time to work out indoors"
EXAMPLE: "While it's ${temp}°F outside, our facility stays a perfect 68°F..."`;
  }

  // Cold weather
  else if (temp < 50) {
    context = `❄️ COLD WEATHER (${temp}°F):
- Hook: "As temps drop to ${temp}°F..."
- Pain: "freezing cold," "brutal winter," "cold snap"
- Solution angle: "${businessType === 'gym' ? 'heated facility' : 'warm environment'}"
- Benefit: "keep momentum," "don't let weather slow you down"
- Urgency: "weather-proof your training"
EXAMPLE: "Don't let the ${temp}° cold be an excuse..."`;
  }

  // Rainy weather
  else if (condition.toLowerCase().includes('rain')) {
    context = `🌧️ RAINY CONDITIONS:
- Hook: "Perfect rainy day weather to..."
- Pain: "wet conditions," "slippery sidewalks," "dreary weather"
- Solution angle: "${businessType === 'gym' ? 'stay dry while staying active' : 'indoor advantage'}"
- Benefit: "rain or shine," "no excuses," "weather-proof"
- Urgency: "rain makes indoor training perfect"
EXAMPLE: "Skip the wet sidewalks and hit your PRs indoors..."`;
  }

  // Snowy weather
  else if (condition.toLowerCase().includes('snow')) {
    context = `❄️ SNOWY CONDITIONS:
- Hook: "With snow in the forecast..."
- Pain: "slippery conditions," "snowstorm," "winter weather"
- Solution angle: "safe indoor environment"
- Benefit: "skip dangerous conditions," "weather-proof routine"
- Urgency: "snow day = perfect training day"
EXAMPLE: "Snow outside? Perfect day to stay warm and train hard..."`;
  }

  // Perfect weather
  else if (temp >= 65 && temp <= 80 && condition.toLowerCase().includes('clear')) {
    context = `☀️ PERFECT WEATHER (${temp}°F):
- Hook: "Beautiful ${temp}° weather today..."
- Mood: "perfect conditions," "ideal weather," "great day"
- Motivation angle: "capitalize on this energy"
- Benefit: "momentum builder," "great weather = great results"
- Urgency: "perfect day to start"
EXAMPLE: "Perfect ${temp}° weather to kick off your transformation..."`;
  }

  else {
    context = `MILD CONDITIONS (${temp}°F):
- Keep messaging standard
- Weather not a strong angle
- Focus on other personalization factors`;
  }

  return context;
}
