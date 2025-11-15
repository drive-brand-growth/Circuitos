"""
Observability Examples - Demonstrating Metrics, Tracing, and Logging
Complete observability demonstration
"""

import asyncio
import time
from datetime import datetime

from observability import (
    get_metrics_collector,
    get_tracing_manager,
    get_logger,
    track_circuit_execution,
    track_ml_prediction,
    track_rag_query,
    trace_span,
)


# ============================================================================
# DEMO 1: PROMETHEUS METRICS
# ============================================================================

async def demo_metrics():
    """Demonstrate Prometheus metrics collection"""
    print("=" * 70)
    print("DEMO 1: PROMETHEUS METRICS")
    print("=" * 70)
    print()

    metrics = get_metrics_collector()

    # Set system info
    print("1. Setting System Information:")
    metrics.set_system_info({
        "version": "3.0.0",
        "environment": "demo",
        "python_version": "3.11"
    })
    print("   ✓ System info recorded")
    print()

    # Record circuit executions
    print("2. Recording Circuit Executions:")
    for i in range(10):
        circuit_name = "lead_processing" if i < 8 else "data_sync"
        status = "success" if i < 9 else "error"
        duration = 0.5 + (i * 0.1)

        metrics.record_circuit_execution(
            circuit_name=circuit_name,
            duration=duration,
            status=status,
            actions_count=5
        )

        print(f"   ✓ Circuit {i+1}: {circuit_name} - {status} ({duration:.2f}s)")

    print()

    # Record API requests
    print("3. Recording API Requests:")
    endpoints = ["/api/v1/execute", "/api/v1/circuits", "/health"]
    for i, endpoint in enumerate(endpoints):
        status_code = 200 if i < 2 else 500

        metrics.record_http_request(
            method="GET" if i == 1 else "POST",
            endpoint=endpoint,
            status_code=status_code,
            duration=0.1 + (i * 0.05)
        )

        print(f"   ✓ {endpoint}: {status_code}")

    print()

    # Record ML predictions
    print("4. Recording ML Predictions:")
    models = ["lead_scorer_v2", "churn_predictor", "lead_scorer_v2"]
    for model in models:
        metrics.record_ml_prediction(
            model_name=model,
            duration=0.05,
            confidence=0.85 + (len(model) * 0.01),
            status="success"
        )

        print(f"   ✓ Model: {model}")

    print()

    # Record RAG queries
    print("5. Recording RAG Queries:")
    for i in range(5):
        metrics.record_rag_query(
            duration=0.3 + (i * 0.1),
            documents_count=10 - i,
            status="success"
        )

        print(f"   ✓ RAG query {i+1}: {10-i} documents")

    print()

    # Record security events
    print("6. Recording Security Events:")

    metrics.record_auth_attempt("success")
    metrics.record_auth_attempt("success")
    metrics.record_auth_attempt("failed")

    print("   ✓ Auth attempts: 2 success, 1 failed")

    metrics.record_rate_limit_hit("user")
    metrics.record_injection_blocked("sql")

    print("   ✓ Rate limit hit: 1")
    print("   ✓ Injection blocked: SQL")
    print()

    # Generate metrics output
    print("7. Generating Prometheus Metrics:")
    print()
    metrics_output = metrics.generate_metrics().decode('utf-8')

    # Show sample metrics
    lines = metrics_output.split('\n')
    interesting_metrics = [
        'circuit_executions_total',
        'circuit_execution_duration',
        'http_requests_total',
        'ml_predictions_total',
        'rag_queries_total',
        'auth_attempts_total'
    ]

    for metric_name in interesting_metrics:
        matching = [line for line in lines if metric_name in line and not line.startswith('#')]
        if matching:
            print(f"   {metric_name}:")
            for line in matching[:3]:  # Show first 3
                print(f"      {line}")
            if len(matching) > 3:
                print(f"      ... and {len(matching) - 3} more")
            print()

    print()


# ============================================================================
# DEMO 2: DISTRIBUTED TRACING
# ============================================================================

