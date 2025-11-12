/**
 * Circuit OS - Testing & Debugging Interface
 *
 * Provides dry-run mode and step-by-step execution tracking
 * without triggering GHL workflows or charging API costs
 *
 * Features:
 * - Dry-run mode (skip Claude API call)
 * - Step-by-step execution visibility
 * - Input validation testing
 * - Mock response generation
 */

import Anthropic from '@anthropic-ai/sdk';
import { createClient } from '@supabase/supabase-js';
import executionTracker from './lib/execution-tracker.js';
import errorTracker from './lib/error-tracker.js';
import memoryManager from './lib/memory-manager.js';

const anthropic = new Anthropic({
  apiKey: process.env.CLAUDE_API_KEY
});

const supabase = createClient(
  process.env.SUPABASE_URL,
  process.env.SUPABASE_KEY
);

/**
 * Main test endpoint handler
 */
export default async function handler(req, res) {
  // CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const executionId = `test-exec-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;

  try {
    const {
      action,
      contactId = 'test-contact-123',
      businessId = 'test-business-456',
      data = {},
      useMemory = false,
      dryRun = true,
      stepByStep = true,
      mockResponse = false
    } = req.body;

    const steps = [];

    // STEP 1: Validate input
    steps.push({ step: 1, name: 'Validate Input', status: 'running', timestamp: Date.now() });

    if (!action) {
      throw new Error('Missing required field: action');
    }

    const validActions = ['score-lead', 'generate-copy', 'respond-to-review', 'get-summary'];
    if (!validActions.includes(action)) {
      throw new Error(`Invalid action: ${action}. Valid actions: ${validActions.join(', ')}`);
    }

    steps[0].status = 'completed';
    steps[0].duration = Date.now() - steps[0].timestamp;
    steps[0].result = { action, contactId, businessId, useMemory, dryRun };

    // STEP 2: Fetch conversation history (if memory enabled)
    if (useMemory) {
      steps.push({ step: 2, name: 'Fetch Conversation History', status: 'running', timestamp: Date.now() });

      try {
        const conversationHistory = await memoryManager.getConversationHistory(contactId, 20);

        steps[1].status = 'completed';
        steps[1].duration = Date.now() - steps[1].timestamp;
        steps[1].result = {
          messageCount: conversationHistory.length,
          messages: conversationHistory.slice(-5) // Last 5 for preview
        };
      } catch (error) {
        steps[1].status = 'failed';
        steps[1].error = error.message;
        throw error;
      }
    }

    // STEP 3: Build agent prompt
    const stepIndex = useMemory ? 2 : 1;
    steps.push({ step: stepIndex + 1, name: 'Build Agent Prompt', status: 'running', timestamp: Date.now() });

    const systemPrompt = getSystemPrompt(action);
    const userPrompt = getUserPrompt(action, data);

    steps[stepIndex].status = 'completed';
    steps[stepIndex].duration = Date.now() - steps[stepIndex].timestamp;
    steps[stepIndex].result = {
      systemPromptLength: systemPrompt.length,
      userPromptLength: userPrompt.length,
      systemPromptPreview: systemPrompt.substring(0, 200) + '...',
      userPromptPreview: userPrompt.substring(0, 200) + '...'
    };

    // STEP 4: Call Claude API (or mock)
    const apiStepIndex = stepIndex + 1;
    steps.push({ step: apiStepIndex + 1, name: 'Claude API Call', status: 'running', timestamp: Date.now() });

    let responseText;
    let tokensUsed = 0;

    if (dryRun && mockResponse) {
      // Mock response for testing
      responseText = getMockResponse(action);
      tokensUsed = 0;

      steps[apiStepIndex].status = 'skipped';
      steps[apiStepIndex].duration = Date.now() - steps[apiStepIndex].timestamp;
      steps[apiStepIndex].result = {
        mode: 'mock',
        responsePreview: responseText.substring(0, 200) + '...',
        tokensUsed: 0
      };
    } else if (dryRun) {
      // Dry run - skip API call
      steps[apiStepIndex].status = 'skipped';
      steps[apiStepIndex].duration = 0;
      steps[apiStepIndex].result = {
        mode: 'dry-run',
        message: 'API call skipped (dry-run mode)',
        estimatedTokens: userPrompt.length / 4 // Rough estimate
      };
    } else {
      // Real API call
      try {
        const conversationHistory = useMemory
          ? await memoryManager.getConversationHistory(contactId, 20)
          : [];

        const messages = [
          ...conversationHistory,
          { role: 'user', content: userPrompt }
        ];

        const message = await anthropic.messages.create({
          model: 'claude-sonnet-4-5-20250929',
          max_tokens: 4096,
          system: systemPrompt,
          messages
        });

        responseText = message.content[0].text;
        tokensUsed = message.usage.input_tokens + message.usage.output_tokens;

        steps[apiStepIndex].status = 'completed';
        steps[apiStepIndex].duration = Date.now() - steps[apiStepIndex].timestamp;
        steps[apiStepIndex].result = {
          mode: 'real',
          tokensUsed,
          inputTokens: message.usage.input_tokens,
          outputTokens: message.usage.output_tokens,
          responsePreview: responseText.substring(0, 200) + '...'
        };
      } catch (error) {
        steps[apiStepIndex].status = 'failed';
        steps[apiStepIndex].error = error.message;
        throw error;
      }
    }

    // STEP 5: Save to memory (if enabled and not dry-run)
    if (useMemory && !dryRun && responseText) {
      const memoryStepIndex = apiStepIndex + 1;
      steps.push({ step: memoryStepIndex + 1, name: 'Save to Memory', status: 'running', timestamp: Date.now() });

      try {
        const agentName = getAgentName(action);
        await memoryManager.saveMessage(contactId, businessId, agentName, 'assistant', responseText);

        steps[memoryStepIndex].status = 'completed';
        steps[memoryStepIndex].duration = Date.now() - steps[memoryStepIndex].timestamp;
        steps[memoryStepIndex].result = { saved: true };
      } catch (error) {
        steps[memoryStepIndex].status = 'failed';
        steps[memoryStepIndex].error = error.message;
        // Non-critical error, continue
      }
    }

    // Return test results
    return res.status(200).json({
      success: true,
      executionId,
      mode: dryRun ? 'dry-run' : 'real',
      action,
      contactId,
      businessId,
      steps,
      summary: {
        totalSteps: steps.length,
        completedSteps: steps.filter(s => s.status === 'completed').length,
        failedSteps: steps.filter(s => s.status === 'failed').length,
        skippedSteps: steps.filter(s => s.status === 'skipped').length,
        totalDuration: steps.reduce((sum, s) => sum + (s.duration || 0), 0),
        tokensUsed
      },
      response: responseText || null
    });

  } catch (error) {
    console.error('[Test API] Error:', error);

    // Log error
    await errorTracker.logError('test-api', error, {
      contactId: req.body?.contactId,
      businessId: req.body?.businessId,
      action: req.body?.action
    });

    return res.status(500).json({
      success: false,
      executionId,
      error: error.message,
      steps
    });
  }
}

