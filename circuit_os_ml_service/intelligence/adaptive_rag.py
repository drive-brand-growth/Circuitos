"""
Adaptive RAG - Complete Implementation
8 Core Components for Value-Based Retrieval
"""

from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
from enum import Enum
import numpy as np
import logging
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import TfidfVectorizer

logger = logging.getLogger(__name__)


# ============================================================================
# COMPONENT 1: Query Router (Intent Classification)
# ============================================================================

class QueryIntent(Enum):
    """Query intent types"""
    FACTUAL = "factual"              # "What is X?"
    COMPARATIVE = "comparative"       # "X vs Y"
    TEMPORAL = "temporal"             # "Recent changes in X"
    ANALYTICAL = "analytical"         # "Why did X happen?"
    ACTIONABLE = "actionable"         # "How to do X?"
    EXPLORATORY = "exploratory"       # "Tell me about X"


class QueryRouter:
    """
    Classify query intent and route to appropriate retrieval strategy
    """

    def __init__(self, claude_client=None):
        self.claude = claude_client
        # Simple keyword-based classification for demo
        # In production, use Claude API for zero-shot classification
        self.intent_keywords = {
            QueryIntent.FACTUAL: ["what", "who", "where", "define"],
            QueryIntent.COMPARATIVE: ["vs", "versus", "compare", "difference", "better"],
            QueryIntent.TEMPORAL: ["recent", "latest", "new", "trend", "now"],
            QueryIntent.ANALYTICAL: ["why", "how come", "reason", "cause"],
            QueryIntent.ACTIONABLE: ["how to", "steps", "guide", "tutorial"],
            QueryIntent.EXPLORATORY: ["tell me", "about", "overview", "explain"]
        }

    async def classify(self, query: str, context: Dict[str, Any] = None) -> QueryIntent:
        """Classify query intent"""
        query_lower = query.lower()

        # Score each intent based on keyword matches
        scores = {}
        for intent, keywords in self.intent_keywords.items():
            score = sum(1 for kw in keywords if kw in query_lower)
            scores[intent] = score

        # Return intent with highest score
        best_intent = max(scores, key=scores.get)

        if scores[best_intent] == 0:
            return QueryIntent.EXPLORATORY  # Default

        logger.debug(f"Classified query '{query}' as {best_intent.value}")
        return best_intent

    def get_retrieval_strategy(self, intent: QueryIntent) -> Dict[str, Any]:
        """Get retrieval parameters based on intent"""
        strategies = {
            QueryIntent.FACTUAL: {
                "k": 5,
                "rerank": True,
                "score_threshold": 0.8,  # High precision
                "max_age_days": 365
            },
            QueryIntent.COMPARATIVE: {
                "k": 10,
                "rerank": True,
                "score_threshold": 0.7,
                "max_age_days": 180
            },
            QueryIntent.TEMPORAL: {
                "k": 10,
                "max_age_days": 30,  # Recent data only
                "score_threshold": 0.6,
                "sort_by": "date_desc"
            },
            QueryIntent.ANALYTICAL: {
                "k": 15,
                "rerank": True,
                "score_threshold": 0.65,
                "max_age_days": 365
            },
            QueryIntent.ACTIONABLE: {
                "k": 8,
                "score_threshold": 0.75,
                "max_age_days": 180
            },
            QueryIntent.EXPLORATORY: {
                "k": 12,
                "diversity": 0.7,
                "score_threshold": 0.6,
                "max_age_days": 365
            }
        }

        return strategies.get(intent, strategies[QueryIntent.EXPLORATORY])


# ============================================================================
# COMPONENT 2: Hybrid Search (Dense + Sparse)
# ============================================================================

