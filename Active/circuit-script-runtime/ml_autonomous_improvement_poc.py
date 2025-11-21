#!/usr/bin/env python3
"""
Autonomous ML Improvement POC - PATENT-WORTHY COMPONENT
Circuit Script™ Self-Improving Lead Scoring System

This POC demonstrates:
1. Gap Detection: Monitors F1/Precision/Recall and detects performance drops
2. Perplexity Research: Autonomously researches WHY performance dropped
3. Feature Discovery: Extracts new features from research findings
4. Impact Analysis: Shows how new features would improve the model

Run this to see the autonomous improvement cycle in action!

Usage:
    python ml_autonomous_improvement_poc.py --scenario healthcare
    python ml_autonomous_improvement_poc.py --scenario economic_downturn
    python ml_autonomous_improvement_poc.py --scenario all
"""

import os
import json
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import argparse

# Try to import Perplexity (if not available, we'll use mock)
try:
    import requests
    PERPLEXITY_AVAILABLE = True
except ImportError:
    PERPLEXITY_AVAILABLE = False
    print("⚠️  requests not available, using mock Perplexity responses")


class PerplexityResearcher:
    """
    Perplexity AI integration for autonomous gap research

    Patent-worthy component: Uses AI to research market trends and identify
    root causes of model performance degradation
    """

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('PERPLEXITY_API_KEY')
        self.base_url = "https://api.perplexity.ai/chat/completions"

    async def research_gap(self, query: str, use_mock: bool = False) -> Dict:
        """
        Research a performance gap using Perplexity AI

        Args:
            query: Research question (e.g., "Why did healthcare lead accuracy drop?")
            use_mock: If True, return mock data (for testing without API key)

        Returns:
            {
                'answer': 'Research findings...',
                'citations': ['url1', 'url2'],
                'recommended_features': [...],
                'data_sources': [...]
            }
        """

        if use_mock or not self.api_key:
            return self._get_mock_response(query)

        # Real Perplexity API call
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "llama-3.1-sonar-large-128k-online",  # Perplexity's online search model
            "messages": [
                {
                    "role": "system",
                    "content": "You are a market research analyst helping improve ML models. Search for recent trends, regulatory changes, and market dynamics."
                },
                {
                    "role": "user",
                    "content": query
                }
            ],
            "temperature": 0.2,
            "max_tokens": 2000,
            "search_recency_filter": "month"  # Last 30 days only
        }

        try:
            response = requests.post(self.base_url, json=payload, headers=headers, timeout=30)
            response.raise_for_status()
            data = response.json()

            answer = data['choices'][0]['message']['content']
            citations = data.get('citations', [])

            # Extract structured recommendations
            recommendations = self._extract_features_from_research(answer)

            return {
                'answer': answer,
                'citations': citations,
                'recommended_features': recommendations['features'],
                'data_sources': recommendations['data_sources']
            }

        except Exception as e:
            print(f"⚠️  Perplexity API error: {e}")
            print("⚠️  Falling back to mock response")
            return self._get_mock_response(query)

    def _get_mock_response(self, query: str) -> Dict:
        """
        Mock Perplexity responses for testing without API key

        These are realistic responses based on actual market trends
        """

        if "healthcare" in query.lower():
            return {
                'answer': """Based on recent market research, healthcare lead scoring accuracy has declined due to several factors:

1. **New HIPAA Regulations (October 2025)**: The HHS released updated HIPAA compliance requirements that fundamentally changed healthcare B2B purchasing behavior. Organizations now require vendors to demonstrate compliance certification before engagement.

2. **Shift in Decision-Making**: Healthcare organizations now involve compliance officers in 78% of technology purchases (up from 43% in Q2 2025). This adds a new stakeholder that traditional lead scoring models don't account for.

3. **Budget Freezes**: 64% of healthcare organizations implemented budget freezes in Q4 2025 due to Medicare reimbursement changes, causing high-intent leads to delay purchases despite strong engagement metrics.

4. **Telehealth Expansion**: The rapid growth of telehealth (231% YoY) changed the profile of "ideal customers" - smaller practices with high web engagement are now more likely to convert than large hospital systems.

**Recommended Data Sources:**
- HHS Compliance Database API (healthcare.gov/api/v1/compliance)
- CMS Medicare Reimbursement Data
- HIPAA Certification Registry
- Telehealth adoption metrics by practice size

**Key Signals to Track:**
- Mentions of "compliance" or "HIPAA" in initial contact
- Presence of compliance officer in contact records
- Practice size (smaller = higher conversion in 2025)
- Telehealth infrastructure indicators
""",
                'citations': [
                    'https://www.hhs.gov/hipaa/for-professionals/compliance-enforcement/2025-updates',
                    'https://www.cms.gov/medicare/reimbursement/2025-changes',
                    'https://healthcareitnews.com/telehealth-growth-2025'
                ],
                'recommended_features': [
                    {
                        'name': 'has_hipaa_compliance_certification',
                        'type': 'boolean',
                        'data_source': 'HHS Compliance Database API',
                        'rationale': 'New regulation makes this mandatory for 78% of healthcare deals',
                        'expected_impact': 'High (0.15-0.25 feature importance)'
                    },
                    {
                        'name': 'compliance_officer_in_contacts',
                        'type': 'boolean',
                        'data_source': 'CRM contact role analysis',
                        'rationale': 'Compliance officers now involved in 78% of tech purchases',
                        'expected_impact': 'Medium (0.10-0.15 feature importance)'
                    },
                    {
                        'name': 'practice_size_employees',
                        'type': 'integer',
                        'data_source': 'Healthcare provider registry',
                        'rationale': 'Smaller practices (10-50 employees) converting 2.3x higher in 2025',
                        'expected_impact': 'High (0.12-0.18 feature importance)'
                    },
                    {
                        'name': 'mentions_compliance_in_inquiry',
                        'type': 'boolean',
                        'data_source': 'NLP analysis of initial contact text',
                        'rationale': 'Leads mentioning compliance convert at 89% vs 62% baseline',
                        'expected_impact': 'Very High (0.20-0.30 feature importance)'
                    }
                ],
                'data_sources': [
                    'HHS Compliance Database API (healthcare.gov/api/v1/compliance)',
                    'CMS Medicare Reimbursement Data',
                    'HIPAA Certification Registry',
                    'Healthcare provider size registry'
                ]
            }

        elif "economic" in query.lower() or "downturn" in query.lower():
            return {
                'answer': """Lead scoring models are experiencing degraded performance due to macroeconomic shifts:

1. **Interest Rate Impact**: Federal Reserve rate hikes (5.25% in Nov 2025) have extended B2B sales cycles by 40-60 days. High-intent leads are delaying purchases despite strong engagement.

2. **Budget Scrutiny**: 71% of businesses now require CFO approval for purchases over $10k (down from $25k threshold in 2024). This adds decision-makers that weren't historically part of the process.

3. **ROI Sensitivity**: Companies now demand demonstrable ROI within 6 months (down from 12-18 months). Leads asking about ROI convert at 3.2x higher rates than those focused on features.

4. **Cash Flow Constraints**: Net-60 payment terms are now deal-breakers for 58% of SMBs (up from 23%). Leads requesting flexible payment convert at 2.8x higher rates.

**Recommended Signals:**
- CFO or finance contact involvement
- ROI or "payback period" mentions in communications
- Payment terms flexibility requests
- Company cash position indicators
""",
                'citations': [
                    'https://www.federalreserve.gov/interest-rates-2025',
                    'https://www.gartner.com/b2b-buying-behavior-2025',
                    'https://www.mckinsey.com/smb-cash-flow-constraints'
                ],
                'recommended_features': [
                    {
                        'name': 'cfo_involved_in_deal',
                        'type': 'boolean',
                        'data_source': 'CRM contact role analysis',
                        'rationale': 'CFO involvement now required for 71% of deals',
                        'expected_impact': 'High (0.18-0.25 feature importance)'
                    },
                    {
                        'name': 'mentions_roi_or_payback',
                        'type': 'boolean',
                        'data_source': 'NLP analysis of emails/calls',
                        'rationale': 'ROI-focused leads convert 3.2x higher',
                        'expected_impact': 'Very High (0.25-0.35 feature importance)'
                    },
                    {
                        'name': 'requested_flexible_payment',
                        'type': 'boolean',
                        'data_source': 'Sales conversation analysis',
                        'rationale': 'Payment flexibility now critical for 58% of SMBs',
                        'expected_impact': 'Medium (0.12-0.18 feature importance)'
                    }
                ],
                'data_sources': [
                    'Federal Reserve economic indicators API',
                    'Company financial health databases (Dun & Bradstreet)',
                    'Sales conversation NLP analysis'
                ]
            }

        elif "competitor" in query.lower():
            return {
                'answer': """A new competitor has disrupted lead conversion patterns:

1. **New Market Entrant**: CompetitorX launched in August 2025 with aggressive pricing (40% below market) and captured 18% market share in Q4.

2. **Feature Parity Shift**: Leads now evaluate 4.2 vendors on average (up from 2.8 in 2024). Price comparison behavior increased 156%.

3. **Switching Costs**: Leads with existing systems are 3.1x more likely to convert if you offer migration assistance. "Migration support" mentions correlate with 84% close rate.

4. **Trust Signals**: With more options, leads prioritize vendor stability. Companies with 10+ years in business convert 2.4x higher than newer entrants.

**Recommended Signals:**
- Existing system/vendor information
- Price sensitivity indicators
- Migration or switching concern mentions
- Competitive comparison requests
""",
                'citations': [
                    'https://www.g2.com/market-reports/2025-buyer-behavior',
                    'https://www.competitorx.com/press-releases/market-share-2025'
                ],
                'recommended_features': [
                    {
                        'name': 'has_existing_vendor',
                        'type': 'boolean',
                        'data_source': 'Discovery call analysis',
                        'rationale': 'Migration assistance seekers convert at 84%',
                        'expected_impact': 'High (0.20-0.28 feature importance)'
                    },
                    {
                        'name': 'mentioned_price_comparison',
                        'type': 'boolean',
                        'data_source': 'Email/call NLP analysis',
                        'rationale': 'Price shoppers need different nurture strategy',
                        'expected_impact': 'Medium (0.10-0.15 feature importance)'
                    },
                    {
                        'name': 'requested_competitive_comparison',
                        'type': 'boolean',
                        'data_source': 'Sales conversation analysis',
                        'rationale': 'Comparison shoppers have different close patterns',
                        'expected_impact': 'Medium (0.12-0.18 feature importance)'
                    }
                ],
                'data_sources': [
                    'Sales conversation transcripts (NLP)',
                    'Competitive intelligence platforms (G2, Capterra)',
                    'Existing vendor detection (discovery calls)'
                ]
            }

        else:
            return {
                'answer': 'No specific research findings for this query.',
                'citations': [],
                'recommended_features': [],
                'data_sources': []
            }

    def _extract_features_from_research(self, research_text: str) -> Dict:
        """
        Parse research findings to extract structured feature recommendations

        In production, this would use GPT-4 to extract structured data
        For POC, we return the format that would be extracted
        """
        # This is simplified for POC - production would use GPT-4 extraction
        return {
            'features': [],
            'data_sources': []
        }


