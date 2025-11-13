/**
 * SOCIAL ANALYTICS TRACKER
 *
 * Purpose: Track and analyze social response performance and ROI
 *
 * Metrics Tracked:
 * 1. Response performance (time, engagement, conversion)
 * 2. Platform effectiveness (which platforms convert best)
 * 3. Framework performance (which copywriting frameworks work)
 * 4. A/B test results (response variant testing)
 * 5. ROI attribution (revenue from social engagement)
 */

import { createClient } from '@supabase/supabase-js';

const supabase = createClient(
  process.env.SUPABASE_URL,
  process.env.SUPABASE_KEY
);

/**
 * Track social response event
 *
 * @param {Object} eventData
 *   - event_type: "response_posted" | "dm_sent" | "lead_created" | "conversion"
 *   - platform: string
 *   - response_data: Object (full response from social-response-agent)
 *   - outcome: Object (what happened after)
 * @returns {Promise<Object>} Tracked event
 */
export async function trackEvent(eventData) {
  const {
    event_type,
    platform,
    response_data,
    outcome = {}
  } = eventData;

  const event = {
    event_type,
    platform,
    timestamp: new Date().toISOString(),

    // Response details
    sentiment: response_data.analysis?.sentiment,
    intent: response_data.analysis?.intent,
    lead_score: response_data.analysis?.lead_score,
    lead_tier: response_data.analysis?.lead_tier,
    routing_decision: response_data.routing_decision,

    // Response content
    response_text: response_data.public_response?.text,
    response_length: response_data.public_response?.estimated_length,
    framework_used: response_data.public_response?.framework_used,

    // DM sent?
    dm_sent: response_data.private_dm?.should_send || false,

    // Lead generation
    lead_created: response_data.lead_generation?.create_ghl_contact || false,

    // Outcome
    commenter_replied: outcome.commenter_replied || false,
    commenter_converted: outcome.commenter_converted || false,
    conversion_value: outcome.conversion_value || 0,
    engagement_score: outcome.engagement_score || 0
  };

  const { data, error } = await supabase
    .from('social_analytics_events')
    .insert(event)
    .select()
    .single();

  if (error) {
    console.error('Error tracking event:', error);
    throw error;
  }

  return data;
}

/**
 * Get response performance metrics
 *
 * @param {Object} filters
 *   - platform: string (optional)
 *   - date_range: { start: Date, end: Date } (optional)
 * @returns {Promise<Object>} Performance metrics
 */
export async function getResponsePerformance(filters = {}) {
  let query = supabase.from('social_analytics_events').select('*');

  if (filters.platform) {
    query = query.eq('platform', filters.platform);
  }

  if (filters.date_range) {
    query = query
      .gte('timestamp', filters.date_range.start.toISOString())
      .lte('timestamp', filters.date_range.end.toISOString());
  }

  const { data, error } = await query;

  if (error) {
    console.error('Error getting performance:', error);
    throw error;
  }

  // Calculate metrics
  const metrics = {
    total_responses: data.length,

    by_platform: {},
    by_tier: {},
    by_routing: {},

    engagement: {
      total_replies: data.filter(e => e.commenter_replied).length,
      reply_rate: 0,
      total_conversions: data.filter(e => e.commenter_converted).length,
      conversion_rate: 0
    },

    revenue: {
      total_revenue: data.reduce((sum, e) => sum + (e.conversion_value || 0), 0),
      avg_conversion_value: 0
    },

    response_quality: {
      avg_response_length: 0,
      framework_usage: {}
    }
  };

  // Platform breakdown
  data.forEach(e => {
    metrics.by_platform[e.platform] = (metrics.by_platform[e.platform] || 0) + 1;
  });

  // Tier breakdown
  data.forEach(e => {
    metrics.by_tier[e.lead_tier] = (metrics.by_tier[e.lead_tier] || 0) + 1;
  });

  // Routing breakdown
  data.forEach(e => {
    metrics.by_routing[e.routing_decision] = (metrics.by_routing[e.routing_decision] || 0) + 1;
  });

  // Engagement rates
  metrics.engagement.reply_rate = metrics.total_responses > 0
    ? (metrics.engagement.total_replies / metrics.total_responses) * 100
    : 0;

  metrics.engagement.conversion_rate = metrics.total_responses > 0
    ? (metrics.engagement.total_conversions / metrics.total_responses) * 100
    : 0;

  // Revenue metrics
  metrics.revenue.avg_conversion_value = metrics.engagement.total_conversions > 0
    ? metrics.revenue.total_revenue / metrics.engagement.total_conversions
    : 0;

  // Response quality
  const responseLengths = data.filter(e => e.response_length).map(e => e.response_length);
  metrics.response_quality.avg_response_length = responseLengths.length > 0
    ? responseLengths.reduce((sum, l) => sum + l, 0) / responseLengths.length
    : 0;

  // Framework usage
  data.forEach(e => {
    if (e.framework_used) {
      metrics.response_quality.framework_usage[e.framework_used] =
        (metrics.response_quality.framework_usage[e.framework_used] || 0) + 1;
    }
  });

  return metrics;
}

