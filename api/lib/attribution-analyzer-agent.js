/**
 * Attribution Analyzer - Multi-Touch Attribution
 * 
 * Tracks which touchpoints contribute to conversions:
 * - First-touch attribution (what brought them in)
 * - Last-touch attribution (what closed the deal)
 * - Time-decay attribution (recent touches weighted more)
 * - Channel ROI analysis
 */

import Anthropic from '@anthropic-ai/sdk';

const anthropic = new Anthropic({ apiKey: process.env.CLAUDE_API_KEY });

const ATTRIBUTION_ANALYZER_PROMPT = `You are the **Attribution Analyzer**, tracking multi-touch attribution across the customer journey.

## ATTRIBUTION MODELS

### Time-Decay Model (Recommended)
- Recent touches get more credit
- Formula: Credit = 2^(-days_ago/7)
- Example: Touch 1 day ago = 1.0x credit, 7 days ago = 0.5x, 14 days ago = 0.25x

### Conversion Path Analysis
Track typical journey:
1. Social media post (awareness)
2. Website visit (consideration)
3. Email open (engagement)
4. Demo request (intent)
5. Sales call (decision)
6. Closed deal (conversion)

## CHANNEL ROI CALCULATION

ROI = (Revenue - Cost) / Cost

Channel Performance:
- LinkedIn: Spent $20K, Generated $100K revenue = 4:1 ROI
- Email: Spent $5K, Generated $40K revenue = 7:1 ROI
- Paid Ads: Spent $15K, Generated $20K revenue = 0.33:1 ROI (KILL)

## OUTPUT: Attribution breakdown + channel ROI + optimization recommendations`;

export async function analyzeAttribution(customerJourneys, channelSpend, revenue) {
  const message = await anthropic.messages.create({
    model: 'claude-sonnet-4-5-20250929',
    max_tokens: 3096,
    temperature: 0.2,
    system: ATTRIBUTION_ANALYZER_PROMPT,
    messages: [{ role: 'user', content: `Journeys: ${JSON.stringify(customerJourneys)}\nSpend: ${JSON.stringify(channelSpend)}\nRevenue: ${JSON.stringify(revenue)}\n\nAnalyze attribution.` }]
  });

  return { attribution_analysis: JSON.parse(message.content[0].text.match(/\{[\s\S]*\}/)[0]), token_usage: message.usage };
}

export default analyzeAttribution;
