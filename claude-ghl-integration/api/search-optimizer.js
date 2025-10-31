import Anthropic from '@anthropic-ai/sdk';

const anthropic = new Anthropic({
  apiKey: process.env.CLAUDE_API_KEY
});

const SYSTEM_PROMPT = `You are the Search Optimizer for Circuit OS™, optimizing content for AI search engines (ChatGPT, Perplexity, Claude, Gemini).

YOUR ROLE:
Optimize content to be cited by LLMs when users ask relevant questions

AI SEARCH OPTIMIZATION STRATEGY:

1. CITATION-WORTHY CONTENT
   - Authoritative statements with data sources
   - Unique insights not available elsewhere
   - Structured answers to common questions
   - Definitive guides and comparisons

2. E-E-A-T SIGNALS (for LLM training data selection)
   - Experience: First-hand accounts, case studies
   - Expertise: Credentials, certifications, detailed knowledge
   - Authority: Industry recognition, backlinks, mentions
   - Trust: Transparency, citations, contact info

3. STRUCTURED DATA
   - FAQPage schema (directly feeds Q&A models)
   - HowTo schema (step-by-step instructions)
   - Review schema (aggregated ratings)
   - LocalBusiness schema (NAP consistency)

4. VOICE SEARCH OPTIMIZATION
   - Natural language questions as H2 headers
   - Conversational answers (how people speak)
   - Featured snippet optimization (position 0)
   - "People Also Ask" targeting

5. ENTITY RECOGNITION
   - Clear entity definitions (who, what, where)
   - Consistent naming conventions
   - Relationship mapping (business ↔ services ↔ location)
   - Synonyms and variations

TARGET METRICS:
- 60%+ AI citation rate (mentioned in LLM responses)
- Position 0 (featured snippet) for target queries
- Voice search ranking for "near me" queries
- 10+ knowledge graph mentions per month

OUTPUT: AI-optimized content that LLMs will cite`;

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { content, business, target_queries, optimization_goal } = req.body;

  if (!content) {
    return res.status(400).json({
      error: 'Missing content to optimize',
      usage: 'POST with: { "content": "...", "business": {...}, "target_queries": [...], "optimization_goal": "citation|snippet|voice" }'
    });
  }

  try {
    const message = await anthropic.messages.create({
      model: 'claude-sonnet-4-20250514',
      max_tokens: 6000,
      temperature: 0.5,
      messages: [{
        role: 'user',
        content: `${SYSTEM_PROMPT}

CONTENT TO OPTIMIZE:
${content}

BUSINESS INFO:
${JSON.stringify(business, null, 2)}

TARGET QUERIES:
${JSON.stringify(target_queries || [])}

OPTIMIZATION GOAL: ${optimization_goal || 'citation'}

Analyze and optimize this content for AI search engines. Return JSON:
{
  "optimized_content": "Rewritten content optimized for LLM citation...",
  "faq_schema": [
    {
      "question": "Natural language question",
      "answer": "Authoritative, citation-worthy answer"
    }
  ],
  "structured_data": {
    "type": "FAQPage",
    "json_ld": "Full JSON-LD schema code..."
  },
  "voice_search_phrases": [
    "best gym near me for powerlifting",
    "where can I train for strongman competition"
  ],
  "featured_snippet_targets": [
    {
      "query": "how to choose a powerlifting gym",
      "optimized_answer": "Short, definitive answer (40-60 words)"
    }
  ],
  "entity_optimization": {
    "primary_entity": "MetroFlex Gym",
    "entity_type": "LocalBusiness > Gym",
    "related_entities": ["powerlifting", "strongman", "Arlington TX"]
  },
  "ai_citation_score": 85,
  "improvements_made": [
    "Added FAQ schema for 10 common questions",
    "Restructured for featured snippet eligibility",
    "Enhanced E-E-A-T signals with certifications"
  ],
  "expected_ai_mention_rate": 0.65
}`
      }]
    });

    const responseText = message.content[0].text;
    const jsonMatch = responseText.match(/\{[\s\S]*\}/);

    if (!jsonMatch) {
      throw new Error('No valid JSON in response');
    }

    const result = JSON.parse(jsonMatch[0]);
    result.optimized_at = new Date().toISOString();
    result.optimization_goal = optimization_goal || 'citation';
    result.api_version = '1.0.0';

    return res.status(200).json(result);

  } catch (error) {
    console.error('Error:', error);
    return res.status(500).json({
      error: 'Failed to optimize content',
      details: error.message
    });
  }
}
