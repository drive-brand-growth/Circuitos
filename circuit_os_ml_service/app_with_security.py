"""
Circuit OS - FastAPI Application with Security
REST API with JWT, RBAC, Rate Limiting, and Input Validation
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
from datetime import datetime
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
    # Authentication
    JWTAuthenticator,
    get_authenticator,
    get_current_user,
    User,
    LoginRequest,
    TokenResponse,

    # Authorization
    Permission,
    Role,
    get_rbac_manager,
    require_permission,
    require_role,

    # Rate Limiting
    RateLimitMiddleware,
    get_rate_limiter,
    rate_limit,

    # Validation
    CircuitRequestValidator,
    validate_circuit_data,
    validate_and_sanitize_request,
    CircuitExecutionRequest,
    RAGQueryRequest,
    MLPredictionRequest,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(
    title="Circuit OS API",
    description="Salesforce Apex + AI Native Operations with Security",
    version="2.0.0",
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

# Initialize Circuit Engine
engine = CircuitScriptEngine()

# Initialize Security
authenticator = get_authenticator()
rbac_manager = get_rbac_manager()
rate_limiter = get_rate_limiter()
validator = CircuitRequestValidator()

# Execution history (in-memory for demo, use database in production)
execution_history: List[Dict] = []


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
    event: str  # TriggerEvent value
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


class SecurityStatusResponse(BaseModel):
    """Security status response"""
    authentication: str
    authorization: str
    rate_limiting: str
    input_validation: str
    total_users: int
    total_roles: int


# ============================================================================
# STARTUP/SHUTDOWN
# ============================================================================

@app.on_event("startup")
async def startup():
    """Initialize engine and register circuits"""
    logger.info("Starting Circuit OS API with Security...")

    # Register example circuits
    engine.register(create_lead_processing_circuit())
    engine.register(create_hot_lead_alert_circuit())
    engine.register(create_competitor_intel_circuit())
    engine.register(create_simple_data_circuit())

    logger.info(f"Registered {len(engine.list())} circuits")

    # Set circuit whitelist for validation
    circuit_names = [c.name for c in engine.list()]
    validator.set_allowed_circuits(circuit_names)

    # Start engine
    await engine.start()

    # Start rate limiter cleanup
    rate_limiter.start_cleanup_task()

    logger.info("Circuit OS API started successfully with security enabled")


@app.on_event("shutdown")
async def shutdown():
    """Shutdown engine"""
    logger.info("Shutting down Circuit OS API...")
    await engine.stop()


# ============================================================================
# AUTHENTICATION ENDPOINTS
# ============================================================================

@app.post("/api/v1/auth/login", response_model=TokenResponse)
async def login(request: LoginRequest):
    """
    Login and get JWT access token

    Default users:
    - admin@circuitos.com / admin123 (admin role)
    - developer@circuitos.com / dev123 (developer role)
    - viewer@circuitos.com / view123 (viewer role)
    """
    return await authenticator.login(request.email, request.password)


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
# HEALTH & STATUS (Public)
# ============================================================================

@app.get("/")
async def root():
    """API root (public)"""
    return {
        "name": "Circuit OS API",
        "version": "2.0.0",
        "status": "running",
        "description": "Salesforce Apex + AI Native Operations with Security",
        "circuits": len(engine.list()),
        "docs": "/docs",
        "security": {
            "authentication": "JWT",
            "authorization": "RBAC",
            "rate_limiting": "Token Bucket"
        }
    }


@app.get("/health")
async def health():
    """Health check (public)"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "engine_running": engine.running,
        "circuits_registered": len(engine.list())
    }


@app.get("/api/v1/security/status")
async def security_status(
    current_user: User = Depends(require_permission(Permission.CONFIG_READ))
):
    """Get security system status (requires CONFIG_READ permission)"""
    return SecurityStatusResponse(
        authentication="JWT (HS256)",
        authorization="RBAC (6 roles, 18 permissions)",
        rate_limiting="Token Bucket (per-user, per-IP, global)",
        input_validation="Injection detection + sanitization",
        total_users=len(authenticator.users),
        total_roles=len(Role)
    )


# ============================================================================
# CIRCUIT MANAGEMENT (Protected)
# ============================================================================

@app.get("/api/v1/circuits", response_model=List[CircuitResponse])
async def list_circuits(
    current_user: User = Depends(require_permission(Permission.CIRCUIT_READ))
):
    """List all registered circuits (requires CIRCUIT_READ permission)"""
    circuits = engine.list_circuits()
    return [CircuitResponse(**circuit) for circuit in circuits]


