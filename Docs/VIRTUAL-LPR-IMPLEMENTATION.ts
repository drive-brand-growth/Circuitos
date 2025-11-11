/**
 * VIRTUAL LPR CIRCUIT™ - PRODUCTION IMPLEMENTATION
 *
 * Applies Contract + Control Loop + Observability patterns to patent-pending Virtual LPR system
 *
 * Classification: HIGHLY CONFIDENTIAL - TRADE SECRET
 * Version: 2.0.0
 * Date: 2025-11-11
 *
 * © 2025 CircuitOS™ - ALL RIGHTS RESERVED
 */

import Anthropic from '@anthropic-ai/sdk';
import { z } from 'zod';
import { v4 as uuidv4 } from 'uuid';

// ============================================================================
// CONTRACTS: DMN Protocol + Virtual LPR Schemas
// ============================================================================

/**
 * Virtual LPR Scoring Output Schema (TRADE SECRET)
 */
const VirtualLPROutputSchema = z.object({
  lprScore: z.number().int().min(0).max(100),
  tier: z.union([z.literal(1), z.literal(2), z.literal(3), z.literal(4)]),
  tierLabel: z.enum(['IMMEDIATE_VISIT', 'HIGH_INTENT', 'MODERATE', 'AWARENESS']),
  breakdown: z.object({
    physicalIntent: z.object({
      score: z.number().int().min(0).max(100),
      weight: z.number().min(0.35).max(0.45),  // TRADE SECRET range
      contribution: z.number()
    }),
    behavioral: z.object({
      score: z.number().int().min(0).max(100),
      weight: z.number().min(0.25).max(0.30),  // TRADE SECRET range
      contribution: z.number()
    }),
    temporal: z.object({
      score: z.number().int().min(0).max(100),
      weight: z.number().min(0.15).max(0.20),  // TRADE SECRET range
      contribution: z.number()
    }),
    competitive: z.object({
      score: z.number().int().min(0).max(100),
      weight: z.number().min(0.10).max(0.15),  // TRADE SECRET range
      contribution: z.number()
    })
  }),
  confidence: z.number().int().min(0).max(100),
  recommendedAction: z.object({
    action: z.enum(['CALL_NOW', 'PRIORITY_FOLLOWUP', 'NURTURE', 'EDUCATIONAL_CONTENT']),
    timing: z.string().datetime(),
    channel: z.string(),
    message: z.string().max(200)
  }),
  predictionExpiry: z.string().datetime(),
  generatedAt: z.string().datetime()
});

/**
 * Lead Router Agent Output Schema
 */
const LeadRouterOutputSchema = z.object({
  routingDecision: z.enum(['IMMEDIATE_OUTREACH', 'SCHEDULED_FOLLOWUP', 'NURTURE_CAMPAIGN', 'DISQUALIFY']),
  priority: z.union([z.literal(1), z.literal(2), z.literal(3), z.literal(4), z.literal(5)]),
  assignedChannel: z.enum(['SMS', 'EMAIL', 'CALL', 'RETARGETING_AD']),
  timing: z.object({
    optimal: z.string().datetime(),
    reason: z.string().max(200)
  }),
  competitiveIntelligence: z.object({
    competitorThreat: z.enum(['LOW', 'MEDIUM', 'HIGH']),
    recommendedDifferentiator: z.string().max(200),
    urgencyBoost: z.number().int().min(0).max(50)
  }),
  personalizedMessage: z.object({
    hook: z.string().max(150),
    offer: z.string().max(150),
    cta: z.string().max(100)
  }),
  expectedConversionProbability: z.number().int().min(0).max(100),
  generatedAt: z.string().datetime()
});

/**
 * Virtual Traffic Camera Output Schema (PATENT-PENDING)
 */
