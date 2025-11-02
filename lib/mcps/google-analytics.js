/**
 * Google Analytics 4 MCP Integration
 * Track website visitor behavior BEFORE they convert
 * Proactive lead identification ("virtual passersby")
 *
 * Cost: $0 (completely free, unlimited)
 * Setup: Requires service account credentials from Google Cloud Console
 */

import { BetaAnalyticsDataClient } from '@google-analytics/data';

let analyticsClient = null;

/**
 * Initialize GA4 client
 */
function getClient() {
  if (!analyticsClient) {
    analyticsClient = new BetaAnalyticsDataClient({
      keyFilename: process.env.GOOGLE_APPLICATION_CREDENTIALS
    });
  }
  return analyticsClient;
}

/**
 * Get visitor geolocation data for Virtual LPR
 * Identifies "virtual passersby" by location
 *
 * @param {string} startDate - Start date (default: 7daysAgo)
 * @param {string} endDate - End date (default: today)
 * @returns {array} Visitor locations with engagement metrics
 */
export async function getVisitorLocations(startDate = '7daysAgo', endDate = 'today') {
  try {
    if (!process.env.GA4_PROPERTY_ID) {
      console.warn('GA4: No property ID configured, returning empty data');
      return [];
    }

    const client = getClient();

    const [response] = await client.runReport({
      property: `properties/${process.env.GA4_PROPERTY_ID}`,
      dateRanges: [{ startDate, endDate }],
      dimensions: [
        { name: 'city' },
        { name: 'region' },
        { name: 'country' }
      ],
      metrics: [
        { name: 'activeUsers' },
        { name: 'sessions' },
        { name: 'averageSessionDuration' },
        { name: 'screenPageViews' }
      ],
      orderBys: [
        {
          metric: { metricName: 'activeUsers' },
          desc: true
        }
      ]
    });

    return response.rows?.map(row => ({
      city: row.dimensionValues[0].value,
      region: row.dimensionValues[1].value,
      country: row.dimensionValues[2].value,
      users: parseInt(row.metricValues[0].value),
      sessions: parseInt(row.metricValues[1].value),
      avgDuration: parseFloat(row.metricValues[2].value),
      pageViews: parseInt(row.metricValues[3].value),

      // Virtual LPR signals
      engagementScore: calculateEngagementScore(
        parseInt(row.metricValues[1].value),
        parseFloat(row.metricValues[2].value),
        parseInt(row.metricValues[3].value)
      )
    })) || [];

  } catch (error) {
    console.error('GA4 Visitor Locations Error:', error.message);
    return [];
  }
}

/**
 * Get high-intent visitors (5+ pages viewed, 3+ min session)
 * These are "virtual passersby" ready to convert
 *
 * @param {string} startDate - Start date
 * @param {string} endDate - End date
 * @returns {array} High-intent visitors
 */
export async function getHighIntentVisitors(startDate = 'today', endDate = 'today') {
  try {
    if (!process.env.GA4_PROPERTY_ID) {
      console.warn('GA4: No property ID configured, returning empty data');
      return [];
    }

    const client = getClient();

    const [response] = await client.runReport({
      property: `properties/${process.env.GA4_PROPERTY_ID}`,
      dateRanges: [{ startDate, endDate }],
      dimensions: [
        { name: 'sessionDefaultChannelGroup' },
        { name: 'deviceCategory' }
      ],
      metrics: [
        { name: 'activeUsers' },
        { name: 'engagementRate' },
        { name: 'screenPageViewsPerSession' },
        { name: 'averageSessionDuration' }
      ],
      // Filter for high engagement
      metricFilter: {
        andGroup: {
          expressions: [
            {
              filter: {
                fieldName: 'screenPageViewsPerSession',
                numericFilter: {
                  operation: 'GREATER_THAN',
                  value: { doubleValue: 3 }
                }
              }
            },
            {
              filter: {
                fieldName: 'averageSessionDuration',
                numericFilter: {
                  operation: 'GREATER_THAN',
                  value: { doubleValue: 120 }
                }
              }
            }
          ]
        }
      }
    });

    return response.rows?.map(row => ({
      channel: row.dimensionValues[0].value,
      device: row.dimensionValues[1].value,
      users: parseInt(row.metricValues[0].value),
      engagementRate: parseFloat(row.metricValues[1].value),
      pagesPerSession: parseFloat(row.metricValues[2].value),
      avgDuration: parseFloat(row.metricValues[3].value),
      intentLevel: 'HIGH'
    })) || [];

  } catch (error) {
    console.error('GA4 High Intent Visitors Error:', error.message);
    return [];
  }
}

/**
 * Track conversion events
 *
 * @param {string} startDate - Start date
 * @param {string} endDate - End date
 * @returns {array} Conversion events
 */
export async function getConversionEvents(startDate = '7daysAgo', endDate = 'today') {
  try {
    if (!process.env.GA4_PROPERTY_ID) {
      console.warn('GA4: No property ID configured, returning empty data');
      return [];
    }

    const client = getClient();

    const [response] = await client.runReport({
      property: `properties/${process.env.GA4_PROPERTY_ID}`,
      dateRanges: [{ startDate, endDate }],
      dimensions: [{ name: 'eventName' }],
      metrics: [
        { name: 'eventCount' },
        { name: 'conversions' }
      ],
      dimensionFilter: {
        filter: {
          fieldName: 'eventName',
          inListFilter: {
            values: ['form_submit', 'contact_submit', 'purchase', 'lead_generated']
          }
        }
      }
    });

    return response.rows?.map(row => ({
      eventName: row.dimensionValues[0].value,
      eventCount: parseInt(row.metricValues[0].value),
      conversions: parseInt(row.metricValues[1].value),
      conversionRate: (parseInt(row.metricValues[1].value) / parseInt(row.metricValues[0].value) * 100).toFixed(2)
    })) || [];

  } catch (error) {
    console.error('GA4 Conversion Events Error:', error.message);
    return [];
  }
}

