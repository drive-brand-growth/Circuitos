/**
 * Virtual LPR™ - Lead Validation API
 * © 2025 CircuitOS™ - Patent Pending
 *
 * Purpose: Validate and score leads using FREE MCP servers
 * Cost: $0/month infrastructure + ~$0.01 per validation (Claude API)
 *
 * Integrations:
 * - Google Maps API (distance, geocoding)
 * - US Census Bureau API (demographics)
 * - Google Analytics 4 (visitor tracking) ✅ NEW
 * - Google My Business (intent signals) ✅ NEW
 * - OpenStreetMap (free geocoding fallback) ✅ NEW
 * - OpenWeather (weather-based personalization) ✅ NEW
 * - Claude API (AI validation)
 */

import Anthropic from '@anthropic-ai/sdk';
import { getVisitorByClientId, getHighIntentVisitors } from '../lib/mcps/google-analytics.js';
import { getGMBInsights, calculateGMBIntentScore, getGMBAwarenessLevel, trackGMBSignal } from '../lib/mcps/google-my-business.js';
import { geocodeWithFallback } from '../lib/mcps/openstreetmap.js';
import { getCurrentWeather, analyzeWeatherImpact, isExtremeWeather } from '../lib/mcps/openweather.js';

const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY
});

// API Keys from environment
const GOOGLE_MAPS_API_KEY = process.env.GOOGLE_MAPS_API_KEY;
const CENSUS_API_BASE = 'https://api.census.gov/data/2021/acs/acs5';
const IPAPI_BASE = 'https://ipapi.co';

/**
 * Main handler for Virtual LPR lead validation
 */
