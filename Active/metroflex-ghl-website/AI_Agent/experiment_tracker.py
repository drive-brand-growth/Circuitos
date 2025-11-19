"""
MetroFlex Experiment Tracker - A/B Testing for Sales Hooks
==========================================================

High-velocity testing system that allows testing 50+ sales hook variants
simultaneously and auto-optimizes based on engagement data.

This replaces the need for large teams running manual A/B tests.

Components:
1. Experiment creation with multiple variants
2. Random assignment with tracking
3. Metric collection (impressions, responses, bookings)
4. Statistical significance calculation
5. Auto-promotion of winners
6. Integration with n8n workflows

Database Schema (PostgreSQL):
- experiments: Experiment metadata
- variants: Hook variants within experiments
- assignments: Which lead got which variant
- metrics: Engagement events per variant
"""

import os
import json
import random
import hashlib
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import statistics


# =============================================================================
# DATA MODELS
# =============================================================================

class ExperimentStatus(str, Enum):
    DRAFT = "draft"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class MetricType(str, Enum):
    IMPRESSION = "impression"  # Message sent
    OPEN = "open"  # Email opened
    CLICK = "click"  # Link clicked
    REPLY = "reply"  # Response received
    BOOKING = "booking"  # Call/meeting booked
    CONVERSION = "conversion"  # Deal closed


@dataclass
class Variant:
    """Single hook variant in an experiment"""
    id: str
    experiment_id: str
    name: str
    hook_text: str
    impressions: int = 0
    opens: int = 0
    clicks: int = 0
    replies: int = 0
    bookings: int = 0
    conversions: int = 0
    is_control: bool = False
    is_winner: bool = False
    created_at: datetime = None


@dataclass
class Experiment:
    """A/B test experiment"""
    id: str
    name: str
    description: str
    status: ExperimentStatus
    business_context: str  # licensing, gym, events
    channel: str  # sms, email
    variants: List[Variant]
    min_sample_size: int = 100
    confidence_threshold: float = 0.95
    created_at: datetime = None
    started_at: datetime = None
    completed_at: datetime = None
    winner_variant_id: Optional[str] = None


# =============================================================================
# IN-MEMORY STORAGE (Replace with PostgreSQL in production)
# =============================================================================

class ExperimentStorage:
    """
    In-memory experiment storage.
    Replace with PostgreSQL for production.
    """

    def __init__(self):
        self.experiments: Dict[str, Experiment] = {}
        self.assignments: Dict[str, str] = {}  # contact_id -> variant_id
        self.metrics: List[Dict] = []

    def save_experiment(self, experiment: Experiment):
        self.experiments[experiment.id] = experiment

    def get_experiment(self, experiment_id: str) -> Optional[Experiment]:
        return self.experiments.get(experiment_id)

    def get_active_experiments(self, business_context: str = None) -> List[Experiment]:
        active = [e for e in self.experiments.values()
                  if e.status == ExperimentStatus.RUNNING]
        if business_context:
            active = [e for e in active if e.business_context == business_context]
        return active

    def save_assignment(self, contact_id: str, variant_id: str, experiment_id: str):
        key = f"{experiment_id}:{contact_id}"
        self.assignments[key] = variant_id

    def get_assignment(self, contact_id: str, experiment_id: str) -> Optional[str]:
        key = f"{experiment_id}:{contact_id}"
        return self.assignments.get(key)

    def record_metric(
        self,
        variant_id: str,
        experiment_id: str,
        metric_type: MetricType,
        contact_id: str
    ):
        self.metrics.append({
            "variant_id": variant_id,
            "experiment_id": experiment_id,
            "metric_type": metric_type.value,
            "contact_id": contact_id,
            "timestamp": datetime.now().isoformat()
        })


# =============================================================================
# EXPERIMENT TRACKER
# =============================================================================

