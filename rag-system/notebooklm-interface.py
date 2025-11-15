"""
NotebookLM-Style Interface for RAG
Query your knowledge bases with natural language
Powered by Qdrant + Claude
"""

from typing import List, Dict, Optional
from dataclasses import dataclass
import anthropic
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from datetime import datetime


@dataclass
class Source:
    """Represents a source document in the knowledge base"""
    text: str
    metadata: Dict
    score: float
    chunk_id: str


@dataclass
class NotebookResponse:
    """Response from NotebookLM-style query"""
    answer: str
    sources: List[Source]
    confidence: float
    query: str
    timestamp: str


class NotebookLM:
    """
    NotebookLM-style interface for intelligent knowledge base queries

    Similar to Google's NotebookLM, but for your own data:
    - Upload documents (PDFs, audio transcripts, websites)
    - Ask questions in natural language
    - Get answers with citations
    - Generate summaries, outlines, study guides
    """

    def __init__(
        self,
        qdrant_host: str = "localhost",
        qdrant_port: int = 6333,
        claude_api_key: str = None,
        embedding_model: str = 'all-MiniLM-L6-v2'
    ):
        self.qdrant_client = QdrantClient(host=qdrant_host, port=qdrant_port)
        self.claude_client = anthropic.Anthropic(api_key=claude_api_key)
        self.embedding_model = SentenceTransformer(embedding_model)

    # ========================================
    # Core Query Interface
    # ========================================

    def query(
        self,
        question: str,
        collection: str,
        top_k: int = 5,
        use_claude: bool = True
    ) -> NotebookResponse:
        """
        Query your knowledge base with a natural language question

        Args:
            question: Natural language question
            collection: Which knowledge base to search
            top_k: Number of relevant sources to retrieve
            use_claude: Whether to use Claude for answer generation

        Returns:
            NotebookResponse with answer and sources
        """

        # Step 1: Retrieve relevant sources from Qdrant
        sources = self._retrieve_sources(question, collection, top_k)

        if not sources:
            return NotebookResponse(
                answer="I couldn't find any relevant information in the knowledge base for this question.",
                sources=[],
                confidence=0.0,
                query=question,
                timestamp=datetime.now().isoformat()
            )

        # Step 2: Generate answer using Claude (RAG)
        if use_claude:
            answer, confidence = self._generate_answer(question, sources)
        else:
            # Just return the top source
            answer = sources[0].text
            confidence = sources[0].score

        return NotebookResponse(
            answer=answer,
            sources=sources,
            confidence=confidence,
            query=question,
            timestamp=datetime.now().isoformat()
        )

    def _retrieve_sources(
        self,
        query: str,
        collection: str,
        top_k: int
    ) -> List[Source]:
        """Retrieve relevant sources from Qdrant"""

        # Create query embedding
        query_embedding = self.embedding_model.encode(query).tolist()

        # Search Qdrant
        results = self.qdrant_client.search(
            collection_name=collection,
            query_vector=query_embedding,
            limit=top_k
        )

        # Convert to Source objects
        sources = []
        for result in results:
            sources.append(Source(
                text=result.payload.get('text', ''),
                metadata=result.payload.get('metadata', {}),
                score=result.score,
                chunk_id=result.payload.get('chunk_id', '')
            ))

        return sources

    def _generate_answer(
        self,
        question: str,
        sources: List[Source]
    ) -> tuple[str, float]:
        """Generate answer using Claude with retrieved context"""

        # Build context from sources
        context = "\n\n".join([
            f"[Source {i+1}] (Relevance: {source.score:.2f})\n{source.text}"
            for i, source in enumerate(sources)
        ])

        # Create prompt for Claude
        prompt = f"""You are an intelligent research assistant analyzing a knowledge base.

Based on the following sources, answer the user's question. If the sources don't contain enough information to answer confidently, say so.

**SOURCES:**
{context}

**QUESTION:**
{question}

**INSTRUCTIONS:**
1. Answer the question using ONLY the information from the sources above
2. Cite which source(s) you used (e.g., "According to Source 2...")
3. If sources conflict, mention both perspectives
4. If sources don't have enough info, say "The available sources don't provide enough information to answer this question"
5. Be concise but complete

**ANSWER:**"""

        # Call Claude
        message = self.claude_client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            temperature=0.3,
            messages=[{"role": "user", "content": prompt}]
        )

        answer = message.content[0].text

        # Calculate confidence based on:
        # - Average source relevance score
        # - Whether Claude said "don't have enough info"
        avg_score = sum(s.score for s in sources) / len(sources)

        if "don't have enough information" in answer.lower():
            confidence = avg_score * 0.5
        else:
            confidence = avg_score

        return answer, confidence

    # ========================================
    # NotebookLM-Style Features
    # ========================================

    def summarize(self, collection: str, max_length: int = 500) -> str:
        """
        Generate a summary of the entire knowledge base

        Like NotebookLM's "Summarize" feature
        """

        # Get a sample of chunks from the collection
        sample_size = 10
        all_points = self.qdrant_client.scroll(
            collection_name=collection,
            limit=sample_size
        )[0]

        # Extract texts
        texts = [point.payload['text'] for point in all_points]
        combined_text = "\n\n".join(texts)

        # Summarize with Claude
        prompt = f"""Provide a comprehensive summary of this knowledge base based on the following samples:

{combined_text}

Create a summary that:
1. Identifies the main topics covered
2. Highlights key points
3. Is approximately {max_length} words
4. Is organized with clear sections"""

        message = self.claude_client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1500,
            messages=[{"role": "user", "content": prompt}]
        )

        return message.content[0].text

    def create_study_guide(self, collection: str, topic: str) -> str:
        """
        Generate a study guide on a specific topic

        Like NotebookLM's "Study Guide" feature
        """

        # Query for relevant content on the topic
        response = self.query(
            question=f"Tell me everything about {topic}",
            collection=collection,
            top_k=10
        )

        # Create study guide with Claude
        context = "\n\n".join([s.text for s in response.sources])

        prompt = f"""Create a comprehensive study guide on "{topic}" based on these sources:

{context}

The study guide should include:
1. **Key Concepts**: Main ideas to understand
2. **Important Terms**: Definitions of crucial terminology
3. **Key Points**: Bullet points of essential information
4. **Practice Questions**: 5-10 questions to test understanding
5. **Summary**: Brief recap of the most important points

Format in clear sections with headers."""

        message = self.claude_client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2048,
            messages=[{"role": "user", "content": prompt}]
        )

        return message.content[0].text

    def generate_faq(self, collection: str, num_questions: int = 10) -> List[Dict[str, str]]:
        """
        Generate FAQ from knowledge base

        Like NotebookLM's FAQ generation
        """

        # Get sample content
        sample_points = self.qdrant_client.scroll(
            collection_name=collection,
            limit=20
        )[0]

        sample_text = "\n\n".join([p.payload['text'] for p in sample_points])

        # Generate FAQ with Claude
        prompt = f"""Based on this content, generate {num_questions} frequently asked questions with answers:

{sample_text}

Format as:
Q: [Question]
A: [Answer]

Make questions practical and useful."""

        message = self.claude_client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2048,
            messages=[{"role": "user", "content": prompt}]
        )

        # Parse response into Q&A pairs
        faq_text = message.content[0].text
        faqs = []

        lines = faq_text.split('\n')
        current_q = None

        for line in lines:
            if line.startswith('Q:'):
                current_q = line[2:].strip()
            elif line.startswith('A:') and current_q:
                faqs.append({
                    'question': current_q,
                    'answer': line[2:].strip()
                })
                current_q = None

        return faqs

    def create_outline(self, collection: str) -> str:
        """
        Generate a structured outline of the knowledge base

        Like NotebookLM's outline feature
        """

        # Get representative samples
        sample_points = self.qdrant_client.scroll(
            collection_name=collection,
            limit=15
        )[0]

        sample_text = "\n\n".join([p.payload['text'] for p in sample_points])

        prompt = f"""Create a hierarchical outline of the topics covered in this content:

{sample_text}

Format as:
I. Main Topic
   A. Subtopic
      1. Detail
      2. Detail
   B. Subtopic
II. Main Topic
   A. Subtopic

Be comprehensive and organize logically."""

        message = self.claude_client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1500,
            messages=[{"role": "user", "content": prompt}]
        )

        return message.content[0].text

    def find_related(
        self,
        concept: str,
        collection: str,
        num_results: int = 5
    ) -> List[Source]:
        """
        Find content related to a concept

        Like NotebookLM's "Find Related" feature
        """
        sources = self._retrieve_sources(concept, collection, num_results)
        return sources

    def compare_sources(
        self,
        question: str,
        collections: List[str]
    ) -> Dict[str, NotebookResponse]:
        """
        Compare answers across multiple knowledge bases

        Example: Compare what NPC docs say vs. competitor docs
        """
        responses = {}

        for collection in collections:
            response = self.query(question, collection, top_k=3)
            responses[collection] = response

        return responses


