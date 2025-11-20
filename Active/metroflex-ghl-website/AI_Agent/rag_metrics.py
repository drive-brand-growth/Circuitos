#!/usr/bin/env python3
"""
Circuit OS RAG Metrics & Explainability
Business metrics instrumentation and query decision transparency.

For investor pitches: Proves ROI claims with real data.
"""

import logging
import psycopg2
from psycopg2.extras import Json
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class QueryLogger:
    """
    Tracks RAG query decisions for explainability and business metrics.

    Enables "Why this answer?" transparency by logging:
    - Which documents were retrieved
    - Relevance scores for each chunk
    - Quality gate decisions
    - Cache hit/miss
    - Query route taken
    """

    def __init__(self, database_url: str):
        self.database_url = database_url
        self.conn = None
        self._connect()
        self._ensure_schema()

    def _connect(self):
        """Establish database connection"""
        try:
            self.conn = psycopg2.connect(self.database_url)
            self.conn.autocommit = False
            logger.info("QueryLogger connected to PostgreSQL")
        except Exception as e:
            logger.error(f"QueryLogger database connection failed: {e}")
            raise

    def _ensure_schema(self):
        """Create query logging tables"""
        with self.conn.cursor() as cur:
            # Query log table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS rag_query_log (
                    id SERIAL PRIMARY KEY,
                    query_id TEXT UNIQUE NOT NULL,
                    query_text TEXT NOT NULL,
                    route TEXT,
                    cached BOOLEAN DEFAULT FALSE,
                    cache_similarity FLOAT,
                    total_time_ms FLOAT,
                    created_at TIMESTAMP DEFAULT NOW(),
                    agent_id TEXT,
                    session_id TEXT,

                    -- Quality metrics
                    relevance_score FLOAT,
                    quality_gate_passed BOOLEAN,
                    quality_gate_action TEXT,

                    -- Business metrics
                    high_intent BOOLEAN DEFAULT FALSE,
                    led_to_conversion BOOLEAN DEFAULT FALSE,
                    conversion_value FLOAT,

                    metadata JSONB DEFAULT '{}'
                );
                CREATE INDEX IF NOT EXISTS idx_query_log_id ON rag_query_log(query_id);
                CREATE INDEX IF NOT EXISTS idx_query_log_created ON rag_query_log(created_at);
                CREATE INDEX IF NOT EXISTS idx_query_log_agent ON rag_query_log(agent_id);
            """)

            # Query-chunk association table (which chunks were retrieved)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS rag_query_chunks (
                    id SERIAL PRIMARY KEY,
                    query_id TEXT REFERENCES rag_query_log(query_id),
                    chunk_id TEXT,
                    document_id INTEGER,
                    similarity_score FLOAT,
                    rank INTEGER,
                    feedback_weight FLOAT DEFAULT 1.0,
                    created_at TIMESTAMP DEFAULT NOW()
                );
                CREATE INDEX IF NOT EXISTS idx_query_chunks_query ON rag_query_chunks(query_id);
            """)

            # Business conversion tracking
            cur.execute("""
                CREATE TABLE IF NOT EXISTS rag_business_events (
                    id SERIAL PRIMARY KEY,
                    query_id TEXT REFERENCES rag_query_log(query_id),
                    event_type TEXT NOT NULL,
                    event_value FLOAT,
                    event_metadata JSONB DEFAULT '{}',
                    created_at TIMESTAMP DEFAULT NOW()
                );
                CREATE INDEX IF NOT EXISTS idx_business_events_query ON rag_business_events(query_id);
                CREATE INDEX IF NOT EXISTS idx_business_events_type ON rag_business_events(event_type);
            """)

            self.conn.commit()
            logger.info("Query logging schema initialized")

    def log_query(self, query_id: str, query_text: str, route: str = None,
                  cached: bool = False, cache_similarity: float = None,
                  total_time_ms: float = None, agent_id: str = None,
                  session_id: str = None, high_intent: bool = False,
                  relevance_score: float = None, quality_gate_passed: bool = None,
                  quality_gate_action: str = None, metadata: Dict = None) -> str:
        """
        Log a RAG query for explainability and metrics.

        Returns: query_id (for linking follow-up events)
        """
        try:
            with self.conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO rag_query_log (
                        query_id, query_text, route, cached, cache_similarity,
                        total_time_ms, agent_id, session_id, high_intent,
                        relevance_score, quality_gate_passed, quality_gate_action,
                        metadata
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (query_id) DO UPDATE SET
                        total_time_ms = EXCLUDED.total_time_ms,
                        relevance_score = EXCLUDED.relevance_score,
                        quality_gate_passed = EXCLUDED.quality_gate_passed,
                        quality_gate_action = EXCLUDED.quality_gate_action
                    RETURNING query_id;
                """, (
                    query_id, query_text, route, cached, cache_similarity,
                    total_time_ms, agent_id, session_id, high_intent,
                    relevance_score, quality_gate_passed, quality_gate_action,
                    Json(metadata or {})
                ))

                result = cur.fetchone()[0]
                self.conn.commit()
                return result

        except Exception as e:
            logger.error(f"Error logging query: {e}")
            self.conn.rollback()
            return query_id

    def log_retrieved_chunks(self, query_id: str, chunks: List[Dict[str, Any]]):
        """
        Log which chunks were retrieved for a query.

        Args:
            query_id: The query ID from log_query()
            chunks: List of chunk dictionaries with 'id', 'similarity', 'document_id'
        """
        try:
            with self.conn.cursor() as cur:
                # Delete existing chunk associations (in case of retry)
                cur.execute("DELETE FROM rag_query_chunks WHERE query_id = %s", (query_id,))

                # Insert chunk associations
                for rank, chunk in enumerate(chunks, start=1):
                    cur.execute("""
                        INSERT INTO rag_query_chunks (
                            query_id, chunk_id, document_id, similarity_score, rank
                        ) VALUES (%s, %s, %s, %s, %s);
                    """, (
                        query_id,
                        chunk.get('id'),
                        chunk.get('document_id'),
                        chunk.get('similarity'),
                        rank
                    ))

                self.conn.commit()

        except Exception as e:
            logger.error(f"Error logging retrieved chunks: {e}")
            self.conn.rollback()

    def log_business_event(self, query_id: str, event_type: str,
                          event_value: float = None, metadata: Dict = None):
        """
        Log business events linked to queries (conversions, revenue, etc).

        Event types:
        - 'high_intent_detected': Query showed buying signals
        - 'ghl_lead_created': Lead sent to GoHighLevel
        - 'meeting_booked': Converted to meeting
        - 'deal_closed': Revenue generated
        """
        try:
            with self.conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO rag_business_events (
                        query_id, event_type, event_value, event_metadata
                    ) VALUES (%s, %s, %s, %s);
                """, (query_id, event_type, event_value, Json(metadata or {})))

                # Update query log if it's a conversion
                if event_type in ['meeting_booked', 'deal_closed']:
                    cur.execute("""
                        UPDATE rag_query_log
                        SET led_to_conversion = TRUE,
                            conversion_value = COALESCE(conversion_value, 0) + %s
                        WHERE query_id = %s;
                    """, (event_value or 0, query_id))

                self.conn.commit()
                logger.info(f"Business event logged: {event_type} for query {query_id}")

        except Exception as e:
            logger.error(f"Error logging business event: {e}")
            self.conn.rollback()

    def get_query_explanation(self, query_id: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed explanation for why a query returned specific results.

        Returns:
        {
            "query": "...",
            "route": "single_step",
            "cached": false,
            "total_time_ms": 185,
            "quality_gate": {...},
            "retrieved_chunks": [
                {
                    "chunk_id": "...",
                    "document_title": "...",
                    "document_url": "...",
                    "text": "...",
                    "similarity_score": 0.85,
                    "rank": 1,
                    "why_selected": "High relevance score, no negative feedback"
                }
            ],
            "business_impact": {
                "high_intent": true,
                "conversions": [...],
                "total_value": 50000
            }
        }
        """
        try:
            with self.conn.cursor() as cur:
                # Get query log
                cur.execute("""
                    SELECT query_text, route, cached, cache_similarity, total_time_ms,
                           relevance_score, quality_gate_passed, quality_gate_action,
                           high_intent, led_to_conversion, conversion_value,
                           created_at, agent_id, metadata
                    FROM rag_query_log
                    WHERE query_id = %s;
                """, (query_id,))

                row = cur.fetchone()
                if not row:
                    return None

                explanation = {
                    "query_id": query_id,
                    "query": row[0],
                    "route": row[1],
                    "cached": row[2],
                    "cache_similarity": row[3],
                    "total_time_ms": row[4],
                    "quality_gate": {
                        "relevance_score": row[5],
                        "passed": row[6],
                        "action": row[7]
                    },
                    "created_at": row[11].isoformat() if row[11] else None,
                    "agent_id": row[12],
                    "metadata": row[13]
                }

                # Get retrieved chunks with document details
                cur.execute("""
                    SELECT
                        qc.chunk_id,
                        qc.similarity_score,
                        qc.rank,
                        qc.feedback_weight,
                        rc.text,
                        rd.title,
                        rd.url,
                        rd.id
                    FROM rag_query_chunks qc
                    JOIN rag_chunks rc ON qc.chunk_id = rc.chunk_id
                    JOIN rag_documents rd ON rc.document_id = rd.id
                    WHERE qc.query_id = %s
                    ORDER BY qc.rank;
                """, (query_id,))

                chunks = []
                for chunk_row in cur.fetchall():
                    chunks.append({
                        "chunk_id": chunk_row[0],
                        "similarity_score": chunk_row[1],
                        "rank": chunk_row[2],
                        "feedback_weight": chunk_row[3],
                        "text": chunk_row[4][:500] + "..." if len(chunk_row[4]) > 500 else chunk_row[4],
                        "document_title": chunk_row[5],
                        "document_url": chunk_row[6],
                        "document_id": chunk_row[7],
                        "why_selected": self._generate_selection_reason(
                            chunk_row[1], chunk_row[2], chunk_row[3]
                        )
                    })

                explanation["retrieved_chunks"] = chunks

                # Get business events
                cur.execute("""
                    SELECT event_type, event_value, event_metadata, created_at
                    FROM rag_business_events
                    WHERE query_id = %s
                    ORDER BY created_at;
                """, (query_id,))

                business_events = []
                for event_row in cur.fetchall():
                    business_events.append({
                        "type": event_row[0],
                        "value": event_row[1],
                        "metadata": event_row[2],
                        "timestamp": event_row[3].isoformat() if event_row[3] else None
                    })

                explanation["business_impact"] = {
                    "high_intent": row[8],
                    "led_to_conversion": row[9],
                    "conversion_value": row[10],
                    "events": business_events
                }

                return explanation

        except Exception as e:
            logger.error(f"Error getting query explanation: {e}")
            return None

    def _generate_selection_reason(self, similarity: float, rank: int,
                                   feedback_weight: float) -> str:
        """Generate human-readable explanation for why a chunk was selected"""
        reasons = []

        if similarity >= 0.8:
            reasons.append("Very high relevance")
        elif similarity >= 0.6:
            reasons.append("High relevance")
        elif similarity >= 0.4:
            reasons.append("Moderate relevance")
        else:
            reasons.append("Low relevance (included for completeness)")

        if rank <= 3:
            reasons.append("top result")

        if feedback_weight > 1.2:
            reasons.append("boosted by positive user feedback")
        elif feedback_weight < 0.8:
            reasons.append("downranked by negative feedback")

        return ", ".join(reasons).capitalize()


class BusinessMetrics:
    """
    Business-level metrics for ROI tracking and investor demos.

    Tracks:
    - Query volume (total, high-intent, conversions)
    - Conversion funnel (queries → leads → meetings → deals)
    - Revenue attribution
    - Agent performance
    - Cache efficiency
    """

    def __init__(self, database_url: str):
        self.database_url = database_url
        self.conn = None
        self._connect()

    def _connect(self):
        """Establish database connection"""
        try:
            self.conn = psycopg2.connect(self.database_url)
            self.conn.autocommit = False
        except Exception as e:
            logger.error(f"BusinessMetrics database connection failed: {e}")
            raise

    def get_roi_dashboard(self, days: int = 30) -> Dict[str, Any]:
        """
        Get comprehensive ROI metrics for investor demos.

        Returns metrics proving:
        - 25-30% operational cost reduction
        - 40% faster information discovery
        - Revenue attribution
        """
        try:
            cutoff = datetime.utcnow() - timedelta(days=days)

            with self.conn.cursor() as cur:
                # === QUERY VOLUME METRICS ===
                cur.execute("""
                    SELECT
                        COUNT(*) as total_queries,
                        COUNT(CASE WHEN cached = TRUE THEN 1 END) as cache_hits,
                        COUNT(CASE WHEN high_intent = TRUE THEN 1 END) as high_intent_queries,
                        COUNT(CASE WHEN led_to_conversion = TRUE THEN 1 END) as converted_queries,
                        AVG(total_time_ms) as avg_query_time_ms,
                        AVG(CASE WHEN cached = TRUE THEN total_time_ms END) as avg_cached_time_ms,
                        AVG(CASE WHEN cached = FALSE THEN total_time_ms END) as avg_uncached_time_ms
                    FROM rag_query_log
                    WHERE created_at >= %s;
                """, (cutoff,))

                query_row = cur.fetchone()

                total_queries = query_row[0] or 0
                cache_hits = query_row[1] or 0
                high_intent_queries = query_row[2] or 0
                converted_queries = query_row[3] or 0

                # === CONVERSION FUNNEL ===
                cur.execute("""
                    SELECT
                        event_type,
                        COUNT(*) as count,
                        SUM(event_value) as total_value
                    FROM rag_business_events
                    WHERE created_at >= %s
                    GROUP BY event_type;
                """, (cutoff,))

                conversion_funnel = {}
                for event_row in cur.fetchall():
                    conversion_funnel[event_row[0]] = {
                        "count": event_row[1],
                        "total_value": float(event_row[2]) if event_row[2] else 0
                    }

                # === REVENUE ATTRIBUTION ===
                cur.execute("""
                    SELECT
                        SUM(conversion_value) as total_revenue,
                        AVG(conversion_value) as avg_deal_size
                    FROM rag_query_log
                    WHERE created_at >= %s AND led_to_conversion = TRUE;
                """, (cutoff,))

                revenue_row = cur.fetchone()
                total_revenue = float(revenue_row[0]) if revenue_row[0] else 0
                avg_deal_size = float(revenue_row[1]) if revenue_row[1] else 0

                # === AGENT PERFORMANCE ===
                cur.execute("""
                    SELECT
                        agent_id,
                        COUNT(*) as queries,
                        COUNT(CASE WHEN high_intent = TRUE THEN 1 END) as high_intent,
                        COUNT(CASE WHEN led_to_conversion = TRUE THEN 1 END) as conversions,
                        SUM(conversion_value) as revenue
                    FROM rag_query_log
                    WHERE created_at >= %s AND agent_id IS NOT NULL
                    GROUP BY agent_id
                    ORDER BY revenue DESC NULLS LAST;
                """, (cutoff,))

                agent_performance = []
                for agent_row in cur.fetchall():
                    agent_performance.append({
                        "agent_id": agent_row[0],
                        "queries": agent_row[1],
                        "high_intent": agent_row[2],
                        "conversions": agent_row[3],
                        "revenue": float(agent_row[4]) if agent_row[4] else 0,
                        "conversion_rate": (agent_row[3] / agent_row[1] * 100) if agent_row[1] > 0 else 0
                    })

                # === CALCULATE ROI METRICS ===
                cache_hit_rate = (cache_hits / total_queries * 100) if total_queries > 0 else 0
                high_intent_rate = (high_intent_queries / total_queries * 100) if total_queries > 0 else 0
                conversion_rate = (converted_queries / total_queries * 100) if total_queries > 0 else 0

                # Cost savings from caching (assuming $0.0004 per query for embedding)
                embedding_cost_per_query = 0.0004
                cache_cost_savings = cache_hits * embedding_cost_per_query

                # Time savings (cached vs uncached)
                avg_cached = query_row[5] or 0
                avg_uncached = query_row[6] or 0
                time_savings_ms = (avg_uncached - avg_cached) * cache_hits if avg_uncached > avg_cached else 0

                return {
                    "period_days": days,
                    "query_volume": {
                        "total": total_queries,
                        "cache_hits": cache_hits,
                        "cache_hit_rate_pct": round(cache_hit_rate, 2),
                        "high_intent": high_intent_queries,
                        "high_intent_rate_pct": round(high_intent_rate, 2),
                        "converted": converted_queries,
                        "conversion_rate_pct": round(conversion_rate, 2)
                    },
                    "performance": {
                        "avg_query_time_ms": round(query_row[4], 2) if query_row[4] else 0,
                        "avg_cached_time_ms": round(avg_cached, 2),
                        "avg_uncached_time_ms": round(avg_uncached, 2),
                        "time_savings_hours": round(time_savings_ms / 1000 / 3600, 2)
                    },
                    "cost_efficiency": {
                        "cache_cost_savings_usd": round(cache_cost_savings, 2),
                        "estimated_monthly_savings_usd": round(cache_cost_savings / days * 30, 2)
                    },
                    "revenue_attribution": {
                        "total_revenue_usd": round(total_revenue, 2),
                        "average_deal_size_usd": round(avg_deal_size, 2),
                        "roi_multiple": round(total_revenue / max(cache_cost_savings, 1), 2)
                    },
                    "conversion_funnel": conversion_funnel,
                    "agent_performance": agent_performance,
                    "investor_claims_validation": {
                        "claim_cache_hit_rate_target": "31%",
                        "actual_cache_hit_rate": f"{round(cache_hit_rate, 1)}%",
                        "claim_time_savings_target": "40% faster",
                        "actual_time_savings": f"{round((1 - avg_cached/max(avg_uncached, 1)) * 100, 1)}%" if avg_uncached > 0 else "N/A",
                        "claim_cost_reduction_target": "25-30%",
                        "actual_cost_reduction": f"{round(cache_cost_savings / (total_queries * embedding_cost_per_query) * 100, 1)}%" if total_queries > 0 else "0%"
                    }
                }

        except Exception as e:
            logger.error(f"Error generating ROI dashboard: {e}")
            return {"error": str(e)}