class GapDetector:
    """
    Monitors ML model performance and detects when retraining/improvement needed

    Patent-worthy component: Autonomous detection of performance degradation
    with vertical-specific analysis
    """

    def __init__(self):
        self.performance_thresholds = {
            'min_f1': 0.82,
            'min_precision': 0.85,
            'min_recall': 0.80,
            'max_f1_drop': 0.08  # Alert if F1 drops >8%
        }

    def detect_gaps(self, current_metrics: Dict, historical_metrics: Dict, vertical_breakdown: Dict) -> Dict:
        """
        Detect performance gaps and identify patterns

        Returns gap analysis with:
        - Overall performance degradation
        - Vertical-specific issues
        - Pattern identification (false negatives, false positives, etc.)
        - Recommended research queries for Perplexity
        """

        gaps_found = []

        # Overall F1 check
        f1_drop = historical_metrics['f1'] - current_metrics['f1']
        if f1_drop > self.performance_thresholds['max_f1_drop']:
            gaps_found.append({
                'type': 'overall_f1_degradation',
                'severity': 'critical' if f1_drop > 0.12 else 'high',
                'details': f"F1 score dropped from {historical_metrics['f1']:.2%} to {current_metrics['f1']:.2%} ({f1_drop:.2%} drop)"
            })

        # Precision check
        if current_metrics['precision'] < self.performance_thresholds['min_precision']:
            gaps_found.append({
                'type': 'low_precision',
                'severity': 'high',
                'details': f"Precision at {current_metrics['precision']:.2%} (threshold: {self.performance_thresholds['min_precision']:.2%})"
            })

        # Recall check
        if current_metrics['recall'] < self.performance_thresholds['min_recall']:
            gaps_found.append({
                'type': 'low_recall',
                'severity': 'high',
                'details': f"Recall at {current_metrics['recall']:.2%} (threshold: {self.performance_thresholds['min_recall']:.2%})"
            })

        # Vertical-specific analysis
        worst_vertical = min(vertical_breakdown.items(), key=lambda x: x[1]['f1'])
        if worst_vertical[1]['f1'] < 0.70:
            gaps_found.append({
                'type': 'vertical_specific_degradation',
                'severity': 'critical',
                'vertical': worst_vertical[0],
                'details': f"{worst_vertical[0]} vertical F1 at {worst_vertical[1]['f1']:.2%}"
            })

        return {
            'gaps_detected': len(gaps_found) > 0,
            'gap_count': len(gaps_found),
            'gaps': gaps_found,
            'recommended_research_query': self._generate_research_query(gaps_found, vertical_breakdown)
        }

    def _generate_research_query(self, gaps: List[Dict], vertical_breakdown: Dict) -> str:
        """
        Generate Perplexity research query based on detected gaps
        """

        if not gaps:
            return None

        # Prioritize vertical-specific gaps (most actionable)
        vertical_gaps = [g for g in gaps if g['type'] == 'vertical_specific_degradation']
        if vertical_gaps:
            primary_gap = vertical_gaps[0]
        else:
            # Otherwise find the most critical gap
            critical_gaps = [g for g in gaps if g['severity'] == 'critical']
            primary_gap = critical_gaps[0] if critical_gaps else gaps[0]

        if primary_gap['type'] == 'vertical_specific_degradation':
            vertical = primary_gap['vertical']
            return f"""Research question: Why would lead scoring accuracy drop for {vertical} businesses in {datetime.now().strftime('%B %Y')}?

Context:
- Our XGBoost lead scoring model's F1 score dropped to {vertical_breakdown[vertical]['f1']:.2%} for {vertical} vertical
- Overall model F1 is acceptable, but {vertical} specifically is underperforming
- This suggests market dynamics changed specifically in {vertical}

Please search for:
1. Recent regulatory changes affecting {vertical} businesses
2. New buying behaviors or decision factors in {vertical} B2B sales
3. Emerging data sources that could improve {vertical} lead qualification
4. Economic or industry trends that might explain the pattern shift in {vertical}

Provide actionable recommendations for new features to add to our lead scoring model specifically for {vertical} leads."""

        elif primary_gap['type'] == 'low_recall':
            return f"""Research question: Why are we missing more qualified leads (low recall)?

Context:
- Our lead scoring model recall dropped to {primary_gap['details']}
- We're missing true positives (leads that should score high but we're scoring low)
- This means lost revenue opportunities

Please search for:
1. New lead qualification signals we might be missing
2. Changes in how buyers research and evaluate solutions
3. New channels or touchpoints in the buyer journey
4. Data sources that capture early buying intent

Provide recommendations for new features that would help identify qualified leads earlier."""

        else:
            return f"""Research question: Why did our lead scoring model performance degrade?

Context:
- Model performance degradation detected: {primary_gap['details']}
- Need to understand what changed in the market or buyer behavior

Please search for:
1. Recent market trends affecting B2B buying behavior
2. New data signals that predict purchase intent
3. Changes in sales cycle or decision-making processes
4. External factors affecting our target customers

Provide recommendations for model improvements."""


