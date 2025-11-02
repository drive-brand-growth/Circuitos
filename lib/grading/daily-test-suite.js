/**
 * Daily Test Suite
 * Automated quality checks that run daily to grade system performance
 *
 * Tests:
 * - Email copy quality (sample recent emails)
 * - Sequence effectiveness
 * - Review response quality
 * - Response time compliance
 * - Conversion rates
 * - System health
 */

import { scoreEmailCopy, scoreSequence, scoreReviewResponse } from './ml-quality-scorer.js';
import { executeRule } from './dmn-rules-engine.js';

/**
 * Run full daily test suite
 *
 * @param {object} systemData - Data from last 24 hours
 * @returns {object} Complete test results
 */
export async function runDailyTests(systemData) {
  console.log('[Daily Tests] Starting daily quality check...');

  const startTime = Date.now();

  const results = {
    testDate: new Date().toISOString(),
    tests: {},
    overallGrade: 0,
    letterGrade: 'F',
    status: 'UNKNOWN',
    actions: [],
    duration: 0
  };

  try {
    // Test 1: Email Copy Quality
    console.log('[Daily Tests] Testing email copy quality...');
    results.tests.emailCopy = await testEmailCopyQuality(systemData.recentEmails || []);

    // Test 2: Sequence Effectiveness
    console.log('[Daily Tests] Testing sequence effectiveness...');
    results.tests.sequences = await testSequenceEffectiveness(systemData.sequences || []);

    // Test 3: Review Response Quality
    console.log('[Daily Tests] Testing review response quality...');
    results.tests.reviewResponses = await testReviewResponseQuality(systemData.reviewResponses || []);

    // Test 4: Response Time
    console.log('[Daily Tests] Testing response time...');
    results.tests.responseTime = testResponseTime(systemData.leads || []);

    // Test 5: Follow-Up Consistency
    console.log('[Daily Tests] Testing follow-up consistency...');
    results.tests.followUpConsistency = testFollowUpConsistency(systemData.leads || []);

    // Test 6: Reputation Metrics
    console.log('[Daily Tests] Testing reputation metrics...');
    results.tests.reputation = testReputationMetrics(systemData.reviews || []);

    // Test 7: Conversion Rate
    console.log('[Daily Tests] Testing conversion rate...');
    results.tests.conversion = testConversionRate(systemData.leads || []);

    // Calculate overall health
    results.overallHealth = calculateOverallHealth(results.tests);
    results.overallGrade = results.overallHealth.healthScore;
    results.letterGrade = results.overallHealth.letterGrade;
    results.status = results.overallHealth.status;
    results.actions = results.overallHealth.actions;

    results.duration = Date.now() - startTime;

    console.log(`[Daily Tests] Complete! Overall Grade: ${results.letterGrade} (${results.overallGrade})`);

    return results;

  } catch (error) {
    console.error('[Daily Tests] Error:', error.message);
    results.error = error.message;
    results.duration = Date.now() - startTime;
    return results;
  }
}

/**
 * Test 1: Email Copy Quality
 * Sample recent emails and grade them
 */
async function testEmailCopyQuality(recentEmails) {
  if (recentEmails.length === 0) {
    return {
      score: 0,
      tested: 0,
      passed: 0,
      failed: 0,
      message: 'No emails to test'
    };
  }

  // Sample up to 10 random emails
  const sample = recentEmails.slice(0, Math.min(10, recentEmails.length));
  const scores = [];

  for (const email of sample) {
    try {
      const score = await scoreEmailCopy(
        `SUBJECT: ${email.subject}\n\nBODY:\n${email.body}`,
        email.context || {}
      );
      scores.push(score.overallScore);

      // Wait to avoid rate limiting
      await new Promise(resolve => setTimeout(resolve, 500));
    } catch (error) {
      console.error('[Daily Tests] Email scoring error:', error.message);
    }
  }

  const avgScore = scores.length > 0
    ? scores.reduce((sum, s) => sum + s, 0) / scores.length
    : 0;

  return {
    score: Math.round(avgScore),
    tested: sample.length,
    passed: scores.filter(s => s >= 80).length,
    failed: scores.filter(s => s < 70).length,
    scores: scores,
    threshold: 80,
    passingRate: scores.length > 0 ? (scores.filter(s => s >= 80).length / scores.length * 100).toFixed(1) : 0
  };
}

/**
 * Test 2: Sequence Effectiveness
 */
