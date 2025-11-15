"""
Intelligent Website Scraper for RAG Knowledge Base
Scrapes websites, converts to markdown, chunks intelligently
"""

import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
from dataclasses import dataclass
import time
from urllib.parse import urljoin, urlparse
import html2text
from chunking_strategies import FileChunker, ChunkStrategy


@dataclass
class WebPage:
    """Represents a scraped webpage"""
    url: str
    title: str
    content: str
    markdown: str
    links: List[str]
    metadata: Dict


class WebsiteScraper:
    """Intelligent website scraper with RAG integration"""

    def __init__(self, max_depth: int = 2, delay: float = 1.0):
        self.max_depth = max_depth
        self.delay = delay
        self.visited_urls = set()
        self.html_converter = html2text.HTML2Text()
        self.html_converter.ignore_links = False
        self.html_converter.ignore_images = False
        self.chunker = FileChunker(chunk_size=1500, chunk_overlap=200)

    def scrape_url(self, url: str) -> Optional[WebPage]:
        """Scrape a single URL and extract content"""
        try:
            # Add delay to be respectful
            time.sleep(self.delay)

            # Fetch the page
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            # Parse HTML
            soup = BeautifulSoup(response.content, 'html.parser')

            # Remove script and style elements
            for script in soup(["script", "style", "nav", "footer"]):
                script.decompose()

            # Extract title
            title = soup.title.string if soup.title else urlparse(url).path

            # Convert to markdown
            markdown_content = self.html_converter.handle(str(soup))

            # Extract links
            links = []
            for link in soup.find_all('a', href=True):
                absolute_url = urljoin(url, link['href'])
                if self._is_same_domain(url, absolute_url):
                    links.append(absolute_url)

            # Get plain text
            text_content = soup.get_text(separator='\n', strip=True)

            return WebPage(
                url=url,
                title=title,
                content=text_content,
                markdown=markdown_content,
                links=links,
                metadata={
                    'source': 'web_scrape',
                    'url': url,
                    'title': title,
                    'domain': urlparse(url).netloc
                }
            )

        except Exception as e:
            print(f"Error scraping {url}: {e}")
            return None

    def scrape_website(self, start_url: str, max_pages: int = 50) -> List[WebPage]:
        """
        Scrape an entire website starting from a URL
        Uses breadth-first search with depth limit
        """
        pages = []
        to_visit = [(start_url, 0)]  # (url, depth)

        while to_visit and len(pages) < max_pages:
            url, depth = to_visit.pop(0)

            # Skip if already visited or depth exceeded
            if url in self.visited_urls or depth > self.max_depth:
                continue

            print(f"Scraping: {url} (depth: {depth})")

            # Scrape the page
            page = self.scrape_url(url)

            if page:
                pages.append(page)
                self.visited_urls.add(url)

                # Add links to visit queue
                if depth < self.max_depth:
                    for link in page.links:
                        if link not in self.visited_urls:
                            to_visit.append((link, depth + 1))

        return pages

    def pages_to_chunks(self, pages: List[WebPage]):
        """Convert scraped pages to RAG chunks"""
        all_chunks = []

        for page in pages:
            # Use markdown chunking strategy
            chunks = self.chunker.chunk_text(
                text=page.markdown,
                metadata=page.metadata,
                strategy=ChunkStrategy.MARKDOWN
            )
            all_chunks.extend(chunks)

        return all_chunks

    def _is_same_domain(self, url1: str, url2: str) -> bool:
        """Check if two URLs are from the same domain"""
        return urlparse(url1).netloc == urlparse(url2).netloc


# ========================================
# Specialized Scrapers
# ========================================

class DocumentationScraper(WebsiteScraper):
    """Specialized scraper for documentation sites"""

    def __init__(self):
        super().__init__(max_depth=3, delay=0.5)

    def scrape_docs(self, base_url: str, sidebar_selector: str = None):
        """
        Scrape documentation following the sidebar structure

        Example:
        scraper = DocumentationScraper()
        pages = scraper.scrape_docs("https://docs.n8n.io", sidebar_selector=".sidebar a")
        """
        # First, scrape the main page
        main_page = self.scrape_url(base_url)

        if not main_page:
            return []

        # If sidebar selector provided, find all docs links
        if sidebar_selector:
            soup = BeautifulSoup(requests.get(base_url).content, 'html.parser')
            doc_links = [urljoin(base_url, a['href'])
                        for a in soup.select(sidebar_selector) if a.get('href')]

            # Scrape each doc link
            pages = [main_page]
            for link in doc_links[:50]:  # Limit to 50 pages
                page = self.scrape_url(link)
                if page:
                    pages.append(page)

            return pages
        else:
            # Fall back to regular website scraping
            return self.scrape_website(base_url)


class BlogScraper(WebsiteScraper):
    """Specialized scraper for blog posts"""

    def scrape_blog(self, blog_url: str, article_selector: str = "article"):
        """
        Scrape blog posts

        Example:
        scraper = BlogScraper()
        pages = scraper.scrape_blog("https://example.com/blog")
        """
        page = self.scrape_url(blog_url)

        if not page:
            return []

        # Extract article links
        soup = BeautifulSoup(requests.get(blog_url).content, 'html.parser')
        articles = soup.select(article_selector + ' a[href]')

        article_urls = [urljoin(blog_url, a['href']) for a in articles]

        pages = []
        for url in article_urls[:20]:  # Limit to 20 articles
            article_page = self.scrape_url(url)
            if article_page:
                pages.append(article_page)

        return pages


