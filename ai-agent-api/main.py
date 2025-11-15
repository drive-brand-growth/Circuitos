"""
Metroflex Events AI Agent API
FastAPI server with RAG capabilities for athlete intelligence and event management
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
from datetime import datetime
import anthropic
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer
import redis
from loguru import logger

# ========================================
# Configuration
# ========================================

app = FastAPI(
    title="Metroflex Events AI Agent API",
    description="AI-powered athlete intelligence and event management",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Environment variables
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")
QDRANT_HOST = os.getenv("QDRANT_HOST", "qdrant")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", 6333))
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

# Initialize clients
claude_client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)
qdrant_client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

# ========================================
# Data Models
# ========================================

class AthleteProfile(BaseModel):
    username: str
    display_name: str
    bio: str
    follower_count: int
    location: Optional[str] = None
    division: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class RAGQuery(BaseModel):
    query: str
    collection: str = "athletes"
    limit: int = 5
    use_claude: bool = True


class ClaudeRequest(BaseModel):
    prompt: str
    max_tokens: int = 1024
    temperature: float = 0.3
    system_prompt: Optional[str] = None


class EventIntelligence(BaseModel):
    event_name: str
    competitor_shows: List[str]
    target_demographics: List[str]


# ========================================
# Helper Functions
# ========================================

def create_embedding(text: str) -> List[float]:
    """Generate embedding vector from text"""
    return embedding_model.encode(text).tolist()


def init_qdrant_collection(collection_name: str, vector_size: int = 384):
    """Initialize Qdrant collection if it doesn't exist"""
    try:
        collections = qdrant_client.get_collections().collections
        if not any(c.name == collection_name for c in collections):
            qdrant_client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
            )
            logger.info(f"Created Qdrant collection: {collection_name}")
    except Exception as e:
        logger.error(f"Error initializing Qdrant collection: {e}")


# ========================================
# API Endpoints
# ========================================

@app.get("/")
def read_root():
    return {
        "service": "Metroflex Events AI Agent API",
        "status": "running",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    health_status = {
        "api": "healthy",
        "qdrant": "unknown",
        "redis": "unknown",
        "claude": "unknown"
    }

    # Check Qdrant
    try:
        qdrant_client.get_collections()
        health_status["qdrant"] = "healthy"
    except Exception as e:
        health_status["qdrant"] = f"unhealthy: {str(e)}"

    # Check Redis
    try:
        redis_client.ping()
        health_status["redis"] = "healthy"
    except Exception as e:
        health_status["redis"] = f"unhealthy: {str(e)}"

    # Check Claude API
    try:
        if CLAUDE_API_KEY:
            health_status["claude"] = "configured"
        else:
            health_status["claude"] = "not configured"
    except Exception as e:
        health_status["claude"] = f"error: {str(e)}"

    return health_status


@app.post("/athletes/add")
async def add_athlete_to_rag(athlete: AthleteProfile):
    """Add athlete profile to RAG vector database"""
    try:
        # Initialize collection
        init_qdrant_collection("athletes")

        # Create searchable text
        searchable_text = f"{athlete.display_name} {athlete.bio} {athlete.location or ''} {athlete.division or ''}"

        # Generate embedding
        embedding = create_embedding(searchable_text)

        # Create unique ID
        point_id = hash(athlete.username) % (10 ** 8)

        # Store in Qdrant
        qdrant_client.upsert(
            collection_name="athletes",
            points=[
                PointStruct(
                    id=point_id,
                    vector=embedding,
                    payload={
                        "username": athlete.username,
                        "display_name": athlete.display_name,
                        "bio": athlete.bio,
                        "follower_count": athlete.follower_count,
                        "location": athlete.location,
                        "division": athlete.division,
                        "metadata": athlete.metadata or {},
                        "added_at": datetime.now().isoformat()
                    }
                )
            ]
        )

        # Cache in Redis
        redis_client.setex(
            f"athlete:{athlete.username}",
            86400,  # 24 hours
            athlete.model_dump_json()
        )

        logger.info(f"Added athlete to RAG: {athlete.username}")

        return {
            "status": "success",
            "athlete": athlete.username,
            "point_id": point_id
        }

    except Exception as e:
        logger.error(f"Error adding athlete to RAG: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/athletes/search")
async def search_athletes(query: RAGQuery):
    """Search athletes using RAG with optional Claude enhancement"""
    try:
        # Generate query embedding
        query_embedding = create_embedding(query.query)

        # Search Qdrant
        search_results = qdrant_client.search(
            collection_name=query.collection,
            query_vector=query_embedding,
            limit=query.limit
        )

        # Format results
        athletes = []
        for result in search_results:
            athletes.append({
                "score": result.score,
                "athlete": result.payload
            })

        # Optional: Enhance with Claude analysis
        if query.use_claude and athletes:
            athlete_summaries = "\n\n".join([
                f"**{a['athlete']['display_name']}** (@{a['athlete']['username']})\n"
                f"Bio: {a['athlete']['bio']}\n"
                f"Division: {a['athlete'].get('division', 'Unknown')}\n"
                f"Location: {a['athlete'].get('location', 'Unknown')}\n"
                f"Relevance Score: {a['score']:.2f}"
                for a in athletes
            ])

            claude_prompt = f"""Based on this query: "{query.query}"

Here are the most relevant athletes found:

{athlete_summaries}

Provide a brief analysis of why these athletes match the query and which ones are the best targets for recruitment to the Ronnie Coleman Classic."""

            message = claude_client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=512,
                messages=[{"role": "user", "content": claude_prompt}]
            )

            claude_analysis = message.content[0].text
        else:
            claude_analysis = None

        return {
            "query": query.query,
            "results_count": len(athletes),
            "athletes": athletes,
            "claude_analysis": claude_analysis
        }

    except Exception as e:
        logger.error(f"Error searching athletes: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/claude/analyze")