const VirtualTrafficCameraOutputSchema = z.object({
  estimatedFootfall: z.object({
    dailyPassersby: z.number().int().nonnegative(),
    hourlyBreakdown: z.array(z.object({
      hour: z.number().int().min(0).max(23),
      traffic: z.number().int().nonnegative(),
      confidence: z.number().int().min(0).max(100)
    })),
    peakHours: z.array(z.object({
      hour: z.number().int().min(0).max(23),
      traffic: z.number().int().nonnegative()
    })).max(5)
  }),
  qualifiedProspects: z.object({
    total: z.number().int().nonnegative(),
    byTier: z.object({
      tier1: z.number().int().nonnegative(),
      tier2: z.number().int().nonnegative(),
      tier3: z.number().int().nonnegative(),
      tier4: z.number().int().nonnegative()
    })
  }),
  top10Prospects: z.array(z.object({
    anonymousId: z.string(),
    profile: z.object({
      age: z.string().optional(),
      gender: z.string().optional(),
      interests: z.array(z.string()),
      incomeRange: z.string().optional()
    }),
    lprScore: z.number().int().min(0).max(100),
    location: z.object({
      distance: z.number().nonnegative(),
      frequencyInArea: z.number().int().nonnegative()
    }),
    intent: z.object({
      searchQuery: z.string().optional(),
      gmbAction: z.string().optional(),
      confidence: z.number().int().min(0).max(100)
    }),
    lifeEvent: z.string().optional(),
    enrichedData: z.object({
      email: z.string().optional(),
      phone: z.string().optional(),
      demographicMatch: z.number().int().min(0).max(100)
    }),
    suggestedOutreach: z.string().max(200)
  })).max(10),
  competitiveIntelligence: z.object({
    localSaturation: z.number().int().min(0).max(100),
    marketOpportunity: z.number().int().min(0).max(100),
    bestTimeToTarget: z.array(z.string()).max(5)
  }),
  dataQuality: z.object({
    completeness: z.number().int().min(0).max(100),
    freshness: z.string().datetime(),
    sources: z.array(z.string())
  }),
  generatedAt: z.string().datetime()
});

// TypeScript interfaces (derived from schemas)
type VirtualLPROutput = z.infer<typeof VirtualLPROutputSchema>;
type LeadRouterOutput = z.infer<typeof LeadRouterOutputSchema>;
type VirtualTrafficCameraOutput = z.infer<typeof VirtualTrafficCameraOutputSchema>;

// ============================================================================
// CONTROL LOOP: DMN Agent Execution with Validation
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

class VirtualLPRControlLoop {
  private client: Anthropic;
  private maxRetries: number = 2;
  private timeout: number = 30000;

  constructor(apiKey: string) {
    this.client = new Anthropic({ apiKey });
  }

  /**
   * Execute Virtual LPR scoring with validation and retry
   */
  async calculateLPRScore(
    leadData: any,
    businessContext: any,
    tracer?: VirtualLPRObservability,
    traceId?: string
  ): Promise<ControlLoopResult<VirtualLPROutput>> {
    const startTime = Date.now();
    let attempts = 0;
    let totalTokens = 0;
    let lastError = '';

    // Build LPR scoring prompt (PROPRIETARY)
    let prompt = this.buildLPRPrompt(leadData, businessContext);

    for (let i = 0; i <= this.maxRetries; i++) {
      attempts++;

      try {
        console.log(`[LPR] Attempt ${attempts}/${this.maxRetries + 1}`);

        const response = await this.callClaude(prompt, {
          model: 'claude-sonnet-4-5',
          temperature: 0.0,
          maxTokens: 4096
        });

        totalTokens += response.usage.input_tokens + response.usage.output_tokens;

        // Parse and validate
        const parseResult = this.parseAndValidate(
          response.content[0].text,
          VirtualLPROutputSchema
        );

        if (parseResult.success) {
          // Additional business rule validation
          const businessRuleCheck = this.validateLPRBusinessRules(parseResult.data);

          if (businessRuleCheck.passed) {
            console.log(`[LPR] ✅ Valid LPR score: ${parseResult.data.lprScore} (Tier ${parseResult.data.tier})`);

            return {
              success: true,
              data: parseResult.data,
              metadata: {
                attempts,
                totalTime: Date.now() - startTime,
                tokensUsed: totalTokens,
                cost: this.calculateCost(totalTokens)
              }
            };
          } else {
            lastError = `Business rule violation: ${businessRuleCheck.errors.join(', ')}`;
            console.log(`[LPR] ❌ Business rule failed: ${lastError}`);
            prompt = this.tightenPrompt(prompt, lastError);
          }
        } else {
          lastError = parseResult.error;
          console.log(`[LPR] ❌ Validation failed: ${lastError}`);
          prompt = this.tightenPrompt(prompt, lastError);
        }

      } catch (error: any) {
        lastError = error.message;
        console.error(`[LPR] ❌ Error: ${error.message}`);
      }
    }

    // All retries failed
    return {
      success: false,
      error: lastError,
      metadata: {
        attempts,
        totalTime: Date.now() - startTime,
        tokensUsed: totalTokens,
        cost: this.calculateCost(totalTokens)
      }
    };
  }

