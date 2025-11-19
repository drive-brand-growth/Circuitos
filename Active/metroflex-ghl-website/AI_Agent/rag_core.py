#!/usr/bin/env python3
"""
Circuit OS Adaptive RAG Core - Modular Components
Provides chunking, cleaning, embedding, and vector storage functionality.
"""

import re
import hashlib
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import trafilatura
import psycopg2
from psycopg2.extras import execute_values
import numpy as np
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)


# =============================================================================
# CONTENT EXTRACTION
# =============================================================================

class ContentExtractor:
    """Extracts readable content from web pages"""

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; CircuitOS-RAG/1.0; +https://circuitos.ai)'
        }

    def fetch_url(self, url: str, timeout: int = 30) -> str:
        """Fetch raw HTML from URL"""
        try:
            response = requests.get(url, headers=self.headers, timeout=timeout)
            response.raise_for_status()
            return response.text
        except Exception as e:
            logger.error(f"Failed to fetch {url}: {e}")
            raise

    def extract_content(self, html: str, url: str = None) -> Dict[str, Any]:
        """Extract main content from HTML using trafilatura"""
        # Try trafilatura first (best for article extraction)
        content = trafilatura.extract(
            html,
            include_links=False,
            include_images=False,
            include_tables=True,
            favor_precision=True
        )

        # Fallback to BeautifulSoup if trafilatura fails
        if not content:
            soup = BeautifulSoup(html, 'html.parser')

            # Remove script, style, nav, footer elements
            for element in soup(['script', 'style', 'nav', 'footer', 'header', 'aside']):
                element.decompose()

            content = soup.get_text(separator='\n', strip=True)

        # Extract metadata
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.title.string if soup.title else ''
        meta_desc = ''
        meta_tag = soup.find('meta', attrs={'name': 'description'})
        if meta_tag:
            meta_desc = meta_tag.get('content', '')

        return {
            'content': content,
            'title': title.strip() if title else '',
            'meta_description': meta_desc,
            'url': url,
            'extracted_at': datetime.utcnow().isoformat()
        }

    def crawl_url(self, url: str) -> Dict[str, Any]:
        """Complete crawl pipeline: fetch + extract"""
        html = self.fetch_url(url)
        return self.extract_content(html, url)


# =============================================================================
# TEXT CLEANING
# =============================================================================

class TextCleaner:
    """Cleans and normalizes extracted text"""

    def __init__(self):
        # Patterns to remove
        self.patterns = [
            (r'\s+', ' '),  # Multiple whitespace to single
            (r'\n{3,}', '\n\n'),  # Multiple newlines to double
            (r'[^\S\n]+', ' '),  # Non-newline whitespace
            (r'(?m)^\s+$', ''),  # Blank lines
        ]

    def clean(self, text: str) -> str:
        """Apply all cleaning operations"""
        if not text:
            return ''

        # Basic normalization
        text = text.strip()

        # Apply regex patterns
        for pattern, replacement in self.patterns:
            text = re.sub(pattern, replacement, text)

        # Remove common boilerplate phrases
        boilerplate = [
            'cookie policy',
            'privacy policy',
            'terms of service',
            'all rights reserved',
            'subscribe to our newsletter',
            'follow us on social media',
        ]

        lines = text.split('\n')
        cleaned_lines = []
        for line in lines:
            if not any(bp in line.lower() for bp in boilerplate):
                cleaned_lines.append(line)

        return '\n'.join(cleaned_lines).strip()

    def normalize_whitespace(self, text: str) -> str:
        """Normalize whitespace while preserving structure"""
        lines = text.split('\n')
        normalized = []
        for line in lines:
            normalized.append(' '.join(line.split()))
        return '\n'.join(normalized)


# =============================================================================
# TEXT CHUNKING
# =============================================================================

