/**
 * SOCIAL LEAD SCORER
 *
 * Purpose: Score social media commenters/engagers as potential leads
 * Different formula than regular lead scoring (optimized for social signals)
 *
 * Scoring Criteria:
 * 1. Engagement Depth (0-40 points)
 * 2. Profile Quality/ICP Match (0-30 points)
 * 3. Buying Intent Signals (0-30 points)
 *
 * Tiers:
 * - HOT (75-100): Immediate DM, high conversion potential
 * - WARM (60-74): Engage + nurture sequence
 * - COOL (40-59): Brand awareness, light touch
 * - COLD (0-39): Minimal engagement
 */

/**
 * Score social media commenter/engager as potential lead
 *
 * @param {Object} engagementData
 *   - comment_text: string (what they said)
 *   - engagement_type: "comment" | "dm" | "share" | "tag" | "save"
 *   - engagement_history: Array of previous engagements
 * @param {Object} profileData
 *   - name: string
 *   - bio: string
 *   - location: string
 *   - company: string
 *   - follower_count: number
 *   - following_count: number
 *   - post_count: number
 * @param {Object} behavioralData
 *   - time_on_profile: number (seconds)
 *   - pages_visited: Array
 *   - links_clicked: Array
 *   - form_interactions: Array
 *
 * @returns {Object} Lead score and tier
 */