  /**
   * Execute Lead Router agent
   */
  async routeLead(
    lprScore: number,
    leadData: any,
    businessContext: any
  ): Promise<ControlLoopResult<LeadRouterOutput>> {
    const startTime = Date.now();
    let attempts = 0;
    let totalTokens = 0;
    let lastError = '';

    let prompt = this.buildLeadRouterPrompt(lprScore, leadData, businessContext);

    for (let i = 0; i <= this.maxRetries; i++) {
      attempts++;

      try {
        const response = await this.callClaude(prompt, {
          model: 'claude-sonnet-4-5',
          temperature: 0.0,
          maxTokens: 4096
        });

        totalTokens += response.usage.input_tokens + response.usage.output_tokens;

        const parseResult = this.parseAndValidate(
          response.content[0].text,
          LeadRouterOutputSchema
        );

        if (parseResult.success) {
          const businessRuleCheck = this.validateLeadRouterBusinessRules(
            parseResult.data,
            lprScore
          );

          if (businessRuleCheck.passed) {
            return {
              success: true,
              data: parseResult.data,
              metadata: {
                attempts,
                totalTime: Date.now() - startTime,
                tokensUsed: totalTokens,
                cost: this.calculateCost(totalTokens)
              }
            };
          } else {
            lastError = `Business rule violation: ${businessRuleCheck.errors.join(', ')}`;
            prompt = this.tightenPrompt(prompt, lastError);
          }
        } else {
          lastError = parseResult.error;
          prompt = this.tightenPrompt(prompt, lastError);
        }

      } catch (error: any) {
        lastError = error.message;
      }
    }

    return {
      success: false,
      error: lastError,
      metadata: {
        attempts,
        totalTime: Date.now() - startTime,
        tokensUsed: totalTokens,
        cost: this.calculateCost(totalTokens)
      }
    };
  }

  /**
   * Validate LPR business rules (TRADE SECRET)
   */
  private validateLPRBusinessRules(output: VirtualLPROutput) {
    const errors: string[] = [];

    // Rule 1: Weights must sum to 1.0
    const weights = output.breakdown;
    const totalWeight =
      weights.physicalIntent.weight +
      weights.behavioral.weight +
      weights.temporal.weight +
      weights.competitive.weight;

    if (Math.abs(totalWeight - 1.0) > 0.01) {
      errors.push(`Weights must sum to 1.0, got ${totalWeight.toFixed(3)}`);
    }

    // Rule 2: Tier must match score ranges
    if (output.lprScore >= 90 && output.tier !== 1) {
      errors.push('Score 90-100 must be Tier 1');
    } else if (output.lprScore >= 70 && output.lprScore < 90 && output.tier !== 2) {
      errors.push('Score 70-89 must be Tier 2');
    } else if (output.lprScore >= 45 && output.lprScore < 70 && output.tier !== 3) {
      errors.push('Score 45-69 must be Tier 3');
    } else if (output.lprScore < 45 && output.tier !== 4) {
      errors.push('Score 0-44 must be Tier 4');
    }

    // Rule 3: Tier label must match tier number
    const expectedLabels: Record<number, string> = {
      1: 'IMMEDIATE_VISIT',
      2: 'HIGH_INTENT',
      3: 'MODERATE',
      4: 'AWARENESS'
    };

    if (output.tierLabel !== expectedLabels[output.tier]) {
      errors.push(`Tier ${output.tier} must have label ${expectedLabels[output.tier]}`);
    }

    // Rule 4: Recommended action must match tier
    if (output.tier === 1 && output.recommendedAction.action !== 'CALL_NOW') {
      errors.push('Tier 1 must recommend CALL_NOW');
    }

    // Rule 5: Confidence must be reasonable given data quality
    // (This would check against input data completeness in production)

    return {
      passed: errors.length === 0,
      errors
    };
  }