@app.get("/api/v1/circuits/{circuit_name}", response_model=CircuitResponse)
async def get_circuit(
    circuit_name: str,
    current_user: User = Depends(require_permission(Permission.CIRCUIT_READ))
):
    """Get circuit details (requires CIRCUIT_READ permission)"""
    circuit = engine.get(circuit_name)

    if not circuit:
        raise HTTPException(status_code=404, detail=f"Circuit {circuit_name} not found")

    return CircuitResponse(**circuit.to_dict())


@app.post("/api/v1/circuits/{circuit_name}/enable")
async def enable_circuit(
    circuit_name: str,
    current_user: User = Depends(require_permission(Permission.CIRCUIT_UPDATE))
):
    """Enable a circuit (requires CIRCUIT_UPDATE permission)"""
    circuit = engine.get(circuit_name)

    if not circuit:
        raise HTTPException(status_code=404, detail=f"Circuit {circuit_name} not found")

    circuit.enable()
    logger.info(f"Circuit enabled by {current_user.email}: {circuit_name}")

    return {"status": "enabled", "circuit_name": circuit_name}


@app.post("/api/v1/circuits/{circuit_name}/disable")
async def disable_circuit(
    circuit_name: str,
    current_user: User = Depends(require_permission(Permission.CIRCUIT_UPDATE))
):
    """Disable a circuit (requires CIRCUIT_UPDATE permission)"""
    circuit = engine.get(circuit_name)

    if not circuit:
        raise HTTPException(status_code=404, detail=f"Circuit {circuit_name} not found")

    circuit.disable()
    logger.info(f"Circuit disabled by {current_user.email}: {circuit_name}")

    return {"status": "disabled", "circuit_name": circuit_name}


# ============================================================================
# CIRCUIT EXECUTION (Protected + Validated)
# ============================================================================

@app.post("/api/v1/execute", response_model=ExecutionResponse)
async def execute_circuit(
    request: ExecuteCircuitRequestAPI,
    current_user: User = Depends(require_permission(Permission.CIRCUIT_EXECUTE))
):
    """
    Execute a circuit (requires CIRCUIT_EXECUTE permission)

    All inputs are validated and sanitized

    Example:
    ```
    POST /api/v1/execute
    Headers: Authorization: Bearer <token>
    {
        "circuit_name": "lead_processing_ai",
        "data": {
            "lead_id": "lead_12345"
        },
        "check_triggers": true
    }
    ```
    """
    try:
        # Validate and sanitize input
        validated_data = validate_circuit_data(request.circuit_name, request.data)

        # Execute circuit
        context = await engine.execute_circuit(
            request.circuit_name,
            validated_data,
            request.check_triggers
        )

        metadata = context.get_metadata()

        # Build response
        response = ExecutionResponse(
            execution_id=metadata.get("execution_id", "unknown"),
            circuit_name=request.circuit_name,
            status=metadata.get("status", "unknown"),
            duration=None,
            actions_executed=metadata.get("actions_executed", []),
            errors=metadata.get("errors", []),
            data=context.get_all()
        )

        # Store in history
        execution_history.append({
            **response.dict(),
            "executed_by": current_user.email,
            "executed_at": datetime.now().isoformat()
        })

        logger.info(f"Circuit executed by {current_user.email}: {request.circuit_name}")

        return response

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Execution error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Execution failed: {str(e)}")


@app.post("/api/v1/events/publish")
async def publish_event(
    request: PublishEventRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(require_permission(Permission.CIRCUIT_EXECUTE))
):
    """
    Publish an event to trigger circuits (requires CIRCUIT_EXECUTE permission)

    Example:
    ```
    POST /api/v1/events/publish
    Headers: Authorization: Bearer <token>
    {
        "event": "lead.created",
        "data": {
            "lead_id": "lead_12345",
            "status": "New"
        }
    }
    ```
    """
    try:
        # Validate and sanitize data
        validated_data = validate_and_sanitize_request(request.data)

        # Parse event
        event = TriggerEvent(request.event)

        # Publish event
        triggered_circuits = await engine.publish_event(event, validated_data)

        logger.info(f"Event published by {current_user.email}: {request.event}")

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
    """Get execution history (requires CIRCUIT_READ permission)"""
    total = len(execution_history)
    results = execution_history[offset:offset + limit]

    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "results": results
    }


@app.get("/api/v1/executions/{execution_id}")
async def get_execution(
    execution_id: str,
    current_user: User = Depends(require_permission(Permission.CIRCUIT_READ))
):
    """Get specific execution details (requires CIRCUIT_READ permission)"""
    for execution in execution_history:
        if execution.get("execution_id") == execution_id:
            return execution

    raise HTTPException(status_code=404, detail=f"Execution {execution_id} not found")


# ============================================================================
# METRICS (Protected)
# ============================================================================

