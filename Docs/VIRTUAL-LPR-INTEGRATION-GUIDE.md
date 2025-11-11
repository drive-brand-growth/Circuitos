# Virtual LPR Circuit™ - Integration Guide
## Applying Production Patterns to Existing System

**Version:** 1.0
**Date:** 2025-11-11
**Classification:** CONFIDENTIAL

---

## Overview

This guide shows how to integrate **Contract + Control Loop + Observability** patterns into your existing Virtual LPR Circuit™ system without disrupting current functionality.

**Goal:** Transform from innovative prototype → production-grade, enterprise-ready system

**Timeline:** 4 weeks

**Effort:** 1-2 engineers

---

## Current State vs Target State

### Current State (What You Have)

```
Lead Data → Claude API → LPR Score → Manual Review
```

**Issues:**
- No validation of LPR scores
- No retry logic if Claude returns malformed data
- No tracking of prediction accuracy
- No learning loop for weight optimization
- Manual quality control

### Target State (After Integration)

```
Lead Data → [Contract Validation] → Claude API → [Schema Validation]
                                        ↓
                            [Retry if invalid]
                                        ↓
                            Valid LPR Score → [Business Rule Check]
                                        ↓
                            [Track Prediction]
                                        ↓
                            [Track Outcome 24h later]
                                        ↓
                            [Measure Accuracy]
                                        ↓
                            [Adjust Weights if needed]
```

**Benefits:**
- ✅ 95%+ valid outputs
- ✅ Automatic retry and repair
- ✅ Measurable accuracy over time
- ✅ Self-improving system
- ✅ Enterprise-ready reliability

---

## Integration Roadmap

### Week 1: Add Contracts

**Goal:** Define and validate all output schemas

#### Step 1.1: Install Dependencies

```bash
cd /path/to/circuitos
npm install zod @anthropic-ai/sdk uuid
```

#### Step 1.2: Create Schema Files

Create `src/contracts/virtual-lpr-schemas.ts`:

```typescript
import { z } from 'zod';

export const VirtualLPROutputSchema = z.object({
  lprScore: z.number().int().min(0).max(100),
  tier: z.union([z.literal(1), z.literal(2), z.literal(3), z.literal(4)]),
  // ... (copy from VIRTUAL-LPR-IMPLEMENTATION.ts)
});

export const LeadRouterOutputSchema = z.object({
  // ... (copy from VIRTUAL-LPR-IMPLEMENTATION.ts)
});

// Export types
export type VirtualLPROutput = z.infer<typeof VirtualLPROutputSchema>;
export type LeadRouterOutput = z.infer<typeof LeadRouterOutputSchema>;
```

#### Step 1.3: Update Existing LPR Scoring Function

**Before:**
```typescript
async function calculateLPRScore(leadData: any) {
  const response = await claude.messages.create({
    model: 'claude-sonnet-4-5',
    messages: [{ role: 'user', content: buildPrompt(leadData) }]
  });

  // Hope it's valid JSON 🤞
  return JSON.parse(response.content[0].text);
}
```

**After:**
```typescript
import { VirtualLPROutputSchema } from './contracts/virtual-lpr-schemas';

async function calculateLPRScore(leadData: any) {
  const response = await claude.messages.create({
    model: 'claude-sonnet-4-5',
    messages: [{ role: 'user', content: buildPrompt(leadData) }]
  });

  const rawOutput = response.content[0].text;

  // Extract JSON
  const jsonMatch = rawOutput.match(/\{[\s\S]*\}/);
  if (!jsonMatch) {
    throw new Error('No JSON found in response');
  }

  const parsed = JSON.parse(jsonMatch[0]);

  // VALIDATE against schema
  try {
    const validated = VirtualLPROutputSchema.parse(parsed);
    return validated;  // ✅ Guaranteed to match schema
  } catch (error) {
    console.error('Validation failed:', error.message);
    throw new Error(`Invalid LPR output: ${error.message}`);
  }
}
```

**Test It:**
```bash
npm test -- --grep "LPR schema validation"
```

---

### Week 2: Add Control Loop

**Goal:** Implement retry/repair logic