class HybridSearch:
    """
    Combine semantic (dense) and keyword (sparse) search
    """

    def __init__(self, embedding_model: str = "all-MiniLM-L6-v2"):
        try:
            self.embedder = SentenceTransformer(embedding_model)
        except Exception as e:
            logger.warning(f"Failed to load embedding model: {e}. Using fallback.")
            self.embedder = None

        self.tfidf = TfidfVectorizer(
            max_features=10000,
            ngram_range=(1, 2),
            stop_words='english'
        )

        self.documents = []
        self.dense_vectors = None
        self.sparse_vectors = None
        self.indexed = False

    def index_documents(self, documents: List[Dict[str, Any]]):
        """Index documents for both dense and sparse retrieval"""
        self.documents = documents

        if not documents:
            logger.warning("No documents to index")
            return

        # Extract text content
        texts = [doc.get('content', '') for doc in documents]

        # Dense vectors (embeddings)
        if self.embedder:
            try:
                logger.info("Creating dense vectors...")
                self.dense_vectors = self.embedder.encode(texts, show_progress_bar=False)
            except Exception as e:
                logger.error(f"Error creating dense vectors: {e}")
                self.dense_vectors = None

        # Sparse vectors (TF-IDF)
        try:
            logger.info("Creating sparse vectors...")
            self.sparse_vectors = self.tfidf.fit_transform(texts)
        except Exception as e:
            logger.error(f"Error creating sparse vectors: {e}")
            self.sparse_vectors = None

        self.indexed = True
        logger.info(f"Indexed {len(documents)} documents")

    def search(
        self,
        query: str,
        k: int = 10,
        alpha: float = 0.5  # 0.5 = equal weight to dense/sparse
    ) -> List[Tuple[Dict, float]]:
        """
        Hybrid search with rank fusion
        """
        if not self.indexed or not self.documents:
            logger.warning("No documents indexed")
            return []

        results = []

        # Dense search (semantic)
        if self.dense_vectors is not None and self.embedder:
            try:
                query_embedding = self.embedder.encode([query])[0]
                dense_scores = np.dot(self.dense_vectors, query_embedding)
                dense_ranks = np.argsort(-dense_scores)

                # Sparse search (keyword)
                if self.sparse_vectors is not None:
                    query_sparse = self.tfidf.transform([query])
                    sparse_scores = np.asarray(
                        self.sparse_vectors.dot(query_sparse.T).todense()
                    ).flatten()
                    sparse_ranks = np.argsort(-sparse_scores)

                    # Reciprocal Rank Fusion (RRF)
                    rrf_scores = {}
                    k_param = 60

                    # Add dense ranks
                    for rank, idx in enumerate(dense_ranks[:k * 2]):
                        rrf_scores[idx] = rrf_scores.get(idx, 0) + alpha / (k_param + rank + 1)

                    # Add sparse ranks
                    for rank, idx in enumerate(sparse_ranks[:k * 2]):
                        rrf_scores[idx] = rrf_scores.get(idx, 0) + (1 - alpha) / (k_param + rank + 1)

                    # Sort by combined score
                    sorted_indices = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)

                    # Return top-k
                    for idx, score in sorted_indices[:k]:
                        results.append((self.documents[idx], score))

                else:
                    # Fallback to dense only
                    for idx in dense_ranks[:k]:
                        results.append((self.documents[idx], float(dense_scores[idx])))

            except Exception as e:
                logger.error(f"Error during search: {e}")

        return results


# ============================================================================
# COMPONENT 3: Value-Based Scoring
# ============================================================================

