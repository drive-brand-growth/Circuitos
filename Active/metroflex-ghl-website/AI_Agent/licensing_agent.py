#!/usr/bin/env python3
"""
MetroFlex Licensing Qualification Agent
Purpose: Qualify and nurture high-value licensing leads ($40,000-$60,000 per deal)
Revenue Impact: $120k-$600k in Year 1
"""

import os
import json
import logging
from typing import Dict, List, Optional
from dataclasses import dataclass
from openai import OpenAI

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class LicensingLead:
    """Licensing lead data structure"""
    name: str
    email: str
    phone: str
    liquid_capital: float
    industry_experience_years: int
    existing_gym: bool
    existing_gym_sqft: int
    location: str
    passion_score: int  # 1-10 self-reported
    query: str


class LicensingQualificationAgent:
    """
    AI Agent for qualifying MetroFlex licensing prospects

    Key Capabilities:
    1. Qualification Scoring (ML-based)
    2. Package Recommendation (New Build $60k vs Rebrand $40k)
    3. Application Guidance (8-step process)
    4. ROI Calculation
    5. High-intent detection → GHL webhook
    """

    def __init__(self, openai_api_key: str, knowledge_base_path: str):
        self.client = OpenAI(api_key=openai_api_key)
        self.knowledge_base = self._load_knowledge_base(knowledge_base_path)
        self.model = "gpt-4o-mini"

    def _load_knowledge_base(self, path: str) -> Dict:
        """Load licensing knowledge base"""
        with open(path, 'r') as f:
            kb = json.load(f)
        return kb.get('metroflex_licensing', {})

    def calculate_qualification_score(self, lead: LicensingLead) -> Dict:
        """
        Calculate licensing qualification score (0-100)

        Scoring Logic:
        - Liquid capital: 40 points (>$150k = full points)
        - Industry experience: 25 points (>3 years = full points)
        - Existing gym: 15 points (bonus for rebrand candidates)
        - Passion score: 20 points (self-reported 1-10, scaled to 20)

        Score Interpretation:
        - 85-100: Fast-track (immediate phone call)
        - 70-84: Qualified (standard process)
        - 50-69: Nurture (education sequence)
        - <50: Not qualified (refer to gym membership)
        """
        score = 0
        details = {}

        # Capital assessment (40 points max)
        if lead.liquid_capital >= 150000:
            capital_score = 40
        elif lead.liquid_capital >= 100000:
            capital_score = 30
        elif lead.liquid_capital >= 60000:
            capital_score = 20
        else:
            capital_score = 10

        score += capital_score
        details['capital_score'] = capital_score
        details['capital_requirement'] = '$150,000 liquid capital recommended'

        # Experience assessment (25 points max)
        if lead.industry_experience_years >= 5:
            experience_score = 25
        elif lead.industry_experience_years >= 3:
            experience_score = 20
        elif lead.industry_experience_years >= 1:
            experience_score = 15
        else:
            experience_score = 10

        score += experience_score
        details['experience_score'] = experience_score

        # Existing gym bonus (15 points max)
        if lead.existing_gym and lead.existing_gym_sqft >= 3000:
            gym_score = 15
            details['recommendation'] = 'Rebrand License ($40,000) - You have existing gym'
        elif lead.existing_gym:
            gym_score = 10
            details['recommendation'] = 'Rebrand License ($40,000) - Expand your gym first'
        else:
            gym_score = 5
            details['recommendation'] = 'New Build License ($60,000) - Build from scratch'

        score += gym_score
        details['gym_score'] = gym_score

        # Passion assessment (20 points max)
        passion_score = (lead.passion_score / 10) * 20
        score += passion_score
        details['passion_score'] = passion_score

        # Determine qualification level
        if score >= 85:
            qualification = 'FAST_TRACK'
            action = 'Immediate phone call within 24 hours'
        elif score >= 70:
            qualification = 'QUALIFIED'
            action = 'Standard application process'
        elif score >= 50:
            qualification = 'NURTURE'
            action = 'Educational email sequence'
        else:
            qualification = 'NOT_QUALIFIED'
            action = 'Refer to MetroFlex Miami membership'

        return {
            'total_score': round(score, 1),
            'qualification_level': qualification,
            'recommended_action': action,
            'details': details,
            'send_to_ghl': score >= 70  # Only qualified+ leads go to GHL
        }

    def get_package_details(self, recommendation: str) -> Dict:
        """Get licensing package details"""
        packages = self.knowledge_base.get('licensing_packages', [])

        for package in packages:
            if recommendation == 'New Build License ($60,000)' and package['name'] == 'New Build License':
                return package
            elif recommendation == 'Rebrand License ($40,000)' and package['name'] == 'Rebrand License':
                return package

        return {}

    def generate_response(self, query: str, lead_data: Optional[Dict] = None) -> Dict:
        """
        Generate AI response for licensing inquiry

        Returns:
        {
            'response': str,
            'qualification_score': dict (if lead data provided),
            'high_intent': bool,
            'ghl_payload': dict (if high-intent)
        }
        """
        # Build system prompt with knowledge base
        system_prompt = f"""You are the MetroFlex Licensing Qualification Agent.

Your mission: Qualify high-value licensing leads and guide them through the application process.

KNOWLEDGE BASE:
{json.dumps(self.knowledge_base, indent=2)}

TONE: Professional, encouraging, legacy-focused (Ronnie Coleman, Branch Warren heritage)

HIGH-INTENT SIGNALS (capture to GHL):
- "open a MetroFlex gym"
- "franchise opportunity" / "licensing cost"
- "how to become a licensee"
- "requirements to open"
- Capital discussion ($150k+)

QUALIFICATION PRIORITIES:
1. Liquid capital: $150k minimum required
2. Industry experience: 3+ years preferred
3. Passion for hardcore bodybuilding culture
4. Business plan readiness

PACKAGES:
- New Build License: $60,000 (build new gym from scratch)
- Rebrand License: $40,000 (rebrand existing gym)
- Beta Discount: $10,000 off for first 3 licensees

NEXT STEPS:
- If qualified → 8-step application process
- If interested → Application form + document checklist
- If unqualified → Refer to MetroFlex Miami membership

Always calculate ROI and emphasize the MetroFlex legacy."""

        # Detect high-intent
        high_intent_keywords = [
            'open a gym', 'franchise', 'licensing', 'licensee',
            'become a licensee', 'requirements', 'capital',
            'how much', 'cost', 'application', 'territory'
        ]

        high_intent = any(keyword in query.lower() for keyword in high_intent_keywords)

        # Generate AI response
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query}
        ]

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.7,
            max_tokens=800
        )

        ai_response = response.choices[0].message.content

        result = {
            'response': ai_response,
            'high_intent': high_intent
        }

        # Calculate qualification score if lead data provided
        if lead_data:
            lead = LicensingLead(**lead_data)
            qualification = self.calculate_qualification_score(lead)
            result['qualification_score'] = qualification

            # Prepare GHL payload if qualified
            if qualification['send_to_ghl']:
                result['ghl_payload'] = {
                    'contact': {
                        'name': lead.name,
                        'email': lead.email,
                        'phone': lead.phone,
                        'tags': [
                            'Licensing - Hot Lead',
                            qualification['qualification_level']
                        ],
                        'custom_fields': {
                            'liquid_capital': lead.liquid_capital,
                            'qualification_score': qualification['total_score'],
                            'recommended_package': qualification['details']['recommendation'],
                            'location': lead.location
                        }
                    },
                    'opportunity': {
                        'name': f"Licensing - {lead.name}",
                        'value': 40000 if 'Rebrand' in qualification['details']['recommendation'] else 60000,
                        'stage': 'Licensing Application - Qualification',
                        'assigned_to': 'Brian Dobson'
                    },
                    'alert': {
                        'type': 'high_value_lead' if qualification['total_score'] >= 85 else 'qualified_lead',
                        'message': f"New {qualification['qualification_level']} licensing lead: {lead.name} (Score: {qualification['total_score']})"
                    }
                }

        return result


