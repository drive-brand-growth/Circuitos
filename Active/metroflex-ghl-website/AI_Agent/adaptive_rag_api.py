#!/usr/bin/env python3
"""
Circuit OS Adaptive RAG API
Provides endpoints for URL ingestion, RAG query, and feedback collection.
"""

import os
import logging
from flask import Blueprint, request, jsonify
from rag_core import RAGPipeline

logger = logging.getLogger(__name__)

# Create Blueprint for RAG API
rag_api = Blueprint('rag_api', __name__, url_prefix='/api/rag')

# Initialize RAG Pipeline (lazy loading)
_rag_pipeline = None


def get_rag_pipeline():
    """Get or initialize RAG pipeline"""
    global _rag_pipeline
    if _rag_pipeline is None:
        database_url = os.getenv(
            'RAG_DATABASE_URL',
            os.getenv('DATABASE_URL', 'postgresql://circuitos:changeme@localhost:5432/agentforce')
        )
        embedding_model = os.getenv('RAG_EMBEDDING_MODEL', 'all-MiniLM-L6-v2')

        try:
            _rag_pipeline = RAGPipeline(database_url, embedding_model)
            logger.info("RAG Pipeline initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize RAG Pipeline: {e}")
            raise

    return _rag_pipeline


# =============================================================================
# INGEST URL ENDPOINT
# =============================================================================

