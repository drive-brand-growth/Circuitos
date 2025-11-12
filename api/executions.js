/**
 * Circuit OS - Execution History API
 *
 * Provides REST API for execution tracking and replay
 * Endpoints:
 * - GET /api/executions?limit=50&action=score-lead&status=SUCCESS
 * - GET /api/executions/:id
 * - GET /api/executions/stats?days=7
 * - POST /api/executions/:id/replay
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
    const lastPart = urlParts[urlParts.length - 1];
    const secondLast = urlParts[urlParts.length - 2];

    // GET /api/executions/stats
    if (req.method === 'GET' && lastPart.startsWith('stats')) {
      const { days = 7 } = req.query;
      const stats = await getExecutionStats(parseInt(days));
      return res.status(200).json(stats);
    }

    // GET /api/executions/:id (single execution)
    if (req.method === 'GET' && secondLast !== 'executions' && !lastPart.includes('?')) {
      const executionId = lastPart.split('?')[0];
      const execution = await getExecution(executionId);

      if (!execution) {
        return res.status(404).json({ error: 'Execution not found' });
      }

      return res.status(200).json(execution);
    }

    // POST /api/executions/:id/replay
    if (req.method === 'POST' && lastPart === 'replay') {
      const executionId = secondLast;
      const replayData = await replayExecution(executionId);

      if (!replayData) {
        return res.status(404).json({ error: 'Execution not found' });
      }

      return res.status(200).json(replayData);
    }

    // GET /api/executions (list with filters)
    if (req.method === 'GET') {
      const {
        limit = 50,
        action = null,
        status = null,
        contactId = null,
        offset = 0
      } = req.query;

      const executions = await getExecutions({
        limit: parseInt(limit),
        action,
        status,
        contactId,
        offset: parseInt(offset)
      });

      return res.status(200).json(executions);
    }

    return res.status(405).json({ error: 'Method not allowed' });

  } catch (error) {
    console.error('[Execution API] Error:', error);
    return res.status(500).json({
      error: error.message,
      stack: process.env.NODE_ENV === 'development' ? error.stack : undefined
    });
  }
}

/**
 * Get executions with filtering
 */
async function getExecutions(options) {
  const {
    limit = 50,
    action = null,
    status = null,
    contactId = null,
    offset = 0
  } = options;

  let query = supabase
    .from('executions')
    .select('*')
    .order('started_at', { ascending: false });

  if (action) query = query.eq('action', action);
  if (status) query = query.eq('status', status);
  if (contactId) query = query.eq('contact_id', contactId);

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
    executions: data || [],
    count: data?.length || 0,
    offset,
    limit
  };
}

/**
 * Get single execution by ID
 */
async function getExecution(executionId) {
  const { data, error } = await supabase
    .from('executions')
    .select('*')
    .eq('execution_id', executionId)
    .single();

  if (error) {
    console.error('[Execution API] Failed to fetch execution:', error);
    return null;
  }

  return data;
}

/**
 * Get execution statistics
 */
async function getExecutionStats(days = 7) {
  try {
    // Call stored procedure
    const { data, error } = await supabase.rpc('get_execution_stats', { days });

    if (error) throw error;

    // Get performance by action from view
    const { data: performanceData } = await supabase
      .from('action_performance')
      .select('*')
      .order('total_executions', { ascending: false });

    // Get recent failures
    const { data: recentFailures } = await supabase
      .from('recent_failures')
      .select('*')
      .limit(10);

    // Get execution trend (last N days)
    const { data: trendData } = await supabase
      .from('executions')
      .select('started_at, status, duration_ms')
      .gte('started_at', new Date(Date.now() - days * 24 * 60 * 60 * 1000).toISOString())
      .order('started_at', { ascending: true });

    // Group by day
    const trend = {};
    trendData?.forEach(execution => {
      const day = execution.started_at.split('T')[0]; // YYYY-MM-DD
      if (!trend[day]) {
        trend[day] = { date: day, total: 0, success: 0, failed: 0, avg_duration: 0, durations: [] };
      }
      trend[day].total++;
      if (execution.status === 'SUCCESS') trend[day].success++;
      if (execution.status === 'FAILED') trend[day].failed++;
      if (execution.duration_ms) trend[day].durations.push(execution.duration_ms);
    });

    // Calculate average duration per day
    Object.values(trend).forEach(day => {
      if (day.durations.length > 0) {
        day.avg_duration = Math.round(day.durations.reduce((a, b) => a + b, 0) / day.durations.length);
      }
      delete day.durations; // Remove raw data
    });

    return {
      ...data,
      performance_by_action: performanceData || [],
      recent_failures: recentFailures || [],
      trend: Object.values(trend)
    };

  } catch (error) {
    console.error('[Execution Stats] Failed to get stats:', error);
    return {
      total_executions: 0,
      by_status: {},
      by_action: {},
      avg_duration_ms: 0,
      total_tokens: 0,
      success_rate: 0,
      performance_by_action: [],
      recent_failures: [],
      trend: []
    };
  }
}

/**
 * Replay an execution
 */
async function replayExecution(executionId) {
  try {
    const execution = await getExecution(executionId);

    if (!execution) {
      return null;
    }

    // Return the original input data for replay
    return {
      action: execution.action,
      contactId: execution.contact_id,
      businessId: execution.business_id,
      inputData: execution.input_data,
      originalExecutionId: executionId,
      originalStatus: execution.status,
      originalStartedAt: execution.started_at,
      originalDuration: execution.duration_ms,
      originalTokens: execution.tokens_used
    };

  } catch (error) {
    console.error('[Execution API] Error replaying execution:', error);
    return null;
  }
}
