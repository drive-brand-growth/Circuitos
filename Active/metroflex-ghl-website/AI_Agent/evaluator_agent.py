"""
MetroFlex Response Evaluator Agent - Quality Assurance Layer
============================================================

This agent acts as the "Manager" - evaluating AI-generated responses
before delivery to ensure quality, accuracy, and brand alignment.

The evaluator runs as middleware between response generation and delivery:
    User Query -> Agent -> Response -> EVALUATOR -> (pass/fail/retry) -> GHL -> User

Key capabilities:
1. Factual accuracy validation against knowledge base
2. Brand tone alignment (MetroFlex: confident, professional, no-nonsense)
3. CTA effectiveness scoring
4. Hallucination detection
5. Self-correction loop for failed responses

This replaces the need for a human manager checking every response.
"""

import os
import json
import re
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from openai import OpenAI
from dataclasses import dataclass


# =============================================================================
# EVALUATION RUBRICS
# =============================================================================

EVALUATION_RUBRICS = {
    "conversation": {
        "factual_accuracy": {
            "weight": 0.35,
            "threshold": 0.90,
            "description": "Response contains accurate information from knowledge base",
            "fail_conditions": [
                "Hallucinated pricing not in KB",
                "Incorrect dates/times",
                "Non-existent divisions or rules",
                "Made-up contact information"
            ]
        },
        "tone_alignment": {
            "weight": 0.25,
            "threshold": 0.80,
            "description": "Response matches MetroFlex brand voice",
            "criteria": [
                "Confident and authoritative",
                "Professional and helpful",
                "No-nonsense and direct",
                "Legacy-focused when appropriate"
            ]
        },
        "cta_effectiveness": {
            "weight": 0.20,
            "threshold": 0.85,
            "description": "Clear, specific call-to-action present",
            "criteria": [
                "Single clear next step",
                "Actionable (not vague)",
                "Appropriate urgency",
                "Relevant to query"
            ]
        },
        "length_appropriate": {
            "weight": 0.10,
            "threshold": 0.75,
            "description": "Response length matches channel (SMS: 160 chars, Chat: 300 chars)",
            "criteria": [
                "SMS: Under 160 characters",
                "Chat: 2-4 paragraphs max",
                "Not too verbose",
                "Not too terse"
            ]
        },
        "objection_handling": {
            "weight": 0.10,
            "threshold": 0.80,
            "description": "Objection properly acknowledged and reframed",
            "criteria": [
                "Empathy shown",
                "Concern acknowledged",
                "Value reframed",
                "Proof provided"
            ]
        }
    },
    "workflow": {
        "channel_diversity": {
            "weight": 0.25,
            "threshold": 0.85,
            "description": "Workflow uses multiple channels appropriately",
            "criteria": [
                "Email for detail",
                "SMS for urgency",
                "Social for awareness",
                "Not all same channel"
            ]
        },
        "timing_logic": {
            "weight": 0.35,
            "threshold": 0.90,
            "description": "Timing between touches is appropriate",
            "criteria": [
                "Not too frequent (spam)",
                "Not too sparse (forgotten)",
                "Respects time zones",
                "Escalates appropriately"
            ]
        },
        "personalization_depth": {
            "weight": 0.25,
            "threshold": 0.80,
            "description": "Messages reference lead's specific context",
            "criteria": [
                "Uses name",
                "References their interest",
                "Adapts to awareness level",
                "Progressive disclosure"
            ]
        },
        "framework_application": {
            "weight": 0.15,
            "threshold": 0.85,
            "description": "Proper application of sales frameworks",
            "criteria": [
                "Schwartz awareness matching",
                "Hormozi value equation",
                "Hook-story-offer structure",
                "StoryBrand guide positioning"
            ]
        }
    }
}


# =============================================================================
# DATA MODELS
# =============================================================================

@dataclass
class EvaluationResult:
    """Result of response evaluation"""
    passed: bool
    overall_score: float
    rubric_scores: Dict[str, float]
    failures: List[str]
    warnings: List[str]
    revised_response: Optional[str]
    confidence: float
    evaluation_time_ms: float
    retry_count: int


# =============================================================================
# EVALUATOR AGENT
# =============================================================================

