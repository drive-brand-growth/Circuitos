/**
 * ML-Based Quality Scorer
 * Uses Claude AI to analyze and score outputs against world-class principles
 *
 * Analyzes:
 * - Email copy quality
 * - Sequence effectiveness
 * - Review responses
 * - Landing page copy
 * - Sales conversations
 */

import Anthropic from '@anthropic-ai/sdk';
import {
  COPYWRITING_PRINCIPLES,
  SALES_PROCESS_PRINCIPLES,
  REPUTATION_PRINCIPLES,
  CONVERSION_PRINCIPLES
} from './world-class-principles.js';

const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
});

/**
 * Score email copy using ML
 *
 * @param {string} emailCopy - The email content (subject + body)
 * @param {object} context - Contact and business context
 * @returns {object} Detailed scoring
 */
export async function scoreEmailCopy(emailCopy, context = {}) {
  try {
    console.log('[ML Scorer] Analyzing email copy...');

    const prompt = buildEmailScoringPrompt(emailCopy, context);

    const message = await anthropic.messages.create({
      model: 'claude-sonnet-4-20250514',
      max_tokens: 3000,
      temperature: 0.3,  // Low temp for consistent scoring
      messages: [{
        role: 'user',
        content: prompt
      }]
    });

    const analysis = message.content[0].text;

    // Parse the structured response
    return parseMLScoreResponse(analysis, 'email');

  } catch (error) {
    console.error('[ML Scorer] Error:', error.message);
    throw error;
  }
}

/**
 * Build email scoring prompt
 */
function buildEmailScoringPrompt(emailCopy, context) {
  return `You are a world-class marketing analyst grading email copy based on principles from $100M+ businesses.

---

**EMAIL TO GRADE:**

${emailCopy}

---

**CONTEXT:**
- Contact: ${context.contact_name || 'Unknown'}
- Awareness Level: ${context.awareness_level || 'Unknown'}
- Lead Source: ${context.lead_source || 'Unknown'}
- Business Type: ${context.business_type || 'Unknown'}

---

**YOUR TASK:**

Grade this email copy on a 0-100 scale across these dimensions:

## 1. HORMOZI VALUE EQUATION (0-20 points)
- Dream Outcome Clarity (0-5): Does it state a specific, tangible outcome?
- Perceived Likelihood (0-5): Social proof, data, guarantees present?
- Time Delay (0-5): Shows speed to results?
- Effort/Sacrifice (0-5): Minimizes perceived difficulty?

## 2. BRUNSON HOOK-STORY-OFFER (0-20 points)
- Hook Attention (0-7): First line stops the scroll?
- Story Relatability (0-7): Story creates connection?
- Offer Clarity (0-6): Crystal clear what to do next?

## 3. SCHWARTZ AWARENESS (0-15 points)
- Awareness Match (0-10): Matches prospect's awareness level?
- Sophistication (0-5): Novel angle for market sophistication?

## 4. MILLER STORYBRAND (0-15 points)
- Hero Positioning (0-5): Customer is hero, not you?
- Problem Clear (0-5): External/internal/philosophical problem addressed?
- Plan Clear (0-5): Simple 3-step plan?

## 5. KENNEDY DIRECT RESPONSE (0-15 points)
- Urgency/Scarcity (0-5): Reason to act NOW?
- Risk Reversal (0-5): Guarantee or trial present?
- Specificity (0-5): Specific numbers vs vague claims?

## 6. HALBERT EMOTION (0-10 points)
- Curiosity (0-5): Creates curiosity gap?
- Loss Aversion (0-5): Shows cost of inaction?

## 7. OGILVY PRINCIPLES (0-5 points)
- Headline Power (0-5): Benefit-driven, specific, compelling?

---

**OUTPUT FORMAT:**

OVERALL SCORE: [0-100]
LETTER GRADE: [A+ to F]

DIMENSION SCORES:
- Hormozi Value: [0-20] - [Brief justification]
- Brunson HSO: [0-20] - [Brief justification]
- Schwartz Awareness: [0-15] - [Brief justification]
- Miller StoryBrand: [0-15] - [Brief justification]
- Kennedy Direct Response: [0-15] - [Brief justification]
- Halbert Emotion: [0-10] - [Brief justification]
- Ogilvy Principles: [0-5] - [Brief justification]

STRENGTHS (Top 3):
1. [Specific strength]
2. [Specific strength]
3. [Specific strength]

WEAKNESSES (Top 3):
1. [Specific weakness with fix]
2. [Specific weakness with fix]
3. [Specific weakness with fix]

IMPROVEMENTS NEEDED:
[Prioritized list of 3-5 specific improvements with examples]

REWRITTEN VERSION (OPTIONAL):
[If score < 70, provide a rewritten version scoring 90+]

---

Grade this email now with brutal honesty. Be specific and actionable.`;
}