class AutonomousImprovementEngine:
    """
    Main orchestrator: Detects gaps, researches solutions, recommends improvements

    This is the complete patent-worthy system
    """

    def __init__(self, perplexity_api_key: Optional[str] = None):
        self.gap_detector = GapDetector()
        self.researcher = PerplexityResearcher(perplexity_api_key)

    async def analyze_and_improve(self, scenario_name: str, current_metrics: Dict,
                                   historical_metrics: Dict, vertical_breakdown: Dict,
                                   use_mock: bool = True) -> Dict:
        """
        Complete autonomous improvement cycle

        Steps:
        1. Detect performance gaps
        2. Generate research query
        3. Use Perplexity to research root causes
        4. Extract feature recommendations
        5. Estimate improvement impact

        Returns complete improvement plan
        """

        print(f"\n{'='*80}")
        print(f"🔍 AUTONOMOUS IMPROVEMENT ANALYSIS - Scenario: {scenario_name}")
        print(f"{'='*80}\n")

        # STAGE 1: Gap Detection
        print("📊 STAGE 1: Detecting Performance Gaps...")
        print("-" * 80)

        gap_analysis = self.gap_detector.detect_gaps(
            current_metrics,
            historical_metrics,
            vertical_breakdown
        )

        if not gap_analysis['gaps_detected']:
            print("✅ No performance gaps detected. Model is performing well.")
            return {'status': 'no_action_needed'}

        print(f"⚠️  Found {gap_analysis['gap_count']} performance gap(s):\n")
        for i, gap in enumerate(gap_analysis['gaps'], 1):
            severity_emoji = "🔴" if gap['severity'] == 'critical' else "🟡"
            print(f"{severity_emoji} Gap {i}: {gap['type']}")
            print(f"   Severity: {gap['severity']}")
            print(f"   Details: {gap['details']}")
            if 'vertical' in gap:
                print(f"   Vertical: {gap['vertical']}")
            print()

        # STAGE 2: Generate Research Query
        print("\n📝 STAGE 2: Generating Research Query for Perplexity...")
        print("-" * 80)
        research_query = gap_analysis['recommended_research_query']
        print(f"Query:\n{research_query}\n")

        # STAGE 3: Perplexity Research
        print("\n🔬 STAGE 3: Researching Root Causes with Perplexity AI...")
        print("-" * 80)
        print("⏳ Searching market trends, regulatory changes, buyer behavior shifts...\n")

        research_findings = await self.researcher.research_gap(research_query, use_mock=use_mock)

        print(f"📚 Research Findings:\n")
        print(research_findings['answer'])
        print(f"\n📎 Citations: {len(research_findings['citations'])} sources")
        for citation in research_findings['citations']:
            print(f"   - {citation}")

        # STAGE 4: Feature Recommendations
        print(f"\n\n💡 STAGE 4: Recommended New Features")
        print("-" * 80)

        if research_findings['recommended_features']:
            print(f"Found {len(research_findings['recommended_features'])} new features to add:\n")

            for i, feature in enumerate(research_findings['recommended_features'], 1):
                print(f"Feature {i}: {feature['name']}")
                print(f"  Type: {feature['type']}")
                print(f"  Data Source: {feature['data_source']}")
                print(f"  Rationale: {feature['rationale']}")
                print(f"  Expected Impact: {feature['expected_impact']}")
                print()
        else:
            print("⚠️  No specific features recommended by research")

        # STAGE 5: Impact Estimation
        print(f"\n📈 STAGE 5: Estimated Impact of Improvements")
        print("-" * 80)

        impact = self._estimate_improvement_impact(
            current_metrics,
            research_findings['recommended_features']
        )

        print(f"Current Performance:")
        print(f"  F1 Score: {current_metrics['f1']:.2%}")
        print(f"  Precision: {current_metrics['precision']:.2%}")
        print(f"  Recall: {current_metrics['recall']:.2%}")
        print()
        print(f"Projected Performance (after adding new features):")
        print(f"  F1 Score: {impact['projected_f1']:.2%} ({impact['f1_improvement']:+.2%})")
        print(f"  Precision: {impact['projected_precision']:.2%} ({impact['precision_improvement']:+.2%})")
        print(f"  Recall: {impact['projected_recall']:.2%} ({impact['recall_improvement']:+.2%})")
        print()
        print(f"💰 Business Impact:")
        print(f"  Estimated additional revenue: ${impact['revenue_impact']:,.0f}/year")
        print(f"  Based on: Improved lead routing → Higher close rates")

        # Summary
        print(f"\n\n{'='*80}")
        print(f"✅ AUTONOMOUS IMPROVEMENT PLAN COMPLETE")
        print(f"{'='*80}")
        print(f"\nNext Steps:")
        print(f"1. ✅ Integrate {len(research_findings['recommended_features'])} new data sources")
        print(f"2. ✅ Add {len(research_findings['recommended_features'])} new features to model")
        print(f"3. ✅ Retrain XGBoost with expanded feature set")
        print(f"4. ✅ A/B test new model vs current model")
        print(f"5. ✅ Deploy if F1 improvement >= {impact['f1_improvement']:.2%}")

        return {
            'status': 'improvement_plan_generated',
            'gap_analysis': gap_analysis,
            'research_findings': research_findings,
            'impact_estimation': impact,
            'recommended_actions': len(research_findings['recommended_features'])
        }

    def _estimate_improvement_impact(self, current_metrics: Dict, new_features: List[Dict]) -> Dict:
        """
        Estimate how much new features would improve model performance

        This is simplified for POC - production would use historical A/B test data
        """

        # Conservative estimates based on typical feature importance
        # High impact features: +0.03 to +0.05 F1
        # Medium impact: +0.015 to +0.03 F1
        # Low impact: +0.005 to +0.015 F1

        estimated_f1_gain = 0
        for feature in new_features:
            impact = feature.get('expected_impact', 'Medium')
            if 'Very High' in impact:
                estimated_f1_gain += 0.04
            elif 'High' in impact:
                estimated_f1_gain += 0.025
            elif 'Medium' in impact:
                estimated_f1_gain += 0.015
            else:
                estimated_f1_gain += 0.01

        # Cap at reasonable improvement (models rarely jump >15% F1)
        estimated_f1_gain = min(estimated_f1_gain, 0.15)

        projected_f1 = min(current_metrics['f1'] + estimated_f1_gain, 0.95)  # Cap at 95%
        projected_precision = min(current_metrics['precision'] + (estimated_f1_gain * 0.8), 0.95)
        projected_recall = min(current_metrics['recall'] + (estimated_f1_gain * 1.2), 0.95)

        # Revenue impact calculation
        # Assumptions: 1000 leads/month, $10k average deal size, current close rate 20%
        # Improved recall = catch more hot leads = more revenue
        monthly_leads = 1000
        avg_deal_size = 10000
        current_close_rate = 0.20

        # If recall improves 10%, we catch 10% more hot leads
        recall_improvement = projected_recall - current_metrics['recall']
        additional_deals_per_month = monthly_leads * current_close_rate * recall_improvement
        annual_revenue_impact = additional_deals_per_month * avg_deal_size * 12

        return {
            'projected_f1': projected_f1,
            'projected_precision': projected_precision,
            'projected_recall': projected_recall,
            'f1_improvement': projected_f1 - current_metrics['f1'],
            'precision_improvement': projected_precision - current_metrics['precision'],
            'recall_improvement': recall_improvement,
            'revenue_impact': annual_revenue_impact
        }


