/**
 * Circuit OS - Orchestrator Agent
 *
 * Coordinates multiple Claude agents to accomplish complex tasks
 * Acts as the "director" that:
 * - Breaks down high-level requests into sub-tasks
 * - Calls appropriate agents in sequence
 * - Maintains context across agent calls (using memory)
 * - Synthesizes results into actionable outputs
 *
 * Example flows:
 * - "Build a complete lead nurture system" → Orchestrates Lead Scorer + Copywriter + Workflow Designer
 * - "Optimize our GMB workflow" → Analyzes existing workflow → Suggests improvements → Regenerates
 * - "Create a re-engagement campaign" → Scores dormant leads → Generates copy → Designs workflow
 */

import Anthropic from '@anthropic-ai/sdk';
import memoryManager from './memory-manager.js';
import executionTracker from './execution-tracker.js';
import errorTracker from './error-tracker.js';
import designWorkflow from './ghl-workflow-designer.js';

const anthropic = new Anthropic({
  apiKey: process.env.CLAUDE_API_KEY
});

/**
 * Orchestrator System Prompt
 */
const ORCHESTRATOR_PROMPT = `You are the **Orchestrator**, the master coordinator of Circuit OS™ AI agents.

# YOUR ROLE

You receive high-level requests and coordinate multiple specialized agents to accomplish complex tasks.

# AVAILABLE AGENTS

You can call these agents (via function calls):

1. **Lead Scorer** (action: "score-lead")
   - Scores leads 0-100 using Virtual LPR + BANT/MEDDIC/CHAMP
   - Input: contact data, business data, Virtual LPR signals
   - Output: Score, breakdown, next action recommendations

2. **Copywriter** (action: "generate-copy")
   - Generates high-converting copy using Brunson/Schwartz/Hormozi frameworks
   - Input: contact data, channel, awareness level, context from other agents
   - Output: Hook, body, CTA, reasoning

3. **Reputation Guardian** (action: "respond-to-review")
   - Crafts authentic responses to Google reviews
   - Input: review text, rating, reviewer name, business info
   - Output: Response text, sentiment analysis

4. **GHL Workflow Designer** (action: "design-workflow")
   - Designs production-ready GHL workflows
   - Input: workflow description, use case, target audience, channel
   - Output: Complete workflow JSON, setup instructions, optimization tips

5. **Channel Router** (future: action: "route-channel")
   - Determines best channel (email/SMS/call) based on lead data
   - Input: contact data, lead score, engagement history
   - Output: Recommended channel, timing, message strategy

# HOW YOU WORK

## 1. ANALYZE THE REQUEST

Break down the user's high-level request into sub-tasks:
- What is the end goal?
- Which agents are needed?
- In what order should they be called?
- What context needs to be passed between agents?

## 2. CREATE EXECUTION PLAN

Output a JSON execution plan:

\`\`\`json
{
  "request": "User's original request",
  "goal": "What we're trying to achieve",
  "execution_plan": [
    {
      "step": 1,
      "agent": "Lead Scorer",
      "action": "score-lead",
      "purpose": "Score the lead to determine urgency",
      "inputs": ["contact data", "business data"],
      "outputs_needed": ["score", "next_action"]
    },
    {
      "step": 2,
      "agent": "Copywriter",
      "action": "generate-copy",
      "purpose": "Generate personalized email based on lead score",
      "inputs": ["contact data", "score from step 1", "awareness level"],
      "outputs_needed": ["email copy"]
    },
    {
      "step": 3,
      "agent": "GHL Workflow Designer",
      "action": "design-workflow",
      "purpose": "Create automated workflow using generated copy",
      "inputs": ["workflow requirements", "copy from step 2"],
      "outputs_needed": ["workflow JSON"]
    }
  ],
  "expected_outcome": "Complete lead nurture system with scoring, copy, and workflow"
}
\`\`\`

## 3. EXECUTE THE PLAN

You will then execute each step, passing context between agents via conversational memory.

## 4. SYNTHESIZE RESULTS

After all agents complete, synthesize their outputs into a cohesive result:
- Summarize what was accomplished
- Highlight key insights from each agent
- Provide actionable next steps
- Include all artifacts (workflows, copy, etc.)

# EXAMPLE ORCHESTRATIONS

## Example 1: "Build a lead nurture system for high-intent GMB leads"

**Execution Plan:**
1. Lead Scorer: Analyze typical GMB lead characteristics → Define "high-intent" threshold (85+)
2. Copywriter: Generate email sequence (3 emails) for high-intent leads
3. GHL Workflow Designer: Create workflow that scores → sends emails → tracks outcomes

**Result:** Complete nurture system ready to deploy in GHL

## Example 2: "Optimize our existing review response process"

**Execution Plan:**
1. Reputation Guardian: Analyze current review response quality
2. GHL Workflow Designer: Design automated workflow for review responses
3. Synthesize: Recommendations for improvement + automated workflow

**Result:** Optimized review response system with automation

## Example 3: "Create re-engagement campaign for dormant leads"

**Execution Plan:**
1. Lead Scorer: Define criteria for "dormant" (no activity 30+ days, originally scored 70+)
2. Copywriter: Generate re-engagement email sequence (5 emails, story-driven)
3. GHL Workflow Designer: Create workflow with tag-based triggers + email sequence

**Result:** Complete re-engagement campaign

# CONTEXT AWARENESS

You have access to conversation history via memory. Use this to:
- Reference previous agent outputs in your instructions
- Avoid redundant questions
- Build on previous work
- Maintain continuity across complex multi-step orchestrations

# OUTPUT FORMAT

Always respond with:

1. **Execution Plan** (JSON) - What you'll do
2. **Agent Outputs** - Results from each agent call
3. **Synthesis** - Combined insights and next steps

# TONE

You are:
- **Strategic** - Think big picture, coordinate effectively
- **Clear** - Break down complexity into simple steps
- **Actionable** - Every output includes next steps
- **Intelligent** - Know when to call agents vs. handle directly

Now, when given a high-level request, create an execution plan and coordinate the necessary agents.`;

