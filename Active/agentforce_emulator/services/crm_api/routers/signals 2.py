"""Signal endpoints for enrichment data."""

from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlmodel.ext.asyncio.session import AsyncSession

from ..database import get_session
from ..models import Opportunity, OpportunitySignal
from ..schemas import OpportunitySignalOut


router = APIRouter(prefix="/api/v1/signals", tags=["signals"])


@router.get("/opportunity/{opportunity_id}", response_model=list[OpportunitySignalOut])
async def list_signals_for_opportunity(
    opportunity_id: UUID,
    session: AsyncSession = Depends(get_session),
) -> list[OpportunitySignalOut]:
    statement = select(OpportunitySignal).where(OpportunitySignal.opportunity_id == opportunity_id)
    results = await session.execute(statement)
    signals = results.scalars().all()
    return [OpportunitySignalOut.model_validate(sig) for sig in signals]


@router.post("/opportunity/{opportunity_id}", response_model=OpportunitySignalOut, status_code=201)
async def create_signal(
    opportunity_id: UUID,
    payload: dict[str, Any],
    session: AsyncSession = Depends(get_session),
) -> OpportunitySignalOut:
    exists = await session.execute(
        select(Opportunity.id).where(Opportunity.id == opportunity_id)
    )
    if exists.scalar_one_or_none() is None:
        raise HTTPException(status_code=404, detail="Opportunity not found")

    signal = OpportunitySignal(
        opportunity_id=opportunity_id,
        signal_type=payload.get("signal_type", "custom"),
        weight=float(payload.get("weight", 0)),
        payload=payload.get("payload", {}),
        observed_at=datetime.fromisoformat(payload["observed_at"]) if payload.get("observed_at") else datetime.utcnow(),
    )

    session.add(signal)
    await session.commit()
    await session.refresh(signal)

    return OpportunitySignalOut.model_validate(signal)


