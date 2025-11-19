"""
Circuit Script Runtime

Executes Circuit Script AST with integrated DMN, ML, and LLM services.
Implements Salesforce-style governor limits.
"""

import sys
import os
import time
from typing import Any, Dict, List, Optional, Callable
from dataclasses import dataclass, field

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from circuit_script.parser import parse_circuit_script, ASTNode
from dmn.engine import DMNEngine, DecisionResult


@dataclass
class GovernorLimits:
    """Salesforce-style governor limits"""
    max_cpu_time_ms: int = 30000  # 30 seconds
    max_heap_size_mb: int = 128
    max_dml_statements: int = 150
    max_queries: int = 100
    max_api_calls: int = 50
    max_email_invocations: int = 10

    # Current usage
    cpu_time_ms: int = 0
    heap_size_mb: int = 0
    dml_statements: int = 0
    queries: int = 0
    api_calls: int = 0
    email_invocations: int = 0

    def check_limit(self, limit_type: str):
        """Check if a limit has been exceeded"""
        limits = {
            'cpu_time': (self.cpu_time_ms, self.max_cpu_time_ms),
            'heap': (self.heap_size_mb, self.max_heap_size_mb),
            'dml': (self.dml_statements, self.max_dml_statements),
            'queries': (self.queries, self.max_queries),
            'api_calls': (self.api_calls, self.max_api_calls),
            'email': (self.email_invocations, self.max_email_invocations)
        }

        if limit_type in limits:
            current, max_val = limits[limit_type]
            if current >= max_val:
                raise RuntimeError(
                    f"Governor limit exceeded: {limit_type} "
                    f"({current}/{max_val})"
                )

    def increment(self, limit_type: str, amount: int = 1):
        """Increment a usage counter"""
        if limit_type == 'cpu_time':
            self.cpu_time_ms += amount
        elif limit_type == 'dml':
            self.dml_statements += amount
        elif limit_type == 'queries':
            self.queries += amount
        elif limit_type == 'api_calls':
            self.api_calls += amount
        elif limit_type == 'email':
            self.email_invocations += amount

        self.check_limit(limit_type)


@dataclass
class ExecutionContext:
    """Execution context for Circuit Script"""
    variables: Dict[str, Any] = field(default_factory=dict)
    functions: Dict[str, Callable] = field(default_factory=dict)
    governor: GovernorLimits = field(default_factory=GovernorLimits)
    logs: List[str] = field(default_factory=list)
    start_time: float = 0


