"""SQLModel ORM definitions for agent runtime persistence."""

from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import Column, func
from sqlmodel import Field, JSON, Relationship, SQLModel


class AgentRun(SQLModel, table=True):
    __tablename__ = "agent_runs"

    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    mode: str = Field(default="weekly", index=True)
    evaluated: int = 0
    acted: int = 0
    dry_run: bool = False
    status: str = Field(default="completed", index=True)
    started_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    completed_at: datetime = Field(default_factory=datetime.utcnow)
    config_version: Optional[str] = None
    notes: Optional[str] = None

    actions: list["AgentAction"] = Relationship(back_populates="run")


class AgentAction(SQLModel, table=True):
    __tablename__ = "agent_actions"

    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    run_id: UUID = Field(foreign_key="agent_runs.id", nullable=False, index=True)
    type: str
    status: str = Field(default="queued", index=True)
    payload: dict = Field(sa_column=Column(JSON, default=dict, nullable=False))
    created_at: datetime = Field(
        sa_column=Column(
            default_factory=datetime.utcnow,
            server_default=func.now(),
            nullable=False,
        )
    )

    run: AgentRun = Relationship(back_populates="actions")