async def demo_tracing():
    """Demonstrate OpenTelemetry distributed tracing"""
    print("=" * 70)
    print("DEMO 2: DISTRIBUTED TRACING")
    print("=" * 70)
    print()

    tracing = get_tracing_manager()

    # Circuit execution trace
    print("1. Tracing Circuit Execution:")
    print()

    with tracing.trace_circuit_execution("lead_processing", {"lead_id": "123"}):
        print("   ✓ Started circuit execution span")

        # Simulate action executions
        with tracing.trace_action_execution("fetch_data", "DataFetchAction"):
            await asyncio.sleep(0.1)
            print("   ✓ Action 1: Fetch data")

        with tracing.trace_action_execution("ml_predict", "MLPredictAction"):
            await asyncio.sleep(0.05)
            print("   ✓ Action 2: ML prediction")

        with tracing.trace_action_execution("save_result", "DataWriteAction"):
            await asyncio.sleep(0.05)
            print("   ✓ Action 3: Save result")

        tracing.add_event("circuit_execution", "checkpoint", {"step": "completed"})
        print("   ✓ Added checkpoint event")

    print()

    # HTTP request trace
    print("2. Tracing HTTP Request:")
    print()

    with tracing.trace_http_request("POST", "/api/v1/execute", user_id="user_123"):
        print("   ✓ Started HTTP request span")
        await asyncio.sleep(0.1)
        tracing.set_attributes({
            "http.status_code": 200,
            "http.request_size": 1024
        })
        print("   ✓ Set HTTP attributes")

    print()

    # Intelligence operations trace
    print("3. Tracing Intelligence Operations:")
    print()

    with tracing.trace_rag_query("What are best practices for AI?", k=10):
        print("   ✓ RAG query span created")
        await asyncio.sleep(0.2)
        tracing.set_attributes({"documents_found": 10})
        print("   ✓ Found 10 documents")

    with tracing.trace_ml_prediction("lead_scorer_v2", feature_count=15):
        print("   ✓ ML prediction span created")
        await asyncio.sleep(0.05)
        tracing.set_attributes({
            "prediction": 0.85,
            "confidence": 0.92
        })
        print("   ✓ Prediction: 0.85 (confidence: 0.92)")

    print()

    # Nested spans
    print("4. Nested Span Hierarchy:")
    print()

    with tracing.create_span("parent_operation"):
        print("   ✓ Parent span")

        with tracing.create_span("child_operation_1"):
            print("     ✓ Child 1")
            await asyncio.sleep(0.05)

        with tracing.create_span("child_operation_2"):
            print("     ✓ Child 2")

            with tracing.create_span("grandchild_operation"):
                print("       ✓ Grandchild")
                await asyncio.sleep(0.03)

    print()

    # Error handling in traces
    print("5. Tracing with Error Handling:")
    print()

    try:
        with tracing.create_span("operation_with_error"):
            print("   ✓ Span created")
            await asyncio.sleep(0.02)
            raise ValueError("Simulated error for tracing demo")
    except ValueError:
        print("   ✓ Error recorded in span")

    print()


# ============================================================================
# DEMO 3: STRUCTURED LOGGING
# ============================================================================

