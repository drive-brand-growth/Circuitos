"""
Sales Conversation Analyzer - Main Analysis Engine
Analyzes sales conversations for patterns, buyer signals, and effectiveness
"""

import json
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime

# Optional imports for AI providers
try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

from .pattern_detector import PatternDetector
from .buyer_signal_detector import BuyerSignalDetector
from .flow_analyzer import FlowAnalyzer
from .gap_analyzer import GapAnalyzer
from .vector_store import VectorStore
from .ml_predictor import MLPredictor
from .loss_analyzer import LossAnalyzer


@dataclass
class ConversationMetadata:
    """Metadata about the conversation"""
    conversation_id: str
    contact_id: Optional[str] = None
    industry: Optional[str] = None
    deal_value: Optional[float] = None
    duration: Optional[int] = None  # seconds
    outcome: Optional[str] = None  # booked, closed, lost, nurture
    timestamp: datetime = field(default_factory=datetime.now)
    agent_id: Optional[str] = None
    buyer_persona: Optional[str] = None


@dataclass
class ConversationAnalysis:
    """Complete analysis results"""
    conversation_id: str
    outcome_classification: str
    confidence_score: float
    effectiveness_score: float
    key_patterns: List[Dict[str, Any]]
    buyer_signals: Dict[str, Any]
    conversation_flow: Dict[str, Any]
    gap_analysis: Dict[str, Any]
    vector_embedding: List[float]
    training_value: str  # high, medium, low
    pattern_tags: List[str]
    recommendations: List[str]
    metadata: ConversationMetadata
    # New enhanced fields
    ml_prediction: Optional[Dict[str, Any]] = None
    loss_analysis: Optional[Dict[str, Any]] = None
    consistent_buying_signals: Optional[List[Dict]] = None
    framework_alignment: Optional[Dict] = None