class SemanticChunker:
    """Splits text into semantic chunks for embedding"""

    def __init__(
        self,
        chunk_size: int = 512,
        chunk_overlap: int = 50,
        min_chunk_size: int = 100
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.min_chunk_size = min_chunk_size

    def chunk_text(self, text: str, metadata: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Split text into overlapping chunks with metadata"""
        if not text:
            return []

        # Split by paragraphs first
        paragraphs = text.split('\n\n')

        chunks = []
        current_chunk = []
        current_size = 0

        for para in paragraphs:
            para = para.strip()
            if not para:
                continue

            para_words = para.split()
            para_size = len(para_words)

            # If paragraph alone exceeds chunk size, split it
            if para_size > self.chunk_size:
                # Flush current chunk first
                if current_chunk:
                    chunk_text = ' '.join(current_chunk)
                    if len(chunk_text.split()) >= self.min_chunk_size:
                        chunks.append(self._create_chunk(chunk_text, len(chunks), metadata))
                    current_chunk = []
                    current_size = 0

                # Split large paragraph
                words = para_words
                for i in range(0, len(words), self.chunk_size - self.chunk_overlap):
                    chunk_words = words[i:i + self.chunk_size]
                    chunk_text = ' '.join(chunk_words)
                    if len(chunk_words) >= self.min_chunk_size:
                        chunks.append(self._create_chunk(chunk_text, len(chunks), metadata))

            # Add paragraph to current chunk
            elif current_size + para_size <= self.chunk_size:
                current_chunk.append(para)
                current_size += para_size

            # Start new chunk with overlap
            else:
                chunk_text = ' '.join(current_chunk)
                if len(chunk_text.split()) >= self.min_chunk_size:
                    chunks.append(self._create_chunk(chunk_text, len(chunks), metadata))

                # Keep overlap from end of previous chunk
                overlap_words = chunk_text.split()[-self.chunk_overlap:] if chunk_text else []
                current_chunk = [' '.join(overlap_words), para] if overlap_words else [para]
                current_size = len(' '.join(current_chunk).split())

        # Don't forget the last chunk
        if current_chunk:
            chunk_text = ' '.join(current_chunk)
            if len(chunk_text.split()) >= self.min_chunk_size:
                chunks.append(self._create_chunk(chunk_text, len(chunks), metadata))

        return chunks

    def _create_chunk(self, text: str, index: int, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """Create a chunk object with metadata"""
        chunk_id = hashlib.md5(f"{text[:100]}{index}".encode()).hexdigest()

        chunk = {
            'id': chunk_id,
            'text': text,
            'index': index,
            'word_count': len(text.split()),
            'char_count': len(text),
        }

        if metadata:
            chunk['metadata'] = metadata

        return chunk


# =============================================================================
# EMBEDDINGS
# =============================================================================

class Embedder:
    """Generates embeddings using SentenceTransformers"""

    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)
        self.embedding_dim = self.model.get_sentence_embedding_dimension()
        logger.info(f"Loaded embedding model: {model_name} (dim={self.embedding_dim})")

    def embed_text(self, text: str) -> List[float]:
        """Generate embedding for a single text"""
        embedding = self.model.encode(text, convert_to_numpy=True)
        return embedding.tolist()

    def embed_batch(self, texts: List[str], batch_size: int = 32) -> List[List[float]]:
        """Generate embeddings for multiple texts"""
        embeddings = self.model.encode(
            texts,
            batch_size=batch_size,
            convert_to_numpy=True,
            show_progress_bar=len(texts) > 100
        )
        return embeddings.tolist()

    def embed_chunks(self, chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Add embeddings to chunk objects"""
        texts = [chunk['text'] for chunk in chunks]
        embeddings = self.embed_batch(texts)

        for chunk, embedding in zip(chunks, embeddings):
            chunk['embedding'] = embedding

        return chunks


# =============================================================================
# VECTOR STORAGE (pgvector)
# =============================================================================

class VectorStore:
    """Manages vector storage in PostgreSQL with pgvector"""

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
            logger.info("Connected to PostgreSQL")
        except Exception as e:
            logger.error(f"Database connection failed: {e}")
            raise

    def _ensure_schema(self):
        """Create tables if they don't exist"""
        with self.conn.cursor() as cur:
            # Enable pgvector extension
            cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")

            # Documents table (source URLs)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS rag_documents (
                    id SERIAL PRIMARY KEY,
                    url TEXT UNIQUE NOT NULL,
                    title TEXT,
                    meta_description TEXT,
                    content_hash TEXT,
                    ingested_at TIMESTAMP DEFAULT NOW(),
                    last_updated TIMESTAMP DEFAULT NOW(),
                    status TEXT DEFAULT 'active',
                    metadata JSONB DEFAULT '{}'
                );
                CREATE INDEX IF NOT EXISTS idx_rag_documents_url ON rag_documents(url);
                CREATE INDEX IF NOT EXISTS idx_rag_documents_status ON rag_documents(status);
            """)

            # Chunks table with vector embeddings
            cur.execute("""
                CREATE TABLE IF NOT EXISTS rag_chunks (
                    id SERIAL PRIMARY KEY,
                    document_id INTEGER REFERENCES rag_documents(id) ON DELETE CASCADE,
                    chunk_id TEXT UNIQUE NOT NULL,
                    chunk_index INTEGER,
                    text TEXT NOT NULL,
                    embedding vector(384),
                    word_count INTEGER,
                    created_at TIMESTAMP DEFAULT NOW(),
                    metadata JSONB DEFAULT '{}'
                );
                CREATE INDEX IF NOT EXISTS idx_rag_chunks_document ON rag_chunks(document_id);
                CREATE INDEX IF NOT EXISTS idx_rag_chunks_embedding ON rag_chunks
                    USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);
            """)

            # Feedback table for adaptive learning
            cur.execute("""
                CREATE TABLE IF NOT EXISTS rag_feedback (
                    id SERIAL PRIMARY KEY,
                    chunk_id TEXT REFERENCES rag_chunks(chunk_id),
                    document_id INTEGER REFERENCES rag_documents(id),
                    feedback_type TEXT NOT NULL,
                    feedback_value INTEGER,
                    comment TEXT,
                    agent_id TEXT,
                    query TEXT,
                    created_at TIMESTAMP DEFAULT NOW(),
                    processed BOOLEAN DEFAULT FALSE
                );
                CREATE INDEX IF NOT EXISTS idx_rag_feedback_chunk ON rag_feedback(chunk_id);
                CREATE INDEX IF NOT EXISTS idx_rag_feedback_processed ON rag_feedback(processed);
            """)

            self.conn.commit()
            logger.info("Database schema initialized")

    def store_document(self, url: str, title: str, meta_description: str,
                       content_hash: str, metadata: Dict = None) -> int:
        """Store or update a document record"""
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO rag_documents (url, title, meta_description, content_hash, metadata)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (url) DO UPDATE SET
                    title = EXCLUDED.title,
                    meta_description = EXCLUDED.meta_description,
                    content_hash = EXCLUDED.content_hash,
                    last_updated = NOW(),
                    metadata = EXCLUDED.metadata
                RETURNING id;
            """, (url, title, meta_description, content_hash,
                  psycopg2.extras.Json(metadata or {})))

            doc_id = cur.fetchone()[0]
            self.conn.commit()
            return doc_id

    def store_chunks(self, document_id: int, chunks: List[Dict[str, Any]]):
        """Store chunk embeddings for a document"""
        with self.conn.cursor() as cur:
            # Delete existing chunks for this document
            cur.execute("DELETE FROM rag_chunks WHERE document_id = %s", (document_id,))

            # Insert new chunks
            values = [
                (document_id, chunk['id'], chunk['index'], chunk['text'],
                 chunk['embedding'], chunk['word_count'],
                 psycopg2.extras.Json(chunk.get('metadata', {})))
                for chunk in chunks
            ]

            execute_values(cur, """
                INSERT INTO rag_chunks
                    (document_id, chunk_id, chunk_index, text, embedding, word_count, metadata)
                VALUES %s
            """, values, template="(%s, %s, %s, %s, %s::vector, %s, %s)")

            self.conn.commit()
            logger.info(f"Stored {len(chunks)} chunks for document {document_id}")

    def search(self, query_embedding: List[float], limit: int = 5,
               threshold: float = 0.7) -> List[Dict[str, Any]]:
        """Search for similar chunks using cosine similarity"""
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT
                    c.chunk_id,
                    c.text,
                    c.metadata,
                    d.url,
                    d.title,
                    1 - (c.embedding <=> %s::vector) as similarity
                FROM rag_chunks c
                JOIN rag_documents d ON c.document_id = d.id
                WHERE d.status = 'active'
                ORDER BY c.embedding <=> %s::vector
                LIMIT %s;
            """, (query_embedding, query_embedding, limit))

            results = []
            for row in cur.fetchall():
                if row[5] >= threshold:  # Filter by similarity threshold
                    results.append({
                        'chunk_id': row[0],
                        'text': row[1],
                        'metadata': row[2],
                        'url': row[3],
                        'title': row[4],
                        'similarity': float(row[5])
                    })

            return results

    def store_feedback(self, chunk_id: str = None, document_id: int = None,
                       feedback_type: str = 'helpful', feedback_value: int = 1,
                       comment: str = None, agent_id: str = None, query: str = None):
        """Store feedback for adaptive learning"""
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO rag_feedback
                    (chunk_id, document_id, feedback_type, feedback_value, comment, agent_id, query)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id;
            """, (chunk_id, document_id, feedback_type, feedback_value,
                  comment, agent_id, query))

            feedback_id = cur.fetchone()[0]
            self.conn.commit()
            return feedback_id

    def get_stale_documents(self, days: int = 7) -> List[Dict[str, Any]]:
        """Get documents that need re-ingestion based on feedback"""
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT DISTINCT d.id, d.url, d.title, d.last_updated,
                    COUNT(f.id) as feedback_count,
                    AVG(f.feedback_value) as avg_feedback
                FROM rag_documents d
                LEFT JOIN rag_feedback f ON d.id = f.document_id
                WHERE d.last_updated < NOW() - INTERVAL '%s days'
                   OR (f.feedback_type = 'outdated' AND f.processed = FALSE)
                   OR (f.feedback_type = 'low_quality' AND f.processed = FALSE)
                GROUP BY d.id, d.url, d.title, d.last_updated
                ORDER BY avg_feedback ASC NULLS LAST, d.last_updated ASC;
            """, (days,))

            return [
                {
                    'id': row[0],
                    'url': row[1],
                    'title': row[2],
                    'last_updated': row[3].isoformat() if row[3] else None,
                    'feedback_count': row[4],
                    'avg_feedback': float(row[5]) if row[5] else None
                }
                for row in cur.fetchall()
            ]

    def mark_feedback_processed(self, document_id: int):
        """Mark all feedback for a document as processed"""
        with self.conn.cursor() as cur:
            cur.execute("""
                UPDATE rag_feedback SET processed = TRUE
                WHERE document_id = %s AND processed = FALSE;
            """, (document_id,))
            self.conn.commit()

    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            logger.info("Database connection closed")


# =============================================================================
# UNIFIED RAG PIPELINE
# =============================================================================

class RAGPipeline:
    """Complete RAG pipeline: crawl -> clean -> chunk -> embed -> store"""

    def __init__(self, database_url: str, embedding_model: str = 'all-MiniLM-L6-v2'):
        self.extractor = ContentExtractor()
        self.cleaner = TextCleaner()
        self.chunker = SemanticChunker()
        self.embedder = Embedder(embedding_model)
        self.store = VectorStore(database_url)
        logger.info("RAG Pipeline initialized")

    def ingest_url(self, url: str, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """Complete ingestion pipeline for a URL"""
        try:
            # 1. Crawl
            logger.info(f"Crawling: {url}")
            extracted = self.extractor.crawl_url(url)

            # 2. Clean
            cleaned_content = self.cleaner.clean(extracted['content'])

            # 3. Generate content hash for change detection
            content_hash = hashlib.md5(cleaned_content.encode()).hexdigest()

            # 4. Store document
            doc_id = self.store.store_document(
                url=url,
                title=extracted['title'],
                meta_description=extracted['meta_description'],
                content_hash=content_hash,
                metadata=metadata
            )

            # 5. Chunk
            chunk_metadata = {
                'url': url,
                'title': extracted['title'],
                **(metadata or {})
            }
            chunks = self.chunker.chunk_text(cleaned_content, chunk_metadata)

            # 6. Embed
            chunks = self.embedder.embed_chunks(chunks)

            # 7. Store chunks
            self.store.store_chunks(doc_id, chunks)

            result = {
                'success': True,
                'document_id': doc_id,
                'url': url,
                'title': extracted['title'],
                'chunks_created': len(chunks),
                'content_hash': content_hash
            }

            logger.info(f"Ingested {url}: {len(chunks)} chunks")
            return result

        except Exception as e:
            logger.error(f"Ingestion failed for {url}: {e}")
            return {
                'success': False,
                'url': url,
                'error': str(e)
            }

    def query(self, query_text: str, limit: int = 5, threshold: float = 0.5) -> List[Dict[str, Any]]:
        """Query the RAG database"""
        # Embed the query
        query_embedding = self.embedder.embed_text(query_text)

        # Search
        results = self.store.search(query_embedding, limit, threshold)

        return results

    def add_feedback(self, feedback_type: str, chunk_id: str = None,
                     document_id: int = None, value: int = 1,
                     comment: str = None, agent_id: str = None,
                     query: str = None) -> int:
        """Add feedback for adaptive learning"""
        return self.store.store_feedback(
            chunk_id=chunk_id,
            document_id=document_id,
            feedback_type=feedback_type,
            feedback_value=value,
            comment=comment,
            agent_id=agent_id,
            query=query
        )

    def get_documents_to_reingest(self, days: int = 7) -> List[Dict[str, Any]]:
        """Get list of documents that need re-ingestion"""
        return self.store.get_stale_documents(days)

    def reingest_document(self, document_id: int) -> Dict[str, Any]:
        """Re-ingest a specific document by ID"""
        with self.store.conn.cursor() as cur:
            cur.execute("SELECT url, metadata FROM rag_documents WHERE id = %s", (document_id,))
            row = cur.fetchone()
            if not row:
                return {'success': False, 'error': 'Document not found'}

            url, metadata = row

        result = self.ingest_url(url, metadata)

        if result['success']:
            self.store.mark_feedback_processed(document_id)

        return result

    def close(self):
        """Clean up resources"""
        self.store.close()
