"""
Gap Analyzer - Compares current patterns to world-class standards
"""

from typing import Dict, List, Any
from .vector_store import VectorStore


class GapAnalyzer:
    """
    Analyzes gaps between current performance and world-class standards
    """

    def __init__(self, vector_store: VectorStore):
        """
        Initialize gap analyzer

        Args:
            vector_store: Vector store containing world-class patterns
        """
        self.vector_store = vector_store
        self.world_class_threshold = 0.85

    def analyze(
        self,
        patterns: List[Dict],
        effectiveness_score: float,
        industry: str = None
    ) -> Dict[str, Any]:
        """
        Analyze gaps compared to world-class conversations

        Args:
            patterns: Detected patterns in current conversation
            effectiveness_score: Current effectiveness score
            industry: Industry for comparison

        Returns:
            Gap analysis dictionary
        """
        # Get world-class patterns for comparison
        world_class_patterns = self.vector_store.get_world_class_patterns(
            min_effectiveness=self.world_class_threshold
        )

        # Calculate world-class comparison score
        world_class_comparison = self._compare_to_world_class(
            patterns,
            effectiveness_score,
            world_class_patterns
        )

        # Identify current level
        current_level = self._determine_level(effectiveness_score)

        # Identify improvement areas
        improvement_areas = self._identify_improvement_areas(
            patterns,
            world_class_patterns
        )

        # Generate gap closure recommendations
        recommendations = self._generate_recommendations(improvement_areas)

        return {
            "current_level": current_level,
            "world_class_comparison": world_class_comparison,
            "effectiveness_score": effectiveness_score,
            "world_class_threshold": self.world_class_threshold,
            "gap_score": self.world_class_threshold - effectiveness_score,
            "improvement_areas": improvement_areas,
            "recommendations": recommendations,
            "world_class_patterns_analyzed": len(world_class_patterns)
        }

    def _compare_to_world_class(
        self,
        patterns: List[Dict],
        effectiveness_score: float,
        world_class_patterns: List[Dict]
    ) -> float:
        """
        Compare current patterns to world-class

        Returns:
            Comparison score (0-1), where 1 = matches world-class
        """
        if not world_class_patterns:
            # If no world-class patterns available, compare to threshold
            return effectiveness_score / self.world_class_threshold

        # Compare pattern diversity
        current_techniques = set(p.get("technique", "") for p in patterns)
        world_class_techniques = set()

        for wc_pattern in world_class_patterns:
            if isinstance(wc_pattern, dict):
                techniques = wc_pattern.get("techniques_used", "")
                if isinstance(techniques, str):
                    # Parse JSON string if needed
                    try:
                        import json
                        techniques = json.loads(techniques)
                    except:
                        techniques = []
                if isinstance(techniques, list):
                    world_class_techniques.update(techniques)

        # Calculate technique overlap
        if world_class_techniques:
            technique_overlap = len(current_techniques & world_class_techniques) / len(world_class_techniques)
        else:
            technique_overlap = 0.5

        # Calculate effectiveness comparison
        if world_class_patterns:
            avg_world_class_effectiveness = sum(
                float(p.get("effectiveness_score", 0.85))
                for p in world_class_patterns
            ) / len(world_class_patterns)
            effectiveness_comparison = effectiveness_score / avg_world_class_effectiveness
        else:
            effectiveness_comparison = effectiveness_score / self.world_class_threshold

        # Weighted average
        comparison_score = (technique_overlap * 0.4 + effectiveness_comparison * 0.6)

        return min(comparison_score, 1.0)

    def _determine_level(self, effectiveness_score: float) -> str:
        """Determine current skill level"""
        if effectiveness_score >= 0.85:
            return "world_class"
        elif effectiveness_score >= 0.7:
            return "advanced"
        elif effectiveness_score >= 0.55:
            return "intermediate"
        elif effectiveness_score >= 0.4:
            return "developing"
        else:
            return "beginner"

    def _identify_improvement_areas(
        self,
        patterns: List[Dict],
        world_class_patterns: List[Dict]
    ) -> List[Dict[str, Any]]:
        """Identify specific areas for improvement"""
        improvement_areas = []

        # Check for pattern gaps
        current_pattern_types = set(p.get("pattern_type", "") for p in patterns)

        # Define critical pattern types
        critical_patterns = {
            "pain_discovery": "Pain Discovery",
            "pain_amplification": "Pain Amplification",
            "value_articulation": "Value Articulation",
            "objection_handling": "Objection Handling",
            "closing": "Closing"
        }

        for pattern_type, pattern_name in critical_patterns.items():
            if pattern_type not in current_pattern_types:
                improvement_areas.append({
                    "area": pattern_type,
                    "name": pattern_name,
                    "current_score": 0.0,
                    "world_class_score": 0.9,
                    "gap": 0.9,
                    "recommendations": self._get_pattern_recommendations(pattern_type)
                })

        # Check for low-effectiveness patterns
        for pattern in patterns:
            if pattern.get("effectiveness", 1.0) < 0.6:
                improvement_areas.append({
                    "area": pattern.get("pattern_type", "unknown"),
                    "name": pattern.get("technique", "Unknown Technique"),
                    "current_score": pattern.get("effectiveness", 0.5),
                    "world_class_score": 0.85,
                    "gap": 0.85 - pattern.get("effectiveness", 0.5),
                    "recommendations": [
                        f"Improve execution of {pattern.get('technique', 'this technique')}",
                        "Study world-class examples of this pattern",
                        "Practice with role-playing scenarios"
                    ]
                })

        # Sort by gap size (largest gaps first)
        improvement_areas.sort(key=lambda x: x["gap"], reverse=True)

        return improvement_areas[:5]  # Return top 5 improvement areas

    def _get_pattern_recommendations(self, pattern_type: str) -> List[str]:
        """Get recommendations for a specific pattern type"""
        recommendations = {
            "pain_discovery": [
                "Ask more open-ended problem questions",
                "Use SPIN Problem Questions: 'What's the biggest challenge with...'",
                "Listen more, talk less during discovery"
            ],
            "pain_amplification": [
                "Use SPIN Implication Questions to amplify pain",
                "Ask: 'If this continues, what's the impact on...'",
                "Quantify the cost of inaction"
            ],
            "value_articulation": [
                "Use SPIN Need-Payoff Questions",
                "Ask: 'If you could solve this, what would that mean for you?'",
                "Have the buyer articulate value, not you"
            ],
            "objection_handling": [
                "Validate objections before reframing",
                "Use Chris Voss labeling: 'It seems like [objection] is a concern'",
                "Ask calibrated questions to understand the real objection"
            ],
            "closing": [
                "Use assumptive closes",
                "Ask: 'When would be the best time to get started?'",
                "Create urgency by linking to pain and timeline"
            ],
            "discovery": [
                "Ask more Situation questions to understand context",
                "Gather background before diving into problems",
                "Use a consultative approach"
            ],
            "teaching": [
                "Provide unique insights the buyer doesn't know",
                "Use Challenger Sale: Teach something new",
                "Share relevant data or trends from your industry experience"
            ],
            "personalization": [
                "Tailor message to buyer's specific situation",
                "Use phrases like: 'Given your [specific situation]...'",
                "Reference their industry, company size, or challenges"
            ]
        }

        return recommendations.get(pattern_type, [
            "Study world-class examples of this pattern",
            "Practice this technique in role-playing",
            "Get feedback on your execution"
        ])

    def _generate_recommendations(self, improvement_areas: List[Dict]) -> List[str]:
        """Generate overall recommendations for closing gaps"""
        recommendations = []

        if not improvement_areas:
            return [
                "Maintain current performance level",
                "Continue using effective techniques",
                "Share best practices with team"
            ]

        # Generate recommendations based on top gaps
        for area in improvement_areas[:3]:  # Focus on top 3 gaps
            recommendations.extend(area.get("recommendations", []))

        # Add general recommendations
        general_recommendations = [
            "Record and review your sales calls weekly",
            "Study transcripts of your best performing calls",
            "Practice new techniques before using them with real prospects",
            "Get peer feedback on your conversation approach",
            "Use role-playing to rehearse difficult scenarios"
        ]

        # Combine and limit
        all_recommendations = recommendations + general_recommendations
        return list(dict.fromkeys(all_recommendations))[:10]  # Remove duplicates, limit to 10

    def generate_coaching_plan(self, gap_analysis: Dict) -> Dict[str, Any]:
        """
        Generate a coaching plan based on gap analysis

        Args:
            gap_analysis: Gap analysis results

        Returns:
            Structured coaching plan
        """
        current_level = gap_analysis.get("current_level", "intermediate")
        improvement_areas = gap_analysis.get("improvement_areas", [])

        # Determine focus areas (top 3)
        focus_areas = improvement_areas[:3]

        # Generate training plan
        training_modules = []
        for area in focus_areas:
            training_modules.append({
                "skill": area.get("name", "Unknown"),
                "current_proficiency": area.get("current_score", 0.5),
                "target_proficiency": area.get("world_class_score", 0.85),
                "priority": "high" if area.get("gap", 0) > 0.3 else "medium",
                "estimated_time": "2-4 weeks",
                "resources": [
                    f"Study world-class {area.get('name', '')} examples",
                    "Practice in role-playing sessions",
                    "Get feedback from manager or peer"
                ],
                "success_metrics": [
                    f"Effectiveness score for {area.get('name', '')} > 0.75",
                    "Use technique in at least 80% of qualifying conversations",
                    "Positive feedback from prospects or peers"
                ]
            })

        coaching_plan = {
            "current_level": current_level,
            "target_level": "world_class" if current_level != "world_class" else "world_class",
            "gap_score": gap_analysis.get("gap_score", 0),
            "focus_areas": [area.get("name", "") for area in focus_areas],
            "training_modules": training_modules,
            "estimated_timeline": "4-8 weeks",
            "success_criteria": [
                f"Increase effectiveness score from {gap_analysis.get('effectiveness_score', 0):.2f} to {self.world_class_threshold}",
                "Master top 3 improvement areas",
                "Consistently use world-class patterns"
            ],
            "next_steps": [
                "Review training modules",
                "Schedule role-playing sessions",
                "Set up weekly review cadence",
                "Track progress metrics"
            ]
        }

        return coaching_plan
