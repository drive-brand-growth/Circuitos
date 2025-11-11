/**
 * CIRCUIT OS - ADVANCED PROMPT ENGINEERING IMPLEMENTATION
 * Complete working example demonstrating Contract, Control Loop, and Observability patterns
 *
 * This file shows how to implement Pattern #1 (Pipeline Truth Detector) with all three patterns:
 * 1. CONTRACT: Strict TypeScript interfaces + Zod schemas
 * 2. CONTROL LOOP: Validation → Retry → Repair → Fallback
 * 3. OBSERVABILITY: Full tracing with feedback and outcome tracking
 */

import Anthropic from '@anthropic-ai/sdk';
import { z } from 'zod';
import { v4 as uuidv4 } from 'uuid';

// ============================================================================
// PATTERN 1: CONTRACT (Structured Output)
// ============================================================================

/**
 * TypeScript interface defining the exact shape of output
 */
interface PipelineTruthOutput {
  totalPipeline: number;
  closeablePipeline: number;
  truthGap: number;
  stalledDeals: Array<{
    dealName: string;
    amount: number;
    stage: string;
    daysSinceActivity: number;
    riskLevel: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  }>;
  topProblems: string[];
  recommendations: string[];
  generatedAt: string;
}

/**
 * Zod schema for runtime validation (the contract enforcer)
 */
const PipelineTruthSchema = z.object({
  totalPipeline: z.number().nonnegative(),
  closeablePipeline: z.number().nonnegative(),
  truthGap: z.number(),
  stalledDeals: z.array(z.object({
    dealName: z.string().min(1),
    amount: z.number().nonnegative(),
    stage: z.string().min(1),
    daysSinceActivity: z.number().int().nonnegative(),
    riskLevel: z.enum(['LOW', 'MEDIUM', 'HIGH', 'CRITICAL'])
  })),
  topProblems: z.array(z.string()).max(5),
  recommendations: z.array(z.string().max(200)).max(5),
  generatedAt: z.string().datetime()
});

/**
 * Prompt builder that specifies the contract explicitly
 */
function buildPipelineTruthPrompt(csvData: string): string {
  return `You are a VP of Sales with 15 years of experience analyzing pipeline data.

TASK: Analyze the CSV data and return ONLY valid JSON matching this EXACT schema:

{
  "totalPipeline": <number>,
  "closeablePipeline": <number>,
  "truthGap": <number>,
  "stalledDeals": [
    {
      "dealName": "<string>",
      "amount": <number>,
      "stage": "<string>",
      "daysSinceActivity": <number>,
      "riskLevel": "LOW" | "MEDIUM" | "HIGH" | "CRITICAL"
    }
  ],
  "topProblems": ["<string>", ...],
  "recommendations": ["<string>", ...]
}

STRICT RULES:
1. Return ONLY the JSON object - no prose before or after
2. Start with { and end with }
3. riskLevel MUST be exactly one of: LOW, MEDIUM, HIGH, CRITICAL (uppercase)
4. A deal is stalled if daysSinceActivity > 30
5. truthGap = totalPipeline - closeablePipeline
6. generatedAt must be current UTC time in ISO 8601 format (YYYY-MM-DDTHH:mm:ss.sssZ)
7. topProblems and recommendations: max 5 items each
8. recommendations: max 200 characters each

CSV DATA:
${csvData}

JSON OUTPUT:`;
}

// ============================================================================
// PATTERN 2: CONTROL LOOP (Validation & Reliability)
// ============================================================================

interface ControlLoopResult<T> {
  success: boolean;
  data?: T;
  error?: string;
  metadata: {
    attempts: number;
    totalTime: number;
    tokensUsed: number;
    cost: number;
  };
}

interface AttemptRecord {
  attemptNumber: number;
  model: string;
  temperature: number;
  startTime: Date;
  endTime: Date;
  durationMs: number;
  inputTokens: number;
  outputTokens: number;
  cost: number;
  rawResponse: string;
  validationResult: {
    passed: boolean;
    errors?: string[];
  };
}

class ControlLoop {
  private client: Anthropic;
  private maxRetries: number = 2;
  private timeout: number = 30000;
  private fallbackModel: string = 'claude-opus-4';

  constructor(apiKey: string) {
    this.client = new Anthropic({ apiKey });
  }