async def claude_analyze(request: ClaudeRequest):
    """Send request to Claude API"""
    try:
        messages = [{"role": "user", "content": request.prompt}]

        kwargs = {
            "model": "claude-3-5-sonnet-20241022",
            "max_tokens": request.max_tokens,
            "temperature": request.temperature,
            "messages": messages
        }

        if request.system_prompt:
            kwargs["system"] = request.system_prompt

        message = claude_client.messages.create(**kwargs)

        return {
            "response": message.content[0].text,
            "usage": {
                "input_tokens": message.usage.input_tokens,
                "output_tokens": message.usage.output_tokens
            },
            "model": message.model
        }

    except Exception as e:
        logger.error(f"Error calling Claude API: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/intelligence/competitor-analysis")
async def competitor_analysis(event: EventIntelligence):
    """Analyze competitor shows and provide strategic insights"""
    try:
        # Search for athletes who attended competitor shows
        competitor_athletes = []

        for show in event.competitor_shows:
            query = f"competed at {show} NPC bodybuilding"
            embedding = create_embedding(query)

            results = qdrant_client.search(
                collection_name="athletes",
                query_vector=embedding,
                limit=10
            )

            for result in results:
                competitor_athletes.append(result.payload)

        # Use Claude to analyze
        athlete_data = "\n".join([
            f"- {a['display_name']} (@{a['username']}): {a.get('division', 'Unknown')} | {a.get('location', 'Unknown')}"
            for a in competitor_athletes[:20]
        ])

        claude_prompt = f"""You are a competitive intelligence analyst for the {event.event_name}.

We've identified athletes who competed at these competitor shows:
{', '.join(event.competitor_shows)}

Here are some of those athletes:
{athlete_data}

Target demographics: {', '.join(event.target_demographics)}

Provide a strategic analysis:
1. What patterns do you see in competitor attendees?
2. Which athletes should we prioritize for recruitment?
3. What messaging would resonate with each segment?
4. What competitive advantages can we highlight?

Return structured insights."""

        message = claude_client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2048,
            messages=[{"role": "user", "content": claude_prompt}]
        )

        return {
            "event": event.event_name,
            "competitor_athletes_found": len(competitor_athletes),
            "analysis": message.content[0].text
        }

    except Exception as e:
        logger.error(f"Error in competitor analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/stats")
async def get_stats():
    """Get system statistics"""
    try:
        # Qdrant stats
        collections = qdrant_client.get_collections().collections
        collection_stats = []
        for collection in collections:
            info = qdrant_client.get_collection(collection.name)
            collection_stats.append({
                "name": collection.name,
                "vectors_count": info.vectors_count,
                "points_count": info.points_count
            })

        # Redis stats
        redis_keys = redis_client.dbsize()

        return {
            "qdrant": {
                "collections": collection_stats,
                "total_collections": len(collections)
            },
            "redis": {
                "keys": redis_keys
            },
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ========================================
# Startup & Shutdown Events
# ========================================

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    logger.info("Starting Metroflex Events AI Agent API...")

    # Initialize Qdrant collections
    init_qdrant_collection("athletes", 384)
    init_qdrant_collection("events", 384)
    init_qdrant_collection("documents", 384)

    logger.info("API started successfully!")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down API...")
    # Add any cleanup code here


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