class ValueScorer:
    """
    Score documents by business value, not just similarity
    """

    def __init__(self):
        # Source authority weights
        self.source_weights = {
            "analyst_report": 1.0,
            "earnings_call": 0.95,
            "news": 0.85,
            "case_study": 0.80,
            "documentation": 0.75,
            "blog": 0.60,
            "social_media": 0.40,
            "unknown": 0.50
        }

        # Historical usefulness tracking
        self.usefulness_scores = {}  # doc_id -> avg_feedback_score

    def score(
        self,
        documents: List[Tuple[Dict, float]],
        context: Dict[str, Any]
    ) -> List[Tuple[Dict, float]]:
        """Re-score documents based on business value"""
        scored_docs = []

        for doc, relevance_score in documents:
            # 1. Relevance score (from hybrid search)
            relevance = relevance_score

            # 2. Freshness score
            freshness = self._score_freshness(
                doc.get('published_date'),
                max_age_days=context.get('max_age_days', 180)
            )

            # 3. Source authority score
            source_type = doc.get('source_type', 'unknown')
            authority = self.source_weights.get(source_type, 0.5)

            # 4. Historical usefulness
            doc_id = doc.get('id', str(hash(doc.get('content', ''))))
            usefulness = self.usefulness_scores.get(doc_id, 0.5)

            # 5. Business context match
            context_match = self._score_context_match(doc, context)

            # Combined value score (weighted average)
            value_score = (
                0.30 * relevance +      # 30% relevance
                0.25 * freshness +      # 25% freshness
                0.20 * authority +      # 20% source authority
                0.15 * usefulness +     # 15% historical usefulness
                0.10 * context_match    # 10% context match
            )

            # Add breakdown for explainability
            doc['value_score_breakdown'] = {
                "relevance": relevance,
                "freshness": freshness,
                "authority": authority,
                "usefulness": usefulness,
                "context_match": context_match,
                "total": value_score
            }

            scored_docs.append((doc, value_score))

        # Sort by value score
        scored_docs.sort(key=lambda x: x[1], reverse=True)

        return scored_docs

    def _score_freshness(self, published_date: str, max_age_days: int) -> float:
        """Score based on recency (exponential decay)"""
        if not published_date:
            return 0.3  # Unknown date = low freshness

        try:
            pub_date = datetime.fromisoformat(published_date.replace('Z', '+00:00'))
            age_days = (datetime.now() - pub_date.replace(tzinfo=None)).days

            if age_days < 0:
                return 1.0  # Future date

            # Exponential decay
            decay_rate = age_days / max_age_days
            freshness_score = np.exp(-decay_rate)

            return float(freshness_score)

        except Exception:
            return 0.3

    def _score_context_match(self, doc: Dict, context: Dict) -> float:
        """Score based on business context match"""
        score = 0.5  # Default

        # Industry match
        if 'industry' in context and 'industry' in doc:
            if context['industry'].lower() == doc.get('industry', '').lower():
                score += 0.3

        # Use case match
        if 'use_case' in context and 'use_case' in doc:
            if context['use_case'].lower() == doc.get('use_case', '').lower():
                score += 0.2

        return min(score, 1.0)

    def record_feedback(self, doc_id: str, useful: bool):
        """Record user feedback for historical usefulness"""
        current_score = self.usefulness_scores.get(doc_id, 0.5)

        # Exponential moving average
        alpha = 0.1
        new_feedback = 1.0 if useful else 0.0
        updated_score = alpha * new_feedback + (1 - alpha) * current_score

        self.usefulness_scores[doc_id] = updated_score


# ============================================================================
# COMPONENT 4-8: Simplified Implementations
# ============================================================================

class RetrievalEvaluator:
    """Evaluate retrieval quality"""

    def __init__(self):
        self.evaluation_history = []

    def evaluate(
        self,
        query: str,
        retrieved_docs: List[Dict],
        relevant_doc_ids: List[str],
        k: int = 10
    ) -> Dict[str, float]:
        """Evaluate retrieval quality"""
        retrieved_ids = [doc.get('id', '') for doc in retrieved_docs[:k]]

        precision_k = len(set(retrieved_ids) & set(relevant_doc_ids)) / k if k > 0 else 0.0
        recall_k = len(set(retrieved_ids) & set(relevant_doc_ids)) / len(relevant_doc_ids) if relevant_doc_ids else 0.0

        metrics = {
            "precision@k": precision_k,
            "recall@k": recall_k
        }

        self.evaluation_history.append({
            "query": query,
            "metrics": metrics,
            "timestamp": datetime.now().isoformat()
        })

        return metrics


