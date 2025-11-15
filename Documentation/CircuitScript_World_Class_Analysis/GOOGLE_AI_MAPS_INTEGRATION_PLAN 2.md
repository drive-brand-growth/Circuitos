# Google AI Maps Platform - Integration Plan
## Upgrade from Basic Maps API to AI-Powered Features

**Gap Addressed:** Critical Gap #2, #3, #5, #6 from World-Class Analysis
**Build Time:** 2 weeks (40 hours)
**Cost:** +$0-200/month (usage-based, estimated <$50/month)

---

## What You're Upgrading From

### Current Implementation ✅
```javascript
// Virtual LPR currently uses basic Maps API
sources: ['google-maps', 'census', 'clearbit', 'linkedin', 'gmb']

// Distance calculation (lines 324-355 of Virtual LPR)
const distance = calculateDistance(lead.location, business.location);
```

**Works today:**
- ✅ Geocoding (addresses → lat/lng)
- ✅ Distance Matrix (calculate miles between points)
- ✅ Proximity scoring (0.5/2/5 mile tiers)

**Missing:**
- ❌ AI-generated place summaries
- ❌ Route optimization for SDR territories
- ❌ Grounding layer for LLM insights
- ❌ Places Insights (BigQuery POI data)

---

## What You're Upgrading To

### Google AI Maps Platform (2024-2025 Features)

**1. Place Summaries (AI-Generated)**
```javascript
// AI-generated human-centric context about locations
const summary = await googleAIMaps.getPlaceSummary({
  placeId: lead.businessPlaceId,
  fields: ['summary', 'reviews_summary', 'area_summary', 'editorial_summary']
});

// Example output:
{
  "summary": "Upscale tech startup hub in SoMa, known for innovative workspace culture",
  "reviews_summary": "Highly rated for work-life balance, collaborative environment",
  "area_summary": "Trendy neighborhood with high concentration of Series A-C startups",
  "editorial_summary": "Premium office space targeting fast-growth tech companies"
}
```

**Use case:** Enrich Virtual LPR qualification with AI-generated market context

---

**2. Route Optimization Agent (Natural Language)**
```javascript
// Natural language routing for SDR territory planning
const route = await googleAIMaps.optimizeRoute({
  request: "Optimize my route to visit 5 high-priority leads in Manhattan tomorrow 2-6pm",
  leads: [
    { address: "123 Broadway, NY 10012", priority: 95 },
    { address: "456 5th Ave, NY 10018", priority: 88 },
    // ... 3 more
  ],
  constraints: {
    startTime: "2024-11-14T14:00:00Z",
    endTime: "2024-11-14T18:00:00Z",
    meetingDuration: 30  // minutes
  }
});

// AI generates optimal route considering:
// - Traffic patterns
// - Lead priority scores
// - Meeting durations
// - Time windows
```

**Use case:** SDR agents auto-plan daily territory routes

---

**3. Contextual View (Maps in AI Chat)**
```javascript
// Embed interactive maps in conversational UI
const contextualMap = await googleAIMaps.createContextualView({
  conversation: {
    query: "Show me all A-grade leads within 2 miles of our flagship location",
    context: {
      businessLocation: { lat: 40.7614, lng: -73.9776 },
      leadGrade: "A",
      radius: 2
    }
  },
  displayFormat: "interactive"
});

// Returns embeddable map with:
// - Lead markers (color-coded by grade)
// - Business location
// - Service area overlay
// - Clickable lead details
```

**Use case:** Circuit Script dashboard with visual lead geography

---