/**
 * Compare platform performance
 *
 * @returns {Promise<Array>} Platform comparison
 */
export async function comparePlatforms() {
  const { data, error } = await supabase
    .from('social_analytics_events')
    .select('*');

  if (error) {
    console.error('Error comparing platforms:', error);
    throw error;
  }

  const platforms = ['instagram', 'linkedin', 'twitter', 'facebook', 'tiktok', 'youtube'];
  const comparison = [];

  platforms.forEach(platform => {
    const platformData = data.filter(e => e.platform === platform);

    if (platformData.length === 0) {
      comparison.push({
        platform,
        responses: 0,
        reply_rate: 0,
        conversion_rate: 0,
        avg_revenue: 0,
        recommendation: 'No data yet'
      });
      return;
    }

    const replies = platformData.filter(e => e.commenter_replied).length;
    const conversions = platformData.filter(e => e.commenter_converted).length;
    const revenue = platformData.reduce((sum, e) => sum + (e.conversion_value || 0), 0);

    comparison.push({
      platform,
      responses: platformData.length,
      reply_rate: (replies / platformData.length) * 100,
      conversion_rate: (conversions / platformData.length) * 100,
      avg_revenue: conversions > 0 ? revenue / conversions : 0,
      total_revenue: revenue,
      recommendation: getplatformRecommendation(platform, platformData.length, conversions)
    });
  });

  return comparison.sort((a, b) => b.conversion_rate - a.conversion_rate);
}

/**
 * Helper: Get platform recommendation
 */
function getplatformRecommendation(platform, responses, conversions) {
  const conversionRate = responses > 0 ? (conversions / responses) * 100 : 0;

  if (conversionRate >= 20) {
    return `SCALE - ${platform} is converting exceptionally well (${conversionRate.toFixed(1)}%)`;
  } else if (conversionRate >= 10) {
    return `MAINTAIN - ${platform} is performing well (${conversionRate.toFixed(1)}%)`;
  } else if (conversionRate >= 5) {
    return `OPTIMIZE - ${platform} has potential, improve response strategy`;
  } else {
    return `EVALUATE - ${platform} underperforming, consider reducing focus`;
  }
}

/**
 * Track A/B test results
 *
 * @param {Object} testData
 *   - test_name: string
 *   - variant_a: Object
 *   - variant_b: Object
 * @returns {Promise<Object>} Test results
 */
export async function trackABTest(testData) {
  const { test_name, variant_a, variant_b } = testData;

  // Get responses for each variant
  const { data: variantAData } = await supabase
    .from('social_analytics_events')
    .select('*')
    .eq('a_b_test_name', test_name)
    .eq('a_b_test_variant', 'A');

  const { data: variantBData } = await supabase
    .from('social_analytics_events')
    .select('*')
    .eq('a_b_test_name', test_name)
    .eq('a_b_test_variant', 'B');

  const results = {
    test_name,
    variant_a: analyzeVariant(variant_a, variantAData || []),
    variant_b: analyzeVariant(variant_b, variantBData || []),
    winner: null,
    confidence: 0,
    recommendation: ''
  };

  // Determine winner
  if (results.variant_a.conversion_rate > results.variant_b.conversion_rate) {
    results.winner = 'A';
    const improvement = ((results.variant_a.conversion_rate - results.variant_b.conversion_rate) / results.variant_b.conversion_rate) * 100;
    results.recommendation = `Variant A wins with ${improvement.toFixed(1)}% higher conversion rate. Roll out to all traffic.`;
  } else if (results.variant_b.conversion_rate > results.variant_a.conversion_rate) {
    results.winner = 'B';
    const improvement = ((results.variant_b.conversion_rate - results.variant_a.conversion_rate) / results.variant_a.conversion_rate) * 100;
    results.recommendation = `Variant B wins with ${improvement.toFixed(1)}% higher conversion rate. Roll out to all traffic.`;
  } else {
    results.winner = 'TIE';
    results.recommendation = 'No significant difference. Continue testing or choose based on other factors.';
  }

  // Calculate statistical confidence (simplified)
  const totalSampleSize = (variantAData?.length || 0) + (variantBData?.length || 0);
  if (totalSampleSize >= 100) {
    results.confidence = 0.95; // High confidence with 100+ samples
  } else if (totalSampleSize >= 50) {
    results.confidence = 0.80; // Medium confidence with 50-99 samples
  } else {
    results.confidence = 0.50; // Low confidence with <50 samples
  }

  return results;
}

