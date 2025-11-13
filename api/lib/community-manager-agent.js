/**
 * COMMUNITY MANAGER AGENT
 *
 * Purpose: Identify and nurture top community members, brand advocates, and ambassadors
 *
 * Features:
 * 1. Top commenter identification (5+ quality interactions)
 * 2. Brand advocate detection (shares, tags, positive sentiment)
 * 3. Super-user scoring (engagement + influence + advocacy)
 * 4. Ambassador program eligibility
 * 5. Community health metrics
 * 6. Reward/recognition recommendations
 */

/**
 * Analyze community member engagement and value
 *
 * @param {Object} memberData
 *   - name: string
 *   - profile: Object (social profile data)
 *   - engagement_history: Array of interactions
 *   - sentiment_history: Array of sentiment scores
 *   - referrals: number (how many people they've referred)
 * @returns {Object} Community value analysis
 */
export function analyzeCommunityMember(memberData) {
  const {
    name,
    profile = {},
    engagement_history = [],
    sentiment_history = [],
    referrals = 0
  } = memberData;

  let score = 0;
  const breakdown = {
    engagement_frequency: 0,      // 0-30 points
    engagement_quality: 0,         // 0-25 points
    advocacy_impact: 0,            // 0-25 points
    influence_reach: 0,            // 0-20 points
  };

  // ===== ENGAGEMENT FREQUENCY (0-30 points) =====

  const engagementCount = engagement_history.length;

  if (engagementCount >= 20) {
    breakdown.engagement_frequency = 30; // Super engaged
  } else if (engagementCount >= 10) {
    breakdown.engagement_frequency = 25; // Very engaged
  } else if (engagementCount >= 5) {
    breakdown.engagement_frequency = 20; // Engaged
  } else if (engagementCount >= 3) {
    breakdown.engagement_frequency = 15; // Regular
  } else if (engagementCount >= 1) {
    breakdown.engagement_frequency = 10; // Occasional
  }

  // Engagement recency bonus
  const lastEngagement = engagement_history[engagement_history.length - 1];
  if (lastEngagement) {
    const daysSinceLastEngagement = Math.floor(
      (Date.now() - new Date(lastEngagement.timestamp).getTime()) / (1000 * 60 * 60 * 24)
    );

    if (daysSinceLastEngagement <= 7) {
      breakdown.engagement_frequency += 5; // Engaged within last week
    }
  }

  breakdown.engagement_frequency = Math.min(breakdown.engagement_frequency, 30);

  // ===== ENGAGEMENT QUALITY (0-25 points) =====

  // Detailed comments (not just emoji/short replies)
  const detailedComments = engagement_history.filter(e =>
    e.type === 'comment' && e.content && e.content.split(/\s+/).length >= 10
  );

  breakdown.engagement_quality += Math.min(detailedComments.length * 3, 15);

  // Questions asked (shows deep interest)
  const questions = engagement_history.filter(e =>
    e.content && e.content.includes('?')
  );

  breakdown.engagement_quality += Math.min(questions.length * 2, 10);

  breakdown.engagement_quality = Math.min(breakdown.engagement_quality, 25);

  // ===== ADVOCACY IMPACT (0-25 points) =====

  // Shares (spreading awareness)
  const shares = engagement_history.filter(e => e.type === 'share');
  breakdown.advocacy_impact += Math.min(shares.length * 5, 15);

  // Tags others (bringing new people in)
  const tags = engagement_history.filter(e =>
    e.content && e.content.includes('@')
  );
  breakdown.advocacy_impact += Math.min(tags.length * 3, 10);

  // Referrals (actual conversions)
  breakdown.advocacy_impact += Math.min(referrals * 10, 20);

  // Positive sentiment (brand advocate)
  const avgSentiment = sentiment_history.length > 0
    ? sentiment_history.reduce((sum, s) => sum + s, 0) / sentiment_history.length
    : 0;

  if (avgSentiment >= 0.8) {
    breakdown.advocacy_impact += 15; // Consistently positive
  } else if (avgSentiment >= 0.6) {
    breakdown.advocacy_impact += 10; // Mostly positive
  } else if (avgSentiment >= 0.4) {
    breakdown.advocacy_impact += 5; // Neutral
  }

  breakdown.advocacy_impact = Math.min(breakdown.advocacy_impact, 25);

  // ===== INFLUENCE REACH (0-20 points) =====

  const followerCount = profile.follower_count || 0;

  if (followerCount >= 100000) {
    breakdown.influence_reach = 20; // Macro-influencer
  } else if (followerCount >= 10000) {
    breakdown.influence_reach = 15; // Micro-influencer
  } else if (followerCount >= 1000) {
    breakdown.influence_reach = 10; // Growing audience
  } else if (followerCount >= 500) {
    breakdown.influence_reach = 5; // Small audience
  }

  breakdown.influence_reach = Math.min(breakdown.influence_reach, 20);

  // ===== TOTAL SCORE =====

  score = Object.values(breakdown).reduce((sum, val) => sum + val, 0);

  // Determine member tier
  let tier, status;
  if (score >= 75) {
    tier = 'SUPER_USER';
    status = 'Ambassador Program Eligible';
  } else if (score >= 60) {
    tier = 'BRAND_ADVOCATE';
    status = 'Recognition Worthy';
  } else if (score >= 40) {
    tier = 'ACTIVE_MEMBER';
    status = 'Nurture for Advocacy';
  } else if (score >= 20) {
    tier = 'CASUAL_MEMBER';
    status = 'Standard Engagement';
  } else {
    tier = 'LURKER';
    status = 'Encourage Participation';
  }

  return {
    name,
    score,
    tier,
    status,
    breakdown,
    recommendations: getRecommendations(tier, breakdown, profile)
  };
}