#### Step 2.1: Create Control Loop Class

Create `src/services/virtual-lpr-control-loop.ts`:

```typescript
// Copy VirtualLPRControlLoop class from VIRTUAL-LPR-IMPLEMENTATION.ts
```

#### Step 2.2: Replace Direct Claude Calls

**Before:**
```typescript
const lprScore = await calculateLPRScore(leadData);
```

**After:**
```typescript
import { VirtualLPRControlLoop } from './services/virtual-lpr-control-loop';

const controlLoop = new VirtualLPRControlLoop(process.env.ANTHROPIC_API_KEY);

const result = await controlLoop.calculateLPRScore(
  leadData,
  businessContext
);

if (result.success) {
  const lprScore = result.data;
  console.log(`✅ LPR Score: ${lprScore.lprScore}`);
  console.log(`   Attempts: ${result.metadata.attempts}`);
  console.log(`   Cost: $${result.metadata.cost.toFixed(4)}`);
} else {
  console.error(`❌ Failed after ${result.metadata.attempts} attempts: ${result.error}`);
  // Fallback logic here
}
```

#### Step 2.3: Add Business Rule Validation

Enhance `validateLPRBusinessRules` with your proprietary rules:

```typescript
private validateLPRBusinessRules(output: VirtualLPROutput) {
  const errors: string[] = [];

  // YOUR PROPRIETARY RULES HERE
  // Example: Weights must sum to 1.0
  const totalWeight = /* calculate */;
  if (Math.abs(totalWeight - 1.0) > 0.01) {
    errors.push('Weights must sum to 1.0');
  }

  // Example: Tier must match score
  if (output.lprScore >= 90 && output.tier !== 1) {
    errors.push('Score 90+ must be Tier 1');
  }

  // ADD MORE RULES...

  return {
    passed: errors.length === 0,
    errors
  };
}
```

**Test It:**
```bash
npm test -- --grep "Control loop retries"
```

---

### Week 3: Add Observability

**Goal:** Track predictions and outcomes

#### Step 3.1: Set Up Database for Traces

**Option A: Supabase (Recommended)**

```sql
-- Create traces table
CREATE TABLE virtual_lpr_traces (
  trace_id UUID PRIMARY KEY,
  business_id TEXT NOT NULL,
  timestamp TIMESTAMPTZ NOT NULL,

  -- Input
  lead_data JSONB NOT NULL,
  business_context JSONB NOT NULL,
  data_sources TEXT[],
  data_quality INTEGER,

  -- Prediction
  lpr_score INTEGER NOT NULL,
  tier INTEGER NOT NULL,
  confidence INTEGER,
  weights JSONB NOT NULL,  -- TRADE SECRET - restricted access

  -- Routing
  routing_decision TEXT,
  priority INTEGER,
  channel TEXT,

  -- Outcome (tracked later)
  outcome_tracked_at TIMESTAMPTZ,
  physical_visit BOOLEAN,
  visit_date TIMESTAMPTZ,
  conversion BOOLEAN,
  revenue NUMERIC,
  actual_conversion_time NUMERIC,

  -- Accuracy (calculated when outcome known)
  score_accuracy NUMERIC,
  tier_accuracy BOOLEAN,
  overall_accuracy NUMERIC,

  -- Learning signals
  adjust_weights BOOLEAN DEFAULT FALSE,
  new_pattern BOOLEAN DEFAULT FALSE,
  learning_notes TEXT[],

  CONSTRAINT valid_lpr_score CHECK (lpr_score >= 0 AND lpr_score <= 100),
  CONSTRAINT valid_tier CHECK (tier IN (1, 2, 3, 4))
);

-- Index for fast lookups
CREATE INDEX idx_traces_business ON virtual_lpr_traces(business_id);
CREATE INDEX idx_traces_timestamp ON virtual_lpr_traces(timestamp);
CREATE INDEX idx_traces_outcome ON virtual_lpr_traces(outcome_tracked_at) WHERE outcome_tracked_at IS NOT NULL;

-- Restrict access to weights column (TRADE SECRET)
ALTER TABLE virtual_lpr_traces ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Weights visible only to admins" ON virtual_lpr_traces
  FOR SELECT
  USING (auth.jwt() ->> 'role' = 'admin' OR weights IS NULL);
```