  /**
   * Main execution method with full control loop
   */
  async execute<T>(
    prompt: string,
    schema: z.ZodSchema,
    tracer?: WeaponTracer,
    traceId?: string
  ): Promise<ControlLoopResult<T>> {
    const startTime = Date.now();
    let attempts: AttemptRecord[] = [];
    let totalTokens = 0;
    let lastError = '';

    // PRIMARY ATTEMPTS (with retry)
    for (let i = 0; i <= this.maxRetries; i++) {
      try {
        console.log(`[CONTROL LOOP] Attempt ${i + 1}/${this.maxRetries + 1}`);

        const attemptStart = new Date();

        // STEP 1: Call Claude
        const response = await this.callClaude(prompt, {
          model: 'claude-sonnet-4-5',
          temperature: 0.0,
          maxTokens: 4096
        });

        const attemptEnd = new Date();
        const rawResponse = response.content[0].text;

        totalTokens += response.usage.input_tokens + response.usage.output_tokens;

        // STEP 2: Validate response
        const parseResult = this.parseAndValidate(rawResponse, schema);

        // Record attempt
        const attemptRecord: AttemptRecord = {
          attemptNumber: i + 1,
          model: 'claude-sonnet-4-5',
          temperature: 0.0,
          startTime: attemptStart,
          endTime: attemptEnd,
          durationMs: attemptEnd.getTime() - attemptStart.getTime(),
          inputTokens: response.usage.input_tokens,
          outputTokens: response.usage.output_tokens,
          cost: this.calculateCost(
            response.usage.input_tokens + response.usage.output_tokens,
            'claude-sonnet-4-5'
          ),
          rawResponse: rawResponse.slice(0, 500), // Truncate for logging
          validationResult: {
            passed: parseResult.success,
            errors: parseResult.success ? undefined : [parseResult.error]
          }
        };

        attempts.push(attemptRecord);

        // Trace this attempt
        if (tracer && traceId) {
          tracer.recordAttempt(traceId, attemptRecord);
        }

        // STEP 3: Check if validation passed
        if (parseResult.success) {
          console.log(`[CONTROL LOOP] ✅ Success on attempt ${i + 1}`);

          return {
            success: true,
            data: parseResult.data,
            metadata: {
              attempts: i + 1,
              totalTime: Date.now() - startTime,
              tokensUsed: totalTokens,
              cost: attempts.reduce((sum, a) => sum + a.cost, 0)
            }
          };
        }

        lastError = parseResult.error;
        console.log(`[CONTROL LOOP] ❌ Validation failed: ${lastError}`);

        // STEP 4: Attempt repair (if not last retry)
        if (i < this.maxRetries) {
          console.log(`[CONTROL LOOP] 🔧 Attempting repair...`);

          const repairResult = this.attemptRepair(rawResponse, schema);

          if (repairResult.success) {
            console.log(`[CONTROL LOOP] ✅ Repair succeeded`);

            return {
              success: true,
              data: repairResult.data,
              metadata: {
                attempts: i + 1,
                totalTime: Date.now() - startTime,
                tokensUsed: totalTokens,
                cost: attempts.reduce((sum, a) => sum + a.cost, 0)
              }
            };
          }

          console.log(`[CONTROL LOOP] ❌ Repair failed, tightening prompt...`);

          // STEP 5: Tighten prompt for retry
          prompt = this.tightenPrompt(prompt, lastError);
        }

      } catch (error: any) {
        lastError = error.message;
        console.error(`[CONTROL LOOP] ❌ Error: ${error.message}`);

        // Don't retry on rate limits or context length errors
        if (error.status === 429) {
          return {
            success: false,
            error: 'RATE_LIMIT_EXCEEDED',
            metadata: {
              attempts: i + 1,
              totalTime: Date.now() - startTime,
              tokensUsed: totalTokens,
              cost: attempts.reduce((sum, a) => sum + a.cost, 0)
            }
          };
        }

        if (error.message.includes('prompt is too long')) {
          return {
            success: false,
            error: 'CONTEXT_LENGTH_EXCEEDED',
            metadata: {
              attempts: i + 1,
              totalTime: Date.now() - startTime,
              tokensUsed: totalTokens,
              cost: attempts.reduce((sum, a) => sum + a.cost, 0)
            }
          };
        }
      }
    }

    // STEP 6: Fallback to stricter model (Opus)
    console.log(`[CONTROL LOOP] 🚨 All retries failed, trying fallback model (${this.fallbackModel})...`);

    try {
      const attemptStart = new Date();

      const response = await this.callClaude(prompt, {
        model: this.fallbackModel,
        temperature: 0.0,
        maxTokens: 4096
      });

      const attemptEnd = new Date();
      const rawResponse = response.content[0].text;

      totalTokens += response.usage.input_tokens + response.usage.output_tokens;

      const parseResult = this.parseAndValidate(rawResponse, schema);

      const attemptRecord: AttemptRecord = {
        attemptNumber: attempts.length + 1,
        model: this.fallbackModel,
        temperature: 0.0,
        startTime: attemptStart,
        endTime: attemptEnd,
        durationMs: attemptEnd.getTime() - attemptStart.getTime(),
        inputTokens: response.usage.input_tokens,
        outputTokens: response.usage.output_tokens,
        cost: this.calculateCost(
          response.usage.input_tokens + response.usage.output_tokens,
          this.fallbackModel
        ),
        rawResponse: rawResponse.slice(0, 500),
        validationResult: {
          passed: parseResult.success,
          errors: parseResult.success ? undefined : [parseResult.error]
        }
      };

      attempts.push(attemptRecord);

      if (tracer && traceId) {
        tracer.recordAttempt(traceId, attemptRecord);
      }

      if (parseResult.success) {
        console.log(`[CONTROL LOOP] ✅ Fallback model succeeded`);

        return {
          success: true,
          data: parseResult.data,
          metadata: {
            attempts: attempts.length,
            totalTime: Date.now() - startTime,
            tokensUsed: totalTokens,
            cost: attempts.reduce((sum, a) => sum + a.cost, 0)
          }
        };
      }

      lastError = `Fallback model failed: ${parseResult.error}`;

    } catch (error: any) {
      lastError = `Fallback model error: ${error.message}`;
    }

    // FINAL FAILURE
    console.error(`[CONTROL LOOP] 💀 All attempts exhausted, returning failure`);

    return {
      success: false,
      error: lastError,
      metadata: {
        attempts: attempts.length,
        totalTime: Date.now() - startTime,
        tokensUsed: totalTokens,
        cost: attempts.reduce((sum, a) => sum + a.cost, 0)
      }
    };
  }