async def demo_logging():
    """Demonstrate structured JSON logging"""
    print("=" * 70)
    print("DEMO 3: STRUCTURED LOGGING")
    print("=" * 70)
    print()

    logger = get_logger("circuit-os-demo")

    # Basic logging
    print("1. Basic Structured Logs:")
    print()

    logger.info("Application started", version="3.0.0", environment="demo")
    print("   ✓ Info log with context")

    logger.warning("High memory usage detected", memory_usage_mb=512, threshold_mb=400)
    print("   ✓ Warning log with metrics")

    print()

    # Circuit execution logs
    print("2. Circuit Execution Logs:")
    print()

    logger.log_circuit_execution(
        circuit_name="lead_processing",
        execution_id="exec_12345",
        status="success",
        duration=1.25,
        actions_count=8
    )
    print("   ✓ Circuit execution logged")

    logger.log_circuit_execution(
        circuit_name="data_sync",
        execution_id="exec_12346",
        status="error",
        duration=0.5,
        actions_count=3,
        error="Connection timeout"
    )
    print("   ✓ Failed circuit execution logged")

    print()

    # API request logs
    print("3. API Request Logs:")
    print()

    logger.log_api_request(
        method="POST",
        endpoint="/api/v1/execute",
        status_code=200,
        duration=1.15,
        user_id="user_123",
        request_id="req_abc123"
    )
    print("   ✓ Successful API request logged")

    logger.log_api_request(
        method="GET",
        endpoint="/api/v1/circuits",
        status_code=500,
        duration=0.05,
        user_id="user_456"
    )
    print("   ✓ Failed API request logged")

    print()

    # Security event logs
    print("4. Security Event Logs:")
    print()

    logger.log_security_event(
        event_type="login",
        user_id="user_123",
        email="user@example.com",
        status="success"
    )
    print("   ✓ Successful login logged")

    logger.log_security_event(
        event_type="login",
        email="hacker@example.com",
        status="failed",
        details={"reason": "invalid_password", "attempts": 3}
    )
    print("   ✓ Failed login logged")

    logger.log_security_event(
        event_type="injection_blocked",
        status="blocked",
        details={"attack_type": "sql", "payload": "'; DROP TABLE--"}
    )
    print("   ✓ Injection attack logged")

    print()

    # ML prediction logs
    print("5. ML Prediction Logs:")
    print()

    logger.log_ml_prediction(
        model_name="lead_scorer_v2",
        prediction_id="pred_789",
        confidence=0.92,
        duration=0.05,
        features_count=15
    )
    print("   ✓ ML prediction logged")

    print()

    # RAG query logs
    print("6. RAG Query Logs:")
    print()

    logger.log_rag_query(
        query="What are the best practices for implementing AI in enterprise?",
        documents_count=10,
        duration=0.35,
        query_id="rag_query_456"
    )
    print("   ✓ RAG query logged")

    print()

    # Error logs
    print("7. Error Logs:")
    print()

    logger.log_error(
        error_type="database_error",
        error_message="Connection refused",
        context={
            "database": "postgresql",
            "host": "localhost",
            "port": 5432
        }
    )
    print("   ✓ Error logged with context")

    try:
        1 / 0
    except Exception as e:
        logger.log_error(
            error_type="division_error",
            error_message="Division by zero",
            context={"operation": "calculation"},
            exception=e
        )
        print("   ✓ Error logged with exception")

    print()


# ============================================================================
# DEMO 4: DECORATOR USAGE
# ============================================================================

@track_circuit_execution("demo_circuit")
async def demo_circuit_with_metrics():
    """Circuit execution with automatic metrics"""
    await asyncio.sleep(0.5)
    return {"status": "success"}


@track_ml_prediction("demo_model")
async def demo_ml_prediction_with_metrics():
    """ML prediction with automatic metrics"""
    await asyncio.sleep(0.05)
    return {"confidence": 0.88}


@track_rag_query()
async def demo_rag_with_metrics():
    """RAG query with automatic metrics"""
    await asyncio.sleep(0.2)
    return [{"doc": "result1"}, {"doc": "result2"}]


@trace_span("demo_operation", attributes={"type": "test"})
async def demo_traced_operation():
    """Operation with automatic tracing"""
    await asyncio.sleep(0.1)
    return "completed"


async def demo_decorators():
    """Demonstrate decorator usage for observability"""
    print("=" * 70)
    print("DEMO 4: DECORATOR USAGE")
    print("=" * 70)
    print()

    logger = get_logger()

    # Track circuit execution
    print("1. Circuit Execution Decorator:")
    result = await demo_circuit_with_metrics()
    print(f"   ✓ Circuit executed with automatic metrics: {result['status']}")
    print()

    # Track ML prediction
    print("2. ML Prediction Decorator:")
    result = await demo_ml_prediction_with_metrics()
    print(f"   ✓ ML prediction with automatic metrics: {result['confidence']}")
    print()

    # Track RAG query
    print("3. RAG Query Decorator:")
    results = await demo_rag_with_metrics()
    print(f"   ✓ RAG query with automatic metrics: {len(results)} documents")
    print()

    # Trace operation
    print("4. Tracing Decorator:")
    result = await demo_traced_operation()
    print(f"   ✓ Operation traced automatically: {result}")
    print()