**Option B: PostgreSQL (Self-hosted)**

Same schema, deploy to your own Postgres instance.

#### Step 3.2: Create Observability Class

Create `src/services/virtual-lpr-observability.ts`:

```typescript
// Copy VirtualLPRObservability class from VIRTUAL-LPR-IMPLEMENTATION.ts

// Add Supabase integration:
import { createClient } from '@supabase/supabase-js';

class VirtualLPRObservability {
  private supabase: any;

  constructor() {
    this.supabase = createClient(
      process.env.SUPABASE_URL!,
      process.env.SUPABASE_KEY!
    );
  }

  async trackPrediction(/* ... */) {
    const trace = { /* ... */ };

    // Store in Supabase
    const { error } = await this.supabase
      .from('virtual_lpr_traces')
      .insert(trace);

    if (error) {
      console.error('Failed to store trace:', error);
    }

    return trace.traceId;
  }

  async trackOutcome(traceId: string, outcome: any) {
    // Fetch trace
    const { data, error } = await this.supabase
      .from('virtual_lpr_traces')
      .select('*')
      .eq('trace_id', traceId)
      .single();

    if (error || !data) {
      console.error('Trace not found:', traceId);
      return;
    }

    // Calculate accuracy
    const accuracy = this.calculateAccuracy(data, outcome);

    // Update trace
    await this.supabase
      .from('virtual_lpr_traces')
      .update({
        outcome_tracked_at: new Date().toISOString(),
        physical_visit: outcome.physicalVisit,
        conversion: outcome.conversion,
        revenue: outcome.revenue,
        score_accuracy: accuracy.scoreAccuracy,
        overall_accuracy: accuracy.overallAccuracy,
        // ... more fields
      })
      .eq('trace_id', traceId);
  }
}
```

#### Step 3.3: Schedule Outcome Tracking

Create `src/jobs/track-outcomes.ts`:

```typescript
/**
 * Cron job: Check outcomes for predictions made 24-48 hours ago
 * Run every 6 hours
 */

export async function trackOutcomesJob() {
  const supabase = createClient(/* ... */);

  // Get predictions from 24-48 hours ago without outcomes
  const { data: traces } = await supabase
    .from('virtual_lpr_traces')
    .select('*')
    .is('outcome_tracked_at', null)
    .gte('timestamp', /* 48 hours ago */)
    .lte('timestamp', /* 24 hours ago */);

  for (const trace of traces) {
    // Check business's CRM/database for outcome
    const outcome = await checkBusinessOutcome(
      trace.business_id,
      trace.lead_data
    );

    if (outcome) {
      // Track outcome
      const observability = new VirtualLPRObservability();
      await observability.trackOutcome(trace.trace_id, outcome);
    }
  }
}

async function checkBusinessOutcome(businessId: string, leadData: any) {
  // Query business's CRM/database
  // Did this lead visit? Did they convert?
  // Return { physicalVisit, conversion, revenue }

  // This is business-specific integration
  // Could be: Salesforce, HubSpot, GoHighLevel, etc.
}
```

**Deploy with cron:**
```bash
# Add to crontab (run every 6 hours)
0 */6 * * * node /path/to/track-outcomes.js
```

**Or use Vercel Cron:**
```javascript
// api/cron/track-outcomes.js
export default async function handler(req, res) {
  await trackOutcomesJob();
  res.status(200).json({ success: true });
}

// vercel.json
{
  "crons": [{
    "path": "/api/cron/track-outcomes",
    "schedule": "0 */6 * * *"
  }]
}
```

---

### Week 4: ML Feedback Loop

**Goal:** Self-improving weight calibration

#### Step 4.1: Collect Accuracy Data

```typescript
// Query traces with outcomes
const traces = await supabase
  .from('virtual_lpr_traces')
  .select('*')
  .not('outcome_tracked_at', 'is', null)
  .gte('timestamp', /* last 30 days */);

// Calculate aggregate accuracy
const avgAccuracy = traces.reduce((sum, t) => sum + t.overall_accuracy, 0) / traces.length;

console.log(`Average prediction accuracy: ${avgAccuracy.toFixed(2)}%`);
```

