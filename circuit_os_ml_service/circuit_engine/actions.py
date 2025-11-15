"""
Action System - Circuit Script actions
20+ built-in actions for business logic automation
"""

from abc import ABC, abstractmethod
from typing import Any, Optional, List, Dict, Callable
import time
import asyncio
from datetime import datetime, timedelta
from .context import CircuitContext


class ActionResult:
    """Result of action execution"""

    def __init__(
        self,
        success: bool,
        data: Any = None,
        error: Optional[str] = None,
        duration: float = 0.0
    ):
        self.success = success
        self.data = data
        self.error = error
        self.duration = duration

    @classmethod
    def success_result(cls, data: Any = None, duration: float = 0.0):
        return cls(success=True, data=data, duration=duration)

    @classmethod
    def error_result(cls, error: str, duration: float = 0.0):
        return cls(success=False, error=error, duration=duration)

    def __repr__(self):
        status = "SUCCESS" if self.success else "ERROR"
        return f"ActionResult({status}, duration={self.duration:.3f}s)"


class Action(ABC):
    """
    Base action class
    All actions must extend this
    """

    def __init__(self, name: Optional[str] = None):
        self.name = name or self.__class__.__name__
        self.max_retries = 3
        self.retry_delay = 1.0  # seconds
        self.timeout = 30.0  # seconds

    @abstractmethod
    async def execute(self, context: CircuitContext) -> ActionResult:
        """Execute the action - must be implemented by subclasses"""
        pass

    def can_execute(self, context: CircuitContext) -> bool:
        """Pre-execution validation"""
        return True

    async def on_success(self, result: ActionResult, context: CircuitContext):
        """Post-success hook"""
        pass

    async def on_error(self, error: Exception, context: CircuitContext):
        """Error handler"""
        context.record_error(self.name, str(error))

    async def execute_with_retry(self, context: CircuitContext) -> ActionResult:
        """Execute with automatic retry on failure"""
        start_time = time.time()

        for attempt in range(self.max_retries):
            try:
                # Pre-execution check
                if not self.can_execute(context):
                    return ActionResult.error_result(
                        f"Action {self.name} cannot execute (pre-condition failed)",
                        time.time() - start_time
                    )

                # Execute with timeout
                result = await asyncio.wait_for(
                    self.execute(context),
                    timeout=self.timeout
                )

                # Post-success hook
                if result.success:
                    await self.on_success(result, context)

                result.duration = time.time() - start_time
                return result

            except asyncio.TimeoutError:
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(self.retry_delay * (attempt + 1))
                else:
                    return ActionResult.error_result(
                        f"Action {self.name} timed out after {self.timeout}s",
                        time.time() - start_time
                    )

            except Exception as e:
                await self.on_error(e, context)

                if attempt < self.max_retries - 1:
                    await asyncio.sleep(self.retry_delay * (attempt + 1))
                else:
                    return ActionResult.error_result(
                        str(e),
                        time.time() - start_time
                    )

        return ActionResult.error_result(
            f"Action {self.name} failed after {self.max_retries} retries",
            time.time() - start_time
        )

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name})"


# ============================================================================
# DATA ACTIONS (Salesforce SOQL/DML equivalent)
# ============================================================================

class GetLeadDataAction(Action):
    """Retrieve lead data - equivalent to SOQL query"""

    def __init__(self, db_client=None):
        super().__init__()
        self.db = db_client

    async def execute(self, context: CircuitContext) -> ActionResult:
        lead_id = context.get("lead_id")

        if not lead_id:
            return ActionResult.error_result("No lead_id provided in context")

        # Simulate database query
        # In production, this would call actual database
        lead = {
            "id": lead_id,
            "name": "John Doe",
            "email": "john@example.com",
            "company_name": "Example Corp",
            "website": "https://example.com",
            "industry": "Technology",
            "company_size": 250,
            "engagement_score": 75,
            "location": "San Francisco, CA"
        }

        context.set("lead", lead)
        context.set("company_name", lead["company_name"])
        context.set("website_url", lead["website"])
        context.set("industry", lead["industry"])

        return ActionResult.success_result(lead)


