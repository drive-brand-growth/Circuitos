"""
Trigger System - Event-driven execution triggers
Salesforce Apex-style triggers with AI-native events
"""

from enum import Enum
from typing import Callable, Dict, Any, Optional
from abc import ABC, abstractmethod
from .context import CircuitContext


class TriggerEvent(Enum):
    """
    Predefined trigger events
    Extensible for custom business events
    """
    # Lead events (Salesforce-style)
    LEAD_CREATED = "lead.created"
    LEAD_UPDATED = "lead.updated"
    LEAD_CONVERTED = "lead.converted"
    LEAD_DELETED = "lead.deleted"

    # Opportunity events
    OPPORTUNITY_CREATED = "opportunity.created"
    OPPORTUNITY_UPDATED = "opportunity.updated"
    OPPORTUNITY_STAGE_CHANGED = "opportunity.stage_changed"
    OPPORTUNITY_CLOSED_WON = "opportunity.closed_won"
    OPPORTUNITY_CLOSED_LOST = "opportunity.closed_lost"

    # Account events
    ACCOUNT_CREATED = "account.created"
    ACCOUNT_UPDATED = "account.updated"
    ACCOUNT_DELETED = "account.deleted"

    # Contact events
    CONTACT_CREATED = "contact.created"
    CONTACT_UPDATED = "contact.updated"

    # AI-native events (Apex doesn't have these!)
    HOT_LEAD_DETECTED = "lead.hot"
    COLD_LEAD_DETECTED = "lead.cold"
    COMPETITOR_MENTIONED = "competitor.mentioned"
    MODEL_RETRAIN_TRIGGERED = "model.retrain"
    DEAL_AT_RISK = "deal.at_risk"
    SENTIMENT_NEGATIVE = "sentiment.negative"
    SENTIMENT_POSITIVE = "sentiment.positive"
    CHURN_RISK_HIGH = "churn.risk.high"
    ANOMALY_DETECTED = "anomaly.detected"

    # Scheduled events
    DAILY_SYNC = "schedule.daily"
    WEEKLY_REPORT = "schedule.weekly"
    MONTHLY_REPORT = "schedule.monthly"
    NIGHTLY_TRAINING = "schedule.nightly_training"
    HOURLY_REFRESH = "schedule.hourly_refresh"

    # Data events
    DATA_INGESTED = "data.ingested"
    DATA_STALE = "data.stale"
    DATA_QUALITY_ISSUE = "data.quality_issue"

    # System events
    SYSTEM_ERROR = "system.error"
    SYSTEM_OVERLOAD = "system.overload"


class Trigger(ABC):
    """
    Base trigger class
    All triggers must extend this
    """

    def __init__(
        self,
        event: TriggerEvent,
        conditions: Optional[Dict[str, Any]] = None,
        priority: int = 5
    ):
        """
        Initialize trigger

        Args:
            event: Trigger event type
            conditions: Optional conditions for firing (dict of key-value pairs)
            priority: Execution priority (1-10, higher = more urgent)
        """
        self.event = event
        self.conditions = conditions or {}
        self.priority = priority

    @abstractmethod
    def should_fire(self, context: CircuitContext) -> bool:
        """
        Determine if trigger should fire

        Args:
            context: Circuit execution context

        Returns:
            True if trigger conditions are met
        """
        pass

    def __repr__(self):
        return f"Trigger(event={self.event.value}, priority={self.priority})"


class SimpleTrigger(Trigger):
    """
    Simple trigger with basic condition matching
    """

    def __init__(
        self,
        event: TriggerEvent,
        conditions: Optional[Dict[str, Any]] = None,
        priority: int = 5
    ):
        super().__init__(event, conditions, priority)

    def should_fire(self, context: CircuitContext) -> bool:
        """
        Evaluate if trigger should fire based on conditions
        """
        if not self.conditions:
            return True  # No conditions = always fire

        # Evaluate each condition
        for key, expected_value in self.conditions.items():
            actual_value = context.get(key)

            # Support callable conditions
            if callable(expected_value):
                if not expected_value(actual_value):
                    return False
            # Support direct comparison
            elif actual_value != expected_value:
                return False

        return True


class ConditionalTrigger(Trigger):
    """
    Trigger with advanced conditional logic via lambda/function
    """

    def __init__(
        self,
        event: TriggerEvent,
        condition_fn: Callable[[CircuitContext], bool],
        priority: int = 5
    ):
        """
        Initialize conditional trigger

        Args:
            event: Trigger event type
            condition_fn: Function that takes context and returns bool
            priority: Execution priority
        """
        super().__init__(event, {}, priority)
        self.condition_fn = condition_fn

    def should_fire(self, context: CircuitContext) -> bool:
        """Evaluate custom condition function"""
        try:
            return self.condition_fn(context)
        except Exception as e:
            # If condition evaluation fails, don't fire
            print(f"Error evaluating condition: {e}")
            return False


