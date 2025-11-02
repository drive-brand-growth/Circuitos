/**
 * OpenStreetMap MCP Integration
 * Free, unlimited geocoding and mapping (backup for Google Maps)
 *
 * Cost: $0 (completely free, no API key required, unlimited requests)
 * Setup: No credentials needed!
 * Docs: https://nominatim.org/release-docs/latest/api/Overview/
 */

import axios from 'axios';

const OSM_GEOCODE_URL = 'https://nominatim.openstreetmap.org/search';
const OSM_REVERSE_URL = 'https://nominatim.openstreetmap.org/reverse';

// User agent required by OSM usage policy
const USER_AGENT = 'CircuitOS-DualPathLeadSystem/1.0';

/**
 * Geocode address to lat/lng
 * Free alternative to Google Maps geocoding
 *
 * @param {string} address - Address to geocode
 * @returns {object} Location with lat/lng
 */
export async function geocodeAddress(address) {
  try {
    const response = await axios.get(OSM_GEOCODE_URL, {
      params: {
        q: address,
        format: 'json',
        limit: 1,
        addressdetails: 1
      },
      headers: {
        'User-Agent': USER_AGENT
      }
    });

    if (!response.data || response.data.length === 0) {
      return null;
    }

    const result = response.data[0];

    return {
      lat: parseFloat(result.lat),
      lng: parseFloat(result.lon),
      formatted_address: result.display_name,
      address_components: {
        city: result.address?.city || result.address?.town || result.address?.village,
        state: result.address?.state,
        country: result.address?.country,
        postal_code: result.address?.postcode,
        county: result.address?.county
      },
      source: 'openstreetmap'
    };

  } catch (error) {
    console.error('OSM Geocode Error:', error.message);
    return null;
  }
}

/**
 * Reverse geocode lat/lng to address
 *
 * @param {number} lat - Latitude
 * @param {number} lng - Longitude
 * @returns {object} Address details
 */
export async function reverseGeocode(lat, lng) {
  try {
    const response = await axios.get(OSM_REVERSE_URL, {
      params: {
        lat,
        lon: lng,
        format: 'json',
        addressdetails: 1
      },
      headers: {
        'User-Agent': USER_AGENT
      }
    });

    if (!response.data) {
      return null;
    }

    const result = response.data;

    return {
      formatted_address: result.display_name,
      address_components: {
        street: result.address?.road,
        city: result.address?.city || result.address?.town || result.address?.village,
        state: result.address?.state,
        country: result.address?.country,
        postal_code: result.address?.postcode,
        county: result.address?.county
      },
      lat,
      lng,
      source: 'openstreetmap'
    };

  } catch (error) {
    console.error('OSM Reverse Geocode Error:', error.message);
    return null;
  }
}

/**
 * Search for places/businesses (alternative to Google Places)
 *
 * @param {string} query - Search query
 * @param {number} lat - Center latitude
 * @param {number} lng - Center longitude
 * @param {number} radius - Search radius in km (default: 5)
 * @returns {array} Places found
 */
export async function searchPlaces(query, lat, lng, radius = 5) {
  try {
    // Create a bounding box around the center point
    // Roughly 1 degree = 111km
    const degreeOffset = radius / 111;

    const response = await axios.get(OSM_GEOCODE_URL, {
      params: {
        q: query,
        format: 'json',
        limit: 20,
        bounded: 1,
        viewbox: `${lng - degreeOffset},${lat + degreeOffset},${lng + degreeOffset},${lat - degreeOffset}`,
        addressdetails: 1
      },
      headers: {
        'User-Agent': USER_AGENT
      }
    });

    if (!response.data) {
      return [];
    }

    return response.data.map(place => ({
      name: place.display_name.split(',')[0],
      lat: parseFloat(place.lat),
      lng: parseFloat(place.lon),
      address: place.display_name,
      type: place.type,
      category: place.class,
      distance: calculateDistance(lat, lng, parseFloat(place.lat), parseFloat(place.lon)),
      source: 'openstreetmap'
    }));

  } catch (error) {
    console.error('OSM Search Places Error:', error.message);
    return [];
  }
}

/**
 * Calculate distance between two points (Haversine formula)
 *
 * @param {number} lat1 - Latitude 1
 * @param {number} lng1 - Longitude 1
 * @param {number} lat2 - Latitude 2
 * @param {number} lng2 - Longitude 2
 * @returns {number} Distance in miles
 */
export function calculateDistance(lat1, lng1, lat2, lng2) {
  const R = 3958.8; // Earth's radius in miles
  const dLat = toRad(lat2 - lat1);
  const dLng = toRad(lng2 - lng1);

  const a =
    Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) *
    Math.sin(dLng / 2) * Math.sin(dLng / 2);

  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  const distance = R * c;

  return Math.round(distance * 10) / 10; // Round to 1 decimal
}

function toRad(degrees) {
  return degrees * (Math.PI / 180);
}

/**
 * Geocode with Google Maps fallback to OSM
 * Use this as your primary geocoding function
 *
 * @param {string} address - Address to geocode
 * @param {function} googleMapsGeocode - Google Maps geocode function
 * @returns {object} Location data
 */
export async function geocodeWithFallback(address, googleMapsGeocode = null) {
  // Try Google Maps first (better accuracy)
  if (googleMapsGeocode && process.env.GOOGLE_MAPS_API_KEY) {
    try {
      const result = await googleMapsGeocode(address);
      if (result) {
        return result;
      }
    } catch (error) {
      // If quota exceeded or error, fall back to OSM
      console.warn('Google Maps failed, falling back to OSM:', error.message);
    }
  }

  // Use OSM as fallback (free, unlimited)
  return await geocodeAddress(address);
}

/**
 * Get ZIP code from lat/lng
 *
 * @param {number} lat - Latitude
 * @param {number} lng - Longitude
 * @returns {string} ZIP code
 */
export async function getZipCode(lat, lng) {
  try {
    const result = await reverseGeocode(lat, lng);
    return result?.address_components?.postal_code || null;
  } catch (error) {
    console.error('OSM Get ZIP Error:', error.message);
    return null;
  }
}

/**
 * Batch geocode multiple addresses
 * Note: OSM has rate limits (1 request/second), so we add delays
 *
 * @param {array} addresses - Array of addresses
 * @returns {array} Geocoded results
 */
export async function batchGeocode(addresses) {
  const results = [];

  for (const address of addresses) {
    const result = await geocodeAddress(address);
    results.push({
      input: address,
      result
    });

    // Respect OSM rate limit: 1 request per second
    await new Promise(resolve => setTimeout(resolve, 1100));
  }

  return results;
}

export default {
  geocodeAddress,
  reverseGeocode,
  searchPlaces,
  calculateDistance,
  geocodeWithFallback,
  getZipCode,
  batchGeocode
};