/**
 * Score sequence effectiveness
 *
 * @param {array} sequence - Array of touches
 * @param {object} performance - Actual performance data
 * @returns {object} Sequence quality score
 */
export async function scoreSequence(sequence, performance = {}) {
  try {
    console.log('[ML Scorer] Analyzing sequence effectiveness...');

    const prompt = buildSequenceScoringPrompt(sequence, performance);

    const message = await anthropic.messages.create({
      model: 'claude-sonnet-4-20250514',
      max_tokens: 3000,
      temperature: 0.3,
      messages: [{
        role: 'user',
        content: prompt
      }]
    });

    const analysis = message.content[0].text;

    return parseMLScoreResponse(analysis, 'sequence');

  } catch (error) {
    console.error('[ML Scorer] Error:', error.message);
    throw error;
  }
}

/**
 * Build sequence scoring prompt
 */
function buildSequenceScoringPrompt(sequence, performance) {
  const sequenceSummary = sequence.map((touch, i) => `
Touch ${i + 1} (Day ${touch.dayOffset}):
Subject: ${touch.subject || 'N/A'}
Framework: ${touch.framework}
Goal: ${touch.goal}
`).join('\n');

  return `You are a world-class sales analyst grading a multi-touch email sequence.

---

**SEQUENCE TO GRADE:**

${sequenceSummary}

---

**PERFORMANCE DATA:**
- Open Rate: ${performance.open_rate || 'Unknown'}
- Reply Rate: ${performance.reply_rate || 'Unknown'}
- Conversion Rate: ${performance.conversion_rate || 'Unknown'}
- Touches Before Response: ${performance.avg_touches_to_response || 'Unknown'}

---

**GRADE ON:**

## 1. TOUCH COUNT & TIMING (0-25 points)
- Number of touches: 7-14 optimal (80% of sales after touch 5)
- Timing between touches: 2-4 days optimal
- Sequence duration: 2-3 weeks optimal

## 2. FRAMEWORK VARIETY (0-20 points)
- Uses multiple frameworks? (prevents pattern fatigue)
- Each touch has different angle?
- Progressive building (awareness → interest → desire → action)?

## 3. VALUE PROGRESSION (0-20 points)
- Touch 1-2: Attention/Problem aware
- Touch 3-4: Value/No-ask touch included?
- Touch 5+: Direct offer → Breakup → Long nurture
- Follows proven sequence structure?

## 4. PERSISTENCE vs ANNOYANCE (0-15 points)
- Appropriate frequency?
- Gives value not just asks?
- Breakup email included?
- Auto-pause on reply?

## 5. CHANNEL DIVERSITY (0-10 points)
- Multiple channels used? (email, LinkedIn, SMS, call)
- Right channel for right message?

## 6. PERSONALIZATION (0-10 points)
- Sequences adapt to behavior?
- Different sequences for different awareness levels?
- Context-specific content?

---

**OUTPUT FORMAT:**

OVERALL SCORE: [0-100]
LETTER GRADE: [A+ to F]

DIMENSION SCORES:
- Touch Count & Timing: [0-25] - [Justification]
- Framework Variety: [0-20] - [Justification]
- Value Progression: [0-20] - [Justification]
- Persistence Balance: [0-15] - [Justification]
- Channel Diversity: [0-10] - [Justification]
- Personalization: [0-10] - [Justification]

STRENGTHS (Top 3):
1. [Specific strength]
2. [Specific strength]
3. [Specific strength]

WEAKNESSES (Top 3):
1. [Specific weakness with fix]
2. [Specific weakness with fix]
3. [Specific weakness with fix]

IMPROVEMENTS NEEDED:
[Prioritized list with specific changes]

BENCHMARK COMPARISON:
- vs Average Sequence (2 touches): [Comparison]
- vs Good Sequence (5-7 touches): [Comparison]
- vs World-Class (12-14 touches): [Comparison]

---

Grade this sequence with brutal honesty.`;
}