@app.get("/api/v1/metrics", response_model=MetricsResponse)
async def get_metrics(
    current_user: User = Depends(require_permission(Permission.METRICS_READ))
):
    """Get engine metrics (requires METRICS_READ permission)"""
    metrics = engine.get_metrics()
    return MetricsResponse(**metrics)


@app.get("/api/v1/metrics/rate-limiter")
async def get_rate_limiter_metrics(
    current_user: User = Depends(require_permission(Permission.METRICS_READ))
):
    """Get rate limiter metrics (requires METRICS_READ permission)"""
    return rate_limiter.get_statistics()


@app.post("/api/v1/metrics/reset")
async def reset_metrics(
    current_user: User = Depends(require_role(Role.ADMIN))
):
    """Reset metrics (requires ADMIN role)"""
    engine.reset_metrics()
    logger.info(f"Metrics reset by {current_user.email}")

    return {
        "status": "reset",
        "timestamp": datetime.now().isoformat(),
        "reset_by": current_user.email
    }


# ============================================================================
# TRIGGER EVENTS (Protected)
# ============================================================================

@app.get("/api/v1/events")
async def list_events(
    current_user: User = Depends(require_permission(Permission.CIRCUIT_READ))
):
    """List all available trigger events (requires CIRCUIT_READ permission)"""
    events = [
        {
            "name": event.name,
            "value": event.value,
            "category": event.value.split(".")[0]
        }
        for event in TriggerEvent
    ]

    # Group by category
    categories = {}
    for event in events:
        category = event["category"]
        if category not in categories:
            categories[category] = []
        categories[category].append(event)

    return {
        "total": len(events),
        "events": events,
        "by_category": categories
    }


# ============================================================================
# DEMO ENDPOINTS (Protected)
# ============================================================================

@app.post("/api/v1/demo/lead-processing")
async def demo_lead_processing(
    current_user: User = Depends(require_permission(Permission.CIRCUIT_EXECUTE))
):
    """
    Demo: Process a lead with full AI pipeline (requires CIRCUIT_EXECUTE permission)
    """
    data = {
        "lead_id": f"demo_lead_{datetime.now().timestamp()}",
        "status": "New"
    }

    context = await engine.execute_circuit("lead_processing_ai", data)

    logger.info(f"Demo lead processing executed by {current_user.email}")

    return {
        "demo": "Lead Processing Circuit",
        "status": context.get_metadata().get("status"),
        "lead_score": context.get("lead_score"),
        "opportunity_created": context.get("opportunity_id") is not None,
        "intelligence_documents": len(context.get("company_intelligence", [])),
        "competitors_found": len(context.get("competitors", [])),
        "execution_summary": context.get_metadata().get("execution_summary"),
        "executed_by": current_user.email
    }


@app.post("/api/v1/demo/hot-lead")
async def demo_hot_lead(
    current_user: User = Depends(require_permission(Permission.CIRCUIT_EXECUTE))
):
    """
    Demo: Hot lead alert (requires CIRCUIT_EXECUTE permission)
    """
    data = {
        "lead_id": f"demo_hot_lead_{datetime.now().timestamp()}",
        "lead_score": 95
    }

    context = await engine.execute_circuit("hot_lead_alert", data)

    logger.info(f"Demo hot lead executed by {current_user.email}")

    return {
        "demo": "Hot Lead Alert Circuit",
        "status": context.get_metadata().get("status"),
        "slack_alert_sent": context.get("slack_notification_sent"),
        "opportunity_id": context.get("opportunity_id"),
        "executed_by": current_user.email
    }


# ============================================================================
# ADMIN ENDPOINTS (Admin Only)
# ============================================================================

@app.get("/api/v1/admin/users")
async def list_users(
    current_user: User = Depends(require_role(Role.ADMIN))
):
    """List all users (requires ADMIN role)"""
    return {
        "total": len(authenticator.users),
        "users": [
            {
                "user_id": user_data["user_id"],
                "email": email,
                "username": user_data["username"],
                "roles": user_data["roles"],
                "is_active": user_data["is_active"],
                "created_at": user_data.get("created_at")
            }
            for email, user_data in authenticator.users.items()
        ]
    }


@app.get("/api/v1/admin/permissions")
async def list_permissions(
    current_user: User = Depends(require_role(Role.ADMIN))
):
    """List all permissions and role mappings (requires ADMIN role)"""
    from security.rbac import ROLE_PERMISSIONS

    return {
        "total_permissions": len(Permission),
        "total_roles": len(Role),
        "permissions": [p.value for p in Permission],
        "roles": {
            role.value: [p.value for p in perms]
            for role, perms in ROLE_PERMISSIONS.items()
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
