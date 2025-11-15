"""Seed script for CRM API service."""

from __future__ import annotations

import asyncio
import csv
from datetime import datetime
from pathlib import Path
from uuid import UUID

from sqlmodel import select

from .database import async_session_factory, init_db
from .models import Account, Opportunity, OpportunitySignal


DATA_DIR = Path(__file__).resolve().parents[2] / "seed_data"


def parse_uuid(value: str | None) -> UUID | None:
    if not value:
        return None
    return UUID(value)


async def seed_accounts(session) -> dict[str, Account]:
    accounts: dict[str, Account] = {}
    accounts_csv = DATA_DIR / "accounts.csv"
    if not accounts_csv.exists():
        return accounts

    with accounts_csv.open() as fp:
        reader = csv.DictReader(fp)
        for row in reader:
            account = Account(
                name=row["name"],
                industry=row.get("industry"),
                region=row.get("region"),
                employee_count=int(row.get("employee_count" or 0) or 0) or None,
            )
            session.add(account)
            await session.flush()
            accounts[account.name] = account

    await session.commit()
    return accounts


async def seed_opportunities(session, accounts: dict[str, Account]) -> dict[UUID, Opportunity]:
    opportunities_csv = DATA_DIR / "opportunities.csv"
    opportunities: dict[UUID, Opportunity] = {}
    if not opportunities_csv.exists():
        return opportunities

    with opportunities_csv.open() as fp:
        reader = csv.DictReader(fp)
        for row in reader:
            account_name = row["account_name"]
            account = accounts.get(account_name)
            if account is None:
                account = Account(name=account_name)
                session.add(account)
                await session.flush()
                accounts[account.name] = account

            opportunity = Opportunity(
                name=row["name"],
                stage=row["stage"],
                amount=float(row["amount"]),
                close_date=datetime.fromisoformat(row["close_date"]),
                account_id=account.id,
                owner_id=parse_uuid(row.get("owner_id")),
            )

            session.add(opportunity)
            await session.flush()
            opportunities[opportunity.id] = opportunity

    await session.commit()
    return opportunities


async def seed_signals(session, opportunities: dict[UUID, Opportunity]) -> None:
    signals_csv = DATA_DIR / "signals.csv"
    if not signals_csv.exists():
        return

    with signals_csv.open() as fp:
        reader = csv.DictReader(fp)
        for row in reader:
            raw_id = row.get("opportunity_external_id")
            opportunity: Opportunity | None = None
            if raw_id:
                stmt = select(Opportunity).where(Opportunity.name == raw_id)
                result = await session.execute(stmt)
                opportunity = result.scalar_one_or_none()
            if opportunity is None and opportunities:
                opportunity = next(iter(opportunities.values()))
            if opportunity is None:
                continue

            signal = OpportunitySignal(
                opportunity_id=opportunity.id,
                signal_type=row["signal_type"],
                weight=float(row.get("weight", 0) or 0),
                payload={
                    "source": row.get("source"),
                    "summary": row.get("summary"),
                    "url": row.get("url"),
                },
                observed_at=datetime.fromisoformat(row["observed_at"]),
            )
            session.add(signal)

    await session.commit()


async def main() -> None:
    await init_db()
    async with async_session_factory() as session:
        accounts = await seed_accounts(session)
        opportunities = await seed_opportunities(session, accounts)
        await seed_signals(session, opportunities)


if __name__ == "__main__":
    asyncio.run(main())