async function testSequenceEffectiveness(sequences) {
  if (sequences.length === 0) {
    return {
      score: 0,
      tested: 0,
      message: 'No sequences to test'
    };
  }

  const results = {
    avgTouches: 0,
    avgConversionRate: 0,
    channelDiversity: 0,
    score: 0
  };

  // Analyze sequence structure
  const touchCounts = sequences.map(s => s.touches?.length || 0);
  results.avgTouches = touchCounts.reduce((sum, t) => sum + t, 0) / touchCounts.length;

  // Conversion rates
  const conversionRates = sequences
    .filter(s => s.performance?.conversion_rate)
    .map(s => s.performance.conversion_rate);

  results.avgConversionRate = conversionRates.length > 0
    ? conversionRates.reduce((sum, r) => sum + r, 0) / conversionRates.length
    : 0;

  // Channel diversity
  const channelsUsed = new Set();
  sequences.forEach(s => {
    s.touches?.forEach(t => channelsUsed.add(t.channel));
  });
  results.channelDiversity = channelsUsed.size;

  // Calculate score
  let score = 0;

  // Touch count scoring (0-40 points)
  if (results.avgTouches >= 12) score += 40;
  else if (results.avgTouches >= 7) score += 30;
  else if (results.avgTouches >= 5) score += 20;
  else score += 10;

  // Conversion rate scoring (0-40 points)
  if (results.avgConversionRate >= 0.25) score += 40;
  else if (results.avgConversionRate >= 0.18) score += 30;
  else if (results.avgConversionRate >= 0.12) score += 20;
  else score += 10;

  // Channel diversity scoring (0-20 points)
  if (results.channelDiversity >= 4) score += 20;
  else if (results.channelDiversity >= 3) score += 15;
  else if (results.channelDiversity >= 2) score += 10;
  else score += 5;

  results.score = score;
  results.tested = sequences.length;

  return results;
}

/**
 * Test 3: Review Response Quality
 */
async function testReviewResponseQuality(reviewResponses) {
  if (reviewResponses.length === 0) {
    return {
      score: 0,
      tested: 0,
      message: 'No review responses to test'
    };
  }

  const sample = reviewResponses.slice(0, Math.min(5, reviewResponses.length));
  const scores = [];

  for (const item of sample) {
    try {
      const score = await scoreReviewResponse(item.review, item.response);
      scores.push(score.overallScore);

      await new Promise(resolve => setTimeout(resolve, 500));
    } catch (error) {
      console.error('[Daily Tests] Review response scoring error:', error.message);
    }
  }

  const avgScore = scores.length > 0
    ? scores.reduce((sum, s) => sum + s, 0) / scores.length
    : 0;

  return {
    score: Math.round(avgScore),
    tested: sample.length,
    passed: scores.filter(s => s >= 85).length,
    failed: scores.filter(s => s < 70).length,
    scores: scores,
    threshold: 85
  };
}

/**
 * Test 4: Response Time
 */
function testResponseTime(leads) {
  if (leads.length === 0) {
    return {
      score: 0,
      tested: 0,
      message: 'No leads to test'
    };
  }

  // Calculate response times
  const responseTimes = leads
    .filter(l => l.created_at && l.first_response_at)
    .map(l => {
      const created = new Date(l.created_at).getTime();
      const responded = new Date(l.first_response_at).getTime();
      return Math.floor((responded - created) / 60000); // Minutes
    });

  if (responseTimes.length === 0) {
    return {
      score: 0,
      tested: 0,
      message: 'No response time data'
    };
  }

  const avgResponseTime = responseTimes.reduce((sum, t) => sum + t, 0) / responseTimes.length;

  // Grading (Harvard study: respond in < 5 min = 60x more likely to qualify)
  let score = 0;
  if (avgResponseTime < 5) score = 100;
  else if (avgResponseTime < 10) score = 90;
  else if (avgResponseTime < 30) score = 75;
  else if (avgResponseTime < 60) score = 60;
  else score = 40;

  return {
    score,
    avgResponseTime: Math.round(avgResponseTime),
    tested: responseTimes.length,
    distribution: {
      under_5min: responseTimes.filter(t => t < 5).length,
      under_15min: responseTimes.filter(t => t < 15).length,
      under_1hour: responseTimes.filter(t => t < 60).length,
      over_1hour: responseTimes.filter(t => t >= 60).length
    }
  };
}

/**
 * Test 5: Follow-Up Consistency
 */
function testFollowUpConsistency(leads) {
  if (leads.length === 0) {
    return {
      score: 0,
      tested: 0,
      message: 'No leads to test'
    };
  }

  // Check how many leads got proper follow-up
  const withFollowUp = leads.filter(l => {
    const touchCount = l.touch_count || 0;
    return touchCount >= 5; // Should have at least 5 touches
  });

  const followUpRate = (withFollowUp.length / leads.length) * 100;

  // Score
  let score = 0;
  if (followUpRate >= 95) score = 100;
  else if (followUpRate >= 85) score = 90;
  else if (followUpRate >= 75) score = 80;
  else if (followUpRate >= 60) score = 70;
  else score = 50;

  return {
    score,
    tested: leads.length,
    withFollowUp: withFollowUp.length,
    followUpRate: followUpRate.toFixed(1),
    avgTouches: leads.reduce((sum, l) => sum + (l.touch_count || 0), 0) / leads.length
  };
}

/**
 * Test 6: Reputation Metrics
 */