#### Step 4.2: Identify Patterns for Weight Adjustment

```typescript
/**
 * Analyze prediction errors to adjust weights
 */
function analyzeErrorPatterns(traces: any[]) {
  const errors = traces.filter(t => t.overall_accuracy < 70);

  // Pattern 1: Over-predicting physical intent
  const highPhysicalNoConversion = errors.filter(t =>
    t.weights.physicalIntent.contribution > 40 &&
    !t.physical_visit
  );

  if (highPhysicalNoConversion.length > errors.length * 0.3) {
    console.log('🔧 Pattern detected: Over-weighting physical intent');
    console.log('   Recommendation: Decrease physicalIntent weight from 0.40 to 0.37');
    console.log('   Increase behavioral weight from 0.27 to 0.30');
  }

  // Pattern 2: Under-predicting behavioral signals
  const lowBehavioralButConverted = errors.filter(t =>
    t.weights.behavioral.contribution < 20 &&
    t.conversion
  );

  if (lowBehavioralButConverted.length > errors.length * 0.3) {
    console.log('🔧 Pattern detected: Under-weighting behavioral signals');
    console.log('   Recommendation: Increase behavioral weight');
  }

  // MORE PATTERNS...
}
```

#### Step 4.3: Implement Weight Adjustment System

```typescript
/**
 * TRADE SECRET: Proprietary weight calibration algorithm
 * Adjusts weights based on prediction accuracy
 */

interface WeightConfig {
  physicalIntent: number;  // 0.35-0.45
  behavioral: number;      // 0.25-0.30
  temporal: number;        // 0.15-0.20
  competitive: number;     // 0.10-0.15
}

class WeightCalibrator {
  private defaultWeights: WeightConfig = {
    physicalIntent: 0.40,
    behavioral: 0.27,
    temporal: 0.18,
    competitive: 0.15
  };

  /**
   * Calibrate weights for a specific business
   * Based on their historical accuracy data
   */
  async calibrateForBusiness(businessId: string): Promise<WeightConfig> {
    // Get last 100 predictions with outcomes
    const traces = await this.getTracesWithOutcomes(businessId, 100);

    if (traces.length < 20) {
      // Not enough data, use defaults
      return this.defaultWeights;
    }

    // Calculate optimal weights using gradient descent or similar
    const optimized = this.optimizeWeights(traces);

    console.log(`[CALIBRATION] Business ${businessId}:`);
    console.log(`  Physical Intent: ${optimized.physicalIntent.toFixed(3)}`);
    console.log(`  Behavioral: ${optimized.behavioral.toFixed(3)}`);
    console.log(`  Temporal: ${optimized.temporal.toFixed(3)}`);
    console.log(`  Competitive: ${optimized.competitive.toFixed(3)}`);

    // Store calibrated weights for this business
    await this.storeWeights(businessId, optimized);

    return optimized;
  }

  private optimizeWeights(traces: any[]): WeightConfig {
    // TRADE SECRET: Your proprietary optimization algorithm
    // This could be:
    // - Gradient descent
    // - Bayesian optimization
    // - Reinforcement learning
    // - Simple heuristic adjustments

    // Placeholder: Simple adjustment based on error patterns
    let weights = { ...this.defaultWeights };

    const errors = traces.filter(t => t.overall_accuracy < 70);

    // Adjust based on error patterns
    // (Your actual algorithm goes here)

    // Ensure constraints
    weights = this.ensureConstraints(weights);

    return weights;
  }

  private ensureConstraints(weights: WeightConfig): WeightConfig {
    // Ensure weights are within valid ranges
    weights.physicalIntent = Math.max(0.35, Math.min(0.45, weights.physicalIntent));
    weights.behavioral = Math.max(0.25, Math.min(0.30, weights.behavioral));
    weights.temporal = Math.max(0.15, Math.min(0.20, weights.temporal));
    weights.competitive = Math.max(0.10, Math.min(0.15, weights.competitive));

    // Normalize to sum to 1.0
    const total = Object.values(weights).reduce((a, b) => a + b, 0);
    Object.keys(weights).forEach(key => {
      weights[key as keyof WeightConfig] /= total;
    });

    return weights;
  }

  private async getTracesWithOutcomes(businessId: string, limit: number) {
    // Query database
    return [];
  }

  private async storeWeights(businessId: string, weights: WeightConfig) {
    // Store in database for this business
  }
}
```