  /**
   * Validate Lead Router business rules (TRADE SECRET)
   */
  private validateLeadRouterBusinessRules(output: LeadRouterOutput, lprScore: number) {
    const errors: string[] = [];

    // Rule 1: Priority must match LPR score
    if (lprScore >= 90 && output.priority > 1) {
      errors.push('LPR score 90+ must have priority 1');
    }

    // Rule 2: Routing decision must match priority
    if (output.priority === 1 && output.routingDecision !== 'IMMEDIATE_OUTREACH') {
      errors.push('Priority 1 must have IMMEDIATE_OUTREACH');
    }

    // Rule 3: High competitor threat should not result in DISQUALIFY
    if (output.competitiveIntelligence.competitorThreat === 'HIGH' &&
        output.routingDecision === 'DISQUALIFY') {
      errors.push('High competitor threat should trigger aggressive outreach, not disqualify');
    }

    return {
      passed: errors.length === 0,
      errors
    };
  }

  /**
   * Build LPR scoring prompt (PROPRIETARY - TRADE SECRET)
   */
  private buildLPRPrompt(leadData: any, businessContext: any): string {
    return `You are the Virtual LPR™ scoring engine, a proprietary system that predicts physical visit likelihood.

MISSION: Calculate LPR score (0-100) using 4-factor hybrid attribution model.

SCORING FACTORS (TRADE SECRET WEIGHTS):

1. Physical Intent (35-45% weight)
   - GMB actions: CALL=high, DIRECTIONS=very high, WEBSITE=medium, PHOTO_VIEW=low
   - Distance: <0.5mi=very high, 0.5-2mi=high, 2-5mi=medium, >5mi=low
   - Travel patterns: Frequent passerby=high

2. Behavioral Intelligence (25-30% weight)
   - Website visits: 3+=high, 1-2=medium, 0=low
   - Time on site: >2min=high, 30s-2min=medium, <30s=low
   - Social engagement: Recent activity=high

3. Temporal Signals (15-20% weight)
   - Time of day: Business hours=high, off-hours=low
   - Seasonality: January gym sign-ups=high, summer=lower
   - Event proximity: Near local event=boost

4. Competitive Context (10-15% weight)
   - Local saturation: Few competitors=high, many=lower
   - Competitor distance: Far=high, near=lower

TIER DEFINITIONS:
- Tier 1 (90-100): IMMEDIATE_VISIT - Call them NOW
- Tier 2 (70-89): HIGH_INTENT - Priority follow-up
- Tier 3 (45-69): MODERATE - Nurture campaign
- Tier 4 (20-44): AWARENESS - Educational content

LEAD DATA:
${JSON.stringify(leadData, null, 2)}

BUSINESS CONTEXT:
${JSON.stringify(businessContext, null, 2)}

RETURN ONLY VALID JSON (no prose):
{
  "lprScore": <0-100>,
  "tier": <1-4>,
  "tierLabel": "<IMMEDIATE_VISIT|HIGH_INTENT|MODERATE|AWARENESS>",
  "breakdown": {
    "physicalIntent": {"score": <0-100>, "weight": <0.35-0.45>, "contribution": <weighted score>},
    "behavioral": {"score": <0-100>, "weight": <0.25-0.30>, "contribution": <weighted score>},
    "temporal": {"score": <0-100>, "weight": <0.15-0.20>, "contribution": <weighted score>},
    "competitive": {"score": <0-100>, "weight": <0.10-0.15>, "contribution": <weighted score>}
  },
  "confidence": <0-100>,
  "recommendedAction": {
    "action": "<CALL_NOW|PRIORITY_FOLLOWUP|NURTURE|EDUCATIONAL_CONTENT>",
    "timing": "<ISO 8601>",
    "channel": "<SMS|EMAIL|CALL>",
    "message": "<max 200 chars>"
  },
  "predictionExpiry": "<ISO 8601, +24 hours>",
  "generatedAt": "<ISO 8601 now>"
}

CRITICAL: Ensure weights sum to 1.0 and tier matches score ranges.`;
  }