class SalesConversationAnalyzer:
    """
    Main analyzer class that orchestrates conversation analysis
    """

    def __init__(
        self,
        vector_db_path: str = "./data/vector_db",
        anthropic_api_key: Optional[str] = None,
        openai_api_key: Optional[str] = None,
        frameworks: List[str] = None
    ):
        """
        Initialize the analyzer

        Args:
            vector_db_path: Path to ChromaDB vector database
            anthropic_api_key: Anthropic API key for Claude
            openai_api_key: OpenAI API key for embeddings
            frameworks: List of frameworks to use (SPIN, Challenger, etc.)
        """
        self.vector_store = VectorStore(vector_db_path)
        self.pattern_detector = PatternDetector(frameworks or [
            "SPIN", "Challenger", "Gap_Selling", "MEDDIC", "BANT",
            "Value_Selling", "Solution_Selling", "NEAT", "Conceptual_Selling",
            "Never_Split_Difference", "Sandler", "Straight_Line"
        ])
        self.buyer_signal_detector = BuyerSignalDetector()
        self.flow_analyzer = FlowAnalyzer()
        self.gap_analyzer = GapAnalyzer(self.vector_store)
        self.ml_predictor = MLPredictor(self.vector_store)
        self.loss_analyzer = LossAnalyzer(self.vector_store)

        # Initialize API clients
        self.anthropic_client = None
        self.openai_client = None

        if anthropic_api_key and ANTHROPIC_AVAILABLE:
            self.anthropic_client = anthropic.Anthropic(api_key=anthropic_api_key)
        elif anthropic_api_key and not ANTHROPIC_AVAILABLE:
            print("Warning: anthropic package not installed. Install with: pip install anthropic")

        if openai_api_key and OPENAI_AVAILABLE:
            self.openai_client = openai.OpenAI(api_key=openai_api_key)
        elif openai_api_key and not OPENAI_AVAILABLE:
            print("Warning: openai package not installed. Install with: pip install openai")

    def analyze(
        self,
        transcript: str,
        metadata: Dict[str, Any],
        use_ai: bool = True
    ) -> ConversationAnalysis:
        """
        Analyze a sales conversation

        Args:
            transcript: Full conversation transcript
            metadata: Conversation metadata (contact_id, outcome, etc.)
            use_ai: Whether to use Claude for deep analysis

        Returns:
            ConversationAnalysis object with complete results
        """
        # Parse metadata
        conv_metadata = self._parse_metadata(metadata)

        # Step 1: Pattern Detection
        patterns = self.pattern_detector.detect_patterns(transcript)

        # Step 2: Buyer Signal Detection
        buyer_signals = self.buyer_signal_detector.analyze(transcript)

        # Step 3: Conversation Flow Analysis
        flow_analysis = self.flow_analyzer.analyze(transcript, patterns)

        # Step 4: Calculate Effectiveness Score
        effectiveness_score = self._calculate_effectiveness(
            patterns=patterns,
            buyer_signals=buyer_signals,
            flow_analysis=flow_analysis,
            outcome=conv_metadata.outcome
        )

        # Step 5: Gap Analysis (compare to world-class)
        gap_analysis = self.gap_analyzer.analyze(
            patterns=patterns,
            effectiveness_score=effectiveness_score,
            industry=conv_metadata.industry
        )

        # Step 6: Generate Embedding
        embedding = self._generate_embedding(transcript, patterns)

        # Step 7: AI-Powered Deep Analysis (optional)
        if use_ai and self.anthropic_client:
            ai_insights = self._deep_analysis_with_claude(
                transcript=transcript,
                patterns=patterns,
                buyer_signals=buyer_signals,
                flow_analysis=flow_analysis
            )
            # Enhance results with AI insights
            patterns = self._merge_insights(patterns, ai_insights.get("patterns", []))
            recommendations = ai_insights.get("recommendations", [])
        else:
            recommendations = self._generate_basic_recommendations(gap_analysis)

        # Step 8: Classify outcome and training value
        outcome_classification = self._classify_outcome(effectiveness_score, conv_metadata.outcome)
        training_value = self._assess_training_value(effectiveness_score, patterns)

        # Step 9: Extract pattern tags
        pattern_tags = self._extract_pattern_tags(patterns, buyer_signals)

        # Step 10: ML Prediction (predict outcome and identify consistent signals)
        ml_prediction = self.ml_predictor.predict_outcome(
            patterns=patterns,
            buyer_signals=buyer_signals,
            conversation_flow=flow_analysis
        )

        # Step 11: Loss Analysis (if negative outcome)
        loss_analysis = None
        if conv_metadata.outcome in ['lost', 'no_response', 'unqualified'] or outcome_classification == 'negative':
            loss_analysis = self.loss_analyzer.analyze_loss(
                conversation_analysis=None,  # Will create temp object
                actual_outcome=conv_metadata.outcome or 'lost'
            )
            # Pass the current analysis data to loss analyzer
            loss_analysis['_temp_analysis'] = {
                'buyer_signals': buyer_signals,
                'key_patterns': patterns,
                'conversation_flow': flow_analysis,
                'gap_analysis': gap_analysis,
                'effectiveness_score': effectiveness_score,
                'metadata': conv_metadata
            }

        # Create analysis result
        analysis = ConversationAnalysis(
            conversation_id=conv_metadata.conversation_id,
            outcome_classification=outcome_classification,
            confidence_score=self._calculate_confidence(patterns, buyer_signals),
            effectiveness_score=effectiveness_score,
            key_patterns=patterns,
            buyer_signals=buyer_signals,
            conversation_flow=flow_analysis,
            gap_analysis=gap_analysis,
            vector_embedding=embedding,
            training_value=training_value,
            pattern_tags=pattern_tags,
            recommendations=recommendations,
            metadata=conv_metadata,
            # Enhanced fields
            ml_prediction=ml_prediction,
            loss_analysis=loss_analysis,
            consistent_buying_signals=ml_prediction.get('consistent_buying_signals', []),
            framework_alignment=ml_prediction.get('framework_alignment', {})
        )

        # Step 10: Store in vector database if high value
        if training_value in ["high", "medium"] and outcome_classification == "positive":
            self.vector_store.add_conversation(analysis)

        return analysis

    def _parse_metadata(self, metadata: Dict[str, Any]) -> ConversationMetadata:
        """Parse metadata dictionary into ConversationMetadata object"""
        return ConversationMetadata(
            conversation_id=metadata.get("conversation_id", f"conv_{datetime.now().timestamp()}"),
            contact_id=metadata.get("contact_id"),
            industry=metadata.get("industry"),
            deal_value=metadata.get("deal_value"),
            duration=metadata.get("duration"),
            outcome=metadata.get("outcome"),
            agent_id=metadata.get("agent_id"),
            buyer_persona=metadata.get("buyer_persona")
        )

    def _calculate_effectiveness(
        self,
        patterns: List[Dict],
        buyer_signals: Dict,
        flow_analysis: Dict,
        outcome: Optional[str]
    ) -> float:
        """
        Calculate overall conversation effectiveness score (0-1)

        Weighted factors:
        - Pattern quality: 30%
        - Buyer engagement: 30%
        - Flow structure: 20%
        - Outcome: 20%
        """
        # Pattern quality score
        if patterns:
            pattern_scores = [p.get("effectiveness", 0.5) for p in patterns]
            pattern_score = sum(pattern_scores) / len(pattern_scores)
        else:
            pattern_score = 0.3

        # Buyer engagement score
        intent_score = buyer_signals.get("intent_score", 50) / 100
        engagement_score = len(buyer_signals.get("positive_indicators", [])) * 0.1
        buyer_score = min((intent_score + engagement_score) / 2, 1.0)

        # Flow structure score
        phases = flow_analysis.get("phases_completed", [])
        flow_score = len(phases) / 5  # Assuming 5 ideal phases

        # Outcome score
        outcome_scores = {
            "closed": 1.0,
            "booked": 0.85,
            "demo_scheduled": 0.85,
            "qualified": 0.7,
            "nurture": 0.5,
            "lost": 0.2,
            None: 0.5
        }
        outcome_score = outcome_scores.get(outcome, 0.5)

        # Weighted average
        effectiveness = (
            pattern_score * 0.3 +
            buyer_score * 0.3 +
            flow_score * 0.2 +
            outcome_score * 0.2
        )

        return min(max(effectiveness, 0.0), 1.0)

    def _calculate_confidence(self, patterns: List[Dict], buyer_signals: Dict) -> float:
        """Calculate confidence in the analysis"""
        # More patterns detected = higher confidence
        pattern_confidence = min(len(patterns) * 0.1, 0.5)

        # More buyer signals = higher confidence
        signal_confidence = min(len(buyer_signals.get("positive_indicators", [])) * 0.05, 0.3)

        # Base confidence
        base_confidence = 0.2

        confidence = base_confidence + pattern_confidence + signal_confidence
        return min(confidence, 1.0)

    def _classify_outcome(self, effectiveness_score: float, actual_outcome: Optional[str]) -> str:
        """Classify conversation outcome as positive, neutral, or negative"""
        if actual_outcome in ["closed", "booked", "demo_scheduled"]:
            return "positive"
        elif actual_outcome in ["lost", "unqualified"]:
            return "negative"
        elif effectiveness_score >= 0.7:
            return "positive"
        elif effectiveness_score <= 0.4:
            return "negative"
        else:
            return "neutral"

    def _assess_training_value(self, effectiveness_score: float, patterns: List[Dict]) -> str:
        """Assess the training value of this conversation"""
        if effectiveness_score >= 0.8 and len(patterns) >= 3:
            return "high"
        elif effectiveness_score >= 0.6 and len(patterns) >= 2:
            return "medium"
        else:
            return "low"

    def _extract_pattern_tags(self, patterns: List[Dict], buyer_signals: Dict) -> List[str]:
        """Extract searchable tags from patterns"""
        tags = []

        # Pattern-based tags
        for pattern in patterns:
            technique = pattern.get("technique", "")
            if technique:
                tags.append(technique.lower().replace(" ", "_"))

        # Signal-based tags
        if buyer_signals.get("pain_level") == "high":
            tags.append("high_pain")
        if buyer_signals.get("authority") == "decision_maker":
            tags.append("decision_maker")
        if buyer_signals.get("budget_qualification") == "qualified":
            tags.append("budget_qualified")

        # Objection tags
        for objection in buyer_signals.get("objections", []):
            tags.append(f"objection_{objection}")

        return list(set(tags))  # Remove duplicates

    def _generate_embedding(self, transcript: str, patterns: List[Dict]) -> List[float]:
        """Generate vector embedding for the conversation"""
        if self.openai_client:
            try:
                # Use OpenAI embeddings
                response = self.openai_client.embeddings.create(
                    model="text-embedding-3-small",
                    input=transcript[:8000]  # Limit to 8k chars
                )
                return response.data[0].embedding
            except Exception as e:
                print(f"Error generating embedding: {e}")
                return [0.0] * 1536  # Default embedding size

        # Fallback: Simple pattern-based embedding
        return self._simple_embedding(transcript, patterns)

    def _simple_embedding(self, transcript: str, patterns: List[Dict]) -> List[float]:
        """Simple pattern-based embedding (fallback)"""
        # This is a simplified version - in production, use sentence-transformers
        embedding = [0.0] * 384  # Smaller embedding size

        # Encode pattern presence
        pattern_types = ["SPIN", "Challenger", "Gap_Selling", "MEDDIC", "Sandler"]
        for i, ptype in enumerate(pattern_types):
            if any(p.get("technique", "").startswith(ptype) for p in patterns):
                embedding[i] = 1.0

        return embedding

    def _deep_analysis_with_claude(
        self,
        transcript: str,
        patterns: List[Dict],
        buyer_signals: Dict,
        flow_analysis: Dict
    ) -> Dict[str, Any]:
        """Use Claude for deep conversation analysis"""
        if not self.anthropic_client:
            return {}

        prompt = self._build_analysis_prompt(transcript, patterns, buyer_signals, flow_analysis)

        try:
            message = self.anthropic_client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=4000,
                messages=[{"role": "user", "content": prompt}]
            )

            response_text = message.content[0].text
            return self._parse_claude_response(response_text)

        except Exception as e:
            print(f"Error in Claude analysis: {e}")
            return {}

    def _build_analysis_prompt(
        self,
        transcript: str,
        patterns: List[Dict],
        buyer_signals: Dict,
        flow_analysis: Dict
    ) -> str:
        """Build prompt for Claude analysis"""
        return f"""You are a world-class sales conversation analyzer. Analyze this conversation deeply.

TRANSCRIPT:
{transcript[:4000]}

DETECTED PATTERNS:
{json.dumps(patterns, indent=2)}

BUYER SIGNALS:
{json.dumps(buyer_signals, indent=2)}

FLOW ANALYSIS:
{json.dumps(flow_analysis, indent=2)}

Provide your analysis in JSON format with these keys:
1. "additional_patterns": Any patterns not detected by the automated system
2. "recommendations": Specific, actionable recommendations (at least 5)
3. "key_insights": Most important insights about this conversation
4. "what_worked": What the agent did well
5. "what_to_improve": What could be improved
6. "world_class_comparison": How this compares to world-class conversations (0-1 score)

Focus on being specific and actionable. Use examples from the transcript.
"""

    def _parse_claude_response(self, response: str) -> Dict[str, Any]:
        """Parse Claude's JSON response"""
        try:
            # Try to extract JSON from the response
            start = response.find("{")
            end = response.rfind("}") + 1
            if start != -1 and end != 0:
                json_str = response[start:end]
                return json.loads(json_str)
        except Exception as e:
            print(f"Error parsing Claude response: {e}")

        return {}

    def _merge_insights(self, patterns: List[Dict], ai_patterns: List[Dict]) -> List[Dict]:
        """Merge automated patterns with AI-detected patterns"""
        all_patterns = patterns.copy()

        for ai_pattern in ai_patterns:
            # Check if pattern already exists
            if not any(p.get("technique") == ai_pattern.get("technique") for p in all_patterns):
                all_patterns.append(ai_pattern)

        return all_patterns

    def _generate_basic_recommendations(self, gap_analysis: Dict) -> List[str]:
        """Generate basic recommendations from gap analysis"""
        recommendations = []

        for area in gap_analysis.get("improvement_areas", []):
            recommendations.extend(area.get("recommendations", []))

        if not recommendations:
            recommendations = [
                "Focus on uncovering pain points before presenting solutions",
                "Ask more implication questions to amplify pain",
                "Use the buyer's own words when presenting value",
                "Handle objections by validating first, then reframing",
                "Use assumptive closes to advance the sale"
            ]

        return recommendations[:7]  # Limit to 7 recommendations


