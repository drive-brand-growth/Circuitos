"""
DMN (Decision Model and Notation) Engine for CircuitOS

This engine evaluates DMN decision tables defined in JSON format.
Supports FIRST, UNIQUE, ANY, and COLLECT hit policies.
"""

import json
import re
import os
from typing import Any, Dict, List, Optional
from dataclasses import dataclass
from pathlib import Path


@dataclass
class DecisionResult:
    """Result of a DMN decision evaluation"""
    decision_id: str
    rule_id: str
    rule_description: str
    outputs: Dict[str, Any]
    matched: bool
    all_matches: List[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "decision_id": self.decision_id,
            "rule_id": self.rule_id,
            "rule_description": self.rule_description,
            "outputs": self.outputs,
            "matched": self.matched,
            "all_matches": self.all_matches
        }


class DMNEngine:
    """
    DMN Decision Table Engine

    Evaluates business rules defined in DMN format.
    Supports Salesforce-style decision automation.
    """

    def __init__(self, decisions_path: str = None):
        self.decisions: Dict[str, Dict] = {}
        self.decisions_path = decisions_path or os.path.dirname(__file__)
        self._load_decisions()

    def _load_decisions(self):
        """Load all decision tables from the decisions directory"""
        path = Path(self.decisions_path)
        for file in path.glob("*.json"):
            try:
                with open(file, 'r') as f:
                    decision = json.load(f)
                    self.decisions[decision['id']] = decision
            except Exception as e:
                print(f"Warning: Could not load decision from {file}: {e}")

    def load_decision(self, decision_id: str, decision_data: Dict):
        """Manually load a decision table"""
        self.decisions[decision_id] = decision_data

    def evaluate(self, decision_id: str, inputs: Dict[str, Any]) -> DecisionResult:
        """
        Evaluate a decision table with given inputs

        Args:
            decision_id: ID of the decision table to evaluate
            inputs: Dictionary of input values

        Returns:
            DecisionResult with the matched rule and outputs
        """
        if decision_id not in self.decisions:
            raise ValueError(f"Decision table '{decision_id}' not found")

        decision = self.decisions[decision_id]
        hit_policy = decision.get('hitPolicy', 'FIRST')

        matches = []

        for rule in decision['rules']:
            if self._evaluate_rule(rule, inputs, decision['inputs']):
                matches.append({
                    'rule_id': rule['id'],
                    'description': rule.get('description', ''),
                    'outputs': rule['outputs']
                })

                # For FIRST hit policy, return immediately
                if hit_policy == 'FIRST':
                    return DecisionResult(
                        decision_id=decision_id,
                        rule_id=rule['id'],
                        rule_description=rule.get('description', ''),
                        outputs=rule['outputs'],
                        matched=True,
                        all_matches=matches
                    )

        # Handle different hit policies
        if hit_policy == 'COLLECT' and matches:
            # Return all matches
            return DecisionResult(
                decision_id=decision_id,
                rule_id='MULTIPLE',
                rule_description=f'{len(matches)} rules matched',
                outputs=self._collect_outputs(matches),
                matched=True,
                all_matches=matches
            )
        elif hit_policy == 'UNIQUE' and len(matches) > 1:
            raise ValueError(f"Multiple rules matched for UNIQUE hit policy: {[m['rule_id'] for m in matches]}")
        elif matches:
            return DecisionResult(
                decision_id=decision_id,
                rule_id=matches[0]['rule_id'],
                rule_description=matches[0]['description'],
                outputs=matches[0]['outputs'],
                matched=True,
                all_matches=matches
            )

        # No match
        return DecisionResult(
            decision_id=decision_id,
            rule_id=None,
            rule_description='No rules matched',
            outputs={},
            matched=False,
            all_matches=[]
        )

    def _evaluate_rule(self, rule: Dict, inputs: Dict[str, Any], input_defs: List[Dict]) -> bool:
        """Evaluate if a rule matches the given inputs"""
        conditions = rule.get('conditions', {})

        for input_def in input_defs:
            input_id = input_def['id']
            condition = conditions.get(input_id, 'any')
            input_value = inputs.get(input_id)

            if not self._evaluate_condition(condition, input_value, input_def['type']):
                return False

        return True

    def _evaluate_condition(self, condition: str, value: Any, value_type: str) -> bool:
        """
        Evaluate a single condition against a value

        Supports:
        - "any" - always matches
        - Comparison operators: >=, <=, >, <, ==, !=
        - Range: [min..max]
        - List: value1, value2, value3
        - Boolean: true, false
        """
        # Handle "any" condition
        if condition == "any":
            return True

        # Handle None values
        if value is None:
            return condition == "null" or condition == "any"

        # Handle boolean conditions
        if value_type == "boolean":
            if condition.lower() == "true":
                return value is True
            elif condition.lower() == "false":
                return value is False
            return True

        # Handle string equality for string types
        if value_type == "string":
            # Check if it's a list of allowed values
            if "," in condition:
                allowed = [v.strip().strip('"\'') for v in condition.split(",")]
                return str(value) in allowed
            return str(value) == condition.strip('"\'')

        # Handle numeric comparisons
        if value_type == "number":
            try:
                # Parse comparison operators
                if condition.startswith(">="):
                    return float(value) >= float(condition[2:].strip())
                elif condition.startswith("<="):
                    return float(value) <= float(condition[2:].strip())
                elif condition.startswith(">"):
                    return float(value) > float(condition[1:].strip())
                elif condition.startswith("<"):
                    return float(value) < float(condition[1:].strip())
                elif condition.startswith("=="):
                    return float(value) == float(condition[2:].strip())
                elif condition.startswith("!="):
                    return float(value) != float(condition[2:].strip())

                # Handle range [min..max]
                range_match = re.match(r'\[(\d+)\.\.(\d+)\]', condition)
                if range_match:
                    min_val, max_val = float(range_match.group(1)), float(range_match.group(2))
                    return min_val <= float(value) <= max_val

                # Direct equality
                return float(value) == float(condition)
            except ValueError:
                return False

        return False

    def _collect_outputs(self, matches: List[Dict]) -> Dict[str, List]:
        """Collect outputs from multiple matches into lists"""
        collected = {}
        for match in matches:
            for key, value in match['outputs'].items():
                if key not in collected:
                    collected[key] = []
                collected[key].append(value)
        return collected

    def list_decisions(self) -> List[str]:
        """List all available decision table IDs"""
        return list(self.decisions.keys())

    def get_decision_info(self, decision_id: str) -> Dict:
        """Get metadata about a decision table"""
        if decision_id not in self.decisions:
            raise ValueError(f"Decision table '{decision_id}' not found")

        decision = self.decisions[decision_id]
        return {
            "id": decision['id'],
            "name": decision['name'],
            "description": decision.get('description', ''),
            "inputs": [i['label'] for i in decision['inputs']],
            "outputs": [o['label'] for o in decision['outputs']],
            "rule_count": len(decision['rules'])
        }


