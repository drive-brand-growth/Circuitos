#!/usr/bin/env python3
"""
MetroFlex Gym Member Onboarding Agent
Purpose: Convert prospects into Miami members + reduce churn
Revenue Impact: $175k-$250k in Year 1 (70-100 Founder's @ $2,500)
Time-Sensitive: Founder's deadline May 15, 2026
"""

import os
import json
import logging
from typing import Dict, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
from openai import OpenAI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class MemberProspect:
    """Gym member prospect data"""
    name: str
    email: str
    phone: str
    workout_frequency: str  # "daily", "4-5x/week", "2-3x/week", "1x/week"
    budget: float
    commitment_level: int  # 1-10
    location: str
    query: str


class GymMemberOnboardingAgent:
    """
    AI Agent for MetroFlex Miami member conversion

    Key Capabilities:
    1. Membership tier recommendation
    2. Founder's membership FOMO messaging
    3. Savings calculation
    4. Trial class scheduling
    5. High-intent detection → GHL
    """

    def __init__(self, openai_api_key: str, knowledge_base_path: str):
        self.api_key = openai_api_key
        self._client = None  # Lazy initialization
        self.knowledge_base = self._load_knowledge_base(knowledge_base_path)
        self.model = "gpt-4o-mini"

        # Founder's membership tracking
        self.founders_total = 100
        self.founders_deadline = datetime(2026, 5, 15)

    def _get_openai_client(self):
        """Get or create OpenAI client (lazy initialization)"""
        if self._client is None:
            if not self.api_key:
                raise ValueError("OPENAI_API_KEY not provided")
            self._client = OpenAI(api_key=self.api_key)
        return self._client

    def _load_knowledge_base(self, path: str) -> Dict:
        """Load gym knowledge base"""
        with open(path, 'r') as f:
            kb = json.load(f)
        return kb.get('metroflex_gym_miami', {})

    def calculate_membership_recommendation(self, prospect: MemberProspect) -> Dict:
        """
        Recommend best membership tier

        Tiers:
        - Founder's: $2,500 one-time (LIFETIME, limited to 100)
        - Annual: $899/year (saves $169 vs monthly)
        - Monthly: $89/month
        - 10-Pack: $99 (10 day passes, saves $51)
        - Day Pass: $15/day

        Logic:
        - High commitment (8+) + budget > $2000 → Founder's
        - Workout 4-5x/week + budget > $800 → Annual
        - Workout 2-3x/week → Monthly
        - Trying it out → 10-Pack or Day Pass
        """
        recommendation = {}

        # Founder's urgency check
        days_until_deadline = (self.founders_deadline - datetime.now()).days
        founders_urgency = days_until_deadline <= 180  # 6 months out

        # Decision tree
        if prospect.commitment_level >= 8 and prospect.budget >= 2500:
            recommendation = {
                'tier': "Founder's Membership",
                'price': 2500,
                'billing': 'One-time payment',
                'savings': 'UNLIMITED - Lifetime access, no recurring fees',
                'urgency': f'⚠️ LIMITED: Only 100 spots total. Deadline: May 15, 2026 ({days_until_deadline} days left)',
                'best_for': 'Serious lifters committed to MetroFlex legacy',
                'cta': 'Secure your Founder\'s spot NOW before they\'re gone!'
            }
        elif prospect.workout_frequency in ['daily', '4-5x/week'] and prospect.budget >= 899:
            recommendation = {
                'tier': 'Annual Membership',
                'price': 899,
                'billing': 'Paid annually',
                'savings': '$169/year (vs monthly at $89 x 12 = $1,068)',
                'best_for': 'Regular lifters (4-5x/week)',
                'cta': 'Save $169/year with Annual membership'
            }
        elif prospect.workout_frequency in ['2-3x/week', '1x/week']:
            recommendation = {
                'tier': 'Monthly Membership',
                'price': 89,
                'billing': 'Per month',
                'savings': 'Flexible - cancel anytime',
                'best_for': 'Regular lifters with flexibility',
                'cta': 'Start your journey with Monthly membership'
            }
        else:
            recommendation = {
                'tier': '10-Pack Day Passes',
                'price': 99,
                'billing': 'One-time (10 passes)',
                'savings': '$51 (vs 10 day passes at $15 each = $150)',
                'best_for': 'Trying MetroFlex or occasional visitors',
                'cta': 'Try us out with the 10-Pack'
            }

        recommendation['founders_urgency'] = founders_urgency

        return recommendation

    def calculate_founders_roi(self, years_planned: int = 10) -> Dict:
        """
        Calculate Founder's membership ROI vs other options

        Founder's: $2,500 one-time
        vs
        Annual: $899/year
        Monthly: $89/month = $1,068/year
        """
        founders_cost = 2500
        annual_cost_per_year = 899
        monthly_cost_per_year = 1068

        roi = {
            'founders_total_cost': founders_cost,
            'annual_total_cost_10yr': annual_cost_per_year * years_planned,
            'monthly_total_cost_10yr': monthly_cost_per_year * years_planned,
            'savings_vs_annual_10yr': (annual_cost_per_year * years_planned) - founders_cost,
            'savings_vs_monthly_10yr': (monthly_cost_per_year * years_planned) - founders_cost,
            'breakeven_years_annual': round(founders_cost / annual_cost_per_year, 1),
            'breakeven_years_monthly': round(founders_cost / monthly_cost_per_year, 1),
        }

        roi['message'] = f"""
💰 Founder's Membership ROI:

Pay once: $2,500
vs
Annual members pay: ${roi['annual_total_cost_10yr']:,} over 10 years
Monthly members pay: ${roi['monthly_total_cost_10yr']:,} over 10 years

YOU SAVE: ${roi['savings_vs_monthly_10yr']:,} over 10 years!

Breakeven: Just {roi['breakeven_years_monthly']} years vs monthly (2.8 years vs annual)

After that? FREE FOREVER. That's the Founder's advantage.
"""

        return roi

    def generate_response(self, query: str, prospect_data: Optional[Dict] = None) -> Dict:
        """
        Generate AI response for gym membership inquiry

        Returns:
        {
            'response': str,
            'recommendation': dict (if prospect data provided),
            'high_intent': bool,
            'ghl_payload': dict (if high-intent)
        }
        """
        # System prompt
        system_prompt = f"""You are the MetroFlex Miami Gym Member Onboarding Agent.

Your mission: Convert prospects into members and create FOMO for Founder's memberships.

KNOWLEDGE BASE:
{json.dumps(self.knowledge_base, indent=2)}

TONE: Motivational, legacy-focused, urgent (for Founder's)

CURRENT SITUATION:
- MetroFlex Miami opens June 2026
- Founder's Membership: LIMITED to first 100 members
- Deadline: May 15, 2026
- Pre-sale started March 2026

MEMBERSHIP TIERS:
1. Founder's: $2,500 one-time → LIFETIME access (best value, LIMITED)
2. Annual: $899/year (saves $169 vs monthly)
3. Monthly: $89/month (flexible)
4. 10-Pack: $99 for 10 day passes (saves $51)
5. Day Pass: $15/day

FOUNDER'S URGENCY MESSAGING:
- "Only 100 Founder's spots TOTAL"
- "Lifetime access - pay once, train forever"
- "ROI: Breaks even in 2.3 years vs monthly"
- "After that? FREE FOREVER"
- "Deadline: May 15, 2026"

HIGH-INTENT SIGNALS (capture to GHL):
- "join", "membership", "sign up", "how much"
- "founder's membership"
- "lifetime access"
- Budget discussion
- Trial class request

NEXT STEPS:
- Recommend tier based on workout frequency + budget
- Calculate savings
- Create urgency for Founder's
- Offer trial class (2-week pass: $25)
- Capture to GHL if interested

Always emphasize the MetroFlex legacy and community."""

        # Detect high-intent
        high_intent_keywords = [
            'join', 'membership', 'sign up', 'how much', 'cost', 'price',
            'founder', 'lifetime', 'annual', 'monthly', 'trial', 'visit'
        ]

        high_intent = any(keyword in query.lower() for keyword in high_intent_keywords)

        # Generate AI response
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query}
        ]

        response = self._get_openai_client().chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.7,
            max_tokens=700
        )

        ai_response = response.choices[0].message.content

        result = {
            'response': ai_response,
            'high_intent': high_intent
        }

        # Calculate recommendation if prospect data provided
        if prospect_data:
            prospect = MemberProspect(**prospect_data)
            recommendation = self.calculate_membership_recommendation(prospect)
            result['recommendation'] = recommendation

            # Add ROI if Founder's recommended
            if recommendation['tier'] == "Founder's Membership":
                result['founders_roi'] = self.calculate_founders_roi()

            # Prepare GHL payload if high intent
            if high_intent or recommendation['tier'] == "Founder's Membership":
                opportunity_value = recommendation['price']

                result['ghl_payload'] = {
                    'contact': {
                        'name': prospect.name,
                        'email': prospect.email,
                        'phone': prospect.phone,
                        'tags': [
                            'Miami Gym - Prospect',
                            recommendation['tier'],
                            'High Priority' if recommendation['tier'] == "Founder's Membership" else 'Standard'
                        ],
                        'custom_fields': {
                            'workout_frequency': prospect.workout_frequency,
                            'budget': prospect.budget,
                            'recommended_tier': recommendation['tier'],
                            'location': prospect.location
                        }
                    },
                    'opportunity': {
                        'name': f"Membership - {prospect.name}",
                        'value': opportunity_value,
                        'stage': "Founder's - Hot Lead" if recommendation['tier'] == "Founder's Membership" else 'Membership - Prospect',
                        'assigned_to': 'Brian Dobson'
                    },
                    'alert': {
                        'type': 'founders_lead' if recommendation['tier'] == "Founder's Membership" else 'membership_inquiry',
                        'message': f"New {recommendation['tier']} prospect: {prospect.name}"
                    }
                }

        return result