class ExperimentTracker:
    """
    Manages A/B testing experiments for sales hooks.

    Usage:
    1. Create experiment with variants
    2. Assign variants to incoming leads
    3. Track engagement metrics
    4. Calculate statistical significance
    5. Promote winners automatically
    """

    def __init__(self, storage: ExperimentStorage = None):
        self.storage = storage or ExperimentStorage()

    def create_experiment(
        self,
        name: str,
        description: str,
        business_context: str,
        channel: str,
        variants: List[Dict[str, str]],  # [{"name": "v1", "hook_text": "..."}]
        min_sample_size: int = 100,
        confidence_threshold: float = 0.95
    ) -> Experiment:
        """
        Create a new A/B test experiment.

        Args:
            name: Experiment name
            description: What we're testing
            business_context: licensing, gym, events
            channel: sms, email
            variants: List of variant configs
            min_sample_size: Min impressions per variant before analysis
            confidence_threshold: Required confidence to declare winner

        Returns:
            Created Experiment
        """
        # Generate experiment ID
        exp_id = f"exp_{hashlib.md5(f'{name}{datetime.now()}'.encode()).hexdigest()[:8]}"

        # Create variant objects
        variant_objects = []
        for i, v in enumerate(variants):
            var_id = f"{exp_id}_v{i}"
            variant_objects.append(Variant(
                id=var_id,
                experiment_id=exp_id,
                name=v.get("name", f"Variant {i}"),
                hook_text=v["hook_text"],
                is_control=(i == 0),  # First variant is control
                created_at=datetime.now()
            ))

        # Create experiment
        experiment = Experiment(
            id=exp_id,
            name=name,
            description=description,
            status=ExperimentStatus.DRAFT,
            business_context=business_context,
            channel=channel,
            variants=variant_objects,
            min_sample_size=min_sample_size,
            confidence_threshold=confidence_threshold,
            created_at=datetime.now()
        )

        self.storage.save_experiment(experiment)
        return experiment

    def start_experiment(self, experiment_id: str) -> bool:
        """Start running an experiment"""
        experiment = self.storage.get_experiment(experiment_id)
        if not experiment:
            return False

        experiment.status = ExperimentStatus.RUNNING
        experiment.started_at = datetime.now()
        self.storage.save_experiment(experiment)
        return True

    def assign_variant(
        self,
        experiment_id: str,
        contact_id: str
    ) -> Optional[Variant]:
        """
        Assign a variant to a contact for an experiment.

        Uses consistent hashing so same contact always gets same variant.

        Returns:
            Assigned Variant or None if experiment not found/running
        """
        experiment = self.storage.get_experiment(experiment_id)
        if not experiment or experiment.status != ExperimentStatus.RUNNING:
            return None

        # Check for existing assignment
        existing = self.storage.get_assignment(contact_id, experiment_id)
        if existing:
            for v in experiment.variants:
                if v.id == existing:
                    return v

        # Consistent hash assignment (same contact = same variant)
        hash_input = f"{experiment_id}:{contact_id}"
        hash_value = int(hashlib.md5(hash_input.encode()).hexdigest(), 16)
        variant_index = hash_value % len(experiment.variants)

        variant = experiment.variants[variant_index]

        # Save assignment
        self.storage.save_assignment(contact_id, variant.id, experiment_id)

        # Increment impressions
        variant.impressions += 1
        self.storage.save_experiment(experiment)

        return variant

    def get_variant_for_context(
        self,
        contact_id: str,
        business_context: str,
        channel: str
    ) -> Optional[Tuple[str, str]]:
        """
        Get the hook text for a contact based on active experiments.

        Returns:
            (variant_id, hook_text) or None if no active experiment
        """
        # Find active experiments for this context
        experiments = self.storage.get_active_experiments(business_context)
        experiments = [e for e in experiments if e.channel == channel]

        if not experiments:
            return None

        # Use first matching experiment
        experiment = experiments[0]
        variant = self.assign_variant(experiment.id, contact_id)

        if variant:
            return (variant.id, variant.hook_text)

        return None

    def record_metric(
        self,
        variant_id: str,
        metric_type: MetricType,
        contact_id: str
    ):
        """
        Record an engagement metric for a variant.

        Args:
            variant_id: The variant that produced this metric
            metric_type: Type of engagement (open, click, reply, booking)
            contact_id: The contact who engaged
        """
        # Find experiment and variant
        for experiment in self.storage.experiments.values():
            for variant in experiment.variants:
                if variant.id == variant_id:
                    # Update variant metrics
                    if metric_type == MetricType.IMPRESSION:
                        pass  # Already counted in assign_variant
                    elif metric_type == MetricType.OPEN:
                        variant.opens += 1
                    elif metric_type == MetricType.CLICK:
                        variant.clicks += 1
                    elif metric_type == MetricType.REPLY:
                        variant.replies += 1
                    elif metric_type == MetricType.BOOKING:
                        variant.bookings += 1
                    elif metric_type == MetricType.CONVERSION:
                        variant.conversions += 1

                    self.storage.save_experiment(experiment)
                    self.storage.record_metric(
                        variant_id, experiment.id, metric_type, contact_id
                    )
                    return

    def calculate_variant_stats(self, variant: Variant) -> Dict:
        """Calculate performance statistics for a variant"""
        if variant.impressions == 0:
            return {
                "open_rate": 0,
                "click_rate": 0,
                "reply_rate": 0,
                "booking_rate": 0,
                "conversion_rate": 0
            }

        return {
            "open_rate": variant.opens / variant.impressions,
            "click_rate": variant.clicks / variant.impressions,
            "reply_rate": variant.replies / variant.impressions,
            "booking_rate": variant.bookings / variant.impressions,
            "conversion_rate": variant.conversions / variant.impressions,
            "impressions": variant.impressions,
            "bookings": variant.bookings
        }

    def calculate_significance(
        self,
        control: Variant,
        treatment: Variant,
        metric: str = "reply_rate"
    ) -> Dict:
        """
        Calculate statistical significance between control and treatment.

        Uses simple z-test for proportions.

        Returns:
            {
                "is_significant": bool,
                "confidence": float,
                "lift": float,
                "p_value": float
            }
        """
        import math

        # Get rates based on metric
        if metric == "reply_rate":
            control_successes = control.replies
            treatment_successes = treatment.replies
        elif metric == "booking_rate":
            control_successes = control.bookings
            treatment_successes = treatment.bookings
        else:
            control_successes = control.replies
            treatment_successes = treatment.replies

        n1 = control.impressions
        n2 = treatment.impressions

        if n1 == 0 or n2 == 0:
            return {
                "is_significant": False,
                "confidence": 0,
                "lift": 0,
                "p_value": 1.0
            }

        p1 = control_successes / n1
        p2 = treatment_successes / n2

        # Pooled proportion
        p_pooled = (control_successes + treatment_successes) / (n1 + n2)

        # Standard error
        if p_pooled == 0 or p_pooled == 1:
            return {
                "is_significant": False,
                "confidence": 0,
                "lift": 0,
                "p_value": 1.0
            }

        se = math.sqrt(p_pooled * (1 - p_pooled) * (1/n1 + 1/n2))

        if se == 0:
            return {
                "is_significant": False,
                "confidence": 0,
                "lift": 0,
                "p_value": 1.0
            }

        # Z-score
        z = (p2 - p1) / se

        # P-value (two-tailed) - simplified approximation
        p_value = 2 * (1 - self._norm_cdf(abs(z)))

        # Confidence
        confidence = 1 - p_value

        # Lift
        lift = ((p2 - p1) / p1) if p1 > 0 else 0

        return {
            "is_significant": confidence >= 0.95,
            "confidence": confidence,
            "lift": lift,
            "p_value": p_value,
            "control_rate": p1,
            "treatment_rate": p2
        }

    def _norm_cdf(self, x: float) -> float:
        """Approximation of normal CDF"""
        import math
        return (1.0 + math.erf(x / math.sqrt(2.0))) / 2.0

    def analyze_experiment(self, experiment_id: str) -> Dict:
        """
        Analyze an experiment and determine if there's a winner.

        Returns:
            {
                "status": "needs_more_data" | "has_winner" | "no_winner",
                "winner": Variant or None,
                "analysis": {...}
            }
        """
        experiment = self.storage.get_experiment(experiment_id)
        if not experiment:
            return {"status": "not_found"}

        # Check sample size
        min_impressions = min(v.impressions for v in experiment.variants)
        if min_impressions < experiment.min_sample_size:
            return {
                "status": "needs_more_data",
                "current_impressions": min_impressions,
                "required_impressions": experiment.min_sample_size,
                "variants": [
                    {"name": v.name, "impressions": v.impressions, **self.calculate_variant_stats(v)}
                    for v in experiment.variants
                ]
            }

        # Find control variant
        control = next((v for v in experiment.variants if v.is_control), experiment.variants[0])

        # Analyze each treatment vs control
        best_variant = control
        best_lift = 0
        analysis_results = []

        for variant in experiment.variants:
            stats = self.calculate_variant_stats(variant)

            if variant.id != control.id:
                significance = self.calculate_significance(control, variant)
                stats["significance"] = significance

                if significance["is_significant"] and significance["lift"] > best_lift:
                    best_variant = variant
                    best_lift = significance["lift"]
            else:
                stats["significance"] = {"is_control": True}

            analysis_results.append({
                "variant": variant.name,
                "variant_id": variant.id,
                **stats
            })

        # Determine if we have a winner
        if best_lift > 0:
            return {
                "status": "has_winner",
                "winner": {
                    "id": best_variant.id,
                    "name": best_variant.name,
                    "lift": best_lift
                },
                "analysis": analysis_results
            }
        else:
            return {
                "status": "no_winner",
                "message": "No variant significantly outperformed control",
                "analysis": analysis_results
            }

    def complete_experiment(
        self,
        experiment_id: str,
        winner_variant_id: str = None
    ) -> bool:
        """
        Complete an experiment and optionally set winner.

        Args:
            experiment_id: The experiment to complete
            winner_variant_id: The winning variant (auto-detected if not provided)
        """
        experiment = self.storage.get_experiment(experiment_id)
        if not experiment:
            return False

        # Auto-detect winner if not provided
        if not winner_variant_id:
            analysis = self.analyze_experiment(experiment_id)
            if analysis.get("status") == "has_winner":
                winner_variant_id = analysis["winner"]["id"]

        # Update experiment
        experiment.status = ExperimentStatus.COMPLETED
        experiment.completed_at = datetime.now()
        experiment.winner_variant_id = winner_variant_id

        # Mark winner
        for variant in experiment.variants:
            variant.is_winner = (variant.id == winner_variant_id)

        self.storage.save_experiment(experiment)
        return True

    def get_experiment_report(self, experiment_id: str) -> Dict:
        """Get comprehensive experiment report"""
        experiment = self.storage.get_experiment(experiment_id)
        if not experiment:
            return {"error": "Experiment not found"}

        analysis = self.analyze_experiment(experiment_id)

        return {
            "experiment": {
                "id": experiment.id,
                "name": experiment.name,
                "description": experiment.description,
                "status": experiment.status.value,
                "business_context": experiment.business_context,
                "channel": experiment.channel,
                "created_at": experiment.created_at.isoformat() if experiment.created_at else None,
                "started_at": experiment.started_at.isoformat() if experiment.started_at else None,
                "completed_at": experiment.completed_at.isoformat() if experiment.completed_at else None
            },
            "variants": [
                {
                    "id": v.id,
                    "name": v.name,
                    "hook_text": v.hook_text,
                    "is_control": v.is_control,
                    "is_winner": v.is_winner,
                    **self.calculate_variant_stats(v)
                }
                for v in experiment.variants
            ],
            "analysis": analysis
        }


