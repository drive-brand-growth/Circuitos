/**
 * Circuit OS - Intelligent Model Router
 *
 * Automatically selects the optimal Claude model based on:
 * - Task complexity
 * - Quality requirements
 * - Cost optimization
 * - Response time needs
 *
 * Model Tiers:
 * - Sonnet 4.5: Complex reasoning, strategic decisions ($$$)
 * - Haiku: Simple tasks, high-volume operations ($)
 * - Regex: Deterministic patterns (FREE)
 */

/**
 * Model configurations
 */
const MODELS = {
  SONNET: {
    id: 'claude-sonnet-4-5-20250929',
    name: 'Sonnet 4.5',
    cost_per_1m_input: 3.00,
    cost_per_1m_output: 15.00,
    use_for: 'Complex reasoning, strategic analysis, creative tasks',
    avg_response_time: '3-8 seconds'
  },
  HAIKU: {
    id: 'claude-haiku-4-20250514',
    name: 'Haiku 4',
    cost_per_1m_input: 0.25,
    cost_per_1m_output: 1.25,
    use_for: 'Simple classification, validation, routing',
    avg_response_time: '1-2 seconds'
  },
  REGEX: {
    id: 'regex',
    name: 'Regex (No AI)',
    cost_per_1m_input: 0,
    cost_per_1m_output: 0,
    use_for: 'Pattern matching, sanitization, validation',
    avg_response_time: '<100ms'
  }
};

/**
 * Task complexity levels
 */
const COMPLEXITY = {
  HIGH: 'high',      // Requires Sonnet 4.5
  MEDIUM: 'medium',  // Can use Haiku
  LOW: 'low',        // Can use Regex
  AUTO: 'auto'       // Router decides
};

/**
 * Task-to-model mapping
 *
 * WORLD-CLASS STRATEGY:
 * - Use Sonnet 4.5 for EVERYTHING that affects customer experience, revenue, or security
 * - Only use Regex for deterministic pattern matching (where it's actually better than AI)
 * - Haiku available as override option, but NOT default (quality > cost)
 */