export function scoreSocialLead(engagementData, profileData, behavioralData = {}) {
  let score = 0;
  const breakdown = {
    engagement_depth: 0,
    profile_quality: 0,
    buying_intent: 0,
    bonus_points: 0
  };

  // ===== ENGAGEMENT DEPTH (0-40 points) =====

  const { comment_text, engagement_type, engagement_history = [] } = engagementData;

  // Comment length and quality
  if (comment_text) {
    const wordCount = comment_text.split(/\s+/).length;

    if (wordCount >= 20) {
      breakdown.engagement_depth += 20; // Detailed, thoughtful comment
    } else if (wordCount >= 10) {
      breakdown.engagement_depth += 15; // Decent comment
    } else if (wordCount >= 5) {
      breakdown.engagement_depth += 10; // Short comment
    } else if (wordCount >= 2) {
      breakdown.engagement_depth += 5; // Very short (e.g., "Great post!")
    }

    // Question asked? (High engagement signal)
    if (comment_text.includes('?')) {
      breakdown.engagement_depth += 10;
    }
  }

  // Engagement type value
  const engagementTypeScores = {
    'dm': 20,           // Direct message = highest intent
    'comment': 15,      // Comment = high intent
    'tag': 12,          // Tagged someone = spreading awareness
    'share': 10,        // Shared post
    'save': 8,          // Saved for later
    'like': 2           // Low intent
  };

  breakdown.engagement_depth += engagementTypeScores[engagement_type] || 0;

  // Engagement frequency (repeat engager = higher intent)
  if (engagement_history.length >= 5) {
    breakdown.engagement_depth += 10; // Very engaged (5+ interactions)
  } else if (engagement_history.length >= 3) {
    breakdown.engagement_depth += 7;  // Regular engager
  } else if (engagement_history.length >= 2) {
    breakdown.engagement_depth += 4;  // Repeat engager
  }

  // Cap engagement depth at 40
  breakdown.engagement_depth = Math.min(breakdown.engagement_depth, 40);

  // ===== PROFILE QUALITY / ICP MATCH (0-30 points) =====

  const { bio = '', location = '', company = '', follower_count = 0 } = profileData;

  // ICP keywords (customize for your target market)
  const icpKeywords = {
    high_value: ['gym owner', 'fitness center', 'personal trainer', 'crossfit', 'pilates', 'yoga studio', 'martial arts', 'boxing gym', 'ceo', 'founder', 'owner', 'director'],
    medium_value: ['fitness', 'health', 'wellness', 'trainer', 'coach', 'instructor', 'manager', 'marketing', 'sales'],
    low_value: ['enthusiast', 'lover', 'fan', 'student']
  };

  const lowerBio = bio.toLowerCase();
  const lowerCompany = company.toLowerCase();
  const combined = `${lowerBio} ${lowerCompany} ${location.toLowerCase()}`;

  // Check for high-value ICP match
  if (icpKeywords.high_value.some(keyword => combined.includes(keyword))) {
    breakdown.profile_quality += 30; // Perfect ICP match
  } else if (icpKeywords.medium_value.some(keyword => combined.includes(keyword))) {
    breakdown.profile_quality += 20; // Related industry
  } else if (icpKeywords.low_value.some(keyword => combined.includes(keyword))) {
    breakdown.profile_quality += 10; // Some relevance
  } else {
    breakdown.profile_quality += 5; // Generic profile
  }

  // Follower count (authority/influence)
  if (follower_count >= 10000) {
    breakdown.profile_quality += 5; // Influencer (bonus for reach)
  } else if (follower_count >= 1000) {
    breakdown.profile_quality += 3; // Micro-influencer
  }

  // Location match (if targeting specific geo)
  const targetLocations = ['usa', 'united states', 'canada', 'uk', 'australia'];
  if (targetLocations.some(loc => location.toLowerCase().includes(loc))) {
    breakdown.profile_quality += 5;
  }

  // Cap profile quality at 30
  breakdown.profile_quality = Math.min(breakdown.profile_quality, 30);

  // ===== BUYING INTENT SIGNALS (0-30 points) =====

  if (comment_text) {
    const lowerComment = comment_text.toLowerCase();

    // High-intent keywords
    const highIntentKeywords = [
      'price', 'pricing', 'cost', 'how much',
      'buy', 'purchase', 'get started', 'sign up',
      'trial', 'demo', 'book', 'schedule',
      'interested', 'looking for', 'need', 'want',
      'budget', 'timeline', 'when can', 'how soon'
    ];

    const matchedIntentKeywords = highIntentKeywords.filter(keyword =>
      lowerComment.includes(keyword)
    );

    // Score based on number of intent keywords
    if (matchedIntentKeywords.length >= 3) {
      breakdown.buying_intent += 30; // Very high intent
    } else if (matchedIntentKeywords.length === 2) {
      breakdown.buying_intent += 25; // High intent
    } else if (matchedIntentKeywords.length === 1) {
      breakdown.buying_intent += 20; // Medium intent
    }

    // Competitor mentions (comparing options = buying mode)
    const competitorMentions = ['hubspot', 'salesforce', 'mailchimp', 'activecampaign'];
    if (competitorMentions.some(comp => lowerComment.includes(comp))) {
      breakdown.buying_intent += 10; // Evaluating options
    }

    // Urgency indicators
    const urgencyKeywords = ['now', 'asap', 'urgent', 'immediately', 'today', 'this week'];
    if (urgencyKeywords.some(keyword => lowerComment.includes(keyword))) {
      breakdown.buying_intent += 10; // Immediate need
    }
  }

  // Behavioral signals (website activity)
  if (behavioralData.time_on_profile && behavioralData.time_on_profile > 120) {
    breakdown.buying_intent += 10; // Spent 2+ minutes on profile/site
  }

  if (behavioralData.pages_visited && behavioralData.pages_visited.includes('pricing')) {
    breakdown.buying_intent += 15; // Viewed pricing page
  }

  if (behavioralData.links_clicked && behavioralData.links_clicked.length > 0) {
    breakdown.buying_intent += 10; // Clicked links (high engagement)
  }

  // Cap buying intent at 30
  breakdown.buying_intent = Math.min(breakdown.buying_intent, 30);

  // ===== BONUS POINTS (Special cases) =====

  // Tagged others (spreading awareness = evangelist potential)
  if (comment_text && comment_text.includes('@')) {
    breakdown.bonus_points += 5;
  }

  // Mentioned specific pain point
  const painPoints = ['struggling with', 'challenge', 'problem', 'issue', 'difficulty', 'hard to', 'can\'t figure out'];
  if (comment_text && painPoints.some(pain => comment_text.toLowerCase().includes(pain))) {
    breakdown.bonus_points += 10; // Expressed pain = high conversion potential
  }

  // Asked "how to get started" (clear buying signal)
  if (comment_text && /how (to|do i|can i) (get started|begin|start|sign up)/i.test(comment_text)) {
    breakdown.bonus_points += 15; // Ready to buy
  }

  // ===== TOTAL SCORE =====

  score = breakdown.engagement_depth + breakdown.profile_quality + breakdown.buying_intent + breakdown.bonus_points;

  // Determine tier
  let tier;
  if (score >= 75) {
    tier = 'HOT';
  } else if (score >= 60) {
    tier = 'WARM';
  } else if (score >= 40) {
    tier = 'COOL';
  } else {
    tier = 'COLD';
  }

  return {
    score: Math.min(score, 100), // Cap at 100
    tier,
    breakdown,
    recommended_action: getRecommendedAction(tier),
    conversion_probability: estimateConversionProbability(score)
  };
}

