#!/usr/bin/env python3
"""
Circuit OS Orchestrator Core
Multi-agent command and control with governance.

Implements "Strategic Center, Tactical Edges" pattern:
- Centralized: Task routing, policy enforcement, state management
- Decentralized: Worker agents execute independently within guardrails
"""

import logging
import uuid
from typing import Dict, Any, List, Optional, Callable
from datetime import datetime
from enum import Enum
import json

logger = logging.getLogger(__name__)


class TaskStatus(Enum):
    """Task execution states"""
    PENDING = "pending"
    ROUTING = "routing"
    POLICY_CHECK = "policy_check"
    AWAITING_APPROVAL = "awaiting_approval"
    EXECUTING = "executing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class AgentCapability(Enum):
    """Worker agent capabilities"""
    KNOWLEDGE_RETRIEVAL = "knowledge_retrieval"  # RAG
    ACTION_EXECUTION = "action_execution"        # GHL writes, API calls
    DATA_PROCESSING = "data_processing"          # Transform, enrich
    COMMUNICATION = "communication"              # Email, Slack, etc.


class WorkerAgent:
    """
    Base class for worker agents in the Circuit OS mesh.

    All worker agents must implement:
    - capabilities: What this agent can do
    - execute(): How it performs tasks
    - health_check(): Is it ready to work
    """

    def __init__(self, agent_id: str, name: str, capabilities: List[AgentCapability]):
        self.agent_id = agent_id
        self.name = name
        self.capabilities = capabilities
        self.status = "idle"

    def can_handle(self, task_type: str) -> bool:
        """Check if this agent can handle a task type"""
        raise NotImplementedError("Worker agents must implement can_handle()")

    def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a task and return results"""
        raise NotImplementedError("Worker agents must implement execute()")

    def health_check(self) -> bool:
        """Check if agent is healthy and ready"""
        return True


class AgentRegistry:
    """
    Maintains inventory of available worker agents.

    Supports:
    - Agent registration/deregistration
    - Capability-based routing
    - Health monitoring
    """

    def __init__(self):
        self.agents: Dict[str, WorkerAgent] = {}

    def register(self, agent: WorkerAgent):
        """Add agent to registry"""
        self.agents[agent.agent_id] = agent
        logger.info(f"✅ Registered agent: {agent.name} ({agent.agent_id})")
        logger.info(f"   Capabilities: {[c.value for c in agent.capabilities]}")

    def deregister(self, agent_id: str):
        """Remove agent from registry"""
        if agent_id in self.agents:
            agent_name = self.agents[agent_id].name
            del self.agents[agent_id]
            logger.info(f"🗑️  Deregistered agent: {agent_name} ({agent_id})")

    def find_agent(self, task_type: str) -> Optional[WorkerAgent]:
        """Find agent that can handle a task type"""
        for agent in self.agents.values():
            if agent.can_handle(task_type):
                return agent
        return None

    def get_all_agents(self) -> List[Dict[str, Any]]:
        """Get status of all registered agents"""
        return [
            {
                "agent_id": agent.agent_id,
                "name": agent.name,
                "capabilities": [c.value for c in agent.capabilities],
                "status": agent.status,
                "healthy": agent.health_check()
            }
            for agent in self.agents.values()
        ]


class PolicyEngine:
    """
    Enforces governance rules across orchestrated workflows.

    Rules can:
    - Block actions (compliance violation)
    - Require approval (high-risk operations)
    - Transform tasks (add metadata, route differently)
    - Audit decisions (log all evaluations)
    """

    def __init__(self):
        self.rules: List[Callable] = []
        self.audit_log: List[Dict[str, Any]] = []

    def add_rule(self, rule: Callable):
        """Add policy rule (function that evaluates tasks)"""
        self.rules.append(rule)

    def evaluate(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate task against all rules.

        Returns:
        {
            "approved": True/False,
            "requires_approval": True/False,
            "blocked": True/False,
            "reason": "...",
            "modified_task": {...}  # If rule transformed the task
        }
        """
        decision = {
            "approved": True,
            "requires_approval": False,
            "blocked": False,
            "reason": "No restrictions",
            "modified_task": task
        }

        for rule in self.rules:
            try:
                rule_result = rule(task)

                # Rules can block, require approval, or transform
                if rule_result.get("blocked"):
                    decision["approved"] = False
                    decision["blocked"] = True
                    decision["reason"] = rule_result.get("reason", "Policy violation")
                    break

                if rule_result.get("requires_approval"):
                    decision["requires_approval"] = True
                    decision["reason"] = rule_result.get("reason", "Approval required")

                if "modified_task" in rule_result:
                    decision["modified_task"] = rule_result["modified_task"]

            except Exception as e:
                logger.error(f"Policy rule evaluation error: {e}")
                # Fail-safe: Block on rule error
                decision["approved"] = False
                decision["blocked"] = True
                decision["reason"] = f"Policy evaluation failed: {e}"
                break

        # Audit all decisions
        self.audit_log.append({
            "timestamp": datetime.utcnow().isoformat(),
            "task_id": task.get("task_id"),
            "task_type": task.get("task_type"),
            "decision": decision,
            "rules_evaluated": len(self.rules)
        })

        return decision


