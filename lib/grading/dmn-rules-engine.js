/**
 * DMN (Decision Model Notation) Rules Engine
 * Makes automated decisions based on quality scores
 *
 * Rules:
 * - What content needs rewriting?
 * - Which sequences need optimization?
 * - What processes need immediate attention?
 * - When to escalate to human?
 */

/**
 * Decision: Should content be auto-approved or needs review?
 *
 * @param {number} score - Quality score 0-100
 * @param {string} type - Content type
 * @returns {object} Decision
 */
export function decideContentApproval(score, type) {
  // Different thresholds by content type
  const thresholds = {
    email: 80,              // High bar for cold email
    review_response: 85,    // Higher bar for public responses
    sms: 75,               // Medium bar for SMS
    landing_page: 90,      // Highest bar for landing pages
    ad_copy: 85            // High bar for paid ads
  };

  const threshold = thresholds[type] || 80;

  if (score >= threshold) {
    return {
      decision: 'AUTO_APPROVE',
      action: 'send',
      reason: `Score ${score} meets threshold ${threshold}`,
      confidence: 'high'
    };
  } else if (score >= threshold - 10) {
    return {
      decision: 'REVIEW_RECOMMENDED',
      action: 'queue_for_review',
      reason: `Score ${score} is close to threshold ${threshold}. Minor improvements suggested.`,
      confidence: 'medium'
    };
  } else {
    return {
      decision: 'REJECT',
      action: 'rewrite',
      reason: `Score ${score} is below threshold ${threshold}. Significant improvements needed.`,
      confidence: 'high'
    };
  }
}

/**
 * Decision: Response time priority
 *
 * @param {object} lead - Lead information
 * @returns {object} Priority decision
 */
export function decideResponsePriority(lead) {
  const score = lead.validation_score || 0;
  const signalType = lead.signal_type || 'unknown';
  const leadAge = Date.now() - new Date(lead.created_at).getTime();
  const minutes = Math.floor(leadAge / 60000);

  // Highest priority signals (respond immediately)
  const hotSignals = ['gmb_direction', 'phone_call', 'live_chat', 'demo_request'];

  if (hotSignals.includes(signalType)) {
    return {
      priority: 'URGENT',
      target_response: '< 5 minutes',
      reason: `${signalType} is highest-intent signal`,
      escalate: minutes > 5,
      action: minutes > 5 ? 'ALERT_MANAGER' : 'IMMEDIATE_RESPONSE'
    };
  }

  // High-score leads
  if (score >= 80) {
    return {
      priority: 'HIGH',
      target_response: '< 15 minutes',
      reason: `Score ${score} = high-quality lead`,
      escalate: minutes > 15,
      action: minutes > 15 ? 'ALERT_SALES' : 'FAST_RESPONSE'
    };
  }

  // Medium-score leads
  if (score >= 60) {
    return {
      priority: 'MEDIUM',
      target_response: '< 1 hour',
      reason: `Score ${score} = qualified lead`,
      escalate: minutes > 60,
      action: 'NORMAL_RESPONSE'
    };
  }

  // Low-score leads
  return {
    priority: 'LOW',
    target_response: '< 4 hours',
    reason: `Score ${score} = nurture candidate`,
    escalate: false,
    action: 'AUTO_NURTURE_SEQUENCE'
  };
}

/**
 * Decision: Which sequence to use?
 *
 * @param {object} lead - Lead information
 * @returns {object} Sequence decision
 */