export default async function handler(req, res) {
  // CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const {
      signal_type,  // "website_visit" | "gmb_view" | "social_profile_view" | "email_open" | "location_proximity"
      signal_data,  // Data from the signal source
      business
    } = req.body;

    // Validate required fields
    if (!signal_type || !signal_data || !business) {
      return res.status(400).json({
        error: 'Missing required fields',
        required: ['signal_type', 'signal_data', 'business']
      });
    }

    console.log('[Virtual LPR] Processing signal:', signal_type);

    // === STEP 1: ENRICH WITH LOCAL DATA ===
    let enrichmentData = {};

    // Get ZIP code from various sources
    const zipCode = signal_data.location?.zip_code ||
                    signal_data.zip_code ||
                    (signal_data.ip_address ? await getZipFromIP(signal_data.ip_address) : null);

    if (zipCode) {
      console.log('[Virtual LPR] Enriching with Census data for ZIP:', zipCode);

      // Fetch Census demographics (FREE API)
      try {
        const censusData = await getCensusDemographics(zipCode);
        enrichmentData.census = censusData;
      } catch (error) {
        console.warn('[Virtual LPR] Census API error:', error.message);
        enrichmentData.census = null;
      }

      // === NEW: Enrich with Weather Data ===
      console.log('[Virtual LPR] Enriching with weather data');
      try {
        const weather = await getCurrentWeather(zipCode);
        const weatherImpact = analyzeWeatherImpact(weather, business.type || 'gym');

        enrichmentData.weather = {
          ...weather,
          impact: weatherImpact,
          isExtreme: isExtremeWeather(weather)
        };
      } catch (error) {
        console.warn('[Virtual LPR] Weather API error:', error.message);
        enrichmentData.weather = null;
      }
    }

    // === NEW: Enrich with GA4 Visitor Data ===
    if (signal_type === 'website_visit' && signal_data.ga4_client_id) {
      console.log('[Virtual LPR] Enriching with GA4 visitor data');
      try {
        const visitorData = await getVisitorByClientId(signal_data.ga4_client_id);
        if (visitorData) {
          enrichmentData.ga4 = {
            pages_viewed: visitorData.pagesViewed,
            session_duration: visitorData.sessionDuration,
            total_sessions: visitorData.totalSessions,
            engagement_score: visitorData.engagementScore,
            awareness_level: visitorData.awarenessLevel,
            is_high_intent: visitorData.isHighIntent
          };
        }
      } catch (error) {
        console.warn('[Virtual LPR] GA4 API error:', error.message);
        enrichmentData.ga4 = null;
      }
    }

    // === NEW: Enrich with GMB Signals ===
    if (signal_type === 'gmb_view' || signal_type === 'gmb_direction' || signal_type === 'gmb_call') {
      console.log('[Virtual LPR] Enriching with GMB data (HIGH INTENT!)');
      try {
        const gmbInsights = await getGMBInsights(
          process.env.GMB_ACCOUNT_ID,
          process.env.GMB_LOCATION_ID
        );

        const gmbIntentScore = calculateGMBIntentScore(gmbInsights);
        const gmbAwareness = getGMBAwarenessLevel(gmbInsights);

        enrichmentData.gmb = {
          ...gmbInsights,
          intent_score: gmbIntentScore,
          awareness_level: gmbAwareness,
          signal_type
        };

        // Auto-boost score for direction requests (EXTREMELY HIGH INTENT)
        if (signal_type === 'gmb_direction') {
          enrichmentData.gmb.intent_boost = 25;
          console.log('[Virtual LPR] 🔥 GMB DIRECTION REQUEST - Boosting score +25!');
        } else if (signal_type === 'gmb_call') {
          enrichmentData.gmb.intent_boost = 20;
          console.log('[Virtual LPR] 🔥 GMB CALL CLICK - Boosting score +20!');
        }
      } catch (error) {
        console.warn('[Virtual LPR] GMB API error:', error.message);
        enrichmentData.gmb = null;
      }
    }

    // Calculate distance if coordinates available
    if (signal_data.location?.lat && signal_data.location?.lng && business.lat && business.lng) {
      console.log('[Virtual LPR] Calculating distance');

      try {
        const distanceData = await calculateDistance(
          business.lat,
          business.lng,
          signal_data.location.lat,
          signal_data.location.lng
        );
        enrichmentData.distance = distanceData;
      } catch (error) {
        console.warn('[Virtual LPR] Distance calculation error:', error.message);
        enrichmentData.distance = null;
      }
    }

    // === STEP 2: AI VALIDATION & SCORING ===
    console.log('[Virtual LPR] Sending to Claude for AI validation');

    const detectionResult = await aiValidateLead({
      signal_type,
      signal_data,
      business,
      enrichmentData
    });

    // === STEP 3: RETURN RESULTS ===
    if (detectionResult.qualified_lead) {
      console.log('[Virtual LPR] ✓ Lead QUALIFIED - Score:', detectionResult.signal_strength);

      return res.status(200).json({
        success: true,
        qualified: true,
        detection: detectionResult,
        ghl_integration: {
          action: 'create_contact',
          initial_tags: detectionResult.initial_tags,
          custom_fields: {
            vlpr_source: signal_type,
            vlpr_signal_strength: detectionResult.signal_strength,
            vlpr_score: detectionResult.predicted_lpr_score,
            distance_miles: enrichmentData.distance?.miles || null,
            median_income: enrichmentData.census?.median_income || null,
            median_age: enrichmentData.census?.median_age || null,
            zip_code: zipCode || null,
            awareness_level: detectionResult.awareness_level || 'Unknown',

            // NEW: GA4 enrichment
            ga4_pages_viewed: enrichmentData.ga4?.pages_viewed || null,
            ga4_session_duration: enrichmentData.ga4?.session_duration || null,
            ga4_engagement_score: enrichmentData.ga4?.engagement_score || null,

            // NEW: GMB enrichment (HIGH INTENT signals)
            gmb_intent_score: enrichmentData.gmb?.intent_score || null,
            gmb_direction_requests: enrichmentData.gmb?.directionRequests || null,
            gmb_call_clicks: enrichmentData.gmb?.callClicks || null,

            // NEW: Weather enrichment
            weather_temp: enrichmentData.weather?.temp || null,
            weather_condition: enrichmentData.weather?.condition || null,
            weather_impact: enrichmentData.weather?.impact?.impact || null
          },
          next_workflow: 'Lead Scorer',

          // NEW: Pass enrichment data for copywriter
          enrichment: {
            weather: enrichmentData.weather,
            ga4: enrichmentData.ga4,
            gmb: enrichmentData.gmb
          }
        }
      });
    } else {
      console.log('[Virtual LPR] ✗ Lead NOT qualified - Score:', detectionResult.signal_strength);

      return res.status(200).json({
        success: true,
        qualified: false,
        detection: detectionResult,
        recommended_action: detectionResult.recommended_action
      });
    }

  } catch (error) {
    console.error('[Virtual LPR] Error:', error);

    return res.status(500).json({
      success: false,
      error: 'Failed to process virtual sighting',
      details: error.message
    });
  }
}