function testReputationMetrics(reviews) {
  if (reviews.length === 0) {
    return {
      score: 0,
      tested: 0,
      message: 'No reviews to analyze'
    };
  }

  // Recent reviews (last 30 days)
  const thirtyDaysAgo = Date.now() - (30 * 24 * 60 * 60 * 1000);
  const recentReviews = reviews.filter(r =>
    new Date(r.created_at).getTime() > thirtyDaysAgo
  );

  // Average rating
  const ratings = reviews.map(r => r.rating);
  const avgRating = ratings.reduce((sum, r) => sum + r, 0) / ratings.length;

  // Response rate
  const responded = reviews.filter(r => r.response).length;
  const responseRate = (responded / reviews.length) * 100;

  // Response time (for negative reviews)
  const negativeReviews = reviews.filter(r => r.rating <= 3);
  const negativeWithResponseTime = negativeReviews.filter(r =>
    r.response_time_hours !== undefined
  );
  const avgNegativeResponseTime = negativeWithResponseTime.length > 0
    ? negativeWithResponseTime.reduce((sum, r) => sum + r.response_time_hours, 0) / negativeWithResponseTime.length
    : 0;

  // Calculate score
  let score = 0;

  // Rating score (0-40 points)
  if (avgRating >= 4.8) score += 40;
  else if (avgRating >= 4.5) score += 35;
  else if (avgRating >= 4.0) score += 25;
  else score += 10;

  // Response rate score (0-30 points)
  if (responseRate >= 95) score += 30;
  else if (responseRate >= 85) score += 25;
  else if (responseRate >= 70) score += 15;
  else score += 5;

  // Recent reviews score (0-20 points)
  if (recentReviews.length >= 10) score += 20;
  else if (recentReviews.length >= 5) score += 15;
  else if (recentReviews.length >= 2) score += 10;
  else score += 5;

  // Negative response time score (0-10 points)
  if (avgNegativeResponseTime < 4) score += 10;
  else if (avgNegativeResponseTime < 12) score += 7;
  else if (avgNegativeResponseTime < 24) score += 4;
  else score += 2;

  return {
    score,
    tested: reviews.length,
    avgRating: avgRating.toFixed(2),
    responseRate: responseRate.toFixed(1),
    recentReviews: recentReviews.length,
    avgNegativeResponseTime: Math.round(avgNegativeResponseTime)
  };
}

/**
 * Test 7: Conversion Rate
 */
function testConversionRate(leads) {
  if (leads.length === 0) {
    return {
      score: 0,
      tested: 0,
      message: 'No leads to analyze'
    };
  }

  const converted = leads.filter(l => l.converted === true).length;
  const conversionRate = (converted / leads.length) * 100;

  // Score based on conversion rate
  let score = 0;
  if (conversionRate >= 30) score = 100;
  else if (conversionRate >= 25) score = 95;
  else if (conversionRate >= 20) score = 90;
  else if (conversionRate >= 15) score = 80;
  else if (conversionRate >= 10) score = 70;
  else if (conversionRate >= 5) score = 60;
  else score = 40;

  return {
    score,
    tested: leads.length,
    converted: converted,
    conversionRate: conversionRate.toFixed(1)
  };
}

/**
 * Calculate overall health from test results
 */
function calculateOverallHealth(tests) {
  const results = {
    copywriting_avg: tests.emailCopy?.score || 0,
    sequences_avg: tests.sequences?.score || 0,
    reputation_avg: tests.reputation?.score || 0,
    response_time_avg: tests.responseTime?.score || 0,
    conversion_rate: tests.conversion?.score || 0
  };

  return executeRule('system_health', { results });
}

/**
 * Generate daily report
 */
export function generateDailyReport(testResults) {
  const report = {
    date: testResults.testDate,
    summary: {
      overallGrade: testResults.letterGrade,
      overallScore: testResults.overallGrade,
      status: testResults.status,
      testsRun: Object.keys(testResults.tests).length,
      duration: `${(testResults.duration / 1000).toFixed(1)}s`
    },
    results: {},
    priorityActions: testResults.actions || [],
    recommendations: []
  };

  // Format each test result
  for (const [testName, result] of Object.entries(testResults.tests)) {
    report.results[testName] = {
      score: result.score,
      status: result.score >= 80 ? 'PASS' : result.score >= 70 ? 'WARNING' : 'FAIL',
      details: result
    };

    // Add recommendations for failing tests
    if (result.score < 70) {
      report.recommendations.push({
        test: testName,
        issue: `Score ${result.score} below threshold 70`,
        action: getRecommendationForTest(testName, result)
      });
    }
  }

  return report;
}

function getRecommendationForTest(testName, result) {
  const recommendations = {
    emailCopy: 'Review and rewrite low-scoring emails. Use ML scorer to identify specific weaknesses.',
    sequences: 'Increase touch count to 7-14. Add more channels (LinkedIn, SMS, call).',
    reviewResponses: 'Improve response quality. Use world-class examples as templates.',
    responseTime: 'Reduce response time. Target < 15 minutes for all leads.',
    followUpConsistency: 'Ensure all leads get minimum 7 touches. Fix automation gaps.',
    reputation: 'Increase review request frequency. Improve response rate to 95%+.',
    conversion: 'Run A/B tests on copy. Optimize sequences. Improve lead quality.'
  };

  return recommendations[testName] || 'Review and optimize this component.';
}

export default {
  runDailyTests,
  generateDailyReport
};
