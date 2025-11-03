"""
ML Predictor - Machine Learning-enhanced prediction and consistency analysis
Uses pattern recognition and consistency scoring to predict outcomes
"""

from typing import Dict, List, Any, Tuple
import json
from collections import Counter, defaultdict


class MLPredictor:
    """
    Machine Learning-enhanced predictor for sales outcomes
    Analyzes consistency patterns and predicts outcomes
    """

    def __init__(self, vector_store=None):
        """
        Initialize ML predictor

        Args:
            vector_store: Vector store with historical data
        """
        self.vector_store = vector_store
        self.consistency_threshold = 0.75
        self.min_signal_count = 3

    def predict_outcome(
        self,
        patterns: List[Dict],
        buyer_signals: Dict,
        conversation_flow: Dict,
        historical_data: List[Dict] = None
    ) -> Dict[str, Any]:
        """
        Predict conversation outcome using ML-enhanced analysis

        Args:
            patterns: Detected patterns in current conversation
            buyer_signals: Buyer signals detected
            conversation_flow: Conversation flow analysis
            historical_data: Historical conversations for training

        Returns:
            Prediction dictionary with confidence and reasoning
        """
        # Calculate consistency score
        consistency_score = self._calculate_consistency_score(
            patterns, buyer_signals, conversation_flow
        )

        # Identify consistent buying signals
        consistent_signals = self._identify_consistent_signals(
            buyer_signals, patterns
        )

        # Predict outcome based on patterns
        outcome_prediction = self._predict_from_patterns(
            patterns, buyer_signals, consistency_score
        )

        # Calculate confidence
        confidence = self._calculate_prediction_confidence(
            consistency_score,
            len(consistent_signals),
            len(patterns),
            buyer_signals.get('intent_score', 50)
        )

        # Identify key success factors
        success_factors = self._identify_success_factors(
            patterns, consistent_signals, conversation_flow
        )

        # Identify risk factors
        risk_factors = self._identify_risk_factors(
            buyer_signals, conversation_flow, patterns
        )

        return {
            "predicted_outcome": outcome_prediction["outcome"],
            "confidence": confidence,
            "consistency_score": consistency_score,
            "consistent_buying_signals": consistent_signals,
            "success_factors": success_factors,
            "risk_factors": risk_factors,
            "recommendation": self._generate_recommendation(
                outcome_prediction, success_factors, risk_factors
            ),
            "next_best_actions": self._suggest_next_actions(
                outcome_prediction, risk_factors, patterns
            ),
            "framework_alignment": self._analyze_framework_alignment(patterns),
            "signal_strength_by_framework": self._map_signals_to_frameworks(
                consistent_signals, patterns
            )
        }

    def _calculate_consistency_score(
        self,
        patterns: List[Dict],
        buyer_signals: Dict,
        conversation_flow: Dict
    ) -> float:
        """
        Calculate consistency score based on pattern alignment

        Measures how consistently world-class techniques are applied
        """
        if not patterns:
            return 0.0

        # Factor 1: Pattern effectiveness consistency (30%)
        effectiveness_scores = [p.get('effectiveness', 0.5) for p in patterns]
        effectiveness_std = self._calculate_std_dev(effectiveness_scores)
        effectiveness_consistency = 1.0 - min(effectiveness_std, 1.0)

        # Factor 2: Framework consistency (25%)
        frameworks_used = [p.get('framework', '') for p in patterns]
        framework_consistency = self._calculate_framework_consistency(frameworks_used)

        # Factor 3: Buyer signal consistency (25%)
        signal_consistency = self._calculate_signal_consistency(buyer_signals)

        # Factor 4: Flow consistency (20%)
        flow_consistency = conversation_flow.get('completion_rate', 0.5)

        # Weighted average
        consistency = (
            effectiveness_consistency * 0.30 +
            framework_consistency * 0.25 +
            signal_consistency * 0.25 +
            flow_consistency * 0.20
        )

        return min(max(consistency, 0.0), 1.0)

    def _identify_consistent_signals(
        self,
        buyer_signals: Dict,
        patterns: List[Dict]
    ) -> List[Dict[str, Any]]:
        """
        Identify 3-5+ consistent buying signals across frameworks

        Returns signals that appear consistently and map to multiple frameworks
        """
        signals = []

        # Signal 1: High Intent + Framework Alignment
        intent_score = buyer_signals.get('intent_score', 0)
        if intent_score >= 70:
            frameworks_aligned = self._get_frameworks_from_patterns(patterns)
            signals.append({
                "signal": "High Intent with Framework Alignment",
                "strength": intent_score / 100,
                "confidence": 0.9 if len(frameworks_aligned) >= 3 else 0.7,
                "frameworks": frameworks_aligned,
                "indicators": buyer_signals.get('positive_indicators', []),
                "description": f"Buyer showing {intent_score}/100 intent with alignment across {len(frameworks_aligned)} frameworks"
            })

        # Signal 2: Pain + Economic Impact
        pain_level = buyer_signals.get('pain_level', 'low')
        if pain_level in ['medium', 'high']:
            pain_strength = 0.9 if pain_level == 'high' else 0.7
            signals.append({
                "signal": "Pain with Economic Impact",
                "strength": pain_strength,
                "confidence": 0.85,
                "frameworks": ["SPIN", "Gap_Selling", "MEDDIC", "NEAT", "Value_Selling"],
                "indicators": [
                    f"{pain_level} pain level",
                    "Economic impact discussed" if "economic" in str(buyer_signals).lower() else "Pain quantified"
                ],
                "description": f"{pain_level.capitalize()} pain with quantifiable business impact"
            })

        # Signal 3: Authority + Budget Alignment
        authority = buyer_signals.get('authority', '')
        budget = buyer_signals.get('budget_qualification', '')
        if authority == 'decision_maker' and budget == 'qualified':
            signals.append({
                "signal": "Authority with Budget Alignment",
                "strength": 0.95,
                "confidence": 0.9,
                "frameworks": ["BANT", "MEDDIC", "NEAT", "Sandler"],
                "indicators": [
                    "Decision maker identified",
                    "Budget confirmed"
                ],
                "description": "Decision maker with confirmed budget - highest conversion indicator"
            })

        # Signal 4: Timeline Urgency + Champion Behavior
        timeline = buyer_signals.get('timeline', '')
        positive_indicators = buyer_signals.get('positive_indicators', [])
        if timeline in ['immediate', 'near_term'] and len(positive_indicators) >= 3:
            timeline_strength = 0.9 if timeline == 'immediate' else 0.75
            signals.append({
                "signal": "Urgency with Champion Behavior",
                "strength": timeline_strength,
                "confidence": 0.85,
                "frameworks": ["BANT", "MEDDIC", "NEAT", "Sandler", "SPIN"],
                "indicators": positive_indicators[:5],
                "description": f"{timeline.capitalize()} timeline with active champion behavior"
            })

        # Signal 5: Value Recognition + Solution Alignment
        value_patterns = [p for p in patterns if 'value' in p.get('pattern_type', '').lower()]
        solution_patterns = [p for p in patterns if 'solution' in p.get('pattern_type', '').lower()]
        if value_patterns and (buyer_signals.get('intent_score', 0) >= 60):
            signals.append({
                "signal": "Value Recognition with Solution Alignment",
                "strength": 0.8,
                "confidence": 0.8,
                "frameworks": ["Value_Selling", "Solution_Selling", "Conceptual_Selling", "SPIN"],
                "indicators": [
                    f"{len(value_patterns)} value articulation moments",
                    "Buyer recognizes business value",
                    "Solution alignment confirmed"
                ],
                "description": "Buyer articulates and recognizes value proposition"
            })

        # Signal 6: Multi-stakeholder Engagement
        if 'involved_colleague' in buyer_signals.get('positive_indicators', []):
            signals.append({
                "signal": "Multi-stakeholder Engagement",
                "strength": 0.85,
                "confidence": 0.8,
                "frameworks": ["MEDDIC", "Conceptual_Selling", "Solution_Selling"],
                "indicators": [
                    "Multiple stakeholders involved",
                    "Cross-functional alignment"
                ],
                "description": "Multiple decision makers engaged - indicates serious intent"
            })

        # Sort by strength and return top signals
        signals.sort(key=lambda x: x['strength'] * x['confidence'], reverse=True)
        return signals[:7]  # Return up to 7 consistent signals

    def _predict_from_patterns(
        self,
        patterns: List[Dict],
        buyer_signals: Dict,
        consistency_score: float
    ) -> Dict[str, Any]:
        """
        Predict outcome based on detected patterns
        """
        # Calculate scores for different outcomes
        intent_score = buyer_signals.get('intent_score', 50) / 100
        pain_score = 0.9 if buyer_signals.get('pain_level') == 'high' else 0.5
        authority_score = 0.9 if buyer_signals.get('authority') == 'decision_maker' else 0.5
        budget_score = 0.9 if buyer_signals.get('budget_qualification') == 'qualified' else 0.5
        timeline_score = 0.9 if buyer_signals.get('timeline') == 'immediate' else 0.6

        # Pattern quality score
        if patterns:
            avg_pattern_effectiveness = sum(p.get('effectiveness', 0.5) for p in patterns) / len(patterns)
        else:
            avg_pattern_effectiveness = 0.3

        # Composite score
        composite_score = (
            intent_score * 0.25 +
            pain_score * 0.20 +
            authority_score * 0.15 +
            budget_score * 0.15 +
            timeline_score * 0.10 +
            avg_pattern_effectiveness * 0.10 +
            consistency_score * 0.05
        )

        # Predict outcome
        if composite_score >= 0.75:
            outcome = "closed"
            probability = composite_score
        elif composite_score >= 0.60:
            outcome = "booked"
            probability = composite_score
        elif composite_score >= 0.45:
            outcome = "qualified"
            probability = composite_score
        elif composite_score >= 0.30:
            outcome = "nurture"
            probability = composite_score
        else:
            outcome = "lost"
            probability = 1.0 - composite_score

        return {
            "outcome": outcome,
            "probability": probability,
            "composite_score": composite_score,
            "contributing_factors": {
                "intent": intent_score,
                "pain": pain_score,
                "authority": authority_score,
                "budget": budget_score,
                "timeline": timeline_score,
                "pattern_quality": avg_pattern_effectiveness,
                "consistency": consistency_score
            }
        }

    def _calculate_prediction_confidence(
        self,
        consistency_score: float,
        signal_count: int,
        pattern_count: int,
        intent_score: float
    ) -> float:
        """
        Calculate confidence in the prediction
        """
        # More signals = higher confidence
        signal_confidence = min(signal_count / 5, 1.0)

        # More patterns = higher confidence
        pattern_confidence = min(pattern_count / 7, 1.0)

        # Higher consistency = higher confidence
        consistency_confidence = consistency_score

        # Higher intent = higher confidence
        intent_confidence = intent_score / 100

        # Weighted average
        confidence = (
            signal_confidence * 0.30 +
            pattern_confidence * 0.25 +
            consistency_confidence * 0.25 +
            intent_confidence * 0.20
        )

        return min(max(confidence, 0.0), 1.0)

    def _identify_success_factors(
        self,
        patterns: List[Dict],
        consistent_signals: List[Dict],
        conversation_flow: Dict
    ) -> List[str]:
        """Identify factors contributing to success"""
        factors = []

        # Strong signals
        if len(consistent_signals) >= 4:
            factors.append(f"Strong buying signals ({len(consistent_signals)} identified)")

        # High-effectiveness patterns
        high_eff_patterns = [p for p in patterns if p.get('effectiveness', 0) >= 0.85]
        if high_eff_patterns:
            factors.append(f"World-class technique execution ({len(high_eff_patterns)} patterns)")

        # Good flow
        if conversation_flow.get('structure_quality') in ['excellent', 'good']:
            factors.append(f"Strong conversation structure ({conversation_flow.get('structure_quality')})")

        # Framework alignment
        frameworks = set(p.get('framework', '') for p in patterns)
        if len(frameworks) >= 3:
            factors.append(f"Multi-framework approach ({len(frameworks)} frameworks)")

        return factors

    def _identify_risk_factors(
        self,
        buyer_signals: Dict,
        conversation_flow: Dict,
        patterns: List[Dict]
    ) -> List[str]:
        """Identify factors that may prevent conversion"""
        risks = []

        # Objections
        objections = buyer_signals.get('objections', [])
        if objections:
            risks.append(f"Unresolved objections: {', '.join(objections)}")

        # Low intent
        if buyer_signals.get('intent_score', 100) < 50:
            risks.append(f"Low buyer intent ({buyer_signals.get('intent_score')}/ 100)")

        # Authority issues
        if buyer_signals.get('authority') == 'influencer':
            risks.append("Not speaking with decision maker")

        # Budget concerns
        if buyer_signals.get('budget_qualification') == 'not_qualified':
            risks.append("Budget not confirmed or unavailable")

        # Timeline issues
        if buyer_signals.get('timeline') == 'long_term':
            risks.append("Long timeline - may lose momentum")

        # Missing phases
        missed = conversation_flow.get('missed_opportunities', [])
        if missed:
            risks.append(f"Missed phases: {len(missed)}")

        # Low pattern quality
        if patterns:
            avg_eff = sum(p.get('effectiveness', 0.5) for p in patterns) / len(patterns)
            if avg_eff < 0.6:
                risks.append(f"Pattern execution below threshold ({avg_eff:.2f})")

        return risks

    def _generate_recommendation(
        self,
        prediction: Dict,
        success_factors: List[str],
        risk_factors: List[str]
    ) -> str:
        """Generate recommendation based on prediction"""
        outcome = prediction['outcome']
        probability = prediction['probability']

        if outcome in ['closed', 'booked'] and probability >= 0.75:
            return f"Strong likelihood of {outcome} ({probability:.0%}). Push for commitment now."
        elif outcome in ['closed', 'booked'] and len(risk_factors) > 0:
            return f"Likely to {outcome} but address: {risk_factors[0]}. Then close."
        elif outcome == 'qualified':
            return f"Qualified opportunity. Focus on: {', '.join(risk_factors[:2]) if risk_factors else 'building urgency'}"
        elif outcome == 'nurture':
            return "Not ready to buy. Nurture with value content and stay engaged."
        else:
            return f"At risk of losing. Immediate action needed: {risk_factors[0] if risk_factors else 'rebuild value'}"

    def _suggest_next_actions(
        self,
        prediction: Dict,
        risk_factors: List[str],
        patterns: List[Dict]
    ) -> List[str]:
        """Suggest specific next actions"""
        actions = []
        outcome = prediction['outcome']

        if outcome in ['closed', 'booked']:
            actions.append("Schedule next step immediately (demo/implementation/contract)")
            actions.append("Send follow-up with clear timeline and next steps")
            actions.append("Introduce implementation team to build momentum")

        elif outcome == 'qualified':
            if 'decision maker' in str(risk_factors).lower():
                actions.append("Request introduction to decision maker")
            if 'budget' in str(risk_factors).lower():
                actions.append("Discuss budget and build business case")
            if 'timeline' in str(risk_factors).lower():
                actions.append("Create urgency by amplifying pain/opportunity cost")

            actions.append("Schedule follow-up call with additional stakeholders")

        elif outcome == 'nurture':
            actions.append("Share case study relevant to their industry")
            actions.append("Set up quarterly check-in cadence")
            actions.append("Send thought leadership content to stay top-of-mind")

        else:  # lost or at risk
            actions.append("Schedule executive-to-executive call to reset")
            actions.append("Re-discover pain points and quantify impact")
            actions.append("Offer limited-time incentive or pilot program")

        return actions[:5]

    def _analyze_framework_alignment(self, patterns: List[Dict]) -> Dict[str, Any]:
        """Analyze which frameworks are being used"""
        frameworks = [p.get('framework', 'unknown') for p in patterns if p.get('framework')]
        framework_counts = Counter(frameworks)

        # Calculate effectiveness by framework
        framework_effectiveness = defaultdict(list)
        for pattern in patterns:
            fw = pattern.get('framework')
            eff = pattern.get('effectiveness', 0.5)
            if fw:
                framework_effectiveness[fw].append(eff)

        framework_avg_eff = {
            fw: sum(effs) / len(effs)
            for fw, effs in framework_effectiveness.items()
        }

        return {
            "frameworks_used": list(framework_counts.keys()),
            "framework_frequency": dict(framework_counts),
            "framework_effectiveness": framework_avg_eff,
            "primary_framework": framework_counts.most_common(1)[0][0] if framework_counts else "none",
            "framework_diversity": len(framework_counts)
        }

    def _map_signals_to_frameworks(
        self,
        consistent_signals: List[Dict],
        patterns: List[Dict]
    ) -> Dict[str, List[str]]:
        """Map buying signals to frameworks that support them"""
        mapping = defaultdict(list)

        for signal in consistent_signals:
            signal_name = signal.get('signal', '')
            frameworks = signal.get('frameworks', [])

            for framework in frameworks:
                mapping[framework].append(signal_name)

        return dict(mapping)

    # Helper methods

    def _calculate_std_dev(self, values: List[float]) -> float:
        """Calculate standard deviation"""
        if not values:
            return 0.0

        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        return variance ** 0.5

    def _calculate_framework_consistency(self, frameworks: List[str]) -> float:
        """Calculate framework consistency score"""
        if not frameworks:
            return 0.0

        # Check if frameworks are complementary
        framework_counts = Counter(frameworks)

        # Ideal: 3-5 different frameworks used consistently
        diversity = len(framework_counts)
        if 3 <= diversity <= 5:
            diversity_score = 1.0
        elif diversity < 3:
            diversity_score = diversity / 3
        else:
            diversity_score = 5 / diversity

        # Check distribution
        counts = list(framework_counts.values())
        if counts:
            max_count = max(counts)
            min_count = min(counts)
            distribution_score = min_count / max_count if max_count > 0 else 0
        else:
            distribution_score = 0

        return (diversity_score * 0.6 + distribution_score * 0.4)

    def _calculate_signal_consistency(self, buyer_signals: Dict) -> float:
        """Calculate buyer signal consistency"""
        # Check alignment between different signal types
        intent = buyer_signals.get('intent_score', 50) / 100
        pain = 0.8 if buyer_signals.get('pain_level') == 'high' else 0.4
        authority = 0.8 if buyer_signals.get('authority') == 'decision_maker' else 0.4
        budget = 0.8 if buyer_signals.get('budget_qualification') == 'qualified' else 0.4
        timeline = 0.8 if buyer_signals.get('timeline') == 'immediate' else 0.4

        # Signals should align - if intent is high, other signals should be too
        signals = [intent, pain, authority, budget, timeline]
        avg = sum(signals) / len(signals)

        # Calculate how much signals deviate from average
        deviation = sum(abs(s - avg) for s in signals) / len(signals)

        # Lower deviation = higher consistency
        consistency = 1.0 - min(deviation, 1.0)

        return consistency

    def _get_frameworks_from_patterns(self, patterns: List[Dict]) -> List[str]:
        """Extract unique frameworks from patterns"""
        return list(set(p.get('framework', '') for p in patterns if p.get('framework')))