# ============================================================================
# DEMO 5: COMPLETE OBSERVABILITY FLOW
# ============================================================================

async def demo_complete_flow():
    """Demonstrate complete observability flow"""
    print("=" * 70)
    print("DEMO 5: COMPLETE OBSERVABILITY FLOW")
    print("=" * 70)
    print()

    metrics = get_metrics_collector()
    tracing = get_tracing_manager()
    logger = get_logger()

    print("Simulating Complete Request Flow:")
    print()

    # Incoming API request
    print("1. API Request Received")
    request_start = time.time()

    with tracing.trace_http_request("POST", "/api/v1/execute", "user_123"):
        metrics.increment_active_requests()

        logger.log_api_request(
            method="POST",
            endpoint="/api/v1/execute",
            status_code=200,
            user_id="user_123"
        )

        # Circuit execution
        print("2. Circuit Execution Started")
        with tracing.trace_circuit_execution("lead_processing", {"lead_id": "456"}):
            metrics.increment_active_circuits()

            circuit_start = time.time()

            # Action 1: RAG query
            print("3. RAG Query")
            with tracing.trace_rag_query("company intel", k=10):
                await asyncio.sleep(0.2)
                metrics.record_rag_query(0.2, 10)
                logger.log_rag_query("company intel", 10, 0.2)

            # Action 2: ML prediction
            print("4. ML Prediction")
            with tracing.trace_ml_prediction("lead_scorer", 15):
                await asyncio.sleep(0.05)
                metrics.record_ml_prediction("lead_scorer", 0.05, 0.89)
                logger.log_ml_prediction("lead_scorer", "pred_123", 0.89, 0.05, 15)

            # Action 3: Save result
            print("5. Save Result")
            await asyncio.sleep(0.1)

            circuit_duration = time.time() - circuit_start

            metrics.record_circuit_execution(
                "lead_processing",
                circuit_duration,
                "success",
                3
            )

            logger.log_circuit_execution(
                "lead_processing",
                "exec_789",
                "success",
                circuit_duration,
                3
            )

            metrics.decrement_active_circuits()

        request_duration = time.time() - request_start

        metrics.record_http_request(
            "POST",
            "/api/v1/execute",
            200,
            request_duration
        )

        metrics.decrement_active_requests()

    print()
    print("Complete Flow Summary:")
    print(f"   Total Duration: {request_duration:.3f}s")
    print(f"   Circuit Duration: {circuit_duration:.3f}s")
    print(f"   Actions Executed: 3")
    print(f"   RAG Documents: 10")
    print(f"   ML Confidence: 0.89")
    print()
    print("   ✓ Metrics recorded")
    print("   ✓ Traces generated")
    print("   ✓ Logs written")
    print()


# ============================================================================
# MAIN DEMO
# ============================================================================

async def main():
    """Run all observability demos"""
    print()
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 13 + "CIRCUIT OS - OBSERVABILITY LAYER DEMO" + " " * 18 + "║")
    print("║" + " " * 9 + "Prometheus + OpenTelemetry + Structured Logging" + " " * 11 + "║")
    print("╚" + "═" * 68 + "╝")
    print()

    await demo_metrics()
    await demo_tracing()
    await demo_logging()
    await demo_decorators()
    await demo_complete_flow()

    print("=" * 70)
    print("OBSERVABILITY LAYER DEMONSTRATION COMPLETE")
    print("=" * 70)
    print()
    print("Summary:")
    print("  ✓ Prometheus Metrics - 40+ metric types")
    print("  ✓ OpenTelemetry Tracing - Distributed tracing with nested spans")
    print("  ✓ Structured Logging - JSON formatted logs with full context")
    print("  ✓ Decorator Support - Automatic instrumentation")
    print("  ✓ Complete Integration - End-to-end observability")
    print()
    print("All observability components are production-ready!")
    print()
    print("Next Steps:")
    print("  1. View metrics: http://localhost:8000/metrics")
    print("  2. View logs: Check console or log files (JSON format)")
    print("  3. Import Grafana dashboard: monitoring/grafana_dashboard.json")
    print("  4. Configure alerts: monitoring/prometheus_alerts.yml")
    print()


if __name__ == "__main__":
    asyncio.run(main())
