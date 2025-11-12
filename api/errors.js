/**
 * Circuit OS - Error Dashboard API
 *
 * Provides REST API for error tracking dashboard
 * Endpoints:
 * - GET /api/errors?limit=50&severity=HIGH&resolved=false
 * - GET /api/errors/stats?days=7
 * - POST /api/errors/:id/resolve
 */

import { createClient } from '@supabase/supabase-js';

const supabase = createClient(
  process.env.SUPABASE_URL,
  process.env.SUPABASE_KEY
);

export default async function handler(req, res) {
  // CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  try {
    // Parse URL path
    const urlParts = req.url.split('/');
    const errorId = urlParts[urlParts.length - 2]; // e.g., /api/errors/:id/resolve
    const action = urlParts[urlParts.length - 1]; // e.g., "resolve" or "stats"

    // GET /api/errors/stats
    if (req.method === 'GET' && action === 'stats') {
      const { days = 7 } = req.query;
      const stats = await getErrorStats(parseInt(days));
      return res.status(200).json(stats);
    }

    // POST /api/errors/:id/resolve
    if (req.method === 'POST' && action === 'resolve') {
      const result = await resolveError(errorId);
      return res.status(200).json({ success: result });
    }

    // GET /api/errors (default)
    if (req.method === 'GET') {
      const {
        limit = 50,
        severity = null,
        context = null,
        resolved = 'false',
        offset = 0
      } = req.query;

      const errors = await getErrors({
        limit: parseInt(limit),
        severity,
        context,
        resolved: resolved === 'true',
        offset: parseInt(offset)
      });

      return res.status(200).json(errors);
    }

    return res.status(405).json({ error: 'Method not allowed' });

  } catch (error) {
    console.error('[Error API] Error:', error);
    return res.status(500).json({
      error: error.message,
      stack: process.env.NODE_ENV === 'development' ? error.stack : undefined
    });
  }
}

/**
 * Get errors with filtering
 */
async function getErrors(options) {
  const {
    limit = 50,
    severity = null,
    context = null,
    resolved = false,
    offset = 0
  } = options;

  let query = supabase
    .from('error_log')
    .select('*')
    .eq('resolved', resolved)
    .order('timestamp', { ascending: false });

  if (severity) query = query.eq('severity', severity);
  if (context) query = query.eq('context', context);

  if (offset > 0) {
    query = query.range(offset, offset + limit - 1);
  } else {
    query = query.limit(limit);
  }

  const { data, error } = await query;

  if (error) {
    throw error;
  }

  return {
    errors: data || [],
    count: data?.length || 0,
    offset,
    limit
  };
}

/**
 * Get error statistics
 */
async function getErrorStats(days = 7) {
  try {
    // Call stored procedure
    const { data, error } = await supabase.rpc('get_error_stats', { days });

    if (error) throw error;

    // Also get recent critical errors
    const { data: criticalErrors } = await supabase
      .from('error_log')
      .select('id, context, error_message, timestamp, retry_count')
      .eq('severity', 'CRITICAL')
      .eq('resolved', false)
      .order('timestamp', { ascending: false })
      .limit(10);

    // Get error trend (last 7 days)
    const { data: trendData } = await supabase
      .from('error_log')
      .select('timestamp, severity')
      .gte('timestamp', new Date(Date.now() - days * 24 * 60 * 60 * 1000).toISOString())
      .order('timestamp', { ascending: true });

    // Group by day
    const trend = {};
    trendData?.forEach(error => {
      const day = error.timestamp.split('T')[0]; // YYYY-MM-DD
      if (!trend[day]) trend[day] = { date: day, total: 0, critical: 0, high: 0, medium: 0, low: 0 };
      trend[day].total++;
      trend[day][error.severity.toLowerCase()]++;
    });

    return {
      ...data,
      critical_errors: criticalErrors || [],
      trend: Object.values(trend)
    };

  } catch (error) {
    console.error('[Error Stats] Failed to get stats:', error);
    return {
      total_errors: 0,
      by_severity: {},
      by_context: {},
      unresolved_count: 0,
      critical_errors: [],
      trend: []
    };
  }
}

/**
 * Mark error as resolved
 */
async function resolveError(errorId) {
  const { data, error } = await supabase
    .from('error_log')
    .update({
      resolved: true,
      resolved_at: new Date().toISOString()
    })
    .eq('id', errorId)
    .select();

  if (error) {
    console.error('[Error API] Failed to resolve error:', error);
    return false;
  }

  return true;
}