class CircuitScriptRuntime:
    """
    Circuit Script Runtime Engine

    Executes Circuit Script with integrated AI services.
    """

    def __init__(self, dmn_path: str = None):
        self.dmn_engine = DMNEngine(dmn_path or os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'dmn'
        ))
        self.registered_classes: Dict[str, ASTNode] = {}
        self.registered_triggers: Dict[str, List[str]] = {}

    def register_script(self, source: str):
        """Parse and register a Circuit Script"""
        ast = parse_circuit_script(source)

        for child in ast.children:
            if child.node_type == "class":
                class_name = child.value
                self.registered_classes[class_name] = child

                # Register triggers
                decorator = child.metadata.get('decorator')
                if decorator and decorator.startswith('@Trigger'):
                    event = self._extract_trigger_event(decorator)
                    if event:
                        if event not in self.registered_triggers:
                            self.registered_triggers[event] = []
                        self.registered_triggers[event].append(class_name)

    def _extract_trigger_event(self, decorator: str) -> Optional[str]:
        """Extract event name from @Trigger decorator"""
        import re
        match = re.search(r"event\s*=\s*['\"]([^'\"]+)['\"]", decorator)
        if match:
            return match.group(1)
        return None

    def execute(self, class_name: str, method_name: str, args: Dict[str, Any]) -> Any:
        """
        Execute a method on a registered class

        Args:
            class_name: Name of the Circuit Script class
            method_name: Name of the method to execute
            args: Arguments to pass to the method

        Returns:
            Result of the method execution
        """
        if class_name not in self.registered_classes:
            raise ValueError(f"Class '{class_name}' not found")

        class_node = self.registered_classes[class_name]
        method_node = None

        for child in class_node.children:
            if child.node_type == "method" and child.value == method_name:
                method_node = child
                break

        if not method_node:
            raise ValueError(f"Method '{method_name}' not found in class '{class_name}'")

        # Create execution context
        context = ExecutionContext()
        context.start_time = time.time()

        # Initialize variables from parameters
        params = method_node.metadata.get('parameters', [])
        for param in params:
            param_name = param['name']
            if param_name in args:
                context.variables[param_name] = args[param_name]

        # Register built-in services
        self._register_services(context)

        # Execute method body
        result = self._execute_block(method_node.children, context)

        # Log execution summary
        elapsed_ms = (time.time() - context.start_time) * 1000
        context.governor.cpu_time_ms = int(elapsed_ms)

        return {
            "result": result,
            "logs": context.logs,
            "governor_usage": {
                "cpu_time_ms": context.governor.cpu_time_ms,
                "api_calls": context.governor.api_calls,
                "queries": context.governor.queries
            }
        }

    def fire_trigger(self, event: str, data: Dict[str, Any]) -> List[Dict]:
        """
        Fire triggers for an event

        Args:
            event: Event name (e.g., 'Lead.Created')
            data: Event data

        Returns:
            List of execution results
        """
        results = []

        if event in self.registered_triggers:
            for class_name in self.registered_triggers[event]:
                # Find the execute method
                result = self.execute(class_name, 'execute', data)
                results.append({
                    "class": class_name,
                    "result": result
                })

        return results

    def _register_services(self, context: ExecutionContext):
        """Register built-in service functions"""

        # DMN Service
        def dmn_evaluate(decision_id: str, inputs: Any) -> Dict:
            context.governor.increment('api_calls')
            context.logs.append(f"DMN.evaluate('{decision_id}')")

            # Convert inputs to dict if needed
            if hasattr(inputs, '__dict__'):
                inputs = inputs.__dict__
            elif not isinstance(inputs, dict):
                inputs = {"value": inputs}

            result = self.dmn_engine.evaluate(decision_id, inputs)
            return {
                "result": result.outputs.get("qualification", result.outputs),
                "score": result.outputs.get("score", 0),
                "nextAction": result.outputs.get("nextAction", ""),
                "rule_id": result.rule_id,
                "matched": result.matched
            }

        # ML Service (stub - would connect to real ML pipeline)
        def ml_predict(model_id: str, features: Any) -> float:
            context.governor.increment('api_calls')
            context.logs.append(f"ML.predict('{model_id}')")

            # Stub implementation - returns mock score
            # In production, this would call your ML service
            return 0.85  # Mock propensity score

        def ml_classify(model_id: str, text: str) -> Dict:
            context.governor.increment('api_calls')
            context.logs.append(f"ML.classify('{model_id}')")

            # Stub implementation
            return {
                "intent": "licensing_inquiry",
                "confidence": 0.92
            }

        # LLM Service (stub - would connect to OpenAI)
        def llm_generate(prompt_id: str, context_data: Any) -> str:
            context.governor.increment('api_calls')
            context.logs.append(f"LLM.generate('{prompt_id}')")

            # Stub implementation - returns mock response
            # In production, this would call GPT-4o-mini
            return f"Generated personalized message for {prompt_id}"

        def llm_chat(messages: List[Dict]) -> str:
            context.governor.increment('api_calls')
            context.logs.append(f"LLM.chat()")

            return "AI response based on conversation history"

        # Workflow Service
        def workflow_trigger(workflow_id: str, data: Any, message: str = None):
            context.governor.increment('api_calls')
            context.logs.append(f"Workflow.trigger('{workflow_id}')")

            return {
                "workflow_id": workflow_id,
                "status": "triggered",
                "message": message
            }

        # Database Service (CircuitDB)
        def db_query(soql: str) -> List[Dict]:
            context.governor.increment('queries')
            context.logs.append(f"DB.query()")

            # Stub - would query unified CircuitDB
            return []

        def db_insert(sobject: str, records: List[Dict]) -> List[str]:
            context.governor.increment('dml', len(records))
            context.logs.append(f"DB.insert('{sobject}', {len(records)} records)")

            return [f"mock_id_{i}" for i in range(len(records))]

        def db_update(sobject: str, records: List[Dict]) -> int:
            context.governor.increment('dml', len(records))
            context.logs.append(f"DB.update('{sobject}', {len(records)} records)")

            return len(records)

        # System utilities
        def system_log(message: str):
            context.logs.append(f"[LOG] {message}")

        def system_debug(value: Any):
            context.logs.append(f"[DEBUG] {value}")

        # Register all services
        context.functions = {
            "DMN.evaluate": dmn_evaluate,
            "ML.predict": ml_predict,
            "ML.classify": ml_classify,
            "LLM.generate": llm_generate,
            "LLM.chat": llm_chat,
            "Workflow.trigger": workflow_trigger,
            "DB.query": db_query,
            "DB.insert": db_insert,
            "DB.update": db_update,
            "System.log": system_log,
            "System.debug": system_debug
        }

    def _execute_block(self, statements: List[ASTNode], context: ExecutionContext) -> Any:
        """Execute a block of statements"""
        result = None

        for stmt in statements:
            result = self._execute_statement(stmt, context)

            # Check for return
            if isinstance(result, dict) and result.get("__return__"):
                return result["value"]

        return result

    def _execute_statement(self, node: ASTNode, context: ExecutionContext) -> Any:
        """Execute a single statement"""
        if node.node_type == "assignment":
            return self._execute_assignment(node, context)
        elif node.node_type == "method_call":
            return self._execute_method_call(node, context)
        elif node.node_type == "function_call":
            return self._execute_function_call(node, context)
        elif node.node_type == "if":
            return self._execute_if(node, context)
        elif node.node_type == "return":
            value = self._evaluate(node.children[0], context) if node.children else None
            return {"__return__": True, "value": value}
        elif node.node_type == "identifier":
            # Variable declaration
            var_name = node.value
            if var_name not in context.variables:
                context.variables[var_name] = None
            return context.variables[var_name]

        return None

    def _execute_assignment(self, node: ASTNode, context: ExecutionContext) -> Any:
        """Execute an assignment statement"""
        left = node.children[0]
        right = node.children[1]

        # Get variable name
        if left.node_type == "identifier":
            var_name = left.value
        else:
            var_name = self._get_var_name(left)

        # Evaluate right side
        value = self._evaluate(right, context)
        context.variables[var_name] = value

        return value

    def _execute_method_call(self, node: ASTNode, context: ExecutionContext) -> Any:
        """Execute a method call (e.g., DMN.evaluate)"""
        method_name = node.value
        target = node.children[0] if node.children else None
        args = [self._evaluate(arg, context) for arg in node.children[1:]]

        # Build full method name
        if target and target.node_type == "identifier":
            full_name = f"{target.value}.{method_name}"
        else:
            full_name = method_name

        # Call registered function
        if full_name in context.functions:
            return context.functions[full_name](*args)

        # Check if it's a property access on a variable
        if target and target.node_type == "identifier":
            var = context.variables.get(target.value)
            if var and isinstance(var, dict) and method_name in var:
                return var[method_name]

        return None

    def _execute_function_call(self, node: ASTNode, context: ExecutionContext) -> Any:
        """Execute a function call"""
        func_name = node.value
        args = [self._evaluate(arg, context) for arg in node.children]

        if func_name in context.functions:
            return context.functions[func_name](*args)

        return None

    def _execute_if(self, node: ASTNode, context: ExecutionContext) -> Any:
        """Execute an if statement"""
        condition = self._evaluate(node.children[0], context)

        if condition:
            return self._execute_block(node.children[1:], context)
        elif node.metadata.get("else"):
            return self._execute_block(node.metadata["else"], context)

        return None

    def _evaluate(self, node: ASTNode, context: ExecutionContext) -> Any:
        """Evaluate an expression"""
        if node.node_type == "string":
            return node.value
        elif node.node_type == "number":
            return node.value
        elif node.node_type == "boolean":
            return node.value
        elif node.node_type == "identifier":
            return context.variables.get(node.value)
        elif node.node_type == "object":
            obj = {}
            for prop in node.children:
                key = prop.value
                value = self._evaluate(prop.children[0], context)
                obj[key] = value
            return obj
        elif node.node_type == "method_call":
            return self._execute_method_call(node, context)
        elif node.node_type == "function_call":
            return self._execute_function_call(node, context)
        elif node.node_type == "property_access":
            target = self._evaluate(node.children[0], context)
            prop = node.value
            if isinstance(target, dict):
                return target.get(prop)
            return None

        return None

    def _get_var_name(self, node: ASTNode) -> str:
        """Extract variable name from AST node"""
        if node.node_type == "identifier":
            return node.value
        return "unknown"


