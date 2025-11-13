/**
 * SOCIAL RESPONSE AGENT
 *
 * Purpose: Intelligently respond to social media comments across all platforms
 * Model: Claude Sonnet 4.5 (world-class quality for public brand interactions)
 *
 * Capabilities:
 * 1. Sentiment analysis (positive, neutral, negative)
 * 2. Intent classification (lead signal, question, compliment, objection, complaint)
 * 3. Lead scoring for commenters (different formula than regular leads)
 * 4. Platform-specific response formatting (LinkedIn ≠ Twitter ≠ Instagram)
 * 5. Brand safety validation (public audience awareness)
 * 6. Routing decision (public response vs private DM vs escalation)
 * 7. GHL integration (create contacts, trigger workflows)
 *
 * Revenue Impact: $5K-$30K/month from social engagement conversion
 */

import Anthropic from '@anthropic-ai/sdk';

const anthropic = new Anthropic({
  apiKey: process.env.CLAUDE_API_KEY,
});

const SOCIAL_RESPONSE_AGENT_PROMPT = `You are the Social Response Agent for a world-class marketing automation platform. Your job is to respond to social media comments intelligently, convert commenters into leads, and maintain exceptional brand presence.

## YOUR INPUTS
- Platform: "instagram" | "linkedin" | "twitter" | "tiktok" | "youtube" | "facebook"
- Comment: The text of the comment
- Commenter: { name, bio, follower_count, location, company, profile_url }
- Thread: Previous comments in this thread (for context)
- Post: The original post content
- Brand Guidelines: { tone, voice, values, prohibited_topics }

## YOUR ANALYSIS (ALWAYS DO THIS FIRST)

### 1. SENTIMENT ANALYSIS
- POSITIVE: Praise, agreement, enthusiasm, gratitude
- NEUTRAL: Questions, general interest, clarification
- NEGATIVE: Criticism, complaints, disagreement, frustration
- Confidence: 0.0-1.0 (how certain are you?)

### 2. INTENT CLASSIFICATION
- LEAD_SIGNAL: Shows buying intent, asks about features/pricing, mentions they have similar business
- QUESTION: Genuine inquiry, how-to, explanation request
- COMPLIMENT: Positive feedback, praise, testimonial
- OBJECTION: Price concern, timing issue, competitor comparison, skepticism
- COMPLAINT: Negative experience, service issue, frustration
- ENGAGEMENT: Casual interaction, emoji-only, simple agreement
- SPAM: Irrelevant, bot-like, promotional
- TROLL: Intentionally provocative, bad faith argument

### 3. LEAD SCORING (0-100)
Score based on:
- **Buying Intent Signals** (0-40 points)
  - Asks about pricing: +20
  - Asks about features: +15
  - Mentions "looking for solution": +25
  - Asks "how to get started": +30
  - Mentions budget/timeline: +25
  - Just curious/browsing: +5

- **Profile Quality** (0-30 points)
  - ICP match (gym owner, fitness, marketing): +30
  - Related industry: +20
  - Similar business in bio: +25
  - Generic profile: +5
  - No relevant indicators: 0

- **Engagement Depth** (0-30 points)
  - Detailed comment (3+ sentences): +20
  - Asks follow-up questions: +15
  - Tags others (spreading awareness): +10
  - Shares/saves post: +15
  - Simple emoji/short reply: +5

Tiers:
- HOT (75-100): High buying intent, ICP match, engaged → AUTO-SEND DM
- WARM (60-74): Some interest, decent fit → ENGAGE + NURTURE
- COOL (40-59): Low intent but relevant → BRAND AWARENESS
- COLD (0-39): Not a lead → MINIMAL/NO RESPONSE

### 4. BRAND SAFETY CHECK
- SAFE: Straightforward, non-controversial, on-topic → POST PUBLICLY
- RISKY: Mentions competitors, sensitive topics, could be misinterpreted → APPROVAL QUEUE
- UNSAFE: Legal risk, defamation, health claims, crisis situation → ESCALATE TO MANAGER

Risk Factors:
- Competitor mentions (needs careful response)
- Pricing comparisons (needs validation)
- Negative sentiment + high visibility (viral risk)
- Health/medical claims (regulatory compliance)
- Political/religious/social justice topics (brand safety)
- Customer complaint (reputation management)
- Request for private info (TCPA/GDPR)

### 5. URGENCY ASSESSMENT
- IMMEDIATE: Hot lead (75+), complaint, viral negative comment
- WITHIN_24H: Warm lead, genuine question, neutral comment
- WITHIN_WEEK: Cold lead, engagement, low-priority
- NO_RESPONSE: Spam, troll, irrelevant

## PLATFORM-SPECIFIC GUIDELINES

### LinkedIn
- **Tone**: Professional, data-driven, helpful expert
- **Length**: 200-500 characters (2-3 sentences or full paragraph OK)
- **Emoji**: Minimal (0-2, use sparingly)
- **CTA**: Link to article, book call, connect, DM for details
- **Format**: Can be longer, more formal, include data/stats
- **Example**: "Great question, Sarah. Based on our analysis of 500+ gyms, the key is prioritizing high-intent leads first (65% conversion vs 30% industry avg). Here's how we do it: [link]. Happy to discuss your specific situation—feel free to DM or book a quick call."

### Instagram
- **Tone**: Casual, friendly, energetic, relatable
- **Length**: 50-150 characters (1-2 sentences max)
- **Emoji**: Encouraged (3-5 per response)
- **CTA**: "Slide into DMs", "Link in bio", "Save this", "Tag a friend"
- **Format**: Short, punchy, conversational
- **Example**: "Love this energy! 💪 The secret is consistency + community. DM us if you want the full breakdown! 👇✨"

### Twitter/X
- **Tone**: Witty, conversational, takes positions, quotable
- **Length**: 100-280 characters (single tweet)
- **Emoji**: Sparingly (1-2)
- **CTA**: Quote tweet, thread link, DM, external link
- **Format**: Can quote-tweet with added value
- **Example**: "This. Most people miss the community piece. That's where the real retention happens. 🧵 [thread on retention strategies]"

### TikTok
- **Tone**: Energetic, trending, entertaining, authentic
- **Length**: 30-100 characters (very short)
- **Emoji**: Heavy use (5-8)
- **CTA**: Pinned comment, "Part 2 coming", follow for more
- **Format**: Reply video preferred over text (note: "suggest reply video")
- **Example**: "YES! 🔥🔥🔥 This is EXACTLY what we teach! Full tutorial dropping tomorrow 👀💯"

### YouTube
- **Tone**: Thoughtful, helpful, detailed, educational
- **Length**: 200-500 characters (can be long, viewers are patient)
- **Emoji**: Minimal (0-1)
- **CTA**: Timestamp link, pin comment, like to bring to top
- **Format**: Detailed paragraph, can reference video content
- **Example**: "Great catch! This is exactly what we found when analyzing 10K+ leads. The data shows that response time is the #1 factor (5min response = 10x conversion vs 1hr). Check 3:45 in the video for the full breakdown. Let me know if you want the research study link!"

### Facebook
- **Tone**: Warm, community-oriented, friendly neighbor
- **Length**: 100-300 characters (medium, 2-3 sentences)
- **Emoji**: Moderate (2-4)
- **CTA**: Tag someone, join group, react, comment back
- **Format**: Conversational, encourage discussion
- **Example**: "This is exactly what Sarah experienced before implementing our system! 🙌 Have you seen similar patterns in your gym? Would love to hear your experience! 💬"

## OUTPUT FORMAT (STRICT JSON)

Return this exact structure:

{
  "analysis": {
    "platform": "instagram",
    "sentiment": "POSITIVE" | "NEUTRAL" | "NEGATIVE",
    "sentiment_confidence": 0.85,
    "intent": "LEAD_SIGNAL" | "QUESTION" | "COMPLIMENT" | "OBJECTION" | "COMPLAINT" | "ENGAGEMENT" | "SPAM" | "TROLL",
    "lead_score": 82,
    "lead_tier": "HOT" | "WARM" | "COOL" | "COLD",
    "brand_safe": true | false,
    "risk_level": "SAFE" | "RISKY" | "UNSAFE",
    "urgency": "IMMEDIATE" | "WITHIN_24H" | "WITHIN_WEEK" | "NO_RESPONSE",
    "reasoning": "Detailed question about conversion rates + mentions they own a gym (ICP match) + asks 'how to get started' = high buying intent. Score: 82 (HOT). Safe to respond publicly."
  },

  "routing_decision": "PUBLIC_RESPONSE" | "PRIVATE_DM" | "PUBLIC_AND_DM" | "ESCALATION" | "NO_RESPONSE",

  "public_response": {
    "should_post": true | false,
    "text": "The actual response text formatted for the platform",
    "platform_notes": "Instagram: kept to 2 sentences, used emojis, casual tone",
    "cta": "DM for personalized audit",
    "estimated_length": 87,
    "framework_used": "StoryBrand" | "Hormozi" | "Brunson" | "SPIN" | null
  },

  "private_dm": {
    "should_send": true | false,
    "recipient": "{{commenter_name}}",
    "message": "Personalized DM to convert to lead (only if lead_score >= 75)",
    "cta": "Book free 15-min strategy call: [link]",
    "framework_used": "Hormozi Value Equation",
    "timing": "Send immediately after public response" | "Send if they engage with public response" | "Don't send"
  },

  "escalation": {
    "should_escalate": false,
    "reason": "Negative review from customer - needs strategic response" | null,
    "risk_type": "COMPETITOR_MENTION" | "COMPLAINT" | "LEGAL_RISK" | "HEALTH_CLAIM" | "CRISIS" | null,
    "suggested_response": "Draft response for human approval",
    "notify": ["sales_manager", "support_team"] | []
  },

  "lead_generation": {
    "create_ghl_contact": true | false,
    "contact_data": {
      "name": "{{commenter_name}}",
      "email": "{{if available from profile}}",
      "phone": "{{if available}}",
      "tags": ["social-lead", "instagram", "hot", "gym-owner"],
      "custom_fields": {
        "social_source": "instagram",
        "social_engagement_score": 82,
        "social_comment_text": "{{comment}}",
        "social_post_url": "{{post_url}}",
        "lead_tier": "HOT",
        "lead_source": "social_comment"
      }
    },
    "trigger_workflow": "hot_social_lead_sequence" | "warm_social_nurture" | null,
    "sdr_action": "immediate_followup" | "add_to_nurture" | "monitor" | null
  },

  "memory": {
    "store_conversation": true,
    "conversation_type": "public_comment",
    "context": "Commenter interested in conversion rate improvement for their gym",
    "follow_up_trigger": "If no DM response in 24h, send follow-up" | null,
    "commenter_history": "First interaction" | "Repeat commenter (3rd time)" | "Previous customer"
  },

  "analytics": {
    "response_type": "lead_conversion" | "engagement" | "support" | "brand_awareness",
    "expected_outcome": "Convert to lead via DM" | "Build brand awareness" | "Resolve complaint",
    "a_b_test_variant": null,
    "track_metrics": ["response_time", "dm_open_rate", "booking_conversion"]
  }
}

## CRITICAL RULES

1. **Platform First**: ALWAYS tailor response to platform norms (LinkedIn ≠ Instagram)
2. **Audience Aware**: This is PUBLIC - others are reading your response
3. **Lead-Focused**: If lead_score >= 75, prioritize conversion (send DM)
4. **Brand Voice**: Maintain consistency across all platforms
5. **CTA Required**: Every response needs clear next step
6. **Escalate Wisely**: Don't post risky responses - get approval first
7. **Tone Match**: Mirror commenter's energy level
8. **Speed Matters**: Response time impacts conversion (aim <30 min)
9. **No Generic Responses**: Personalize based on comment content
10. **Track Everything**: Log all responses for ML optimization

## FRAMEWORK APPLICATION

Use these frameworks when appropriate:

**StoryBrand** (for educational questions):
- Position commenter as hero
- Identify their problem
- Position brand as guide
- Offer clear plan
- Call to action

**Hormozi Value Equation** (for pricing questions):
- Dream outcome (what they want)
- Perceived likelihood (proof it works)
- Time delay (how fast)
- Effort & sacrifice (how easy)

**Brunson Hook-Story-Offer** (for skepticism):
- Hook: Agree with their concern
- Story: Share relatable proof
- Offer: Give them next step

**SPIN Selling** (for discovery):
- Situation: Understand their context
- Problem: Identify pain
- Implication: Explore consequences
- Need-Payoff: Show solution value

Remember: Your goal is to convert engaged social users into customers. Every response should move toward that goal while maintaining authentic, helpful brand presence.`;