/**
 * Get ZIP code from IP address using ipapi.co (FREE)
 */
async function getZipFromIP(ip) {
  try {
    const response = await fetch(`${IPAPI_BASE}/${ip}/json/`);
    if (!response.ok) throw new Error('IP API failed');

    const data = await response.json();
    return data.postal;
  } catch (error) {
    console.warn('[Virtual LPR] Could not get ZIP from IP:', error.message);
    return null;
  }
}

/**
 * Get Census demographics data by ZIP code (FREE)
 */
async function getCensusDemographics(zipCode) {
  try {
    // Census API: Get population, income, age data
    // Variables: B01003_001E (population), B19013_001E (income), B01002_001E (age)
    const url = `${CENSUS_API_BASE}?get=NAME,B01003_001E,B19013_001E,B01002_001E&for=zip%20code%20tabulation%20area:${zipCode}`;

    const response = await fetch(url);
    if (!response.ok) throw new Error('Census API failed');

    const data = await response.json();

    if (!data || data.length < 2) {
      throw new Error('No Census data for ZIP');
    }

    return {
      zip_code: zipCode,
      population: parseInt(data[1][1]) || 0,
      median_income: parseInt(data[1][2]) || 0,
      median_age: parseFloat(data[1][3]) || 0,
      affluence: parseInt(data[1][2]) > 75000 ? 'high' :
                 parseInt(data[1][2]) > 50000 ? 'medium' : 'low'
    };
  } catch (error) {
    throw new Error(`Census lookup failed: ${error.message}`);
  }
}

/**
 * Calculate distance between two coordinates using Google Maps Distance Matrix API
 */
async function calculateDistance(lat1, lng1, lat2, lng2) {
  if (!GOOGLE_MAPS_API_KEY) {
    // Fallback to Haversine formula if no API key
    return calculateHaversineDistance(lat1, lng1, lat2, lng2);
  }

  try {
    const url = `https://maps.googleapis.com/maps/api/distancematrix/json?origins=${lat1},${lng1}&destinations=${lat2},${lng2}&key=${GOOGLE_MAPS_API_KEY}`;

    const response = await fetch(url);
    if (!response.ok) throw new Error('Google Maps API failed');

    const data = await response.json();

    if (data.status !== 'OK' || !data.rows[0]?.elements[0]) {
      throw new Error('Invalid Maps API response');
    }

    const element = data.rows[0].elements[0];

    return {
      miles: (element.distance.value / 1609.34).toFixed(1),
      meters: element.distance.value,
      drive_time_minutes: Math.round(element.duration.value / 60),
      drive_time_text: element.duration.text
    };
  } catch (error) {
    console.warn('[Virtual LPR] Google Maps error, using Haversine:', error.message);
    return calculateHaversineDistance(lat1, lng1, lat2, lng2);
  }
}

/**
 * Fallback distance calculation using Haversine formula
 */
function calculateHaversineDistance(lat1, lng1, lat2, lng2) {
  const R = 3958.8; // Earth radius in miles
  const dLat = toRadians(lat2 - lat1);
  const dLng = toRadians(lng2 - lng1);

  const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
            Math.cos(toRadians(lat1)) * Math.cos(toRadians(lat2)) *
            Math.sin(dLng / 2) * Math.sin(dLng / 2);

  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  const distance = R * c;

  return {
    miles: distance.toFixed(1),
    meters: Math.round(distance * 1609.34),
    drive_time_minutes: Math.round(distance * 2), // Rough estimate: 30 mph average
    drive_time_text: null
  };
}