/**
 * Score review response quality
 *
 * @param {object} review - Original review
 * @param {string} response - Your response
 * @returns {object} Response quality score
 */
export async function scoreReviewResponse(review, response) {
  try {
    console.log('[ML Scorer] Analyzing review response...');

    const prompt = buildReviewResponsePrompt(review, response);

    const message = await anthropic.messages.create({
      model: 'claude-sonnet-4-20250514',
      max_tokens: 2000,
      temperature: 0.3,
      messages: [{
        role: 'user',
        content: prompt
      }]
    });

    const analysis = message.content[0].text;

    return parseMLScoreResponse(analysis, 'review_response');

  } catch (error) {
    console.error('[ML Scorer] Error:', error.message);
    throw error;
  }
}

/**
 * Build review response scoring prompt
 */
function buildReviewResponsePrompt(review, response) {
  return `You are a reputation management expert grading a review response.

---

**ORIGINAL REVIEW:**
Rating: ${review.rating}/5 ⭐
Review: "${review.text}"

**YOUR RESPONSE:**
"${response}"

---

**GRADE ON:**

## 1. TONE APPROPRIATENESS (0-25 points)
- 5★: Warm, grateful, personal
- 4★: Appreciative, address feedback
- 3★: Apologetic, solution-focused
- 2★: Very apologetic, immediate action offered
- 1★: Deeply apologetic, take offline, personal contact

## 2. SPECIFICITY (0-20 points)
- References specific details from their review?
- Not generic "thank you for feedback"?
- Shows you actually read their review?

## 3. PERSONALIZATION (0-15 points)
- Uses their name?
- Personal touch (not corporate)?
- Sounds like human, not AI/template?

## 4. ACTION/SOLUTION (0-20 points)
- For negative: Offers clear solution/contact?
- For positive: Invites them back or next step?
- Appropriate action for rating level?

## 5. BRAND VOICE (0-10 points)
- Consistent with brand personality?
- Professional yet conversational?
- Authentic not robotic?

## 6. LENGTH (0-10 points)
- Appropriate length (50-100 words)?
- Not too short (seems uncaring)?
- Not too long (rambling)?

---

**OUTPUT FORMAT:**

OVERALL SCORE: [0-100]
LETTER GRADE: [A+ to F]

DIMENSION SCORES:
- Tone: [0-25] - [Justification]
- Specificity: [0-20] - [Justification]
- Personalization: [0-15] - [Justification]
- Action/Solution: [0-20] - [Justification]
- Brand Voice: [0-10] - [Justification]
- Length: [0-10] - [Justification]

STRENGTHS:
[List strengths]

WEAKNESSES:
[List weaknesses]

IMPROVED VERSION:
[Rewrite the response to score 95+]

---

Grade this response now.`;
}

/**
 * Parse ML score response into structured data
 */
function parseMLScoreResponse(analysisText, type) {
  try {
    // Extract overall score
    const scoreMatch = analysisText.match(/OVERALL SCORE:\s*(\d+)/i);
    const overallScore = scoreMatch ? parseInt(scoreMatch[1]) : 0;

    // Extract letter grade
    const gradeMatch = analysisText.match(/LETTER GRADE:\s*([A-F][+-]?)/i);
    const letterGrade = gradeMatch ? gradeMatch[1] : 'F';

    // Extract strengths
    const strengthsSection = analysisText.match(/STRENGTHS.*?:\s*([\s\S]*?)(?=WEAKNESSES|IMPROVEMENTS|$)/i);
    const strengths = strengthsSection
      ? strengthsSection[1].split('\n').filter(s => s.trim() && s.match(/^\d+\./)).map(s => s.trim())
      : [];

    // Extract weaknesses
    const weaknessesSection = analysisText.match(/WEAKNESSES.*?:\s*([\s\S]*?)(?=IMPROVEMENTS|REWRITTEN|$)/i);
    const weaknesses = weaknessesSection
      ? weaknessesSection[1].split('\n').filter(s => s.trim() && s.match(/^\d+\./)).map(s => s.trim())
      : [];

    // Extract improvements
    const improvementsSection = analysisText.match(/IMPROVEMENTS NEEDED:\s*([\s\S]*?)(?=REWRITTEN|IMPROVED|BENCHMARK|$)/i);
    const improvements = improvementsSection
      ? improvementsSection[1].split('\n').filter(s => s.trim()).map(s => s.trim())
      : [];

    return {
      type,
      overallScore,
      letterGrade,
      strengths,
      weaknesses,
      improvements,
      fullAnalysis: analysisText,
      gradedAt: new Date().toISOString(),
      needsImprovement: overallScore < 70
    };

  } catch (error) {
    console.error('[ML Scorer] Parse error:', error.message);
    return {
      type,
      overallScore: 0,
      letterGrade: 'F',
      strengths: [],
      weaknesses: ['Failed to parse analysis'],
      improvements: ['Re-run analysis'],
      fullAnalysis: analysisText,
      gradedAt: new Date().toISOString(),
      needsImprovement: true,
      parseError: error.message
    };
  }
}