class ResponseEvaluator:
    """
    Grades agent outputs against strict rubrics before delivery.
    Integrates as middleware in webhook handlers.
    """

    def __init__(self, openai_api_key: str = None):
        """Initialize evaluator with OpenAI client"""
        api_key = openai_api_key or os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")

        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4o-mini"  # Cost-optimized
        self.rubrics = EVALUATION_RUBRICS
        self.max_retries = 2  # Maximum self-correction attempts

    def evaluate(
        self,
        agent_type: str,
        response: str,
        context: Dict,
        channel: str = "chat"
    ) -> EvaluationResult:
        """
        Evaluate a response against rubrics.

        Args:
            agent_type: "conversation" or "workflow"
            response: The generated response to evaluate
            context: {
                "user_query": str,
                "knowledge_base_context": str,
                "lead_data": dict,
                "awareness_level": int,
                "detected_objection": dict
            }
            channel: "sms" or "chat"

        Returns:
            EvaluationResult with pass/fail, scores, and optional revision
        """
        import time
        start_time = time.time()

        # Get rubric for this agent type
        rubric = self.rubrics.get(agent_type, self.rubrics["conversation"])

        # Build evaluation prompt
        eval_prompt = self._build_evaluation_prompt(
            response=response,
            context=context,
            rubric=rubric,
            channel=channel
        )

        # Call evaluator LLM
        try:
            evaluation = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self._get_evaluator_system_prompt()},
                    {"role": "user", "content": eval_prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.1  # Low temp for consistent evaluation
            )

            result = json.loads(evaluation.choices[0].message.content)

        except Exception as e:
            # If evaluation fails, pass through (fail-safe)
            return EvaluationResult(
                passed=True,
                overall_score=0.0,
                rubric_scores={},
                failures=[f"Evaluation error: {str(e)}"],
                warnings=["Evaluation failed - response passed through"],
                revised_response=None,
                confidence=0.0,
                evaluation_time_ms=(time.time() - start_time) * 1000,
                retry_count=0
            )

        # Calculate overall score
        overall_score = self._calculate_overall_score(result["rubric_scores"], rubric)

        # Determine if passed
        passed = self._check_passed(result["rubric_scores"], rubric)

        # Attempt self-correction if failed but recoverable
        revised_response = None
        retry_count = 0

        if not passed and overall_score > 0.5:  # Recoverable
            revised_response, retry_count = self._self_correct(
                response=response,
                context=context,
                failures=result.get("failures", []),
                rubric=rubric
            )

            # Re-evaluate revised response
            if revised_response:
                re_eval = self._quick_revalidate(revised_response, context, rubric)
                if re_eval["passed"]:
                    passed = True
                    overall_score = re_eval["score"]

        evaluation_time = (time.time() - start_time) * 1000

        return EvaluationResult(
            passed=passed,
            overall_score=overall_score,
            rubric_scores=result.get("rubric_scores", {}),
            failures=result.get("failures", []),
            warnings=result.get("warnings", []),
            revised_response=revised_response,
            confidence=result.get("confidence", 0.8),
            evaluation_time_ms=evaluation_time,
            retry_count=retry_count
        )

    def _get_evaluator_system_prompt(self) -> str:
        """System prompt for evaluator LLM"""
        return """You are a Quality Assurance Evaluator for MetroFlex Events AI responses.

Your job is to grade AI-generated responses against strict rubrics before they are sent to customers.

EVALUATION PRINCIPLES:
1. Be strict but fair - real quality issues must fail
2. Focus on customer impact - what could hurt the customer or brand?
3. Hallucinations are critical failures - any made-up facts = fail
4. Tone matters - MetroFlex is confident, professional, no-nonsense
5. Actionability matters - vague responses waste customer time

AUTOMATIC FAILURES:
- Hallucinated pricing (any price not in knowledge base)
- Wrong dates/times for events
- Made-up divisions or rules
- Incorrect contact information
- Off-brand tone (too casual, unprofessional, or aggressive)
- Missing CTA when one is clearly needed
- Response too long for channel (SMS > 160 chars)

EVALUATION APPROACH:
1. Check each rubric criterion independently
2. Score 0.0 to 1.0 for each
3. List specific failures with evidence
4. Note warnings (minor issues)
5. Be consistent - same issues = same scores

You must return JSON only."""

    def _build_evaluation_prompt(
        self,
        response: str,
        context: Dict,
        rubric: Dict,
        channel: str
    ) -> str:
        """Build the evaluation prompt"""

        rubric_text = json.dumps(rubric, indent=2)

        return f"""
EVALUATE THIS AI RESPONSE:

---
RESPONSE TO EVALUATE:
"{response}"
---

CONTEXT:
- User Query: {context.get('user_query', 'N/A')}
- Channel: {channel.upper()}
- Awareness Level: {context.get('awareness_level', 'Unknown')}/5
- Detected Objection: {json.dumps(context.get('detected_objection', {}), indent=2)}
- Business Context: {context.get('business_context', 'gym_membership')}

KNOWLEDGE BASE CONTEXT PROVIDED TO AGENT:
{context.get('knowledge_base_context', 'No context provided')}

LEAD DATA:
{json.dumps(context.get('lead_data', {}), indent=2)}

---

RUBRIC TO EVALUATE AGAINST:
{rubric_text}

---

YOUR TASK:
1. Score each rubric criterion from 0.0 to 1.0
2. List any failures (critical issues that must be fixed)
3. List any warnings (minor issues to note)
4. Provide confidence in your evaluation (0.0-1.0)

Return JSON:
{{
    "rubric_scores": {{
        "factual_accuracy": <0.0-1.0>,
        "tone_alignment": <0.0-1.0>,
        "cta_effectiveness": <0.0-1.0>,
        "length_appropriate": <0.0-1.0>,
        "objection_handling": <0.0-1.0>
    }},
    "failures": [
        "<specific failure with evidence>"
    ],
    "warnings": [
        "<minor issue to note>"
    ],
    "confidence": <0.0-1.0>,
    "reasoning": "<brief explanation of evaluation>"
}}
"""

    def _calculate_overall_score(self, rubric_scores: Dict, rubric: Dict) -> float:
        """Calculate weighted overall score"""
        total_score = 0.0
        total_weight = 0.0

        for criterion, score in rubric_scores.items():
            if criterion in rubric:
                weight = rubric[criterion]["weight"]
                total_score += score * weight
                total_weight += weight

        if total_weight == 0:
            return 0.0

        return total_score / total_weight

    def _check_passed(self, rubric_scores: Dict, rubric: Dict) -> bool:
        """Check if all criteria meet thresholds"""
        for criterion, score in rubric_scores.items():
            if criterion in rubric:
                threshold = rubric[criterion]["threshold"]
                if score < threshold:
                    return False
        return True

    def _self_correct(
        self,
        response: str,
        context: Dict,
        failures: List[str],
        rubric: Dict
    ) -> Tuple[Optional[str], int]:
        """
        Attempt to self-correct a failed response.

        Returns:
            (revised_response, retry_count)
        """
        if not failures:
            return None, 0

        correction_prompt = f"""
FIX THIS RESPONSE:

ORIGINAL RESPONSE:
"{response}"

FAILURES TO FIX:
{json.dumps(failures, indent=2)}

CONTEXT:
- User Query: {context.get('user_query', 'N/A')}
- Awareness Level: {context.get('awareness_level', 'Unknown')}/5
- Business Context: {context.get('business_context', 'gym_membership')}

KNOWLEDGE BASE (use ONLY these facts):
{context.get('knowledge_base_context', 'No context provided')}

RULES FOR CORRECTION:
1. Fix ONLY the specific failures listed
2. Maintain the same general message intent
3. Use ONLY facts from the knowledge base - no hallucinations
4. Keep the MetroFlex brand voice (confident, professional, no-nonsense)
5. Ensure there's a clear CTA
6. Stay within character limits for the channel

Return ONLY the corrected response text, nothing else.
"""

        try:
            correction = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a copywriter fixing AI responses. Return ONLY the corrected text."},
                    {"role": "user", "content": correction_prompt}
                ],
                temperature=0.3,
                max_tokens=400
            )

            revised = correction.choices[0].message.content.strip()

            # Remove quotes if the model wrapped the response
            if revised.startswith('"') and revised.endswith('"'):
                revised = revised[1:-1]

            return revised, 1

        except Exception as e:
            print(f"Self-correction failed: {e}")
            return None, 0

    def _quick_revalidate(
        self,
        response: str,
        context: Dict,
        rubric: Dict
    ) -> Dict:
        """Quick revalidation of revised response"""

        # Simplified check - just verify critical issues are fixed
        prompt = f"""
QUICK VALIDATION:

Response: "{response}"

Check these critical criteria:
1. No hallucinated facts (all info matches knowledge base)
2. Has clear CTA
3. Appropriate length for channel
4. Professional tone

Knowledge Base:
{context.get('knowledge_base_context', 'N/A')}

Return JSON:
{{"passed": true/false, "score": 0.0-1.0, "reason": "brief explanation"}}
"""

        try:
            result = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
                temperature=0.1
            )

            return json.loads(result.choices[0].message.content)

        except Exception:
            return {"passed": False, "score": 0.0}