**4. Grounding Layer (Prevent Hallucinations)**
```javascript
// Before (hallucination risk):
const prompt = `Is this lead close to our business?`;

// After (grounded in Maps data):
const groundedPrompt = await googleAIMaps.groundPrompt({
  prompt: "Evaluate proximity fit for this lead",
  groundingData: {
    leadAddress: "123 Main St, Brooklyn NY 11201",
    businessAddress: "456 Broadway, Manhattan NY 10012",
    actualDistance: 3.2,  // miles from Maps API
    travelTime: 18,       // minutes via car
    transitOptions: ["subway", "car", "walk"]
  }
});

// Grounded prompt sent to LLM:
`Based on Google Maps verified data:
- Lead location: 123 Main St, Brooklyn NY 11201
- Business location: 456 Broadway, Manhattan NY 10012
- Actual distance: 3.2 miles
- Travel time: 18 minutes by car
- Transit options: subway (25 min), car (18 min), walk (63 min)

Evaluate proximity fit for Virtual LPR scoring (0.5mi=4pts, 2mi=3pts, 5mi=1.5pts).`
```

**Use case:** All location-based LLM prompts grounded in real Maps data

---

**5. Places Insights (BigQuery Integration)**
```sql
-- Query POI data for market segmentation
SELECT
  place_name,
  category,
  rating,
  review_count,
  price_level,
  geometry.location AS location
FROM `bigquery-public-data.geo_us_boundaries.places_insights`
WHERE
  ST_DWITHIN(
    geometry.location,
    ST_GEOGPOINT(-73.9776, 40.7614),  -- MetroFlex Gym
    3218.69  -- 2 miles in meters
  )
  AND category IN ('gym', 'fitness_center', 'crossfit')
ORDER BY rating DESC, review_count DESC
```

**Use case:** Competitive intelligence, market density analysis

---

## Implementation Roadmap

### Week 1: Setup & Basic Integration (20 hours)

#### Day 1-2: Google Cloud Setup (4 hours)
```bash
# 1. Create Google Cloud project
gcloud projects create circuit-script-ai-maps --name="Circuit Script AI Maps"

# 2. Enable APIs
gcloud services enable \
  places.googleapis.com \
  routes.googleapis.com \
  geocoding.googleapis.com \
  places-insights.googleapis.com \
  --project=circuit-script-ai-maps

# 3. Create service account
gcloud iam service-accounts create circuit-script-maps \
  --display-name="Circuit Script Maps Service Account" \
  --project=circuit-script-ai-maps

# 4. Generate API key
gcloud alpha services api-keys create \
  --display-name="Circuit Script AI Maps Key" \
  --project=circuit-script-ai-maps

# 5. Add to Heroku config
heroku config:set GOOGLE_MAPS_AI_KEY=YOUR_API_KEY --app circuit-script-production
```

---

#### Day 3-4: Python Client Library (8 hours)

**Create:** `/circuit_script/integrations/google_ai_maps.py`

