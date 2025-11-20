#!/usr/bin/env python3
"""
Circuit OS RAG Worker Agent
Wraps existing RAG pipeline for orchestrator compatibility.

This makes our production RAG system (adaptive_rag_api.py) callable
by the orchestrator as a first-class worker agent.
"""

import logging
from typing import Dict, Any
from orchestrator_core import WorkerAgent, AgentCapability
from rag_core import RAGPipeline
from rag_adaptive import QueryRouter, SemanticCache, FeedbackReranker
import os

logger = logging.getLogger(__name__)


class RAGWorkerAgent(WorkerAgent):
    """
    Knowledge retrieval agent using Circuit OS Adaptive RAG stack.

    Capabilities:
    - URL-based document ingestion
    - Semantic search with quality gates
    - Multi-tier query routing
    - Feedback-driven reranking

    Governance features (already built):
    - Query logging for explainability
    - Quality gate validation
    - Cache performance tracking
    """

    def __init__(self):
        super().__init__(
            agent_id="rag_worker_001",
            name="RAG Worker",
            capabilities=[AgentCapability.KNOWLEDGE_RETRIEVAL]
        )

        # Initialize RAG pipeline
        database_url = os.getenv(
            'RAG_DATABASE_URL',
            os.getenv('DATABASE_URL', 'postgresql://circuitos:changeme@localhost:5432/agentforce')
        )
        embedding_model = os.getenv('RAG_EMBEDDING_MODEL', 'all-MiniLM-L6-v2')

        try:
            self.rag_pipeline = RAGPipeline(database_url, embedding_model)
            self.query_router = QueryRouter(openai_api_key=os.getenv('OPENAI_API_KEY'))
            self.status = "ready"
            logger.info("✅ RAG Worker initialized with adaptive pipeline")

        except Exception as e:
            logger.error(f"❌ RAG Worker initialization failed: {e}")
            self.status = "failed"
            self.rag_pipeline = None

    def can_handle(self, task_type: str) -> bool:
        """Check if this agent can handle task type"""
        supported_tasks = [
            "knowledge_retrieval",
            "document_ingest",
            "semantic_search"
        ]
        return task_type in supported_tasks

    def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute RAG task through orchestrator"""
        if not self.rag_pipeline:
            return {
                "success": False,
                "error": "RAG pipeline not initialized"
            }

        task_type = task.get("task_type")
        task_data = task.get("task_data", {})

        logger.info(f"🔍 RAG Worker executing: {task_type}")

        try:
            if task_type == "knowledge_retrieval":
                return self._retrieve_knowledge(task_data)
            elif task_type == "document_ingest":
                return self._ingest_document(task_data)
            elif task_type == "semantic_search":
                return self._semantic_search(task_data)
            else:
                return {
                    "success": False,
                    "error": f"Unsupported task type: {task_type}"
                }

        except Exception as e:
            logger.error(f"❌ RAG Worker execution failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "task_type": task_type
            }

    def _retrieve_knowledge(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Retrieve relevant documents for a query.

        Uses the full adaptive RAG pipeline:
        - Query routing (no_retrieval, single_step, multi_step)
        - Semantic search with quality gates
        - Feedback reranking
        """
        query = data.get("query")
        limit = data.get("limit", 5)
        threshold = data.get("threshold", 0.5)

        if not query:
            return {"success": False, "error": "query required"}

        # Step 1: Route query
        route_info = self.query_router.classify_query(query)
        logger.info(f"Query routed to: {route_info['route']}")

        # If query doesn't need retrieval, return early
        if route_info['route'] == 'no_retrieval':
            return {
                "success": True,
                "query": query,
                "route": "no_retrieval",
                "results": [],
                "message": "Query does not require knowledge base retrieval"
            }

        # Step 2: Retrieve from vector store
        results = self.rag_pipeline.query(query, limit, threshold)

        # Step 3: Return structured results
        return {
            "success": True,
            "query": query,
            "route": route_info['route'],
            "results": results,
            "count": len(results),
            "retrieval_metadata": {
                "limit": limit,
                "threshold": threshold,
                "embedding_model": self.rag_pipeline.embedder.model_name
            }
        }

    def _ingest_document(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Ingest a URL into the knowledge base.

        Returns document ID and chunk count for tracking.
        """
        url = data.get("url")
        metadata = data.get("metadata", {})

        if not url:
            return {"success": False, "error": "url required"}

        try:
            result = self.rag_pipeline.ingest_url(url, metadata)
            return result

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "url": url
            }

    def _semantic_search(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Direct semantic search (bypasses query router).

        Useful for when orchestrator knows retrieval is needed.
        """
        query = data.get("query")
        limit = data.get("limit", 10)
        threshold = data.get("threshold", 0.3)

        if not query:
            return {"success": False, "error": "query required"}

        results = self.rag_pipeline.query(query, limit, threshold)

        return {
            "success": True,
            "query": query,
            "results": results,
            "count": len(results)
        }

    def health_check(self) -> bool:
        """Check if RAG worker is healthy"""
        if not self.rag_pipeline:
            return False

        try:
            # Test database connection
            with self.rag_pipeline.store.conn.cursor() as cur:
                cur.execute("SELECT 1;")
            return True

        except Exception as e:
            logger.error(f"RAG Worker health check failed: {e}")
            return False