# =============================================================================
# MIDDLEWARE INTEGRATION
# =============================================================================

def evaluate_before_send(
    evaluator: ResponseEvaluator,
    response: str,
    context: Dict,
    agent_type: str = "conversation",
    channel: str = "chat"
) -> Dict:
    """
    Middleware function to evaluate response before sending.

    Returns:
        {
            "response": str,  # Original or revised
            "evaluation": EvaluationResult,
            "was_revised": bool,
            "blocked": bool
        }
    """
    evaluation = evaluator.evaluate(
        agent_type=agent_type,
        response=response,
        context=context,
        channel=channel
    )

    # Determine final response
    if evaluation.passed:
        if evaluation.revised_response:
            return {
                "response": evaluation.revised_response,
                "evaluation": evaluation,
                "was_revised": True,
                "blocked": False
            }
        else:
            return {
                "response": response,
                "evaluation": evaluation,
                "was_revised": False,
                "blocked": False
            }
    else:
        # Failed and couldn't self-correct
        # Return human handoff message
        fallback = "I want to make sure I give you accurate information. Let me connect you with our team - Brian Dobson can help at brian@metroflexgym.com or 817-465-9331."

        return {
            "response": fallback,
            "evaluation": evaluation,
            "was_revised": False,
            "blocked": True
        }