# =============================================================================
# POSTGRESQL SCHEMA (For production deployment)
# =============================================================================

POSTGRESQL_SCHEMA = """
-- Experiment Tracking Schema for MetroFlex A/B Testing

-- Experiments table
CREATE TABLE IF NOT EXISTS experiments (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(20) DEFAULT 'draft',
    business_context VARCHAR(50),  -- licensing, gym, events
    channel VARCHAR(20),  -- sms, email
    min_sample_size INT DEFAULT 100,
    confidence_threshold DECIMAL(3,2) DEFAULT 0.95,
    winner_variant_id VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW(),
    started_at TIMESTAMP,
    completed_at TIMESTAMP
);

-- Variants table
CREATE TABLE IF NOT EXISTS variants (
    id VARCHAR(50) PRIMARY KEY,
    experiment_id VARCHAR(50) REFERENCES experiments(id) ON DELETE CASCADE,
    name VARCHAR(255),
    hook_text TEXT NOT NULL,
    is_control BOOLEAN DEFAULT FALSE,
    is_winner BOOLEAN DEFAULT FALSE,
    impressions INT DEFAULT 0,
    opens INT DEFAULT 0,
    clicks INT DEFAULT 0,
    replies INT DEFAULT 0,
    bookings INT DEFAULT 0,
    conversions INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Assignments table (which contact got which variant)
CREATE TABLE IF NOT EXISTS experiment_assignments (
    id SERIAL PRIMARY KEY,
    experiment_id VARCHAR(50) REFERENCES experiments(id) ON DELETE CASCADE,
    contact_id VARCHAR(100) NOT NULL,
    variant_id VARCHAR(50) REFERENCES variants(id) ON DELETE CASCADE,
    assigned_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(experiment_id, contact_id)
);

-- Metrics table (engagement events)
CREATE TABLE IF NOT EXISTS experiment_metrics (
    id SERIAL PRIMARY KEY,
    experiment_id VARCHAR(50) REFERENCES experiments(id) ON DELETE CASCADE,
    variant_id VARCHAR(50) REFERENCES variants(id) ON DELETE CASCADE,
    contact_id VARCHAR(100),
    metric_type VARCHAR(20) NOT NULL,  -- impression, open, click, reply, booking, conversion
    recorded_at TIMESTAMP DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_variants_experiment ON variants(experiment_id);
CREATE INDEX IF NOT EXISTS idx_assignments_experiment ON experiment_assignments(experiment_id);
CREATE INDEX IF NOT EXISTS idx_assignments_contact ON experiment_assignments(contact_id);
CREATE INDEX IF NOT EXISTS idx_metrics_experiment ON experiment_metrics(experiment_id);
CREATE INDEX IF NOT EXISTS idx_metrics_variant ON experiment_metrics(variant_id);
CREATE INDEX IF NOT EXISTS idx_metrics_type ON experiment_metrics(metric_type);
CREATE INDEX IF NOT EXISTS idx_experiments_status ON experiments(status);
CREATE INDEX IF NOT EXISTS idx_experiments_context ON experiments(business_context);
"""