/**
 * Get system prompt for action
 */
function getSystemPrompt(action) {
  const prompts = {
    'score-lead': `You are the Lead Scorer for Circuit OS™, a sophisticated AI agent that combines BANT, MEDDIC, and CHAMP qualification frameworks with Virtual LPR™ geospatial intelligence.

Your job: Score leads 0-100 based on FIT (40 points), INTENT (40 points), and TIMING (20 points).

Return structured JSON with score, reasoning, and next actions.`,

    'generate-copy': `You are the Master Copywriter for Circuit OS™, trained in:
- Russell Brunson's Hook-Story-Offer framework
- Eugene Schwartz's 5 Awareness Levels
- Alex Hormozi's Value Equation

Your job: Generate high-converting copy that matches the lead's awareness level and channel.

Return structured response with hook, body, CTA, and reasoning.`,

    'respond-to-review': `You are the Reputation Guardian for Circuit OS™.

Your job: Craft authentic, empathetic responses to Google reviews that:
- Thank positive reviewers
- Address negative feedback professionally
- Showcase business values
- Encourage action

Return structured response with reply text and sentiment analysis.`,

    'get-summary': `You are the Conversation Summarizer for Circuit OS™.

Your job: Analyze conversation history and provide actionable insights.`
  };

  return prompts[action] || 'You are a helpful AI assistant.';
}

/**
 * Get user prompt for action
 */
function getUserPrompt(action, data) {
  switch (action) {
    case 'score-lead':
      return `Score this lead:

Contact: ${JSON.stringify(data.contact || {}, null, 2)}
Business: ${JSON.stringify(data.business || {}, null, 2)}
Virtual LPR Data: ${JSON.stringify(data.virtualLPR || {}, null, 2)}

Return JSON with: { score, fit_score, intent_score, timing_score, reasoning, next_actions }`;

    case 'generate-copy':
      return `Generate copy for this lead:

Contact: ${JSON.stringify(data.contact || {}, null, 2)}
Business: ${JSON.stringify(data.business || {}, null, 2)}
Channel: ${data.channel || 'EMAIL'}
Awareness Level: ${data.awareness_level || 'Problem Aware'}

Return JSON with: { hook, body, cta, reasoning }`;

    case 'respond-to-review':
      return `Respond to this review:

Business: ${data.business?.name || 'Unknown Business'}
Review Rating: ${data.rating || 0}/5
Review Text: "${data.review_text || ''}"
Reviewer Name: ${data.reviewer_name || 'Anonymous'}

Return JSON with: { reply_text, sentiment, tone, keywords }`;

    default:
      return JSON.stringify(data);
  }
}

/**
 * Get mock response for testing
 */
function getMockResponse(action) {
  const mockResponses = {
    'score-lead': JSON.stringify({
      score: 87,
      fit_score: 36,
      intent_score: 35,
      timing_score: 16,
      reasoning: "HIGH-INTENT LEAD: Recent GMB directions click (0.3 mi away), mobile search, fitness interest matches gym category.",
      next_actions: ["Send immediate SMS offer", "Schedule automated follow-up", "Flag for sales team"]
    }, null, 2),

    'generate-copy': JSON.stringify({
      hook: "John - you're literally 5 minutes away from your first FREE training session 🎯",
      body: "Saw you looked up directions to Test Gym in Brooklyn. Here's the deal: most people spend 6+ months 'planning' to start. You already took action by looking us up.\n\nWhat if you could start TODAY? First session on us, no strings attached.",
      cta: "Reply YES and I'll text you the best times for tomorrow.",
      reasoning: "Solution Aware prospect, high intent signal (directions), proximity creates urgency."
    }, null, 2),

    'respond-to-review': JSON.stringify({
      reply_text: "Thank you so much for the 5-star review! We're thrilled you had a great experience. Looking forward to seeing you again soon!",
      sentiment: "positive",
      tone: "grateful",
      keywords: ["thank you", "thrilled", "great experience"]
    }, null, 2)
  };

  return mockResponses[action] || '{ "mock": true, "message": "This is a mock response" }';
}

/**
 * Get agent name for action
 */
function getAgentName(action) {
  const agentNames = {
    'score-lead': 'Lead Scorer',
    'generate-copy': 'Copywriter',
    'respond-to-review': 'Reputation Guardian'
  };

  return agentNames[action] || 'Unknown Agent';
}