export function decideSequenceType(lead) {
  const score = lead.validation_score || 0;
  const awarenessLevel = lead.awareness_level || 'Unaware';
  const leadSource = lead.source || 'unknown';
  const hasLinkedIn = !!lead.linkedin_url;
  const hasPhone = !!lead.phone;

  // Decision tree
  if (score >= 80) {
    // High-quality lead = aggressive sequence
    if (hasLinkedIn && hasPhone) {
      return {
        sequence: 'omnichannel_aggressive',
        touches: 9,
        channels: ['email', 'linkedin', 'sms', 'call'],
        reason: 'High score + all channels available',
        estimated_conversion: '25-30%'
      };
    } else {
      return {
        sequence: 'email_aggressive',
        touches: 7,
        channels: ['email'],
        reason: 'High score but limited channels',
        estimated_conversion: '18-22%'
      };
    }
  }

  if (score >= 60) {
    // Medium quality = moderate sequence
    return {
      sequence: 'email_moderate',
      touches: 7,
      channels: ['email', hasLinkedIn ? 'linkedin' : null].filter(Boolean),
      reason: 'Medium score = steady nurture',
      estimated_conversion: '12-15%'
    };
  }

  // Low quality = gentle nurture
  return {
    sequence: 'email_gentle',
    touches: 4,
    channels: ['email'],
    reason: 'Low score = light touch nurture',
    estimated_conversion: '5-8%'
  };
}

/**
 * Decision: When to request review?
 *
 * @param {object} contact - Contact information
 * @param {object} interaction - Latest interaction
 * @returns {object} Review request decision
 */
export function decideReviewRequest(contact, interaction) {
  const satisfactionScore = interaction.satisfaction_score || contact.satisfaction_score || 0;
  const daysSinceLastReview = contact.last_review_date
    ? Math.floor((Date.now() - new Date(contact.last_review_date).getTime()) / (1000 * 60 * 60 * 24))
    : 999;

  // Already reviewed recently
  if (daysSinceLastReview < 180) {
    return {
      decision: 'SKIP',
      reason: 'Reviewed within last 6 months',
      action: 'WAIT',
      retry_after: `${180 - daysSinceLastReview} days`
    };
  }

  // Unhappy customer (low satisfaction)
  if (satisfactionScore < 7) {
    return {
      decision: 'REDIRECT_TO_FEEDBACK',
      reason: 'Low satisfaction - get private feedback first',
      action: 'SEND_FEEDBACK_SURVEY',
      escalate: satisfactionScore < 5
    };
  }

  // Happy customer (high satisfaction)
  if (satisfactionScore >= 8 || interaction.type === 'positive_milestone') {
    return {
      decision: 'REQUEST_REVIEW',
      reason: 'High satisfaction or positive moment',
      action: 'SEND_REVIEW_REQUEST',
      channel: contact.phone ? 'sms' : 'email',
      estimated_response_rate: '35-45%'
    };
  }

  // Neutral
  return {
    decision: 'WAIT',
    reason: 'Neutral satisfaction - wait for better moment',
    action: 'CONTINUE_MONITORING',
    trigger_on: 'positive_milestone or score >= 8'
  };
}

/**
 * Decision: Should negative review response be auto-published?
 *
 * @param {object} review - Review details
 * @param {string} response - Generated response
 * @param {number} responseScore - ML score of response
 * @returns {object} Publishing decision
 */