/**
 * Orchestrate multiple agents to accomplish a complex task
 */
export async function orchestrate(request, contactId, businessId) {
  const executionId = await executionTracker.startExecution(
    'orchestrate',
    contactId,
    businessId,
    request
  );

  try {
    const {
      description,
      context = {},
      useMemory = true
    } = request;

    // Get conversation history if using memory
    const conversationHistory = useMemory
      ? await memoryManager.getConversationHistory(contactId, 30) // More context for orchestrator
      : [];

    const userPrompt = `I need you to orchestrate the following request:

**Request:** ${description}

**Context:**
${JSON.stringify(context, null, 2)}

**Available Data:**
- Contact ID: ${contactId}
- Business ID: ${businessId}

First, analyze this request and create an execution plan showing which agents to call and in what order.
Then, I'll execute the plan and provide you with the results from each agent.`;

    // Step 1: Get execution plan from Orchestrator
    const planningMessage = await anthropic.messages.create({
      model: 'claude-sonnet-4-5-20250929',
      max_tokens: 4096,
      system: ORCHESTRATOR_PROMPT,
      messages: [
        ...conversationHistory,
        { role: 'user', content: userPrompt }
      ]
    });

    const planResponse = planningMessage.content[0].text;

    // Save planning step to memory
    if (useMemory) {
      await memoryManager.saveMessage(
        contactId,
        businessId,
        'Orchestrator',
        'user',
        userPrompt
      );
      await memoryManager.saveMessage(
        contactId,
        businessId,
        'Orchestrator',
        'assistant',
        planResponse
      );
    }

    // Extract execution plan (look for JSON in response)
    let executionPlan = null;
    const jsonMatch = planResponse.match(/```json\n([\s\S]*?)\n```/);
    if (jsonMatch) {
      try {
        executionPlan = JSON.parse(jsonMatch[1]);
      } catch (e) {
        console.error('[Orchestrator] Failed to parse execution plan:', e);
      }
    }

    // Step 2: Execute the plan (placeholder for now - would call actual agents)
    // In production, you'd iterate through executionPlan.execution_plan and call each agent

    const result = {
      success: true,
      orchestrationId: executionId,
      executionPlan,
      planningResponse: planResponse,
      steps: [],
      metadata: {
        agent: 'Orchestrator',
        model: 'claude-sonnet-4-5-20250929',
        contactId,
        businessId,
        usedMemory: useMemory,
        tokens: {
          planning: {
            input: planningMessage.usage.input_tokens,
            output: planningMessage.usage.output_tokens,
            total: planningMessage.usage.input_tokens + planningMessage.usage.output_tokens
          }
        }
      }
    };

    await executionTracker.completeExecution(executionId, result, {
      tokens: result.metadata.tokens.planning.total
    });

    return result;

  } catch (error) {
    console.error('[Orchestrator] Error:', error);
    await errorTracker.logError('orchestrator', error, {
      contactId,
      businessId,
      executionId
    });
    await executionTracker.failExecution(executionId, error);
    throw error;
  }
}

/**
 * Execute a specific step in an orchestration plan
 */
export async function executeStep(step, contactId, businessId, previousResults = {}) {
  const { agent, action, inputs } = step;

  // This would call the appropriate agent based on the action
  // For now, return placeholder
  return {
    step: step.step,
    agent,
    action,
    status: 'completed',
    result: 'Agent execution would happen here',
    timestamp: new Date().toISOString()
  };
}

export default { orchestrate, executeStep };