# =============================================================================
# EVALUATION ANALYTICS
# =============================================================================

class EvaluationAnalytics:
    """Track evaluation metrics for continuous improvement"""

    def __init__(self):
        self.evaluations = []

    def record(self, evaluation: EvaluationResult, metadata: Dict = None):
        """Record an evaluation for analytics"""
        record = {
            "timestamp": datetime.now().isoformat(),
            "passed": evaluation.passed,
            "score": evaluation.overall_score,
            "rubric_scores": evaluation.rubric_scores,
            "failures": evaluation.failures,
            "was_revised": evaluation.revised_response is not None,
            "eval_time_ms": evaluation.evaluation_time_ms,
            "metadata": metadata or {}
        }
        self.evaluations.append(record)

    def get_pass_rate(self, hours: int = 24) -> float:
        """Get pass rate for recent evaluations"""
        cutoff = datetime.now().timestamp() - (hours * 3600)
        recent = [e for e in self.evaluations
                  if datetime.fromisoformat(e["timestamp"]).timestamp() > cutoff]

        if not recent:
            return 0.0

        passed = sum(1 for e in recent if e["passed"])
        return passed / len(recent)

    def get_common_failures(self, limit: int = 5) -> List[Tuple[str, int]]:
        """Get most common failure reasons"""
        failure_counts = {}
        for e in self.evaluations:
            for failure in e.get("failures", []):
                failure_counts[failure] = failure_counts.get(failure, 0) + 1

        sorted_failures = sorted(failure_counts.items(), key=lambda x: x[1], reverse=True)
        return sorted_failures[:limit]

    def get_avg_rubric_scores(self) -> Dict[str, float]:
        """Get average scores per rubric criterion"""
        rubric_totals = {}
        rubric_counts = {}

        for e in self.evaluations:
            for criterion, score in e.get("rubric_scores", {}).items():
                rubric_totals[criterion] = rubric_totals.get(criterion, 0) + score
                rubric_counts[criterion] = rubric_counts.get(criterion, 0) + 1

        return {
            criterion: rubric_totals[criterion] / rubric_counts[criterion]
            for criterion in rubric_totals
        }


# =============================================================================
# TESTING
# =============================================================================

if __name__ == "__main__":
    # Test the evaluator
    print("Testing Response Evaluator...")

    evaluator = ResponseEvaluator()

    # Test good response
    good_response = "The Better Bodies Texas Championship is on June 28, 2025 at Arlington Convention Center. Registration is open via MuscleWare - early entry is $150 with a $25 late fee after June 14. It's an NPC National Qualifier so you can earn your pro card. Ready to register? Head to muscleware.com/register"

    good_context = {
        "user_query": "When is the Better Bodies event and how do I register?",
        "knowledge_base_context": "Better Bodies Texas Championship: June 28, 2025 at Arlington Convention Center. Registration via MuscleWare. Early entry $150, late fee $25 after June 14. NPC National Qualifier.",
        "awareness_level": 3,
        "detected_objection": {"objection_type": "none"},
        "business_context": "events"
    }

    print("\n--- Testing Good Response ---")
    result = evaluator.evaluate("conversation", good_response, good_context)
    print(f"Passed: {result.passed}")
    print(f"Score: {result.overall_score:.2f}")
    print(f"Failures: {result.failures}")
    print(f"Eval time: {result.evaluation_time_ms:.0f}ms")

    # Test bad response (hallucinated pricing)
    bad_response = "Registration is $500 and the event is on July 4th at the Dallas Convention Center. We have 20 divisions including the new Ultra Heavyweight class."

    bad_context = {
        "user_query": "When is the Better Bodies event?",
        "knowledge_base_context": "Better Bodies Texas Championship: June 28, 2025 at Arlington Convention Center. Registration $150.",
        "awareness_level": 2,
        "detected_objection": {"objection_type": "none"},
        "business_context": "events"
    }

    print("\n--- Testing Bad Response (Hallucinations) ---")
    result = evaluator.evaluate("conversation", bad_response, bad_context)
    print(f"Passed: {result.passed}")
    print(f"Score: {result.overall_score:.2f}")
    print(f"Failures: {result.failures}")
    if result.revised_response:
        print(f"Revised: {result.revised_response}")
    print(f"Eval time: {result.evaluation_time_ms:.0f}ms")

    print("\n--- Evaluator Testing Complete ---")