/**
 * Score entire sales conversation
 *
 * @param {array} conversation - Array of messages
 * @param {object} outcome - Conversion outcome
 * @returns {object} Conversation quality score
 */
export async function scoreConversation(conversation, outcome = {}) {
  try {
    console.log('[ML Scorer] Analyzing sales conversation...');

    const conversationText = conversation.map(msg =>
      `${msg.from} (${msg.timestamp}): ${msg.message}`
    ).join('\n\n');

    const prompt = `You are a sales coach grading a sales conversation.

---

**CONVERSATION:**

${conversationText}

---

**OUTCOME:**
- Converted: ${outcome.converted ? 'Yes' : 'No'}
- Value: ${outcome.value || 'Unknown'}
- Time to Close: ${outcome.time_to_close || 'Unknown'}

---

**GRADE ON SALES PRINCIPLES:**

## 1. DISCOVERY (0-20 points)
- Asked about their problem/pain?
- Uncovered budget (BANT)?
- Identified decision maker?
- Established timeline?

## 2. RAPPORT BUILDING (0-15 points)
- Personal connection made?
- Active listening demonstrated?
- Empathy shown?

## 3. VALUE ARTICULATION (0-20 points)
- Clearly showed ROI/value?
- Tied features to their specific needs?
- Used stories/social proof?

## 4. OBJECTION HANDLING (0-20 points)
- Addressed price objection effectively?
- Handled time objection?
- Turned objections into opportunities?

## 5. CLOSING (0-15 points)
- Asked for the sale?
- Used assumptive/alternative close?
- Clear next steps?

## 6. FOLLOW-UP (0-10 points)
- Followed up if no immediate yes?
- Maintained momentum?

---

Grade this conversation and provide specific feedback.

OUTPUT FORMAT:
OVERALL SCORE: [0-100]
[Detailed analysis]`;

    const message = await anthropic.messages.create({
      model: 'claude-sonnet-4-20250514',
      max_tokens: 3000,
      temperature: 0.3,
      messages: [{
        role: 'user',
        content: prompt
      }]
    });

    const analysis = message.content[0].text;

    return parseMLScoreResponse(analysis, 'conversation');

  } catch (error) {
    console.error('[ML Scorer] Error:', error.message);
    throw error;
  }
}

/**
 * Batch score multiple outputs
 *
 * @param {array} items - Array of {type, content, context}
 * @returns {array} Array of scores
 */
export async function batchScore(items) {
  const results = [];

  for (const item of items) {
    let score;

    switch (item.type) {
      case 'email':
        score = await scoreEmailCopy(item.content, item.context);
        break;
      case 'sequence':
        score = await scoreSequence(item.content, item.context);
        break;
      case 'review_response':
        score = await scoreReviewResponse(item.review, item.response);
        break;
      case 'conversation':
        score = await scoreConversation(item.content, item.outcome);
        break;
      default:
        console.warn(`[ML Scorer] Unknown type: ${item.type}`);
        continue;
    }

    results.push({
      id: item.id,
      ...score
    });

    // Rate limiting - wait 1 second between requests
    await new Promise(resolve => setTimeout(resolve, 1000));
  }

  return results;
}

export default {
  scoreEmailCopy,
  scoreSequence,
  scoreReviewResponse,
  scoreConversation,
  batchScore
};