class ScheduledTrigger(Trigger):
    """
    Cron-like scheduled trigger
    Uses APScheduler for scheduling
    """

    def __init__(
        self,
        cron_expression: str,
        event: TriggerEvent,
        priority: int = 5
    ):
        """
        Initialize scheduled trigger

        Args:
            cron_expression: Cron expression (e.g., "0 2 * * *" for 2am daily)
            event: Trigger event type
            priority: Execution priority
        """
        super().__init__(event, {}, priority)
        self.cron_expression = cron_expression

    def should_fire(self, context: CircuitContext) -> bool:
        """
        Scheduled triggers are managed by scheduler
        This method always returns True when called by scheduler
        """
        return True

    def __repr__(self):
        return f"ScheduledTrigger(cron={self.cron_expression}, event={self.event.value})"


class ThresholdTrigger(Trigger):
    """
    Trigger when a numeric value crosses a threshold
    """

    def __init__(
        self,
        event: TriggerEvent,
        variable_name: str,
        threshold: float,
        operator: str = "gt",  # gt, gte, lt, lte, eq
        priority: int = 5
    ):
        """
        Initialize threshold trigger

        Args:
            event: Trigger event type
            variable_name: Context variable to check
            threshold: Threshold value
            operator: Comparison operator (gt, gte, lt, lte, eq)
            priority: Execution priority
        """
        super().__init__(event, {}, priority)
        self.variable_name = variable_name
        self.threshold = threshold
        self.operator = operator

    def should_fire(self, context: CircuitContext) -> bool:
        """Evaluate threshold condition"""
        value = context.get(self.variable_name)

        if value is None:
            return False

        try:
            value = float(value)
        except (ValueError, TypeError):
            return False

        if self.operator == "gt":
            return value > self.threshold
        elif self.operator == "gte":
            return value >= self.threshold
        elif self.operator == "lt":
            return value < self.threshold
        elif self.operator == "lte":
            return value <= self.threshold
        elif self.operator == "eq":
            return value == self.threshold
        else:
            return False


class CompositeTrigger(Trigger):
    """
    Composite trigger with AND/OR logic
    Combine multiple triggers
    """

    def __init__(
        self,
        event: TriggerEvent,
        triggers: list[Trigger],
        logic: str = "AND",  # AND or OR
        priority: int = 5
    ):
        """
        Initialize composite trigger

        Args:
            event: Trigger event type
            triggers: List of child triggers
            logic: "AND" (all must fire) or "OR" (any can fire)
            priority: Execution priority
        """
        super().__init__(event, {}, priority)
        self.triggers = triggers
        self.logic = logic.upper()

    def should_fire(self, context: CircuitContext) -> bool:
        """Evaluate composite logic"""
        if self.logic == "AND":
            return all(trigger.should_fire(context) for trigger in self.triggers)
        elif self.logic == "OR":
            return any(trigger.should_fire(context) for trigger in self.triggers)
        else:
            return False


# Convenience factory functions
def on_lead_created(conditions: Optional[Dict[str, Any]] = None, priority: int = 5) -> Trigger:
    """Factory for LEAD_CREATED trigger"""
    return SimpleTrigger(TriggerEvent.LEAD_CREATED, conditions, priority)


def on_opportunity_created(conditions: Optional[Dict[str, Any]] = None, priority: int = 5) -> Trigger:
    """Factory for OPPORTUNITY_CREATED trigger"""
    return SimpleTrigger(TriggerEvent.OPPORTUNITY_CREATED, conditions, priority)


def on_hot_lead(score_threshold: float = 80, priority: int = 10) -> Trigger:
    """Factory for HOT_LEAD_DETECTED trigger"""
    return ThresholdTrigger(
        event=TriggerEvent.HOT_LEAD_DETECTED,
        variable_name="lead_score",
        threshold=score_threshold,
        operator="gt",
        priority=priority
    )


def on_churn_risk(risk_threshold: float = 0.7, priority: int = 9) -> Trigger:
    """Factory for CHURN_RISK_HIGH trigger"""
    return ThresholdTrigger(
        event=TriggerEvent.CHURN_RISK_HIGH,
        variable_name="churn_risk",
        threshold=risk_threshold,
        operator="gt",
        priority=priority
    )


def daily_at(hour: int, minute: int = 0, event: TriggerEvent = TriggerEvent.DAILY_SYNC) -> Trigger:
    """Factory for daily scheduled trigger"""
    cron = f"{minute} {hour} * * *"
    return ScheduledTrigger(cron, event, priority=5)


def nightly_training() -> Trigger:
    """Factory for nightly ML training trigger (2am)"""
    return ScheduledTrigger("0 2 * * *", TriggerEvent.NIGHTLY_TRAINING, priority=3)