export function decideReviewResponsePublish(review, response, responseScore) {
  const rating = review.rating;

  // Check for serious complaints
  const seriousKeywords = [
    'lawsuit', 'lawyer', 'attorney', 'sue', 'scam', 'fraud',
    'theft', 'stolen', 'dangerous', 'injury', 'hurt', 'unsafe',
    'discrimination', 'harassment'
  ];

  const hasSeriousComplaint = seriousKeywords.some(keyword =>
    review.text.toLowerCase().includes(keyword)
  );

  // Never auto-publish serious complaints
  if (hasSeriousComplaint) {
    return {
      decision: 'ESCALATE_URGENT',
      action: 'ALERT_OWNER_IMMEDIATELY',
      reason: 'Serious complaint detected - requires immediate human attention',
      publish: false,
      urgency: 'CRITICAL'
    };
  }

  // 5-star reviews - auto-publish if score is good
  if (rating === 5 && responseScore >= 80) {
    return {
      decision: 'AUTO_PUBLISH',
      action: 'PUBLISH_IMMEDIATELY',
      reason: '5★ review + quality response',
      confidence: 'high'
    };
  }

  // 4-star reviews - auto-publish if score is very good
  if (rating === 4 && responseScore >= 85) {
    return {
      decision: 'AUTO_PUBLISH',
      action: 'PUBLISH_IMMEDIATELY',
      reason: '4★ review + high-quality response',
      confidence: 'high'
    };
  }

  // 3-star reviews - review first
  if (rating === 3 && responseScore >= 85) {
    return {
      decision: 'REVIEW_FIRST',
      action: 'QUEUE_FOR_REVIEW',
      reason: '3★ review - human should approve even if response quality is good',
      publish: false
    };
  }

  // 1-2 star reviews - always escalate
  if (rating <= 2) {
    return {
      decision: 'ESCALATE',
      action: 'ALERT_MANAGER',
      reason: 'Low rating requires human attention',
      publish: false,
      urgency: 'HIGH'
    };
  }

  // Default: review first
  return {
    decision: 'REVIEW_FIRST',
    action: 'QUEUE_FOR_REVIEW',
    reason: 'Safety check - human review recommended',
    publish: false
  };
}

/**
 * Decision: Test/optimization priority
 *
 * @param {array} variants - Array of {id, score, performance}
 * @returns {object} Test decision
 */
export function decideTestPriority(variants) {
  // Sort by potential improvement
  const withImprovement = variants.map(v => ({
    ...v,
    potential_lift: (100 - v.score) * (v.traffic || 1)
  })).sort((a, b) => b.potential_lift - a.potential_lift);

  const priorities = withImprovement.map((variant, index) => {
    let priority = 'LOW';
    let reason = '';

    if (variant.score < 60) {
      priority = 'URGENT';
      reason = 'Score < 60 - immediate rewrite needed';
    } else if (variant.score < 75 && variant.traffic > 100) {
      priority = 'HIGH';
      reason = 'Low score + high traffic = big opportunity';
    } else if (variant.score < 85) {
      priority = 'MEDIUM';
      reason = 'Room for improvement';
    } else {
      priority = 'LOW';
      reason = 'Score is good, focus elsewhere';
    }

    return {
      id: variant.id,
      priority,
      reason,
      potential_lift: variant.potential_lift,
      recommended_action: variant.score < 70 ? 'REWRITE' : 'A/B_TEST',
      rank: index + 1
    };
  });

  return {
    priorities,
    next_test: priorities[0],
    estimated_impact: priorities[0] ? `+${Math.round(priorities[0].potential_lift * 0.1)}% conversion` : 'N/A'
  };
}

/**
 * Decision: Daily test suite pass/fail
 *
 * @param {object} results - Daily test results
 * @returns {object} System health decision
 */
