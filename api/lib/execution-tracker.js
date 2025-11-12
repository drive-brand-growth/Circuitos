/**
 * Circuit OS - Execution Tracking System
 *
 * Tracks all API executions with full input/output for debugging and analytics
 * Provides visibility into:
 * - What agents are doing
 * - Performance metrics
 * - Success/failure rates
 * - Token usage
 */

import { createClient } from '@supabase/supabase-js';

const supabase = createClient(
  process.env.SUPABASE_URL,
  process.env.SUPABASE_KEY
);

class ExecutionTracker {

  /**
   * Start tracking a new execution
   */
  async startExecution(action, contactId, businessId, inputData, metadata = {}) {
    try {
      const executionId = `exec-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;

      const { data, error } = await supabase
        .from('executions')
        .insert({
          execution_id: executionId,
          action,
          contact_id: contactId,
          business_id: businessId,
          status: 'RUNNING',
          started_at: new Date().toISOString(),
          input_data: inputData,
          metadata: {
            ...metadata,
            startTime: Date.now()
          }
        })
        .select();

      if (error) {
        console.error('[ExecutionTracker] Failed to start execution:', error);
        // Return a fallback execution ID even if DB insert fails
        return executionId;
      }

      console.log(`[ExecutionTracker] Started execution: ${executionId} (${action})`);
      return executionId;

    } catch (error) {
      console.error('[ExecutionTracker] Error starting execution:', error);
      // Return fallback ID
      return `exec-${Date.now()}-fallback`;
    }
  }

  /**
   * Mark execution as completed successfully
   */
  async completeExecution(executionId, result, metadata = {}) {
    try {
      const duration = metadata.duration || (Date.now() - (metadata.startTime || 0));

      const { data, error } = await supabase
        .from('executions')
        .update({
          status: 'SUCCESS',
          completed_at: new Date().toISOString(),
          duration_ms: duration,
          output_data: result,
          tokens_used: metadata.tokens || metadata.tokensUsed || 0,
          metadata: {
            ...metadata,
            completedAt: Date.now()
          }
        })
        .eq('execution_id', executionId)
        .select();

      if (error) {
        console.error('[ExecutionTracker] Failed to complete execution:', error);
        return false;
      }

      console.log(`[ExecutionTracker] Completed execution: ${executionId} (${duration}ms)`);
      return true;

    } catch (error) {
      console.error('[ExecutionTracker] Error completing execution:', error);
      return false;
    }
  }

  /**
   * Mark execution as failed
   */
  async failExecution(executionId, error, metadata = {}) {
    try {
      const duration = metadata.duration || (Date.now() - (metadata.startTime || 0));

      const { data, dbError } = await supabase
        .from('executions')
        .update({
          status: 'FAILED',
          completed_at: new Date().toISOString(),
          duration_ms: duration,
          error_message: error.message || error.toString(),
          error_stack: error.stack,
          metadata: {
            ...metadata,
            failedAt: Date.now()
          }
        })
        .eq('execution_id', executionId)
        .select();

      if (dbError) {
        console.error('[ExecutionTracker] Failed to mark execution as failed:', dbError);
        return false;
      }

      console.error(`[ExecutionTracker] Failed execution: ${executionId} - ${error.message}`);
      return true;

    } catch (trackingError) {
      console.error('[ExecutionTracker] Error marking execution as failed:', trackingError);
      return false;
    }
  }

  /**
   * Get execution details
   */
  async getExecution(executionId) {
    try {
      const { data, error } = await supabase
        .from('executions')
        .select('*')
        .eq('execution_id', executionId)
        .single();

      if (error) {
        console.error('[ExecutionTracker] Failed to fetch execution:', error);
        return null;
      }

      return data;

    } catch (error) {
      console.error('[ExecutionTracker] Error fetching execution:', error);
      return null;
    }
  }

  /**
   * Get recent executions with filters
   */
  async getRecentExecutions(options = {}) {
    try {
      const {
        limit = 50,
        contactId = null,
        action = null,
        status = null,
        offset = 0
      } = options;

      let query = supabase
        .from('executions')
        .select('*')
        .order('started_at', { ascending: false });

      if (contactId) query = query.eq('contact_id', contactId);
      if (action) query = query.eq('action', action);
      if (status) query = query.eq('status', status);

      if (offset > 0) query = query.range(offset, offset + limit - 1);
      else query = query.limit(limit);

      const { data, error } = await query;

      if (error) {
        console.error('[ExecutionTracker] Failed to fetch executions:', error);
        return [];
      }

      return data;

    } catch (error) {
      console.error('[ExecutionTracker] Error fetching executions:', error);
      return [];
    }
  }

  /**
   * Get execution statistics
   */
  async getExecutionStats(days = 7) {
    try {
      const { data, error } = await supabase.rpc('get_execution_stats', { days });

      if (error) throw error;

      return data;

    } catch (error) {
      console.error('[ExecutionTracker] Failed to get execution stats:', error);
      return {
        total_executions: 0,
        by_status: {},
        by_action: {},
        avg_duration_ms: 0,
        total_tokens: 0,
        success_rate: 0
      };
    }
  }

  /**
   * Get performance metrics by action
   */
  async getActionPerformance() {
    try {
      const { data, error } = await supabase
        .from('action_performance')
        .select('*');

      if (error) throw error;

      return data;

    } catch (error) {
      console.error('[ExecutionTracker] Failed to get action performance:', error);
      return [];
    }
  }

  /**
   * Replay an execution (for testing)
   */
  async replayExecution(executionId) {
    try {
      const execution = await this.getExecution(executionId);

      if (!execution) {
        throw new Error(`Execution ${executionId} not found`);
      }

      // Return the original input data for replay
      return {
        action: execution.action,
        contactId: execution.contact_id,
        businessId: execution.business_id,
        inputData: execution.input_data,
        originalExecutionId: executionId,
        originalStatus: execution.status,
        originalStartedAt: execution.started_at
      };

    } catch (error) {
      console.error('[ExecutionTracker] Error replaying execution:', error);
      return null;
    }
  }

  /**
   * Get execution count by contact (for rate limiting)
   */
  async getExecutionCountByContact(contactId, hours = 24) {
    try {
      const { count, error } = await supabase
        .from('executions')
        .select('*', { count: 'exact', head: true })
        .eq('contact_id', contactId)
        .gte('started_at', new Date(Date.now() - hours * 60 * 60 * 1000).toISOString());

      if (error) throw error;

      return count || 0;

    } catch (error) {
      console.error('[ExecutionTracker] Error getting execution count:', error);
      return 0;
    }
  }
}

// Singleton instance
const executionTracker = new ExecutionTracker();

export default executionTracker;
