/**
 * Non-Traditional Path Suggester
 * Generates creative, lateral, and unconventional solutions
 *
 * @module non-traditional-suggester
 * @copyright 2025 CircuitOS™ - HIGHLY CONFIDENTIAL
 */

const Anthropic = require('@anthropic-ai/sdk');

class NonTraditionalPathSuggester {
  constructor(config = {}) {
    this.config = {
      anthropicApiKey: config.anthropicApiKey || process.env.ANTHROPIC_API_KEY,
      model: config.model || 'claude-sonnet-4-5-20250929',
      ...config
    };

    this.anthropic = new Anthropic({
      apiKey: this.config.anthropicApiKey
    });

    this.lateralThinking = new LateralThinkingEngine(this.anthropic, this.config);
    this.crossDomain = new CrossDomainMapper(this.anthropic, this.config);
    this.noveltyDetector = new NoveltyDetector(this.anthropic, this.config);
  }

  /**
   * Suggest non-traditional paths for a problem
   */
  async suggestNonTraditionalPaths(problem) {
    console.log('💡 Generating non-traditional solutions...');

    const suggestions = [];

    // 1. Lateral thinking approaches
    const lateral = await this.lateralThinking.generate(problem);
    suggestions.push(...lateral);

    // 2. Cross-domain solutions
    const crossDomain = await this.crossDomain.findAnalogies(problem);
    suggestions.push(...crossDomain);

    // 3. Inversion thinking
    const inversions = await this.generateInversions(problem);
    suggestions.push(...inversions);

    // 4. Constraint relaxation
    const relaxed = await this.relaxConstraints(problem);
    suggestions.push(...relaxed);

    // 5. Novel approaches
    const novel = await this.generateNovelApproaches(problem);
    suggestions.push(...novel);

    // Filter to only truly non-traditional
    const nonTraditional = [];
    for (const suggestion of suggestions) {
      if (await this.noveltyDetector.isNonTraditional(suggestion)) {
        nonTraditional.push(suggestion);
      }
    }

    // Rank by impact
    const ranked = await this.rankByImpact(nonTraditional);

    console.log(`✅ Generated ${ranked.length} non-traditional paths`);

    return ranked;
  }

  /**
   * Generate inversions (solve opposite problem)
   * @private
   */
  async generateInversions(problem) {
    const prompt = `# Inversion Thinking

Problem: ${problem.description}
Current Approach: ${problem.currentApproach || 'Standard methods'}

## Task: Inversion Technique
1. First, state the OPPOSITE problem
2. Solve the opposite problem
3. Invert the solution to get novel approach to original problem

Example:
- Problem: "How to get more gym members?"
- Opposite: "How to make sure we NEVER get members?"
- Opposite Solution: "Make it expensive, unwelcoming, inconvenient"
- Inverted: "Make it affordable, welcoming, ultra-convenient"
- Novel Insight: "Ultimate convenience = 24/7 access, no check-in required"

Return 3 inversion-based solutions as JSON array:
{
  "opposite_problem": "...",
  "opposite_solution": "...",
  "inverted_approach": "...",
  "why_novel": "...",
  "expected_impact": "low|medium|high"
}`;

    try {
      const response = await this.anthropic.messages.create({
        model: this.config.model,
        max_tokens: 2048,
        temperature: 0.9,
        messages: [{
          role: 'user',
          content: prompt
        }]
      });

      const content = response.content[0].text;
      const jsonMatch = content.match(/\[[\s\S]*\]/);
      const inversions = jsonMatch ? JSON.parse(jsonMatch[0]) : [];

      return inversions.map(inv => ({
        type: 'inversion',
        approach: inv.inverted_approach,
        description: inv.why_novel,
        potentialImpact: inv.expected_impact,
        novelty: 0.8
      }));
    } catch (error) {
      console.error('Error generating inversions:', error);
      return [];
    }
  }