# Convenience function
def run_circuit_script(source: str, entry_class: str, entry_method: str, args: Dict) -> Dict:
    """
    Run a Circuit Script

    Args:
        source: Circuit Script source code
        entry_class: Class name to execute
        entry_method: Method name to execute
        args: Arguments to pass

    Returns:
        Execution result
    """
    runtime = CircuitScriptRuntime()
    runtime.register_script(source)
    return runtime.execute(entry_class, entry_method, args)


if __name__ == "__main__":
    # Demo
    print("=== Circuit Script Runtime Demo ===\n")

    # Sample Circuit Script
    script = '''
    @Trigger(event='Lead.Created')
    public class LeadQualificationCircuit {
        public void execute(Lead lead) {
            // Evaluate DMN decision
            DecisionResult eligibility = DMN.evaluate('LeadQualification_v1', lead);

            // Log the decision
            System.debug(eligibility);
        }
    }
    '''

    runtime = CircuitScriptRuntime()
    runtime.register_script(script)

    # Test data
    test_lead = {
        "timeInBusiness": 4,
        "vehicleCount": 15,
        "annualRevenue": 750000,
        "hasExistingLicense": False,
        "name": "ABC Transport Co"
    }

    print("Input Lead:", test_lead)
    print("\n--- Executing Circuit Script ---\n")

    result = runtime.execute(
        "LeadQualificationCircuit",
        "execute",
        {"lead": test_lead}
    )

    print("Execution Logs:")
    for log in result["logs"]:
        print(f"  {log}")

    print(f"\nGovernor Usage:")
    for key, value in result["governor_usage"].items():
        print(f"  {key}: {value}")