@rag_api.route('/ingest_url', methods=['POST'])
def ingest_url():
    """
    Ingest a URL into the RAG knowledge base.

    Request:
    {
        "url": "https://example.com/page",
        "metadata": {  // Optional
            "category": "events",
            "source": "npc",
            "priority": "high"
        }
    }

    Response:
    {
        "success": true,
        "document_id": 123,
        "url": "https://example.com/page",
        "title": "Page Title",
        "chunks_created": 15,
        "content_hash": "abc123..."
    }
    """
    try:
        data = request.json or {}
        url = data.get('url')

        if not url:
            return jsonify({
                'success': False,
                'error': 'URL is required'
            }), 400

        # Validate URL format
        if not url.startswith(('http://', 'https://')):
            return jsonify({
                'success': False,
                'error': 'Invalid URL format. Must start with http:// or https://'
            }), 400

        metadata = data.get('metadata', {})

        # Get pipeline and ingest
        pipeline = get_rag_pipeline()
        result = pipeline.ingest_url(url, metadata)

        if result['success']:
            logger.info(f"Successfully ingested: {url} ({result['chunks_created']} chunks)")
            return jsonify(result), 200
        else:
            logger.warning(f"Ingestion failed: {url} - {result.get('error')}")
            return jsonify(result), 500

    except Exception as e:
        logger.error(f"Error in ingest_url: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@rag_api.route('/ingest_batch', methods=['POST'])
def ingest_batch():
    """
    Ingest multiple URLs in batch.

    Request:
    {
        "urls": [
            {"url": "https://example1.com", "metadata": {...}},
            {"url": "https://example2.com", "metadata": {...}}
        ]
    }

    Response:
    {
        "total": 2,
        "successful": 2,
        "failed": 0,
        "results": [...]
    }
    """
    try:
        data = request.json or {}
        urls = data.get('urls', [])

        if not urls:
            return jsonify({
                'success': False,
                'error': 'URLs array is required'
            }), 400

        pipeline = get_rag_pipeline()
        results = []
        successful = 0
        failed = 0

        for item in urls:
            url = item.get('url') if isinstance(item, dict) else item
            metadata = item.get('metadata', {}) if isinstance(item, dict) else {}

            if not url:
                results.append({'success': False, 'error': 'Missing URL'})
                failed += 1
                continue

            result = pipeline.ingest_url(url, metadata)
            results.append(result)

            if result['success']:
                successful += 1
            else:
                failed += 1

        return jsonify({
            'total': len(urls),
            'successful': successful,
            'failed': failed,
            'results': results
        }), 200

    except Exception as e:
        logger.error(f"Error in ingest_batch: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# =============================================================================
# QUERY ENDPOINT
# =============================================================================

@rag_api.route('/query', methods=['POST'])
def query():
    """
    Query the RAG knowledge base.

    Request:
    {
        "query": "What are the 2026 Better Bodies Classic rules?",
        "limit": 5,  // Optional, default 5
        "threshold": 0.5  // Optional, similarity threshold
    }

    Response:
    {
        "query": "...",
        "results": [
            {
                "chunk_id": "abc123",
                "text": "The relevant content...",
                "url": "https://source.com/page",
                "title": "Page Title",
                "similarity": 0.89,
                "metadata": {...}
            }
        ],
        "count": 3
    }
    """
    try:
        data = request.json or {}
        query_text = data.get('query')

        if not query_text:
            return jsonify({
                'success': False,
                'error': 'Query is required'
            }), 400

        limit = data.get('limit', 5)
        threshold = data.get('threshold', 0.5)

        pipeline = get_rag_pipeline()
        results = pipeline.query(query_text, limit, threshold)

        return jsonify({
            'query': query_text,
            'results': results,
            'count': len(results)
        }), 200

    except Exception as e:
        logger.error(f"Error in query: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# =============================================================================
# FEEDBACK ENDPOINT
# =============================================================================

@rag_api.route('/feedback', methods=['POST'])
def feedback():
    """
    Submit feedback for adaptive RAG improvement.

    Request:
    {
        "feedback_type": "helpful" | "unhelpful" | "outdated" | "low_quality" | "re_crawl",
        "chunk_id": "abc123",  // Optional
        "document_id": 123,  // Optional
        "value": 1,  // Optional, -1 to 1 scale
        "comment": "This info is outdated",  // Optional
        "agent_id": "licensing_agent",  // Optional
        "query": "original query text"  // Optional
    }

    Response:
    {
        "success": true,
        "feedback_id": 456
    }
    """
    try:
        data = request.json or {}
        feedback_type = data.get('feedback_type')

        if not feedback_type:
            return jsonify({
                'success': False,
                'error': 'feedback_type is required'
            }), 400

        valid_types = ['helpful', 'unhelpful', 'outdated', 'low_quality', 're_crawl', 'incorrect']
        if feedback_type not in valid_types:
            return jsonify({
                'success': False,
                'error': f'Invalid feedback_type. Must be one of: {valid_types}'
            }), 400

        chunk_id = data.get('chunk_id')
        document_id = data.get('document_id')

        if not chunk_id and not document_id:
            return jsonify({
                'success': False,
                'error': 'Either chunk_id or document_id is required'
            }), 400

        # Convert feedback type to value if not provided
        value = data.get('value')
        if value is None:
            value_map = {
                'helpful': 1,
                'unhelpful': -1,
                'outdated': -1,
                'low_quality': -1,
                're_crawl': 0,
                'incorrect': -1
            }
            value = value_map.get(feedback_type, 0)

        pipeline = get_rag_pipeline()
        feedback_id = pipeline.add_feedback(
            feedback_type=feedback_type,
            chunk_id=chunk_id,
            document_id=document_id,
            value=value,
            comment=data.get('comment'),
            agent_id=data.get('agent_id'),
            query=data.get('query')
        )

        logger.info(f"Feedback recorded: {feedback_type} for chunk={chunk_id}, doc={document_id}")

        return jsonify({
            'success': True,
            'feedback_id': feedback_id
        }), 200

    except Exception as e:
        logger.error(f"Error in feedback: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# =============================================================================
# MANAGEMENT ENDPOINTS
# =============================================================================

@rag_api.route('/documents', methods=['GET'])
def list_documents():
    """
    List all ingested documents.

    Query params:
    - status: filter by status (active, archived)
    - limit: max results (default 50)
    """
    try:
        pipeline = get_rag_pipeline()
        status = request.args.get('status', 'active')
        limit = int(request.args.get('limit', 50))

        with pipeline.store.conn.cursor() as cur:
            cur.execute("""
                SELECT id, url, title, meta_description, ingested_at, last_updated, status,
                    (SELECT COUNT(*) FROM rag_chunks WHERE document_id = rag_documents.id) as chunk_count
                FROM rag_documents
                WHERE status = %s
                ORDER BY last_updated DESC
                LIMIT %s;
            """, (status, limit))

            documents = []
            for row in cur.fetchall():
                documents.append({
                    'id': row[0],
                    'url': row[1],
                    'title': row[2],
                    'meta_description': row[3],
                    'ingested_at': row[4].isoformat() if row[4] else None,
                    'last_updated': row[5].isoformat() if row[5] else None,
                    'status': row[6],
                    'chunk_count': row[7]
                })

        return jsonify({
            'documents': documents,
            'count': len(documents)
        }), 200

    except Exception as e:
        logger.error(f"Error listing documents: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@rag_api.route('/stale', methods=['GET'])
def get_stale_documents():
    """
    Get documents that need re-ingestion based on age or feedback.

    Query params:
    - days: age threshold in days (default 7)
    """
    try:
        pipeline = get_rag_pipeline()
        days = int(request.args.get('days', 7))

        stale = pipeline.get_documents_to_reingest(days)

        return jsonify({
            'stale_documents': stale,
            'count': len(stale),
            'threshold_days': days
        }), 200

    except Exception as e:
        logger.error(f"Error getting stale documents: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@rag_api.route('/reingest/<int:document_id>', methods=['POST'])
def reingest_document(document_id):
    """
    Re-ingest a specific document by ID.
    """
    try:
        pipeline = get_rag_pipeline()
        result = pipeline.reingest_document(document_id)

        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 404

    except Exception as e:
        logger.error(f"Error re-ingesting document {document_id}: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@rag_api.route('/health', methods=['GET'])
def rag_health():
    """Health check for RAG system"""
    try:
        pipeline = get_rag_pipeline()

        # Test database connection
        with pipeline.store.conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM rag_documents;")
            doc_count = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM rag_chunks;")
            chunk_count = cur.fetchone()[0]

        return jsonify({
            'status': 'healthy',
            'documents': doc_count,
            'chunks': chunk_count,
            'embedding_model': pipeline.embedder.model_name,
            'embedding_dim': pipeline.embedder.embedding_dim
        }), 200

    except Exception as e:
        logger.error(f"RAG health check failed: {e}")
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 503


# =============================================================================
# GHL WEBHOOK INTEGRATION
# =============================================================================

@rag_api.route('/webhooks/ghl/page_visited', methods=['POST'])
def ghl_page_visited():
    """
    Webhook for when a GHL contact visits a page.
    Auto-indexes the page for future RAG queries.

    Request (from GHL):
    {
        "contact_id": "ghl_xyz123",
        "page_url": "https://metroflex.com/events/2026-classic",
        "timestamp": "2025-01-15T10:30:00Z"
    }
    """
    try:
        data = request.json or {}
        page_url = data.get('page_url')
        contact_id = data.get('contact_id')

        if not page_url:
            return jsonify({'success': False, 'error': 'page_url required'}), 400

        # Auto-ingest the visited page
        pipeline = get_rag_pipeline()
        result = pipeline.ingest_url(page_url, metadata={
            'source': 'ghl_page_visit',
            'contact_id': contact_id,
            'auto_indexed': True
        })

        logger.info(f"GHL page visit indexed: {page_url} (contact: {contact_id})")

        return jsonify({
            'success': result['success'],
            'message': 'Page indexed for RAG',
            'document_id': result.get('document_id'),
            'chunks_created': result.get('chunks_created', 0)
        }), 200

    except Exception as e:
        logger.error(f"Error in GHL page_visited webhook: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@rag_api.route('/webhooks/ghl/lead_created', methods=['POST'])
def ghl_lead_created():
    """
    Webhook for when a GHL lead is created.
    Can trigger context enrichment based on lead source.
    """
    try:
        data = request.json or {}
        contact_id = data.get('contact_id')
        lead_source = data.get('lead_source')
        source_url = data.get('source_url')

        # If lead came from a specific page, ensure it's indexed
        if source_url:
            pipeline = get_rag_pipeline()
            result = pipeline.ingest_url(source_url, metadata={
                'source': 'ghl_lead_source',
                'contact_id': contact_id,
                'lead_source': lead_source
            })

            return jsonify({
                'success': True,
                'message': 'Lead source page indexed',
                'document_id': result.get('document_id')
            }), 200

        return jsonify({
            'success': True,
            'message': 'Lead created event received'
        }), 200

    except Exception as e:
        logger.error(f"Error in GHL lead_created webhook: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