  /**
   * Relax constraints to find new possibilities
   * @private
   */
  async relaxConstraints(problem) {
    const constraints = problem.constraints || [
      'Must respond quickly',
      'Must be professional',
      'Must be cost-effective'
    ];

    const prompt = `# Constraint Relaxation

Problem: ${problem.description}

## Current Constraints
${constraints.map((c, i) => `${i + 1}. ${c}`).join('\n')}

## Task
For EACH constraint, imagine it doesn't exist. What becomes possible?

Example:
- Constraint: "Must respond within 2 minutes"
- Relaxed: "What if we deliberately wait 30 minutes?"
- Insight: "Delayed response creates urgency psychology, increases perceived value"
- Application: "For VIP leads, strategic delay makes them more eager"

Return 3-5 constraint relaxations as JSON array:
{
  "removed_constraint": "...",
  "new_possibility": "...",
  "counter_intuitive_benefit": "...",
  "how_to_apply": "..."
}`;

    try {
      const response = await this.anthropic.messages.create({
        model: this.config.model,
        max_tokens: 2048,
        temperature: 0.9,
        messages: [{
          role: 'user',
          content: prompt
        }]
      });

      const content = response.content[0].text;
      const jsonMatch = content.match(/\[[\s\S]*\]/);
      const relaxations = jsonMatch ? JSON.parse(jsonMatch[0]) : [];

      return relaxations.map(rel => ({
        type: 'constraint_relaxation',
        approach: rel.new_possibility,
        description: rel.counter_intuitive_benefit,
        application: rel.how_to_apply,
        novelty: 0.75
      }));
    } catch (error) {
      console.error('Error relaxing constraints:', error);
      return [];
    }
  }

  /**
   * Generate completely novel approaches
   * @private
   */
  async generateNovelApproaches(problem) {
    const prompt = `# Novel Approach Generation

Problem: ${problem.description}

## Task: Be Radically Creative
Generate 3 COMPLETELY NOVEL approaches that:
- Have never been tried before
- Challenge fundamental assumptions
- May seem "crazy" but could work
- Use unconventional methods

Think like:
- An artist solving a business problem
- A scientist solving a creative problem
- A child with no preconceptions

Return as JSON array:
{
  "approach": "...",
  "why_novel": "...",
  "potential_breakthrough": "...",
  "risks": "...",
  "how_to_test": "..."
}`;

    try {
      const response = await this.anthropic.messages.create({
        model: this.config.model,
        max_tokens: 2048,
        temperature: 1.0,
        messages: [{
          role: 'user',
          content: prompt
        }]
      });

      const content = response.content[0].text;
      const jsonMatch = content.match(/\[[\s\S]*\]/);
      const approaches = jsonMatch ? JSON.parse(jsonMatch[0]) : [];

      return approaches.map(app => ({
        type: 'novel',
        approach: app.approach,
        description: app.why_novel,
        breakthrough: app.potential_breakthrough,
        risks: app.risks,
        testMethod: app.how_to_test,
        novelty: 0.95
      }));
    } catch (error) {
      console.error('Error generating novel approaches:', error);
      return [];
    }
  }

  /**
   * Rank suggestions by potential impact
   * @private
   */
  async rankByImpact(suggestions) {
    // Simple ranking: novelty * estimated impact
    return suggestions.sort((a, b) => {
      const scoreA = (a.novelty || 0.5) * this.impactScore(a.potentialImpact);
      const scoreB = (b.novelty || 0.5) * this.impactScore(b.potentialImpact);
      return scoreB - scoreA;
    });
  }

  /**
   * Convert impact string to score
   * @private
   */
  impactScore(impact) {
    if (impact === 'high') return 1.0;
    if (impact === 'medium') return 0.6;
    return 0.3;
  }
}

/**
 * Lateral Thinking Engine
 */
class LateralThinkingEngine {
  constructor(anthropic, config) {
    this.anthropic = anthropic;
    this.config = config;
  }

