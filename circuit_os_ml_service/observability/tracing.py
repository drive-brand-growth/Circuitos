"""
Distributed Tracing with OpenTelemetry
Complete tracing instrumentation for Circuit OS
"""

from typing import Dict, Optional, Callable, Any
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.trace import Status, StatusCode, SpanKind
from functools import wraps
from contextlib import contextmanager
import logging
import os

logger = logging.getLogger(__name__)


# ============================================================================
# TRACING MANAGER
# ============================================================================

class TracingManager:
    """
    Centralized tracing manager using OpenTelemetry
    """

    def __init__(
        self,
        service_name: str = "circuit-os",
        service_version: str = "2.0.0",
        environment: str = None
    ):
        self.service_name = service_name
        self.service_version = service_version
        self.environment = environment or os.getenv("ENVIRONMENT", "development")

        # Create resource
        resource = Resource.create({
            "service.name": self.service_name,
            "service.version": self.service_version,
            "deployment.environment": self.environment,
        })

        # Create tracer provider
        self.tracer_provider = TracerProvider(resource=resource)

        # Add console exporter for development
        console_exporter = ConsoleSpanExporter()
        span_processor = BatchSpanProcessor(console_exporter)
        self.tracer_provider.add_span_processor(span_processor)

        # Set global tracer provider
        trace.set_tracer_provider(self.tracer_provider)

        # Get tracer
        self.tracer = trace.get_tracer(__name__)

        logger.info(f"Tracing initialized for service: {self.service_name}")

    def get_tracer(self):
        """Get OpenTelemetry tracer"""
        return self.tracer

    @contextmanager
    def create_span(
        self,
        name: str,
        attributes: Dict[str, Any] = None,
        kind: SpanKind = SpanKind.INTERNAL
    ):
        """
        Create a new span with context manager

        Usage:
            with tracing.create_span("operation_name"):
                # your code here
        """
        with self.tracer.start_as_current_span(name, kind=kind) as span:
            if attributes:
                for key, value in attributes.items():
                    span.set_attribute(key, value)

            try:
                yield span
            except Exception as e:
                span.set_status(Status(StatusCode.ERROR, str(e)))
                span.record_exception(e)
                raise

    def add_event(self, span_name: str, event_name: str, attributes: Dict = None):
        """Add event to current span"""
        span = trace.get_current_span()
        if span:
            span.add_event(event_name, attributes=attributes or {})

    def set_attributes(self, attributes: Dict[str, Any]):
        """Set attributes on current span"""
        span = trace.get_current_span()
        if span:
            for key, value in attributes.items():
                span.set_attribute(key, value)

    def set_status(self, status_code: StatusCode, description: str = None):
        """Set status on current span"""
        span = trace.get_current_span()
        if span:
            span.set_status(Status(status_code, description or ""))

    def record_exception(self, exception: Exception):
        """Record exception on current span"""
        span = trace.get_current_span()
        if span:
            span.record_exception(exception)
            span.set_status(Status(StatusCode.ERROR, str(exception)))

    # ========================================================================
    # CIRCUIT TRACING
    # ========================================================================

    def trace_circuit_execution(
        self,
        circuit_name: str,
        data: Dict[str, Any]
    ):
        """
        Create span for circuit execution

        Returns context manager
        """
        return self.create_span(
            f"circuit.{circuit_name}",
            attributes={
                "circuit.name": circuit_name,
                "circuit.trigger_count": 0,  # Will be updated
                "circuit.action_count": 0,  # Will be updated
            },
            kind=SpanKind.INTERNAL
        )

    def trace_action_execution(
        self,
        action_name: str,
        action_type: str
    ):
        """Create span for action execution"""
        return self.create_span(
            f"action.{action_name}",
            attributes={
                "action.name": action_name,
                "action.type": action_type,
            },
            kind=SpanKind.INTERNAL
        )

    # ========================================================================
    # API TRACING
    # ========================================================================

    def trace_http_request(
        self,
        method: str,
        endpoint: str,
        user_id: Optional[str] = None
    ):
        """Create span for HTTP request"""
        attributes = {
            "http.method": method,
            "http.route": endpoint,
        }

        if user_id:
            attributes["user.id"] = user_id

        return self.create_span(
            f"HTTP {method} {endpoint}",
            attributes=attributes,
            kind=SpanKind.SERVER
        )

    # ========================================================================
    # INTELLIGENCE TRACING
    # ========================================================================

    def trace_rag_query(
        self,
        query: str,
        k: int
    ):
        """Create span for RAG query"""
        return self.create_span(
            "rag.query",
            attributes={
                "rag.query": query[:100],  # Truncate for trace
                "rag.k": k,
            },
            kind=SpanKind.CLIENT
        )

    def trace_ml_prediction(
        self,
        model_name: str,
        feature_count: int
    ):
        """Create span for ML prediction"""
        return self.create_span(
            f"ml.predict.{model_name}",
            attributes={
                "ml.model_name": model_name,
                "ml.feature_count": feature_count,
            },
            kind=SpanKind.CLIENT
        )

    def trace_kg_query(
        self,
        query_type: str
    ):
        """Create span for knowledge graph query"""
        return self.create_span(
            f"kg.{query_type}",
            attributes={
                "kg.query_type": query_type,
            },
            kind=SpanKind.CLIENT
        )

    # ========================================================================
    # SECURITY TRACING
    # ========================================================================

    def trace_authentication(
        self,
        email: str
    ):
        """Create span for authentication"""
        return self.create_span(
            "auth.login",
            attributes={
                "auth.email": email,
            },
            kind=SpanKind.INTERNAL
        )

    def trace_authorization(
        self,
        user_id: str,
        permission: str
    ):
        """Create span for authorization check"""
        return self.create_span(
            "authz.check",
            attributes={
                "authz.user_id": user_id,
                "authz.permission": permission,
            },
            kind=SpanKind.INTERNAL
        )