  /**
   * Build Lead Router prompt (PROPRIETARY)
   */
  private buildLeadRouterPrompt(lprScore: number, leadData: any, businessContext: any): string {
    return `You are the Lead Router agent in the DMN Protocol™ Tactical Layer.

MISSION: Route lead based on LPR score, competitive context, and business capacity.

LPR SCORE: ${lprScore}

LEAD DATA:
${JSON.stringify(leadData, null, 2)}

BUSINESS CONTEXT:
${JSON.stringify(businessContext, null, 2)}

ROUTING RULES:
- LPR 90+: IMMEDIATE_OUTREACH, priority 1
- LPR 70-89: IMMEDIATE_OUTREACH or SCHEDULED_FOLLOWUP, priority 2-3
- LPR 45-69: SCHEDULED_FOLLOWUP or NURTURE_CAMPAIGN, priority 3-4
- LPR <45: NURTURE_CAMPAIGN or DISQUALIFY, priority 4-5

COMPETITIVE INTELLIGENCE:
- If competitor is closer, increase urgency
- If high competitor threat, use differentiation message
- If local saturation high, filter for best-fit leads only

RETURN ONLY VALID JSON:
{
  "routingDecision": "<IMMEDIATE_OUTREACH|SCHEDULED_FOLLOWUP|NURTURE_CAMPAIGN|DISQUALIFY>",
  "priority": <1-5>,
  "assignedChannel": "<SMS|EMAIL|CALL|RETARGETING_AD>",
  "timing": {
    "optimal": "<ISO 8601>",
    "reason": "<max 200 chars>"
  },
  "competitiveIntelligence": {
    "competitorThreat": "<LOW|MEDIUM|HIGH>",
    "recommendedDifferentiator": "<max 200 chars>",
    "urgencyBoost": <0-50>
  },
  "personalizedMessage": {
    "hook": "<max 150 chars>",
    "offer": "<max 150 chars>",
    "cta": "<max 100 chars>"
  },
  "expectedConversionProbability": <0-100>,
  "generatedAt": "<ISO 8601>"
}`;
  }

  // Helper methods
  private async callClaude(prompt: string, options: any) {
    return await this.client.messages.create({
      model: options.model,
      max_tokens: options.maxTokens,
      temperature: options.temperature,
      messages: [{ role: 'user', content: prompt }]
    });
  }

  private parseAndValidate(responseText: string, schema: z.ZodSchema) {
    try {
      const jsonMatch = responseText.match(/\{[\s\S]*\}/);
      if (!jsonMatch) {
        return { success: false, error: 'No JSON found' };
      }

      const parsed = JSON.parse(jsonMatch[0]);
      const validated = schema.parse(parsed);
      return { success: true, data: validated };
    } catch (error: any) {
      return { success: false, error: error.message };
    }
  }

  private tightenPrompt(prompt: string, error: string): string {
    if (error.includes('weights')) {
      return prompt + '\n\n⚠️ CRITICAL: Weights MUST sum to exactly 1.0. Recalculate.';
    }
    if (error.includes('tier')) {
      return prompt + '\n\n⚠️ CRITICAL: Tier must match score ranges (1=90+, 2=70-89, 3=45-69, 4=<45).';
    }
    return prompt + '\n\n⚠️ CRITICAL: Fix validation errors and return valid JSON only.';
  }

  private calculateCost(tokens: number): number {
    // Claude Sonnet 4.5: $0.003 input, $0.015 output per 1K tokens
    return (tokens / 2) * 0.003 / 1000 + (tokens / 2) * 0.015 / 1000;
  }
}

// ============================================================================
// OBSERVABILITY: Prediction Tracking and Accuracy Measurement
// ============================================================================

interface VirtualLPRTrace {
  traceId: string;
  businessId: string;
  timestamp: string;

  input: {
    leadData: any;
    businessContext: any;
    dataSources: string[];
    dataQuality: number;
  };

  prediction: {
    lprScore: number;
    tier: number;
    confidence: number;
    weights: any;
  };

  routing: {
    decision: string;
    priority: number;
    channel: string;
  };

  outcome?: {
    trackedAt: string;
    physicalVisit: boolean;
    visitDate?: string;
    conversion: boolean;
    revenue?: number;
    actualConversionTime: number;
  };

  accuracy?: {
    scoreAccuracy: number;
    tierAccuracy: boolean;
    overallAccuracy: number;
  };

  learningSignals?: {
    adjustWeights: boolean;
    newPattern: boolean;
    notes: string[];
  };
}

class VirtualLPRObservability {
  private traces: Map<string, VirtualLPRTrace> = new Map();