class CreateOpportunityAction(Action):
    """Create opportunity - equivalent to DML insert"""

    def __init__(self, db_client=None):
        super().__init__()
        self.db = db_client

    async def execute(self, context: CircuitContext) -> ActionResult:
        lead = context.get("lead")
        lead_score = context.get("lead_score", 50)

        if not lead:
            return ActionResult.error_result("No lead data in context")

        # Estimate deal size based on lead score
        deal_size = self._estimate_deal_size(lead_score)

        # Create opportunity (simulate)
        opportunity = {
            "id": f"opp_{datetime.now().timestamp()}",
            "name": f"{lead['company_name']} - Opportunity",
            "account_id": lead.get("account_id", "unknown"),
            "stage": "Prospecting",
            "amount": deal_size,
            "close_date": (datetime.now() + timedelta(days=30)).isoformat(),
            "probability": lead_score,
            "created_at": datetime.now().isoformat()
        }

        context.set("opportunity", opportunity)
        context.set("opportunity_id", opportunity["id"])

        return ActionResult.success_result(opportunity)

    def _estimate_deal_size(self, lead_score: float) -> float:
        """Estimate deal size based on lead score"""
        if lead_score > 90:
            return 50000
        elif lead_score > 70:
            return 25000
        elif lead_score > 50:
            return 10000
        else:
            return 5000


class UpdateLeadAction(Action):
    """Update lead - equivalent to DML update"""

    def __init__(self, fields: Dict[str, Any], db_client=None):
        super().__init__()
        self.fields = fields
        self.db = db_client

    async def execute(self, context: CircuitContext) -> ActionResult:
        lead_id = context.get("lead_id")

        if not lead_id:
            return ActionResult.error_result("No lead_id in context")

        # Simulate update
        updated_lead = context.get("lead", {}).copy()
        updated_lead.update(self.fields)
        updated_lead["updated_at"] = datetime.now().isoformat()

        context.set("lead", updated_lead)

        return ActionResult.success_result(updated_lead)


# ============================================================================
# ML ACTIONS (AI-Native - Apex CAN'T DO THIS)
# ============================================================================

class PredictLeadScoreAction(Action):
    """ML prediction as native operation"""

    def __init__(self, ml_service=None):
        super().__init__()
        self.ml_service = ml_service

    async def execute(self, context: CircuitContext) -> ActionResult:
        lead = context.get("lead")

        if not lead:
            return ActionResult.error_result("No lead data in context")

        # Extract features
        features = {
            "company_size": lead.get("company_size", 0),
            "industry": lead.get("industry", "unknown"),
            "engagement_score": lead.get("engagement_score", 0),
            "website_traffic": context.get("website_traffic", 0),
            "geographic_fit": self._calculate_geo_fit(lead.get("location", ""))
        }

        # Simulate ML prediction
        # In production, this calls actual ML model
        score = self._simulate_prediction(features)

        prediction = {
            "score": score,
            "confidence": 0.85,
            "feature_importance": {
                "engagement_score": 0.35,
                "company_size": 0.25,
                "geographic_fit": 0.20,
                "industry": 0.15,
                "website_traffic": 0.05
            }
        }

        context.set("lead_score", prediction["score"])
        context.set("score_confidence", prediction["confidence"])
        context.set("score_factors", prediction["feature_importance"])

        return ActionResult.success_result(prediction)

    def _calculate_geo_fit(self, location: str) -> float:
        """Calculate geographic fit score"""
        # Simplified - in production would use actual geo data
        target_cities = ["San Francisco", "New York", "Austin", "Seattle"]
        for city in target_cities:
            if city in location:
                return 0.9
        return 0.5

    def _simulate_prediction(self, features: Dict) -> float:
        """Simulate ML prediction"""
        score = 50.0  # Base score

        # Engagement
        score += features["engagement_score"] * 0.35

        # Company size
        if features["company_size"] > 100:
            score += 15
        elif features["company_size"] > 50:
            score += 10

        # Industry
        if features["industry"] in ["Technology", "SaaS", "Finance"]:
            score += 10

        # Geo fit
        score += features["geographic_fit"] * 15

        return min(max(score, 0), 100)  # Clamp to 0-100


