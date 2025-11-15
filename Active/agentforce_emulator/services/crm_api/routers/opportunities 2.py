"""Opportunity endpoints."""

from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.orm import selectinload
from sqlalchemy.sql import Select
from sqlmodel.ext.asyncio.session import AsyncSession

from ..database import get_session
from ..models import Opportunity
from ..schemas import OpportunityFilter, OpportunityListResponse, OpportunityOut


router = APIRouter(prefix="/api/v1/opportunities", tags=["opportunities"])


def apply_filters(statement: Select[tuple[Opportunity]], filters: OpportunityFilter) -> Select:
    if filters.stages:
        statement = statement.where(Opportunity.stage.in_(filters.stages))
    if filters.min_amount is not None:
        statement = statement.where(Opportunity.amount >= filters.min_amount)
    if filters.max_amount is not None:
        statement = statement.where(Opportunity.amount <= filters.max_amount)
    if filters.close_date_start:
        statement = statement.where(Opportunity.close_date >= filters.close_date_start)
    if filters.close_date_end:
        statement = statement.where(Opportunity.close_date <= filters.close_date_end)
    return statement


@router.post("/query", response_model=OpportunityListResponse)
async def query_opportunities(
    filters: OpportunityFilter,
    session: AsyncSession = Depends(get_session),
) -> OpportunityListResponse:
    limit = min(filters.limit, 500)
    base_query: Select[tuple[Opportunity]] = (
        select(Opportunity)
        .options(selectinload(Opportunity.signals))
        .order_by(Opportunity.close_date.desc())
    )
    statement = apply_filters(base_query, filters).limit(limit)

    results = await session.execute(statement)
    opportunities = results.unique().scalars().all()

    count_statement = apply_filters(select(func.count()).select_from(Opportunity), filters)
    total = (await session.execute(count_statement)).scalar_one()

    payload = [OpportunityOut.model_validate(op) for op in opportunities]
    return OpportunityListResponse(opportunities=payload, total=total)


@router.get("/{opportunity_id}", response_model=OpportunityOut)
async def get_opportunity(
    opportunity_id: UUID,
    include_signals: bool = Query(True, description="Include enrichment signals"),
    session: AsyncSession = Depends(get_session),
) -> OpportunityOut:
    statement: Select[tuple[Opportunity]] = select(Opportunity)
    if include_signals:
        statement = statement.options(selectinload(Opportunity.signals))
    statement = statement.where(Opportunity.id == opportunity_id)

    result = await session.execute(statement)
    opportunity = result.scalar_one_or_none()
    if opportunity is None:
        raise HTTPException(status_code=404, detail="Opportunity not found")

    return OpportunityOut.model_validate(opportunity)


@router.post("/{opportunity_id}/score", response_model=dict[str, Any])
async def update_reactivation_score(
    opportunity_id: UUID,
    payload: dict[str, Any],
    session: AsyncSession = Depends(get_session),
) -> dict[str, Any]:
    new_score = payload.get("score")
    if new_score is None:
        raise HTTPException(status_code=400, detail="Missing score in payload")

    statement = select(Opportunity).where(Opportunity.id == opportunity_id)
    result = await session.execute(statement)
    opportunity = result.scalar_one_or_none()
    if opportunity is None:
        raise HTTPException(status_code=404, detail="Opportunity not found")

    opportunity.reactivation_score = float(new_score)
    opportunity.last_outreach_at = datetime.utcnow()
    session.add(opportunity)
    await session.commit()

    return {"opportunity_id": str(opportunity_id), "reactivation_score": float(new_score)}

