"""Pydantic schemas for agent runtime API."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field


class AgentRunRequest(BaseModel):
    mode: str = "weekly"
    limit: int = 200
    dry_run: bool = False


class OpportunityAgentView(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    stage: str
    amount: float
    close_date: datetime
    reactivation_score: Optional[float] = None
    signals: list[dict[str, Any]]


class ActionOutcome(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    type: str
    payload: dict[str, Any]
    status: str = "queued"


class AgentRunResponse(BaseModel):
    run_id: UUID
    evaluated: int
    acted: int
    outcomes: list[ActionOutcome]
    started_at: datetime
    completed_at: datetime


class AgentActionRecord(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    run_id: UUID
    type: str
    status: str
    payload: dict[str, Any]
    created_at: datetime


class AgentRunSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    mode: str
    evaluated: int
    acted: int
    dry_run: bool
    status: str
    started_at: datetime
    completed_at: datetime
    config_version: Optional[str] = None
    notes: Optional[str] = None


class AgentRunDetail(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    mode: str
    evaluated: int
    acted: int
    dry_run: bool
    status: str
    started_at: datetime
    completed_at: datetime
    config_version: Optional[str]
    notes: Optional[str]
    actions: list[AgentActionRecord]


class AgentRunListResponse(BaseModel):
    runs: list[AgentRunSummary]