class PredictChurnRiskAction(Action):
    """Predict customer churn risk"""

    def __init__(self, ml_service=None):
        super().__init__()
        self.ml_service = ml_service

    async def execute(self, context: CircuitContext) -> ActionResult:
        account_id = context.get("account_id")

        if not account_id:
            return ActionResult.error_result("No account_id in context")

        # Simulate churn prediction
        churn_risk = 0.35  # 35% risk
        factors = {
            "usage_decline": 0.40,
            "support_tickets": 0.25,
            "payment_delays": 0.20,
            "engagement_drop": 0.15
        }

        context.set("churn_risk", churn_risk)
        context.set("churn_factors", factors)

        if churn_risk > 0.7:
            context.set("trigger_churn_prevention", True)

        return ActionResult.success_result({"churn_risk": churn_risk, "factors": factors})


# ============================================================================
# RAG ACTIONS (AI-Native - Apex CAN'T DO THIS)
# ============================================================================

class RetrieveCompanyIntelAction(Action):
    """Adaptive RAG retrieval for company intelligence"""

    def __init__(self, rag_service=None):
        super().__init__()
        self.rag_service = rag_service

    async def execute(self, context: CircuitContext) -> ActionResult:
        company_name = context.get("company_name")

        if not company_name:
            return ActionResult.error_result("No company_name in context")

        # Simulate RAG retrieval
        # In production, this calls Adaptive RAG system
        intel = {
            "documents": [
                {
                    "title": f"{company_name} raises Series B funding",
                    "content": f"{company_name} announced $50M Series B...",
                    "source": "TechCrunch",
                    "published_date": "2025-11-01",
                    "relevance_score": 0.92
                },
                {
                    "title": f"{company_name} launches new product",
                    "content": f"{company_name} unveiled their AI platform...",
                    "source": "VentureBeat",
                    "published_date": "2025-10-15",
                    "relevance_score": 0.87
                }
            ],
            "sources": ["TechCrunch", "VentureBeat"],
            "confidence": 0.89
        }

        context.set("company_intelligence", intel["documents"])
        context.set("intel_sources", intel["sources"])
        context.set("intel_confidence", intel["confidence"])

        return ActionResult.success_result(intel)


class RetrieveBestPracticesAction(Action):
    """Retrieve best practices from knowledge base"""

    def __init__(self, rag_service=None):
        super().__init__()
        self.rag_service = rag_service

    async def execute(self, context: CircuitContext) -> ActionResult:
        situation = context.get("situation", "general")

        # Simulate RAG retrieval
        best_practices = [
            {
                "title": "How to handle objections",
                "content": "Acknowledge, empathize, provide evidence...",
                "relevance": 0.85
            }
        ]

        context.set("recommended_actions", best_practices)

        return ActionResult.success_result(best_practices)


# ============================================================================
# KNOWLEDGE GRAPH ACTIONS (AI-Native - Apex CAN'T DO THIS)
# ============================================================================

