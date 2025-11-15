"""
Observability Module - Metrics, Tracing, and Logging
Production-grade monitoring for Circuit OS
"""

from .metrics import (
    MetricsCollector,
    get_metrics_collector,
    track_circuit_execution,
    track_api_request,
    track_ml_prediction,
    track_rag_query,
)

from .tracing import (
    TracingManager,
    get_tracing_manager,
    trace_span,
    trace_circuit_execution,
    trace_api_request,
)

from .logging import (
    StructuredLogger,
    get_logger,
    log_circuit_execution,
    log_security_event,
    log_error,
)

__all__ = [
    # Metrics
    "MetricsCollector",
    "get_metrics_collector",
    "track_circuit_execution",
    "track_api_request",
    "track_ml_prediction",
    "track_rag_query",

    # Tracing
    "TracingManager",
    "get_tracing_manager",
    "trace_span",
    "trace_circuit_execution",
    "trace_api_request",

    # Logging
    "StructuredLogger",
    "get_logger",
    "log_circuit_execution",
    "log_security_event",
    "log_error",
]
