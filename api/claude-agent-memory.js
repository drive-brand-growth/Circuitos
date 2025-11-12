/**
 * Circuit OS - Enhanced Claude API Integration with Memory
 *
 * ADK-Level Capabilities:
 * - Multi-turn conversations
 * - Agent collaboration via shared context
 * - Conversational memory (Supabase)
 * - ML feedback loop
 *
 * Deploy to: Vercel/Cloud Run
 */

import Anthropic from '@anthropic-ai/sdk';
import memoryManager from './lib/memory-manager.js';
import designWorkflow from './lib/ghl-workflow-designer.js';
import { orchestrate } from './lib/orchestrator.js';
import { optimizeWorkflow } from './lib/ml-workflow-optimizer.js';
import guardrail from './lib/guardrail-agent.js';

const anthropic = new Anthropic({
  apiKey: process.env.CLAUDE_API_KEY
});

// DMN Protocol System Prompts
const DMN_PROMPTS = {
  'Lead Scorer': `You are the Lead Scorer for Circuit OS™, a strategic-tier agent in the DMN Protocol.

Your role: Score leads 0-100 using BANT/MEDDIC/CHAMP frameworks with Virtual LPR™ signals.

Scoring Breakdown:
- FIT (40 points): Demographics + Psychographics + Geographic proximity
- INTENT (40 points): Explicit signals (GMB calls, direction requests) + Implicit (website visits)
- TIMING (20 points): Urgency + Readiness to buy

CRITICAL RULES:
- NO assumptions - missing data = 0 points + flag it
- Cite every data source with attribution
- Be conservative (better to underscore than overscore)
- Return ONLY valid JSON

You have access to conversation history. Use it to:
- Reference past scoring decisions
- Track lead behavior over time
- Adjust scoring based on engagement patterns`,

  'Copywriter': `You are the Master Copywriter for Circuit OS™, an operational-tier agent in the DMN Protocol.

Your role: Generate world-class copy using:
- Russell Brunson: Hook-Story-Offer framework
- Eugene Schwartz: 5 Awareness Levels (Unaware → Most Aware)
- Alex Hormozi: Value equation (Dream Outcome / Time & Effort * Likelihood / Risk)

BANNED PHRASES:
- "Hi there", "Hello", "I hope this email finds you well"
- "Reaching out", "Just checking in", "Following up"
- "Thought you might be interested"
- Any use of hyphens (--) in copy

QUALITY GATES:
- 80-200 words (concise but complete)
- 3+ paragraphs (story structure)
- Specific numbers/data (not vague)
- Clear single CTA
- Strong personalization (not template)

You have access to conversation history. Use it to:
- Read Lead Scorer's analysis and scoring breakdown
- Reference past outreach attempts
- Avoid repeating previous hooks/angles
- Escalate messaging if no response`,

  'Reputation Guardian': `You are the Reputation Guardian for Circuit OS™, an operational-tier agent in the DMN Protocol.

Your role: Monitor and respond to online reviews with authentic, brand-aligned responses.

Response Framework:
- 5-star: Grateful, specific, invite repeat visit (30-50 words)
- 4-star: Appreciate + acknowledge gap + commitment (50-75 words)
- 1-3 star: Apologize + explain + offer solution + take offline (75-100 words)

Tone Guidelines:
- Authentic (not corporate or robotic)
- Empathetic (genuinely care)
- Solution-focused (not defensive)
- Brand-aligned (matches business personality)

You have access to conversation history. Use it to:
- Reference previous review responses for consistency
- Track recurring issues mentioned in reviews
- Escalate to human if sensitive (legal, PR crisis)`
};

/**
 * Main handler for Vercel/Cloud Run
 */
