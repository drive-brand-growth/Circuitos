"""
Circuit OS - Complete FastAPI Application
REST API with Security + Observability (Metrics, Tracing, Logging)
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
from datetime import datetime
import time
import logging

from circuit_engine import (
    CircuitScriptEngine,
    CircuitContext,
    TriggerEvent,
)
from examples import (
    create_lead_processing_circuit,
    create_hot_lead_alert_circuit,
    create_competitor_intel_circuit,
    create_simple_data_circuit,
)

# Security imports
from security import (
    get_authenticator,
    get_current_user,
    User,
    LoginRequest,
    TokenResponse,
    Permission,
    Role,
    get_rbac_manager,
    require_permission,
    require_role,
    RateLimitMiddleware,
    get_rate_limiter,
    validate_circuit_data,
    validate_and_sanitize_request,
)

# Observability imports
from observability import (
    get_metrics_collector,
    get_tracing_manager,
    get_logger,
)

# Configure logging
structured_logger = get_logger("circuit-os-api")

#Configure root logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(
    title="Circuit OS API - Complete",
    description="Salesforce Apex + AI with Security & Observability",
    version="3.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add Rate Limiting middleware
app.add_middleware(RateLimitMiddleware)

# Initialize components
engine = CircuitScriptEngine()
authenticator = get_authenticator()
rbac_manager = get_rbac_manager()
rate_limiter = get_rate_limiter()
metrics = get_metrics_collector()
tracing = get_tracing_manager()

# Execution history
execution_history: List[Dict] = []


# ============================================================================
# MIDDLEWARE FOR METRICS & TRACING
# ============================================================================

@app.middleware("http")
async def observability_middleware(request: Request, call_next):
    """Add metrics and tracing to all requests"""
    start_time = time.time()

    # Start tracing span
    method = request.method
    endpoint = request.url.path

    # Extract user info if available
    user_id = None
    try:
        auth_header = request.headers.get("authorization")
        if auth_header:
            from security.auth import verify_access_token
            token = auth_header.replace("Bearer ", "")
            token_payload = verify_access_token(token)
            if token_payload:
                user_id = token_payload.sub
    except:
        pass

    # Increment active requests metric
    metrics.increment_active_requests()

    try:
        # Process request
        response = await call_next(request)

        # Record metrics
        duration = time.time() - start_time
        status_code = response.status_code

        metrics.record_http_request(
            method=method,
            endpoint=endpoint,
            status_code=status_code,
            duration=duration
        )

        # Log request
        structured_logger.log_api_request(
            method=method,
            endpoint=endpoint,
            status_code=status_code,
            duration=duration,
            user_id=user_id
        )

        return response

    except Exception as e:
        duration = time.time() - start_time

        # Record error metrics
        metrics.record_http_request(
            method=method,
            endpoint=endpoint,
            status_code=500,
            duration=duration
        )

        # Log error
        structured_logger.log_error(
            error_type="http_request_error",
            error_message=str(e),
            context={
                "method": method,
                "endpoint": endpoint,
                "user_id": user_id
            }
        )

        raise

    finally:
        metrics.decrement_active_requests()


# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class ExecuteCircuitRequestAPI(BaseModel):
    """API request to execute a circuit"""
    circuit_name: str
    data: Dict[str, Any]
    check_triggers: bool = True


class PublishEventRequest(BaseModel):
    """Request to publish an event"""
    event: str
    data: Dict[str, Any]


class CircuitResponse(BaseModel):
    """Circuit information response"""
    name: str
    description: str
    enabled: bool
    trigger_count: int
    action_count: int
    triggers: List[Dict]
    actions: List[Dict]


class ExecutionResponse(BaseModel):
    """Circuit execution response"""
    execution_id: str
    circuit_name: str
    status: str
    duration: Optional[float] = None
    actions_executed: List[Dict]
    errors: List[Dict]
    data: Dict[str, Any]


class MetricsResponse(BaseModel):
    """Engine metrics response"""
    total_executions: int
    successful_executions: int
    failed_executions: int
    average_duration: float
    success_rate: float
    registered_circuits: int
    total_triggers: int
    total_actions: int


# ============================================================================
# STARTUP/SHUTDOWN
# ============================================================================

@app.on_event("startup")
async def startup():
    """Initialize everything"""
    logger.info("Starting Circuit OS API - Complete (Security + Observability)...")

    # Register circuits
    engine.register(create_lead_processing_circuit())
    engine.register(create_hot_lead_alert_circuit())
    engine.register(create_competitor_intel_circuit())
    engine.register(create_simple_data_circuit())

    logger.info(f"Registered {len(engine.list())} circuits")

    # Start engine
    await engine.start()

    # Start rate limiter cleanup
    rate_limiter.start_cleanup_task()

    # Set system info metrics
    metrics.set_system_info({
        "version": "3.0.0",
        "environment": "development",
        "python_version": "3.11"
    })

    metrics.set_circuits_registered(len(engine.list()))

    structured_logger.info("Circuit OS API started successfully",
        version="3.0.0",
        circuits_registered=len(engine.list()),
        security_enabled=True,
        observability_enabled=True
    )


@app.on_event("shutdown")
async def shutdown():
    """Shutdown everything"""
    logger.info("Shutting down Circuit OS API...")
    await engine.stop()
    structured_logger.info("Circuit OS API shutdown complete")


# ============================================================================
# PROMETHEUS METRICS ENDPOINT
# ============================================================================

@app.get("/metrics")
async def prometheus_metrics():
    """Prometheus metrics endpoint"""
    return Response(
        content=metrics.generate_metrics(),
        media_type=metrics.get_content_type()
    )


# ============================================================================
# AUTHENTICATION ENDPOINTS
# ============================================================================

@app.post("/api/v1/auth/login", response_model=TokenResponse)
async def login(request: LoginRequest):
    """Login and get JWT access token"""
    try:
        with tracing.trace_authentication(request.email):
            result = await authenticator.login(request.email, request.password)

            # Record metrics
            metrics.record_auth_attempt("success")

            # Log event
            structured_logger.log_security_event(
                event_type="login",
                email=request.email,
                status="success"
            )

            return result

    except HTTPException as e:
        metrics.record_auth_attempt("failed")

        structured_logger.log_security_event(
            event_type="login",
            email=request.email,
            status="failed"
        )

        raise


@app.get("/api/v1/auth/me")
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user information"""
    return {
        "user_id": current_user.user_id,
        "email": current_user.email,
        "username": current_user.username,
        "roles": current_user.roles,
        "is_active": current_user.is_active,
        "permissions": [p.value for p in rbac_manager.get_user_permissions(current_user.roles)]
    }