# =============================================================================
# N8N INTEGRATION HELPERS
# =============================================================================

def create_n8n_experiment_node_config(experiment_id: str) -> Dict:
    """
    Generate n8n node configuration for experiment routing.

    This creates a "Switch" node that routes contacts to different
    workflow branches based on their variant assignment.
    """
    return {
        "name": f"Experiment Router - {experiment_id}",
        "type": "n8n-nodes-base.switch",
        "parameters": {
            "rules": {
                "rules": [
                    {
                        "conditions": {
                            "conditions": [
                                {
                                    "leftValue": "={{ $json.variant_id }}",
                                    "rightValue": f"{experiment_id}_v0",
                                    "operator": {
                                        "type": "string",
                                        "operation": "equals"
                                    }
                                }
                            ]
                        },
                        "output": 0  # Control branch
                    },
                    {
                        "conditions": {
                            "conditions": [
                                {
                                    "leftValue": "={{ $json.variant_id }}",
                                    "rightValue": f"{experiment_id}_v1",
                                    "operator": {
                                        "type": "string",
                                        "operation": "equals"
                                    }
                                }
                            ]
                        },
                        "output": 1  # Treatment branch
                    }
                ]
            }
        }
    }


def create_webhook_for_metrics() -> Dict:
    """
    Create webhook configuration for recording experiment metrics.

    Call this webhook when engagement events occur (opens, clicks, etc.)
    """
    return {
        "endpoint": "/api/experiments/metric",
        "method": "POST",
        "payload": {
            "variant_id": "{{ variant_id from assignment }}",
            "metric_type": "reply|booking|click|open",
            "contact_id": "{{ contact_id }}"
        }
    }