/**
 * Analyze single A/B test variant
 */
function analyzeVariant(variant, data) {
  return {
    name: variant.name,
    responses: data.length,
    replies: data.filter(e => e.commenter_replied).length,
    conversions: data.filter(e => e.commenter_converted).length,
    reply_rate: data.length > 0 ? (data.filter(e => e.commenter_replied).length / data.length) * 100 : 0,
    conversion_rate: data.length > 0 ? (data.filter(e => e.commenter_converted).length / data.length) * 100 : 0,
    total_revenue: data.reduce((sum, e) => sum + (e.conversion_value || 0), 0)
  };
}

/**
 * Get framework performance comparison
 *
 * @returns {Promise<Array>} Framework performance
 */
export async function compareFrameworks() {
  const { data, error } = await supabase
    .from('social_analytics_events')
    .select('*')
    .not('framework_used', 'is', null);

  if (error) {
    console.error('Error comparing frameworks:', error);
    throw error;
  }

  const frameworks = [...new Set(data.map(e => e.framework_used))];
  const comparison = [];

  frameworks.forEach(framework => {
    const frameworkData = data.filter(e => e.framework_used === framework);

    const conversions = frameworkData.filter(e => e.commenter_converted).length;
    const revenue = frameworkData.reduce((sum, e) => sum + (e.conversion_value || 0), 0);

    comparison.push({
      framework,
      usage_count: frameworkData.length,
      conversion_rate: (conversions / frameworkData.length) * 100,
      total_revenue: revenue,
      avg_revenue_per_use: frameworkData.length > 0 ? revenue / frameworkData.length : 0
    });
  });

  return comparison.sort((a, b) => b.conversion_rate - a.conversion_rate);
}

/**
 * Calculate ROI from social engagement
 *
 * @param {Object} costs
 *   - ai_cost: number (monthly AI API cost)
 *   - human_time_cost: number (reduced human cost due to automation)
 * @returns {Promise<Object>} ROI analysis
 */
export async function calculateSocialROI(costs = {}) {
  const { ai_cost = 50, human_time_cost = 2000 } = costs;

  // Get all conversions from social
  const { data, error } = await supabase
    .from('social_analytics_events')
    .select('*')
    .eq('commenter_converted', true);

  if (error) {
    console.error('Error calculating ROI:', error);
    throw error;
  }

  const totalRevenue = data.reduce((sum, e) => sum + (e.conversion_value || 0), 0);
  const totalCost = ai_cost + human_time_cost;

  return {
    total_revenue: totalRevenue,
    total_cost: totalCost,
    net_revenue: totalRevenue - totalCost,
    roi: totalCost > 0 ? ((totalRevenue - totalCost) / totalCost) * 100 : 0,
    conversions: data.length,
    avg_conversion_value: data.length > 0 ? totalRevenue / data.length : 0,
    cost_per_conversion: data.length > 0 ? totalCost / data.length : 0,

    breakdown: {
      ai_cost,
      human_time_cost,
      cost_savings: human_time_cost, // What we would have spent on manual responses
      incremental_revenue: totalRevenue // Revenue we wouldn't have gotten without automation
    }
  };
}

/**
 * Get real-time dashboard data
 *
 * @returns {Promise<Object>} Dashboard metrics
 */
export async function getDashboardMetrics() {
  const last30Days = new Date();
  last30Days.setDate(last30Days.getDate() - 30);

  const { data, error } = await supabase
    .from('social_analytics_events')
    .select('*')
    .gte('timestamp', last30Days.toISOString());

  if (error) {
    console.error('Error getting dashboard metrics:', error);
    throw error;
  }

  return {
    overview: {
      total_responses: data.length,
      total_leads_created: data.filter(e => e.lead_created).length,
      total_conversions: data.filter(e => e.commenter_converted).length,
      total_revenue: data.reduce((sum, e) => sum + (e.conversion_value || 0), 0)
    },

    rates: {
      reply_rate: data.length > 0 ? (data.filter(e => e.commenter_replied).length / data.length) * 100 : 0,
      lead_rate: data.length > 0 ? (data.filter(e => e.lead_created).length / data.length) * 100 : 0,
      conversion_rate: data.length > 0 ? (data.filter(e => e.commenter_converted).length / data.length) * 100 : 0
    },

    by_platform: {},
    by_tier: {},

    top_performers: data
      .filter(e => e.commenter_converted)
      .sort((a, b) => b.conversion_value - a.conversion_value)
      .slice(0, 5)
  };
}

export default {
  trackEvent,
  getResponsePerformance,
  comparePlatforms,
  trackABTest,
  compareFrameworks,
  calculateSocialROI,
  getDashboardMetrics
};
