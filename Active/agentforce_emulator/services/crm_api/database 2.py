"""Database utilities for the CRM API."""

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


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="", env_file=".env", extra="ignore")

    database_url: AnyUrl = Field(
        default="postgresql+asyncpg://agentforce:agentforce@localhost:5434/agentforce",
        description="Async database URL",
    )


settings = Settings()


def create_engine() -> AsyncEngine:
    return create_async_engine(str(settings.database_url), echo=False, future=True)


engine = create_engine()
async_session_factory = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


@asynccontextmanager
async def lifespan(app):  # type: ignore[reportAny]
    yield
    await engine.dispose()


async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


@asynccontextmanager
async def get_session() -> AsyncIterator[AsyncSession]:
    async with async_session_factory() as session:  # type: ignore[reportGeneralTypeIssues]
        yield session

