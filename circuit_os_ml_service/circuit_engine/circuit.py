"""
Circuit - Workflow definition and execution
Combines triggers and actions into executable workflows
"""

from typing import List, Dict, Callable, Optional
from datetime import datetime
import logging
from .context import CircuitContext
from .triggers import Trigger
from .actions import Action, ActionResult

logger = logging.getLogger(__name__)


class Circuit:
    """
    Circuit = Trigger + Action Sequence

    Like Salesforce Flow or Process Builder, but with AI-native operations.
    Executes deterministically with full observability and error handling.
    """

    def __init__(self, name: str, description: str = ""):
        """
        Initialize circuit

        Args:
            name: Unique circuit name
            description: Human-readable description
        """
        self.name = name
        self.description = description
        self.triggers: List[Trigger] = []
        self.actions: List[Action] = []
        self.error_handlers: Dict[str, Callable] = {}
        self.enabled = True
        self.metadata = {
            "created_at": datetime.now().isoformat(),
            "version": "1.0"
        }

    def add_trigger(self, trigger: Trigger) -> 'Circuit':
        """
        Add trigger to circuit

        Args:
            trigger: Trigger instance

        Returns:
            self (for method chaining)
        """
        self.triggers.append(trigger)
        return self

    def add_action(self, action: Action) -> 'Circuit':
        """
        Add action to sequence

        Args:
            action: Action instance

        Returns:
            self (for method chaining)
        """
        self.actions.append(action)
        return self

    def add_error_handler(
        self,
        action_name: str,
        handler: Callable[[Exception, CircuitContext], None]
    ) -> 'Circuit':
        """
        Add custom error handler for specific action

        Args:
            action_name: Name of action to handle
            handler: Error handler function

        Returns:
            self (for method chaining)
        """
        self.error_handlers[action_name] = handler
        return self

    def enable(self) -> 'Circuit':
        """Enable circuit execution"""
        self.enabled = True
        return self

    def disable(self) -> 'Circuit':
        """Disable circuit execution"""
        self.enabled = False
        return self

    def should_execute(self, context: CircuitContext) -> bool:
        """
        Check if circuit should execute

        Args:
            context: Execution context

        Returns:
            True if any trigger conditions are met and circuit is enabled
        """
        if not self.enabled:
            return False

        # Check all triggers
        return any(trigger.should_fire(context) for trigger in self.triggers)

    async def execute(self, context: CircuitContext) -> CircuitContext:
        """
        Execute circuit

        Runs all actions in sequence with:
        - Error handling
        - Retry logic (handled by Action.execute_with_retry)
        - Metrics tracking
        - Full audit trail

        Args:
            context: Execution context

        Returns:
            Updated context after execution
        """
        logger.info(f"Executing circuit: {self.name}")

        # Add circuit metadata
        context.add_metadata("circuit_name", self.name)
        context.add_metadata("circuit_started_at", datetime.now().isoformat())

        execution_summary = {
            "total_actions": len(self.actions),
            "successful_actions": 0,
            "failed_actions": 0
        }

        try:
            for i, action in enumerate(self.actions, start=1):
                logger.debug(f"[{self.name}] Executing action {i}/{len(self.actions)}: {action.name}")

                # Execute action with retry
                result = await action.execute_with_retry(context)

                # Record in context
                context.record_action(
                    action_name=action.name,
                    duration=result.duration,
                    success=result.success
                )

                # Handle failure
                if not result.success:
                    execution_summary["failed_actions"] += 1
                    logger.error(f"[{self.name}] Action {action.name} failed: {result.error}")

                    # Custom error handler
                    if action.name in self.error_handlers:
                        try:
                            self.error_handlers[action.name](
                                Exception(result.error),
                                context
                            )
                        except Exception as handler_error:
                            logger.error(f"Error handler failed: {handler_error}")

                    # Stop execution on failure
                    context.add_metadata("status", "failed")
                    context.add_metadata("failed_action", action.name)
                    context.add_metadata("failure_reason", result.error)
                    break
                else:
                    execution_summary["successful_actions"] += 1

            else:
                # All actions succeeded
                context.add_metadata("status", "success")
                logger.info(f"[{self.name}] Circuit completed successfully")

            context.add_metadata("circuit_finished_at", datetime.now().isoformat())
            context.add_metadata("execution_summary", execution_summary)

        except Exception as e:
            logger.error(f"[{self.name}] Circuit execution error: {e}", exc_info=True)
            context.record_error("circuit", str(e))
            context.add_metadata("status", "error")
            context.add_metadata("error", str(e))
            raise

        return context

    def to_dict(self) -> Dict:
        """
        Serialize circuit to dictionary

        Returns:
            Dictionary representation
        """
        return {
            "name": self.name,
            "description": self.description,
            "enabled": self.enabled,
            "trigger_count": len(self.triggers),
            "action_count": len(self.actions),
            "triggers": [
                {
                    "event": trigger.event.value,
                    "priority": trigger.priority
                }
                for trigger in self.triggers
            ],
            "actions": [
                {
                    "name": action.name,
                    "type": action.__class__.__name__
                }
                for action in self.actions
            ],
            "metadata": self.metadata
        }

    def __repr__(self):
        status = "enabled" if self.enabled else "disabled"
        return f"Circuit(name={self.name}, triggers={len(self.triggers)}, actions={len(self.actions)}, {status})"


class CircuitBuilder:
    """
    Fluent builder for creating circuits

    Example:
        circuit = CircuitBuilder("lead_processing") \
            .description("Process new leads with AI") \
            .on_event(TriggerEvent.LEAD_CREATED) \
            .add_actions([
                GetLeadDataAction(),
                PredictLeadScoreAction(),
                CreateOpportunityAction()
            ]) \
            .build()
    """

    def __init__(self, name: str):
        self.circuit = Circuit(name)

    def description(self, desc: str) -> 'CircuitBuilder':
        """Set circuit description"""
        self.circuit.description = desc
        return self

    def on_event(self, trigger: Trigger) -> 'CircuitBuilder':
        """Add trigger"""
        self.circuit.add_trigger(trigger)
        return self

    def add_actions(self, actions: List[Action]) -> 'CircuitBuilder':
        """Add multiple actions"""
        for action in actions:
            self.circuit.add_action(action)
        return self

    def with_error_handler(
        self,
        action_name: str,
        handler: Callable
    ) -> 'CircuitBuilder':
        """Add error handler"""
        self.circuit.add_error_handler(action_name, handler)
        return self

    def build(self) -> Circuit:
        """Build and return circuit"""
        return self.circuit