  async generate(problem) {
    const prompt = `# Lateral Thinking Challenge

Problem: ${problem.description}
Traditional Solution: ${problem.traditionalSolution || 'Standard industry practices'}

## Task: Think Laterally
Generate 5 LATERAL solutions that:
1. Approach from unexpected angles
2. Challenge core assumptions
3. Use unconventional methods
4. May seem "wrong" at first but could work brilliantly
5. Draw from unrelated domains

Examples of lateral thinking:
- Southwest Airlines: "What if we ran an airline like a bus service?"
- Apple Store: "What if we had no checkout counters?"
- Netflix: "What if late fees... didn't exist?"

Return as JSON array:
{
  "approach": "...",
  "why_unconventional": "...",
  "assumptions_challenged": [],
  "potential_impact": "low|medium|high",
  "inspiration_source": "What domain/idea inspired this?"
}`;

    try {
      const response = await this.anthropic.messages.create({
        model: this.config.model,
        max_tokens: 2048,
        temperature: 0.95,
        messages: [{
          role: 'user',
          content: prompt
        }]
      });

      const content = response.content[0].text;
      const jsonMatch = content.match(/\[[\s\S]*\]/);
      const solutions = jsonMatch ? JSON.parse(jsonMatch[0]) : [];

      return solutions.map(s => ({
        type: 'lateral',
        approach: s.approach,
        description: s.why_unconventional,
        assumptions: s.assumptions_challenged,
        potentialImpact: s.potential_impact,
        inspiration: s.inspiration_source,
        novelty: 0.85
      }));
    } catch (error) {
      console.error('Error in lateral thinking:', error);
      return [];
    }
  }
}

/**
 * Cross-Domain Mapper - Borrow solutions from other fields
 */
class CrossDomainMapper {
  constructor(anthropic, config) {
    this.anthropic = anthropic;
    this.config = config;
  }

  async findAnalogies(problem) {
    const prompt = `# Cross-Domain Solution Mining

Problem: ${problem.description}
Industry: ${problem.industry || 'General'}

## Task: Find Analogous Solutions
Find 5 solutions from DIFFERENT industries and adapt them.

Examples:
- Netflix engagement → Applied to gym retention
- Uber routing optimization → Applied to appointment scheduling
- TikTok's algorithm → Applied to email campaign optimization
- Spotify playlists → Applied to workout program recommendations

For each:
1. Identify the source industry
2. Explain their solution
3. Adapt it to the current problem
4. Explain why it could work

Return as JSON array:
{
  "source_industry": "...",
  "source_solution": "...",
  "adaptation": "...",
  "why_applicable": "...",
  "novelty_score": 0-100
}`;

    try {
      const response = await this.anthropic.messages.create({
        model: this.config.model,
        max_tokens: 2048,
        temperature: 0.85,
        messages: [{
          role: 'user',
          content: prompt
        }]
      });

      const content = response.content[0].text;
      const jsonMatch = content.match(/\[[\s\S]*\]/);
      const analogies = jsonMatch ? JSON.parse(jsonMatch[0]) : [];

      return analogies.map(a => ({
        type: 'cross_domain',
        sourceIndustry: a.source_industry,
        sourceSolution: a.source_solution,
        approach: a.adaptation,
        description: a.why_applicable,
        novelty: a.novelty_score / 100
      }));
    } catch (error) {
      console.error('Error finding analogies:', error);
      return [];
    }
  }
}

/**
 * Novelty Detector - Measures how non-traditional something is
 */
class NoveltyDetector {
  constructor(anthropic, config) {
    this.anthropic = anthropic;
    this.config = config;
  }

  async isNonTraditional(solution) {
    // Simple heuristic: if novelty score > 0.6, it's non-traditional
    return (solution.novelty || 0) > 0.6;
  }

  async scoreNovelty(solution) {
    const prompt = `# Novelty Scoring

Solution: ${solution.approach}
Description: ${solution.description}

## Score (0-100)
0 = Completely conventional, everyone does this
50 = Somewhat unusual, few do this
75 = Very unusual, rarely done
100 = Never been done before, revolutionary

Provide score with brief reasoning.

Return JSON:
{
  "novelty": 0-100,
  "reasoning": "..."
}`;

    try {
      const response = await this.anthropic.messages.create({
        model: this.config.model,
        max_tokens: 512,
        temperature: 0.5,
        messages: [{
          role: 'user',
          content: prompt
        }]
      });

      const content = response.content[0].text;
      const jsonMatch = content.match(/\{[\s\S]*\}/);
      const score = jsonMatch ? JSON.parse(jsonMatch[0]) : { novelty: 50 };

      return score.novelty / 100;
    } catch (error) {
      console.error('Error scoring novelty:', error);
      return 0.5;
    }
  }
}

module.exports = {
  NonTraditionalPathSuggester,
  LateralThinkingEngine,
  CrossDomainMapper,
  NoveltyDetector
};