# =============================================================================
# TESTING
# =============================================================================

if __name__ == "__main__":
    print("Testing Experiment Tracker...")

    tracker = ExperimentTracker()

    # Create test experiment with 3 variants
    experiment = tracker.create_experiment(
        name="Licensing SMS Hook Test",
        description="Testing urgency vs scarcity vs social proof hooks",
        business_context="licensing",
        channel="sms",
        variants=[
            {
                "name": "Control - Direct",
                "hook_text": "Brian Dobson here from MetroFlex. Ready to discuss your gym licensing opportunity?"
            },
            {
                "name": "Urgency",
                "hook_text": "Only 3 licensing territories left in Texas. Brian from MetroFlex - can we talk this week?"
            },
            {
                "name": "Social Proof",
                "hook_text": "15 MetroFlex locations now open. Brian here - want to see why owners are choosing us?"
            }
        ],
        min_sample_size=50
    )

    print(f"\nCreated experiment: {experiment.id}")
    print(f"Variants: {len(experiment.variants)}")

    # Start experiment
    tracker.start_experiment(experiment.id)
    print("Experiment started")

    # Simulate assignments and metrics
    test_contacts = [f"contact_{i}" for i in range(150)]

    for contact_id in test_contacts:
        variant = tracker.assign_variant(experiment.id, contact_id)

        # Simulate random engagement
        if random.random() < 0.3:  # 30% reply rate baseline
            # Urgency variant has higher reply rate
            if "Urgency" in variant.name:
                if random.random() < 0.45:  # 45% reply rate
                    tracker.record_metric(variant.id, MetricType.REPLY, contact_id)
            else:
                tracker.record_metric(variant.id, MetricType.REPLY, contact_id)

        # Some replies convert to bookings
        if random.random() < 0.1:
            tracker.record_metric(variant.id, MetricType.BOOKING, contact_id)

    # Analyze results
    print("\n--- Experiment Analysis ---")
    report = tracker.get_experiment_report(experiment.id)

    for variant in report["variants"]:
        print(f"\n{variant['name']}:")
        print(f"  Impressions: {variant['impressions']}")
        print(f"  Reply rate: {variant['reply_rate']:.1%}")
        print(f"  Booking rate: {variant['booking_rate']:.1%}")

    print(f"\nAnalysis status: {report['analysis']['status']}")
    if report['analysis'].get('winner'):
        print(f"Winner: {report['analysis']['winner']['name']}")
        print(f"Lift: {report['analysis']['winner']['lift']:.1%}")

    print("\n--- Experiment Tracking Test Complete ---")
    print("\nPostgreSQL Schema available in POSTGRESQL_SCHEMA variable")