const TASK_MODEL_MAP = {
  // TIER 1: Customer-facing & Revenue-critical (Sonnet 4.5 - WORLD CLASS)
  'score-lead': MODELS.SONNET,              // Revenue decision - needs best reasoning
  'generate-copy': MODELS.SONNET,           // Customer-facing - needs best quality
  'design-workflow': MODELS.SONNET,         // Strategic - needs deep understanding
  'orchestrate': MODELS.SONNET,             // Coordinates everything - needs best planning
  'optimize-workflow': MODELS.SONNET,       // ML patterns - needs advanced analysis
  'respond-to-review': MODELS.SONNET,       // Public-facing - brand reputation critical

  // SALES SYSTEM (12 Frameworks + World-Class SDR) - TIER 1 CRITICAL
  'validate-lead': MODELS.SONNET,           // 12 sales frameworks - needs best analytical reasoning
  'generate-sdr-outreach': MODELS.SONNET,   // Revenue-critical - Eugene Schwartz + Brunson + Hormozi
  'handle-conversation': MODELS.SONNET,     // Two-way dialogue - needs human-level judgment
  'analyze-churn-risk': MODELS.SONNET,      // Retention = revenue - 5% retention increase = 25-95% profit increase

  // MARKETING SYSTEM (CMO + Director + Content Engine) - TIER 1 BRAND EXPANSION
  'generate-marketing-strategy': MODELS.SONNET,  // Strategic decisions - market analysis, budget allocation, brand positioning
  'plan-campaign-execution': MODELS.SONNET,      // Tactical planning - content calendar, A/B tests, performance tracking
  'create-social-content': MODELS.SONNET,        // Creative + structured - world-class copywriting for all channels
  'discover-channels': MODELS.SONNET,            // Virtual LPR reverse lookup - find where ICP congregates

  // CONVERSION OPTIMIZATION (Final 20% to 100%) - TIER 1 REVENUE CRITICAL
  'route-lead': MODELS.SONNET,                   // Intelligent rep assignment - maximize close rate
  'schedule-appointment': MODELS.SONNET,         // Calendar intelligence - no-show prevention, optimal timing
  'orchestrate-nurture': MODELS.SONNET,          // Adaptive sequences - engagement velocity based
  'analyze-attribution': MODELS.SONNET,          // Multi-touch attribution - channel ROI optimization
  'predict-outcomes': MODELS.SONNET,             // ML predictions - conversion probability, churn forecast, LTV

  // SOCIAL RESPONSE SYSTEM (World-Class 100x) - TIER 1 BRAND & REVENUE CRITICAL
  'respond-to-social-comment': MODELS.SONNET,    // Public brand presence - platform-specific responses, lead conversion
  'manage-reputation': MODELS.SONNET,            // Reputation protection - reviews, negative comments, crisis management
  'score-social-lead': MODELS.SONNET,            // Social lead scoring - different formula than regular leads
  'analyze-community-member': MODELS.SONNET,     // Community health - identify advocates, ambassadors
  'check-social-response-safety': MODELS.SONNET, // Brand safety - competitor mentions, defamation, sensitive topics

  // GEO-INTELLIGENCE SYSTEM (Google Maps AI Integration) - TIER 1 REVENUE & TERRITORY OPTIMIZATION
  'find-icp-locations': MODELS.SONNET,           // Geo-LPR - find ICP businesses by location ("all gyms in Austin")
  'enrich-business-data': MODELS.SONNET,         // Location enrichment - detailed business intelligence from Google Maps
  'analyze-market-territory': MODELS.SONNET,     // Market intelligence - opportunity scoring, competitive density, expansion recommendations
  'score-territories': MODELS.SONNET,            // Territory prioritization - rank markets for sales focus
  'enrich-lead-location': MODELS.SONNET,         // Lead enrichment - add location data, competitors, market position
  'route-with-geo-intelligence': MODELS.SONNET,  // Enhanced lead routing - drive time, territory fit, coverage analysis
  'optimize-travel-schedule': MODELS.SONNET,     // Appointment scheduling - travel time optimization, route planning
  'monitor-competitor': MODELS.SONNET,           // Competitive intelligence - ratings, reviews, trends, threats, opportunities

  // TIER 2: Security & Validation (Sonnet 4.5 - CATCHES EDGE CASES)
  // Using Sonnet because security edge cases cost more than API calls
  'guardrail-jailbreak': MODELS.SONNET,     // Security critical - catch sophisticated attacks
  'guardrail-nsfw': MODELS.SONNET,          // Brand safety - catch nuanced content
  'guardrail-pii-detect': MODELS.SONNET,    // TCPA compliance - catch edge cases ($500-1500 per violation!)
  'guardrail-secret-keys': MODELS.SONNET,   // Security critical - detect obfuscated keys
  'guardrail-topical': MODELS.SONNET,       // Customer experience - nuanced topic detection
  'guardrail-custom': MODELS.SONNET,        // Custom rules - needs best reasoning

  // TIER 3: Deterministic tasks (Regex - PERFECT for patterns)
  // Regex is actually BETTER than AI for these (instant, deterministic, free)
  'sanitize-pii': MODELS.REGEX,             // Pattern matching - regex is ideal
  'sanitize-keys': MODELS.REGEX,            // Pattern matching - regex is ideal
  'sanitize-urls': MODELS.REGEX,            // Pattern matching - regex is ideal
  'sanitize-custom': MODELS.REGEX,          // Pattern matching - regex is ideal
  'keyword-blocking': MODELS.REGEX,         // Exact match - regex is ideal
  'url-validation': MODELS.REGEX,           // Pattern matching - regex is ideal

  // OPTIONAL: Internal operations (can override to Haiku if needed)
  // But default to Sonnet for consistency
  'simple-classification': MODELS.SONNET,
  'keyword-extraction': MODELS.SONNET
};

/**
 * Get optimal model for a task
 */
export function getModelForTask(task, overrideModel = null) {
  // If user explicitly specifies a model, use it
  if (overrideModel && MODELS[overrideModel.toUpperCase()]) {
    return MODELS[overrideModel.toUpperCase()];
  }

  // Get model from task mapping
  const model = TASK_MODEL_MAP[task];

  if (!model) {
    console.warn(`[Model Router] Unknown task: ${task}, defaulting to Sonnet 4.5`);
    return MODELS.SONNET;
  }

  return model;
}

/**
 * Estimate cost for a task
 */