```python
import googlemaps
from google.cloud import bigquery
import os
from typing import Dict, List, Optional

class GoogleAIMapsClient:
    """Google AI Maps Platform integration for Circuit Script"""

    def __init__(self):
        self.api_key = os.getenv('GOOGLE_MAPS_AI_KEY')
        self.gmaps = googlemaps.Client(key=self.api_key)
        self.bq_client = bigquery.Client()

    # 1. AI Place Summaries
    def get_place_summary(self, place_id: str) -> Dict:
        """Get AI-generated summary of a place"""
        place = self.gmaps.place(
            place_id=place_id,
            fields=['name', 'editorial_summary', 'rating', 'user_ratings_total',
                   'price_level', 'types', 'geometry', 'reviews']
        )

        # AI-generated summary (new AI feature)
        summary = {
            'place_id': place_id,
            'name': place['result'].get('name'),
            'summary': place['result'].get('editorial_summary', {}).get('overview'),
            'rating': place['result'].get('rating'),
            'review_count': place['result'].get('user_ratings_total'),
            'price_level': place['result'].get('price_level'),
            'types': place['result'].get('types', []),

            # AI-generated insights (requires AI Maps Platform)
            'ai_insights': self._generate_ai_insights(place['result'])
        }

        return summary

    def _generate_ai_insights(self, place_data: Dict) -> Dict:
        """Generate AI insights from place data"""
        # Extract review themes using AI
        reviews = place_data.get('reviews', [])
        review_texts = [r['text'] for r in reviews[:10]]

        return {
            'market_positioning': self._analyze_market_position(place_data),
            'customer_sentiment': self._analyze_reviews(review_texts),
            'competitive_context': self._get_competitive_density(place_data)
        }

    # 2. Route Optimization
    def optimize_route(self,
                      leads: List[Dict],
                      start_time: str,
                      end_time: str,
                      origin: Optional[Dict] = None) -> Dict:
        """Optimize SDR territory route using AI"""

        waypoints = [lead['address'] for lead in leads]

        # Use Directions API with optimization
        directions = self.gmaps.directions(
            origin=origin or waypoints[0],
            destination=waypoints[-1],
            waypoints=waypoints[1:-1],
            optimize_waypoints=True,
            mode='driving',
            departure_time=start_time,
            traffic_model='best_guess'
        )

        optimized = {
            'total_distance': sum([leg['distance']['value']
                                  for leg in directions[0]['legs']]),
            'total_duration': sum([leg['duration_in_traffic']['value']
                                  for leg in directions[0]['legs']]),
            'optimized_order': directions[0]['waypoint_order'],
            'route_polyline': directions[0]['overview_polyline']['points'],
            'legs': directions[0]['legs']
        }

        return optimized

    # 3. Grounding Layer
    def ground_location_prompt(self,
                              lead_address: str,
                              business_address: str,
                              prompt: str) -> str:
        """Ground LLM prompt in verified Maps data"""

        # Get actual distance
        distance_result = self.gmaps.distance_matrix(
            origins=[business_address],
            destinations=[lead_address],
            mode='driving'
        )

        distance_meters = distance_result['rows'][0]['elements'][0]['distance']['value']
        distance_miles = distance_meters * 0.000621371
        duration_seconds = distance_result['rows'][0]['elements'][0]['duration']['value']
        duration_minutes = duration_seconds // 60

        # Create grounded prompt
        grounded = f"""Based on Google Maps verified data:
- Lead location: {lead_address}
- Business location: {business_address}
- Actual distance: {distance_miles:.2f} miles
- Travel time: {duration_minutes} minutes by car

Original prompt: {prompt}

Use only the verified Maps data above for location-based scoring."""

        return grounded

    # 4. Places Insights (BigQuery)
    def get_competitive_density(self,
                               center_lat: float,
                               center_lng: float,
                               radius_miles: float,
                               categories: List[str]) -> Dict:
        """Query BigQuery Places Insights for competitive intelligence"""

        radius_meters = radius_miles * 1609.34

        query = f"""
        SELECT
          place_name,
          category,
          rating,
          review_count,
          price_level,
          ST_DISTANCE(
            geometry.location,
            ST_GEOGPOINT({center_lng}, {center_lat})
          ) AS distance_meters
        FROM `bigquery-public-data.geo_us_boundaries.places_insights`
        WHERE
          ST_DWITHIN(
            geometry.location,
            ST_GEOGPOINT({center_lng}, {center_lat}),
            {radius_meters}
          )
          AND category IN UNNEST({categories})
        ORDER BY rating DESC, review_count DESC
        LIMIT 50
        """

        results = self.bq_client.query(query).to_dataframe()

        return {
            'total_competitors': len(results),
            'avg_rating': results['rating'].mean(),
            'market_density': len(results) / radius_miles,  # competitors per sq mile
            'top_competitors': results.head(10).to_dict('records')
        }
```

---

#### Day 5: Integration with Virtual LPR (8 hours)

**Update:** `/circuit_script/agents/VirtualLPR.py`

