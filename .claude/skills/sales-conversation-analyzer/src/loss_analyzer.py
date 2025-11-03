"""
Loss Analyzer - Analyzes non-converted opportunities to identify failure patterns
"""

from typing import Dict, List, Any, Tuple
from collections import Counter, defaultdict


class LossAnalyzer:
    """
    Analyzes lost deals and non-converted opportunities
    Identifies patterns, root causes, and preventable losses
    """

    def __init__(self, vector_store=None):
        """
        Initialize loss analyzer

        Args:
            vector_store: Vector store for comparing to successful patterns
        """
        self.vector_store = vector_store

    def analyze_loss(
        self,
        conversation_analysis: Any,
        actual_outcome: str = "lost"
    ) -> Dict[str, Any]:
        """
        Analyze why a deal was lost or didn't convert

        Args:
            conversation_analysis: Full conversation analysis object
            actual_outcome: Actual outcome (lost, no_response, etc.)

        Returns:
            Loss analysis with root causes and prevention strategies
        """
        # Identify root causes
        root_causes = self._identify_root_causes(conversation_analysis)

        # Determine if loss was preventable
        preventable, prevention_analysis = self._assess_preventability(
            conversation_analysis, root_causes
        )

        # Compare to successful conversations
        success_comparison = self._compare_to_success_patterns(
            conversation_analysis
        )

        # Identify critical moments
        critical_moments = self._identify_critical_moments(
            conversation_analysis, root_causes
        )

        # Generate prevention strategies
        prevention_strategies = self._generate_prevention_strategies(
            root_causes, critical_moments
        )

        # Calculate opportunity cost
        opportunity_cost = self._calculate_opportunity_cost(
            conversation_analysis
        )

        # Coaching recommendations
        coaching_recommendations = self._generate_coaching_recommendations(
            root_causes, prevention_analysis
        )

        return {
            "outcome": actual_outcome,
            "preventable": preventable,
            "preventability_score": prevention_analysis.get('score', 0),
            "root_causes": root_causes,
            "critical_moments": critical_moments,
            "success_comparison": success_comparison,
            "prevention_strategies": prevention_strategies,
            "opportunity_cost": opportunity_cost,
            "coaching_recommendations": coaching_recommendations,
            "similar_losses": self._find_similar_losses(conversation_analysis),
            "what_went_wrong": self._summarize_what_went_wrong(root_causes),
            "what_could_have_been_done": self._summarize_what_could_have_been(
                prevention_strategies
            )
        }

    def _identify_root_causes(self, analysis: Any) -> List[Dict[str, Any]]:
        """
        Identify root causes of the loss

        Categorizes causes by: Qualification, Discovery, Value, Objection Handling, Timing, External
        """
        root_causes = []

        buyer_signals = analysis.buyer_signals
        patterns = analysis.key_patterns
        flow = analysis.conversation_flow
        gap = analysis.gap_analysis

        # Cause 1: Poor Qualification
        if buyer_signals.get('authority') != 'decision_maker':
            root_causes.append({
                "category": "Qualification",
                "cause": "Not speaking with decision maker",
                "severity": "high",
                "preventable": True,
                "evidence": f"Authority: {buyer_signals.get('authority', 'unknown')}",
                "impact": "Cannot get to yes without economic buyer"
            })

        if buyer_signals.get('budget_qualification') != 'qualified':
            root_causes.append({
                "category": "Qualification",
                "cause": "Budget not confirmed",
                "severity": "high",
                "preventable": True,
                "evidence": f"Budget: {buyer_signals.get('budget_qualification', 'unknown')}",
                "impact": "Deals without budget rarely close"
            })

        # Cause 2: Insufficient Pain Discovery
        if buyer_signals.get('pain_level') == 'low':
            root_causes.append({
                "category": "Discovery",
                "cause": "Failed to uncover sufficient pain",
                "severity": "critical",
                "preventable": True,
                "evidence": f"Pain level: {buyer_signals.get('pain_level')}",
                "impact": "No pain = no urgency = no purchase"
            })

        pain_patterns = [p for p in patterns if 'pain' in p.get('pattern_type', '').lower()]
        if len(pain_patterns) < 2:
            root_causes.append({
                "category": "Discovery",
                "cause": "Insufficient pain amplification",
                "severity": "high",
                "preventable": True,
                "evidence": f"Only {len(pain_patterns)} pain discovery patterns",
                "impact": "Pain not amplified enough to create urgency"
            })

        # Cause 3: Weak Value Proposition
        value_patterns = [p for p in patterns if 'value' in p.get('pattern_type', '').lower()]
        if not value_patterns:
            root_causes.append({
                "category": "Value",
                "cause": "Value proposition not articulated",
                "severity": "critical",
                "preventable": True,
                "evidence": "No value articulation patterns detected",
                "impact": "Buyer doesn't understand value or ROI"
            })

        if buyer_signals.get('intent_score', 0) < 50:
            root_causes.append({
                "category": "Value",
                "cause": "Low buyer interest/intent",
                "severity": "high",
                "preventable": True,
                "evidence": f"Intent score: {buyer_signals.get('intent_score')}/100",
                "impact": "Buyer not engaged or not seeing value"
            })

        # Cause 4: Unhandled Objections
        objections = buyer_signals.get('objections', [])
        if objections:
            root_causes.append({
                "category": "Objection Handling",
                "cause": f"Unresolved objections: {', '.join(objections)}",
                "severity": "high",
                "preventable": True,
                "evidence": f"{len(objections)} objections not fully addressed",
                "impact": "Objections create barriers to purchase"
            })

        # Cause 5: Poor Conversation Flow
        if flow.get('structure_quality') == 'needs_improvement':
            root_causes.append({
                "category": "Process",
                "cause": "Poor conversation structure",
                "severity": "medium",
                "preventable": True,
                "evidence": f"Structure quality: {flow.get('structure_quality')}",
                "impact": "Conversation didn't follow proven frameworks"
            })

        missed = flow.get('missed_opportunities', [])
        if len(missed) >= 2:
            root_causes.append({
                "category": "Process",
                "cause": f"Missed critical phases",
                "severity": "high",
                "preventable": True,
                "evidence": f"Missed: {', '.join(missed[:3])}",
                "impact": "Incomplete sales process leads to incomplete buy-in"
            })

        # Cause 6: Timing Issues
        if buyer_signals.get('timeline') == 'long_term':
            root_causes.append({
                "category": "Timing",
                "cause": "No immediate timeline",
                "severity": "medium",
                "preventable": False,
                "evidence": f"Timeline: {buyer_signals.get('timeline')}",
                "impact": "Buyer not ready to purchase now"
            })

        # Cause 7: Competitive Pressure (inferred)
        if 'competitor' in str(buyer_signals.get('positive_indicators', [])).lower():
            root_causes.append({
                "category": "External",
                "cause": "Lost to competitor",
                "severity": "high",
                "preventable": True,
                "evidence": "Competitor mentioned in conversation",
                "impact": "Buyer chose alternative solution"
            })

        # Cause 8: Poor Pattern Execution
        if patterns:
            avg_effectiveness = sum(p.get('effectiveness', 0.5) for p in patterns) / len(patterns)
            if avg_effectiveness < 0.6:
                root_causes.append({
                    "category": "Execution",
                    "cause": "Poor technique execution",
                    "severity": "high",
                    "preventable": True,
                    "evidence": f"Average pattern effectiveness: {avg_effectiveness:.2f}",
                    "impact": "Techniques used but not executed effectively"
                })

        # Cause 9: Gap vs World-Class
        gap_score = gap.get('gap_score', 0)
        if gap_score > 0.2:
            root_causes.append({
                "category": "Skill Gap",
                "cause": "Significant gap vs world-class",
                "severity": "high",
                "preventable": True,
                "evidence": f"Gap score: {gap_score:.2f}",
                "impact": "Performance significantly below best practices"
            })

        # Sort by severity
        severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        root_causes.sort(key=lambda x: severity_order.get(x['severity'], 4))

        return root_causes

    def _assess_preventability(
        self,
        analysis: Any,
        root_causes: List[Dict]
    ) -> Tuple[bool, Dict]:
        """
        Assess if the loss was preventable

        Returns: (preventable: bool, analysis: Dict)
        """
        preventable_causes = [c for c in root_causes if c.get('preventable', False)]
        unpreventable_causes = [c for c in root_causes if not c.get('preventable', True)]

        # Calculate preventability score
        if not root_causes:
            preventability_score = 0.5
        else:
            preventability_score = len(preventable_causes) / len(root_causes)

        # High severity preventable causes
        critical_preventable = [
            c for c in preventable_causes
            if c.get('severity') in ['critical', 'high']
        ]

        was_preventable = preventability_score >= 0.5

        return was_preventable, {
            "score": preventability_score,
            "preventable_causes": preventable_causes,
            "unpreventable_causes": unpreventable_causes,
            "critical_preventable": critical_preventable,
            "key_insight": self._generate_preventability_insight(
                was_preventable,
                critical_preventable
            )
        }

    def _compare_to_success_patterns(self, analysis: Any) -> Dict[str, Any]:
        """
        Compare lost conversation to successful ones
        """
        if not self.vector_store:
            return {"error": "No vector store available for comparison"}

        # Get successful patterns from vector store
        success_patterns = self.vector_store.get_world_class_patterns(
            min_effectiveness=0.8
        )

        if not success_patterns:
            return {"error": "No success patterns in database"}

        # Compare key metrics
        current_effectiveness = analysis.effectiveness_score

        # Calculate average success metrics
        if isinstance(success_patterns, list) and success_patterns:
            if isinstance(success_patterns[0], dict):
                avg_success_effectiveness = sum(
                    float(p.get('effectiveness_score', 0.85))
                    for p in success_patterns
                ) / len(success_patterns)
            else:
                avg_success_effectiveness = 0.85
        else:
            avg_success_effectiveness = 0.85

        # Identify gaps
        effectiveness_gap = avg_success_effectiveness - current_effectiveness

        return {
            "current_effectiveness": current_effectiveness,
            "average_success_effectiveness": avg_success_effectiveness,
            "effectiveness_gap": effectiveness_gap,
            "gap_percentage": (effectiveness_gap / avg_success_effectiveness * 100) if avg_success_effectiveness > 0 else 0,
            "key_differences": self._identify_key_differences(
                analysis, success_patterns
            )
        }

    def _identify_critical_moments(
        self,
        analysis: Any,
        root_causes: List[Dict]
    ) -> List[Dict[str, Any]]:
        """
        Identify critical moments where the conversation went wrong
        """
        critical_moments = []

        # Moment 1: Failed to qualify
        if any(c['category'] == 'Qualification' for c in root_causes):
            critical_moments.append({
                "moment": "Qualification Phase",
                "what_happened": "Failed to properly qualify buyer",
                "should_have": "Used BANT/MEDDIC to confirm Budget, Authority, Need, Timeline",
                "impact": "Wasted time on unqualified opportunity",
                "timing": "Early in conversation"
            })

        # Moment 2: Missed pain discovery
        if any(c['category'] == 'Discovery' for c in root_causes):
            critical_moments.append({
                "moment": "Discovery Phase",
                "what_happened": "Didn't uncover or amplify pain sufficiently",
                "should_have": "Used SPIN Implication Questions to amplify pain and create urgency",
                "impact": "No urgency = no action",
                "timing": "Mid conversation"
            })

        # Moment 3: Poor value articulation
        if any(c['category'] == 'Value' for c in root_causes):
            critical_moments.append({
                "moment": "Value Proposition",
                "what_happened": "Failed to articulate clear value or ROI",
                "should_have": "Used SPIN Need-Payoff or Value Selling to quantify ROI",
                "impact": "Buyer doesn't see business case",
                "timing": "Mid-to-late conversation"
            })

        # Moment 4: Objections not handled
        if any(c['category'] == 'Objection Handling' for c in root_causes):
            critical_moments.append({
                "moment": "Objection Handling",
                "what_happened": "Objections raised but not fully addressed",
                "should_have": "Used Chris Voss tactics: Label, validate, then reframe",
                "impact": "Objections became barriers",
                "timing": "Late conversation"
            })

        # Moment 5: Failed to close
        phases = analysis.conversation_flow.get('phases_completed', [])
        if 'closing' not in phases:
            critical_moments.append({
                "moment": "Closing Phase",
                "what_happened": "Never attempted to close or ask for next step",
                "should_have": "Used assumptive close: 'When should we get started?'",
                "impact": "No clear next steps = deal stalls",
                "timing": "End of conversation"
            })

        return critical_moments

    def _generate_prevention_strategies(
        self,
        root_causes: List[Dict],
        critical_moments: List[Dict]
    ) -> List[Dict[str, Any]]:
        """
        Generate specific strategies to prevent similar losses
        """
        strategies = []

        # Group causes by category
        causes_by_category = defaultdict(list)
        for cause in root_causes:
            if cause.get('preventable', False):
                causes_by_category[cause['category']].append(cause)

        # Strategy for each category
        if 'Qualification' in causes_by_category:
            strategies.append({
                "category": "Qualification",
                "strategy": "Implement strict BANT/MEDDIC qualification at start",
                "tactics": [
                    "Ask: 'Who else is involved in this decision?'",
                    "Confirm: 'Do you have budget allocated for this?'",
                    "Verify: 'What's your timeline for making a decision?'"
                ],
                "expected_impact": "Filter out 30-40% of unqualified leads early"
            })

        if 'Discovery' in causes_by_category:
            strategies.append({
                "category": "Discovery",
                "strategy": "Use SPIN framework to uncover and amplify pain",
                "tactics": [
                    "Problem Questions: 'What's the biggest challenge?'",
                    "Implication Questions: 'If this continues, what's the impact?'",
                    "Quantify: 'What's this costing you per month?'"
                ],
                "expected_impact": "Increase urgency by 40-50%"
            })

        if 'Value' in causes_by_category:
            strategies.append({
                "category": "Value",
                "strategy": "Always quantify ROI and business value",
                "tactics": [
                    "Calculate cost of doing nothing",
                    "Show ROI in buyer's terms (time saved, revenue gained)",
                    "Use case studies from similar companies"
                ],
                "expected_impact": "Improve conversion by 25-30%"
            })

        if 'Objection Handling' in causes_by_category:
            strategies.append({
                "category": "Objection Handling",
                "strategy": "Address objections proactively using Chris Voss",
                "tactics": [
                    "Label: 'It seems like price is a concern'",
                    "Validate: 'That's fair'",
                    "Reframe: 'What would staying with the current approach cost?'"
                ],
                "expected_impact": "Convert 60% of objection-based losses"
            })

        if 'Process' in causes_by_category:
            strategies.append({
                "category": "Process",
                "strategy": "Follow structured conversation framework",
                "tactics": [
                    "Use checklist for each phase",
                    "Don't skip discovery to pitch",
                    "Always confirm next steps before ending call"
                ],
                "expected_impact": "Increase close rate by 20%"
            })

        return strategies

    def _calculate_opportunity_cost(self, analysis: Any) -> Dict[str, Any]:
        """
        Calculate the cost of losing this deal
        """
        deal_value = analysis.metadata.deal_value or 0

        # Estimate lifetime value (3x first year for SaaS)
        estimated_ltv = deal_value * 3 if deal_value > 0 else 0

        # Time invested
        duration_minutes = (analysis.metadata.duration or 0) / 60

        # Calculate cost
        return {
            "deal_value": deal_value,
            "estimated_lifetime_value": estimated_ltv,
            "time_invested_minutes": duration_minutes,
            "time_invested_hours": duration_minutes / 60,
            "cost_summary": f"Lost ${deal_value:,.0f} deal (${estimated_ltv:,.0f} LTV) after {duration_minutes:.0f} minutes invested"
        }

    def _generate_coaching_recommendations(
        self,
        root_causes: List[Dict],
        prevention_analysis: Dict
    ) -> List[str]:
        """
        Generate coaching recommendations for rep
        """
        recommendations = []

        # Focus on critical preventable causes
        critical_causes = prevention_analysis.get('critical_preventable', [])

        for cause in critical_causes[:3]:
            category = cause.get('category', '')

            if category == 'Qualification':
                recommendations.append("Practice: BANT/MEDDIC qualification in every discovery call")
            elif category == 'Discovery':
                recommendations.append("Practice: SPIN Implication Questions to amplify pain")
            elif category == 'Value':
                recommendations.append("Practice: ROI calculation and value quantification")
            elif category == 'Objection Handling':
                recommendations.append("Practice: Chris Voss objection handling (label, validate, reframe)")
            elif category == 'Execution':
                recommendations.append("Shadow top performer to observe world-class execution")

        # General recommendations
        recommendations.append("Record and review your lost calls to identify patterns")
        recommendations.append("Role-play with manager focusing on failure points")

        return recommendations[:5]

    def _find_similar_losses(self, analysis: Any) -> List[Dict]:
        """Find similar lost deals for pattern identification"""
        # This would query the vector store for similar lost conversations
        # For now, return placeholder
        return []

    def _summarize_what_went_wrong(self, root_causes: List[Dict]) -> str:
        """Generate summary of what went wrong"""
        if not root_causes:
            return "Unable to identify specific failure points."

        critical = [c for c in root_causes if c['severity'] in ['critical', 'high']]

        if not critical:
            return "Minor issues but no critical failures identified."

        summary = "Critical failures: "
        summary += ", ".join([c['cause'] for c in critical[:3]])

        return summary

    def _summarize_what_could_have_been(self, strategies: List[Dict]) -> str:
        """Generate summary of what could have prevented the loss"""
        if not strategies:
            return "No clear prevention strategies identified."

        summary = "Could have been prevented by: "
        summary += ", ".join([s['strategy'] for s in strategies[:3]])

        return summary

    def _generate_preventability_insight(
        self,
        was_preventable: bool,
        critical_preventable: List[Dict]
    ) -> str:
        """Generate insight about preventability"""
        if not was_preventable:
            return "Loss was likely due to external factors or timing - not easily preventable."

        if critical_preventable:
            top_cause = critical_preventable[0]['cause']
            return f"Loss was preventable. Primary failure: {top_cause}"

        return "Loss was preventable with better execution of sales fundamentals."

    def _identify_key_differences(
        self,
        analysis: Any,
        success_patterns: List
    ) -> List[str]:
        """Identify key differences vs successful conversations"""
        differences = []

        # Pattern count difference
        current_pattern_count = len(analysis.key_patterns)
        # Assume successful conversations have 5+ patterns
        if current_pattern_count < 5:
            differences.append(f"Used only {current_pattern_count} techniques vs 5+ in successful calls")

        # Intent difference
        current_intent = analysis.buyer_signals.get('intent_score', 0)
        if current_intent < 70:
            differences.append(f"Intent score {current_intent}/100 vs 70+ in successful calls")

        # Flow difference
        current_flow = analysis.conversation_flow.get('structure_quality', '')
        if current_flow in ['needs_improvement', 'fair']:
            differences.append(f"Flow quality '{current_flow}' vs 'good/excellent' in successful calls")

        return differences[:5]
