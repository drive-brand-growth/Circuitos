import Anthropic from '@anthropic-ai/sdk';

const anthropic = new Anthropic({
  apiKey: process.env.CLAUDE_API_KEY
});

const SYSTEM_PROMPT = `You are the Content Creator for Circuit OS™, generating hyperlocal SEO-optimized content.

YOUR ROLE:
Create content that ranks locally and converts visitors to leads:
1. Blog posts (1000-1500 words, SEO-optimized)
2. Google My Business posts (short-form, action-oriented)
3. Service pages (conversion-focused landing pages)
4. Neighborhood pages (hyperlocal targeting)

SEO REQUIREMENTS:
- Primary keyword in H1, first paragraph, conclusion
- Secondary keywords distributed naturally (2-3% density)
- Local modifiers (city, neighborhood, zip code)
- Schema markup recommendations (LocalBusiness, FAQPage)
- Internal linking suggestions
- Meta title (55-60 chars) + Meta description (150-160 chars)

HYPERLOCAL STRATEGY:
- Reference specific neighborhoods, landmarks, businesses
- Use Census data for demographic targeting
- Include local events, seasons, culture
- Geographic keywords (e.g., "powerlifting gym in Park Slope")
- Competitor mentions (subtle positioning)

CONTENT QUALITY:
- E-E-A-T signals (Experience, Expertise, Authority, Trust)
- Original insights (not generic content mill copy)
- Actionable advice with specific examples
- Natural language (conversational, not keyword-stuffed)

TARGET PERFORMANCE:
- 45% organic traffic increase within 90 days
- Page 1 ranking for primary keyword within 60 days
- 5%+ conversion rate (visitor → lead)

OUTPUT: SEO-optimized content ready to publish`;

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { content_type, topic, business, target_keywords, location } = req.body;

  if (!content_type || !topic) {
    return res.status(400).json({
      error: 'Missing required fields',
      usage: 'POST with: { "content_type": "blog|gmb|service_page|neighborhood", "topic": "...", "business": {...}, "target_keywords": [...], "location": {...} }'
    });
  }

  try {
    const message = await anthropic.messages.create({
      model: 'claude-sonnet-4-20250514',
      max_tokens: 8000,
      temperature: 0.7,
      messages: [{
        role: 'user',
        content: `${SYSTEM_PROMPT}

CONTENT REQUEST:
Type: ${content_type}
Topic: ${topic}
Target Keywords: ${JSON.stringify(target_keywords || [])}

BUSINESS INFO:
${JSON.stringify(business, null, 2)}

LOCATION DATA:
${JSON.stringify(location, null, 2)}

Create ${content_type} content on topic: "${topic}". Return JSON:
{
  "title": "SEO-optimized title",
  "meta_title": "55-60 char meta title",
  "meta_description": "150-160 char meta description",
  "content": "Full content here (markdown format)...",
  "primary_keyword": "main keyword",
  "secondary_keywords": ["keyword2", "keyword3"],
  "schema_markup": {
    "type": "LocalBusiness",
    "code": "JSON-LD schema code..."
  },
  "internal_links": [
    {"text": "anchor text", "url": "/page-url"}
  ],
  "cta": "Primary call to action",
  "seo_score": 85,
  "readability_grade": 8,
  "estimated_traffic_per_month": 250,
  "target_ranking_days": 60
}`
      }]
    });

    const responseText = message.content[0].text;
    const jsonMatch = responseText.match(/\{[\s\S]*\}/);

    if (!jsonMatch) {
      throw new Error('No valid JSON in response');
    }

    const result = JSON.parse(jsonMatch[0]);
    result.created_at = new Date().toISOString();
    result.content_type = content_type;
    result.api_version = '1.0.0';

    return res.status(200).json(result);

  } catch (error) {
    console.error('Error:', error);
    return res.status(500).json({
      error: 'Failed to create content',
      details: error.message
    });
  }
}
