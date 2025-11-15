"""Database utilities for agent runtime persistence."""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from pydantic import AnyUrl, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlmodel import SQLModel

# Import models so SQLModel.metadata is populated
from . import models  # noqa: F401


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: AnyUrl = Field(
        default="postgresql+asyncpg://agentforce:agentforce@localhost:5434/agentforce",
        description="Async database URL used for runtime persistence",
    )


settings = Settings()


def create_engine() -> AsyncEngine:
    return create_async_engine(str(settings.database_url), echo=False, future=True)


engine = create_engine()
session_factory = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


@asynccontextmanager
async def lifespan(app):  # type: ignore[reportAny]
    yield
    await engine.dispose()


@asynccontextmanager
async def get_session() -> AsyncIterator[AsyncSession]:
    async with session_factory() as session:  # type: ignore[reportGeneralTypeIssues]
        yield session