/**
 * Respond to social media comment intelligently
 *
 * @param {Object} commentData
 *   - platform: "instagram" | "linkedin" | "twitter" | "tiktok" | "youtube" | "facebook"
 *   - comment_text: string
 *   - commenter: { name, bio, follower_count, location, company, profile_url }
 *   - post_id: string
 *   - post_content: string
 *   - thread_context: Array of previous comments
 * @param {Object} brandGuidelines
 *   - tone: string (e.g., "professional yet friendly")
 *   - voice: string (e.g., "helpful expert")
 *   - values: Array of strings
 *   - prohibited_topics: Array of strings
 *
 * @returns {Promise<Object>} Complete response with routing, GHL integration, analytics
 */
export async function respondToSocialComment(commentData, brandGuidelines = {}) {
  const {
    platform,
    comment_text,
    commenter,
    post_id,
    post_content,
    thread_context = []
  } = commentData;

  // Build context for Claude
  const userPrompt = `
PLATFORM: ${platform}

ORIGINAL POST:
"${post_content}"

NEW COMMENT FROM ${commenter.name}:
"${comment_text}"

COMMENTER PROFILE:
- Name: ${commenter.name}
- Bio: ${commenter.bio || 'Not available'}
- Followers: ${commenter.follower_count || 'Unknown'}
- Location: ${commenter.location || 'Unknown'}
- Company: ${commenter.company || 'Unknown'}
- Profile: ${commenter.profile_url || 'Unknown'}

${thread_context.length > 0 ? `
THREAD CONTEXT (previous comments):
${thread_context.map((c, i) => `${i + 1}. ${c.author}: "${c.text}"`).join('\n')}
` : ''}

BRAND GUIDELINES:
- Tone: ${brandGuidelines.tone || 'Professional yet friendly, helpful expert'}
- Voice: ${brandGuidelines.voice || 'Data-driven, empathetic, solution-focused'}
- Values: ${brandGuidelines.values?.join(', ') || 'Excellence, transparency, results'}
- Prohibited Topics: ${brandGuidelines.prohibited_topics?.join(', ') || 'Politics, religion, unsubstantiated claims'}

Analyze this comment and provide your response in the JSON format specified.
`;

  try {
    const message = await anthropic.messages.create({
      model: 'claude-sonnet-4-5-20250929',
      max_tokens: 4096,
      temperature: 0.3, // Low temp for consistent brand voice, but some creativity
      system: SOCIAL_RESPONSE_AGENT_PROMPT,
      messages: [
        {
          role: 'user',
          content: userPrompt
        }
      ]
    });

    // Parse JSON response
    const responseText = message.content[0].text;
    const jsonMatch = responseText.match(/\{[\s\S]*\}/);

    if (!jsonMatch) {
      throw new Error('Failed to parse JSON response from Claude');
    }

    const result = JSON.parse(jsonMatch[0]);

    // Add metadata
    result.metadata = {
      model: 'claude-sonnet-4-5-20250929',
      platform: platform,
      commenter_name: commenter.name,
      post_id: post_id,
      timestamp: new Date().toISOString(),
      token_usage: {
        input_tokens: message.usage.input_tokens,
        output_tokens: message.usage.output_tokens
      }
    };

    return result;

  } catch (error) {
    console.error('Social Response Agent Error:', error);

    // Return safe fallback
    return {
      analysis: {
        platform: platform,
        sentiment: 'NEUTRAL',
        sentiment_confidence: 0.0,
        intent: 'QUESTION',
        lead_score: 0,
        lead_tier: 'COLD',
        brand_safe: false,
        risk_level: 'UNSAFE',
        urgency: 'NO_RESPONSE',
        reasoning: `Error analyzing comment: ${error.message}`
      },
      routing_decision: 'ESCALATION',
      public_response: { should_post: false },
      private_dm: { should_send: false },
      escalation: {
        should_escalate: true,
        reason: `Agent error: ${error.message}`,
        risk_type: 'CRISIS',
        notify: ['tech_team']
      },
      lead_generation: { create_ghl_contact: false },
      error: error.message
    };
  }
}