function toRadians(degrees) {
  return degrees * (Math.PI / 180);
}

/**
 * AI-powered lead validation using Claude
 */
async function aiValidateLead({ signal_type, signal_data, business, enrichmentData }) {
  const message = await anthropic.messages.create({
    model: 'claude-sonnet-4-20250514',
    max_tokens: 2000,
    temperature: 0.4,
    messages: [{
      role: 'user',
      content: `You are the Virtual LPR™ Detection System for ${business.name}.

BUSINESS CONTEXT:
- Name: ${business.name}
- Location: ${business.city}, ${business.state}
- Type: ${business.type || 'Local business'}
- Target Radius: ${business.target_radius_miles || 10} miles

YOUR ROLE:
Analyze "virtual sighting" signals to determine if this person is a qualified lead.

SIGNAL TYPE: ${signal_type}

SIGNAL DATA:
${JSON.stringify(signal_data, null, 2)}

ENRICHMENT DATA:
${JSON.stringify(enrichmentData, null, 2)}

---

## VIRTUAL LPR™ DETECTION FRAMEWORK

### Signal Strength Scoring (0-100)

**HIGH STRENGTH (70-100):**
- Website visit from <5 miles away
- GMB "Get Directions" clicked
- Phone call from GMB listing
- Email opened + link clicked
- Multiple touchpoints in 48 hours

**MEDIUM STRENGTH (40-69):**
- Website visit from 5-15 miles away
- GMB listing viewed (no action)
- Email opened (no click)
- Return website visitor

**LOW STRENGTH (0-39):**
- Website visit from >15 miles away
- Wrong demographics (Census data mismatch)
- Bot traffic patterns
- Single touchpoint, no engagement

### Lead Qualification Criteria

**CREATE LEAD IF:**
1. Signal strength ≥ 40, OR
2. Multiple signals (2+) within 7 days, OR
3. High-intent action (directions, phone call, pricing page)

**SKIP IF:**
- Signal strength < 40 AND single touchpoint
- Distance > ${business.max_distance_miles || 25} miles
- Demographics mismatch

### Awareness Level Attribution (Schwartz Framework)

Based on the signal type, determine awareness level:
- **Unaware**: First website visit, no prior engagement
- **Problem Aware**: Searching for solutions, reading content
- **Solution Aware**: Comparing options, visiting competitors
- **Product Aware**: Viewing pricing, requesting info
- **Most Aware**: Clicked directions, called, ready to buy

---

## YOUR TASK:

Analyze this virtual sighting and return a lead qualification decision.

**Return ONLY valid JSON in this exact format:**

{
  "qualified_lead": true or false,
  "signal_strength": 0-100,
  "reasoning": "Brief explanation (2-3 sentences)",
  "enrichment_summary": {
    "distance_miles": 3.2,
    "median_income": 65320,
    "median_age": 33,
    "zip_code": "76011"
  },
  "recommended_action": "Create lead in GHL" or "Monitor for additional signals" or "Ignore",
  "initial_tags": ["Virtual LPR - High Intent", "ZIP 76011", "Within 5 miles"],
  "predicted_lpr_score": 0-100,
  "awareness_level": "Product Aware",
  "data_attribution": {
    "census_api": ["population", "median_income", "median_age"],
    "distance_calculation": "Google Maps API" or "Haversine formula",
    "signal_source": "${signal_type}"
  }
}

**CRITICAL RULES:**
1. NEVER create leads for bot traffic
2. NEVER assume demographics - use provided Census data
3. ALWAYS calculate distance if location provided
4. Signal strength must match criteria
5. Return ONLY valid JSON, no explanations outside JSON.`
    }]
  });

  try {
    const result = JSON.parse(message.content[0].text);
    return result;
  } catch (error) {
    console.error('[Virtual LPR] Failed to parse AI response:', message.content[0].text);
    throw new Error('AI returned invalid JSON');
  }
}