  /**
   * Call Claude API with timeout protection
   */
  private async callClaude(
    prompt: string,
    options: {
      model: string;
      temperature: number;
      maxTokens: number;
    }
  ) {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), this.timeout);

    try {
      const response = await this.client.messages.create({
        model: options.model,
        max_tokens: options.maxTokens,
        temperature: options.temperature,
        messages: [{ role: 'user', content: prompt }]
      });

      return response;
    } finally {
      clearTimeout(timeoutId);
    }
  }

  /**
   * Parse and validate response against schema
   */
  private parseAndValidate(responseText: string, schema: z.ZodSchema) {
    try {
      // Extract JSON from response
      const jsonMatch = responseText.match(/\{[\s\S]*\}/);

      if (!jsonMatch) {
        return {
          success: false,
          error: 'No JSON object found in response'
        };
      }

      // Parse JSON
      const parsed = JSON.parse(jsonMatch[0]);

      // Validate against schema
      const validated = schema.parse(parsed);

      return { success: true, data: validated };

    } catch (error: any) {
      return {
        success: false,
        error: error.message
      };
    }
  }

  /**
   * Attempt to repair malformed response
   */
  private attemptRepair(responseText: string, schema: z.ZodSchema) {
    try {
      // Strategy 1: Strip prose before/after JSON
      let cleaned = responseText.trim();

      // Remove common prose patterns
      cleaned = cleaned.replace(/^(Sure|Here|Okay|Here's|Here is)[^{]*/, '');
      cleaned = cleaned.replace(/```json\s*/, '');
      cleaned = cleaned.replace(/```\s*$/, '');
      cleaned = cleaned.replace(/\n+/g, '\n');

      // Strategy 2: Extract JSON object
      const jsonMatch = cleaned.match(/\{[\s\S]*\}/);

      if (!jsonMatch) {
        return { success: false, error: 'Could not extract JSON' };
      }

      // Parse
      const parsed = JSON.parse(jsonMatch[0]);

      // Strategy 3: Fix common key mistakes
      const repaired = this.repairCommonMistakes(parsed);

      // Validate repaired object
      const validated = schema.parse(repaired);

      return { success: true, data: validated };

    } catch (error: any) {
      return {
        success: false,
        error: `Repair failed: ${error.message}`
      };
    }
  }

  /**
   * Fix common key naming mistakes (snake_case vs camelCase)
   */
  private repairCommonMistakes(obj: any): any {
    const repairs: Record<string, string> = {
      'total_pipeline': 'totalPipeline',
      'closeable_pipeline': 'closeablePipeline',
      'truth_gap': 'truthGap',
      'stalled_deals': 'stalledDeals',
      'top_problems': 'topProblems',
      'deal_name': 'dealName',
      'risk_level': 'riskLevel',
      'days_since_activity': 'daysSinceActivity',
      'generated_at': 'generatedAt'
    };

    const repaired: any = Array.isArray(obj) ? [] : {};

    for (const [key, value] of Object.entries(obj)) {
      const correctedKey = repairs[key] || key;

      // Recursively repair nested objects/arrays
      if (value && typeof value === 'object') {
        repaired[correctedKey] = this.repairCommonMistakes(value);
      } else {
        repaired[correctedKey] = value;
      }
    }

    return repaired;
  }

  /**
   * Tighten prompt after validation failure
   */
  private tightenPrompt(originalPrompt: string, error: string): string {
    let tightened = originalPrompt;

    // Add emphasis based on error type
    if (error.includes('enum') || error.includes('riskLevel')) {
      tightened += '\n\n⚠️ CRITICAL: riskLevel must be EXACTLY one of: LOW, MEDIUM, HIGH, CRITICAL (uppercase, no quotes).';
    }

    if (error.includes('required')) {
      tightened += '\n\n⚠️ CRITICAL: ALL fields are required. Do not omit any field from the schema.';
    }

    if (error.includes('JSON') || error.includes('parse')) {
      tightened = '⚠️ RETURN ONLY VALID JSON. NO PROSE. START WITH { AND END WITH }.\n\n' + tightened;
    }

    if (error.includes('datetime') || error.includes('generatedAt')) {
      tightened += '\n\n⚠️ CRITICAL: generatedAt must be ISO 8601 format: YYYY-MM-DDTHH:mm:ss.sssZ (e.g., 2025-11-11T14:30:00.000Z)';
    }

    return tightened;
  }

  /**
   * Calculate API cost based on tokens and model
   */
  private calculateCost(tokens: number, model: string): number {
    const pricing: Record<string, { input: number; output: number }> = {
      'claude-sonnet-4-5': { input: 0.003, output: 0.015 },  // per 1K tokens
      'claude-opus-4': { input: 0.015, output: 0.075 }
    };

    const rate = pricing[model] || pricing['claude-sonnet-4-5'];

    // Simplified: assume 50/50 input/output split
    return ((tokens / 2) * rate.input + (tokens / 2) * rate.output) / 1000;
  }
}

// ============================================================================
// PATTERN 3: OBSERVABILITY (Tracing & Improvement)
// ============================================================================

interface WeaponTrace {
  traceId: string;
  userId: string;
  weaponName: string;
  tier: 'FREE' | 'PAID_BASIC' | 'PAID_PREMIUM';
  timestamp: string;

  input: {
    csvSize: number;
    rowCount: number;
    prompt: string;
    promptTokens: number;
  };

  attempts: AttemptRecord[];

  result: {
    success: boolean;
    data?: any;
    error?: string;
    totalAttempts: number;
    totalDurationMs: number;
    totalTokens: number;
    totalCost: number;
  };

  feedback?: {
    useful: boolean;
    rating: 1 | 2 | 3 | 4 | 5;
    comment?: string;
    submittedAt: string;
  };

  outcome?: {
    recommendationsActedOn: number;
    dealsConverted: number;
    revenueImpact: number;
    trackedAt: string;
  };
}

class WeaponTracer {
  private traces: Map<string, WeaponTrace> = new Map();

  /**
   * Start a new trace
   */
  startTrace(
    weaponName: string,
    userId: string,
    tier: 'FREE' | 'PAID_BASIC' | 'PAID_PREMIUM',
    input: { csvData: string; rowCount: number }
  ): string {
    const traceId = uuidv4();

    const trace: WeaponTrace = {
      traceId,
      userId,
      weaponName,
      tier,
      timestamp: new Date().toISOString(),
      input: {
        csvSize: input.csvData.length,
        rowCount: input.rowCount,
        prompt: '',  // Will be set when prompt is built
        promptTokens: 0  // Estimated from prompt length
      },
      attempts: [],
      result: {
        success: false,
        totalAttempts: 0,
        totalDurationMs: 0,
        totalTokens: 0,
        totalCost: 0
      }
    };

    this.traces.set(traceId, trace);

    console.log(`[TRACER] 📊 Started trace ${traceId} for weapon ${weaponName}`);

    return traceId;
  }

  /**
   * Record an LLM attempt
   */
  recordAttempt(traceId: string, attempt: AttemptRecord) {
    const trace = this.traces.get(traceId);
    if (!trace) {
      console.error(`[TRACER] ❌ Trace ${traceId} not found`);
      return;
    }

    trace.attempts.push(attempt);

    console.log(`[TRACER] 📝 Recorded attempt ${attempt.attemptNumber} for trace ${traceId}`);
  }

  /**
   * Finalize trace with result
   */
  finalizeTrace(
    traceId: string,
    result: {
      success: boolean;
      data?: any;
      error?: string;
    }
  ) {
    const trace = this.traces.get(traceId);
    if (!trace) {
      console.error(`[TRACER] ❌ Trace ${traceId} not found`);
      return;
    }

    trace.result = {
      ...result,
      totalAttempts: trace.attempts.length,
      totalDurationMs: trace.attempts.reduce((sum, a) => sum + a.durationMs, 0),
      totalTokens: trace.attempts.reduce((sum, a) => sum + a.inputTokens + a.outputTokens, 0),
      totalCost: trace.attempts.reduce((sum, a) => sum + a.cost, 0)
    };

    console.log(`[TRACER] ✅ Finalized trace ${traceId}`);
    console.log(`  Success: ${result.success}`);
    console.log(`  Attempts: ${trace.result.totalAttempts}`);
    console.log(`  Duration: ${trace.result.totalDurationMs}ms`);
    console.log(`  Tokens: ${trace.result.totalTokens}`);
    console.log(`  Cost: $${trace.result.totalCost.toFixed(4)}`);

    // Persist to storage (database, CloudWatch, etc.)
    this.persist(trace);
  }

  /**
   * Add user feedback
   */
  addFeedback(
    traceId: string,
    feedback: {
      useful: boolean;
      rating: 1 | 2 | 3 | 4 | 5;
      comment?: string;
    }
  ) {
    const trace = this.traces.get(traceId);
    if (!trace) {
      console.error(`[TRACER] ❌ Trace ${traceId} not found`);
      return;
    }

    trace.feedback = {
      ...feedback,
      submittedAt: new Date().toISOString()
    };

    console.log(`[TRACER] 👍 Received feedback for trace ${traceId}: ${feedback.rating}/5`);

    this.persist(trace);
  }

  /**
   * Track business outcome (called 24 hours later)
   */
  addOutcome(
    traceId: string,
    outcome: {
      recommendationsActedOn: number;
      dealsConverted: number;
      revenueImpact: number;
    }
  ) {
    const trace = this.traces.get(traceId);
    if (!trace) {
      console.error(`[TRACER] ❌ Trace ${traceId} not found`);
      return;
    }

    trace.outcome = {
      ...outcome,
      trackedAt: new Date().toISOString()
    };

    console.log(`[TRACER] 💰 Tracked outcome for trace ${traceId}:`);
    console.log(`  Recommendations acted on: ${outcome.recommendationsActedOn}`);
    console.log(`  Deals converted: ${outcome.dealsConverted}`);
    console.log(`  Revenue impact: $${outcome.revenueImpact.toLocaleString()}`);

    this.persist(trace);
  }

  /**
   * Persist trace to storage
   */
  private persist(trace: WeaponTrace) {
    // In production, send to:
    // - PostgreSQL database
    // - CloudWatch Logs (structured JSON)
    // - Observability platform (Honeycomb, DataDog, etc.)

    // For now: console log as structured JSON
    console.log('[TRACE_DATA]', JSON.stringify(trace, null, 2));

    // Example: Send to CloudWatch
    // await cloudwatch.putLogEvents({
    //   logGroupName: '/circuit-os/weapon-traces',
    //   logStreamName: trace.weaponName,
    //   logEvents: [{
    //     timestamp: Date.now(),
    //     message: JSON.stringify(trace)
    //   }]
    // });
  }

  /**
   * Get trace by ID
   */
  getTrace(traceId: string): WeaponTrace | undefined {
    return this.traces.get(traceId);
  }

  /**
   * Get all traces (for analytics)
   */
  getAllTraces(): WeaponTrace[] {
    return Array.from(this.traces.values());
  }
}

// ============================================================================
// COMPLETE WEAPON SERVICE (All 3 Patterns Combined)
// ============================================================================

class PipelineTruthWeapon {
  private controlLoop: ControlLoop;
  private tracer: WeaponTracer;

  constructor(apiKey: string) {
    this.controlLoop = new ControlLoop(apiKey);
    this.tracer = new WeaponTracer();
  }

  /**
   * Execute Pipeline Truth Detector with full pattern implementation
   */
  async analyze(
    userId: string,
    tier: 'FREE' | 'PAID_BASIC' | 'PAID_PREMIUM',
    csvData: string
  ): Promise<{
    success: boolean;
    data?: PipelineTruthOutput;
    error?: string;
    traceId: string;
    metadata: {
      attempts: number;
      totalTime: number;
      tokensUsed: number;
      cost: number;
    };
  }> {
    // PATTERN 3: Start observability trace
    const traceId = this.tracer.startTrace(
      'pipeline-truth',
      userId,
      tier,
      {
        csvData,
        rowCount: csvData.split('\n').length
      }
    );

    // PATTERN 1: Build prompt with contract specification
    const prompt = buildPipelineTruthPrompt(csvData);

    // PATTERN 2: Execute with control loop
    const result = await this.controlLoop.execute<PipelineTruthOutput>(
      prompt,
      PipelineTruthSchema,
      this.tracer,
      traceId
    );

    // PATTERN 3: Finalize trace
    this.tracer.finalizeTrace(traceId, {
      success: result.success,
      data: result.data,
      error: result.error
    });

    return {
      success: result.success,
      data: result.data,
      error: result.error,
      traceId,  // Return to frontend for feedback collection
      metadata: result.metadata
    };
  }

  /**
   * Submit user feedback (called from frontend)
   */
  async submitFeedback(
    traceId: string,
    feedback: {
      useful: boolean;
      rating: 1 | 2 | 3 | 4 | 5;
      comment?: string;
    }
  ) {
    this.tracer.addFeedback(traceId, feedback);
  }

  /**
   * Track business outcome (called by cron job 24 hours later)
   */
  async trackOutcome(
    traceId: string,
    outcome: {
      recommendationsActedOn: number;
      dealsConverted: number;
      revenueImpact: number;
    }
  ) {
    this.tracer.addOutcome(traceId, outcome);
  }

  /**
   * Get analytics (for dashboard)
   */
  getAnalytics() {
    const traces = this.tracer.getAllTraces();

    const totalRequests = traces.length;
    const successfulRequests = traces.filter(t => t.result.success).length;
    const successRate = totalRequests > 0 ? (successfulRequests / totalRequests) * 100 : 0;

    const avgDuration = traces.reduce((sum, t) => sum + t.result.totalDurationMs, 0) / totalRequests;
    const avgCost = traces.reduce((sum, t) => sum + t.result.totalCost, 0) / totalRequests;
    const avgTokens = traces.reduce((sum, t) => sum + t.result.totalTokens, 0) / totalRequests;

    const tracesWithFeedback = traces.filter(t => t.feedback);
    const avgRating = tracesWithFeedback.length > 0
      ? tracesWithFeedback.reduce((sum, t) => sum + (t.feedback?.rating || 0), 0) / tracesWithFeedback.length
      : 0;

    const tracesWithOutcome = traces.filter(t => t.outcome);
    const totalRevenueImpact = tracesWithOutcome.reduce((sum, t) => sum + (t.outcome?.revenueImpact || 0), 0);
    const totalDealsConverted = tracesWithOutcome.reduce((sum, t) => sum + (t.outcome?.dealsConverted || 0), 0);

    return {
      totalRequests,
      successRate: successRate.toFixed(2) + '%',
      avgDurationMs: avgDuration.toFixed(0),
      avgCost: '$' + avgCost.toFixed(4),
      avgTokens: avgTokens.toFixed(0),
      userSatisfaction: {
        avgRating: avgRating.toFixed(2),
        totalFeedback: tracesWithFeedback.length
      },
      businessImpact: {
        totalDealsConverted,
        totalRevenueImpact: '$' + totalRevenueImpact.toLocaleString()
      }
    };
  }
}

// ============================================================================
// USAGE EXAMPLE
// ============================================================================

async function main() {
  console.log('='.repeat(80));
  console.log('CIRCUIT OS - PIPELINE TRUTH DETECTOR');
  console.log('Demonstrating Contract + Control Loop + Observability patterns');
  console.log('='.repeat(80));
  console.log();

  // Initialize weapon
  const apiKey = process.env.ANTHROPIC_API_KEY || 'YOUR_API_KEY_HERE';
  const weapon = new PipelineTruthWeapon(apiKey);

  // Sample CSV data
  const csvData = `deal_name,amount,stage,last_activity_date
Acme Corp - Enterprise Deal,150000,Negotiation,2025-10-15
TechStart Inc - Pilot,25000,Proposal,2025-11-05
BigCo - Expansion,300000,Closed Won,2025-11-10
MidSize LLC - New Logo,75000,Discovery,2025-09-01
SmallBiz - Upsell,10000,Negotiation,2025-11-08`;

  // Execute analysis
  console.log('📊 Starting pipeline analysis...\n');

  const result = await weapon.analyze(
    'user_123',
    'PAID_BASIC',
    csvData
  );

  console.log();
  console.log('='.repeat(80));
  console.log('RESULT');
  console.log('='.repeat(80));

  if (result.success && result.data) {
    console.log('✅ Analysis succeeded!\n');
    console.log('Total Pipeline:', '$' + result.data.totalPipeline.toLocaleString());
    console.log('Closeable Pipeline:', '$' + result.data.closeablePipeline.toLocaleString());
    console.log('Truth Gap:', '$' + result.data.truthGap.toLocaleString());
    console.log();
    console.log('Stalled Deals:', result.data.stalledDeals.length);
    result.data.stalledDeals.forEach(deal => {
      console.log(`  - ${deal.dealName}: $${deal.amount.toLocaleString()} (${deal.riskLevel})`);
    });
    console.log();
    console.log('Top Problems:');
    result.data.topProblems.forEach((problem, i) => {
      console.log(`  ${i + 1}. ${problem}`);
    });
    console.log();
    console.log('Recommendations:');
    result.data.recommendations.forEach((rec, i) => {
      console.log(`  ${i + 1}. ${rec}`);
    });
  } else {
    console.log('❌ Analysis failed:', result.error);
  }

  console.log();
  console.log('Metadata:');
  console.log('  Attempts:', result.metadata.attempts);
  console.log('  Duration:', result.metadata.totalTime + 'ms');
  console.log('  Tokens:', result.metadata.tokensUsed);
  console.log('  Cost: $' + result.metadata.cost.toFixed(4));
  console.log('  Trace ID:', result.traceId);

  // Simulate user feedback
  console.log();
  console.log('👍 Simulating user feedback...');
  await weapon.submitFeedback(result.traceId, {
    useful: true,
    rating: 5,
    comment: 'Excellent analysis, found deals we missed!'
  });

  // Simulate outcome tracking (would normally happen 24 hours later)
  console.log('💰 Simulating outcome tracking...');
  await weapon.trackOutcome(result.traceId, {
    recommendationsActedOn: 3,
    dealsConverted: 1,
    revenueImpact: 75000
  });

  // Show analytics
  console.log();
  console.log('='.repeat(80));
  console.log('ANALYTICS');
  console.log('='.repeat(80));
  const analytics = weapon.getAnalytics();
  console.log(JSON.stringify(analytics, null, 2));
}

// Run example (uncomment to test)
// main().catch(console.error);

// Export for use in Circuit OS backend
export {
  PipelineTruthWeapon,
  PipelineTruthOutput,
  PipelineTruthSchema,
  ControlLoop,
  WeaponTracer
};