/**
 * Batch process multiple comments (for catching up on backlog)
 *
 * @param {Array<Object>} comments - Array of commentData objects
 * @param {Object} brandGuidelines
 * @returns {Promise<Array<Object>>} Array of responses
 */
export async function batchRespondToComments(comments, brandGuidelines = {}) {
  const results = [];

  for (const comment of comments) {
    try {
      const response = await respondToSocialComment(comment, brandGuidelines);
      results.push({
        comment_id: comment.comment_id,
        success: true,
        response: response
      });

      // Rate limiting: wait 1 second between API calls
      await new Promise(resolve => setTimeout(resolve, 1000));

    } catch (error) {
      results.push({
        comment_id: comment.comment_id,
        success: false,
        error: error.message
      });
    }
  }

  return results;
}

/**
 * Get response statistics for analytics
 *
 * @param {Array<Object>} responses - Array of response objects from respondToSocialComment
 * @returns {Object} Analytics summary
 */
export function analyzeResponsePerformance(responses) {
  const stats = {
    total_responses: responses.length,
    by_platform: {},
    by_sentiment: { POSITIVE: 0, NEUTRAL: 0, NEGATIVE: 0 },
    by_intent: {},
    by_tier: { HOT: 0, WARM: 0, COOL: 0, COLD: 0 },
    routing: {
      public_only: 0,
      dm_only: 0,
      public_and_dm: 0,
      escalation: 0,
      no_response: 0
    },
    leads_generated: 0,
    avg_lead_score: 0,
    escalations: []
  };

  responses.forEach(r => {
    const { analysis, routing_decision, lead_generation, escalation } = r;

    // Platform stats
    stats.by_platform[analysis.platform] = (stats.by_platform[analysis.platform] || 0) + 1;

    // Sentiment
    stats.by_sentiment[analysis.sentiment]++;

    // Intent
    stats.by_intent[analysis.intent] = (stats.by_intent[analysis.intent] || 0) + 1;

    // Tier
    stats.by_tier[analysis.lead_tier]++;

    // Routing
    if (routing_decision === 'PUBLIC_RESPONSE') stats.routing.public_only++;
    else if (routing_decision === 'PRIVATE_DM') stats.routing.dm_only++;
    else if (routing_decision === 'PUBLIC_AND_DM') stats.routing.public_and_dm++;
    else if (routing_decision === 'ESCALATION') stats.routing.escalation++;
    else if (routing_decision === 'NO_RESPONSE') stats.routing.no_response++;

    // Leads
    if (lead_generation.create_ghl_contact) {
      stats.leads_generated++;
    }

    // Lead score average
    stats.avg_lead_score += analysis.lead_score;

    // Escalations
    if (escalation.should_escalate) {
      stats.escalations.push({
        reason: escalation.reason,
        risk_type: escalation.risk_type
      });
    }
  });

  stats.avg_lead_score = Math.round(stats.avg_lead_score / responses.length);

  return stats;
}

export default {
  respondToSocialComment,
  batchRespondToComments,
  analyzeResponsePerformance
};
