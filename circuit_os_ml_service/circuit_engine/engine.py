"""
CircuitScriptEngine - Main orchestration engine
Manages circuit registration, event handling, and execution
"""

from typing import Dict, List, Optional
import asyncio
import logging
from datetime import datetime
from .circuit import Circuit
from .context import CircuitContext
from .triggers import TriggerEvent

logger = logging.getLogger(__name__)


class CircuitScriptEngine:
    """
    Main engine that manages all circuits

    Features:
    - Register circuits
    - Subscribe to events
    - Execute circuits on triggers
    - Track metrics
    - Manage execution queue
    """

    def __init__(self):
        self.circuits: Dict[str, Circuit] = {}
        self.event_subscribers: Dict[str, List[Circuit]] = {}
        self.execution_queue = asyncio.Queue()
        self.running = False
        self.metrics = {
            "total_executions": 0,
            "successful_executions": 0,
            "failed_executions": 0,
            "total_duration": 0.0
        }

    def register(self, circuit: Circuit) -> None:
        """
        Register a circuit

        Args:
            circuit: Circuit to register
        """
        if circuit.name in self.circuits:
            logger.warning(f"Circuit {circuit.name} already registered, overwriting")

        self.circuits[circuit.name] = circuit

        # Subscribe to all trigger events
        for trigger in circuit.triggers:
            event_name = trigger.event.value

            if event_name not in self.event_subscribers:
                self.event_subscribers[event_name] = []

            if circuit not in self.event_subscribers[event_name]:
                self.event_subscribers[event_name].append(circuit)

        logger.info(f"Registered circuit: {circuit.name} ({len(circuit.triggers)} triggers, {len(circuit.actions)} actions)")

    def unregister(self, circuit_name: str) -> bool:
        """
        Unregister a circuit

        Args:
            circuit_name: Name of circuit to unregister

        Returns:
            True if circuit was found and removed
        """
        if circuit_name not in self.circuits:
            return False

        circuit = self.circuits[circuit_name]

        # Remove from event subscribers
        for trigger in circuit.triggers:
            event_name = trigger.event.value
            if event_name in self.event_subscribers:
                self.event_subscribers[event_name].remove(circuit)

        del self.circuits[circuit_name]
        logger.info(f"Unregistered circuit: {circuit_name}")
        return True

    def get(self, circuit_name: str) -> Optional[Circuit]:
        """Get circuit by name"""
        return self.circuits.get(circuit_name)

    def list(self) -> List[str]:
        """List all registered circuit names"""
        return list(self.circuits.keys())

    def list_circuits(self) -> List[Dict]:
        """
        List all circuits with metadata

        Returns:
            List of circuit dictionaries
        """
        return [circuit.to_dict() for circuit in self.circuits.values()]

    async def publish_event(self, event: TriggerEvent, data: Dict) -> List[str]:
        """
        Publish an event to trigger circuits

        Args:
            event: Event type
            data: Event data

        Returns:
            List of circuit names that were queued for execution
        """
        event_name = event.value
        triggered_circuits = []

        if event_name in self.event_subscribers:
            for circuit in self.event_subscribers[event_name]:
                # Queue for execution
                await self.execution_queue.put((circuit, data))
                triggered_circuits.append(circuit.name)
                logger.debug(f"Queued circuit: {circuit.name} for event: {event_name}")

        logger.info(f"Event {event_name} triggered {len(triggered_circuits)} circuits")
        return triggered_circuits

    async def execute_circuit(
        self,
        circuit_name: str,
        data: Dict,
        check_triggers: bool = True
    ) -> CircuitContext:
        """
        Execute a circuit by name

        Args:
            circuit_name: Name of circuit to execute
            data: Initial context data
            check_triggers: Whether to check trigger conditions (default True)

        Returns:
            Execution context

        Raises:
            ValueError: If circuit not found
        """
        circuit = self.circuits.get(circuit_name)
        if not circuit:
            raise ValueError(f"Circuit {circuit_name} not found")

        context = CircuitContext(data)
        start_time = datetime.now()

        # Check if circuit should execute
        if check_triggers and not circuit.should_execute(context):
            logger.info(f"Circuit {circuit_name} skipped (trigger conditions not met)")
            context.add_metadata("status", "skipped")
            context.add_metadata("reason", "trigger conditions not met")
            return context

        # Execute
        logger.info(f"Executing circuit: {circuit_name}")
        self.metrics["total_executions"] += 1

        try:
            result_context = await circuit.execute(context)

            # Update metrics
            status = result_context.get_metadata().get("status", "unknown")
            if status == "success":
                self.metrics["successful_executions"] += 1
            elif status in ["failed", "error"]:
                self.metrics["failed_executions"] += 1

            duration = (datetime.now() - start_time).total_seconds()
            self.metrics["total_duration"] += duration

            logger.info(f"Circuit {circuit_name} completed: {status} ({duration:.2f}s)")
            return result_context

        except Exception as e:
            self.metrics["failed_executions"] += 1
            logger.error(f"Circuit {circuit_name} error: {e}", exc_info=True)
            raise

    async def _process_queue(self):
        """
        Process execution queue (background task)
        """
        logger.info("Circuit execution queue started")

        while self.running:
            try:
                # Wait for circuit in queue
                circuit, data = await asyncio.wait_for(
                    self.execution_queue.get(),
                    timeout=1.0
                )

                # Execute circuit
                await self.execute_circuit(
                    circuit.name,
                    data,
                    check_triggers=True
                )

            except asyncio.TimeoutError:
                # No circuits in queue, continue
                continue

            except Exception as e:
                logger.error(f"Error processing queue: {e}", exc_info=True)

        logger.info("Circuit execution queue stopped")

    async def start(self):
        """
        Start the engine (begin processing queue)
        """
        if self.running:
            logger.warning("Engine already running")
            return

        self.running = True
        logger.info("CircuitScriptEngine started")

        # Start queue processor
        asyncio.create_task(self._process_queue())

    async def stop(self):
        """
        Stop the engine
        """
        self.running = False
        logger.info("CircuitScriptEngine stopped")

    def get_metrics(self) -> Dict:
        """
        Get engine metrics

        Returns:
            Dictionary of metrics
        """
        avg_duration = (
            self.metrics["total_duration"] / self.metrics["total_executions"]
            if self.metrics["total_executions"] > 0
            else 0.0
        )

        success_rate = (
            self.metrics["successful_executions"] / self.metrics["total_executions"]
            if self.metrics["total_executions"] > 0
            else 0.0
        )

        return {
            **self.metrics,
            "average_duration": avg_duration,
            "success_rate": success_rate,
            "registered_circuits": len(self.circuits),
            "total_triggers": sum(len(c.triggers) for c in self.circuits.values()),
            "total_actions": sum(len(c.actions) for c in self.circuits.values())
        }

    def reset_metrics(self):
        """Reset all metrics to zero"""
        self.metrics = {
            "total_executions": 0,
            "successful_executions": 0,
            "failed_executions": 0,
            "total_duration": 0.0
        }

    def __repr__(self):
        return f"CircuitScriptEngine(circuits={len(self.circuits)}, running={self.running})"