---

## Testing Strategy

### Unit Tests

```typescript
// tests/virtual-lpr-control-loop.test.ts

describe('VirtualLPRControlLoop', () => {
  it('should validate weights sum to 1.0', () => {
    const invalidOutput = {
      lprScore: 85,
      breakdown: {
        physicalIntent: { weight: 0.40, /* ... */ },
        behavioral: { weight: 0.30, /* ... */ },
        temporal: { weight: 0.20, /* ... */ },
        competitive: { weight: 0.15, /* ... */ }
        // Sum = 1.05 (invalid)
      }
    };

    const result = controlLoop.validateLPRBusinessRules(invalidOutput);
    expect(result.passed).toBe(false);
    expect(result.errors).toContain('Weights must sum to 1.0');
  });

  it('should retry on validation failure', async () => {
    // Mock Claude to return invalid JSON first, then valid
    const result = await controlLoop.calculateLPRScore(leadData, context);

    expect(result.success).toBe(true);
    expect(result.metadata.attempts).toBeGreaterThan(1);
  });
});
```

### Integration Tests

```typescript
// tests/virtual-lpr-end-to-end.test.ts

describe('Virtual LPR End-to-End', () => {
  it('should process lead and track prediction', async () => {
    const system = new VirtualLPRSystem(process.env.ANTHROPIC_API_KEY);

    const result = await system.processLead(
      'test_business_001',
      testLeadData,
      testBusinessContext
    );

    expect(result.success).toBe(true);
    expect(result.lpr.lprScore).toBeGreaterThanOrEqual(0);
    expect(result.lpr.lprScore).toBeLessThanOrEqual(100);
    expect(result.traceId).toBeDefined();

    // Verify trace was stored
    const trace = await getTrace(result.traceId);
    expect(trace).toBeDefined();
    expect(trace.prediction.lprScore).toBe(result.lpr.lprScore);
  });

  it('should track outcome and calculate accuracy', async () => {
    // Create prediction
    const result = await system.processLead(/* ... */);

    // Simulate outcome
    await system.recordOutcome(result.traceId, {
      physicalVisit: true,
      conversion: true,
      revenue: 199
    });

    // Check accuracy was calculated
    const trace = await getTrace(result.traceId);
    expect(trace.accuracy).toBeDefined();
    expect(trace.accuracy.overallAccuracy).toBeGreaterThan(0);
  });
});
```

---

## Deployment Checklist

### Pre-Deployment

- [ ] All contracts defined and tested
- [ ] Control loop implemented with retry logic
- [ ] Observability database set up (Supabase/Postgres)
- [ ] Outcome tracking job scheduled
- [ ] Unit tests passing (>90% coverage)
- [ ] Integration tests passing
- [ ] Load testing completed (handle 100+ req/sec)

### Deployment Steps

1. **Deploy Database Schema**
   ```bash
   psql -h your-db.supabase.co -U postgres -d postgres < schema.sql
   ```

2. **Deploy Application Code**
   ```bash
   git push production main
   ```

3. **Deploy Cron Jobs**
   ```bash
   # Vercel
   vercel --prod

   # Or traditional cron
   crontab -e
   # Add: 0 */6 * * * /path/to/track-outcomes
   ```

4. **Monitor First 24 Hours**
   - Check logs for validation errors
   - Monitor retry rates
   - Verify traces being stored
   - Check outcome tracking job runs

### Post-Deployment

- [ ] Monitor success rate (target: >95%)
- [ ] Monitor average cost per prediction (target: <$0.10)
- [ ] Track prediction accuracy after 7 days
- [ ] Review learning signals weekly
- [ ] Adjust weights monthly based on data

---

## Success Metrics

