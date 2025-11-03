"""
Pattern Detector - Detects sales conversation patterns and techniques
"""

import re
from typing import List, Dict, Any
import json


class PatternDetector:
    """
    Detects sales patterns and techniques in conversations
    """

    def __init__(self, frameworks: List[str] = None):
        """
        Initialize pattern detector

        Args:
            frameworks: List of frameworks to detect (SPIN, Challenger, etc.)
        """
        self.frameworks = frameworks or ["SPIN", "Challenger", "Gap_Selling", "MEDDIC"]
        self.patterns = self._load_patterns()

    def _load_patterns(self) -> Dict[str, List[Dict]]:
        """Load pattern definitions for each framework"""
        return {
            "SPIN": self._spin_patterns(),
            "Challenger": self._challenger_patterns(),
            "Gap_Selling": self._gap_selling_patterns(),
            "MEDDIC": self._meddic_patterns(),
            "Never_Split_Difference": self._voss_patterns(),
            "Sandler": self._sandler_patterns(),
            "BANT": self._bant_patterns(),
            "Value_Selling": self._value_selling_patterns(),
            "Solution_Selling": self._solution_selling_patterns(),
            "NEAT": self._neat_patterns(),
            "Conceptual_Selling": self._conceptual_selling_patterns(),
            "Straight_Line": []  # Already defined above
        }

    def detect_patterns(self, transcript: str) -> List[Dict[str, Any]]:
        """
        Detect patterns in the conversation

        Args:
            transcript: Full conversation transcript

        Returns:
            List of detected patterns
        """
        detected = []

        for framework in self.frameworks:
            if framework in self.patterns:
                framework_patterns = self._detect_framework_patterns(
                    transcript,
                    self.patterns[framework],
                    framework
                )
                detected.extend(framework_patterns)

        return detected

    def _detect_framework_patterns(
        self,
        transcript: str,
        patterns: List[Dict],
        framework: str
    ) -> List[Dict[str, Any]]:
        """Detect patterns for a specific framework"""
        detected = []

        for pattern in patterns:
            matches = self._find_pattern_matches(transcript, pattern)
            for match in matches:
                detected.append({
                    "pattern_type": pattern["type"],
                    "technique": f"{framework}_{pattern['name']}",
                    "text": match["text"],
                    "effectiveness": pattern.get("effectiveness", 0.7),
                    "framework": framework,
                    "description": pattern.get("description", "")
                })

        return detected

    def _find_pattern_matches(self, transcript: str, pattern: Dict) -> List[Dict]:
        """Find matches for a specific pattern"""
        matches = []
        keywords = pattern.get("keywords", [])
        regex_patterns = pattern.get("regex", [])

        # Keyword matching
        for keyword in keywords:
            if keyword.lower() in transcript.lower():
                # Find the sentence containing the keyword
                sentences = self._split_into_sentences(transcript)
                for sentence in sentences:
                    if keyword.lower() in sentence.lower():
                        matches.append({
                            "text": sentence.strip(),
                            "match_type": "keyword",
                            "keyword": keyword
                        })

        # Regex matching
        for regex in regex_patterns:
            for match in re.finditer(regex, transcript, re.IGNORECASE):
                matches.append({
                    "text": match.group(0),
                    "match_type": "regex",
                    "pattern": regex
                })

        return matches[:3]  # Limit to 3 matches per pattern

    def _split_into_sentences(self, text: str) -> List[str]:
        """Simple sentence splitter"""
        # Split on common sentence endings
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]

    # Framework Pattern Definitions

    def _spin_patterns(self) -> List[Dict]:
        """SPIN Selling patterns"""
        return [
            {
                "name": "Situation_Question",
                "type": "discovery",
                "keywords": [
                    "current setup",
                    "how long have you",
                    "tell me about your",
                    "walk me through",
                    "who's responsible"
                ],
                "regex": [
                    r"(what|how|who).*(current|currently|right now)",
                    r"tell me about"
                ],
                "description": "Gathering context and background information",
                "effectiveness": 0.6
            },
            {
                "name": "Problem_Question",
                "type": "pain_discovery",
                "keywords": [
                    "biggest challenge",
                    "what's the problem",
                    "struggling with",
                    "issues with",
                    "difficulties",
                    "what's not working"
                ],
                "regex": [
                    r"what'?s? the (biggest|main)? ?(challenge|problem|issue)",
                    r"(struggling|having trouble|difficult) with"
                ],
                "description": "Uncovering problems and dissatisfaction",
                "effectiveness": 0.85
            },
            {
                "name": "Implication_Question",
                "type": "pain_amplification",
                "keywords": [
                    "if this continues",
                    "impact on",
                    "affect your",
                    "what's the cost",
                    "how does that affect",
                    "what happens if"
                ],
                "regex": [
                    r"if (this|that) continues",
                    r"what'?s? the (impact|effect|cost)",
                    r"how (does|would) (this|that) affect"
                ],
                "description": "Amplifying pain and creating urgency",
                "effectiveness": 0.9
            },
            {
                "name": "Need_Payoff_Question",
                "type": "value_articulation",
                "keywords": [
                    "if you could solve",
                    "what would that mean",
                    "how would you benefit",
                    "what would be possible",
                    "imagine if"
                ],
                "regex": [
                    r"if you could (solve|fix|improve)",
                    r"what would (that mean|be possible|change)",
                    r"how would (you|your team) benefit"
                ],
                "description": "Having buyer articulate value",
                "effectiveness": 0.88
            }
        ]

    def _challenger_patterns(self) -> List[Dict]:
        """Challenger Sale patterns"""
        return [
            {
                "name": "Teach_Insight",
                "type": "teaching",
                "keywords": [
                    "did you know",
                    "most companies don't realize",
                    "what we're seeing",
                    "here's what's interesting",
                    "surprising finding"
                ],
                "regex": [
                    r"did you know",
                    r"most .* don'?t realize",
                    r"what we'?re seeing (is|across)"
                ],
                "description": "Teaching unique insight",
                "effectiveness": 0.82
            },
            {
                "name": "Tailor_Message",
                "type": "personalization",
                "keywords": [
                    "given your",
                    "for companies like yours",
                    "in your industry",
                    "specific to your"
                ],
                "regex": [
                    r"given your",
                    r"for (companies|organizations) like (you|yours)",
                    r"in your (industry|situation)"
                ],
                "description": "Tailoring message to specific situation",
                "effectiveness": 0.8
            },
            {
                "name": "Take_Control",
                "type": "assertiveness",
                "keywords": [
                    "here's what I recommend",
                    "the best path is",
                    "let's move forward",
                    "what we should do next"
                ],
                "regex": [
                    r"here'?s what (I|we) recommend",
                    r"the best (path|approach|way) is",
                    r"let'?s (move forward|do this)"
                ],
                "description": "Taking control of the conversation",
                "effectiveness": 0.85
            }
        ]

    def _gap_selling_patterns(self) -> List[Dict]:
        """Gap Selling patterns"""
        return [
            {
                "name": "Current_State_Discovery",
                "type": "current_state",
                "keywords": [
                    "what does it look like today",
                    "how are you currently",
                    "what's working",
                    "what's not working"
                ],
                "regex": [
                    r"what (does|is) .* (today|currently|right now)",
                    r"how are you (currently|now)"
                ],
                "description": "Understanding current state",
                "effectiveness": 0.75
            },
            {
                "name": "Future_State_Vision",
                "type": "future_state",
                "keywords": [
                    "what does success look like",
                    "if everything worked perfectly",
                    "where do you want to be",
                    "your ideal scenario"
                ],
                "regex": [
                    r"what does success look like",
                    r"if everything worked (perfectly|ideally)",
                    r"where (do you|would you like to) (want to )?be"
                ],
                "description": "Painting future state vision",
                "effectiveness": 0.83
            },
            {
                "name": "Gap_Quantification",
                "type": "gap_analysis",
                "keywords": [
                    "gap between",
                    "difference between where you are",
                    "what it's costing you"
                ],
                "regex": [
                    r"gap between",
                    r"difference between .* where you (are|want)"
                ],
                "description": "Quantifying the gap",
                "effectiveness": 0.87
            }
        ]

    def _meddic_patterns(self) -> List[Dict]:
        """MEDDIC patterns"""
        return [
            {
                "name": "Metrics_Discovery",
                "type": "metrics",
                "keywords": [
                    "what metrics",
                    "how do you measure",
                    "what's the ROI",
                    "quantify the impact"
                ],
                "regex": [
                    r"what (metrics|numbers|KPIs)",
                    r"how do you measure"
                ],
                "description": "Discovering key metrics",
                "effectiveness": 0.8
            },
            {
                "name": "Economic_Buyer_Identification",
                "type": "authority",
                "keywords": [
                    "who makes the final decision",
                    "who signs off",
                    "who controls the budget"
                ],
                "regex": [
                    r"who (makes|has) (the)? ?(final)? ?decision",
                    r"who (signs off|approves|controls the budget)"
                ],
                "description": "Identifying economic buyer",
                "effectiveness": 0.92
            },
            {
                "name": "Decision_Criteria",
                "type": "criteria",
                "keywords": [
                    "what's most important",
                    "how will you evaluate",
                    "what criteria"
                ],
                "regex": [
                    r"what'?s (most important|critical)",
                    r"how will you (evaluate|decide|choose)"
                ],
                "description": "Understanding decision criteria",
                "effectiveness": 0.85
            },
            {
                "name": "Pain_Identification",
                "type": "pain",
                "keywords": [
                    "what pain",
                    "what's broken",
                    "what keeps you up"
                ],
                "regex": [
                    r"what (pain|problem|issue)",
                    r"what keeps you (up|awake)"
                ],
                "description": "Identifying pain points",
                "effectiveness": 0.88
            }
        ]

    def _voss_patterns(self) -> List[Dict]:
        """Chris Voss Never Split the Difference patterns"""
        return [
            {
                "name": "Labeling",
                "type": "tactical_empathy",
                "keywords": [
                    "it seems like",
                    "it sounds like",
                    "it looks like"
                ],
                "regex": [
                    r"it (seems|sounds|looks) like"
                ],
                "description": "Labeling emotions",
                "effectiveness": 0.81
            },
            {
                "name": "Mirroring",
                "type": "tactical_empathy",
                "keywords": [],  # Detected by pattern of repeating last words
                "regex": [],
                "description": "Mirroring last 1-3 words",
                "effectiveness": 0.75
            },
            {
                "name": "Calibrated_Question",
                "type": "negotiation",
                "keywords": [
                    "how am I supposed to",
                    "what am I supposed to",
                    "how can I"
                ],
                "regex": [
                    r"how (am I|can I) supposed to",
                    r"what (am I|should I) supposed to"
                ],
                "description": "Calibrated questions",
                "effectiveness": 0.86
            },
            {
                "name": "No_Oriented_Question",
                "type": "negotiation",
                "keywords": [
                    "is now a bad time",
                    "have you given up",
                    "is there any reason we shouldn't"
                ],
                "regex": [
                    r"is (now|this) a bad time",
                    r"have you given up",
                    r"is there any reason .* shouldn'?t"
                ],
                "description": "No-oriented questions",
                "effectiveness": 0.79
            }
        ]

    def _sandler_patterns(self) -> List[Dict]:
        """Sandler Selling System patterns"""
        return [
            {
                "name": "Pain_Budget_Decision",
                "type": "qualification",
                "keywords": [
                    "is this a priority",
                    "do you have budget",
                    "who else needs to be involved"
                ],
                "regex": [
                    r"is this a (priority|top priority)",
                    r"do you have (budget|funds|money)",
                    r"who (else|also) needs to"
                ],
                "description": "Pain-Budget-Decision qualification",
                "effectiveness": 0.84
            },
            {
                "name": "Upfront_Contract",
                "type": "process",
                "keywords": [
                    "at the end of this call",
                    "here's what we'll cover",
                    "sound fair"
                ],
                "regex": [
                    r"at the end of (this|our) (call|meeting)",
                    r"here'?s what we'?ll cover"
                ],
                "description": "Setting upfront contract",
                "effectiveness": 0.77
            }
        ]

    def _bant_patterns(self) -> List[Dict]:
        """BANT Qualification patterns"""
        return [
            {
                "name": "Budget_Qualification",
                "type": "qualification",
                "keywords": [
                    "what's your budget",
                    "budget allocated",
                    "how much can you spend",
                    "budget approved"
                ],
                "regex": [
                    r"what'?s (your|the) budget",
                    r"budget (allocated|approved|available)",
                    r"how much can you (spend|invest)"
                ],
                "description": "Qualifying budget availability",
                "effectiveness": 0.82
            },
            {
                "name": "Authority_Identification",
                "type": "qualification",
                "keywords": [
                    "who makes the decision",
                    "who signs off",
                    "decision maker",
                    "who approves"
                ],
                "regex": [
                    r"who (makes|has) (the)? ?(final)? ?decision",
                    r"who (signs off|approves)",
                    r"who'?s the decision maker"
                ],
                "description": "Identifying decision authority",
                "effectiveness": 0.89
            },
            {
                "name": "Need_Qualification",
                "type": "qualification",
                "keywords": [
                    "why do you need",
                    "what problem are you solving",
                    "why is this important"
                ],
                "regex": [
                    r"why (do you need|is this important)",
                    r"what (problem|challenge) are you solving"
                ],
                "description": "Qualifying need and urgency",
                "effectiveness": 0.81
            },
            {
                "name": "Timeline_Qualification",
                "type": "qualification",
                "keywords": [
                    "when do you need",
                    "what's your timeline",
                    "by when",
                    "implementation date"
                ],
                "regex": [
                    r"when (do you need|are you looking to)",
                    r"what'?s (your|the) timeline",
                    r"by when"
                ],
                "description": "Qualifying timeline and urgency",
                "effectiveness": 0.78
            }
        ]

    def _value_selling_patterns(self) -> List[Dict]:
        """Value Selling patterns"""
        return [
            {
                "name": "ROI_Quantification",
                "type": "value",
                "keywords": [
                    "return on investment",
                    "ROI",
                    "payback period",
                    "cost savings",
                    "revenue increase"
                ],
                "regex": [
                    r"(return on investment|ROI)",
                    r"payback (period|in)",
                    r"(cost savings|save you|revenue increase)"
                ],
                "description": "Quantifying ROI and business value",
                "effectiveness": 0.88
            },
            {
                "name": "Business_Case_Building",
                "type": "value",
                "keywords": [
                    "business case",
                    "justify the investment",
                    "present to executives",
                    "board approval"
                ],
                "regex": [
                    r"business case",
                    r"justify (the|this) investment",
                    r"present to (executives|board|leadership)"
                ],
                "description": "Building business case for decision makers",
                "effectiveness": 0.85
            },
            {
                "name": "Cost_of_Inaction",
                "type": "value",
                "keywords": [
                    "cost of doing nothing",
                    "if you don't solve this",
                    "what's it costing you",
                    "impact of waiting"
                ],
                "regex": [
                    r"cost of (doing nothing|inaction|waiting)",
                    r"if you don'?t solve this",
                    r"what'?s (it|this) costing you"
                ],
                "description": "Quantifying cost of maintaining status quo",
                "effectiveness": 0.90
            }
        ]

    def _solution_selling_patterns(self) -> List[Dict]:
        """Solution Selling patterns"""
        return [
            {
                "name": "Problem_Discovery",
                "type": "discovery",
                "keywords": [
                    "what problem are you trying to solve",
                    "root cause",
                    "underlying issue",
                    "why is this happening"
                ],
                "regex": [
                    r"what (problem|issue|challenge)",
                    r"root cause",
                    r"why is this happening"
                ],
                "description": "Deep problem discovery",
                "effectiveness": 0.86
            },
            {
                "name": "Implementation_Planning",
                "type": "solution",
                "keywords": [
                    "implementation plan",
                    "rollout strategy",
                    "integration process",
                    "onboarding"
                ],
                "regex": [
                    r"implementation (plan|process|timeline)",
                    r"rollout strategy",
                    r"how (we|you) would integrate"
                ],
                "description": "Planning solution implementation",
                "effectiveness": 0.82
            },
            {
                "name": "Proof_of_Concept",
                "type": "solution",
                "keywords": [
                    "proof of concept",
                    "pilot program",
                    "trial",
                    "test it out"
                ],
                "regex": [
                    r"proof of concept",
                    r"pilot (program|project)",
                    r"(trial|test) (it|this) out"
                ],
                "description": "Offering proof of concept or pilot",
                "effectiveness": 0.84
            }
        ]

    def _neat_patterns(self) -> List[Dict]:
        """NEAT Selling patterns"""
        return [
            {
                "name": "Core_Needs_Discovery",
                "type": "discovery",
                "keywords": [
                    "core need",
                    "fundamental challenge",
                    "strategic priority",
                    "business objective"
                ],
                "regex": [
                    r"core (need|challenge|objective)",
                    r"(fundamental|strategic) (challenge|priority)",
                    r"business objective"
                ],
                "description": "Discovering core business needs",
                "effectiveness": 0.85
            },
            {
                "name": "Economic_Impact",
                "type": "value",
                "keywords": [
                    "economic impact",
                    "bottom line",
                    "financial impact",
                    "affect revenue"
                ],
                "regex": [
                    r"economic impact",
                    r"(bottom line|financial) impact",
                    r"(affect|impact) (revenue|profit)"
                ],
                "description": "Discussing economic business impact",
                "effectiveness": 0.87
            },
            {
                "name": "Access_to_Authority",
                "type": "qualification",
                "keywords": [
                    "introduce me to",
                    "speak with your",
                    "meet the",
                    "include in conversation"
                ],
                "regex": [
                    r"introduce me to",
                    r"speak with (your|the)",
                    r"(meet|include) the"
                ],
                "description": "Requesting access to decision makers",
                "effectiveness": 0.83
            }
        ]

    def _conceptual_selling_patterns(self) -> List[Dict]:
        """Conceptual Selling patterns"""
        return [
            {
                "name": "Concept_Questions",
                "type": "discovery",
                "keywords": [
                    "ideal solution",
                    "perfect world",
                    "if you could wave a magic wand",
                    "what does success look like"
                ],
                "regex": [
                    r"ideal (solution|scenario|situation)",
                    r"(perfect|ideal) world",
                    r"(wave a magic wand|dream scenario)",
                    r"what does success look like"
                ],
                "description": "Understanding buyer's concept of solution",
                "effectiveness": 0.84
            },
            {
                "name": "Win_Results",
                "type": "value",
                "keywords": [
                    "what would winning look like",
                    "how will you know if successful",
                    "measure success",
                    "definition of success"
                ],
                "regex": [
                    r"what (would|does) winning look like",
                    r"how (will|would) you (know|measure) (if|whether) successful",
                    r"definition of success"
                ],
                "description": "Defining what winning looks like",
                "effectiveness": 0.82
            },
            {
                "name": "Buying_Vision",
                "type": "discovery",
                "keywords": [
                    "envision",
                    "picture this",
                    "imagine if",
                    "think about"
                ],
                "regex": [
                    r"(envision|picture|imagine) (this|if|that)",
                    r"think about (what|how)"
                ],
                "description": "Building buying vision with prospect",
                "effectiveness": 0.80
            }
        ]
