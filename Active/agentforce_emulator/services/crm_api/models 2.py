"""SQLModel ORM definitions for CRM entities."""

from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import Column, func
from sqlmodel import Field, JSON, Relationship, SQLModel


class TimestampMixin:
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column_kwargs={"server_default": func.now(), "nullable": False}
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column_kwargs={"server_default": func.now(), "onupdate": datetime.utcnow, "nullable": False}
    )


class Account(SQLModel, table=True):
    __tablename__ = "accounts"

    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    name: str
    industry: Optional[str] = None
    region: Optional[str] = None
    employee_count: Optional[int] = None

    opportunities: list["Opportunity"] = Relationship(back_populates="account")
    contacts: list["Contact"] = Relationship(back_populates="account")


class Contact(SQLModel, table=True):
    __tablename__ = "contacts"

    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    account_id: UUID = Field(foreign_key="accounts.id", nullable=False)
    name: str
    title: Optional[str] = None
    email: Optional[str] = None
    persona: Optional[str] = None

    account: Account = Relationship(back_populates="contacts")


class Opportunity(SQLModel, TimestampMixin, table=True):
    __tablename__ = "opportunities"

    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    name: str
    stage: str = Field(index=True)
    amount: float
    close_date: datetime = Field(index=True)
    account_id: UUID = Field(foreign_key="accounts.id", nullable=False)
    owner_id: Optional[UUID] = None
    last_outreach_at: Optional[datetime] = None
    reactivation_score: Optional[float] = None
    currency: str = "USD"

    account: Account = Relationship(back_populates="opportunities")
    signals: list["OpportunitySignal"] = Relationship(back_populates="opportunity")


class OpportunitySignal(SQLModel, TimestampMixin, table=True):
    __tablename__ = "opportunity_signals"

    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    opportunity_id: UUID = Field(foreign_key="opportunities.id", nullable=False, index=True)
    signal_type: str = Field(index=True)
    weight: float = 0.0
    payload: dict = Field(sa_column=Column(JSON, nullable=False, default=dict))
    observed_at: datetime = Field(default_factory=datetime.utcnow, index=True)

    opportunity: Opportunity = Relationship(back_populates="signals")