/**
 * Get visitor by client ID (for individual tracking)
 *
 * @param {string} clientId - GA4 client ID
 * @returns {object} Visitor data
 */
export async function getVisitorByClientId(clientId) {
  try {
    if (!process.env.GA4_PROPERTY_ID || !clientId) {
      return null;
    }

    const client = getClient();

    const [response] = await client.runReport({
      property: `properties/${process.env.GA4_PROPERTY_ID}`,
      dateRanges: [{ startDate: '30daysAgo', endDate: 'today' }],
      dimensions: [
        { name: 'city' },
        { name: 'deviceCategory' }
      ],
      metrics: [
        { name: 'sessions' },
        { name: 'screenPageViews' },
        { name: 'averageSessionDuration' }
      ],
      dimensionFilter: {
        filter: {
          fieldName: 'sessionId',
          stringFilter: {
            matchType: 'EXACT',
            value: clientId
          }
        }
      }
    });

    if (!response.rows || response.rows.length === 0) {
      return null;
    }

    const row = response.rows[0];
    const sessions = parseInt(row.metricValues[0].value);
    const pageViews = parseInt(row.metricValues[1].value);
    const avgDuration = parseFloat(row.metricValues[2].value);

    return {
      clientId,
      city: row.dimensionValues[0].value,
      device: row.dimensionValues[1].value,
      totalSessions: sessions,
      pagesViewed: pageViews,
      sessionDuration: avgDuration,

      // Virtual LPR signals
      engagementScore: calculateEngagementScore(sessions, avgDuration, pageViews),
      awarenessLevel: determineAwarenessLevel(sessions, pageViews, avgDuration),
      isHighIntent: pageViews >= 5 && avgDuration >= 180
    };

  } catch (error) {
    console.error('GA4 Get Visitor Error:', error.message);
    return null;
  }
}

/**
 * Calculate engagement score from GA4 metrics
 *
 * @param {number} sessions - Number of sessions
 * @param {number} avgDuration - Average session duration (seconds)
 * @param {number} pageViews - Page views
 * @returns {number} Engagement score 0-100
 */
function calculateEngagementScore(sessions, avgDuration, pageViews) {
  let score = 0;

  // Multiple sessions = returning visitor (high interest)
  if (sessions >= 3) score += 30;
  else if (sessions >= 2) score += 15;
  else if (sessions >= 1) score += 5;

  // Time on site = engagement level
  if (avgDuration >= 300) score += 30;  // 5+ min
  else if (avgDuration >= 180) score += 20;  // 3+ min
  else if (avgDuration >= 60) score += 10;   // 1+ min

  // Page views = interest breadth
  if (pageViews >= 10) score += 25;
  else if (pageViews >= 5) score += 15;
  else if (pageViews >= 3) score += 5;

  // Bonus for "power users"
  if (sessions >= 3 && avgDuration >= 180 && pageViews >= 7) {
    score += 15;  // Bonus: highly engaged
  }

  return Math.min(score, 100);
}

/**
 * Determine awareness level from engagement patterns
 *
 * @param {number} sessions - Number of sessions
 * @param {number} pageViews - Page views
 * @param {number} avgDuration - Average duration
 * @returns {string} Awareness level
 */
function determineAwarenessLevel(sessions, pageViews, avgDuration) {
  // Multiple sessions + deep engagement = Most Aware
  if (sessions >= 3 && pageViews >= 7 && avgDuration >= 180) {
    return 'Most Aware';
  }

  // Returning visitor exploring = Product Aware
  if (sessions >= 2 && pageViews >= 5) {
    return 'Product Aware';
  }

  // Deep first session = Solution Aware
  if (sessions === 1 && pageViews >= 5 && avgDuration >= 180) {
    return 'Solution Aware';
  }

  // Moderate engagement = Problem Aware
  if (pageViews >= 3) {
    return 'Problem Aware';
  }

  // Bounce or quick visit = Unaware
  return 'Unaware';
}

/**
 * Get real-time active users (last 30 minutes)
 *
 * @returns {number} Active users count
 */
export async function getRealtimeUsers() {
  try {
    if (!process.env.GA4_PROPERTY_ID) {
      return 0;
    }

    const client = getClient();

    const [response] = await client.runRealtimeReport({
      property: `properties/${process.env.GA4_PROPERTY_ID}`,
      metrics: [{ name: 'activeUsers' }]
    });

    return parseInt(response.rows?.[0]?.metricValues?.[0]?.value || 0);

  } catch (error) {
    console.error('GA4 Realtime Users Error:', error.message);
    return 0;
  }
}

export default {
  getVisitorLocations,
  getHighIntentVisitors,
  getConversionEvents,
  getVisitorByClientId,
  getRealtimeUsers,
  calculateEngagementScore,
  determineAwarenessLevel
};