export function decideSystemHealth(results) {
  const scores = {
    copywriting: results.copywriting_avg || 0,
    sequences: results.sequences_avg || 0,
    reputation: results.reputation_avg || 0,
    response_time: results.response_time_avg || 0,
    conversion: results.conversion_rate || 0
  };

  // Calculate weighted health score
  const healthScore =
    (scores.copywriting * 0.25) +
    (scores.sequences * 0.25) +
    (scores.reputation * 0.20) +
    (scores.response_time * 0.15) +
    (scores.conversion * 0.15);

  let status = 'HEALTHY';
  let actions = [];
  let alerts = [];

  // Critical thresholds
  if (healthScore < 60) {
    status = 'CRITICAL';
    alerts.push('OVERALL SYSTEM HEALTH BELOW 60%');
  } else if (healthScore < 75) {
    status = 'WARNING';
    alerts.push('System health declining');
  } else if (healthScore >= 90) {
    status = 'EXCELLENT';
  }

  // Individual component checks
  if (scores.copywriting < 70) {
    actions.push({
      priority: 'HIGH',
      component: 'copywriting',
      action: 'REWRITE_LOW_SCORING_EMAILS',
      threshold: 70,
      current: scores.copywriting
    });
  }

  if (scores.sequences < 70) {
    actions.push({
      priority: 'HIGH',
      component: 'sequences',
      action: 'OPTIMIZE_FOLLOW_UP_SEQUENCES',
      threshold: 70,
      current: scores.sequences
    });
  }

  if (scores.reputation < 80) {
    actions.push({
      priority: 'MEDIUM',
      component: 'reputation',
      action: 'INCREASE_REVIEW_REQUESTS',
      threshold: 80,
      current: scores.reputation
    });
  }

  if (scores.response_time < 80) {
    actions.push({
      priority: 'HIGH',
      component: 'response_time',
      action: 'IMPROVE_RESPONSE_SPEED',
      threshold: 80,
      current: scores.response_time
    });
  }

  if (scores.conversion < 15) {
    actions.push({
      priority: 'URGENT',
      component: 'conversion',
      action: 'RUN_CONVERSION_OPTIMIZATION_TESTS',
      threshold: 15,
      current: scores.conversion
    });
  }

  return {
    status,
    healthScore: Math.round(healthScore),
    letterGrade: getLetterGrade(healthScore),
    scores,
    actions: actions.sort((a, b) => priorityWeight(b.priority) - priorityWeight(a.priority)),
    alerts,
    recommendation: getHealthRecommendation(status, healthScore)
  };
}

function priorityWeight(priority) {
  const weights = {
    URGENT: 4,
    HIGH: 3,
    MEDIUM: 2,
    LOW: 1
  };
  return weights[priority] || 0;
}

function getLetterGrade(score) {
  if (score >= 95) return 'A+';
  if (score >= 90) return 'A';
  if (score >= 85) return 'A-';
  if (score >= 80) return 'B+';
  if (score >= 75) return 'B';
  if (score >= 70) return 'B-';
  if (score >= 65) return 'C+';
  if (score >= 60) return 'C';
  if (score >= 55) return 'C-';
  if (score >= 50) return 'D';
  return 'F';
}

function getHealthRecommendation(status, score) {
  if (status === 'CRITICAL') {
    return 'IMMEDIATE ACTION REQUIRED: Multiple systems below threshold. Focus on highest-priority actions first.';
  }
  if (status === 'WARNING') {
    return 'Optimization needed: System is functional but has room for improvement. Address medium/high priority items.';
  }
  if (status === 'HEALTHY') {
    return 'System performing well: Continue monitoring and run periodic tests to maintain quality.';
  }
  if (status === 'EXCELLENT') {
    return 'System performing at world-class level: Focus on scaling and advanced optimizations.';
  }
  return 'Continue monitoring system health.';
}

/**
 * Execute decision rule
 *
 * @param {string} ruleType - Type of decision
 * @param {object} input - Input data
 * @returns {object} Decision
 */
export function executeRule(ruleType, input) {
  switch (ruleType) {
    case 'content_approval':
      return decideContentApproval(input.score, input.type);

    case 'response_priority':
      return decideResponsePriority(input.lead);

    case 'sequence_type':
      return decideSequenceType(input.lead);

    case 'review_request':
      return decideReviewRequest(input.contact, input.interaction);

    case 'review_response_publish':
      return decideReviewResponsePublish(input.review, input.response, input.responseScore);

    case 'test_priority':
      return decideTestPriority(input.variants);

    case 'system_health':
      return decideSystemHealth(input.results);

    default:
      throw new Error(`Unknown rule type: ${ruleType}`);
  }
}

export default {
  decideContentApproval,
  decideResponsePriority,
  decideSequenceType,
  decideReviewRequest,
  decideReviewResponsePublish,
  decideTestPriority,
  decideSystemHealth,
  executeRule
};