class TaskOrchestrator:
    """
    Central command plane for multi-agent workflows.

    Responsibilities:
    - Route tasks to appropriate worker agents
    - Enforce policies before execution
    - Maintain task state and history
    - Coordinate multi-step workflows
    - Provide observability (telemetry, explainability)
    """

    def __init__(self, agent_registry: AgentRegistry, policy_engine: PolicyEngine):
        self.registry = agent_registry
        self.policy = policy_engine
        self.tasks: Dict[str, Dict[str, Any]] = {}
        self.workflow_history: List[Dict[str, Any]] = []

    def submit_task(self, task_type: str, task_data: Dict[str, Any],
                    requester: str = None, metadata: Dict = None) -> str:
        """
        Submit a task for orchestrated execution.

        Args:
            task_type: Type of task (e.g., "knowledge_retrieval", "ghl_lead_create")
            task_data: Task-specific parameters
            requester: Who/what submitted this task (for audit trail)
            metadata: Additional context (session_id, user_id, etc.)

        Returns:
            task_id: Unique identifier for tracking
        """
        task_id = str(uuid.uuid4())

        task = {
            "task_id": task_id,
            "task_type": task_type,
            "task_data": task_data,
            "requester": requester,
            "metadata": metadata or {},
            "status": TaskStatus.PENDING.value,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
            "history": []
        }

        self.tasks[task_id] = task
        self._log_state_change(task_id, TaskStatus.PENDING, "Task submitted")

        logger.info(f"📥 Task submitted: {task_id} (type: {task_type})")

        return task_id

    def execute_task(self, task_id: str, approval_token: str = None) -> Dict[str, Any]:
        """
        Execute a task through the full orchestration pipeline.

        Pipeline:
        1. Route to worker agent
        2. Policy evaluation
        3. Approval gate (if required)
        4. Execute
        5. Log telemetry

        Returns:
            Result dictionary with execution details
        """
        if task_id not in self.tasks:
            return {"success": False, "error": "Task not found"}

        task = self.tasks[task_id]

        try:
            # === STEP 1: Route to agent ===
            self._log_state_change(task_id, TaskStatus.ROUTING, "Finding capable agent")

            agent = self.registry.find_agent(task["task_type"])
            if not agent:
                self._log_state_change(task_id, TaskStatus.FAILED, "No capable agent found")
                return {
                    "success": False,
                    "error": f"No agent can handle task type: {task['task_type']}"
                }

            logger.info(f"🎯 Routed to agent: {agent.name}")
            task["assigned_agent"] = agent.agent_id

            # === STEP 2: Policy evaluation ===
            self._log_state_change(task_id, TaskStatus.POLICY_CHECK, "Evaluating policies")

            policy_decision = self.policy.evaluate(task)
            task["policy_decision"] = policy_decision

            if policy_decision["blocked"]:
                self._log_state_change(task_id, TaskStatus.FAILED,
                                     f"Blocked by policy: {policy_decision['reason']}")
                return {
                    "success": False,
                    "error": "Policy violation",
                    "reason": policy_decision["reason"]
                }

            # Use modified task if policy transformed it
            execution_task = policy_decision.get("modified_task", task)

            # === STEP 3: Approval gate (if required) ===
            if policy_decision["requires_approval"]:
                if not approval_token:
                    self._log_state_change(task_id, TaskStatus.AWAITING_APPROVAL,
                                         f"Approval required: {policy_decision['reason']}")
                    return {
                        "success": False,
                        "requires_approval": True,
                        "reason": policy_decision["reason"],
                        "approval_instructions": "Provide approval_token to proceed",
                        "task_id": task_id
                    }

                # Validate approval token (in production, check signatures, permissions, etc.)
                logger.info(f"✅ Approval received: {approval_token[:8]}...")
                task["approval_token"] = approval_token
                task["approved_at"] = datetime.utcnow().isoformat()

            # === STEP 4: Execute via worker agent ===
            self._log_state_change(task_id, TaskStatus.EXECUTING, f"Executing via {agent.name}")

            result = agent.execute(execution_task)

            # === STEP 5: Complete and log telemetry ===
            self._log_state_change(task_id, TaskStatus.COMPLETED, "Execution successful")
            task["result"] = result
            task["completed_at"] = datetime.utcnow().isoformat()

            # Add to workflow history for observability
            self.workflow_history.append({
                "task_id": task_id,
                "task_type": task["task_type"],
                "agent": agent.name,
                "policy_decision": policy_decision,
                "required_approval": policy_decision["requires_approval"],
                "timestamp": datetime.utcnow().isoformat(),
                "success": result.get("success", True)
            })

            logger.info(f"✅ Task completed: {task_id}")

            return {
                "success": True,
                "task_id": task_id,
                "result": result,
                "agent": agent.name,
                "required_approval": policy_decision["requires_approval"]
            }

        except Exception as e:
            self._log_state_change(task_id, TaskStatus.FAILED, f"Execution error: {e}")
            logger.error(f"❌ Task failed: {task_id} - {e}")
            return {
                "success": False,
                "error": str(e),
                "task_id": task_id
            }

    def get_task_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get current status and history of a task"""
        if task_id not in self.tasks:
            return None

        task = self.tasks[task_id]
        return {
            "task_id": task_id,
            "task_type": task["task_type"],
            "status": task["status"],
            "created_at": task["created_at"],
            "updated_at": task["updated_at"],
            "assigned_agent": task.get("assigned_agent"),
            "requires_approval": task.get("policy_decision", {}).get("requires_approval", False),
            "history": task["history"],
            "result": task.get("result")
        }

    def _log_state_change(self, task_id: str, new_status: TaskStatus, message: str):
        """Internal: Log task state transitions"""
        if task_id in self.tasks:
            task = self.tasks[task_id]
            task["status"] = new_status.value
            task["updated_at"] = datetime.utcnow().isoformat()
            task["history"].append({
                "timestamp": datetime.utcnow().isoformat(),
                "status": new_status.value,
                "message": message
            })

    def get_workflow_telemetry(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent workflow execution history for observability"""
        return self.workflow_history[-limit:]

    def get_governance_metrics(self) -> Dict[str, Any]:
        """Get metrics proving governance effectiveness"""
        total_tasks = len(self.tasks)
        if total_tasks == 0:
            return {"message": "No tasks executed yet"}

        completed = sum(1 for t in self.tasks.values() if t["status"] == TaskStatus.COMPLETED.value)
        failed = sum(1 for t in self.tasks.values() if t["status"] == TaskStatus.FAILED.value)
        blocked = sum(1 for t in self.tasks.values()
                     if t.get("policy_decision", {}).get("blocked", False))
        required_approval = sum(1 for t in self.tasks.values()
                               if t.get("policy_decision", {}).get("requires_approval", False))

        return {
            "total_tasks": total_tasks,
            "completed": completed,
            "failed": failed,
            "success_rate_pct": round(completed / total_tasks * 100, 2) if total_tasks > 0 else 0,
            "governance": {
                "policy_blocks": blocked,
                "approval_gates_triggered": required_approval,
                "compliance_rate_pct": 100.0  # If any task executed, it passed policy
            },
            "policy_audit_entries": len(self.policy.audit_log)
        }


