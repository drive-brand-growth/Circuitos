"""
Main FastAPI application for Virtual AgentForce environment.
"""

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Dict, Any, List

from .data.database import get_session, init_database
from .core.agent import Agent, AgentConfig
from .core.atlas import AtlasEngine
from .core.actions import ActionExecutor, ActionType
from .data.soql import execute_soql

app = FastAPI(title="Virtual Salesforce AgentForce", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    init_database()


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "Virtual Salesforce AgentForce Environment",
        "version": "1.0.0",
        "status": "running",
    }


@app.post("/agents/execute")
async def execute_agent(
    config: Dict[str, Any],
    task: str,
    context: Dict[str, Any] = None,
    session: Session = Depends(get_session),
):
    """
    Execute an agent with a task.
    
    Args:
        config: Agent configuration
        task: Task description
        context: Optional context data
        
    Returns:
        Agent execution result
    """
    agent = Agent.from_config(config, session)
    result = await agent.execute(task, context)
    
    if not result.success:
        raise HTTPException(status_code=500, detail=result.error)
    
    return result.dict()


@app.post("/soql/query")
async def query_soql(
    query: str,
    session: Session = Depends(get_session),
):
    """
    Execute a SOQL query.
    
    Args:
        query: SOQL query string
        
    Returns:
        Query results
    """
    try:
        results = execute_soql(session, query)
        return {
            "success": True,
            "records": results,
            "count": len(results),
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/actions/execute")
async def execute_action(
    action_type: str,
    params: Dict[str, Any],
    session: Session = Depends(get_session),
):
    """
    Execute an action directly.
    
    Args:
        action_type: Type of action
        params: Action parameters
        
    Returns:
        Action result
    """
    try:
        executor = ActionExecutor(session)
        action_type_enum = ActionType(action_type)
        result = executor.execute(action_type_enum, params)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/atlas/reason")
async def reason_with_atlas(
    system_prompt: str,
    user_prompt: str,
    context: Dict[str, Any] = None,
):
    """
    Perform reasoning with Atlas engine.
    
    Args:
        system_prompt: System instructions
        user_prompt: User prompt
        context: Optional context
        
    Returns:
        Reasoning result
    """
    try:
        atlas = AtlasEngine()
        result = await atlas.reason(system_prompt, user_prompt, context)
        return result.dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/validation/backtest")
async def run_backtest(
    config: Dict[str, Any],
    backtest_type: str = "closed_won",
    days_back: int = 180,
    min_amount: float = 50000,
    session: Session = Depends(get_session),
):
    """
    Run a backtest on an agent.
    
    Args:
        config: Agent configuration
        backtest_type: Type of backtest ('closed_won' or 'loss_reason')
        days_back: Days to look back
        min_amount: Minimum opportunity amount
        
    Returns:
        Backtest results
    """
    from .validation import BacktestRunner
    from .core.agent import Agent
    
    try:
        agent = Agent.from_config(config, session)
        runner = BacktestRunner(agent, session)
        
        if backtest_type == "closed_won":
            result = await runner.backtest_closed_won(days_back=days_back, min_amount=min_amount)
        elif backtest_type == "loss_reason":
            result = await runner.backtest_loss_reason_detection(days_back=days_back)
        else:
            raise HTTPException(status_code=400, detail=f"Unknown backtest type: {backtest_type}")
        
        return {
            "success": True,
            "accuracy": result.accuracy,
            "precision": result.precision,
            "recall": result.recall,
            "f1_score": result.f1_score,
            "tier_distribution": result.tier_distribution,
            "details": result.details[:10],  # Limit details for response size
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/validation/validate-config")
async def validate_config(config: Dict[str, Any]):
    """
    Validate agent configuration.
    
    Args:
        config: Agent configuration
        
    Returns:
        Validation result
    """
    from .validation import AgentValidator
    from .data.database import SessionLocal
    
    try:
        session = SessionLocal()
        validator = AgentValidator(session)
        result = validator.validate_config(config)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

