"""
Circuit Engine - Core module
Salesforce Apex-like execution with AI-native operations
"""

from .context import CircuitContext
from .triggers import Trigger, TriggerEvent, ScheduledTrigger, ConditionalTrigger
from .actions import (
    Action,
    ActionResult,
    # Data actions
    GetLeadDataAction,
    CreateOpportunityAction,
    UpdateLeadAction,
    # ML actions
    PredictLeadScoreAction,
    PredictChurnRiskAction,
    # RAG actions
    RetrieveCompanyIntelAction,
    RetrieveBestPracticesAction,
    # Knowledge Graph actions
    QueryCompetitorsAction,
    InferRelationshipsAction,
    # MCP actions
    ScrapeWebsiteAction,
    SearchNewsAction,
    # Control flow actions
    ConditionalAction,
    ParallelAction,
    LoopAction,
    # Notification actions
    SendSlackAlertAction,
    SendEmailAction,
)
from .circuit import Circuit
from .engine import CircuitScriptEngine

__all__ = [
    "CircuitContext",
    "Trigger",
    "TriggerEvent",
    "ScheduledTrigger",
    "ConditionalTrigger",
    "Action",
    "ActionResult",
    "GetLeadDataAction",
    "CreateOpportunityAction",
    "UpdateLeadAction",
    "PredictLeadScoreAction",
    "PredictChurnRiskAction",
    "RetrieveCompanyIntelAction",
    "RetrieveBestPracticesAction",
    "QueryCompetitorsAction",
    "InferRelationshipsAction",
    "ScrapeWebsiteAction",
    "SearchNewsAction",
    "ConditionalAction",
    "ParallelAction",
    "LoopAction",
    "SendSlackAlertAction",
    "SendEmailAction",
    "Circuit",
    "CircuitScriptEngine",
]
