"""Lost opportunity orchestrator logic."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any
from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from ..schemas import ActionOutcome, AgentRunRequest, AgentRunResponse, OpportunityAgentView
from .clients.crm_client import CRMClient
from .clients.signals_client import SignalCache
from .utils import actions as action_utils
from .utils.prompts import build_email_prompt
from .utils.scoring import ScoreResult, compute_score, load_scoring_config
from .models import AgentAction, AgentRun


@dataclass(slots=True)
class LostOpportunityOrchestrator:
    crm_client: CRMClient
    signal_cache: SignalCache
    config: dict[str, Any]

    def __init__(self, crm_client: CRMClient | None = None, signal_cache: SignalCache | None = None) -> None:
        self.crm_client = crm_client or CRMClient()
        self.signal_cache = signal_cache or SignalCache()
        self.config = load_scoring_config()

    async def run(
        self,
        request: AgentRunRequest,
        session: AsyncSession | None = None,
    ) -> AgentRunResponse:
        run_id = uuid4()
        started_at = datetime.utcnow()

        run_record: AgentRun | None = None
        if session is not None:
            run_record = AgentRun(
                id=run_id,
                mode=request.mode,
                dry_run=request.dry_run,
                status="running",
                started_at=started_at,
                config_version=str(self.config.get("version", "unknown")),
            )
            session.add(run_record)
            await session.commit()

        outcomes: list[ActionOutcome] = []
        acted = 0
        error: Exception | None = None

        try:
            opportunities = await self.crm_client.fetch_closed_lost_opportunities(limit=request.limit)
            thresholds = self.config.get("global_thresholds", {})
            action_plan = self.config.get("actions", {})

            for opportunity in opportunities:
                signals = await self._load_signals(opportunity)
                score_result = compute_score(opportunity, signals, self.config)

                decision = self._determine_band(score_result.score, thresholds)
                if decision == "ignore":
                    continue

                executed = await self._execute_actions(
                    opportunity,
                    decision,
                    score_result,
                    action_plan,
                    dry_run=request.dry_run,
                )
                if executed:
                    acted += 1
                    outcomes.extend(executed)

        except Exception as exc:  # pragma: no cover - bubbled to FastAPI
            error = exc
            raise
        finally:
            completed_at = datetime.utcnow()
            if session is not None and run_record is not None:
                run_record.evaluated = len(opportunities) if 'opportunities' in locals() else 0
                run_record.acted = acted
                run_record.status = "failed" if error else "completed"
                run_record.completed_at = completed_at
                if error:
                    run_record.notes = str(error)
                session.add(run_record)
                await session.flush()

                if not error:
                    action_models = [
                        AgentAction(
                            run_id=run_record.id,
                            type=outcome.type,
                            status=outcome.status,
                            payload=outcome.payload,
                        )
                        for outcome in outcomes
                    ]
                    session.add_all(action_models)

                await session.commit()

        return AgentRunResponse(
            run_id=run_id,
            evaluated=len(opportunities) if 'opportunities' in locals() else 0,
            acted=acted,
            outcomes=outcomes,
            started_at=started_at,
            completed_at=completed_at,
        )

    async def _load_signals(self, opportunity: OpportunityAgentView) -> list[dict[str, Any]]:
        if opportunity.signals:
            return list(opportunity.signals)
        cached = await self.signal_cache.get_signals(opportunity.id)
        if cached:
            return list(cached)
        signals = await self.crm_client.fetch_signals(opportunity.id)
        if signals:
            await self.signal_cache.set_signals(opportunity.id, signals)
        return list(signals)

    def _determine_band(self, score: float, thresholds: dict[str, Any]) -> str:
        urgent = thresholds.get("urgent", 80)
        high = thresholds.get("high", 60)
        if score >= urgent:
            return "urgent"
        if score >= high:
            return "high"
        return "ignore"

    async def _execute_actions(
        self,
        opportunity: OpportunityAgentView,
        decision: str,
        score_result: ScoreResult,
        action_plan: dict[str, Any],
        dry_run: bool,
    ) -> list[ActionOutcome]:
        plan = action_plan.get(decision, {})
        tasks_cfg = plan.get("tasks")
        alerts_cfg = plan.get("alerts")
        annotation_cfg = plan.get("annotations", {})

        outcomes: list[ActionOutcome] = []

        if tasks_cfg:
            outcome = action_utils.action_registry.create_task(
                opportunity_id=str(opportunity.id),
                due_in_days=int(tasks_cfg.get("due_in_days", 7)),
                priority=str(tasks_cfg.get("priority", "normal")),
            )
            if dry_run:
                outcome.status = "simulated"
            outcomes.append(outcome)

        if alerts_cfg and alerts_cfg.get("channels"):
            outcome = action_utils.action_registry.send_slack_alert(
                opportunity_id=str(opportunity.id),
                score=score_result.score,
                urgency=decision,
            )
            if dry_run:
                outcome.status = "simulated"
            outcomes.append(outcome)

        if annotation_cfg:
            annotation_payload = {
                key: (score_result.score if value == "score" else value)
                for key, value in annotation_cfg.items()
            }
            outcome = action_utils.action_registry.record_annotation(
                opportunity_id=str(opportunity.id),
                annotation=annotation_payload,
            )
            if dry_run:
                outcome.status = "simulated"
            outcomes.append(outcome)

        email_body = self._draft_email(opportunity, score_result)
        email_outcome = action_utils.action_registry.compose_email(
            opportunity_id=str(opportunity.id),
            body=email_body,
        )
        if dry_run:
            email_outcome.status = "simulated"
        outcomes.append(email_outcome)

        if not dry_run:
            await self.crm_client.update_reactivation_score(opportunity.id, score_result.score)
        return outcomes

    def _draft_email(self, opportunity: OpportunityAgentView, score_result: ScoreResult) -> str:
        trigger_summary = ", ".join(score_result.reasons[:2]) or "Recent changes at the account"
        objection_summary = "Budget constraints from prior cycle"
        value_proof = "New ROI benchmarks and financing options"
        prompt = build_email_prompt(
            opportunity_name=opportunity.name,
            account_name="",
            contact_name="",
            trigger_summary=trigger_summary,
            objection_summary=objection_summary,
            value_proof=value_proof,
        )
        body = (
            f"Subject: Reigniting {opportunity.name}\n\n"
            f"Hi team,\n\n"
            f"{trigger_summary}. Given the earlier {objection_summary}, I wanted to share {value_proof}."
            f" Let's connect for 15 minutes this week to align on next steps.\n\nBest,\nAgentforce Emulator"
        )
        return f"Prompt:\n{prompt}\n\nDraft:\n{body}"

