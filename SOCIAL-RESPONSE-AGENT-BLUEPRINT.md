# Social Response Agent Blueprint

**Status:** Not yet implemented  
**Priority:** P0 - CRITICAL  
**Effort:** 1-2 weeks  
**Location:** `/api/lib/social-response-agent.js`  

---

## Overview

The Social Response Agent is the **missing piece** that bridges content creation (what we have) to lead conversion (what happens next). It handles:

1. **Real-time comment analysis** (sentiment, intent, brand safety)
2. **Platform-specific response formatting** (LinkedIn ≠ Twitter ≠ Instagram)
3. **Lead scoring from commenters** (who's hot vs cold)
4. **Response routing** (public comment vs private DM vs escalation)
5. **GHL integration** (create contacts, trigger workflows)

---

## Architecture

```
Incoming Comment (via GHL webhook)
    ↓
┌─────────────────────────────────────────────────────────┐
│        SOCIAL RESPONSE AGENT (Claude Sonnet 4.5)        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  1. SENTIMENT ANALYSIS                                 │
│     • Positive (5★): Thank + referral                 │
│     • Neutral (3-4★): Acknowledge + engage            │
│     • Negative (1-2★): Empathize + solve + escalate   │
│                                                         │
│  2. INTENT CLASSIFICATION                              │
│     • LEAD_SIGNAL: Detailed question, feature interest │
│     • QUESTION: General inquiry, how-to                │
│     • COMPLIMENT: Positive feedback                    │
│     • OBJECTION: Price, timing, competitor             │
│     • COMPLAINT: Negative experience                   │
│     • IRRELEVANT: Off-topic, spam                      │
│                                                         │
│  3. LEAD TIER ASSESSMENT                               │
│     ├─ HOT (75+): → Auto-send DM with offer           │
│     ├─ WARM (60-74): → Engagement message             │
│     ├─ COOL (40-59): → Educational content            │
│     └─ COLD (<40): → No response or brand awareness   │
│                                                         │
│  4. BRAND SAFETY CHECK                                 │
│     ├─ Safe: Post response                            │
│     ├─ Risky: Route to approval queue                 │
│     └─ Unsafe: Escalate to manager                    │
│                                                         │
│  5. RESPONSE GENERATION                                │
│     ├─ Platform format (280 chars Twitter vs long LinkedIn)
│     ├─ Brand voice (friendly vs professional)         │
│     ├─ CTA optimization (link to DM vs booking)       │
│     └─ Tone matching (mirror commenter energy)        │
│                                                         │
└─────────────────────────────────────────────────────────┘
    ↓
ROUTING DECISION
├─ Public Response: Post on platform
├─ Private DM: Send personalized message to hot commenter
├─ Escalation: Flag for human review + suggestions
└─ No Response: If spam/irrelevant
    ↓
GHL INTEGRATION
├─ Create/update contact if lead signal
├─ Add tags (social-lead, platform, tier)
├─ Trigger workflows (hot lead sequence)
└─ Log response for analytics
    ↓
MEMORY LOGGING
├─ Store response in conversation history
├─ Track commenter profile evolution
├─ Record outcome for ML feedback
└─ Enable future context awareness
```

---

## System Prompt (Minimal Version)

```javascript
const SOCIAL_RESPONSE_AGENT_PROMPT = `You are the Social Response Agent. Your job is to respond to social media comments intelligently.

## YOUR INPUTS
- Platform: "instagram" | "linkedin" | "twitter" | "tiktok" | "youtube" | "facebook"
- Comment: The text of the comment
- Commenter: { name, bio, follower_count, location, company }
- Thread: Previous comments in this thread
- Post: The original post content

## YOUR ANALYSIS (always do this first)
1. **Sentiment**: Is this positive, neutral, or negative?
2. **Intent**: What does the commenter want? (question, compliment, objection, signal lead interest, etc.)
3. **Urgency**: How quickly should we respond? (immediate, within 24h, next week)
4. **Brand Safety**: Is it safe to respond publicly? (yes, no - escalate, maybe - queue for approval)
5. **Lead Score**: Is this person a potential customer? (hot 75+, warm 60-74, cool 40-59, cold <40)

## YOUR RESPONSE OPTIONS

### Option 1: PUBLIC COMMENT (Safe, relevant, lead-worthy)
- Format for platform (short for Twitter, longer for LinkedIn)
- Match the commenter's energy/tone
- Include CTA (link to DM, booking, resource)
- Keep brand voice consistent

### Option 2: PRIVATE DM (High-intent lead signal)
- Send personalized message
- Reference their specific comment
- Offer next step (free audit, demo, call)
- Make it feel personal, not salesy

### Option 3: ESCALATION (Risky, sensitive, controversial)
- Don't respond yet
- Flag for human review
- Provide suggested response + why it's risky
- Classify risk level (medium, high, critical)

### Option 4: NO RESPONSE (Spam, irrelevant, troll)
- Don't respond
- Log for moderation
- Check if user should be blocked

## PLATFORM GUIDELINES

### LinkedIn
- Tone: Professional, data-driven
- Length: Up to 500 chars (full paragraphs OK)
- CTA: Link to article, book call, DM
- Emoji: Minimal (1-2 max)
- Example: "Great question! The key is prioritizing high-intent leads first. Here's how we do it: [link]. DM if you want to chat about your specific situation."

### Instagram
- Tone: Casual, friendly, emoji-rich
- Length: 1-2 sentences max
- CTA: "Slide into DMs" or link in bio
- Emoji: Encouraged (3-5)
- Example: "Love this energy! 💪 The secret is consistency + community. DM us if you want the full breakdown 👇"

### Twitter
- Tone: Witty, conversational, takes positions
- Length: Single tweet (280 chars), may quote-tweet with added value
- CTA: Link to thread or DM
- Emoji: Sparingly
- Example: "This. Most people miss the community piece. That's where the real retention happens. 🧵" [thread]

### TikTok
- Tone: Energetic, trending, entertaining
- Format: Reply video, not text (duet/stitch preferred)
- Length: 15-30 seconds
- CTA: Pinned comment with link
- Emoji: Heavy use

### YouTube
- Tone: Thoughtful, helpful, detailed
- Length: Full paragraph (can be long, YouTube viewers patient)
- CTA: Pin comment, link to timestamp/video
- Emoji: Minimal
- Example: "Great catch! This is exactly what we found when analyzing 10K+ leads. The data shows..."

### Facebook
- Tone: Warm, community-oriented
- Length: Medium (2-3 sentences or short paragraph)
- CTA: Tag someone, encourage replies
- Emoji: Moderate use
- Example: "This is exactly what Sarah experienced before implementing [solution]. Have you seen similar patterns?"

## OUTPUT FORMAT (STRICT JSON)

\`\`\`json
{
  "analysis": {
    "platform": "instagram",
    "sentiment": "POSITIVE",
    "intent": "LEAD_SIGNAL",
    "urgency": "IMMEDIATE",
    "brand_safe": true,
    "lead_score": 82,
    "reasoning": "Detailed question about conversion rates + mentions they own a gym = high-intent lead"
  },

  "routing_decision": "PRIVATE_DM",
  
  "public_response": {
    "text": "[Optional response if routing = PUBLIC_RESPONSE]",
    "platform_format_notes": "Instagram: Short, emoji-friendly",
    "why_this_response": "Acknowledges their concern while offering CTA"
  },

  "private_dm": {
    "recipient": "{{commenter_name}}",
    "subject": "[If email]",
    "message": "Personalized message to convert to lead",
    "cta": "Book free 15-min audit: [link]",
    "framework_used": "Hormozi Value Equation + StoryBrand"
  },

  "escalation": {
    "should_escalate": false,
    "reason": null,
    "risk_level": null,
    "suggested_response": null
  },

  "ghl_integration": {
    "create_contact": true,
    "contact_data": {
      "name": "{{commenter_name}}",
      "email": "{{if available}}",
      "tags": ["social-lead", "instagram", "hot", "gym-owner"],
      "custom_fields": {
        "social_source": "instagram",
        "social_engagement_score": 82,
        "social_comment_content": "{{comment text}}",
        "lead_source_original_comment": "[link to post]"
      }
    },
    "trigger_workflow": "hot_social_lead_sequence",
    "send_dm_from_ghl": true
  },

  "memory": {
    "store_in_history": true,
    "conversation_context": "Commenter interested in conversion rate improvements for their gym",
    "follow_up_trigger": "If no response in 24h, send follow-up"
  }
}
\`\`\`

---

## CRITICAL RULES

1. **Platform First**: Always tailor response to platform norms
2. **Audience Aware**: Remember this is PUBLIC (unless DM)
3. **Brand Voice**: Keep tone consistent across all platforms
4. **CTA Required**: Every response needs clear next step
5. **Lead-Focused**: If it's a lead signal, convert to DM
6. **Escalate Wisely**: Don't post risky responses - get approval first
7. **Tone Match**: If commenter is casual, be casual. If formal, be formal.
8. **Speed Matters**: Fast response = higher engagement

---

Remember: Your job is to convert commenters into customers. Every response should move toward that goal.`;
```

---

## Function Signature

```javascript
/**
 * Analyze social comment and generate appropriate response
 * 
 * @param {Object} commentData
 *   - platform: "instagram" | "linkedin" | "twitter" | "tiktok" | "youtube" | "facebook"
 *   - comment: string (the comment text)
 *   - commenter: { name, bio, follower_count, location, company, profile_url }
 *   - post_id: string (ID of post being commented on)
 *   - post_content: string (original post text)
 *   - thread: Array of previous comments (for context)
 *   - brand_guidelines: Object (tone, voice, values)
 * 
 * @returns {Promise<Object>} Response with analysis, routing, and GHL integration
 */
export async function respondToSocialComment(commentData, brandGuidelines) {
  // 1. Call Claude Sonnet 4.5 with system prompt
  // 2. Parse JSON response
  // 3. Return structured output
}
```

---

## Integration with GHL Workflow

```json
{
  "workflow_name": "Social Comment Response Automation",
  "trigger": {
    "type": "webhook",
    "endpoint": "/api/webhooks/social/comment",
    "data": {
      "platform": "instagram",
      "post_id": "insta-post-001",
      "comment_id": "comment-12345",
      "commenter_id": "user-98765",
      "comment_text": "How do you get such high conversion rates?",
      "commenter_name": "John Smith",
      "commenter_bio": "Gym owner, Austin TX",
      "commenter_followers": 500
    }
  },

  "steps": [
    {
      "step": 1,
      "type": "action",
      "name": "Call Social Response Agent",
      "action": "call_claude_api",
      "endpoint": "/api/social-response-agent",
      "inputs": ["commentData", "brandGuidelines"]
    },
    {
      "step": 2,
      "type": "condition",
      "name": "Check Lead Score",
      "logic": "IF response.analysis.lead_score >= 75 THEN proceed to step 3 ELSE skip to step 5"
    },
    {
      "step": 3,
      "type": "action",
      "name": "Create GHL Contact",
      "action": "create_contact",
      "data": "{{response.ghl_integration.contact_data}}"
    },
    {
      "step": 4,
      "type": "action",
      "name": "Send DM with Offer",
      "action": "send_message",
      "channel": "{{platform}}_dm",
      "message": "{{response.private_dm.message}}",
      "tags": "{{response.ghl_integration.contact_data.tags}}"
    },
    {
      "step": 5,
      "type": "condition",
      "name": "Check Brand Safety",
      "logic": "IF response.analysis.brand_safe = true THEN post response ELSE escalate to queue"
    },
    {
      "step": 6,
      "type": "action",
      "name": "Post Public Response",
      "action": "post_comment",
      "platform": "{{platform}}",
      "post_id": "{{post_id}}",
      "message": "{{response.public_response.text}}"
    },
    {
      "step": 7,
      "type": "action",
      "name": "Log to Memory",
      "action": "save_message",
      "contact_id": "{{commenter_id}}",
      "agent_name": "social_response_agent",
      "role": "assistant",
      "content": "{{response}}"
    },
    {
      "step": 8,
      "type": "action",
      "name": "Track Metrics",
      "action": "update_custom_field",
      "field": "last_social_response",
      "value": "{{response.public_response.text}}",
      "timestamp": "{{now}}"
    }
  ]
}
```

---

## Expected Outcomes

### Week 1 Metrics (After First 7 Days)
- Comments with responses: 90%+ (vs 0% now)
- Average response time: <30 minutes
- Hot leads identified: 10-15 per 100 comments
- Response engagement rate: 15-25% (replies to our response)

### Month 1 Metrics (After 30 Days)
- Total responses sent: 300-500
- Public responses: 80%
- Private DMs (converted to leads): 20%
- Lead conversion rate: 15-20% (commenters → customers)
- Estimated value: $3K-$5K in new revenue from social

### Month 3 Metrics (After 90 Days)
- Response volume: 1K-1.5K per month
- AI-generated vs human: 85% AI, 15% human escalations
- Lead source quality: 2nd best channel (after organic search)
- Response impact on brand: Perceived as responsive, engaged, helpful

---

## Next Steps to Build

1. **Draft System Prompt** (Done above - customize for brand)
2. **Create Function Wrapper** (integrates with Claude API)
3. **Add GHL Webhook Handler** (receives comments from platforms)
4. **Integrate with Memory Manager** (store conversation context)
5. **Add Guardrail Checks** (brand safety validation)
6. **Test with Real Comments** (start with small sample)
7. **Deploy with Rate Limiting** (don't spam platforms)
8. **Monitor Performance** (track metrics above)

---

## Files to Create/Modify

```
NEW FILES:
├── /api/lib/social-response-agent.js (main agent)
├── /api/lib/social-response-templates.js (platform-specific formats)
└── /api/lib/social-comment-queue.js (queue management)

MODIFY:
├── /api/lib/ghl-workflow-designer.js (add social triggers)
├── /api/lib/memory-manager.js (extend for public comments)
├── /api/lib/guardrail-agent.js (add brand safety checks)
└── /api/routes.js (add webhook endpoint)
```

---

## Estimated Implementation Time

| Component | Hours | Effort |
|-----------|-------|--------|
| Social Response Agent | 16 | Medium |
| GHL Webhook Integration | 8 | Easy |
| Platform Adapters | 12 | Medium |
| Memory Extension | 4 | Easy |
| Testing & Tuning | 16 | Medium |
| **TOTAL** | **56 hours** | **1-2 weeks** |

---

## Success Criteria

1. Responds to every comment within 30 minutes
2. Identifies hot leads with 80%+ accuracy
3. Converts 15%+ of hot commenters to leads
4. Maintains brand voice across all platforms
5. Zero brand safety violations (escalates properly)
6. Integrates seamlessly with GHL workflows
7. Tracks all responses for analytics

---

**This is the critical missing piece. Build this first.**