export default async function handler(req, res) {
  // CORS headers for GHL
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { action, contactId, businessId, data, useMemory = true } = req.body;

  // Validate required fields
  if (!action || !contactId || !businessId) {
    return res.status(400).json({
      error: 'Missing required fields: action, contactId, businessId'
    });
  }

  try {
    switch (action) {
      case 'score-lead':
        return await scoreLead(req, res, contactId, businessId, data, useMemory);
      case 'generate-copy':
        return await generateCopy(req, res, contactId, businessId, data, useMemory);
      case 'respond-to-review':
        return await respondToReview(req, res, contactId, businessId, data, useMemory);
      case 'design-workflow':
        return await designGHLWorkflow(req, res, contactId, businessId, data, useMemory);
      case 'orchestrate':
        return await orchestrateAgents(req, res, contactId, businessId, data);
      case 'optimize-workflow':
        return await optimizeWorkflowHandler(req, res, contactId, businessId, data, useMemory);
      case 'check-violations':
        return await checkViolationsHandler(req, res, data);
      case 'sanitize-text':
        return await sanitizeTextHandler(req, res, data);
      case 'get-summary':
        return await getConversationSummary(req, res, contactId);
      case 'record-feedback':
        return await recordAgentFeedback(req, res, contactId, data);
      default:
        return res.status(400).json({ error: 'Invalid action' });
    }
  } catch (error) {
    console.error('[Claude API] Error:', error);
    return res.status(500).json({
      error: 'Internal server error',
      message: error.message
    });
  }
}

/**
 * Lead Scoring with Memory
 */
async function scoreLead(req, res, contactId, businessId, data, useMemory) {
  const { contact, business } = data;

  // Get conversation history (if useMemory enabled)
  const conversationHistory = useMemory
    ? await memoryManager.getConversationHistory(contactId)
    : [];

  // Get context from other agents
  const agentContext = useMemory
    ? await memoryManager.getAgentContext(contactId)
    : [];

  // Build user prompt with context
  let userPrompt = `Score this lead using BANT/MEDDIC/CHAMP + Virtual LPR™ frameworks.

CONTACT DATA:
${JSON.stringify(contact, null, 2)}

BUSINESS DATA:
${JSON.stringify(business, null, 2)}`;

  // Add agent context if available
  if (agentContext.length > 0) {
    userPrompt += `\n\nPREVIOUS AGENT ACTIONS:
${agentContext.map(ctx => `- ${ctx.agent}: ${ctx.action} at ${ctx.timestamp}`).join('\n')}`;
  }

  userPrompt += `\n\nReturn ONLY valid JSON with this structure:
{
  "total_score": 78,
  "breakdown": {
    "fit": 26,
    "intent": 36,
    "timing": 16
  },
  "grade": "A",
  "priority": "HIGH",
  "next_action": "IMMEDIATE_COLD_EMAIL",
  "confidence": "VERY_HIGH",
  "missing_data": ["income", "company_size"],
  "detailed_attribution": {
    "fit_reasons": ["Industry match: Tech", "Distance: 1.2mi from business"],
    "intent_reasons": ["Called business from GMB 2hrs ago", "Viewed GMB listing 3x this week"],
    "timing_reasons": ["Very recent activity <2hrs", "High urgency signals"]
  }
}`;

  // Add user message to history
  const messages = [...conversationHistory, { role: 'user', content: userPrompt }];

  // Call Claude with conversation history
  const message = await anthropic.messages.create({
    model: 'claude-sonnet-4-5-20250929',
    max_tokens: 4096,
    temperature: 0.3,
    system: DMN_PROMPTS['Lead Scorer'],
    messages
  });

  const responseText = message.content[0].text;
  const result = JSON.parse(responseText);

  // Save to conversation memory
  if (useMemory) {
    await memoryManager.saveMessage(
      contactId,
      businessId,
      'Lead Scorer',
      'user',
      userPrompt
    );

    await memoryManager.saveMessage(
      contactId,
      businessId,
      'Lead Scorer',
      'assistant',
      responseText,
      {
        action: 'SCORED_LEAD',
        score: result.total_score,
        grade: result.grade,
        inputTokens: message.usage.input_tokens,
        outputTokens: message.usage.output_tokens
      }
    );
  }

  // Return result
  return res.status(200).json({
    ...result,
    metadata: {
      agent: 'Lead Scorer',
      model: 'claude-sonnet-4-5-20250929',
      conversationTurns: Math.floor(messages.length / 2),
      usedMemory: useMemory,
      tokens: {
        input: message.usage.input_tokens,
        output: message.usage.output_tokens,
        total: message.usage.input_tokens + message.usage.output_tokens
      }
    }
  });
}

/**
 * Copy Generation with Memory
 */
