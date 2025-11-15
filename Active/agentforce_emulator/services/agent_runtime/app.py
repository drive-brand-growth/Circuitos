"""Agent runtime FastAPI application."""

from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

from .database import get_session, init_db, lifespan as db_lifespan
from .orchestrator import LostOpportunityOrchestrator
from .routers import runs
from .schemas import AgentRunRequest, AgentRunResponse


@asynccontextmanager
async def lifespan(app: FastAPI):  # type: ignore[reportAny]
    await init_db()
    orchestrator = LostOpportunityOrchestrator()
    app.state.orchestrator = orchestrator
    async with db_lifespan(app):
        try:
            yield
        finally:
            await orchestrator.signal_cache.close()


def get_orchestrator(request: Request) -> LostOpportunityOrchestrator:
    return request.app.state.orchestrator


def create_app() -> FastAPI:
    app = FastAPI(title="Agentforce Emulator Runtime", version="0.1.0", lifespan=lifespan)

    app.include_router(runs.router)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.post("/api/v1/agents/lost-opportunity/run", response_model=AgentRunResponse)
    async def run_lost_opportunity_agent(
        request: AgentRunRequest,
        orchestrator: LostOpportunityOrchestrator = Depends(get_orchestrator),
        session: AsyncSession = Depends(get_session),
    ) -> AgentRunResponse:
        return await orchestrator.run(request, session=session)

    @app.get("/health", tags=["health"])
    async def healthcheck() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()