# ============================================================================
# GLOBAL TRACING MANAGER
# ============================================================================

_tracing_manager = None


def get_tracing_manager() -> TracingManager:
    """Get global tracing manager instance"""
    global _tracing_manager
    if _tracing_manager is None:
        _tracing_manager = TracingManager()
    return _tracing_manager


# ============================================================================
# DECORATOR FUNCTIONS
# ============================================================================

def trace_span(
    name: str,
    attributes: Dict[str, Any] = None,
    kind: SpanKind = SpanKind.INTERNAL
):
    """
    Decorator to create a traced span

    Usage:
        @trace_span("process_lead", attributes={"type": "lead"})
        async def process_lead(lead_id):
            ...
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            tracing = get_tracing_manager()

            with tracing.create_span(name, attributes, kind):
                try:
                    result = await func(*args, **kwargs)
                    tracing.set_status(StatusCode.OK)
                    return result
                except Exception as e:
                    tracing.record_exception(e)
                    raise

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            tracing = get_tracing_manager()

            with tracing.create_span(name, attributes, kind):
                try:
                    result = func(*args, **kwargs)
                    tracing.set_status(StatusCode.OK)
                    return result
                except Exception as e:
                    tracing.record_exception(e)
                    raise

        # Return appropriate wrapper based on function type
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper

    return decorator


def trace_circuit_execution(circuit_name: str):
    """
    Decorator to trace circuit execution

    Usage:
        @trace_circuit_execution("lead_processing")
        async def execute_circuit(context):
            ...
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            tracing = get_tracing_manager()

            data = {}
            if kwargs.get('data'):
                data = kwargs['data']
            elif len(args) > 0 and isinstance(args[0], dict):
                data = args[0]

            with tracing.trace_circuit_execution(circuit_name, data):
                try:
                    result = await func(*args, **kwargs)

                    # Add result attributes
                    if hasattr(result, 'get_metadata'):
                        metadata = result.get_metadata()
                        tracing.set_attributes({
                            "circuit.status": metadata.get("status", "unknown"),
                            "circuit.actions_executed": len(metadata.get("actions_executed", [])),
                        })

                    tracing.set_status(StatusCode.OK)
                    return result
                except Exception as e:
                    tracing.record_exception(e)
                    raise

        return wrapper
    return decorator


def trace_api_request(method: str, endpoint: str):
    """
    Decorator to trace API requests

    Usage:
        @trace_api_request("POST", "/api/v1/execute")
        async def execute_circuit():
            ...
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            tracing = get_tracing_manager()

            # Try to extract user_id from kwargs
            user_id = None
            if 'current_user' in kwargs:
                user = kwargs['current_user']
                user_id = getattr(user, 'user_id', None)

            with tracing.trace_http_request(method, endpoint, user_id):
                try:
                    result = await func(*args, **kwargs)
                    tracing.set_status(StatusCode.OK)
                    return result
                except Exception as e:
                    tracing.record_exception(e)
                    raise

        return wrapper
    return decorator


# Import asyncio for checking coroutine functions
import asyncio
