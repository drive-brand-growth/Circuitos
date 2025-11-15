"""
Prometheus Metrics Collector
Complete metrics instrumentation for Circuit OS
"""

from typing import Dict, Optional, Callable, Any
from prometheus_client import (
    Counter,
    Histogram,
    Gauge,
    Summary,
    Info,
    CollectorRegistry,
    generate_latest,
    CONTENT_TYPE_LATEST,
)
from functools import wraps
import time
import logging

logger = logging.getLogger(__name__)


# ============================================================================
# METRICS COLLECTOR
# ============================================================================

class MetricsCollector:
    """
    Centralized metrics collector using Prometheus
    """

    def __init__(self, registry: Optional[CollectorRegistry] = None):
        self.registry = registry or CollectorRegistry()

        # ====================================================================
        # CIRCUIT EXECUTION METRICS
        # ====================================================================

        # Circuit execution counter
        self.circuit_executions_total = Counter(
            'circuit_executions_total',
            'Total number of circuit executions',
            ['circuit_name', 'status'],
            registry=self.registry
        )

        # Circuit execution duration
        self.circuit_execution_duration = Histogram(
            'circuit_execution_duration_seconds',
            'Circuit execution duration in seconds',
            ['circuit_name'],
            buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0, 60.0],
            registry=self.registry
        )

        # Actions executed per circuit
        self.circuit_actions_executed = Histogram(
            'circuit_actions_executed',
            'Number of actions executed per circuit',
            ['circuit_name'],
            buckets=[1, 5, 10, 20, 50, 100],
            registry=self.registry
        )

        # Circuit errors
        self.circuit_errors_total = Counter(
            'circuit_errors_total',
            'Total number of circuit errors',
            ['circuit_name', 'error_type'],
            registry=self.registry
        )

        # Active circuits gauge
        self.circuits_active = Gauge(
            'circuits_active',
            'Number of currently executing circuits',
            registry=self.registry
        )

        # ====================================================================
        # API METRICS
        # ====================================================================

        # HTTP requests
        self.http_requests_total = Counter(
            'http_requests_total',
            'Total HTTP requests',
            ['method', 'endpoint', 'status'],
            registry=self.registry
        )

        # HTTP request duration
        self.http_request_duration = Histogram(
            'http_request_duration_seconds',
            'HTTP request duration in seconds',
            ['method', 'endpoint'],
            buckets=[0.01, 0.05, 0.1, 0.5, 1.0, 2.0, 5.0],
            registry=self.registry
        )

        # Active HTTP requests
        self.http_requests_active = Gauge(
            'http_requests_active',
            'Number of active HTTP requests',
            registry=self.registry
        )

        # ====================================================================
        # INTELLIGENCE METRICS
        # ====================================================================

        # RAG queries
        self.rag_queries_total = Counter(
            'rag_queries_total',
            'Total RAG queries',
            ['status'],
            registry=self.registry
        )

        # RAG query duration
        self.rag_query_duration = Histogram(
            'rag_query_duration_seconds',
            'RAG query duration in seconds',
            buckets=[0.1, 0.5, 1.0, 2.0, 5.0],
            registry=self.registry
        )

        # RAG documents retrieved
        self.rag_documents_retrieved = Histogram(
            'rag_documents_retrieved',
            'Number of documents retrieved per RAG query',
            buckets=[1, 5, 10, 20, 50],
            registry=self.registry
        )

        # ML predictions
        self.ml_predictions_total = Counter(
            'ml_predictions_total',
            'Total ML predictions',
            ['model_name', 'status'],
            registry=self.registry
        )

        # ML prediction duration
        self.ml_prediction_duration = Histogram(
            'ml_prediction_duration_seconds',
            'ML prediction duration in seconds',
            ['model_name'],
            buckets=[0.01, 0.05, 0.1, 0.5, 1.0],
            registry=self.registry
        )

        # ML prediction confidence
        self.ml_prediction_confidence = Histogram(
            'ml_prediction_confidence',
            'ML prediction confidence score',
            ['model_name'],
            buckets=[0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 0.99],
            registry=self.registry
        )

        # ML model retraining
        self.ml_model_retraining_total = Counter(
            'ml_model_retraining_total',
            'Total ML model retraining events',
            ['model_name', 'status'],
            registry=self.registry
        )

        # Knowledge graph queries
        self.kg_queries_total = Counter(
            'kg_queries_total',
            'Total knowledge graph queries',
            ['query_type', 'status'],
            registry=self.registry
        )

        # Knowledge graph query duration
        self.kg_query_duration = Histogram(
            'kg_query_duration_seconds',
            'Knowledge graph query duration in seconds',
            ['query_type'],
            buckets=[0.01, 0.05, 0.1, 0.5, 1.0],
            registry=self.registry
        )

        # ====================================================================
        # SECURITY METRICS
        # ====================================================================

        # Authentication attempts
        self.auth_attempts_total = Counter(
            'auth_attempts_total',
            'Total authentication attempts',
            ['status'],
            registry=self.registry
        )

        # Authorization checks
        self.authz_checks_total = Counter(
            'authz_checks_total',
            'Total authorization checks',
            ['permission', 'status'],
            registry=self.registry
        )

        # Rate limit hits
        self.rate_limit_hits_total = Counter(
            'rate_limit_hits_total',
            'Total rate limit hits',
            ['user_role'],
            registry=self.registry
        )

        # Injection attempts blocked
        self.injection_attempts_blocked = Counter(
            'injection_attempts_blocked_total',
            'Total injection attempts blocked',
            ['attack_type'],
            registry=self.registry
        )

        # Active user sessions
        self.active_sessions = Gauge(
            'active_sessions',
            'Number of active user sessions',
            registry=self.registry
        )

        # ====================================================================
        # SYSTEM METRICS
        # ====================================================================

        # System info
        self.system_info = Info(
            'circuit_os_system',
            'Circuit OS system information',
            registry=self.registry
        )

        # Registered circuits
        self.circuits_registered = Gauge(
            'circuits_registered',
            'Number of registered circuits',
            registry=self.registry
        )

        # Actions registered
        self.actions_registered = Gauge(
            'actions_registered',
            'Number of registered action types',
            registry=self.registry
        )

        # Database connections (if applicable)
        self.db_connections_active = Gauge(
            'db_connections_active',
            'Number of active database connections',
            registry=self.registry
        )

        # Memory usage (application-level)
        self.memory_usage_bytes = Gauge(
            'memory_usage_bytes',
            'Application memory usage in bytes',
            registry=self.registry
        )

        logger.info("Metrics collector initialized with Prometheus")

    # ========================================================================
    # CIRCUIT METRICS METHODS
    # ========================================================================

    def record_circuit_execution(
        self,
        circuit_name: str,
        duration: float,
        status: str,
        actions_count: int,
        error_type: Optional[str] = None
    ):
        """Record circuit execution metrics"""
        self.circuit_executions_total.labels(
            circuit_name=circuit_name,
            status=status
        ).inc()

        self.circuit_execution_duration.labels(
            circuit_name=circuit_name
        ).observe(duration)

        self.circuit_actions_executed.labels(
            circuit_name=circuit_name
        ).observe(actions_count)

        if error_type:
            self.circuit_errors_total.labels(
                circuit_name=circuit_name,
                error_type=error_type
            ).inc()

    def increment_active_circuits(self):
        """Increment active circuits gauge"""
        self.circuits_active.inc()

    def decrement_active_circuits(self):
        """Decrement active circuits gauge"""
        self.circuits_active.dec()

    # ========================================================================
    # API METRICS METHODS
    # ========================================================================

    def record_http_request(
        self,
        method: str,
        endpoint: str,
        status_code: int,
        duration: float
    ):
        """Record HTTP request metrics"""
        self.http_requests_total.labels(
            method=method,
            endpoint=endpoint,
            status=status_code
        ).inc()

        self.http_request_duration.labels(
            method=method,
            endpoint=endpoint
        ).observe(duration)

    def increment_active_requests(self):
        """Increment active requests gauge"""
        self.http_requests_active.inc()

    def decrement_active_requests(self):
        """Decrement active requests gauge"""
        self.http_requests_active.dec()

    # ========================================================================
    # INTELLIGENCE METRICS METHODS
    # ========================================================================

    def record_rag_query(
        self,
        duration: float,
        documents_count: int,
        status: str = "success"
    ):
        """Record RAG query metrics"""
        self.rag_queries_total.labels(status=status).inc()
        self.rag_query_duration.observe(duration)
        self.rag_documents_retrieved.observe(documents_count)

    def record_ml_prediction(
        self,
        model_name: str,
        duration: float,
        confidence: float,
        status: str = "success"
    ):
        """Record ML prediction metrics"""
        self.ml_predictions_total.labels(
            model_name=model_name,
            status=status
        ).inc()

        self.ml_prediction_duration.labels(
            model_name=model_name
        ).observe(duration)

        self.ml_prediction_confidence.labels(
            model_name=model_name
        ).observe(confidence)

    def record_ml_retraining(
        self,
        model_name: str,
        status: str = "success"
    ):
        """Record ML model retraining event"""
        self.ml_model_retraining_total.labels(
            model_name=model_name,
            status=status
        ).inc()

    def record_kg_query(
        self,
        query_type: str,
        duration: float,
        status: str = "success"
    ):
        """Record knowledge graph query metrics"""
        self.kg_queries_total.labels(
            query_type=query_type,
            status=status
        ).inc()

        self.kg_query_duration.labels(
            query_type=query_type
        ).observe(duration)

    # ========================================================================
    # SECURITY METRICS METHODS
    # ========================================================================

    def record_auth_attempt(self, status: str):
        """Record authentication attempt"""
        self.auth_attempts_total.labels(status=status).inc()

    def record_authz_check(self, permission: str, status: str):
        """Record authorization check"""
        self.authz_checks_total.labels(
            permission=permission,
            status=status
        ).inc()

    def record_rate_limit_hit(self, user_role: str):
        """Record rate limit hit"""
        self.rate_limit_hits_total.labels(user_role=user_role).inc()

    def record_injection_blocked(self, attack_type: str):
        """Record blocked injection attempt"""
        self.injection_attempts_blocked.labels(
            attack_type=attack_type
        ).inc()

    def set_active_sessions(self, count: int):
        """Set active sessions count"""
        self.active_sessions.set(count)

    # ========================================================================
    # SYSTEM METRICS METHODS
    # ========================================================================

    def set_system_info(self, info: Dict[str, str]):
        """Set system information"""
        self.system_info.info(info)

    def set_circuits_registered(self, count: int):
        """Set registered circuits count"""
        self.circuits_registered.set(count)

    def set_actions_registered(self, count: int):
        """Set registered actions count"""
        self.actions_registered.set(count)

    def set_db_connections(self, count: int):
        """Set active database connections"""
        self.db_connections_active.set(count)

    def set_memory_usage(self, bytes_used: int):
        """Set memory usage"""
        self.memory_usage_bytes.set(bytes_used)

    # ========================================================================
    # EXPORT METHODS
    # ========================================================================

    def generate_metrics(self) -> bytes:
        """Generate Prometheus metrics output"""
        return generate_latest(self.registry)

    def get_content_type(self) -> str:
        """Get Prometheus content type"""
        return CONTENT_TYPE_LATEST