async function generateCopy(req, res, contactId, businessId, data, useMemory) {
  const { contact, channel, awareness_level, business } = data;

  // Get conversation history (Copywriter can see Lead Scorer's work!)
  const conversationHistory = useMemory
    ? await memoryManager.getConversationHistory(contactId)
    : [];

  let userPrompt = `Generate world-class ${channel} copy.

CONTACT: ${contact.first_name} ${contact.last_name} in ${contact.city || 'unknown location'}
BUSINESS: ${business.name} (${business.category})
AWARENESS LEVEL: ${awareness_level || 'Solution Aware'}

Framework: Hook-Story-Offer (Russell Brunson)
Awareness: ${awareness_level || 'Solution Aware'} (Eugene Schwartz)

Generate 3 variants (A/B/C testing) with different hooks.

QUALITY REQUIREMENTS:
- 80-200 words per variant
- NO banned phrases (see system prompt)
- Specific numbers/data (not vague)
- Clear single CTA
- Strong personalization

Return ONLY valid JSON:
{
  "variants": [
    {
      "id": "A",
      "subject": "...",
      "body": "...",
      "cta": "...",
      "qualityScore": 87
    },
    // ... B and C
  ]
}`;

  const messages = [...conversationHistory, { role: 'user', content: userPrompt }];

  const message = await anthropic.messages.create({
    model: 'claude-sonnet-4-5-20250929',
    max_tokens: 3096,
    temperature: 0.7,
    system: DMN_PROMPTS['Copywriter'],
    messages
  });

  const responseText = message.content[0].text;
  const result = JSON.parse(responseText);

  // Save to memory
  if (useMemory) {
    await memoryManager.saveMessage(contactId, businessId, 'Copywriter', 'user', userPrompt);
    await memoryManager.saveMessage(
      contactId,
      businessId,
      'Copywriter',
      'assistant',
      responseText,
      {
        action: 'GENERATED_COPY',
        channel,
        variantCount: result.variants.length
      }
    );
  }

  return res.status(200).json({
    ...result,
    metadata: {
      agent: 'Copywriter',
      model: 'claude-sonnet-4-5-20250929',
      conversationTurns: Math.floor(messages.length / 2),
      usedMemory: useMemory,
      tokens: {
        input: message.usage.input_tokens,
        output: message.usage.output_tokens,
        total: message.usage.input_tokens + message.usage.output_tokens
      }
    }
  });
}

/**
 * Review Response with Memory
 */
async function respondToReview(req, res, contactId, businessId, data, useMemory) {
  const { review, business } = data;

  const conversationHistory = useMemory
    ? await memoryManager.getConversationHistory(contactId)
    : [];

  let userPrompt = `Generate authentic review response.

REVIEW: ${review.rating} stars
TEXT: "${review.text}"
REVIEWER: ${review.author_name || 'Anonymous'}
BUSINESS: ${business.name}

Tone: ${review.rating >= 4 ? 'Grateful + Specific' : 'Apologetic + Solution-focused'}
Length: ${review.rating >= 4 ? '30-50 words' : '75-100 words'}

Return ONLY valid JSON:
{
  "response": "...",
  "approval_needed": ${review.rating <= 3},
  "escalate_to_human": ${review.rating <= 2},
  "sentiment": "POSITIVE/NEGATIVE/NEUTRAL"
}`;

  const messages = [...conversationHistory, { role: 'user', content: userPrompt }];

  const message = await anthropic.messages.create({
    model: 'claude-sonnet-4-5-20250929',
    max_tokens: 1024,
    temperature: 0.7,
    system: DMN_PROMPTS['Reputation Guardian'],
    messages
  });

  const responseText = message.content[0].text;
  const result = JSON.parse(responseText);

  if (useMemory) {
    await memoryManager.saveMessage(contactId, businessId, 'Reputation Guardian', 'user', userPrompt);
    await memoryManager.saveMessage(
      contactId,
      businessId,
      'Reputation Guardian',
      'assistant',
      responseText,
      {
        action: 'RESPONDED_TO_REVIEW',
        rating: review.rating,
        sentiment: result.sentiment
      }
    );
  }

  return res.status(200).json({
    ...result,
    metadata: {
      agent: 'Reputation Guardian',
      model: 'claude-sonnet-4-5-20250929',
      conversationTurns: Math.floor(messages.length / 2),
      usedMemory: useMemory
    }
  });
}

/**
 * Get conversation summary (for GHL custom fields)
 */