export function estimateCost(task, inputTokens, outputTokens, model = null) {
  const selectedModel = model || getModelForTask(task);

  if (selectedModel.id === 'regex') {
    return {
      model: selectedModel.name,
      input_cost: 0,
      output_cost: 0,
      total_cost: 0,
      currency: 'USD'
    };
  }

  const inputCost = (inputTokens / 1_000_000) * selectedModel.cost_per_1m_input;
  const outputCost = (outputTokens / 1_000_000) * selectedModel.cost_per_1m_output;
  const totalCost = inputCost + outputCost;

  return {
    model: selectedModel.name,
    input_tokens: inputTokens,
    output_tokens: outputTokens,
    input_cost: inputCost.toFixed(6),
    output_cost: outputCost.toFixed(6),
    total_cost: totalCost.toFixed(6),
    currency: 'USD'
  };
}

/**
 * Get cost savings by using optimal model vs always using Sonnet
 */
export function calculateSavings(task, inputTokens, outputTokens) {
  const optimalModel = getModelForTask(task);
  const optimalCost = estimateCost(task, inputTokens, outputTokens, optimalModel);
  const sonnetCost = estimateCost(task, inputTokens, outputTokens, MODELS.SONNET);

  const savings = parseFloat(sonnetCost.total_cost) - parseFloat(optimalCost.total_cost);
  const savingsPercent = ((savings / parseFloat(sonnetCost.total_cost)) * 100).toFixed(1);

  return {
    optimal_model: optimalModel.name,
    optimal_cost: optimalCost.total_cost,
    sonnet_cost: sonnetCost.total_cost,
    savings: savings.toFixed(6),
    savings_percent: savingsPercent + '%'
  };
}

/**
 * Analyze complexity and recommend model
 */
export function analyzeComplexity(taskDescription, requiresReasoning = false, requiresCreativity = false) {
  // High complexity indicators
  const highComplexityKeywords = [
    'analyze', 'evaluate', 'design', 'create', 'generate', 'optimize',
    'strategic', 'multi-step', 'framework', 'psychographic', 'demographic'
  ];

  // Medium complexity indicators
  const mediumComplexityKeywords = [
    'classify', 'detect', 'check', 'validate', 'filter', 'categorize'
  ];

  // Low complexity indicators (can use regex)
  const lowComplexityKeywords = [
    'sanitize', 'redact', 'replace', 'remove', 'block', 'match'
  ];

  const description = taskDescription.toLowerCase();

  // Check for low complexity (regex patterns)
  if (lowComplexityKeywords.some(keyword => description.includes(keyword))) {
    if (description.includes('pattern') || description.includes('regex') || description.includes('format')) {
      return {
        complexity: COMPLEXITY.LOW,
        recommended_model: MODELS.REGEX,
        reasoning: 'Task is pattern-based and deterministic - regex is sufficient'
      };
    }
  }

  // Check for high complexity
  if (requiresReasoning || requiresCreativity ||
      highComplexityKeywords.some(keyword => description.includes(keyword))) {
    return {
      complexity: COMPLEXITY.HIGH,
      recommended_model: MODELS.SONNET,
      reasoning: 'Task requires complex reasoning or creative output - Sonnet 4.5 needed'
    };
  }

  // Check for medium complexity
  if (mediumComplexityKeywords.some(keyword => description.includes(keyword))) {
    return {
      complexity: COMPLEXITY.MEDIUM,
      recommended_model: MODELS.HAIKU,
      reasoning: 'Task is simple classification/validation - Haiku is sufficient and 10x cheaper'
    };
  }

  // Default to Sonnet if unsure
  return {
    complexity: COMPLEXITY.AUTO,
    recommended_model: MODELS.SONNET,
    reasoning: 'Complexity unclear - defaulting to Sonnet 4.5 for safety'
  };
}

/**
 * Get monthly cost projection
 */