class QueryCompetitorsAction(Action):
    """Knowledge graph query for competitors"""

    def __init__(self, kg_service=None):
        super().__init__()
        self.kg_service = kg_service

    async def execute(self, context: CircuitContext) -> ActionResult:
        company_id = context.get("company_id")
        company_name = context.get("company_name", "Unknown")

        # Simulate knowledge graph query
        competitors = [
            {
                "name": "Competitor A",
                "market_share": 0.25,
                "strengths": ["Enterprise focus", "Strong brand"],
                "weaknesses": ["High price", "Complex setup"]
            },
            {
                "name": "Competitor B",
                "market_share": 0.18,
                "strengths": ["Easy to use", "Good support"],
                "weaknesses": ["Limited features", "Scalability"]
            }
        ]

        landscape = {
            "total_competitors": len(competitors),
            "market_leader": competitors[0]["name"],
            "positioning": "challenger"
        }

        context.set("competitors", competitors)
        context.set("competitive_landscape", landscape)

        return ActionResult.success_result(competitors)


class InferRelationshipsAction(Action):
    """ML-powered relationship inference"""

    def __init__(self, kg_service=None):
        super().__init__()
        self.kg_service = kg_service

    async def execute(self, context: CircuitContext) -> ActionResult:
        entity_id = context.get("entity_id")

        # Simulate relationship inference
        relationships = [
            {"entity": "Company X", "relationship": "PARTNER", "confidence": 0.87},
            {"entity": "Company Y", "relationship": "CUSTOMER", "confidence": 0.92}
        ]

        context.set("inferred_relationships", relationships)

        return ActionResult.success_result(relationships)


# ============================================================================
# MCP INTEGRATION ACTIONS (Data Enrichment)
# ============================================================================

class ScrapeWebsiteAction(Action):
    """Scrape company website using Firecrawl MCP"""

    def __init__(self, mcp_client=None):
        super().__init__()
        self.mcp = mcp_client

    async def execute(self, context: CircuitContext) -> ActionResult:
        website_url = context.get("website_url")

        if not website_url:
            return ActionResult.error_result("No website_url in context")

        # Simulate web scraping
        scraped_data = {
            "content": "Company offers AI-powered solutions...",
            "tech_stack": ["React", "Python", "AWS"],
            "products": ["Product A", "Product B"],
            "employee_count": 150
        }

        context.set("website_content", scraped_data["content"])
        context.set("company_tech_stack", scraped_data["tech_stack"])
        context.set("product_list", scraped_data["products"])
        context.set("website_traffic", 50000)  # Monthly visitors

        return ActionResult.success_result(scraped_data)


class SearchNewsAction(Action):
    """Search recent news using Tavily MCP"""

    def __init__(self, mcp_client=None):
        super().__init__()
        self.mcp = mcp_client

    async def execute(self, context: CircuitContext) -> ActionResult:
        company_name = context.get("company_name")

        if not company_name:
            return ActionResult.error_result("No company_name in context")

        # Simulate news search
        news = [
            {
                "title": f"{company_name} Secures Funding",
                "summary": "Company announces growth round...",
                "url": "https://news.example.com/article1",
                "published": "2025-11-10",
                "sentiment": "positive"
            }
        ]

        sentiment_score = 0.8  # Positive

        context.set("recent_news", news)
        context.set("news_sentiment", sentiment_score)

        return ActionResult.success_result(news)


# ============================================================================
# CONTROL FLOW ACTIONS
# ============================================================================

class ConditionalAction(Action):
    """If-then-else logic"""

    def __init__(
        self,
        condition: Callable[[CircuitContext], bool],
        true_action: Action,
        false_action: Optional[Action] = None
    ):
        super().__init__()
        self.condition = condition
        self.true_action = true_action
        self.false_action = false_action

    async def execute(self, context: CircuitContext) -> ActionResult:
        if self.condition(context):
            return await self.true_action.execute_with_retry(context)
        elif self.false_action:
            return await self.false_action.execute_with_retry(context)
        else:
            return ActionResult.success_result("Condition not met, no false action")


class ParallelAction(Action):
    """Execute multiple actions in parallel"""

    def __init__(self, actions: List[Action]):
        super().__init__()
        self.actions = actions

    async def execute(self, context: CircuitContext) -> ActionResult:
        # Execute all actions concurrently
        results = await asyncio.gather(
            *[action.execute_with_retry(context) for action in self.actions],
            return_exceptions=True
        )

        # Check if all succeeded
        all_success = all(
            isinstance(r, ActionResult) and r.success
            for r in results
        )

        return ActionResult.success_result({
            "results": results,
            "all_success": all_success
        })