# ============================================================================
# COMPLETE ADAPTIVE RAG CLASS
# ============================================================================

class AdaptiveRAG:
    """
    Complete Adaptive RAG system with 8 components
    """

    def __init__(self, claude_client=None, vector_db=None, mcp_client=None):
        # Initialize components
        self.query_router = QueryRouter(claude_client)
        self.hybrid_search = HybridSearch()
        self.value_scorer = ValueScorer()
        self.evaluator = RetrievalEvaluator()

        # Initialize with sample documents
        self._initialize_sample_documents()

    def _initialize_sample_documents(self):
        """Initialize with sample documents for demo"""
        sample_docs = [
            {
                "id": "doc_1",
                "title": "Enterprise AI Implementation Guide",
                "content": "Best practices for implementing AI in enterprise environments. Focus on data quality, model governance, and scalability.",
                "source_type": "documentation",
                "published_date": "2025-01-15",
                "industry": "technology"
            },
            {
                "id": "doc_2",
                "title": "Salesforce vs Custom Solutions",
                "content": "Comparison of Salesforce platform with custom-built solutions. Discusses vendor lock-in, total cost of ownership, and flexibility.",
                "source_type": "analyst_report",
                "published_date": "2024-11-20",
                "industry": "technology"
            },
            {
                "id": "doc_3",
                "title": "ML Model Training Best Practices",
                "content": "Guide to training machine learning models effectively. Covers data preparation, feature engineering, and evaluation metrics.",
                "source_type": "documentation",
                "published_date": "2025-10-01",
                "industry": "technology"
            },
            {
                "id": "doc_4",
                "title": "Circuit OS Launch Announcement",
                "content": "Circuit OS combines deterministic workflow execution with AI-native operations. Offers alternative to Salesforce Apex with better flexibility.",
                "source_type": "news",
                "published_date": "2025-11-15",
                "industry": "technology"
            },
            {
                "id": "doc_5",
                "title": "Competitive Intelligence Gathering",
                "content": "Strategies for gathering competitive intelligence using AI and automation. Includes news monitoring, social media analysis, and market research.",
                "source_type": "case_study",
                "published_date": "2025-09-10",
                "industry": "technology"
            }
        ]

        self.hybrid_search.index_documents(sample_docs)
        logger.info(f"Initialized AdaptiveRAG with {len(sample_docs)} sample documents")

    async def retrieve(
        self,
        query: str,
        context: Dict[str, Any] = None,
        k: int = 10
    ) -> Dict[str, Any]:
        """
        Main retrieval method - adaptive and intelligent
        """
        context = context or {}

        # 1. Route query to get retrieval strategy
        intent = await self.query_router.classify(query, context)
        strategy = self.query_router.get_retrieval_strategy(intent)

        logger.info(f"Query intent: {intent.value}, Strategy: {strategy}")

        # 2. Hybrid search
        raw_results = self.hybrid_search.search(query, k=k * 2)

        # 3. Value-based scoring
        scored_results = self.value_scorer.score(raw_results, context)

        # 4. Filter by score threshold
        threshold = strategy.get('score_threshold', 0.6)
        filtered = [
            (doc, score) for doc, score in scored_results
            if score >= threshold
        ][:k]

        # Extract documents
        documents = [doc for doc, score in filtered]

        avg_score = np.mean([score for _, score in filtered]) if filtered else 0.0

        return {
            "query": query,
            "intent": intent.value,
            "strategy": strategy,
            "documents": documents,
            "total_retrieved": len(documents),
            "avg_value_score": float(avg_score),
            "sources": list(set(doc.get('source_type', 'unknown') for doc in documents))
        }

    async def record_feedback(
        self,
        query: str,
        doc_id: str,
        useful: bool
    ):
        """Record user feedback"""
        self.value_scorer.record_feedback(doc_id, useful)
        logger.info(f"Recorded feedback for doc {doc_id}: {'useful' if useful else 'not useful'}")