# ============================================================================
# GLOBAL METRICS COLLECTOR
# ============================================================================

_metrics_collector = None


def get_metrics_collector() -> MetricsCollector:
    """Get global metrics collector instance"""
    global _metrics_collector
    if _metrics_collector is None:
        _metrics_collector = MetricsCollector()
    return _metrics_collector


# ============================================================================
# DECORATOR FUNCTIONS
# ============================================================================

def track_circuit_execution(circuit_name: str):
    """
    Decorator to track circuit execution metrics

    Usage:
        @track_circuit_execution("lead_processing")
        async def process_lead(context):
            ...
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            metrics = get_metrics_collector()
            metrics.increment_active_circuits()

            start_time = time.time()
            status = "success"
            error_type = None

            try:
                result = await func(*args, **kwargs)
                return result
            except Exception as e:
                status = "error"
                error_type = type(e).__name__
                raise
            finally:
                duration = time.time() - start_time
                metrics.decrement_active_circuits()

                # Get actions count from context if available
                actions_count = 0
                if args and hasattr(args[0], 'get_metadata'):
                    metadata = args[0].get_metadata()
                    actions_count = len(metadata.get('actions_executed', []))

                metrics.record_circuit_execution(
                    circuit_name=circuit_name,
                    duration=duration,
                    status=status,
                    actions_count=actions_count,
                    error_type=error_type
                )

        return wrapper
    return decorator


def track_api_request(method: str, endpoint: str):
    """
    Decorator to track API request metrics

    Usage:
        @track_api_request("POST", "/api/v1/execute")
        async def execute_circuit():
            ...
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            metrics = get_metrics_collector()
            metrics.increment_active_requests()

            start_time = time.time()
            status_code = 200

            try:
                result = await func(*args, **kwargs)
                return result
            except Exception as e:
                status_code = getattr(e, 'status_code', 500)
                raise
            finally:
                duration = time.time() - start_time
                metrics.decrement_active_requests()

                metrics.record_http_request(
                    method=method,
                    endpoint=endpoint,
                    status_code=status_code,
                    duration=duration
                )

        return wrapper
    return decorator


