"""
MCP Gateway - Unified access to all MCP servers
Simplifies integration across all projects
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
import httpx
import redis
import json
import os
from datetime import datetime
from loguru import logger


app = FastAPI(
    title="MCP Gateway",
    description="Unified access to all Model Context Protocol servers",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

# MCP Server URLs
MCP_SERVERS = {
    "google_maps": os.getenv("MCP_GOOGLE_MAPS_URL", "http://mcp-google-maps:8080"),
    "google_analytics": os.getenv("MCP_GOOGLE_ANALYTICS_URL", "http://mcp-google-analytics:8080"),
    "gmb": os.getenv("MCP_GMB_URL", "http://mcp-gmb:8080"),
    "census": os.getenv("MCP_CENSUS_URL", "http://mcp-census:8080"),
    "osm": os.getenv("MCP_OSM_URL", "http://mcp-osm:8080"),
    "weather": os.getenv("MCP_WEATHER_URL", "http://mcp-weather:8080"),
}

# Initialize Redis
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)


# ========================================
# Models
# ========================================

class MCPRequest(BaseModel):
    server: str
    endpoint: str
    params: Optional[Dict[str, Any]] = {}
    cache_ttl: Optional[int] = 3600  # 1 hour default


# ========================================
# Helper Functions
# ========================================

async def call_mcp_server(server: str, endpoint: str, params: Dict = None):
    """Call an MCP server with caching"""

    if server not in MCP_SERVERS:
        raise HTTPException(status_code=404, detail=f"MCP server '{server}' not found")

    # Check cache
    cache_key = f"mcp:{server}:{endpoint}:{json.dumps(params or {}, sort_keys=True)}"
    cached = redis_client.get(cache_key)

    if cached:
        logger.info(f"Cache hit for {server}/{endpoint}")
        return json.loads(cached)

    # Call MCP server
    url = f"{MCP_SERVERS[server]}/{endpoint}"

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.get(url, params=params or {})
            response.raise_for_status()
            data = response.json()

            # Cache the response
            redis_client.setex(cache_key, 3600, json.dumps(data))

            logger.info(f"MCP call successful: {server}/{endpoint}")
            return data

        except httpx.HTTPStatusError as e:
            logger.error(f"MCP server error: {e}")
            raise HTTPException(status_code=e.response.status_code, detail=str(e))
        except Exception as e:
            logger.error(f"MCP call failed: {e}")
            raise HTTPException(status_code=500, detail=str(e))


# ========================================
# Generic MCP Endpoint
# ========================================

@app.post("/mcp")
async def generic_mcp_call(request: MCPRequest):
    """Generic MCP server call"""
    return await call_mcp_server(request.server, request.endpoint, request.params)


# ========================================
# Google Maps Endpoints
# ========================================

@app.get("/maps/geocode")
async def geocode(address: str):
    """Geocode an address to lat/lng"""
    return await call_mcp_server("google_maps", "geocode", {"address": address})


@app.get("/maps/reverse-geocode")
async def reverse_geocode(lat: float, lng: float):
    """Reverse geocode lat/lng to address"""
    return await call_mcp_server("google_maps", "reverse_geocode", {"lat": lat, "lng": lng})


@app.get("/maps/nearby")
async def nearby_places(lat: float, lng: float, type: str, radius: int = 5000):
    """Find nearby places"""
    return await call_mcp_server("google_maps", "nearby", {
        "lat": lat,
        "lng": lng,
        "type": type,
        "radius": radius
    })


@app.get("/maps/distance")
async def calculate_distance(origin: str, destination: str):
    """Calculate distance between two addresses"""
    return await call_mcp_server("google_maps", "distance", {
        "origin": origin,
        "destination": destination
    })


# ========================================
# Google Analytics Endpoints
# ========================================

@app.get("/analytics/traffic")
async def get_traffic(start_date: str, end_date: str):
    """Get website traffic data"""
    return await call_mcp_server("google_analytics", "traffic", {
        "start_date": start_date,
        "end_date": end_date
    })


@app.get("/analytics/top-pages")
async def get_top_pages(start_date: str, end_date: str, limit: int = 10):
    """Get top performing pages"""
    return await call_mcp_server("google_analytics", "top_pages", {
        "start_date": start_date,
        "end_date": end_date,
        "limit": limit
    })


@app.get("/analytics/conversions")
async def get_conversions(start_date: str, end_date: str):
    """Get conversion data"""
    return await call_mcp_server("google_analytics", "conversions", {
        "start_date": start_date,
        "end_date": end_date
    })


# ========================================
# Google My Business Endpoints
# ========================================

@app.get("/gmb/insights")
async def get_gmb_insights(location_id: Optional[str] = None):
    """Get GMB location insights"""
    params = {}
    if location_id:
        params["location_id"] = location_id
    return await call_mcp_server("gmb", "insights", params)


@app.get("/gmb/reviews")
async def get_gmb_reviews(location_id: Optional[str] = None):
    """Get GMB reviews"""
    params = {}
    if location_id:
        params["location_id"] = location_id
    return await call_mcp_server("gmb", "reviews", params)


@app.get("/gmb/questions")
async def get_gmb_questions(location_id: Optional[str] = None):
    """Get GMB Q&A"""
    params = {}
    if location_id:
        params["location_id"] = location_id
    return await call_mcp_server("gmb", "questions", params)


# ========================================
# US Census Endpoints
# ========================================

@app.get("/census/demographics")
async def get_demographics(zip: Optional[str] = None, state: Optional[str] = None):
    """Get demographic data"""
    params = {}
    if zip:
        params["zip"] = zip
    if state:
        params["state"] = state
    return await call_mcp_server("census", "demographics", params)


@app.get("/census/income")
async def get_income_data(zip: Optional[str] = None):
    """Get income statistics"""
    params = {}
    if zip:
        params["zip"] = zip
    return await call_mcp_server("census", "income", params)


@app.get("/census/population")
async def get_population(zip: Optional[str] = None, city: Optional[str] = None):
    """Get population data"""
    params = {}
    if zip:
        params["zip"] = zip
    if city:
        params["city"] = city
    return await call_mcp_server("census", "population", params)


# ========================================
# OpenStreetMap Endpoints
# ========================================

@app.get("/osm/search")
async def osm_search(query: str):
    """Search OpenStreetMap"""
    return await call_mcp_server("osm", "search", {"query": query})


@app.get("/osm/nearby")
async def osm_nearby(lat: float, lng: float, amenity: str):
    """Find nearby amenities"""
    return await call_mcp_server("osm", "nearby", {
        "lat": lat,
        "lng": lng,
        "amenity": amenity
    })


# ========================================
# OpenWeather Endpoints
# ========================================

@app.get("/weather/current")
async def get_current_weather(city: Optional[str] = None, lat: Optional[float] = None, lng: Optional[float] = None):
    """Get current weather"""
    params = {}
    if city:
        params["city"] = city
    if lat and lng:
        params["lat"] = lat
        params["lng"] = lng
    return await call_mcp_server("weather", "current", params)


@app.get("/weather/forecast")
async def get_forecast(city: Optional[str] = None, days: int = 5):
    """Get weather forecast"""
    params = {"days": days}
    if city:
        params["city"] = city
    return await call_mcp_server("weather", "forecast", params)


# ========================================
# Composite Endpoints (Use Multiple MCPs)
# ========================================

@app.get("/composite/location-intelligence")
async def location_intelligence(address: str):
    """
    Get complete intelligence about a location using multiple MCP servers

    Returns:
    - Geocode data (Google Maps)
    - Demographics (US Census)
    - Weather (OpenWeather)
    - Nearby amenities (OpenStreetMap)
    """

    # Geocode first
    geocode_data = await call_mcp_server("google_maps", "geocode", {"address": address})

    if not geocode_data or "results" not in geocode_data:
        raise HTTPException(status_code=404, detail="Address not found")

    location = geocode_data["results"][0]["geometry"]["location"]
    lat, lng = location["lat"], location["lng"]

    # Get ZIP from address components
    zip_code = None
    for component in geocode_data["results"][0].get("address_components", []):
        if "postal_code" in component.get("types", []):
            zip_code = component["short_name"]
            break

    # Parallel calls to other MCP servers
    results = {
        "address": address,
        "geocode": geocode_data,
        "coordinates": {"lat": lat, "lng": lng}
    }

    # Get demographics if we have ZIP
    if zip_code:
        try:
            demo_data = await call_mcp_server("census", "demographics", {"zip": zip_code})
            results["demographics"] = demo_data
        except:
            pass

    # Get weather
    try:
        weather_data = await call_mcp_server("weather", "current", {"lat": lat, "lng": lng})
        results["weather"] = weather_data
    except:
        pass

    # Get nearby gyms (for gym use case)
    try:
        nearby = await call_mcp_server("osm", "nearby", {
            "lat": lat,
            "lng": lng,
            "amenity": "gym"
        })
        results["nearby_gyms"] = nearby
    except:
        pass

    return results


@app.get("/composite/event-location-analysis")
async def event_location_analysis(venue_address: str, target_radius_miles: int = 5):
    """
    Analyze a potential event location

    Returns:
    - Venue geocode
    - Demographics within radius
    - Nearby hotels
    - Nearby restaurants
    - Nearby gyms (potential competitors)
    - Parking availability
    - Weather forecast
    """

    # Geocode venue
    geocode_data = await call_mcp_server("google_maps", "geocode", {"address": venue_address})
    location = geocode_data["results"][0]["geometry"]["location"]
    lat, lng = location["lat"], location["lng"]

    radius_meters = int(target_radius_miles * 1609.34)

    # Get all nearby data
    results = {
        "venue": {
            "address": venue_address,
            "coordinates": {"lat": lat, "lng": lng}
        }
    }

    # Nearby hotels
    try:
        hotels = await call_mcp_server("google_maps", "nearby", {
            "lat": lat,
            "lng": lng,
            "type": "lodging",
            "radius": radius_meters
        })
        results["nearby_hotels"] = hotels
    except:
        pass

    # Nearby restaurants
    try:
        restaurants = await call_mcp_server("google_maps", "nearby", {
            "lat": lat,
            "lng": lng,
            "type": "restaurant",
            "radius": radius_meters
        })
        results["nearby_restaurants"] = restaurants
    except:
        pass

    # Nearby gyms (competitors or partners)
    try:
        gyms = await call_mcp_server("osm", "nearby", {
            "lat": lat,
            "lng": lng,
            "amenity": "gym"
        })
        results["nearby_gyms"] = gyms
    except:
        pass

    # Weather forecast for event date
    try:
        weather = await call_mcp_server("weather", "forecast", {"lat": lat, "lng": lng, "days": 7})
        results["weather_forecast"] = weather
    except:
        pass

    return results


# ========================================
# Health & Status
# ========================================

@app.get("/health")
def health_check():
    """Health check for MCP gateway"""
    return {
        "status": "healthy",
        "mcp_servers": list(MCP_SERVERS.keys()),
        "timestamp": datetime.now().isoformat()
    }


@app.get("/servers")
def list_servers():
    """List all available MCP servers"""
    return {
        "servers": MCP_SERVERS,
        "count": len(MCP_SERVERS)
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
