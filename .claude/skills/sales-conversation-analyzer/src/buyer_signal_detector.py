"""
Buyer Signal Detector - Detects buyer intent and engagement signals
"""

import re
from typing import Dict, List, Any


class BuyerSignalDetector:
    """
    Detects buyer signals indicating intent, pain, authority, budget, timeline
    """

    def __init__(self):
        self.signals = self._load_signal_patterns()

    def analyze(self, transcript: str) -> Dict[str, Any]:
        """
        Analyze transcript for buyer signals

        Args:
            transcript: Full conversation transcript

        Returns:
            Dictionary of buyer signals and scores
        """
        # Detect various signal categories
        intent_signals = self._detect_intent_signals(transcript)
        pain_signals = self._detect_pain_signals(transcript)
        authority_signals = self._detect_authority_signals(transcript)
        budget_signals = self._detect_budget_signals(transcript)
        timeline_signals = self._detect_timeline_signals(transcript)
        objection_signals = self._detect_objections(transcript)

        # Calculate intent score
        intent_score = self._calculate_intent_score(intent_signals)

        # Determine pain level
        pain_level = self._determine_pain_level(pain_signals)

        # Determine authority
        authority = self._determine_authority(authority_signals)

        # Determine budget qualification
        budget_qualification = self._determine_budget_qualification(budget_signals)

        # Determine timeline
        timeline = self._determine_timeline(timeline_signals)

        return {
            "intent_score": intent_score,
            "pain_level": pain_level,
            "authority": authority,
            "budget_qualification": budget_qualification,
            "timeline": timeline,
            "objections": objection_signals,
            "positive_indicators": intent_signals.get("high", []),
            "engagement_level": self._calculate_engagement(intent_signals, pain_signals)
        }

    def _load_signal_patterns(self) -> Dict:
        """Load signal detection patterns"""
        return {
            "high_intent": [
                r"what'?s the (price|cost|pricing)",
                r"how much (does it cost|is it)",
                r"(tell me|show me) about pricing",
                r"when can we (start|begin|implement)",
                r"(request|need|want) a (demo|trial)",
                r"compared to \w+",  # comparing to competitors
                r"what about (contract|terms|agreement)",
                r"do you have (references|case studies|testimonials)",
                r"how long (is|does) (the|your)? ?implementation",
                r"can you send (proposal|quote|estimate)",
                r"(I|we)'?(ll|d) like to move forward",
                r"let'?s (schedule|book|set up)",
                r"who would be our (contact|account manager)",
            ],
            "medium_intent": [
                r"tell me more about",
                r"how does (this|that|it) work",
                r"what (features|capabilities|integrations)",
                r"(I|we)'?m interested in",
                r"this (sounds|seems) (interesting|good)",
                r"what (else|other)",
                r"can (you|it|this)",
            ],
            "pain": [
                r"(struggling|having trouble|difficult) (with|to)",
                r"(frustrated|annoyed|upset) (with|about|by)",
                r"(problem|issue|challenge) (is|with)",
                r"not working",
                r"broken",
                r"inefficient",
                r"(wasting|losing) (time|money)",
                r"(constantly|always|keeps) (breaking|failing)",
                r"missing deadlines",
                r"customers are complaining",
                r"losing (customers|revenue|business)",
            ],
            "authority": [
                r"(I|we) (make|made) (the|this) decision",
                r"(I|we) (have|control) the budget",
                r"(I|we) can (approve|sign off)",
                r"(I|we)'?re the (decision maker|one who decides)",
                r"it'?s (my|our) (decision|call)",
            ],
            "influencer": [
                r"(I|we)'?ll (need to|have to) (check|ask|run this by)",
                r"(I|we) need (approval|sign off) from",
                r"(boss|manager|team) (needs to|has to) (approve|decide)",
                r"(I|we)'?m not the (only|final) decision maker",
            ],
            "budget": [
                r"(have|got|allocated) (budget|funds|money)",
                r"(budget|money) (is|was) (approved|set aside)",
                r"we can (spend|invest|afford)",
                r"(we|I) budgeted \$?\d",
            ],
            "no_budget": [
                r"(no|don'?t have) (budget|money|funds)",
                r"not in the budget",
                r"can'?t afford",
                r"too expensive",
                r"out of our price range",
            ],
            "timeline_immediate": [
                r"(need|want) (this|it) (now|asap|immediately|urgently)",
                r"(as soon as possible|right away)",
                r"(this|next) (week|month)",
            ],
            "timeline_near": [
                r"(within|in) (the)? ?(next)? ?\d+ (weeks?|months?)",
                r"(this|next) (quarter|Q\d)",
                r"(by|before) (end of|the end of)",
            ],
            "timeline_far": [
                r"(next year|2025|2026)",
                r"(in)? ?(6|six|7|seven|8|eight|9|nine|10|ten|11|eleven|12|twelve) months",
                r"not (urgent|a priority right now)",
            ],
            "objections": {
                "price": [
                    r"too expensive",
                    r"(can'?t|cannot) afford",
                    r"(out of|over) (budget|price range)",
                    r"(too much|costs too much)",
                    r"cheaper (option|alternative)"
                ],
                "timing": [
                    r"not (right now|now|yet)",
                    r"(maybe|call|talk) later",
                    r"(too|really) busy",
                    r"not the right time"
                ],
                "authority": [
                    r"(need to|have to) (check|ask)",
                    r"not my decision",
                    r"(have to|need to) talk to"
                ],
                "need": [
                    r"(don'?t|do not) (need|want) (this|that|it)",
                    r"not (interested|looking)",
                    r"(happy|satisfied) with (current|what we have)"
                ],
                "trust": [
                    r"(never heard|not familiar|don'?t know) (of|about) (you|your company)",
                    r"can I trust",
                    r"(sounds|seems) too good to be true"
                ]
            }
        }

    def _detect_intent_signals(self, transcript: str) -> Dict[str, List[str]]:
        """Detect intent signals"""
        high = self._find_matches(transcript, self.signals["high_intent"])
        medium = self._find_matches(transcript, self.signals["medium_intent"])

        return {
            "high": high,
            "medium": medium
        }

    def _detect_pain_signals(self, transcript: str) -> List[str]:
        """Detect pain signals"""
        return self._find_matches(transcript, self.signals["pain"])

    def _detect_authority_signals(self, transcript: str) -> Dict[str, List[str]]:
        """Detect authority signals"""
        decision_maker = self._find_matches(transcript, self.signals["authority"])
        influencer = self._find_matches(transcript, self.signals["influencer"])

        return {
            "decision_maker": decision_maker,
            "influencer": influencer
        }

    def _detect_budget_signals(self, transcript: str) -> Dict[str, List[str]]:
        """Detect budget signals"""
        has_budget = self._find_matches(transcript, self.signals["budget"])
        no_budget = self._find_matches(transcript, self.signals["no_budget"])

        return {
            "has_budget": has_budget,
            "no_budget": no_budget
        }

    def _detect_timeline_signals(self, transcript: str) -> Dict[str, List[str]]:
        """Detect timeline signals"""
        immediate = self._find_matches(transcript, self.signals["timeline_immediate"])
        near = self._find_matches(transcript, self.signals["timeline_near"])
        far = self._find_matches(transcript, self.signals["timeline_far"])

        return {
            "immediate": immediate,
            "near": near,
            "far": far
        }

    def _detect_objections(self, transcript: str) -> List[str]:
        """Detect objections"""
        objections = []

        for objection_type, patterns in self.signals["objections"].items():
            matches = self._find_matches(transcript, patterns)
            if matches:
                objections.append(objection_type)

        return objections

    def _find_matches(self, text: str, patterns: List[str]) -> List[str]:
        """Find pattern matches in text"""
        matches = []

        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                # Extract the matching sentence or phrase
                sentences = re.split(r'[.!?\n]+', text)
                for sentence in sentences:
                    if re.search(pattern, sentence, re.IGNORECASE):
                        matches.append(sentence.strip())
                        break

        return matches[:5]  # Limit to 5 matches

    def _calculate_intent_score(self, intent_signals: Dict) -> int:
        """Calculate intent score (0-100)"""
        high_count = len(intent_signals.get("high", []))
        medium_count = len(intent_signals.get("medium", []))

        # High signals worth 15 points each, medium worth 5 points each
        score = min(high_count * 15 + medium_count * 5, 100)

        # Baseline score
        if score == 0:
            score = 50  # Neutral if no signals detected

        return score

    def _determine_pain_level(self, pain_signals: List[str]) -> str:
        """Determine pain level"""
        count = len(pain_signals)

        if count >= 3:
            return "high"
        elif count >= 1:
            return "medium"
        else:
            return "low"

    def _determine_authority(self, authority_signals: Dict) -> str:
        """Determine authority level"""
        decision_maker = authority_signals.get("decision_maker", [])
        influencer = authority_signals.get("influencer", [])

        if decision_maker:
            return "decision_maker"
        elif influencer:
            return "influencer"
        else:
            return "unknown"

    def _determine_budget_qualification(self, budget_signals: Dict) -> str:
        """Determine budget qualification"""
        has_budget = budget_signals.get("has_budget", [])
        no_budget = budget_signals.get("no_budget", [])

        if has_budget and not no_budget:
            return "qualified"
        elif no_budget:
            return "not_qualified"
        else:
            return "unknown"

    def _determine_timeline(self, timeline_signals: Dict) -> str:
        """Determine timeline"""
        immediate = timeline_signals.get("immediate", [])
        near = timeline_signals.get("near", [])
        far = timeline_signals.get("far", [])

        if immediate:
            return "immediate"
        elif near:
            return "near_term"
        elif far:
            return "long_term"
        else:
            return "unknown"

    def _calculate_engagement(self, intent_signals: Dict, pain_signals: List[str]) -> str:
        """Calculate overall engagement level"""
        intent_count = len(intent_signals.get("high", [])) + len(intent_signals.get("medium", []))
        pain_count = len(pain_signals)
        total = intent_count + pain_count

        if total >= 5:
            return "high"
        elif total >= 2:
            return "medium"
        else:
            return "low"
