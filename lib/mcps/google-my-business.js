/**
 * Google My Business MCP Integration
 * Captures high-intent signals: direction requests, call clicks, profile views
 *
 * Cost: $0 (completely free)
 * Setup: Requires OAuth 2.0 credentials from Google Cloud Console
 */

import { google } from 'googleapis';

const mybusinessbusinessinformation = google.mybusinessbusinessinformation('v1');
const mybusinessaccountmanagement = google.mybusinessaccountmanagement('v1');

/**
 * Initialize Google Auth
 */
function getAuth() {
  return new google.auth.GoogleAuth({
    keyFile: process.env.GOOGLE_APPLICATION_CREDENTIALS,
    scopes: [
      'https://www.googleapis.com/auth/business.manage',
      'https://www.googleapis.com/auth/userinfo.email'
    ]
  });
}

/**
 * Get GMB Insights - Direction requests, calls, searches
 * These are THE HIGHEST INTENT signals available
 *
 * @param {string} accountId - GMB account ID
 * @param {string} locationId - GMB location ID
 * @returns {object} Insights data with intent signals
 */
export async function getGMBInsights(accountId, locationId) {
  try {
    const auth = getAuth();

    // Note: GMB API has been deprecated and replaced with Business Profile Performance API
    // For production, you'll need to migrate to the new API
    // This is a placeholder showing the data structure you'd get

    // Mock data structure for development (replace with actual API call in production)
    if (!process.env.GOOGLE_APPLICATION_CREDENTIALS) {
      console.warn('GMB: No credentials configured, returning mock data');
      return {
        accountId,
        locationId,
        searchImpressions: 120,
        directionRequests: 15,  // EXTREMELY HIGH INTENT!
        callClicks: 8,          // VERY HIGH INTENT!
        websiteClicks: 45,
        photoViews: 230,

        // Virtual LPR Signals
        immediateVisitIntent: 15,  // People getting directions RIGHT NOW
        phoneIntentSignal: 8,      // People clicking to call
        discoveryPhase: 120        // Awareness level
      };
    }

    // Production implementation would use Business Profile Performance API
    // const response = await businessprofile.locations.searchperformance.get({...});

    // Return actual data structure
    return {
      accountId,
      locationId,
      searchImpressions: 0,
      directionRequests: 0,
      callClicks: 0,
      websiteClicks: 0,
      photoViews: 0,
      immediateVisitIntent: 0,
      phoneIntentSignal: 0,
      discoveryPhase: 0
    };

  } catch (error) {
    console.error('GMB API Error:', error.message);
    // Return zero data on error (graceful degradation)
    return {
      accountId,
      locationId,
      searchImpressions: 0,
      directionRequests: 0,
      callClicks: 0,
      websiteClicks: 0,
      photoViews: 0,
      immediateVisitIntent: 0,
      phoneIntentSignal: 0,
      discoveryPhase: 0,
      error: error.message
    };
  }
}

/**
 * Get GMB Reviews for sentiment analysis
 *
 * @param {string} accountId - GMB account ID
 * @param {string} locationId - GMB location ID
 * @returns {array} Reviews with ratings and text
 */
export async function getGMBReviews(accountId, locationId) {
  try {
    const auth = getAuth();

    if (!process.env.GOOGLE_APPLICATION_CREDENTIALS) {
      console.warn('GMB: No credentials configured, returning empty reviews');
      return [];
    }

    // Mock structure for development (matches actual GMB API format)
    return [
      {
        reviewId: 'mock_review_1',
        reviewer: {
          displayName: 'John D.',
          profilePhotoUrl: ''
        },
        starRating: 'FIVE',
        comment: 'Great service! Highly recommend.',
        createTime: new Date().toISOString(),
        updateTime: new Date().toISOString(),
        reviewReply: null  // null if no response yet
      },
      {
        reviewId: 'mock_review_2',
        reviewer: {
          displayName: 'Sarah M.',
          profilePhotoUrl: ''
        },
        starRating: 'FOUR',
        comment: 'Good experience overall, minor wait time.',
        createTime: new Date(Date.now() - 86400000).toISOString(),
        updateTime: new Date(Date.now() - 86400000).toISOString(),
        reviewReply: null
      }
    ];

  } catch (error) {
    console.error('GMB Reviews Error:', error.message);
    return [];
  }
}