  /**
   * Track LPR prediction
   */
  trackPrediction(
    businessId: string,
    leadData: any,
    businessContext: any,
    lprOutput: VirtualLPROutput,
    routingOutput: LeadRouterOutput
  ): string {
    const traceId = uuidv4();

    const trace: VirtualLPRTrace = {
      traceId,
      businessId,
      timestamp: new Date().toISOString(),
      input: {
        leadData,
        businessContext,
        dataSources: this.detectDataSources(leadData),
        dataQuality: this.calculateDataQuality(leadData)
      },
      prediction: {
        lprScore: lprOutput.lprScore,
        tier: lprOutput.tier,
        confidence: lprOutput.confidence,
        weights: lprOutput.breakdown  // TRADE SECRET - store but don't expose publicly
      },
      routing: {
        decision: routingOutput.routingDecision,
        priority: routingOutput.priority,
        channel: routingOutput.assignedChannel
      }
    };

    this.traces.set(traceId, trace);

    console.log(`[TRACE] 📊 Tracked prediction ${traceId}: LPR=${lprOutput.lprScore}, Tier=${lprOutput.tier}`);

    return traceId;
  }

  /**
   * Track actual outcome (physical visit, conversion)
   */
  trackOutcome(
    traceId: string,
    outcome: {
      physicalVisit: boolean;
      visitDate?: string;
      conversion: boolean;
      revenue?: number;
    }
  ) {
    const trace = this.traces.get(traceId);
    if (!trace) {
      console.error(`[TRACE] ❌ Trace ${traceId} not found`);
      return;
    }

    const predictionTime = new Date(trace.timestamp);
    const outcomeTime = outcome.visitDate ? new Date(outcome.visitDate) : new Date();
    const hoursToConversion = (outcomeTime.getTime() - predictionTime.getTime()) / (1000 * 60 * 60);

    // Calculate accuracy
    const accuracy = this.calculateAccuracy(trace.prediction, outcome);

    trace.outcome = {
      trackedAt: new Date().toISOString(),
      ...outcome,
      actualConversionTime: hoursToConversion
    };

    trace.accuracy = accuracy;

    // Generate learning signals
    trace.learningSignals = this.generateLearningSignals(trace);

    console.log(`[TRACE] ✅ Outcome tracked for ${traceId}:`);
    console.log(`  Physical visit: ${outcome.physicalVisit}`);
    console.log(`  Conversion: ${outcome.conversion}`);
    console.log(`  Accuracy: ${accuracy.overallAccuracy.toFixed(2)}%`);

    if (trace.learningSignals.adjustWeights) {
      console.log(`[LEARNING] 🔧 Weight adjustment recommended`);
    }
  }

  /**
   * Calculate prediction accuracy (PROPRIETARY)
   */
  private calculateAccuracy(prediction: any, outcome: any) {
    let scoreAccuracy = 100;

    // High LPR score + conversion = accurate
    if (outcome.conversion && prediction.lprScore >= 70) {
      scoreAccuracy = 100;
    }
    // High LPR score + no conversion = inaccurate
    else if (!outcome.conversion && prediction.lprScore >= 70) {
      scoreAccuracy = Math.max(0, 100 - prediction.lprScore);
    }
    // Low LPR score + conversion = inaccurate (missed opportunity)
    else if (outcome.conversion && prediction.lprScore < 70) {
      scoreAccuracy = prediction.lprScore;
    }
    // Low LPR score + no conversion = accurate
    else {
      scoreAccuracy = prediction.lprScore;
    }

    const expectedTier = outcome.conversion ? (outcome.physicalVisit ? 1 : 2) : 4;
    const tierAccuracy = prediction.tier === expectedTier;

    const overallAccuracy = (scoreAccuracy + (tierAccuracy ? 100 : 0)) / 2;

    return {
      scoreAccuracy,
      tierAccuracy,
      overallAccuracy
    };
  }

  /**
   * Generate learning signals for ML improvement
   */
  private generateLearningSignals(trace: VirtualLPRTrace) {
    const signals: any = {
      adjustWeights: false,
      newPattern: false,
      notes: []
    };

    // Check if weights need adjustment
    if (trace.accuracy && trace.accuracy.overallAccuracy < 70) {
      signals.adjustWeights = true;
      signals.notes.push(`Low accuracy (${trace.accuracy.overallAccuracy.toFixed(2)}%) - recalibrate weights`);
    }

    // Check for new patterns
    if (trace.outcome?.conversion && trace.prediction.lprScore < 50) {
      signals.newPattern = true;
      signals.notes.push('Unexpected conversion from low-score lead - analyze pattern');
    }

    return signals;
  }