def track_ml_prediction(model_name: str):
    """
    Decorator to track ML prediction metrics

    Usage:
        @track_ml_prediction("lead_scorer_v2")
        async def predict(features):
            ...
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            metrics = get_metrics_collector()

            start_time = time.time()
            status = "success"
            confidence = 0.0

            try:
                result = await func(*args, **kwargs)

                # Extract confidence if available
                if hasattr(result, 'confidence'):
                    confidence = result.confidence
                elif isinstance(result, dict) and 'confidence' in result:
                    confidence = result['confidence']

                return result
            except Exception:
                status = "error"
                raise
            finally:
                duration = time.time() - start_time

                metrics.record_ml_prediction(
                    model_name=model_name,
                    duration=duration,
                    confidence=confidence,
                    status=status
                )

        return wrapper
    return decorator


def track_rag_query():
    """
    Decorator to track RAG query metrics

    Usage:
        @track_rag_query()
        async def retrieve(query, k):
            ...
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            metrics = get_metrics_collector()

            start_time = time.time()
            status = "success"
            documents_count = 0

            try:
                result = await func(*args, **kwargs)

                # Count documents
                if isinstance(result, list):
                    documents_count = len(result)
                elif isinstance(result, dict) and 'documents' in result:
                    documents_count = len(result['documents'])

                return result
            except Exception:
                status = "error"
                raise
            finally:
                duration = time.time() - start_time

                metrics.record_rag_query(
                    duration=duration,
                    documents_count=documents_count,
                    status=status
                )

        return wrapper
    return decorator
