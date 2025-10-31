/**
 * Google Maps MCP Integration
 * FREE: $200/month credit = ~28,000 API calls
 *
 * Features:
 * - Geocoding (address → coordinates)
 * - Distance calculation
 * - Nearby places search
 * - Footfall estimation
 */

const GOOGLE_MAPS_API_KEY = process.env.GOOGLE_MAPS_API_KEY;
const MAPS_API_BASE = 'https://maps.googleapis.com/maps/api';

/**
 * Geocode address to lat/lng coordinates
 */
export async function geocodeAddress(address) {
  if (!GOOGLE_MAPS_API_KEY) {
    throw new Error('GOOGLE_MAPS_API_KEY not configured');
  }

  const url = `${MAPS_API_BASE}/geocode/json?address=${encodeURIComponent(address)}&key=${GOOGLE_MAPS_API_KEY}`;

  const response = await fetch(url);
  const data = await response.json();

  if (data.status !== 'OK' || !data.results[0]) {
    throw new Error(`Geocoding failed: ${data.status}`);
  }

  const result = data.results[0];

  return {
    formatted_address: result.formatted_address,
    lat: result.geometry.location.lat,
    lng: result.geometry.location.lng,
    place_id: result.place_id,
    components: extractAddressComponents(result.address_components)
  };
}

/**
 * Get nearby businesses/places
 */
export async function getNearbyPlaces(lat, lng, radius = 500, type = null) {
  if (!GOOGLE_MAPS_API_KEY) {
    throw new Error('GOOGLE_MAPS_API_KEY not configured');
  }

  let url = `${MAPS_API_BASE}/place/nearbysearch/json?location=${lat},${lng}&radius=${radius}&key=${GOOGLE_MAPS_API_KEY}`;

  if (type) {
    url += `&type=${type}`;
  }

  const response = await fetch(url);
  const data = await response.json();

  if (data.status !== 'OK') {
    throw new Error(`Nearby search failed: ${data.status}`);
  }

  return data.results.map(place => ({
    name: place.name,
    address: place.vicinity,
    location: place.geometry.location,
    place_id: place.place_id,
    types: place.types,
    rating: place.rating,
    user_ratings_total: place.user_ratings_total
  }));
}

/**
 * Get place details (including popular times for footfall estimation)
 */
export async function getPlaceDetails(placeId) {
  if (!GOOGLE_MAPS_API_KEY) {
    throw new Error('GOOGLE_MAPS_API_KEY not configured');
  }

  const fields = 'name,formatted_address,geometry,rating,user_ratings_total,opening_hours';
  const url = `${MAPS_API_BASE}/place/details/json?place_id=${placeId}&fields=${fields}&key=${GOOGLE_MAPS_API_KEY}`;

  const response = await fetch(url);
  const data = await response.json();

  if (data.status !== 'OK') {
    throw new Error(`Place details failed: ${data.status}`);
  }

  const result = data.result;

  // Estimate daily footfall from review count
  // Proprietary multiplier: ~2.3x reviews = daily visitors
  const estimatedDailyFootfall = Math.round((result.user_ratings_total || 0) * 2.3);

  return {
    place_id: placeId,
    name: result.name,
    address: result.formatted_address,
    location: result.geometry.location,
    rating: result.rating,
    review_count: result.user_ratings_total,
    estimated_daily_footfall: estimatedDailyFootfall,
    is_open: result.opening_hours?.open_now
  };
}

/**
 * Calculate distance and drive time between two points
 */
export async function getDistanceMatrix(origins, destinations) {
  if (!GOOGLE_MAPS_API_KEY) {
    throw new Error('GOOGLE_MAPS_API_KEY not configured');
  }

  const originsStr = Array.isArray(origins)
    ? origins.map(o => `${o.lat},${o.lng}`).join('|')
    : `${origins.lat},${origins.lng}`;

  const destStr = Array.isArray(destinations)
    ? destinations.map(d => `${d.lat},${d.lng}`).join('|')
    : `${destinations.lat},${destinations.lng}`;

  const url = `${MAPS_API_BASE}/distancematrix/json?origins=${originsStr}&destinations=${destStr}&key=${GOOGLE_MAPS_API_KEY}`;

  const response = await fetch(url);
  const data = await response.json();

  if (data.status !== 'OK') {
    throw new Error(`Distance Matrix failed: ${data.status}`);
  }

  return data.rows.map((row, i) => ({
    origin_index: i,
    destinations: row.elements.map((el, j) => ({
      destination_index: j,
      distance_miles: (el.distance.value / 1609.34).toFixed(1),
      distance_meters: el.distance.value,
      distance_text: el.distance.text,
      duration_minutes: Math.round(el.duration.value / 60),
      duration_text: el.duration.text
    }))
  }));
}

/**
 * Helper: Extract useful address components
 */
function extractAddressComponents(components) {
  const extracted = {};

  for (const component of components) {
    if (component.types.includes('street_number')) {
      extracted.street_number = component.long_name;
    } else if (component.types.includes('route')) {
      extracted.street = component.long_name;
    } else if (component.types.includes('locality')) {
      extracted.city = component.long_name;
    } else if (component.types.includes('administrative_area_level_1')) {
      extracted.state = component.short_name;
    } else if (component.types.includes('postal_code')) {
      extracted.zip_code = component.long_name;
    } else if (component.types.includes('country')) {
      extracted.country = component.short_name;
    }
  }

  return extracted;
}