/**
 * Get recommended action based on tier
 */
function getRecommendedAction(tier) {
  const actions = {
    HOT: {
      action: 'IMMEDIATE_DM',
      message_type: 'Personalized offer with clear CTA',
      timeline: 'Send within 5 minutes',
      workflow: 'hot_social_lead_sequence',
      expected_conversion: '25-40%'
    },
    WARM: {
      action: 'ENGAGE_AND_NURTURE',
      message_type: 'Helpful response + soft CTA',
      timeline: 'Respond within 30 minutes',
      workflow: 'warm_social_nurture',
      expected_conversion: '10-20%'
    },
    COOL: {
      action: 'BRAND_AWARENESS',
      message_type: 'Educational content + follow',
      timeline: 'Respond within 24 hours',
      workflow: 'cool_social_awareness',
      expected_conversion: '3-8%'
    },
    COLD: {
      action: 'MINIMAL_ENGAGEMENT',
      message_type: 'Simple acknowledgment or no response',
      timeline: 'No urgency',
      workflow: null,
      expected_conversion: '0-2%'
    }
  };

  return actions[tier];
}

/**
 * Estimate conversion probability based on score
 */
function estimateConversionProbability(score) {
  if (score >= 90) return 0.40; // 40%
  if (score >= 80) return 0.35; // 35%
  if (score >= 75) return 0.30; // 30%
  if (score >= 70) return 0.25; // 25%
  if (score >= 65) return 0.20; // 20%
  if (score >= 60) return 0.15; // 15%
  if (score >= 50) return 0.10; // 10%
  if (score >= 40) return 0.05; // 5%
  return 0.02; // 2%
}

/**
 * Batch score multiple social engagers
 */
export function batchScoreSocialLeads(engagers) {
  return engagers.map(engager => ({
    name: engager.profileData.name,
    ...scoreSocialLead(engager.engagementData, engager.profileData, engager.behavioralData)
  })).sort((a, b) => b.score - a.score); // Sort by score descending
}

/**
 * Get scoring insights (what's working, what's not)
 */
export function analyzeScoring(scoredLeads) {
  const insights = {
    total_scored: scoredLeads.length,
    by_tier: {
      HOT: scoredLeads.filter(l => l.tier === 'HOT').length,
      WARM: scoredLeads.filter(l => l.tier === 'WARM').length,
      COOL: scoredLeads.filter(l => l.tier === 'COOL').length,
      COLD: scoredLeads.filter(l => l.tier === 'COLD').length
    },
    avg_score: scoredLeads.reduce((sum, l) => sum + l.score, 0) / scoredLeads.length,
    score_distribution: {
      '90-100': scoredLeads.filter(l => l.score >= 90).length,
      '80-89': scoredLeads.filter(l => l.score >= 80 && l.score < 90).length,
      '70-79': scoredLeads.filter(l => l.score >= 70 && l.score < 80).length,
      '60-69': scoredLeads.filter(l => l.score >= 60 && l.score < 70).length,
      '50-59': scoredLeads.filter(l => l.score >= 50 && l.score < 60).length,
      '0-49': scoredLeads.filter(l => l.score < 50).length
    },
    top_engagement_sources: getTopSources(scoredLeads, 'engagement_depth'),
    top_profile_matches: getTopSources(scoredLeads, 'profile_quality'),
    top_buying_intent: getTopSources(scoredLeads, 'buying_intent')
  };

  return insights;
}

/**
 * Helper: Get top sources for a breakdown category
 */
function getTopSources(scoredLeads, category) {
  return scoredLeads
    .map(l => ({ name: l.name, score: l.breakdown[category] }))
    .sort((a, b) => b.score - a.score)
    .slice(0, 10);
}

export default {
  scoreSocialLead,
  batchScoreSocialLeads,
  analyzeScoring
};