# =============================================================================
# PRE-BUILT POLICY RULES
# =============================================================================

def require_approval_for_writes(task: Dict[str, Any]) -> Dict[str, Any]:
    """
    Policy: All write operations require human approval.

    Applies to: GHL lead creation, database writes, external API calls
    """
    write_task_types = [
        "ghl_lead_create",
        "ghl_contact_update",
        "database_write",
        "api_call"
    ]

    if task.get("task_type") in write_task_types:
        return {
            "requires_approval": True,
            "reason": f"Write operation '{task.get('task_type')}' requires approval"
        }

    return {"approved": True}


def block_pii_in_logs(task: Dict[str, Any]) -> Dict[str, Any]:
    """
    Policy: Prevent PII from being logged in task metadata.

    Transforms task by redacting sensitive fields.
    """
    sensitive_fields = ["ssn", "credit_card", "password", "api_key"]

    modified_task = task.copy()
    task_data = modified_task.get("task_data", {})

    redacted = False
    for field in sensitive_fields:
        if field in task_data:
            task_data[field] = "[REDACTED]"
            redacted = True

    if redacted:
        modified_task["task_data"] = task_data
        return {
            "approved": True,
            "modified_task": modified_task,
            "reason": "PII redacted from task data"
        }

    return {"approved": True}