async function getConversationSummary(req, res, contactId) {
  const summary = await memoryManager.getSummary(contactId);
  return res.status(200).json(summary);
}

/**
 * Record agent feedback (ML loop)
 */
async function recordAgentFeedback(req, res, contactId, data) {
  const { conversationId, predicted, actual, learnedPatterns } = data;

  const feedback = await memoryManager.recordFeedback(
    contactId,
    conversationId,
    predicted,
    actual,
    learnedPatterns
  );

  return res.status(200).json({
    success: true,
    feedback
  });
}

/**
 * Design GHL Workflow with AI
 */
async function designGHLWorkflow(req, res, contactId, businessId, data, useMemory) {
  const {
    description,
    useCase,
    targetAudience,
    channel,
    includeAI,
    complianceLevel
  } = data;

  // Get conversation history if using memory
  const conversationHistory = useMemory
    ? await memoryManager.getConversationHistory(contactId, 20)
    : [];

  // Call workflow designer
  const result = await designWorkflow({
    description,
    useCase,
    targetAudience,
    channel,
    includeAI,
    complianceLevel
  }, conversationHistory);

  // Save to conversation memory
  if (useMemory) {
    const requestPrompt = `Design a GHL workflow: ${description}`;

    await memoryManager.saveMessage(
      contactId,
      businessId,
      'GHL Workflow Designer',
      'user',
      requestPrompt
    );

    await memoryManager.saveMessage(
      contactId,
      businessId,
      'GHL Workflow Designer',
      'assistant',
      result.fullResponse,
      {
        action: 'DESIGNED_WORKFLOW',
        workflowName: result.workflow?.workflow_name,
        inputTokens: result.metadata.tokens.input,
        outputTokens: result.metadata.tokens.output
      }
    );
  }

  return res.status(200).json(result);
}

/**
 * Orchestrate multiple agents to accomplish complex tasks
 */
async function orchestrateAgents(req, res, contactId, businessId, data) {
  const result = await orchestrate(data, contactId, businessId);
  return res.status(200).json(result);
}

/**
 * Optimize workflow using ML insights
 */
async function optimizeWorkflowHandler(req, res, contactId, businessId, data, useMemory) {
  const {
    workflowId,
    performanceData,
    demographicData,
    psychographicData,
    marketTrends
  } = data;

  // Get conversation history if using memory
  const conversationHistory = useMemory
    ? await memoryManager.getConversationHistory(contactId, 20)
    : [];

  // Call ML optimizer
  const result = await optimizeWorkflow({
    workflowId,
    performanceData,
    demographicData,
    psychographicData,
    marketTrends,
    conversationHistory
  });

  // Save to conversation memory
  if (useMemory) {
    const requestPrompt = `Optimize workflow ${workflowId} using ML insights`;

    await memoryManager.saveMessage(
      contactId,
      businessId,
      'ML Workflow Optimizer',
      'user',
      requestPrompt
    );

    await memoryManager.saveMessage(
      contactId,
      businessId,
      'ML Workflow Optimizer',
      'assistant',
      result.fullResponse,
      {
        action: 'OPTIMIZED_WORKFLOW',
        mlScore: result.optimization?.ml_score?.total,
        inputTokens: result.metadata.tokens.input,
        outputTokens: result.metadata.tokens.output
      }
    );
  }

  return res.status(200).json(result);
}

/**
 * Check text for violations (Guardrail)
 */
async function checkViolationsHandler(req, res, data) {
  const { text, guardrails = [] } = data;

  if (!text) {
    return res.status(400).json({ error: 'Missing required field: text' });
  }

  const result = await guardrail.checkTextForViolations(text, guardrails);

  return res.status(200).json({
    success: true,
    ...result,
    metadata: {
      agent: 'Guardrail (Check Violations)',
      checks_performed: guardrails.length
    }
  });
}

/**
 * Sanitize text (Guardrail)
 */
async function sanitizeTextHandler(req, res, data) {
  const { text, sanitizers = [] } = data;

  if (!text) {
    return res.status(400).json({ error: 'Missing required field: text' });
  }

  const result = guardrail.sanitizeText(text, sanitizers);

  return res.status(200).json({
    success: true,
    ...result,
    metadata: {
      agent: 'Guardrail (Sanitize)',
      sanitizers_applied: sanitizers.length
    }
  });
}
