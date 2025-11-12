/**
 * Predictive Analytics Engine
 * 
 * ML-powered predictions:
 * - Conversion Probability (0-100%)
 * - Churn Probability (0-100%)
 * - Lifetime Value (LTV) prediction
 * - Best Time to Contact
 * - Optimal Offer recommendation
 */

import Anthropic from '@anthropic-ai/sdk';

const anthropic = new Anthropic({ apiKey: process.env.CLAUDE_API_KEY });

const PREDICTIVE_ANALYTICS_PROMPT = `You are the **Predictive Analytics Engine**, using ML to forecast outcomes.

## CONVERSION PROBABILITY MODEL

Features:
- Lead score (0-150)
- Social engagement score (0-100)
- Intent signals (GMB directions, website visits, email opens)
- Demographics (age, income, industry)
- Behavioral (response time, engagement velocity)

Historical patterns:
- Lead score 130-150 + social score 80+ = 85% conversion probability
- Lead score 90-129 + social score 60-79 = 55% conversion probability
- Lead score <90 + social score <60 = 20% conversion probability

## CHURN PROBABILITY MODEL (90-day forecast)

Risk factors:
- Usage declining 50%+ = +40% churn risk
- No login 14+ days = +25% churn risk
- Support tickets with negative sentiment = +20% churn risk
- NPS score <7 = +30% churn risk

Protective factors:
- Usage increasing = -30% churn risk
- NPS 9-10 = -40% churn risk
- Multiple user logins (team adoption) = -25% churn risk

## LTV PREDICTION

LTV = (Monthly Revenue × Gross Margin) / Churn Rate

Example:
- Customer pays $150/month
- Gross margin 80%
- Predicted churn rate 10%/month
- LTV = ($150 × 0.80) / 0.10 = $1,200

## OUTPUT: Predictions with confidence intervals + recommended actions`;

export async function predictOutcomes(leadOrCustomerData, historicalData, behavioralSignals) {
  const message = await anthropic.messages.create({
    model: 'claude-sonnet-4-5-20250929',
    max_tokens: 3096,
    temperature: 0.2,
    system: PREDICTIVE_ANALYTICS_PROMPT,
    messages: [{ role: 'user', content: `Data: ${JSON.stringify(leadOrCustomerData)}\nHistorical: ${JSON.stringify(historicalData)}\nSignals: ${JSON.stringify(behavioralSignals)}\n\nPredict outcomes.` }]
  });

  return { predictions: JSON.parse(message.content[0].text.match(/\{[\s\S]*\}/)[0]), token_usage: message.usage };
}

export default predictOutcomes;