/**
 * Get recommendations based on member tier
 */
function getRecommendations(tier, breakdown, profile) {
  const recommendations = {
    actions: [],
    rewards: [],
    engagement_strategy: ''
  };

  if (tier === 'SUPER_USER') {
    recommendations.actions = [
      'Invite to Ambassador Program (exclusive access, referral commission)',
      'Feature their content/testimonial in marketing',
      'Offer early access to new features',
      'Invite to customer advisory board',
      'Send personalized thank you gift'
    ];
    recommendations.rewards = [
      'Free premium account (lifetime)',
      '30% commission on referrals',
      'Exclusive swag/merchandise',
      'Public recognition (social shoutout)'
    ];
    recommendations.engagement_strategy = 'Treat as VIP partner. Regular check-ins, exclusive insights, co-create content.';

  } else if (tier === 'BRAND_ADVOCATE') {
    recommendations.actions = [
      'Send personalized thank you message',
      'Share their positive comments on social',
      'Offer referral incentive (20% commission)',
      'Invite to exclusive webinar/event',
      'Ask for testimonial/case study'
    ];
    recommendations.rewards = [
      'Free month of service',
      'Branded swag',
      '20% referral commission',
      'Priority support'
    ];
    recommendations.engagement_strategy = 'Nurture toward super-user status. Encourage referrals and testimonials.';

  } else if (tier === 'ACTIVE_MEMBER') {
    recommendations.actions = [
      'Acknowledge their engagement (reply to comments)',
      'Invite to community events',
      'Offer helpful resources',
      'Ask for feedback on features',
      'Encourage sharing/tagging'
    ];
    recommendations.rewards = [
      'Discount code (10% off)',
      'Access to exclusive content',
      'Community badge/recognition'
    ];
    recommendations.engagement_strategy = 'Build relationship through value-add. Encourage more sharing and advocacy.';

  } else if (tier === 'CASUAL_MEMBER') {
    recommendations.actions = [
      'Continue engagement (respond to comments)',
      'Share educational content',
      'Encourage questions/interaction',
      'Invite to community challenges'
    ];
    recommendations.rewards = [
      'Entry into monthly giveaway',
      'Access to free resources'
    ];
    recommendations.engagement_strategy = 'Increase engagement frequency. Provide value to build trust.';

  } else {
    // LURKER
    recommendations.actions = [
      'Encourage first comment/interaction',
      'Share interesting content to spark engagement',
      'Run community challenge/contest',
      'Ask open-ended questions'
    ];
    recommendations.rewards = [];
    recommendations.engagement_strategy = 'Lower barrier to participation. Make first engagement easy and rewarding.';
  }

  return recommendations;
}

/**
 * Identify top community members from a list
 *
 * @param {Array<Object>} members - Array of member data
 * @param {number} topN - Number of top members to return
 * @returns {Array<Object>} Top community members sorted by score
 */
export function getTopCommunityMembers(members, topN = 10) {
  return members
    .map(member => analyzeCommunityMember(member))
    .sort((a, b) => b.score - a.score)
    .slice(0, topN);
}

/**
 * Calculate community health metrics
 *
 * @param {Array<Object>} members - All community members
 * @returns {Object} Community health analysis
 */