  /**
   * Get analytics for business
   */
  getAnalytics(businessId: string) {
    const traces = Array.from(this.traces.values()).filter(t => t.businessId === businessId);

    const total = traces.length;
    const withOutcomes = traces.filter(t => t.outcome).length;
    const conversions = traces.filter(t => t.outcome?.conversion).length;

    const avgAccuracy = withOutcomes > 0
      ? traces
          .filter(t => t.accuracy)
          .reduce((sum, t) => sum + (t.accuracy?.overallAccuracy || 0), 0) / withOutcomes
      : 0;

    const tierConversionRates = {
      tier1: this.getTierConversionRate(traces, 1),
      tier2: this.getTierConversionRate(traces, 2),
      tier3: this.getTierConversionRate(traces, 3),
      tier4: this.getTierConversionRate(traces, 4)
    };

    return {
      summary: {
        totalPredictions: total,
        predictionsWithOutcomes: withOutcomes,
        conversions,
        conversionRate: total > 0 ? ((conversions / total) * 100).toFixed(2) + '%' : '0%',
        avgPredictionAccuracy: avgAccuracy.toFixed(2) + '%'
      },
      tierConversionRates,
      revenueImpact: {
        total: traces.reduce((sum, t) => sum + (t.outcome?.revenue || 0), 0),
        avgPerConversion: conversions > 0
          ? traces.reduce((sum, t) => sum + (t.outcome?.revenue || 0), 0) / conversions
          : 0
      },
      learningSignals: {
        weightsNeedAdjustment: traces.filter(t => t.learningSignals?.adjustWeights).length,
        newPatternsDetected: traces.filter(t => t.learningSignals?.newPattern).length
      }
    };
  }

  private getTierConversionRate(traces: VirtualLPRTrace[], tier: number): string {
    const tierTraces = traces.filter(t => t.prediction.tier === tier && t.outcome);
    const tierConversions = tierTraces.filter(t => t.outcome?.conversion).length;
    return tierTraces.length > 0
      ? ((tierConversions / tierTraces.length) * 100).toFixed(2) + '%'
      : 'N/A';
  }

  private detectDataSources(leadData: any): string[] {
    const sources: string[] = [];
    if (leadData.googleMaps) sources.push('Google Maps');
    if (leadData.ga4) sources.push('Google Analytics');
    if (leadData.gmb) sources.push('Google My Business');
    if (leadData.census) sources.push('US Census');
    return sources;
  }

  private calculateDataQuality(leadData: any): number {
    // Simple quality score based on completeness
    let score = 0;
    if (leadData.googleMaps) score += 25;
    if (leadData.ga4) score += 25;
    if (leadData.gmb) score += 25;
    if (leadData.census) score += 25;
    return score;
  }
}

// ============================================================================
// COMPLETE VIRTUAL LPR SYSTEM
// ============================================================================

class VirtualLPRSystem {
  private controlLoop: VirtualLPRControlLoop;
  private observability: VirtualLPRObservability;

  constructor(apiKey: string) {
    this.controlLoop = new VirtualLPRControlLoop(apiKey);
    this.observability = new VirtualLPRObservability();
  }

