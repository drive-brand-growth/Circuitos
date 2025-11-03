"""
Flow Analyzer - Analyzes conversation flow and structure
"""

from typing import Dict, List, Any
import re


class FlowAnalyzer:
    """
    Analyzes conversation flow, structure, and progression
    """

    def __init__(self):
        self.optimal_phases = [
            "rapport_building",
            "pain_discovery",
            "value_proposition",
            "objection_handling",
            "closing"
        ]

    def analyze(self, transcript: str, patterns: List[Dict]) -> Dict[str, Any]:
        """
        Analyze conversation flow

        Args:
            transcript: Full conversation transcript
            patterns: Detected patterns

        Returns:
            Flow analysis dictionary
        """
        # Split conversation into messages
        messages = self._split_into_messages(transcript)

        # Identify phases
        phases_completed = self._identify_phases(messages, patterns)

        # Calculate talk ratio
        talk_ratio = self._calculate_talk_ratio(messages)

        # Identify optimal moments
        optimal_moments = self._identify_optimal_moments(messages, patterns)

        # Identify missed opportunities
        missed_opportunities = self._identify_missed_opportunities(phases_completed, patterns)

        # Calculate structure quality
        structure_quality = self._calculate_structure_quality(phases_completed, talk_ratio)

        return {
            "structure_quality": structure_quality,
            "phases_completed": phases_completed,
            "phases_optimal": self.optimal_phases,
            "completion_rate": len(phases_completed) / len(self.optimal_phases),
            "talk_ratio": talk_ratio,
            "optimal_moments": optimal_moments,
            "missed_opportunities": missed_opportunities,
            "total_messages": len(messages),
            "avg_message_length": sum(len(m["text"]) for m in messages) / len(messages) if messages else 0
        }

    def _split_into_messages(self, transcript: str) -> List[Dict]:
        """Split transcript into individual messages"""
        messages = []

        # Look for speaker labels (e.g., "Agent:", "Prospect:", "Customer:")
        # Split on common patterns
        lines = transcript.split('\n')

        current_speaker = None
        current_text = []

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Check if line starts with a speaker label
            speaker_match = re.match(r'^(Agent|Prospect|Customer|Rep|Buyer|Client|Seller):\s*(.*)$', line, re.IGNORECASE)

            if speaker_match:
                # Save previous message
                if current_speaker and current_text:
                    messages.append({
                        "speaker": current_speaker,
                        "text": ' '.join(current_text)
                    })
                    current_text = []

                # Start new message
                current_speaker = speaker_match.group(1).lower()
                text = speaker_match.group(2).strip()
                if text:
                    current_text.append(text)
            else:
                # Continue current message
                if line:
                    current_text.append(line)

        # Add final message
        if current_speaker and current_text:
            messages.append({
                "speaker": current_speaker,
                "text": ' '.join(current_text)
            })

        # If no speaker labels found, try to split by question marks or periods
        if not messages:
            sentences = re.split(r'[.!?]+', transcript)
            for i, sentence in enumerate(sentences):
                if sentence.strip():
                    messages.append({
                        "speaker": "agent" if i % 2 == 0 else "prospect",
                        "text": sentence.strip()
                    })

        return messages

    def _identify_phases(self, messages: List[Dict], patterns: List[Dict]) -> List[str]:
        """Identify which conversation phases were completed"""
        phases = []

        # Analyze patterns to determine phases
        pattern_types = [p.get("pattern_type", "") for p in patterns]

        # Rapport building (usually first few messages, casual questions)
        if len(messages) >= 2:
            first_messages = [m["text"] for m in messages[:3]]
            rapport_keywords = ["thanks for", "nice to", "how are you", "appreciate", "thanks for taking"]
            if any(keyword in ' '.join(first_messages).lower() for keyword in rapport_keywords):
                phases.append("rapport_building")

        # Pain discovery
        if any(ptype in ["pain_discovery", "discovery", "problem"] for ptype in pattern_types):
            phases.append("pain_discovery")

        # Value proposition
        value_keywords = ["we can", "our solution", "this will", "you'll be able to", "benefit", "help you"]
        if any(keyword in ' '.join([m["text"] for m in messages]).lower() for keyword in value_keywords):
            phases.append("value_proposition")

        # Objection handling
        if any(ptype in ["objection_handling", "negotiation"] for ptype in pattern_types):
            phases.append("objection_handling")

        # Closing
        closing_keywords = ["let's schedule", "when can we", "next step", "move forward", "get started"]
        if any(keyword in ' '.join([m["text"] for m in messages]).lower() for keyword in closing_keywords):
            phases.append("closing")

        return phases

    def _calculate_talk_ratio(self, messages: List[Dict]) -> Dict[str, float]:
        """Calculate talk ratio between agent and prospect"""
        agent_words = 0
        prospect_words = 0

        for message in messages:
            word_count = len(message["text"].split())
            speaker = message["speaker"].lower()

            if speaker in ["agent", "rep", "seller"]:
                agent_words += word_count
            elif speaker in ["prospect", "customer", "buyer", "client"]:
                prospect_words += word_count

        total_words = agent_words + prospect_words

        if total_words == 0:
            return {"agent": 0.5, "prospect": 0.5}

        return {
            "agent": agent_words / total_words,
            "prospect": prospect_words / total_words,
            "total_words": total_words,
            "optimal": abs((prospect_words / total_words) - 0.6) < 0.15  # Optimal is prospect talking 55-75%
        }

    def _identify_optimal_moments(self, messages: List[Dict], patterns: List[Dict]) -> List[Dict]:
        """Identify optimal moments in the conversation"""
        optimal_moments = []

        # Look for key patterns that indicate optimal moments
        high_effectiveness_patterns = [p for p in patterns if p.get("effectiveness", 0) >= 0.85]

        for pattern in high_effectiveness_patterns:
            optimal_moments.append({
                "action": pattern.get("technique", ""),
                "effectiveness": pattern.get("effectiveness"),
                "description": f"Used {pattern.get('technique')} effectively"
            })

        return optimal_moments[:5]  # Return top 5

    def _identify_missed_opportunities(self, phases_completed: List[str], patterns: List[Dict]) -> List[str]:
        """Identify missed opportunities in the conversation"""
        missed = []

        # Check for missing phases
        for phase in self.optimal_phases:
            if phase not in phases_completed:
                missed.append(f"Missing {phase.replace('_', ' ')} phase")

        # Check for pattern gaps
        pattern_types = [p.get("pattern_type", "") for p in patterns]

        # If pain discovered but not amplified
        if "pain_discovery" in pattern_types and "pain_amplification" not in pattern_types:
            missed.append("Pain identified but not amplified (missing implication questions)")

        # If value presented but buyer didn't articulate it
        if "value_proposition" in phases_completed and "value_articulation" not in pattern_types:
            missed.append("Presented value but didn't have buyer articulate it (missing need-payoff questions)")

        return missed

    def _calculate_structure_quality(self, phases_completed: List[str], talk_ratio: Dict) -> str:
        """Calculate overall structure quality"""
        # Calculate completion percentage
        completion_rate = len(phases_completed) / len(self.optimal_phases)

        # Check if phases are in logical order
        phase_order_score = self._calculate_phase_order_score(phases_completed)

        # Check talk ratio
        talk_ratio_score = 1.0 if talk_ratio.get("optimal", False) else 0.5

        # Overall score
        overall_score = (completion_rate * 0.5 + phase_order_score * 0.3 + talk_ratio_score * 0.2)

        if overall_score >= 0.8:
            return "excellent"
        elif overall_score >= 0.6:
            return "good"
        elif overall_score >= 0.4:
            return "fair"
        else:
            return "needs_improvement"

    def _calculate_phase_order_score(self, phases_completed: List[str]) -> float:
        """Calculate how well phases follow optimal order"""
        if not phases_completed:
            return 0.0

        order_score = 0.0
        expected_order = {
            "rapport_building": 1,
            "pain_discovery": 2,
            "value_proposition": 3,
            "objection_handling": 4,
            "closing": 5
        }

        # Check if phases generally follow the expected order
        phase_positions = [expected_order.get(phase, 0) for phase in phases_completed]

        # Check if list is mostly sorted
        sorted_positions = sorted(phase_positions)
        matches = sum(1 for a, b in zip(phase_positions, sorted_positions) if a == b)

        order_score = matches / len(phase_positions) if phase_positions else 0

        return order_score