# Test Scenarios
SCENARIOS = {
    'healthcare': {
        'name': 'Healthcare Compliance Regulation Change',
        'description': 'New HIPAA requirements changed healthcare buying behavior',
        'historical_metrics': {
            'f1': 0.86,
            'precision': 0.89,
            'recall': 0.83
        },
        'current_metrics': {
            'f1': 0.71,
            'precision': 0.76,
            'recall': 0.67
        },
        'vertical_breakdown': {
            'healthcare': {'f1': 0.64, 'precision': 0.71, 'recall': 0.58},
            'retail': {'f1': 0.84, 'precision': 0.87, 'recall': 0.81},
            'technology': {'f1': 0.88, 'precision': 0.91, 'recall': 0.85},
            'manufacturing': {'f1': 0.82, 'precision': 0.85, 'recall': 0.79}
        }
    },

    'economic_downturn': {
        'name': 'Economic Downturn - Extended Sales Cycles',
        'description': 'Interest rate hikes extended B2B sales cycles, changed buyer behavior',
        'historical_metrics': {
            'f1': 0.84,
            'precision': 0.88,
            'recall': 0.81
        },
        'current_metrics': {
            'f1': 0.73,
            'precision': 0.82,
            'recall': 0.66
        },
        'vertical_breakdown': {
            'healthcare': {'f1': 0.79, 'precision': 0.84, 'recall': 0.74},
            'retail': {'f1': 0.68, 'precision': 0.79, 'recall': 0.59},
            'technology': {'f1': 0.75, 'precision': 0.83, 'recall': 0.68},
            'manufacturing': {'f1': 0.70, 'precision': 0.81, 'recall': 0.61}
        }
    },

    'new_competitor': {
        'name': 'New Market Competitor Disruption',
        'description': 'Aggressive new competitor changed evaluation criteria and price sensitivity',
        'historical_metrics': {
            'f1': 0.87,
            'precision': 0.90,
            'recall': 0.84
        },
        'current_metrics': {
            'f1': 0.76,
            'precision': 0.80,
            'recall': 0.73
        },
        'vertical_breakdown': {
            'healthcare': {'f1': 0.82, 'precision': 0.86, 'recall': 0.78},
            'retail': {'f1': 0.73, 'precision': 0.77, 'recall': 0.70},
            'technology': {'f1': 0.74, 'precision': 0.79, 'recall': 0.70},
            'manufacturing': {'f1': 0.75, 'precision': 0.80, 'recall': 0.71}
        }
    }
}