  /**
   * Main entry point: Process lead through Virtual LPR
   */
  async processLead(
    businessId: string,
    leadData: any,
    businessContext: any
  ) {
    console.log('='.repeat(80));
    console.log('VIRTUAL LPR CIRCUIT™ - Processing Lead');
    console.log('='.repeat(80));

    // Step 1: Calculate LPR Score
    console.log('\n📊 Step 1: Calculating LPR Score...');
    const lprResult = await this.controlLoop.calculateLPRScore(
      leadData,
      businessContext,
      this.observability
    );

    if (!lprResult.success) {
      console.error(`❌ LPR scoring failed: ${lprResult.error}`);
      return { success: false, error: lprResult.error };
    }

    console.log(`✅ LPR Score: ${lprResult.data!.lprScore} (Tier ${lprResult.data!.tier})`);
    console.log(`   Confidence: ${lprResult.data!.confidence}%`);
    console.log(`   Cost: $${lprResult.metadata.cost.toFixed(4)}`);

    // Step 2: Route Lead
    console.log('\n📍 Step 2: Routing Lead...');
    const routingResult = await this.controlLoop.routeLead(
      lprResult.data!.lprScore,
      leadData,
      businessContext
    );

    if (!routingResult.success) {
      console.error(`❌ Lead routing failed: ${routingResult.error}`);
      return { success: false, error: routingResult.error };
    }

    console.log(`✅ Routing: ${routingResult.data!.routingDecision}`);
    console.log(`   Priority: ${routingResult.data!.priority}`);
    console.log(`   Channel: ${routingResult.data!.assignedChannel}`);
    console.log(`   Cost: $${routingResult.metadata.cost.toFixed(4)}`);

    // Step 3: Track Prediction
    console.log('\n🔍 Step 3: Tracking Prediction...');
    const traceId = this.observability.trackPrediction(
      businessId,
      leadData,
      businessContext,
      lprResult.data!,
      routingResult.data!
    );

    console.log(`✅ Trace ID: ${traceId}`);

    // Step 4: Return Complete Analysis
    const totalCost = lprResult.metadata.cost + routingResult.metadata.cost;

    console.log('\n='.repeat(80));
    console.log(`Total Cost: $${totalCost.toFixed(4)}`);
    console.log('='.repeat(80));

    return {
      success: true,
      traceId,
      lpr: lprResult.data,
      routing: routingResult.data,
      metadata: {
        totalCost,
        totalTime: lprResult.metadata.totalTime + routingResult.metadata.totalTime,
        totalAttempts: lprResult.metadata.attempts + routingResult.metadata.attempts
      }
    };
  }

  /**
   * Track outcome for a prediction
   */
  async recordOutcome(
    traceId: string,
    outcome: {
      physicalVisit: boolean;
      visitDate?: string;
      conversion: boolean;
      revenue?: number;
    }
  ) {
    this.observability.trackOutcome(traceId, outcome);
  }

  /**
   * Get analytics for a business
   */
  getAnalytics(businessId: string) {
    return this.observability.getAnalytics(businessId);
  }
}

// ============================================================================
// USAGE EXAMPLE
// ============================================================================

async function main() {
  console.log('VIRTUAL LPR CIRCUIT™ - Production Implementation Example\n');

  const apiKey = process.env.ANTHROPIC_API_KEY || 'YOUR_API_KEY';
  const system = new VirtualLPRSystem(apiKey);

  // Sample lead data
  const leadData = {
    googleMaps: {
      distance: 0.8,  // miles
      searchQuery: 'CrossFit gym near me',
      popularTimes: [/* hourly data */]
    },
    ga4: {
      visits: 3,
      timeOnSite: 180,  // seconds
      pages: ['/pricing', '/schedule', '/trial']
    },
    gmb: {
      actions: [
        { action: 'DIRECTIONS', timestamp: '2025-11-11T10:30:00Z' },
        { action: 'CALL', timestamp: '2025-11-11T11:15:00Z' }
      ]
    },
    census: {
      incomeRange: '$75K-$100K',
      age: 28,
      interests: ['fitness', 'wellness']
    }
  };

  const businessContext = {
    businessType: 'gym',
    location: { lat: 42.3601, lon: -71.0589 },  // Boston
    capacity: 50,
    currentLoad: 35,
    competitors: [
      { name: 'Planet Fitness', distance: 1.2, rating: 4.2 },
      { name: 'LA Fitness', distance: 2.5, rating: 4.0 }
    ]
  };

  // Process lead
  const result = await system.processLead(
    'gym_boston_001',
    leadData,
    businessContext
  );

  if (result.success) {
    console.log('\n✅ Lead processed successfully!');
    console.log(`Trace ID: ${result.traceId}`);
    console.log(`Total Cost: $${result.metadata.totalCost.toFixed(4)}`);

    // Simulate outcome tracking (would happen 24-48 hours later)
    console.log('\n📈 Simulating outcome tracking...');
    await system.recordOutcome(result.traceId, {
      physicalVisit: true,
      visitDate: '2025-11-12T09:00:00Z',
      conversion: true,
      revenue: 199  // Monthly membership
    });

    // Get analytics
    console.log('\n📊 Business Analytics:');
    const analytics = system.getAnalytics('gym_boston_001');
    console.log(JSON.stringify(analytics, null, 2));
  }
}

// Uncomment to run example:
// main().catch(console.error);

export {
  VirtualLPRSystem,
  VirtualLPRControlLoop,
  VirtualLPRObservability,
  VirtualLPROutputSchema,
  LeadRouterOutputSchema,
  VirtualTrafficCameraOutputSchema
};