export function projectMonthlyCost(taskVolumes) {
  /*
  taskVolumes format:
  {
    'score-lead': { count: 1000, avg_input_tokens: 1500, avg_output_tokens: 800 },
    'generate-copy': { count: 800, avg_input_tokens: 1200, avg_output_tokens: 600 },
    ...
  }
  */

  const breakdown = [];
  let totalCost = 0;

  for (const [task, volume] of Object.entries(taskVolumes)) {
    const model = getModelForTask(task);
    const { count, avg_input_tokens, avg_output_tokens } = volume;

    const totalInputTokens = count * avg_input_tokens;
    const totalOutputTokens = count * avg_output_tokens;

    const cost = estimateCost(task, totalInputTokens, totalOutputTokens, model);
    const taskTotalCost = parseFloat(cost.total_cost);

    breakdown.push({
      task,
      model: model.name,
      volume: count,
      cost_per_execution: (taskTotalCost / count).toFixed(6),
      total_cost: taskTotalCost.toFixed(2)
    });

    totalCost += taskTotalCost;
  }

  // Calculate savings vs all-Sonnet
  const allSonnetCost = breakdown.reduce((sum, item) => {
    const volume = taskVolumes[item.task];
    const sonnetCost = estimateCost(
      item.task,
      volume.count * volume.avg_input_tokens,
      volume.count * volume.avg_output_tokens,
      MODELS.SONNET
    );
    return sum + parseFloat(sonnetCost.total_cost);
  }, 0);

  const savings = allSonnetCost - totalCost;
  const savingsPercent = ((savings / allSonnetCost) * 100).toFixed(1);

  return {
    breakdown,
    total_cost: totalCost.toFixed(2),
    all_sonnet_cost: allSonnetCost.toFixed(2),
    monthly_savings: savings.toFixed(2),
    savings_percent: savingsPercent + '%',
    currency: 'USD'
  };
}

/**
 * Example usage and cost analysis (WORLD-CLASS STRATEGY)
 */
export function exampleCostAnalysis() {
  // Typical monthly volumes for a gym with 1000 leads/month
  // Using Sonnet 4.5 for ALL AI tasks (world-class quality)
  const monthlyVolumes = {
    'score-lead': {
      count: 1000,
      avg_input_tokens: 1500,
      avg_output_tokens: 800
    },
    'generate-copy': {
      count: 800,  // 80% of leads get AI copy
      avg_input_tokens: 1200,
      avg_output_tokens: 600
    },
    'guardrail-jailbreak': {
      count: 1000,  // Check every input (Sonnet catches sophisticated attacks)
      avg_input_tokens: 500,
      avg_output_tokens: 200
    },
    'guardrail-pii-detect': {
      count: 800,  // Before SMS campaigns (Sonnet catches edge cases - worth it to avoid $500-1500 fines)
      avg_input_tokens: 500,
      avg_output_tokens: 200
    },
    'guardrail-nsfw': {
      count: 800,  // Check all customer-facing outputs
      avg_input_tokens: 600,
      avg_output_tokens: 200
    },
    'sanitize-pii': {
      count: 1000,
      avg_input_tokens: 0,  // Regex (no tokens, no cost, instant)
      avg_output_tokens: 0
    },
    'design-workflow': {
      count: 4,  // Design 4 new workflows per month
      avg_input_tokens: 2000,
      avg_output_tokens: 3000
    },
    'optimize-workflow': {
      count: 8,  // Optimize 2 workflows per week
      avg_input_tokens: 3000,
      avg_output_tokens: 4000
    },
    'respond-to-review': {
      count: 50,  // Respond to 50 reviews per month
      avg_input_tokens: 800,
      avg_output_tokens: 400
    }
  };

  const projection = projectMonthlyCost(monthlyVolumes);

  // Add ROI analysis
  const avgRevenuePerConversion = 1200; // Gym membership LTV
  const conversionRate = 0.65; // 65% with AI vs 35% without
  const conversionsPerMonth = monthlyVolumes['score-lead'].count * conversionRate;
  const monthlyRevenue = conversionsPerMonth * avgRevenuePerConversion;

  projection.roi_analysis = {
    conversions_per_month: Math.round(conversionsPerMonth),
    avg_revenue_per_conversion: avgRevenuePerConversion,
    monthly_revenue_from_ai: monthlyRevenue.toFixed(2),
    ai_cost: projection.total_cost,
    roi: ((monthlyRevenue / parseFloat(projection.total_cost)) - 1).toFixed(1) + 'x',
    profit: (monthlyRevenue - parseFloat(projection.total_cost)).toFixed(2)
  };

  return projection;
}

export default {
  MODELS,
  COMPLEXITY,
  getModelForTask,
  estimateCost,
  calculateSavings,
  analyzeComplexity,
  projectMonthlyCost,
  exampleCostAnalysis
};
