# Advanced Prompt Engineering for Circuit OS
## Leveraging Contract, Control Loop, and Observability Patterns

**Source:** YouTube video on transforming prompt whispering into real software engineering
**Date:** 2025-11-11
**Status:** Implementation Guide for Production Deployment

---

## Executive Summary

LLMs are **probabilistic**, not deterministic. Changing wording or temperature produces different responses, creating a "bug factory" when integrating LLM output into production software. This document applies three battle-tested patterns to make Circuit OS weapons reliable:

1. **Contract** - Define exact output shape upfront
2. **Control Loop** - Validate, retry, repair, fallback
3. **Observability** - Trace every call, measure everything

**Result:** Transform Claude API calls from unpredictable responses → production-ready skills

---

## Table of Contents

1. [Problem Statement](#problem-statement)
2. [Pattern 1: Contract (Structured Output)](#pattern-1-contract-structured-output)
3. [Pattern 2: Control Loop (Validation & Reliability)](#pattern-2-control-loop-validation--reliability)
4. [Pattern 3: Observability (Tracing & Improvement)](#pattern-3-observability-tracing--improvement)
5. [Implementation for Circuit OS Weapons](#implementation-for-circuit-os-weapons)
6. [Tools: LangChain vs PDL vs Custom](#tools-langchain-vs-pdl-vs-custom)
7. [Migration Path](#migration-path)
8. [Success Metrics](#success-metrics)

---

## Problem Statement

### The Bug Factory

```javascript
// FRAGILE: Current approach (what we have)
const prompt = "Analyze this pipeline data and find stalled deals";
const response = await claude.messages.create({
  model: "claude-sonnet-4-5",
  messages: [{ role: "user", content: prompt }]
});

// Response might be:
// "Sure! I found 5 stalled deals..." (prose + data)
// OR: {"stalledDeals": 5, ...} (JSON)
// OR: {"stalled_deal_count": 5, ...} (different key!)
// OR: **Stalled Deals:** 5 (markdown)
```

**Result:** Parsing fails, frontend breaks, user sees error message.

### The Production Requirement

For Circuit OS weapons to be reliable:
- **Pipeline Truth Detector** must return exact JSON schema every time
- **Deal Defibrillator** must generate valid revival strategies, not prose
- **Forecast Reality Check** must calculate drift with numerical precision
- **Quota Kill Switch** must output structured performance metrics

**Without these patterns, we have a demo. With them, we have a product.**

---

## Pattern 1: Contract (Structured Output)

### Definition

The **Contract** is the exact shape of data the LLM must return. Defined upfront, enforced strictly.

### Current State (Circuit OS)

```javascript
// outreach-agent.js - NO ENFORCEMENT
generateEmail(trigger, persona) {
  const prompt = `Generate email with hook, story, offer...`;
  // Returns string - could be anything
  return claudeAPI(prompt);
}
```

### After Applying Contract Pattern

```typescript
// contracts/weapon-contracts.ts

interface PipelineTruthContract {
  totalPipeline: number;              // Required: sum of all deal amounts
  closeablePipeline: number;          // Required: excluding stalled deals
  truthGap: number;                   // Required: totalPipeline - closeablePipeline
  stalledDeals: Array<{
    dealName: string;                 // Required
    amount: number;                   // Required
    stage: string;                    // Required
    daysSinceActivity: number;        // Required
    riskLevel: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';  // Enum enforced
  }>;
  topProblems: string[];              // Max 5 items
  recommendations: string[];          // Max 5 items, each max 200 chars
  generatedAt: string;                // ISO 8601 timestamp
}

interface DealDefibContract {
  dealId: string;
  riskScore: number;                  // 0-100
  rootCause: {
    primary: string;                  // Max 100 chars
    secondary?: string;               // Optional, max 100 chars
    evidence: string[];               // Max 3 items
  };
  revivalStrategy: {
    actions: Array<{
      priority: 1 | 2 | 3;
      description: string;            // Max 150 chars
      timeline: string;               // "immediate" | "24h" | "48h" | "next_week"
      owner: 'REP' | 'MANAGER' | 'SE' | 'EXEC';
    }>;
    urgencyLevel: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
    estimatedTimeToRevive: string;    // "2-3 days" format
  };
  nextCheckIn: string;                // ISO 8601 timestamp
}

interface ForecastRealityContract {
  reportedForecast: number;
  actualForecast: number;
  driftAmount: number;
  driftPercentage: number;
  driftTrend: 'INCREASING' | 'STABLE' | 'DECREASING';
  atRiskDeals: Array<{
    dealName: string;
    projectedAmount: number;
    actualProbability: number;        // 0-100
    reason: string;
  }>;
  recommendations: string[];
}

interface QuotaKillSwitchContract {
  repName: string;
  quotaTarget: number;
  currentProgress: number;
  progressPercentage: number;
  onTrack: boolean;
  gapAnalysis: {
    daysRemaining: number;
    requiredDailyClose: number;
    currentDailyAverage: number;
    verdict: 'ON_TRACK' | 'AT_RISK' | 'CRITICAL' | 'UNRECOVERABLE';
  };
  recommendations: string[];
}
```

### Implementation with Zod Validation

```typescript
// validation/schemas.ts
import { z } from 'zod';

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

const DealDefibSchema = z.object({
  dealId: z.string().min(1),
  riskScore: z.number().int().min(0).max(100),
  rootCause: z.object({
    primary: z.string().max(100),
    secondary: z.string().max(100).optional(),
    evidence: z.array(z.string()).max(3)
  }),
  revivalStrategy: z.object({
    actions: z.array(z.object({
      priority: z.union([z.literal(1), z.literal(2), z.literal(3)]),
      description: z.string().max(150),
      timeline: z.enum(['immediate', '24h', '48h', 'next_week']),
      owner: z.enum(['REP', 'MANAGER', 'SE', 'EXEC'])
    })),
    urgencyLevel: z.enum(['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']),
    estimatedTimeToRevive: z.string()
  }),
  nextCheckIn: z.string().datetime()
});

// Export all schemas
export const WeaponSchemas = {
  PipelineTruth: PipelineTruthSchema,
  DealDefib: DealDefibSchema,
  ForecastReality: ForecastRealitySchema,
  QuotaKillSwitch: QuotaKillSwitchSchema
};
```

### Prompting for Contracts

```typescript
// prompts/pipeline-truth-prompt.ts

export function buildPipelineTruthPrompt(csvData: string): string {
  return `You are a VP of Sales analyzing pipeline data. Return ONLY valid JSON matching this exact schema:

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
  "topProblems": ["<string>", ...],  // Max 5
  "recommendations": ["<string>", ...],  // Max 5, each max 200 chars
  "generatedAt": "<ISO 8601 timestamp>"
}

RULES:
1. Return ONLY the JSON object, no prose before or after
2. riskLevel MUST be one of: LOW, MEDIUM, HIGH, CRITICAL
3. A deal is stalled if daysSinceActivity > 30
4. truthGap = totalPipeline - closeablePipeline
5. generatedAt must be current UTC time in ISO 8601 format

CSV DATA:
${csvData}

JSON OUTPUT:`;
}
```

**Key Contract Principles:**
1. ✅ Define schema BEFORE writing prompts
2. ✅ Use TypeScript interfaces + Zod for double validation
3. ✅ Specify enums explicitly (prevents drift: "High" vs "HIGH")
4. ✅ Set max lengths for arrays and strings
5. ✅ Make required vs optional explicit
6. ✅ Include format examples in prompt ("ISO 8601 timestamp")

---

## Pattern 2: Control Loop (Validation & Reliability)

### Definition

The **Control Loop** ensures the software receives data adhering to the contract. Validates → Retries → Repairs → Falls back.

### Pipeline Architecture

```
┌─────────────┐
│   User      │
│   Request   │
└──────┬──────┘
       │
       v
┌─────────────────────────────────────────────────────────┐
│  CONTROL LOOP PIPELINE                                  │
│                                                         │
│  1. INPUT VALIDATION                                   │
│     ├─ Check file size (<10MB)                        │
│     ├─ Validate CSV structure                         │
│     ├─ Injection pattern detection                    │
│     └─ Rate limit check                               │
│         │                                              │
│         v                                              │
│  2. PROMPT TEMPLATE                                    │
│     ├─ Load weapon-specific prompt                    │
│     ├─ Inject CSV data                                │
│     ├─ Add contract specification                     │
│     └─ Add security context                           │
│         │                                              │
│         v                                              │
│  3. CLAUDE API CALL                                    │
│     ├─ Model: claude-sonnet-4-5                       │
│     ├─ Temperature: 0.0 (deterministic)               │
│     ├─ Max tokens: 4096                               │
│     └─ Timeout: 30 seconds                            │
│         │                                              │
│         v                                              │
│  4. RESPONSE VALIDATION ◄────────────┐                │
│     ├─ Parse JSON                    │                │
│     ├─ Validate against Zod schema   │                │
│     ├─ Check all required fields     │                │
│     └─ Validate enum values          │                │
│         │                             │                │
│         ├─ PASS ─────────────────┐   │                │
│         │                         │   │                │
│         └─ FAIL ──────┐           │   │                │
│                       v           │   │                │
│  5. RETRY/REPAIR      │           │   │                │
│     ├─ Extract JSON from prose    │   │                │
│     ├─ Fix common mistakes        │   │                │
│     ├─ Tighten prompt              │   │                │
│     └─ Re-call Claude ─────────────┘   │                │
│         │ (max 2 retries)              │                │
│         │                               │                │
│         └─ STILL FAIL ──┐               │                │
│                         v               │                │
│  6. FALLBACK            │               │                │
│     ├─ Try strict model (opus)         │                │
│     ├─ Or return safe default          │                │
│     └─ Log failure for analysis        │                │
│         │                               │                │
│         └─────────────────────────────┐ │                │
│                                       v v                │
│  7. OUTPUT FILTER                                       │
│     ├─ PII redaction                                   │
│     ├─ Prompt leakage check                            │
│     └─ Response formatting                             │
│         │                                              │
└─────────┴──────────────────────────────────────────────┘
       │
       v
┌──────────────┐
│   Success    │
│   Response   │
└──────────────┘
```

### Implementation Code

```typescript
// services/control-loop.ts

import Anthropic from '@anthropic-ai/sdk';
import { WeaponSchemas } from '../validation/schemas';

interface ControlLoopConfig {
  maxRetries: number;
  timeout: number;
  fallbackModel?: string;
  enableRepair: boolean;
}

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

export class WeaponControlLoop {
  private client: Anthropic;
  private config: ControlLoopConfig;

  constructor(apiKey: string, config: Partial<ControlLoopConfig> = {}) {
    this.client = new Anthropic({ apiKey });
    this.config = {
      maxRetries: config.maxRetries || 2,
      timeout: config.timeout || 30000,
      fallbackModel: config.fallbackModel || 'claude-opus-4',
      enableRepair: config.enableRepair ?? true
    };
  }

  /**
   * Execute weapon with full control loop
   */
  async execute<T>(
    weaponName: string,
    prompt: string,
    schema: any,
    options: {
      temperature?: number;
      maxTokens?: number;
    } = {}
  ): Promise<ControlLoopResult<T>> {
    const startTime = Date.now();
    let attempts = 0;
    let totalTokens = 0;
    let lastError = '';

    // STEP 1: Primary attempt
    for (let i = 0; i <= this.config.maxRetries; i++) {
      attempts++;

      try {
        const response = await this.callClaude(prompt, {
          model: 'claude-sonnet-4-5',
          temperature: options.temperature || 0.0,
          maxTokens: options.maxTokens || 4096
        });

        totalTokens += response.usage.input_tokens + response.usage.output_tokens;

        // STEP 2: Validate response
        const parseResult = this.parseAndValidate(
          response.content[0].text,
          schema
        );

        if (parseResult.success) {
          // SUCCESS PATH
          return {
            success: true,
            data: parseResult.data,
            metadata: {
              attempts,
              totalTime: Date.now() - startTime,
              tokensUsed: totalTokens,
              cost: this.calculateCost(totalTokens, 'claude-sonnet-4-5')
            }
          };
        }

        lastError = parseResult.error;

        // STEP 3: Repair attempt (if enabled and not last retry)
        if (this.config.enableRepair && i < this.config.maxRetries) {
          const repairResult = this.attemptRepair(
            response.content[0].text,
            schema
          );

          if (repairResult.success) {
            return {
              success: true,
              data: repairResult.data,
              metadata: {
                attempts,
                totalTime: Date.now() - startTime,
                tokensUsed: totalTokens,
                cost: this.calculateCost(totalTokens, 'claude-sonnet-4-5')
              }
            };
          }

          // STEP 4: Tighten prompt for retry
          prompt = this.tightenPrompt(prompt, lastError);
        }

      } catch (error) {
        lastError = error.message;

        // Rate limit error - don't retry
        if (error.status === 429) {
          return {
            success: false,
            error: 'RATE_LIMIT_EXCEEDED',
            metadata: {
              attempts,
              totalTime: Date.now() - startTime,
              tokensUsed: totalTokens,
              cost: this.calculateCost(totalTokens, 'claude-sonnet-4-5')
            }
          };
        }

        // Context length error - return immediately
        if (error.message.includes('prompt is too long')) {
          return {
            success: false,
            error: 'CONTEXT_LENGTH_EXCEEDED',
            metadata: {
              attempts,
              totalTime: Date.now() - startTime,
              tokensUsed: totalTokens,
              cost: this.calculateCost(totalTokens, 'claude-sonnet-4-5')
            }
          };
        }
      }
    }

    // STEP 5: Fallback to stricter model
    if (this.config.fallbackModel) {
      try {
        const response = await this.callClaude(prompt, {
          model: this.config.fallbackModel,
          temperature: 0.0,
          maxTokens: options.maxTokens || 4096
        });

        totalTokens += response.usage.input_tokens + response.usage.output_tokens;
        const parseResult = this.parseAndValidate(
          response.content[0].text,
          schema
        );

        if (parseResult.success) {
          return {
            success: true,
            data: parseResult.data,
            metadata: {
              attempts: attempts + 1,
              totalTime: Date.now() - startTime,
              tokensUsed: totalTokens,
              cost: this.calculateCost(totalTokens, this.config.fallbackModel)
            }
          };
        }
      } catch (error) {
        lastError = `Fallback failed: ${error.message}`;
      }
    }

    // FINAL FAILURE
    return {
      success: false,
      error: lastError,
      metadata: {
        attempts,
        totalTime: Date.now() - startTime,
        tokensUsed: totalTokens,
        cost: this.calculateCost(totalTokens, 'claude-sonnet-4-5')
      }
    };
  }

  /**
   * Call Claude API with timeout
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
    const timeoutId = setTimeout(() => controller.abort(), this.config.timeout);

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
  private parseAndValidate(responseText: string, schema: any) {
    try {
      // Try parsing as JSON
      const jsonMatch = responseText.match(/\{[\s\S]*\}/);
      if (!jsonMatch) {
        return { success: false, error: 'No JSON object found in response' };
      }

      const parsed = JSON.parse(jsonMatch[0]);
      const validated = schema.parse(parsed);

      return { success: true, data: validated };
    } catch (error) {
      return { success: false, error: error.message };
    }
  }

  /**
   * Attempt to repair malformed response
   */
  private attemptRepair(responseText: string, schema: any) {
    // Strategy 1: Strip prose before/after JSON
    let cleaned = responseText.trim();

    // Remove common prose patterns
    cleaned = cleaned.replace(/^(Sure|Here|Okay|Here's)[^{]*/, '');
    cleaned = cleaned.replace(/```json\s*/, '');
    cleaned = cleaned.replace(/```\s*$/, '');

    // Strategy 2: Extract JSON object
    const jsonMatch = cleaned.match(/\{[\s\S]*\}/);
    if (!jsonMatch) {
      return { success: false, error: 'Could not extract JSON' };
    }

    try {
      const parsed = JSON.parse(jsonMatch[0]);

      // Strategy 3: Fix common key mistakes
      const repaired = this.repairCommonMistakes(parsed);

      // Validate repaired object
      const validated = schema.parse(repaired);
      return { success: true, data: validated };
    } catch (error) {
      return { success: false, error: `Repair failed: ${error.message}` };
    }
  }

  /**
   * Fix common key naming mistakes
   */
  private repairCommonMistakes(obj: any): any {
    const repairs = {
      // Common variations
      'total_pipeline': 'totalPipeline',
      'closeable_pipeline': 'closeablePipeline',
      'truth_gap': 'truthGap',
      'stalled_deals': 'stalledDeals',
      'top_problems': 'topProblems',
      'risk_level': 'riskLevel',
      'days_since_activity': 'daysSinceActivity',
      // More repairs...
    };

    const repaired = { ...obj };

    for (const [wrong, correct] of Object.entries(repairs)) {
      if (wrong in repaired && !(correct in repaired)) {
        repaired[correct] = repaired[wrong];
        delete repaired[wrong];
      }
    }

    return repaired;
  }

  /**
   * Tighten prompt after validation failure
   */
  private tightenPrompt(originalPrompt: string, error: string): string {
    let tightened = originalPrompt;

    // Add emphasis based on error
    if (error.includes('enum')) {
      tightened += '\n\nCRITICAL: Use EXACT enum values as specified (case-sensitive).';
    }

    if (error.includes('required')) {
      tightened += '\n\nCRITICAL: All fields marked required MUST be present.';
    }

    if (error.includes('JSON')) {
      tightened = 'RETURN ONLY VALID JSON. NO PROSE. START WITH { AND END WITH }.\n\n' + tightened;
    }

    return tightened;
  }

  /**
   * Calculate API cost
   */
  private calculateCost(tokens: number, model: string): number {
    const pricing = {
      'claude-sonnet-4-5': { input: 0.003, output: 0.015 },  // per 1K tokens
      'claude-opus-4': { input: 0.015, output: 0.075 }
    };

    // Simplified: assume 50/50 input/output split
    const rate = pricing[model] || pricing['claude-sonnet-4-5'];
    return ((tokens / 2) * rate.input + (tokens / 2) * rate.output) / 1000;
  }
}
```

### Usage Example

```typescript
// Example: Pipeline Truth Detector with Control Loop

import { WeaponControlLoop } from './services/control-loop';
import { WeaponSchemas } from './validation/schemas';
import { buildPipelineTruthPrompt } from './prompts/pipeline-truth-prompt';

async function analyzePipeline(csvData: string) {
  const controlLoop = new WeaponControlLoop(process.env.ANTHROPIC_API_KEY, {
    maxRetries: 2,
    timeout: 30000,
    fallbackModel: 'claude-opus-4',
    enableRepair: true
  });

  const prompt = buildPipelineTruthPrompt(csvData);

  const result = await controlLoop.execute(
    'pipeline-truth',
    prompt,
    WeaponSchemas.PipelineTruth
  );

  if (result.success) {
    console.log('✅ Analysis complete:', result.data);
    console.log(`⚡ ${result.metadata.attempts} attempts, ${result.metadata.totalTime}ms, $${result.metadata.cost.toFixed(4)}`);
    return result.data;
  } else {
    console.error('❌ Analysis failed:', result.error);
    console.log(`Metadata:`, result.metadata);
    throw new Error(result.error);
  }
}
```

**Key Control Loop Principles:**
1. ✅ Always validate against schema
2. ✅ Attempt repair before giving up (extract JSON, fix keys)
3. ✅ Tighten prompt on retry (add emphasis based on error)
4. ✅ Fallback to stricter model (Opus if Sonnet fails)
5. ✅ Set timeouts (prevent hanging)
6. ✅ Track metadata (attempts, time, cost)
7. ✅ Fail gracefully (return error, not exception)

---

## Pattern 3: Observability (Tracing & Improvement)

### Definition

**Observability** means tracing every LLM call to see exactly which prompts produced what outputs. This enables continuous improvement and prevents regressions.

### What to Trace

```typescript
interface WeaponTrace {
  // Request Context
  traceId: string;                    // Unique ID for this request
  userId: string;
  weaponName: string;
  tier: 'FREE' | 'PAID_BASIC' | 'PAID_PREMIUM';
  timestamp: string;

  // Input
  input: {
    csvSize: number;                  // bytes
    rowCount: number;
    prompt: string;                   // Full prompt sent
    promptTokens: number;
  };

  // LLM Call(s)
  attempts: Array<{
    attemptNumber: number;
    model: string;
    temperature: number;
    maxTokens: number;
    startTime: string;
    endTime: string;
    durationMs: number;
    inputTokens: number;
    outputTokens: number;
    cost: number;
    rawResponse: string;              // What Claude returned
    validationResult: {
      passed: boolean;
      errors?: string[];
    };
  }>;

  // Final Result
  result: {
    success: boolean;
    data?: any;                       // Final validated output
    error?: string;
    totalAttempts: number;
    totalDurationMs: number;
    totalTokens: number;
    totalCost: number;
  };

  // User Feedback (collected later)
  feedback?: {
    useful: boolean;
    rating: 1 | 2 | 3 | 4 | 5;
    comment?: string;
    submittedAt: string;
  };

  // Business Outcome (tracked later)
  outcome?: {
    recommendationsActedOn: number;   // How many of our recommendations did they use?
    dealsConverted: number;           // Did stalled deals get revived?
    revenueImpact: number;            // $ value of deals that converted
    trackedAt: string;
  };
}
```

### Implementation: Tracing System

```typescript
// services/tracing.ts

import { v4 as uuidv4 } from 'uuid';

export class WeaponTracer {
  private traces: Map<string, WeaponTrace> = new Map();

  /**
   * Start a new trace
   */
  startTrace(weaponName: string, userId: string, tier: string, input: any): string {
    const traceId = uuidv4();

    const trace: WeaponTrace = {
      traceId,
      userId,
      weaponName,
      tier,
      timestamp: new Date().toISOString(),
      input: {
        csvSize: input.csvData?.length || 0,
        rowCount: input.rowCount || 0,
        prompt: '',  // Set when prompt is built
        promptTokens: 0
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
    return traceId;
  }

  /**
   * Record an LLM attempt
   */
  recordAttempt(traceId: string, attempt: {
    attemptNumber: number;
    model: string;
    temperature: number;
    maxTokens: number;
    startTime: Date;
    endTime: Date;
    inputTokens: number;
    outputTokens: number;
    cost: number;
    rawResponse: string;
    validationResult: { passed: boolean; errors?: string[] };
  }) {
    const trace = this.traces.get(traceId);
    if (!trace) return;

    trace.attempts.push({
      ...attempt,
      startTime: attempt.startTime.toISOString(),
      endTime: attempt.endTime.toISOString(),
      durationMs: attempt.endTime.getTime() - attempt.startTime.getTime()
    });
  }

  /**
   * Finalize trace
   */
  finalizeTrace(traceId: string, result: {
    success: boolean;
    data?: any;
    error?: string;
  }) {
    const trace = this.traces.get(traceId);
    if (!trace) return;

    trace.result = {
      ...result,
      totalAttempts: trace.attempts.length,
      totalDurationMs: trace.attempts.reduce((sum, a) => sum + a.durationMs, 0),
      totalTokens: trace.attempts.reduce((sum, a) => sum + a.inputTokens + a.outputTokens, 0),
      totalCost: trace.attempts.reduce((sum, a) => sum + a.cost, 0)
    };

    // Persist to database/logging service
    this.persist(trace);
  }

  /**
   * Add user feedback
   */
  addFeedback(traceId: string, feedback: {
    useful: boolean;
    rating: 1 | 2 | 3 | 4 | 5;
    comment?: string;
  }) {
    const trace = this.traces.get(traceId);
    if (!trace) return;

    trace.feedback = {
      ...feedback,
      submittedAt: new Date().toISOString()
    };

    this.persist(trace);
  }

  /**
   * Track business outcome (24 hours later)
   */
  addOutcome(traceId: string, outcome: {
    recommendationsActedOn: number;
    dealsConverted: number;
    revenueImpact: number;
  }) {
    const trace = this.traces.get(traceId);
    if (!trace) return;

    trace.outcome = {
      ...outcome,
      trackedAt: new Date().toISOString()
    };

    this.persist(trace);
  }

  /**
   * Persist trace to storage
   */
  private async persist(trace: WeaponTrace) {
    // Option 1: PostgreSQL
    // await db.traces.upsert(trace);

    // Option 2: CloudWatch Logs (structured JSON)
    // console.log(JSON.stringify({ type: 'WEAPON_TRACE', ...trace }));

    // Option 3: Dedicated observability platform
    // await honeycomb.send(trace);

    // For now: console log
    console.log('[TRACE]', JSON.stringify(trace, null, 2));
  }

  /**
   * Get trace by ID
   */
  getTrace(traceId: string): WeaponTrace | undefined {
    return this.traces.get(traceId);
  }
}
```

### Integration with Control Loop

```typescript
// services/weapon-service.ts

import { WeaponControlLoop } from './control-loop';
import { WeaponTracer } from './tracing';

export class WeaponService {
  private controlLoop: WeaponControlLoop;
  private tracer: WeaponTracer;

  constructor(apiKey: string) {
    this.controlLoop = new WeaponControlLoop(apiKey);
    this.tracer = new WeaponTracer();
  }

  async executePipelineTruth(userId: string, tier: string, csvData: string) {
    // Start trace
    const traceId = this.tracer.startTrace('pipeline-truth', userId, tier, {
      csvData,
      rowCount: csvData.split('\n').length
    });

    // Build prompt
    const prompt = buildPipelineTruthPrompt(csvData);

    // Execute with control loop (modified to support tracing)
    const result = await this.controlLoop.executeWithTracing(
      'pipeline-truth',
      prompt,
      WeaponSchemas.PipelineTruth,
      traceId,
      this.tracer
    );

    // Finalize trace
    this.tracer.finalizeTrace(traceId, {
      success: result.success,
      data: result.data,
      error: result.error
    });

    // Return result with trace ID
    return {
      ...result,
      traceId  // Frontend can use this to submit feedback
    };
  }

  async submitFeedback(traceId: string, feedback: any) {
    this.tracer.addFeedback(traceId, feedback);
  }
}
```

### Observability Dashboard (Concept)

```typescript
// analytics/weapon-analytics.ts

interface WeaponMetrics {
  totalRequests: number;
  successRate: number;
  avgDurationMs: number;
  avgCost: number;
  avgTokensUsed: number;

  byWeapon: {
    [weaponName: string]: {
      requests: number;
      successRate: number;
      avgDurationMs: number;
      avgCost: number;
    };
  };

  byTier: {
    FREE: { requests: number; successRate: number; };
    PAID_BASIC: { requests: number; successRate: number; };
    PAID_PREMIUM: { requests: number; successRate: number; };
  };

  validationFailures: {
    schemaErrors: number;
    jsonParseErrors: number;
    enumViolations: number;
  };

  retryStatistics: {
    firstAttemptSuccess: number;
    succeededAfterRetry: number;
    succeededAfterFallback: number;
    totalFailures: number;
  };

  userSatisfaction: {
    avgRating: number;
    usefulPercentage: number;
    totalFeedback: number;
  };

  businessImpact: {
    totalDealsRevived: number;
    totalRevenueImpact: number;
    avgRecommendationsActedOn: number;
  };
}

export class WeaponAnalytics {
  async getMetrics(timeRange: { start: Date; end: Date }): Promise<WeaponMetrics> {
    // Query traces from database
    // Calculate metrics
    // Return dashboard data
  }

  async detectRegressions(): Promise<Array<{ metric: string; change: number; alert: string }>> {
    // Compare last 7 days to previous 7 days
    // Flag significant drops in success rate, user satisfaction, etc.
  }

  async identifyImprovementOpportunities(): Promise<string[]> {
    // Analyze failed traces
    // Find common error patterns
    // Suggest prompt improvements
  }
}
```

**Key Observability Principles:**
1. ✅ Trace every request end-to-end
2. ✅ Record raw prompts and responses
3. ✅ Track validation failures (learn from errors)
4. ✅ Collect user feedback (thumbs up/down)
5. ✅ Track business outcomes (did recommendations work?)
6. ✅ Build dashboards (spot regressions quickly)
7. ✅ Alert on anomalies (success rate drops)

---

## Implementation for Circuit OS Weapons

### Weapon #1: Pipeline Truth Detector

**Contract:**
```typescript
PipelineTruthContract (defined above)
```

**Control Loop:**
- Validate CSV structure first
- Call Claude with strict JSON prompt
- Validate against PipelineTruthSchema
- Retry with tightened prompt if needed
- Fallback to Opus if Sonnet fails
- Return validated data + trace ID

**Observability:**
- Track: CSV size, row count, stalled deals found, recommendations given
- Collect feedback: "Was this analysis helpful?"
- Measure outcome: Did user export results? Did they take action?

**Implementation Status:** ⚠️ Frontend complete, backend needed

---

### Weapon #2: Deal Defibrillator

**Contract:**
```typescript
DealDefibContract (defined above)
```

**Control Loop:**
- Validate deal data (deal ID, amount, stage, etc.)
- Call Claude with revival strategy prompt
- Validate against DealDefibSchema
- Ensure urgency level matches risk score (consistency check)
- Retry if actions are too vague ("elaborate on action steps")
- Return validated strategy + trace ID

**Observability:**
- Track: Risk scores assigned, urgency levels, revival strategies generated
- Collect feedback: "Did this strategy work?"
- Measure outcome: Track deal over 30 days - did it convert?

**Implementation Status:** ⚠️ UI designed, full implementation needed

---

### Weapon #3: Forecast Reality Check

**Contract:**
```typescript
ForecastRealityContract (defined above)
```

**Control Loop:**
- Validate CRM data connection
- Call Claude with forecast analysis prompt
- Validate against ForecastRealitySchema
- Cross-check: driftAmount = reportedForecast - actualForecast
- Retry if calculations inconsistent
- Return validated analysis + trace ID

**Observability:**
- Track: Drift percentages, at-risk deals identified
- Collect feedback: "Was the forecast accurate?"
- Measure outcome: Compare predicted vs actual quarter-end results

**Implementation Status:** ⚠️ Not started

---

### Weapon #4: Quota Kill Switch

**Contract:**
```typescript
QuotaKillSwitchContract (defined above)
```

**Control Loop:**
- Validate rep performance data
- Call Claude with quota gap analysis prompt
- Validate against QuotaKillSwitchSchema
- Cross-check: verdict matches gap calculation
- Retry if math is wrong
- Return validated analysis + trace ID

**Observability:**
- Track: Verdicts assigned (ON_TRACK, AT_RISK, etc.), recommendations given
- Collect feedback: "Was this assessment accurate?"
- Measure outcome: Did rep hit quota? Were recommendations followed?

**Implementation Status:** ⚠️ Not started

---

## Tools: LangChain vs PDL vs Custom

### Option 1: LangChain (Code-First)

**Pros:**
- Battle-tested framework
- Composable runnables
- Built-in retry/fallback logic
- Active community
- TypeScript support

**Cons:**
- Heavy dependency (~500KB)
- Learning curve
- Opinionated architecture

**Best for:** Complex multi-step workflows, RAG systems, agent frameworks

### Option 2: PDL (Spec-First)

**Pros:**
- Declarative YAML specification
- Type enforcement built-in
- Explicit control (conditionals, loops)
- Centralized prompt/contract/loop definition

**Cons:**
- Less mature ecosystem
- Requires PDL interpreter
- Limited flexibility for dynamic prompts

**Best for:** Standardized workflows, teams preferring declarative config

### Option 3: Custom (Circuit OS Approach)

**Pros:**
- ✅ Zero dependencies (just Zod + Anthropic SDK)
- ✅ Full control over implementation
- ✅ Lightweight (~200 lines of code)
- ✅ Easy to debug
- ✅ Tailored to Circuit OS weapons

**Cons:**
- Must build retry/repair logic ourselves
- Must maintain tracing ourselves
- No community support

**Recommendation for Circuit OS: Custom Implementation**

**Reasoning:**
1. Circuit OS weapons are **simple, single-step LLM calls** (not complex agent workflows)
2. We value **control and simplicity** over framework features
3. Our codebase is **already lightweight** (no need to add 500KB dependency)
4. We have **specific requirements** (tier-based rate limiting, injection detection) not covered by frameworks
5. The custom implementation above is **<500 lines total** and does everything we need

**If we later need:** Multi-step workflows, RAG, or agent systems → consider LangChain

---

## Migration Path

### Phase 1: Add Contracts (Week 1-2)

**Tasks:**
1. ✅ Create `contracts/weapon-contracts.ts` with all 4 weapon interfaces
2. ✅ Create `validation/schemas.ts` with Zod schemas
3. ✅ Update prompts to specify exact output format
4. ✅ Test validation locally

**Deliverables:**
- TypeScript contracts for all weapons
- Zod schemas with 100% coverage
- Updated prompt templates

### Phase 2: Implement Control Loop (Week 2-3)

**Tasks:**
1. ✅ Create `services/control-loop.ts` with WeaponControlLoop class
2. ✅ Implement validation pipeline
3. ✅ Add retry/repair logic
4. ✅ Add fallback model support
5. ✅ Test with real Claude API calls

**Deliverables:**
- Fully functional control loop
- Unit tests (validate, repair, retry logic)
- Integration tests (end-to-end weapon execution)

### Phase 3: Add Observability (Week 3-4)

**Tasks:**
1. ✅ Create `services/tracing.ts` with WeaponTracer class
2. ✅ Integrate tracing with control loop
3. ✅ Add feedback collection endpoint
4. ✅ Add outcome tracking system
5. ✅ Set up logging/monitoring (CloudWatch or similar)

**Deliverables:**
- Trace collection system
- Feedback UI components
- Outcome tracking cron job (24-hour follow-up)

### Phase 4: Dashboard & Analytics (Week 4-6)

**Tasks:**
1. ✅ Create analytics queries
2. ✅ Build observability dashboard
3. ✅ Set up regression alerts
4. ✅ Create prompt improvement workflow

**Deliverables:**
- Admin dashboard showing weapon metrics
- Regression detection system
- Prompt optimization workflow

### Phase 5: Continuous Improvement (Ongoing)

**Tasks:**
1. ✅ Review traces weekly
2. ✅ Identify failed validations
3. ✅ Improve prompts based on errors
4. ✅ Track business outcomes
5. ✅ Refine contracts based on user feedback

**Deliverables:**
- Monthly improvement reports
- Prompt version history
- Success rate trending graphs

---

## Success Metrics

### Technical Metrics

| Metric | Baseline (Current) | Target (3 months) |
|--------|-------------------|-------------------|
| First-attempt success rate | Unknown | >90% |
| Average retries per request | Unknown | <0.2 |
| Validation error rate | Unknown | <5% |
| Response time (p95) | Unknown | <5 seconds |
| Fallback usage rate | N/A | <1% |

### Business Metrics

| Metric | Baseline | Target (3 months) |
|--------|----------|-------------------|
| User satisfaction (thumbs up) | Unknown | >85% |
| Average rating | Unknown | >4.0 / 5.0 |
| Recommendations acted on | Unknown | >60% |
| Deals revived | 0 | 100+ |
| Revenue impact | $0 | $1M+ |

### Cost Metrics

| Metric | Target |
|--------|--------|
| Average cost per weapon execution | <$0.05 |
| Monthly API spend (1000 users) | <$5,000 |
| Cost per successful outcome | <$1.00 |

### Reliability Metrics

| Metric | Target |
|--------|--------|
| Uptime | >99.5% |
| Error rate | <0.5% |
| Time to recovery (incidents) | <15 minutes |

---

## Conclusion

By applying **Contract, Control Loop, and Observability** patterns to Circuit OS weapons, we transform probabilistic LLM calls into production-ready software components.

**Before:** "Claude, analyze this pipeline" → unpredictable prose
**After:** Strict JSON schema → validated → retried if needed → traced → continuously improved

**The result:** Circuit OS weapons become reliable, measurable, and continuously improving—ready for paying customers.

---

## Next Steps

1. **Review this document** with engineering team
2. **Approve migration plan** (Phases 1-5)
3. **Begin Phase 1** (Add contracts to all 4 weapons)
4. **Track progress** using success metrics above

**Estimated timeline:** 6-8 weeks to full production readiness
**Estimated effort:** 1-2 engineers full-time

---

## References

- YouTube Video: "Advanced Prompt Engineering" (source material)
- Claude API Documentation: https://docs.anthropic.com/claude/reference
- Zod Documentation: https://zod.dev/
- LangChain Documentation: https://js.langchain.com/
- PDL Specification: (PDL official site)

---

**Document Owner:** Circuit OS Engineering Team
**Last Updated:** 2025-11-11
**Version:** 1.0