def main():
    """Test the Licensing Agent"""
    # Test configuration
    api_key = os.getenv('OPENAI_API_KEY')
    kb_path = 'METROFLEX_EVENTS_KB_V3_EVENTS_ONLY.json'  # Will be updated with licensing KB

    agent = LicensingQualificationAgent(api_key, kb_path)

    # Test query
    test_query = "I'm interested in opening a MetroFlex gym in Austin, Texas. What are the requirements?"

    # Test lead data
    test_lead = {
        'name': 'John Smith',
        'email': 'john@example.com',
        'phone': '555-1234',
        'liquid_capital': 180000,
        'industry_experience_years': 5,
        'existing_gym': False,
        'existing_gym_sqft': 0,
        'location': 'Austin, TX',
        'passion_score': 9,
        'query': test_query
    }

    # Generate response
    result = agent.generate_response(test_query, test_lead)

    print("=== LICENSING AGENT RESPONSE ===")
    print(f"\nQuery: {test_query}")
    print(f"\nAI Response:\n{result['response']}")
    print(f"\nHigh Intent: {result['high_intent']}")

    if 'qualification_score' in result:
        score = result['qualification_score']
        print(f"\n=== QUALIFICATION SCORE ===")
        print(f"Total Score: {score['total_score']}/100")
        print(f"Level: {score['qualification_level']}")
        print(f"Action: {score['recommended_action']}")
        print(f"Send to GHL: {score['send_to_ghl']}")

    if 'ghl_payload' in result:
        print(f"\n=== GHL PAYLOAD ===")
        print(json.dumps(result['ghl_payload'], indent=2))


if __name__ == '__main__':
    main()