# ========================================
# Preset Knowledge Bases
# ========================================

class KnowledgeBaseBuilder:
    """Build knowledge bases from common sources"""

    @staticmethod
    def build_npc_knowledge_base():
        """
        Build knowledge base for NPC bodybuilding
        Scrapes: NPC website, rules, divisions, etc.
        """
        scraper = WebsiteScraper(max_depth=2)

        sources = [
            "https://npcnewsonline.com/",
            # Add more NPC-related URLs
        ]

        all_pages = []
        for source in sources:
            print(f"Scraping {source}...")
            pages = scraper.scrape_website(source, max_pages=30)
            all_pages.extend(pages)

        # Convert to chunks
        chunks = scraper.pages_to_chunks(all_pages)

        return {
            'pages': all_pages,
            'chunks': chunks,
            'source': 'npc_knowledge_base'
        }

    @staticmethod
    def build_competitor_knowledge_base(competitor_urls: List[str]):
        """
        Build knowledge base about competitor shows
        Scrapes competitor show websites
        """
        scraper = WebsiteScraper(max_depth=1)

        all_pages = []
        for url in competitor_urls:
            print(f"Scraping competitor: {url}...")
            pages = scraper.scrape_website(url, max_pages=20)
            all_pages.extend(pages)

        chunks = scraper.pages_to_chunks(all_pages)

        return {
            'pages': all_pages,
            'chunks': chunks,
            'source': 'competitor_knowledge_base'
        }

    @staticmethod
    def build_tool_documentation(tool_name: str, docs_url: str):
        """
        Build knowledge base from tool documentation

        Examples:
        - n8n: "https://docs.n8n.io"
        - Apify: "https://docs.apify.com"
        - GHL: "https://help.gohighlevel.com"
        """
        scraper = DocumentationScraper()

        print(f"Scraping {tool_name} documentation...")
        pages = scraper.scrape_docs(docs_url)

        chunks = scraper.pages_to_chunks(pages)

        return {
            'pages': pages,
            'chunks': chunks,
            'source': f'{tool_name}_documentation'
        }


# ========================================
# Integration with Qdrant
# ========================================

class RAGIngestor:
    """Ingest scraped content into Qdrant for RAG"""

    def __init__(self, qdrant_client, collection_name: str):
        self.qdrant_client = qdrant_client
        self.collection_name = collection_name

    def ingest_chunks(self, chunks, embedding_function):
        """
        Ingest chunks into Qdrant vector database

        Usage:
        from sentence_transformers import SentenceTransformer

        model = SentenceTransformer('all-MiniLM-L6-v2')
        ingestor = RAGIngestor(qdrant_client, "knowledge_base")
        ingestor.ingest_chunks(chunks, model.encode)
        """
        from qdrant_client.models import PointStruct

        points = []

        for i, chunk in enumerate(chunks):
            # Create embedding
            embedding = embedding_function(chunk.text)

            # Create point
            point = PointStruct(
                id=hash(chunk.chunk_id) % (10 ** 8),
                vector=embedding.tolist() if hasattr(embedding, 'tolist') else embedding,
                payload={
                    "text": chunk.text,
                    "source": chunk.source,
                    "metadata": chunk.metadata,
                    "chunk_id": chunk.chunk_id,
                    "strategy": chunk.strategy.value
                }
            )
            points.append(point)

        # Batch upsert to Qdrant
        self.qdrant_client.upsert(
            collection_name=self.collection_name,
            points=points
        )

        print(f"Ingested {len(points)} chunks into {self.collection_name}")


# ========================================
# Usage Examples
# ========================================

if __name__ == "__main__":
    # Example 1: Scrape NPC website
    print("=== Building NPC Knowledge Base ===")
    npc_kb = KnowledgeBaseBuilder.build_npc_knowledge_base()
    print(f"Scraped {len(npc_kb['pages'])} pages")
    print(f"Created {len(npc_kb['chunks'])} chunks")

    # Example 2: Scrape competitor shows
    print("\n=== Building Competitor Knowledge Base ===")
    competitor_urls = [
        "https://example-competitor-show.com",
        # Add real URLs here
    ]
    comp_kb = KnowledgeBaseBuilder.build_competitor_knowledge_base(competitor_urls)
    print(f"Scraped {len(comp_kb['pages'])} competitor pages")

    # Example 3: Scrape tool documentation
    print("\n=== Building n8n Documentation Knowledge Base ===")
    n8n_kb = KnowledgeBaseBuilder.build_tool_documentation(
        "n8n",
        "https://docs.n8n.io"
    )
    print(f"Scraped {len(n8n_kb['pages'])} documentation pages")

    # Example 4: Ingest into Qdrant (pseudo-code)
    """
    from qdrant_client import QdrantClient
    from sentence_transformers import SentenceTransformer

    # Initialize
    qdrant_client = QdrantClient(host="localhost", port=6333)
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # Ingest NPC knowledge base
    ingestor = RAGIngestor(qdrant_client, "npc_knowledge")
    ingestor.ingest_chunks(npc_kb['chunks'], model.encode)

    # Now you can query this knowledge base via RAG!
    """