Track these metrics to measure integration success:

### Technical Metrics

| Metric | Baseline | Week 1 | Week 2 | Week 3 | Week 4 | Target |
|--------|----------|--------|--------|--------|--------|--------|
| Validation success rate | Unknown | 70% | 85% | 92% | 95% | >95% |
| Avg attempts per request | 1.0 | 1.0 | 1.2 | 1.1 | 1.05 | <1.2 |
| Response time (p95) | Unknown | 5s | 4s | 3.5s | 3s | <5s |
| Cost per prediction | Unknown | $0.08 | $0.07 | $0.06 | $0.05 | <$0.10 |

### Business Metrics

| Metric | Baseline | Target (30 days) |
|--------|----------|------------------|
| Prediction accuracy | Unknown | >85% |
| Tier 1 conversion rate | Unknown | >40% |
| Revenue per lead | Unknown | >$50 |
| Time to conversion | Unknown | <48 hours (Tier 1) |

---

## Troubleshooting

### Issue: Validation Success Rate <90%

**Symptoms:** High retry rate, frequent validation failures

**Diagnosis:**
```bash
# Check validation error logs
grep "Validation failed" logs/virtual-lpr.log | tail -100

# Common errors:
# - "Weights must sum to 1.0"
# - "Tier must match score"
# - "No JSON found"
```

**Fix:**
1. Review prompt to ensure it specifies exact output format
2. Add more examples in prompt
3. Tighten temperature (reduce from 0.0 to 0.0... already at min)
4. Add repair logic for common mistakes

### Issue: High Cost Per Prediction

**Symptoms:** Cost >$0.10 per prediction

**Diagnosis:**
```bash
# Check token usage
grep "tokensUsed" logs/virtual-lpr.log | awk '{sum+=$2; count++} END {print sum/count}'
```

**Fix:**
1. Reduce prompt length (remove examples if necessary)
2. Use smaller model for simple leads (Haiku for Tier 4)
3. Cache common calculations
4. Batch multiple leads in one API call

### Issue: Low Prediction Accuracy

**Symptoms:** Overall accuracy <70%

**Diagnosis:**
```sql
-- Check accuracy by tier
SELECT tier, AVG(overall_accuracy)
FROM virtual_lpr_traces
WHERE outcome_tracked_at IS NOT NULL
GROUP BY tier;

-- Find common error patterns
SELECT
  CASE
    WHEN lpr_score > 70 AND NOT conversion THEN 'False positive'
    WHEN lpr_score < 50 AND conversion THEN 'False negative'
    ELSE 'Correct range'
  END AS pattern,
  COUNT(*)
FROM virtual_lpr_traces
WHERE outcome_tracked_at IS NOT NULL
GROUP BY pattern;
```

**Fix:**
1. Adjust weight ranges based on error patterns
2. Add more data sources to improve predictions
3. Refine business context inputs
4. Run weight calibration for specific businesses

---

## Maintenance

### Weekly

- [ ] Review validation error logs
- [ ] Check prediction accuracy trends
- [ ] Identify leads with low confidence scores
- [ ] Review learning signals

### Monthly

- [ ] Run weight calibration for all businesses
- [ ] Update prompts based on error patterns
- [ ] Optimize token usage
- [ ] Review and update business rules

### Quarterly

- [ ] Full accuracy audit
- [ ] A/B test new scoring algorithms
- [ ] Review competitive landscape changes
- [ ] Update seasonal patterns

---

## Conclusion

By following this integration guide, you'll transform your Virtual LPR Circuit™ from innovative prototype to production-grade, enterprise-ready system.

**Timeline:** 4 weeks

**Result:**
- ✅ 95%+ reliable outputs
- ✅ Measurable accuracy (>85%)
- ✅ Self-improving over time
- ✅ Enterprise-ready observability
- ✅ Enhanced IP value ($8M-$20M)

**Next Steps:**
1. Review this guide with engineering team
2. Set up Supabase database
3. Begin Week 1: Add Contracts
4. Track progress using metrics above

---

**© 2025 CircuitOS™ - ALL RIGHTS RESERVED**
**Classification:** CONFIDENTIAL