# ========================================
# Usage Examples
# ========================================

if __name__ == "__main__":
    import os

    # Initialize NotebookLM
    notebook = NotebookLM(
        qdrant_host="localhost",
        qdrant_port=6333,
        claude_api_key=os.getenv("CLAUDE_API_KEY")
    )

    # Example 1: Query your knowledge base
    print("=== Query Example ===")
    response = notebook.query(
        question="What are the judging criteria for Men's Physique?",
        collection="npc_knowledge"
    )
    print(f"Answer: {response.answer}")
    print(f"Confidence: {response.confidence:.2%}")
    print(f"\nSources used: {len(response.sources)}")
    for i, source in enumerate(response.sources, 1):
        print(f"  Source {i}: {source.chunk_id} (score: {source.score:.2f})")

    # Example 2: Generate summary
    print("\n=== Summary Example ===")
    summary = notebook.summarize("npc_knowledge")
    print(summary)

    # Example 3: Create study guide
    print("\n=== Study Guide Example ===")
    study_guide = notebook.create_study_guide(
        collection="npc_knowledge",
        topic="NPC competition divisions"
    )
    print(study_guide)

    # Example 4: Generate FAQ
    print("\n=== FAQ Example ===")
    faqs = notebook.generate_faq("npc_knowledge", num_questions=5)
    for faq in faqs:
        print(f"Q: {faq['question']}")
        print(f"A: {faq['answer']}\n")

    # Example 5: Compare sources
    print("\n=== Compare Sources Example ===")
    comparison = notebook.compare_sources(
        question="What is the registration fee?",
        collections=["ronnie_coleman_classic", "competitor_show_1"]
    )
    for collection, response in comparison.items():
        print(f"\n{collection}:")
        print(f"  {response.answer}")

    # Example 6: Create outline
    print("\n=== Outline Example ===")
    outline = notebook.create_outline("npc_knowledge")
    print(outline)