class RealTimeAssistant:
    """
    Provides real-time suggestions during live sales calls
    """

    def __init__(self, vector_db_path: str = "./data/vector_db"):
        self.vector_store = VectorStore(vector_db_path)
        self.analyzer = SalesConversationAnalyzer(vector_db_path=vector_db_path)

    def get_suggestions(
        self,
        current_transcript: str,
        buyer_state: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Get real-time suggestions for the agent

        Args:
            current_transcript: Current conversation so far
            buyer_state: Current state of the buyer

        Returns:
            Suggestions dictionary
        """
        # Analyze current state
        patterns = self.analyzer.pattern_detector.detect_patterns(current_transcript)
        buyer_signals = self.analyzer.buyer_signal_detector.analyze(current_transcript)

        # Find similar successful conversations
        embedding = self.analyzer._generate_embedding(current_transcript, patterns)
        similar_convos = self.vector_store.find_similar(
            embedding=embedding,
            filters={"outcome": "positive"},
            limit=3
        )

        # Determine next best action
        next_action = self._determine_next_action(
            patterns=patterns,
            buyer_state=buyer_state,
            similar_convos=similar_convos
        )

        return {
            "next_best_action": next_action["action"],
            "recommended_technique": next_action["technique"],
            "example_question": next_action["example"],
            "why": next_action["reasoning"],
            "buyer_state": buyer_signals,
            "similar_successful_patterns": similar_convos[:2]
        }

    def _determine_next_action(
        self,
        patterns: List[Dict],
        buyer_state: Dict,
        similar_convos: List[Dict]
    ) -> Dict[str, str]:
        """Determine the next best action based on current state"""
        # This is a simplified version - production would be more sophisticated

        pain_identified = buyer_state.get("pain_identified", False)
        value_understood = buyer_state.get("value_understood", False)
        objections = buyer_state.get("objections", [])

        if not pain_identified:
            return {
                "action": "Uncover pain points",
                "technique": "SPIN Problem Question",
                "example": "What's the biggest challenge with your current approach?",
                "reasoning": "Need to identify pain before presenting solution"
            }
        elif pain_identified and not value_understood:
            return {
                "action": "Amplify pain with implication question",
                "technique": "SPIN Implication Question",
                "example": "If this continues for another quarter, what's the impact on your goals?",
                "reasoning": "Pain identified but need to amplify urgency"
            }
        elif objections:
            return {
                "action": "Handle objection",
                "technique": "Validate and Reframe",
                "example": f"I understand. Many clients initially thought {objections[0]}, but...",
                "reasoning": f"Need to address {objections[0]} objection"
            }
        else:
            return {
                "action": "Move to close",
                "technique": "Assumptive Close",
                "example": "Let's get you started. When would be the best time to implement this?",
                "reasoning": "All buying criteria met, ready to close"
            }


# Example usage
if __name__ == "__main__":
    # Initialize analyzer
    analyzer = SalesConversationAnalyzer(
        vector_db_path="./data/vector_db"
    )

    # Sample conversation
    sample_transcript = """
    Agent: Hi John, thanks for taking my call. I understand you're looking to improve your team's productivity?

    Prospect: Yeah, we've been struggling with that lately.

    Agent: Tell me more. What's the biggest challenge right now?

    Prospect: Well, our current system is really clunky. It takes forever to get anything done.

    Agent: I see. How is that affecting your team?

    Prospect: They're frustrated. We're missing deadlines. It's not good.

    Agent: If this continues for another quarter, what's the impact on your revenue goals?

    Prospect: Honestly, we'll probably miss our Q4 targets. That's a big problem.

    Agent: I understand. What would it mean for you if your team could work 30% faster?

    Prospect: That would be huge. We'd hit our goals and probably exceed them.

    Agent: Great. Let me show you how we can make that happen. Would next Tuesday work for a demo?

    Prospect: Yeah, let's do it.
    """

    # Analyze
    analysis = analyzer.analyze(
        transcript=sample_transcript,
        metadata={
            "conversation_id": "conv_001",
            "outcome": "booked_demo",
            "industry": "SaaS"
        }
    )

    # Print results
    print(f"Effectiveness Score: {analysis.effectiveness_score:.2f}")
    print(f"Buyer Intent Score: {analysis.buyer_signals.get('intent_score', 0)}")
    print(f"Training Value: {analysis.training_value}")
    print(f"\nKey Patterns: {len(analysis.key_patterns)}")
    for pattern in analysis.key_patterns:
        print(f"  - {pattern.get('technique')}: {pattern.get('text', '')[:50]}...")
    print(f"\nRecommendations:")
    for rec in analysis.recommendations[:3]:
        print(f"  - {rec}")
