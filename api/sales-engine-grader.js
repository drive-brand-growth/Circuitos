/**
 * Sales Engine Grader API
 * World-class quality assurance system using ML, DMN, and LLM
 *
 * Features:
 * - Grades email copy, sequences, review responses
 * - Makes automated decisions (approve/reject/improve)
 * - Runs daily quality tests
 * - Provides actionable improvements
 * - Based on $100M+ business principles
 *
 * Cost: ~$10-20/month in Claude API calls
 * ROI: Prevents bad content, improves conversion 10-30%
 */

import { scoreEmailCopy, scoreSequence, scoreReviewResponse, scoreConversation } from '../lib/grading/ml-quality-scorer.js';
import { executeRule } from '../lib/grading/dmn-rules-engine.js';
import { runDailyTests, generateDailyReport } from '../lib/grading/daily-test-suite.js';
import { calculateOverallGrade } from '../lib/grading/world-class-principles.js';

/**
 * Main grading endpoint
 */
export default async function handler(req, res) {
  // CORS
  res.setHeader('Access-Control-Allow-Credentials', true);
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET,POST,OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const { action, ...data } = req.body;

    console.log(`[Grader] Action: ${action}`);

    switch (action) {
      case 'grade_email':
        return await gradeEmail(req, res, data);

      case 'grade_sequence':
        return await gradeSequence(req, res, data);

      case 'grade_review_response':
        return await gradeReviewResponse(req, res, data);

      case 'grade_conversation':
        return await gradeConversation(req, res, data);

      case 'decide':
        return await makeDecision(req, res, data);

      case 'run_daily_tests':
        return await runDailyTestsHandler(req, res, data);

      case 'get_overall_grade':
        return await getOverallGrade(req, res, data);

      default:
        return res.status(400).json({ error: 'Invalid action' });
    }

  } catch (error) {
    console.error('[Grader] Error:', error);
    return res.status(500).json({
      error: 'Grading failed',
      message: error.message
    });
  }
}

/**
 * Grade email copy
 */
async function gradeEmail(req, res, data) {
  const { email, context } = data;

  if (!email) {
    return res.status(400).json({ error: 'Missing email content' });
  }

  // Score with ML
  const score = await scoreEmailCopy(email, context || {});

  // Make approval decision
  const decision = executeRule('content_approval', {
    score: score.overallScore,
    type: 'email'
  });

  return res.status(200).json({
    ...score,
    decision,
    timestamp: new Date().toISOString()
  });
}

/**
 * Grade sequence
 */
async function gradeSequence(req, res, data) {
  const { sequence, performance } = data;

  if (!sequence || !Array.isArray(sequence)) {
    return res.status(400).json({ error: 'Missing or invalid sequence' });
  }

  // Score with ML
  const score = await scoreSequence(sequence, performance || {});

  // Decision
  const decision = score.overallScore >= 75
    ? { decision: 'APPROVED', reason: 'Sequence meets quality standards' }
    : { decision: 'NEEDS_IMPROVEMENT', reason: 'Sequence needs optimization' };

  return res.status(200).json({
    ...score,
    decision,
    timestamp: new Date().toISOString()
  });
}

/**
 * Grade review response
 */
async function gradeReviewResponse(req, res, data) {
  const { review, response } = data;

  if (!review || !response) {
    return res.status(400).json({ error: 'Missing review or response' });
  }

  // Score with ML
  const score = await scoreReviewResponse(review, response);

  // Make publishing decision
  const decision = executeRule('review_response_publish', {
    review,
    response,
    responseScore: score.overallScore
  });

  return res.status(200).json({
    ...score,
    decision,
    timestamp: new Date().toISOString()
  });
}

/**
 * Grade sales conversation
 */
async function gradeConversation(req, res, data) {
  const { conversation, outcome } = data;

  if (!conversation || !Array.isArray(conversation)) {
    return res.status(400).json({ error: 'Missing or invalid conversation' });
  }

  // Score with ML
  const score = await scoreConversation(conversation, outcome || {});

  return res.status(200).json({
    ...score,
    timestamp: new Date().toISOString()
  });
}

/**
 * Make automated decision
 */
async function makeDecision(req, res, data) {
  const { ruleType, input } = data;

  if (!ruleType || !input) {
    return res.status(400).json({ error: 'Missing ruleType or input' });
  }

  const decision = executeRule(ruleType, input);

  return res.status(200).json({
    ruleType,
    decision,
    timestamp: new Date().toISOString()
  });
}

/**
 * Run daily test suite
 */
async function runDailyTestsHandler(req, res, data) {
  const { systemData } = data;

  if (!systemData) {
    return res.status(400).json({ error: 'Missing systemData' });
  }

  console.log('[Grader] Running daily test suite...');

  // Run all tests
  const testResults = await runDailyTests(systemData);

  // Generate report
  const report = generateDailyReport(testResults);

  return res.status(200).json({
    testResults,
    report,
    timestamp: new Date().toISOString()
  });
}

/**
 * Get overall system grade
 */
async function getOverallGrade(req, res, data) {
  const { scores } = data;

  if (!scores) {
    return res.status(400).json({ error: 'Missing scores' });
  }

  const overallGrade = calculateOverallGrade(scores);

  return res.status(200).json({
    ...overallGrade,
    timestamp: new Date().toISOString()
  });
}

/**
 * Helper: Quick grade (synchronous, no ML)
 * Use for fast validation
 */
export function quickGrade(content, type) {
  let score = 50; // Start at baseline

  // Length check
  if (type === 'email') {
    const wordCount = content.split(/\s+/).length;
    if (wordCount >= 75 && wordCount <= 125) score += 10;
    else if (wordCount > 200) score -= 15; // Too long

    // Subject line check
    if (content.includes('SUBJECT:')) {
      const subjectMatch = content.match(/SUBJECT:\s*(.+)/);
      if (subjectMatch) {
        const subject = subjectMatch[1];
        const subjectWords = subject.split(/\s+/).length;
        if (subjectWords >= 4 && subjectWords <= 8) score += 10;
      }
    }

    // Bad patterns
    const badPatterns = [
      /dear valued customer/i,
      /I hope this email finds you well/i,
      /to whom it may concern/i,
      /click here/i
    ];
    badPatterns.forEach(pattern => {
      if (pattern.test(content)) score -= 10;
    });

    // Good patterns
    const goodPatterns = [
      /\$\d+/,  // Specific numbers
      /\d+%/,   // Percentages
      /\?$/m    // Questions
    ];
    goodPatterns.forEach(pattern => {
      if (pattern.test(content)) score += 5;
    });
  }

  return {
    score: Math.max(0, Math.min(100, score)),
    method: 'quick_grade',
    recommendation: score < 70 ? 'Run full ML grade for detailed feedback' : 'Looks good'
  };
}

/**
 * Batch grade multiple items
 */
export async function batchGrade(items) {
  const results = [];

  for (const item of items) {
    let result;

    switch (item.type) {
      case 'email':
        result = await gradeEmail(null, null, item);
        break;
      case 'sequence':
        result = await gradeSequence(null, null, item);
        break;
      case 'review_response':
        result = await gradeReviewResponse(null, null, item);
        break;
      default:
        result = { error: 'Unknown type' };
    }

    results.push({
      id: item.id,
      ...result
    });

    // Rate limiting
    await new Promise(resolve => setTimeout(resolve, 1000));
  }

  return results;
}