# ============================================================================
# HEALTH & STATUS
# ============================================================================

@app.get("/")
async def root():
    """API root"""
    return {
        "name": "Circuit OS API - Complete",
        "version": "3.0.0",
        "status": "running",
        "description": "Salesforce Apex + AI with Security & Observability",
        "circuits": len(engine.list()),
        "docs": "/docs",
        "features": {
            "security": ["JWT", "RBAC", "Rate Limiting", "Input Validation"],
            "observability": ["Prometheus Metrics", "OpenTelemetry Tracing", "Structured Logging"],
            "intelligence": ["Adaptive RAG", "AutoML", "Knowledge Graph"]
        }
    }


@app.get("/health")
async def health():
    """Health check"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "engine_running": engine.running,
        "circuits_registered": len(engine.list()),
        "metrics_enabled": True,
        "tracing_enabled": True
    }


# ============================================================================
# CIRCUIT MANAGEMENT (Protected)
# ============================================================================

@app.get("/api/v1/circuits", response_model=List[CircuitResponse])
async def list_circuits(
    current_user: User = Depends(require_permission(Permission.CIRCUIT_READ))
):
    """List all registered circuits"""
    circuits = engine.list_circuits()
    return [CircuitResponse(**circuit) for circuit in circuits]


@app.get("/api/v1/circuits/{circuit_name}", response_model=CircuitResponse)
async def get_circuit(
    circuit_name: str,
    current_user: User = Depends(require_permission(Permission.CIRCUIT_READ))
):
    """Get circuit details"""
    circuit = engine.get(circuit_name)

    if not circuit:
        raise HTTPException(status_code=404, detail=f"Circuit {circuit_name} not found")

    return CircuitResponse(**circuit.to_dict())


# ============================================================================
# CIRCUIT EXECUTION (Protected + Instrumented)
# ============================================================================

@app.post("/api/v1/execute", response_model=ExecutionResponse)
async def execute_circuit(
    request: ExecuteCircuitRequestAPI,
    current_user: User = Depends(require_permission(Permission.CIRCUIT_EXECUTE))
):
    """Execute a circuit with full observability"""
    start_time = time.time()

    try:
        # Validate input
        validated_data = validate_circuit_data(request.circuit_name, request.data)

        # Start tracing span
        with tracing.trace_circuit_execution(request.circuit_name, validated_data):
            # Increment active circuits
            metrics.increment_active_circuits()

            try:
                # Execute circuit
                context = await engine.execute_circuit(
                    request.circuit_name,
                    validated_data,
                    request.check_triggers
                )

                metadata = context.get_metadata()
                duration = time.time() - start_time

                # Build response
                response = ExecutionResponse(
                    execution_id=metadata.get("execution_id", "unknown"),
                    circuit_name=request.circuit_name,
                    status=metadata.get("status", "unknown"),
                    duration=duration,
                    actions_executed=metadata.get("actions_executed", []),
                    errors=metadata.get("errors", []),
                    data=context.get_all()
                )

                # Record metrics
                metrics.record_circuit_execution(
                    circuit_name=request.circuit_name,
                    duration=duration,
                    status=response.status,
                    actions_count=len(response.actions_executed)
                )

                # Log execution
                structured_logger.log_circuit_execution(
                    circuit_name=request.circuit_name,
                    execution_id=response.execution_id,
                    status=response.status,
                    duration=duration,
                    actions_count=len(response.actions_executed)
                )

                # Store in history
                execution_history.append({
                    **response.dict(),
                    "executed_by": current_user.email,
                    "executed_at": datetime.now().isoformat()
                })

                return response

            finally:
                metrics.decrement_active_circuits()

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        duration = time.time() - start_time

        # Record error metrics
        metrics.record_circuit_execution(
            circuit_name=request.circuit_name,
            duration=duration,
            status="error",
            actions_count=0,
            error_type=type(e).__name__
        )

        # Log error
        structured_logger.log_error(
            error_type="circuit_execution_error",
            error_message=str(e),
            context={
                "circuit_name": request.circuit_name,
                "user": current_user.email
            },
            exception=e
        )

        raise HTTPException(status_code=500, detail=f"Execution failed: {str(e)}")


@app.post("/api/v1/events/publish")
async def publish_event(
    request: PublishEventRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(require_permission(Permission.CIRCUIT_EXECUTE))
):
    """Publish an event to trigger circuits"""
    try:
        validated_data = validate_and_sanitize_request(request.data)
        event = TriggerEvent(request.event)

        triggered_circuits = await engine.publish_event(event, validated_data)

        structured_logger.info(
            f"Event published: {request.event}",
            event=request.event,
            triggered_circuits=len(triggered_circuits),
            user=current_user.email
        )

        return {
            "status": "published",
            "event": request.event,
            "triggered_circuits": triggered_circuits,
            "count": len(triggered_circuits),
            "published_by": current_user.email
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid event: {str(e)}")
    except Exception as e:
        logger.error(f"Event publishing error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to publish event: {str(e)}")


# ============================================================================
# EXECUTION HISTORY (Protected)
# ============================================================================

@app.get("/api/v1/executions")
async def get_executions(
    limit: int = 50,
    offset: int = 0,
    current_user: User = Depends(require_permission(Permission.CIRCUIT_READ))
):
    """Get execution history"""
    total = len(execution_history)
    results = execution_history[offset:offset + limit]

    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "results": results
    }


# ============================================================================
# METRICS (Protected)
# ============================================================================

@app.get("/api/v1/metrics/engine", response_model=MetricsResponse)
async def get_engine_metrics(
    current_user: User = Depends(require_permission(Permission.METRICS_READ))
):
    """Get engine metrics"""
    engine_metrics = engine.get_metrics()
    return MetricsResponse(**engine_metrics)


@app.get("/api/v1/metrics/observability")
async def get_observability_stats(
    current_user: User = Depends(require_permission(Permission.METRICS_READ))
):
    """Get observability statistics"""
    return {
        "rate_limiter": rate_limiter.get_statistics(),
        "system": {
            "circuits_registered": len(engine.list()),
            "active_sessions": len(authenticator.users)
        }
    }


# ============================================================================
# ADMIN ENDPOINTS (Admin Only)
# ============================================================================

@app.get("/api/v1/admin/users")
async def list_users(
    current_user: User = Depends(require_role(Role.ADMIN))
):
    """List all users"""
    return {
        "total": len(authenticator.users),
        "users": [
            {
                "user_id": user_data["user_id"],
                "email": email,
                "username": user_data["username"],
                "roles": user_data["roles"],
                "is_active": user_data["is_active"]
            }
            for email, user_data in authenticator.users.items()
        ]
    }


# ============================================================================
# DEMO ENDPOINTS (Protected)
# ============================================================================

@app.post("/api/v1/demo/lead-processing")
async def demo_lead_processing(
    current_user: User = Depends(require_permission(Permission.CIRCUIT_EXECUTE))
):
    """Demo: Process a lead with full AI pipeline"""
    data = {
        "lead_id": f"demo_lead_{datetime.now().timestamp()}",
        "status": "New"
    }

    context = await engine.execute_circuit("lead_processing_ai", data)

    return {
        "demo": "Lead Processing Circuit",
        "status": context.get_metadata().get("status"),
        "lead_score": context.get("lead_score"),
        "opportunity_created": context.get("opportunity_id") is not None,
        "executed_by": current_user.email
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