```python
from circuit_script.integrations.google_ai_maps import GoogleAIMapsClient

class VirtualLPR:
    def __init__(self):
        self.maps_ai = GoogleAIMapsClient()

    def enrich_lead(self, lead: Dict, business: Dict) -> Dict:
        """Enrich lead with Google AI Maps data"""

        # 1. Get AI place summary for lead's business (if B2B)
        if lead.get('company_place_id'):
            lead['ai_summary'] = self.maps_ai.get_place_summary(
                lead['company_place_id']
            )

        # 2. Ground proximity scoring in real Maps data
        grounded_prompt = self.maps_ai.ground_location_prompt(
            lead_address=lead['address'],
            business_address=business['address'],
            prompt="Evaluate proximity fit for lead scoring"
        )

        # 3. Get competitive density around business
        lead['competitive_context'] = self.maps_ai.get_competitive_density(
            center_lat=business['location']['lat'],
            center_lng=business['location']['lng'],
            radius_miles=5,
            categories=business['competitor_categories']
        )

        return lead

    def score_location_fit(self, lead: Dict, business: Dict) -> Dict:
        """Enhanced location scoring with AI Maps data"""
        score = 0
        attribution = []

        # Use grounded distance (prevents hallucinations)
        distance_miles = lead['maps_verified_distance']

        # Original proximity scoring (lines 324-355)
        if distance_miles <= 0.5:
            score += 4
            attribution.append({
                'points': 4,
                'reason': f'Extremely close: {distance_miles:.2f} miles',
                'source': 'Google Maps AI Distance Matrix',
                'verified': True
            })
        elif distance_miles <= 2:
            score += 3
            attribution.append({
                'points': 3,
                'reason': f'Within service area: {distance_miles:.2f} miles',
                'source': 'Google Maps AI Distance Matrix',
                'verified': True
            })
        elif distance_miles <= 5:
            score += 1.5
            attribution.append({
                'points': 1.5,
                'reason': f'Acceptable distance: {distance_miles:.2f} miles',
                'source': 'Google Maps AI Distance Matrix',
                'verified': True
            })

        # NEW: Bonus points for AI-detected favorable area
        if lead.get('ai_summary', {}).get('market_positioning') == 'premium':
            score += 1
            attribution.append({
                'points': 1,
                'reason': 'Premium market area (AI-detected)',
                'source': 'Google AI Maps Place Summary',
                'verified': True
            })

        return {'score': score, 'attribution': attribution}
```

---

### Week 2: Advanced Features (20 hours)

#### Day 6-7: Route Optimization for SDR Agents (10 hours)

**Create:** `/circuit_script/agents/SDRRouteOptimizer.py`

```python
from circuit_script.integrations.google_ai_maps import GoogleAIMapsClient
from circuit_script.core import CircuitTrigger
from typing import List, Dict

class SDRRouteOptimizer(CircuitTrigger):
    """Optimize SDR daily routes using Google AI Maps"""

    def __init__(self):
        super().__init__()
        self.maps_ai = GoogleAIMapsClient()

    def optimize_daily_route(self, sdr_id: str, date: str) -> Dict:
        """Generate optimized route for SDR's daily meetings"""

        # 1. Get today's scheduled leads (A/B grade, high priority)
        leads = self.db.query(f"""
            SELECT id, address, score, priority, scheduled_time
            FROM contacts
            WHERE assigned_sdr_id = '{sdr_id}'
              AND scheduled_date = '{date}'
              AND grade IN ('A', 'B')
            ORDER BY priority DESC, score DESC
        """)

        if len(leads) == 0:
            return {'message': 'No leads scheduled for today'}

        # 2. Optimize route using AI Maps
        optimized = self.maps_ai.optimize_route(
            leads=leads,
            start_time=f"{date}T09:00:00Z",
            end_time=f"{date}T17:00:00Z",
            origin=self.get_sdr_home_address(sdr_id)
        )

        # 3. Generate meeting schedule
        schedule = self._generate_meeting_schedule(leads, optimized)

        # 4. Send to SDR (SMS or email)
        self.notify_sdr(sdr_id, schedule)

        # 5. Log optimization
        self.logger.info(f"Route optimized for SDR {sdr_id}: {len(leads)} meetings, "
                        f"{optimized['total_distance']/1609:.1f} miles, "
                        f"{optimized['total_duration']/60:.0f} minutes total")

        return {
            'sdr_id': sdr_id,
            'date': date,
            'total_leads': len(leads),
            'total_distance_miles': optimized['total_distance'] / 1609,
            'total_duration_minutes': optimized['total_duration'] / 60,
            'schedule': schedule,
            'map_url': self._generate_maps_url(optimized)
        }

    def _generate_meeting_schedule(self, leads: List[Dict], route: Dict) -> List[Dict]:
        """Generate time-based meeting schedule"""
        schedule = []
        current_time = "09:00"

        for idx, lead_id in enumerate(route['optimized_order']):
            lead = leads[lead_id]
            leg = route['legs'][idx]

            # Drive time to next meeting
            drive_minutes = leg['duration_in_traffic']['value'] // 60

            # Meeting time (default 30 min)
            meeting_duration = 30

            schedule.append({
                'time': current_time,
                'lead_name': lead['name'],
                'lead_address': lead['address'],
                'lead_score': lead['score'],
                'drive_time_minutes': drive_minutes,
                'meeting_duration_minutes': meeting_duration,
                'notes': f"Priority: {lead['priority']}, Grade: {lead['grade']}"
            })

            # Advance time
            current_time = self._add_minutes(current_time, drive_minutes + meeting_duration)

        return schedule
```