# Convenience function for quick evaluation
def evaluate_decision(decision_id: str, inputs: Dict[str, Any], decisions_path: str = None) -> DecisionResult:
    """
    Quick evaluation of a decision table

    Args:
        decision_id: ID of the decision table
        inputs: Input values
        decisions_path: Optional path to decision files

    Returns:
        DecisionResult
    """
    engine = DMNEngine(decisions_path)
    return engine.evaluate(decision_id, inputs)


if __name__ == "__main__":
    # Demo usage
    engine = DMNEngine()

    print("=== DMN Engine Demo ===\n")
    print("Available decisions:", engine.list_decisions())

    # Test Lead Qualification
    print("\n--- Lead Qualification Test ---")
    test_lead = {
        "timeInBusiness": 4,
        "vehicleCount": 15,
        "annualRevenue": 750000,
        "hasExistingLicense": False
    }

    result = engine.evaluate("LeadQualification_v1", test_lead)
    print(f"Input: {test_lead}")
    print(f"Result: {result.outputs}")
    print(f"Rule: {result.rule_id} - {result.rule_description}")

    # Test Handoff Decision
    print("\n--- Handoff Decision Test ---")
    test_conversation = {
        "handoffScore": 65,
        "sentiment": "frustrated",
        "objectionCount": 2,
        "conversationLength": 8
    }

    result = engine.evaluate("HandoffDecision_v1", test_conversation)
    print(f"Input: {test_conversation}")
    print(f"Result: {result.outputs}")
    print(f"Rule: {result.rule_id} - {result.rule_description}")