export function calculateCommunityHealth(members) {
  const analyzed = members.map(m => analyzeCommunityMember(m));

  const health = {
    total_members: members.length,
    by_tier: {
      SUPER_USER: analyzed.filter(m => m.tier === 'SUPER_USER').length,
      BRAND_ADVOCATE: analyzed.filter(m => m.tier === 'BRAND_ADVOCATE').length,
      ACTIVE_MEMBER: analyzed.filter(m => m.tier === 'ACTIVE_MEMBER').length,
      CASUAL_MEMBER: analyzed.filter(m => m.tier === 'CASUAL_MEMBER').length,
      LURKER: analyzed.filter(m => m.tier === 'LURKER').length
    },
    engagement_metrics: {
      avg_score: analyzed.reduce((sum, m) => sum + m.score, 0) / analyzed.length,
      engaged_percentage: (analyzed.filter(m => m.score >= 40).length / analyzed.length) * 100,
      advocate_percentage: (analyzed.filter(m => m.score >= 60).length / analyzed.length) * 100
    },
    health_score: 0,
    health_status: '',
    trends: {
      growing: 'UNKNOWN',
      engagement_increasing: 'UNKNOWN',
      advocacy_increasing: 'UNKNOWN'
    }
  };

  // Calculate overall health score (0-100)
  const advocateRatio = health.by_tier.BRAND_ADVOCATE / health.total_members;
  const superUserRatio = health.by_tier.SUPER_USER / health.total_members;
  const lurkerRatio = health.by_tier.LURKER / health.total_members;

  health.health_score = Math.round(
    (superUserRatio * 40) +
    (advocateRatio * 30) +
    (health.engagement_metrics.engaged_percentage * 0.2) +
    ((1 - lurkerRatio) * 10)
  );

  // Health status
  if (health.health_score >= 75) {
    health.health_status = 'EXCELLENT - Thriving community with strong advocacy';
  } else if (health.health_score >= 60) {
    health.health_status = 'GOOD - Healthy engagement, room for more advocates';
  } else if (health.health_score >= 40) {
    health.health_status = 'FAIR - Needs more engagement and advocacy programs';
  } else {
    health.health_status = 'POOR - Low engagement, focus on activation';
  }

  return health;
}

/**
 * Generate ambassador program invitations
 *
 * @param {Array<Object>} members - Community members
 * @returns {Array<Object>} Members eligible for ambassador program
 */
export function getAmbassadorCandidates(members) {
  return members
    .map(m => analyzeCommunityMember(m))
    .filter(m => m.tier === 'SUPER_USER' || (m.tier === 'BRAND_ADVOCATE' && m.score >= 70))
    .sort((a, b) => b.score - a.score)
    .map(m => ({
      name: m.name,
      score: m.score,
      tier: m.tier,
      why_eligible: `Score: ${m.score}/100. ${m.breakdown.advocacy_impact >= 20 ? 'Strong advocacy impact. ' : ''}${m.breakdown.influence_reach >= 15 ? 'Significant reach. ' : ''}${m.breakdown.engagement_frequency >= 25 ? 'Highly engaged.' : ''}`,
      proposed_offer: {
        commission_rate: m.score >= 85 ? '30%' : '20%',
        perks: m.score >= 85
          ? ['Lifetime premium account', 'Exclusive swag', 'Co-marketing opportunities', 'Advisory board seat']
          : ['Free premium account', 'Branded swag', 'Priority support', 'Referral bonus']
      }
    }));
}

/**
 * Monitor community sentiment trends
 *
 * @param {Array<Object>} sentimentData - Historical sentiment data
 * @returns {Object} Trend analysis
 */
export function analyzeSentimentTrends(sentimentData) {
  // Group by time period (weekly)
  const weeks = {};

  sentimentData.forEach(s => {
    const date = new Date(s.timestamp);
    const weekKey = `${date.getFullYear()}-W${Math.ceil(date.getDate() / 7)}`;

    if (!weeks[weekKey]) {
      weeks[weekKey] = [];
    }

    weeks[weekKey].push(s.sentiment_score);
  });

  // Calculate averages
  const weeklyAverages = Object.entries(weeks).map(([week, scores]) => ({
    week,
    avg_sentiment: scores.reduce((sum, s) => sum + s, 0) / scores.length
  }));

  // Determine trend
  let trend = 'STABLE';
  if (weeklyAverages.length >= 2) {
    const recent = weeklyAverages[weeklyAverages.length - 1].avg_sentiment;
    const previous = weeklyAverages[weeklyAverages.length - 2].avg_sentiment;

    if (recent > previous + 0.1) {
      trend = 'IMPROVING';
    } else if (recent < previous - 0.1) {
      trend = 'DECLINING';
    }
  }

  return {
    weekly_averages: weeklyAverages,
    current_sentiment: weeklyAverages[weeklyAverages.length - 1]?.avg_sentiment || 0,
    trend,
    recommendation: trend === 'DECLINING'
      ? 'Address community concerns. Increase engagement and support.'
      : trend === 'IMPROVING'
      ? 'Capitalize on positive momentum. Feature success stories.'
      : 'Maintain current engagement level. Monitor for changes.'
  };
}

export default {
  analyzeCommunityMember,
  getTopCommunityMembers,
  calculateCommunityHealth,
  getAmbassadorCandidates,
  analyzeSentimentTrends
};