---

#### Day 8-9: Contextual View Dashboard (8 hours)

**Create:** `/circuit_script/dashboard/maps_view.html`

```html
<!DOCTYPE html>
<html>
<head>
  <title>Circuit Script - Lead Geography</title>
  <script src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&libraries=places&callback=initMap" async defer></script>
  <style>
    #map { height: 600px; width: 100%; }
    .lead-marker { cursor: pointer; }
    .lead-info {
      font-family: Arial, sans-serif;
      padding: 10px;
    }
  </style>
</head>
<body>
  <h1>Lead Geography - Circuit Script</h1>

  <div class="filters">
    <label>Grade:
      <select id="gradeFilter">
        <option value="all">All</option>
        <option value="A">A</option>
        <option value="B">B</option>
        <option value="C">C</option>
      </select>
    </label>

    <label>Radius:
      <select id="radiusFilter">
        <option value="2">2 miles</option>
        <option value="5">5 miles</option>
        <option value="10">10 miles</option>
      </select>
    </label>
  </div>

  <div id="map"></div>

  <script>
    let map;
    let markers = [];

    async function initMap() {
      // Center on business location
      const businessLocation = { lat: 40.7614, lng: -73.9776 };

      map = new google.maps.Map(document.getElementById('map'), {
        center: businessLocation,
        zoom: 13,
        mapId: 'circuit_script_lead_map'
      });

      // Add business marker
      new google.maps.Marker({
        position: businessLocation,
        map: map,
        title: 'MetroFlex Gym',
        icon: 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png'
      });

      // Load leads from Circuit Script API
      loadLeads();
    }

    async function loadLeads() {
      const response = await fetch('/api/leads/geography?grade=A&radius=5');
      const leads = await response.json();

      leads.forEach(lead => {
        const marker = new google.maps.Marker({
          position: { lat: lead.lat, lng: lead.lng },
          map: map,
          title: lead.name,
          icon: getMarkerIcon(lead.grade)
        });

        const infoWindow = new google.maps.InfoWindow({
          content: `
            <div class="lead-info">
              <h3>${lead.name}</h3>
              <p>Score: ${lead.score}/100 (Grade ${lead.grade})</p>
              <p>Distance: ${lead.distance_miles.toFixed(2)} miles</p>
              <p>Priority: ${lead.priority}</p>
              <button onclick="viewLead('${lead.id}')">View Details</button>
            </div>
          `
        });

        marker.addListener('click', () => {
          infoWindow.open(map, marker);
        });

        markers.push(marker);
      });
    }

    function getMarkerIcon(grade) {
      const colors = {
        'A': 'green',
        'B': 'yellow',
        'C': 'red'
      };
      return `http://maps.google.com/mapfiles/ms/icons/${colors[grade]}-dot.png`;
    }
  </script>
