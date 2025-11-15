"""
Circuit OS - FastAPI Application
REST API for Circuit Script execution and management
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
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

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(
    title="Circuit OS API",
    description="Salesforce Apex + AI Native Operations",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Circuit Engine
engine = CircuitScriptEngine()

# Execution history (in-memory for demo, use database in production)
execution_history: List[Dict] = []


# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class ExecuteCircuitRequest(BaseModel):
    """Request to execute a circuit"""
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


# ============================================================================
# STARTUP/SHUTDOWN
# ============================================================================

@app.on_event("startup")
async def startup():
    """Initialize engine and register circuits"""
    logger.info("Starting Circuit OS API...")

    # Register example circuits
    engine.register(create_lead_processing_circuit())
    engine.register(create_hot_lead_alert_circuit())
    engine.register(create_competitor_intel_circuit())
    engine.register(create_simple_data_circuit())

    logger.info(f"Registered {len(engine.list())} circuits")

    # Start engine
    await engine.start()
    logger.info("Circuit OS API started successfully")


@app.on_event("shutdown")
async def shutdown():
    """Shutdown engine"""
    logger.info("Shutting down Circuit OS API...")
    await engine.stop()


# ============================================================================
# HEALTH & STATUS
# ============================================================================

@app.get("/")
async def root():
    """API root"""
    return {
        "name": "Circuit OS API",
        "version": "1.0.0",
        "status": "running",
        "description": "Salesforce Apex + AI Native Operations",
        "circuits": len(engine.list()),
        "docs": "/docs"
    }


@app.get("/health")
async def health():
    """Health check"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "engine_running": engine.running,
        "circuits_registered": len(engine.list())
    }


# ============================================================================
# CIRCUIT MANAGEMENT
# ============================================================================

@app.get("/api/v1/circuits", response_model=List[CircuitResponse])
async def list_circuits():
    """List all registered circuits"""
    circuits = engine.list_circuits()
    return [CircuitResponse(**circuit) for circuit in circuits]


@app.get("/api/v1/circuits/{circuit_name}", response_model=CircuitResponse)
async def get_circuit(circuit_name: str):
    """Get circuit details"""
    circuit = engine.get(circuit_name)

    if not circuit:
        raise HTTPException(status_code=404, detail=f"Circuit {circuit_name} not found")

    return CircuitResponse(**circuit.to_dict())


@app.post("/api/v1/circuits/{circuit_name}/enable")
async def enable_circuit(circuit_name: str):
    """Enable a circuit"""
    circuit = engine.get(circuit_name)

    if not circuit:
        raise HTTPException(status_code=404, detail=f"Circuit {circuit_name} not found")

    circuit.enable()
    return {"status": "enabled", "circuit_name": circuit_name}


@app.post("/api/v1/circuits/{circuit_name}/disable")
async def disable_circuit(circuit_name: str):
    """Disable a circuit"""
    circuit = engine.get(circuit_name)

    if not circuit:
        raise HTTPException(status_code=404, detail=f"Circuit {circuit_name} not found")

    circuit.disable()
    return {"status": "disabled", "circuit_name": circuit_name}


# ============================================================================
# CIRCUIT EXECUTION
# ============================================================================

@app.post("/api/v1/execute", response_model=ExecutionResponse)
async def execute_circuit(request: ExecuteCircuitRequest):
    """
    Execute a circuit

    Example:
    ```
    POST /api/v1/execute
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
        # Execute circuit
        context = await engine.execute_circuit(
            request.circuit_name,
            request.data,
            request.check_triggers
        )

        metadata = context.get_metadata()

        # Build response
        response = ExecutionResponse(
            execution_id=metadata.get("execution_id", "unknown"),
            circuit_name=request.circuit_name,
            status=metadata.get("status", "unknown"),
            duration=None,  # Calculate from metadata
            actions_executed=metadata.get("actions_executed", []),
            errors=metadata.get("errors", []),
            data=context.get_all()
        )

        # Store in history
        execution_history.append(response.dict())

        return response

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Execution error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Execution failed: {str(e)}")


@app.post("/api/v1/events/publish")
async def publish_event(request: PublishEventRequest, background_tasks: BackgroundTasks):
    """
    Publish an event to trigger circuits

    Example:
    ```
    POST /api/v1/events/publish
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
        # Parse event
        event = TriggerEvent(request.event)

        # Publish event (queues circuits for execution)
        triggered_circuits = await engine.publish_event(event, request.data)

        return {
            "status": "published",
            "event": request.event,
            "triggered_circuits": triggered_circuits,
            "count": len(triggered_circuits)
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid event: {str(e)}")
    except Exception as e:
        logger.error(f"Event publishing error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to publish event: {str(e)}")


# ============================================================================
# EXECUTION HISTORY
# ============================================================================

@app.get("/api/v1/executions")
async def get_executions(limit: int = 50, offset: int = 0):
    """Get execution history"""
    total = len(execution_history)
    results = execution_history[offset:offset + limit]

    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "results": results
    }


@app.get("/api/v1/executions/{execution_id}")
async def get_execution(execution_id: str):
    """Get specific execution details"""
    for execution in execution_history:
        if execution.get("execution_id") == execution_id:
            return execution

    raise HTTPException(status_code=404, detail=f"Execution {execution_id} not found")


# ============================================================================
# METRICS
# ============================================================================

@app.get("/api/v1/metrics", response_model=MetricsResponse)
async def get_metrics():
    """Get engine metrics"""
    metrics = engine.get_metrics()
    return MetricsResponse(**metrics)


@app.post("/api/v1/metrics/reset")
async def reset_metrics():
    """Reset metrics"""
    engine.reset_metrics()
    return {"status": "reset", "timestamp": datetime.now().isoformat()}


# ============================================================================
# TRIGGER EVENTS (Reference)
# ============================================================================

@app.get("/api/v1/events")
async def list_events():
    """List all available trigger events"""
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
# DEMO ENDPOINTS
# ============================================================================

@app.post("/api/v1/demo/lead-processing")
async def demo_lead_processing():
    """
    Demo: Process a lead with full AI pipeline
    """
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
        "intelligence_documents": len(context.get("company_intelligence", [])),
        "competitors_found": len(context.get("competitors", [])),
        "execution_summary": context.get_metadata().get("execution_summary")
    }


@app.post("/api/v1/demo/hot-lead")
async def demo_hot_lead():
    """
    Demo: Hot lead alert
    """
    data = {
        "lead_id": f"demo_hot_lead_{datetime.now().timestamp()}",
        "lead_score": 95
    }

    context = await engine.execute_circuit("hot_lead_alert", data)

    return {
        "demo": "Hot Lead Alert Circuit",
        "status": context.get_metadata().get("status"),
        "slack_alert_sent": context.get("slack_notification_sent"),
        "opportunity_id": context.get("opportunity_id")
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