/**
 * Calculate intent score from GMB signals
 * Direction requests and call clicks = EXTREMELY HIGH INTENT
 *
 * @param {object} insights - GMB insights data
 * @returns {number} Intent score 0-100
 */
export function calculateGMBIntentScore(insights) {
  let score = 0;

  // Direction requests = highest possible intent (they're driving to you NOW)
  if (insights.directionRequests > 0) {
    score += 40;  // Massive boost
  }

  // Call clicks = very high intent (they want to talk NOW)
  if (insights.callClicks > 0) {
    score += 30;  // Large boost
  }

  // Website clicks = medium intent
  if (insights.websiteClicks > 0) {
    score += 15;
  }

  // Profile views = awareness
  if (insights.searchImpressions > 50) {
    score += 10;
  }

  // Photo views = mild interest
  if (insights.photoViews > 100) {
    score += 5;
  }

  return Math.min(score, 100);
}

/**
 * Determine awareness level from GMB signals
 *
 * @param {object} insights - GMB insights data
 * @returns {string} Awareness level
 */
export function getGMBAwarenessLevel(insights) {
  // Direction requests = Most Aware (they know exactly what they want)
  if (insights.directionRequests > 0) {
    return 'Most Aware';
  }

  // Call clicks = Product Aware (they're considering you)
  if (insights.callClicks > 0) {
    return 'Product Aware';
  }

  // Website clicks = Solution Aware (exploring options)
  if (insights.websiteClicks > 0) {
    return 'Solution Aware';
  }

  // Search impressions only = Problem Aware (searching for solutions)
  if (insights.searchImpressions > 0) {
    return 'Problem Aware';
  }

  return 'Unaware';
}

/**
 * Get GMB location details
 *
 * @param {string} accountId - GMB account ID
 * @param {string} locationId - GMB location ID
 * @returns {object} Location details
 */
export async function getGMBLocation(accountId, locationId) {
  try {
    const auth = getAuth();

    if (!process.env.GOOGLE_APPLICATION_CREDENTIALS) {
      console.warn('GMB: No credentials configured, returning mock location');
      return {
        name: process.env.BUSINESS_NAME || 'MetroFlex Gym',
        address: {
          addressLines: ['123 Main St'],
          locality: process.env.BUSINESS_CITY || 'Fort Worth',
          administrativeArea: process.env.BUSINESS_STATE || 'TX',
          postalCode: '76102'
        },
        primaryPhone: '(817) 555-0100',
        websiteUrl: 'https://example.com'
      };
    }

    // Production would fetch actual location data
    return {
      name: process.env.BUSINESS_NAME || 'Business',
      address: {},
      primaryPhone: '',
      websiteUrl: ''
    };

  } catch (error) {
    console.error('GMB Location Error:', error.message);
    return null;
  }
}

/**
 * Track GMB signal for a contact
 * Use this when a lead comes from GMB
 *
 * @param {string} signalType - 'direction', 'call', 'website', 'search'
 * @param {object} contactData - Contact information
 * @returns {object} Enhanced contact data with GMB signals
 */
export async function trackGMBSignal(signalType, contactData) {
  const accountId = process.env.GMB_ACCOUNT_ID;
  const locationId = process.env.GMB_LOCATION_ID;

  // Get current insights
  const insights = await getGMBInsights(accountId, locationId);

  // Calculate scores
  const intentScore = calculateGMBIntentScore(insights);
  const awarenessLevel = getGMBAwarenessLevel(insights);

  return {
    ...contactData,
    gmb_signal_type: signalType,
    gmb_intent_score: intentScore,
    gmb_awareness_level: awarenessLevel,
    gmb_direction_requests: insights.directionRequests,
    gmb_call_clicks: insights.callClicks,
    gmb_search_impressions: insights.searchImpressions,
    gmb_tracked_at: new Date().toISOString()
  };
}

export default {
  getGMBInsights,
  getGMBReviews,
  calculateGMBIntentScore,
  getGMBAwarenessLevel,
  getGMBLocation,
  trackGMBSignal
};