</body>
</html>
```

---

#### Day 10: Testing & Deployment (2 hours)

**Test Suite:** `/tests/test_google_ai_maps.py`

```python
import pytest
from circuit_script.integrations.google_ai_maps import GoogleAIMapsClient

class TestGoogleAIMaps:
    @pytest.fixture
    def maps_client(self):
        return GoogleAIMapsClient()

    def test_place_summary(self, maps_client):
        """Test AI place summary generation"""
        # MetroFlex Gym place ID (example)
        place_id = "ChIJN1t_tDeuEmsRUsoyG83frY4"

        summary = maps_client.get_place_summary(place_id)

        assert summary['place_id'] == place_id
        assert summary['name'] is not None
        assert 'ai_insights' in summary

    def test_route_optimization(self, maps_client):
        """Test SDR route optimization"""
        leads = [
            {'address': '123 Broadway, NY 10012', 'priority': 95},
            {'address': '456 5th Ave, NY 10018', 'priority': 88},
            {'address': '789 Park Ave, NY 10021', 'priority': 92}
        ]

        route = maps_client.optimize_route(
            leads=leads,
            start_time='2024-11-14T09:00:00Z',
            end_time='2024-11-14T17:00:00Z'
        )

        assert route['total_distance'] > 0
        assert route['total_duration'] > 0
        assert len(route['optimized_order']) == len(leads)

    def test_grounding_layer(self, maps_client):
        """Test prompt grounding"""
        grounded = maps_client.ground_location_prompt(
            lead_address="123 Main St, Brooklyn NY 11201",
            business_address="456 Broadway, Manhattan NY 10012",
            prompt="Is this lead close?"
        )

        assert "Google Maps verified data" in grounded
        assert "Actual distance:" in grounded
        assert "Travel time:" in grounded
```

---

## Cost Estimation

### Google AI Maps Platform Pricing (2025)

**Distance Matrix API:**
- $5 per 1,000 requests
- Estimated: 10,000 requests/month = **$50/month**

**Places API (with AI summaries):**
- $17 per 1,000 requests (with Place Details)
- Estimated: 2,000 requests/month = **$34/month**

**Routes API (optimization):**
- $5 per 1,000 requests
- Estimated: 300 requests/month = **$1.50/month**

**BigQuery Places Insights:**
- $6.25 per TB scanned
- Estimated: 100 GB/month = **$0.60/month**

**Total Estimated:** **$86/month** at moderate usage
**Likely Actual:** **$30-50/month** (lower usage initially)

---

## Deployment Checklist

### Week 1 Deliverables:
- [ ] Google Cloud project created
- [ ] AI Maps Platform APIs enabled
- [ ] Service account + API key generated
- [ ] Python client library built (`google_ai_maps.py`)
- [ ] Virtual LPR integration complete
- [ ] Grounding layer implemented
- [ ] Tests passing

### Week 2 Deliverables:
- [ ] SDR Route Optimizer agent built
- [ ] Contextual View dashboard deployed
- [ ] BigQuery Places Insights connected
- [ ] Route optimization tested with real leads
- [ ] Production deployment (Heroku)
- [ ] Monitoring/alerting configured

---

## Success Metrics

**Week 1:**
- ✅ Virtual LPR enriched with AI place summaries
- ✅ All location prompts grounded (0% hallucinations)
- ✅ Proximity scoring accuracy improved (verified vs estimated)

**Week 2:**
- ✅ SDR routes optimized (20-30% time savings)
- ✅ Lead geography dashboard live
- ✅ Competitive density analysis integrated

**Month 1 Post-Launch:**
- ✅ Cost <$50/month (within budget)
- ✅ 100% of leads enriched with AI Maps data
- ✅ SDR productivity +20-30% (less drive time)

---

**© 2025 CircuitOS™ - Google AI Maps Integration Plan**
**Status:** Ready to Build (Week 1-2 of Critical Gaps Roadmap)
**Build Time:** 40 hours (2 weeks @ 20 hrs/week)
**Cost:** +$30-50/month (usage-based)