class LoopAction(Action):
    """Iterate over collection and execute action"""

    def __init__(self, collection_key: str, action: Action):
        super().__init__()
        self.collection_key = collection_key
        self.action = action

    async def execute(self, context: CircuitContext) -> ActionResult:
        collection = context.get(self.collection_key, [])
        results = []

        for item in collection:
            # Create new context for each iteration
            item_context = CircuitContext(context.get_all())
            item_context.set("current_item", item)

            result = await self.action.execute_with_retry(item_context)
            results.append(result)

        return ActionResult.success_result(results)


# ============================================================================
# NOTIFICATION ACTIONS
# ============================================================================

class SendSlackAlertAction(Action):
    """Send Slack notification"""

    def __init__(self, channel: str, slack_client=None):
        super().__init__()
        self.channel = channel
        self.slack = slack_client

    async def execute(self, context: CircuitContext) -> ActionResult:
        lead = context.get("lead", {})
        lead_score = context.get("lead_score", 0)

        message = f"""
🔥 *Hot Lead Detected!*

Company: {lead.get('company_name', 'Unknown')}
Score: {lead_score}/100
Contact: {lead.get('name', 'Unknown')} ({lead.get('email', 'N/A')})

Intelligence:
{self._format_intel(context.get('company_intelligence', []))}

Action: Opportunity created (ID: {context.get('opportunity_id', 'N/A')})
"""

        # In production, this would call actual Slack API
        print(f"[SLACK {self.channel}] {message}")

        context.set("slack_notification_sent", True)

        return ActionResult.success_result("Slack notification sent")

    def _format_intel(self, intel: List[Dict]) -> str:
        if not intel:
            return "No recent intelligence"
        return "\n".join([f"- {doc.get('title', 'Unknown')}" for doc in intel[:3]])


class SendEmailAction(Action):
    """Send email notification"""

    def __init__(self, email_service=None):
        super().__init__()
        self.email = email_service

    async def execute(self, context: CircuitContext) -> ActionResult:
        recipient = context.get("email_recipient")
        subject = context.get("email_subject", "Notification from Circuit OS")
        body = context.get("email_body", "")

        if not recipient:
            return ActionResult.error_result("No email_recipient in context")

        # In production, this would call actual email service
        print(f"[EMAIL] To: {recipient}, Subject: {subject}")

        context.set("email_sent", True)

        return ActionResult.success_result("Email sent")


# ============================================================================
# UTILITY ACTIONS
# ============================================================================

class LogAction(Action):
    """Log a message"""

    def __init__(self, message: str, level: str = "INFO"):
        super().__init__()
        self.message = message
        self.level = level

    async def execute(self, context: CircuitContext) -> ActionResult:
        formatted_message = self.message.format(**context.get_all())
        print(f"[{self.level}] {formatted_message}")
        return ActionResult.success_result(formatted_message)


class WaitAction(Action):
    """Wait for specified duration"""

    def __init__(self, seconds: float):
        super().__init__()
        self.seconds = seconds

    async def execute(self, context: CircuitContext) -> ActionResult:
        await asyncio.sleep(self.seconds)
        return ActionResult.success_result(f"Waited {self.seconds}s")


class SetVariableAction(Action):
    """Set a variable in context"""

    def __init__(self, key: str, value: Any):
        super().__init__()
        self.key = key
        self.value = value

    async def execute(self, context: CircuitContext) -> ActionResult:
        # Support callable values for dynamic computation
        if callable(self.value):
            computed_value = self.value(context)
        else:
            computed_value = self.value

        context.set(self.key, computed_value)
        return ActionResult.success_result(computed_value)