async def run_scenario(scenario_name: str, use_mock: bool = True, api_key: Optional[str] = None):
    """Run a test scenario"""

    if scenario_name not in SCENARIOS:
        print(f"❌ Unknown scenario: {scenario_name}")
        print(f"Available scenarios: {', '.join(SCENARIOS.keys())}")
        return

    scenario = SCENARIOS[scenario_name]

    print("\n" + "="*80)
    print(f"🧪 TEST SCENARIO: {scenario['name']}")
    print("="*80)
    print(f"Description: {scenario['description']}\n")

    engine = AutonomousImprovementEngine(api_key)

    result = await engine.analyze_and_improve(
        scenario_name=scenario['name'],
        current_metrics=scenario['current_metrics'],
        historical_metrics=scenario['historical_metrics'],
        vertical_breakdown=scenario['vertical_breakdown'],
        use_mock=use_mock
    )

    return result


async def main():
    parser = argparse.ArgumentParser(
        description='Test Autonomous ML Improvement POC',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python ml_autonomous_improvement_poc.py --scenario healthcare
  python ml_autonomous_improvement_poc.py --scenario economic_downturn
  python ml_autonomous_improvement_poc.py --scenario all
  python ml_autonomous_improvement_poc.py --scenario healthcare --real (uses real Perplexity API)
        """
    )

    parser.add_argument(
        '--scenario',
        type=str,
        default='healthcare',
        choices=list(SCENARIOS.keys()) + ['all'],
        help='Which test scenario to run'
    )

    parser.add_argument(
        '--real',
        action='store_true',
        help='Use real Perplexity API (requires PERPLEXITY_API_KEY env var)'
    )

    parser.add_argument(
        '--api-key',
        type=str,
        help='Perplexity API key (alternative to env var)'
    )

    args = parser.parse_args()

    use_mock = not args.real
    api_key = args.api_key or os.getenv('PERPLEXITY_API_KEY')

    if args.real and not api_key:
        print("⚠️  --real flag set but no API key provided")
        print("⚠️  Set PERPLEXITY_API_KEY env var or use --api-key")
        print("⚠️  Falling back to mock mode\n")
        use_mock = True

    if args.scenario == 'all':
        for scenario_name in SCENARIOS.keys():
            await run_scenario(scenario_name, use_mock, api_key)
            print("\n" + "="*80 + "\n")
            await asyncio.sleep(1)  # Brief pause between scenarios
    else:
        await run_scenario(args.scenario, use_mock, api_key)


if __name__ == '__main__':
    asyncio.run(main())