def main():
    """Test the Gym Member Agent"""
    api_key = os.getenv('OPENAI_API_KEY')
    kb_path = 'METROFLEX_GYM_KB_V1.json'

    agent = GymMemberOnboardingAgent(api_key, kb_path)

    # Test query
    test_query = "I'm interested in joining MetroFlex Miami. What are the membership options?"

    # Test prospect
    test_prospect = {
        'name': 'Sarah Johnson',
        'email': 'sarah@example.com',
        'phone': '555-5678',
        'workout_frequency': 'daily',
        'budget': 3000,
        'commitment_level': 9,
        'location': 'Miami, FL',
        'query': test_query
    }

    result = agent.generate_response(test_query, test_prospect)

    print("=== GYM MEMBER AGENT RESPONSE ===")
    print(f"\nQuery: {test_query}")
    print(f"\nAI Response:\n{result['response']}")
    print(f"\nHigh Intent: {result['high_intent']}")

    if 'recommendation' in result:
        rec = result['recommendation']
        print(f"\n=== MEMBERSHIP RECOMMENDATION ===")
        print(f"Tier: {rec['tier']}")
        print(f"Price: ${rec['price']}")
        print(f"Savings: {rec['savings']}")
        print(f"CTA: {rec['cta']}")

    if 'founders_roi' in result:
        print(result['founders_roi']['message'])

    if 'ghl_payload' in result:
        print(f"\n=== GHL PAYLOAD ===")
        print(json.dumps(result['ghl_payload'], indent=2))


if __name__ == '__main__':
    main()
