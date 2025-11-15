"""Pydantic schemas for CRM API responses."""

from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class OpportunityFilter(BaseModel):
    stages: Optional[list[str]] = None
    min_amount: Optional[float] = None
    max_amount: Optional[float] = None
    close_date_start: Optional[datetime] = None
    close_date_end: Optional[datetime] = None
    limit: int = 200


class OpportunitySignalOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    opportunity_id: UUID
    signal_type: str
    weight: float
    payload: dict
    observed_at: datetime


class OpportunityOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    stage: str
    amount: float
    close_date: datetime
    account_id: UUID
    owner_id: Optional[UUID]
    reactivation_score: Optional[float]
    last_outreach_at: Optional[datetime]
    signals: list[OpportunitySignalOut] = []


class AccountOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    industry: Optional[str]
    region: Optional[str]
    employee_count: Optional[int]


class OpportunityListResponse(BaseModel):
    opportunities: list[OpportunityOut]
    total: int

