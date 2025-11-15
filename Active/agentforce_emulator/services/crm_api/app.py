"""Application entrypoint for the CRM API service."""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import get_session, lifespan, init_db
from .routers import opportunities, signals


def create_app() -> FastAPI:
    app = FastAPI(
        title="Agentforce Emulator CRM API",
        version="0.1.0",
        lifespan=lifespan,
    )

    app.include_router(opportunities.router)
    app.include_router(signals.router)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.on_event("startup")
    async def _startup() -> None:
        await init_db()

    return app


app = create_app()


@app.get("/health", tags=["health"])
async def healthcheck() -> dict[str, str]:
    async with get_session() as session:  # noqa: F841 - ensures connection works
        return {"status": "ok"}


