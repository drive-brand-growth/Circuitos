/**
 * Circuit OS - Error Tracking & Retry System
 *
 * Provides:
 * - Automatic error logging to Supabase
 * - Error severity classification
 * - Retry logic with exponential backoff
 * - Admin notifications for critical errors
 */

import { createClient } from '@supabase/supabase-js';

const supabase = createClient(
  process.env.SUPABASE_URL,
  process.env.SUPABASE_KEY
);

class ErrorTracker {

  /**
   * Log an error to Supabase with automatic severity classification
   */
  async logError(context, error, metadata = {}) {
    try {
      const severity = this.classifySeverity(error, context);

      const { data, error: dbError } = await supabase
        .from('error_log')
        .insert({
          context,
          error_message: error.message || error.toString(),
          error_stack: error.stack,
          contact_id: metadata.contactId,
          business_id: metadata.businessId,
          severity,
          retry_count: metadata.retryCount || 0,
          metadata: {
            ...metadata,
            timestamp: new Date().toISOString(),
            userAgent: metadata.userAgent,
            requestId: metadata.requestId
          }
        })
        .select();

      if (dbError) {
        console.error('[ErrorTracker] Failed to log error:', dbError);
        return null;
      }

      // Notify admin if critical
      if (severity === 'CRITICAL') {
        await this.notifyAdmin(error, context, metadata);
      }

      console.log(`[ErrorTracker] Logged ${severity} error in ${context}`);
      return data[0];

    } catch (trackingError) {
      // Fallback: log to console if Supabase fails
      console.error('[ErrorTracker] Error tracking failed:', trackingError);
      console.error('Original error:', error);
      return null;
    }
  }

  /**
   * Classify error severity based on error type and context
   */
  classifySeverity(error, context) {
    const errorMessage = error.message?.toLowerCase() || '';

    // CRITICAL: System-level failures
    if (errorMessage.includes('supabase_key') ||
        errorMessage.includes('claude_api_key') ||
        errorMessage.includes('database connection')) {
      return 'CRITICAL';
    }

    // HIGH: API failures that affect functionality
    if (errorMessage.includes('claude api') ||
        errorMessage.includes('anthropic') ||
        errorMessage.includes('rate limit') ||
        errorMessage.includes('quota exceeded') ||
        error.status === 429 || error.status === 500) {
      return 'HIGH';
    }

    // MEDIUM: Network/temporary issues
    if (errorMessage.includes('network') ||
        errorMessage.includes('timeout') ||
        errorMessage.includes('econnrefused') ||
        error.status === 503 || error.status === 504) {
      return 'MEDIUM';
    }

    // LOW: Input validation, expected errors
    if (errorMessage.includes('validation') ||
        errorMessage.includes('invalid input') ||
        error.status === 400 || error.status === 404) {
      return 'LOW';
    }

    // Default to MEDIUM for unknown errors
    return 'MEDIUM';
  }

  /**
   * Send notification for critical errors
   */
  async notifyAdmin(error, context, metadata) {
    try {
      // Option 1: Slack webhook
      if (process.env.SLACK_WEBHOOK_URL) {
        await fetch(process.env.SLACK_WEBHOOK_URL, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            text: `🚨 *CRITICAL ERROR* in Claude Agent Memory`,
            blocks: [
              {
                type: 'header',
                text: {
                  type: 'plain_text',
                  text: '🚨 Critical System Error'
                }
              },
              {
                type: 'section',
                fields: [
                  { type: 'mrkdwn', text: `*Context:*\n${context}` },
                  { type: 'mrkdwn', text: `*Time:*\n${new Date().toLocaleString()}` }
                ]
              },
              {
                type: 'section',
                text: {
                  type: 'mrkdwn',
                  text: `*Error:*\n\`\`\`${error.message}\`\`\``
                }
              },
              {
                type: 'section',
                fields: [
                  { type: 'mrkdwn', text: `*Contact ID:*\n${metadata.contactId || 'N/A'}` },
                  { type: 'mrkdwn', text: `*Business ID:*\n${metadata.businessId || 'N/A'}` }
                ]
              }
            ]
          })
        });
      }

      // Option 2: Email (if configured)
      if (process.env.ADMIN_EMAIL && process.env.SENDGRID_API_KEY) {
        // TODO: Implement email notification via SendGrid
      }

      console.log('[ErrorTracker] Admin notified of critical error');

    } catch (notifyError) {
      console.error('[ErrorTracker] Failed to notify admin:', notifyError);
    }
  }

  /**
   * Mark error as resolved
   */
  async resolveError(errorId) {
    const { data, error } = await supabase
      .from('error_log')
      .update({
        resolved: true,
        resolved_at: new Date().toISOString()
      })
      .eq('id', errorId)
      .select();

    if (error) {
      console.error('[ErrorTracker] Failed to resolve error:', error);
      return false;
    }

    return true;
  }

  /**
   * Get recent errors
   */
  async getRecentErrors(options = {}) {
    const {
      limit = 50,
      severity = null,
      context = null,
      resolved = false
    } = options;

    let query = supabase
      .from('error_log')
      .select('*')
      .eq('resolved', resolved)
      .order('timestamp', { ascending: false });

    if (severity) query = query.eq('severity', severity);
    if (context) query = query.eq('context', context);

    query = query.limit(limit);

    const { data, error } = await query;

    if (error) {
      console.error('[ErrorTracker] Failed to fetch errors:', error);
      return [];
    }

    return data;
  }

  /**
   * Get error statistics
   */
  async getErrorStats(days = 7) {
    try {
      const { data, error } = await supabase.rpc('get_error_stats', { days });

      if (error) throw error;

      return data;
    } catch (error) {
      console.error('[ErrorTracker] Failed to get error stats:', error);
      return {
        total_errors: 0,
        by_severity: {},
        by_context: {},
        unresolved_count: 0
      };
    }
  }
}

/**
 * Retry helper with exponential backoff
 */
export async function withRetry(fn, options = {}) {
  const {
    maxRetries = 3,
    initialDelayMs = 1000,
    backoffMultiplier = 2,
    context = 'unknown',
    metadata = {}
  } = options;

  let lastError;

  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      const result = await fn();

      // Success! Log if we had retries
      if (attempt > 0) {
        console.log(`[Retry] Success after ${attempt} retries in ${context}`);
      }

      return result;

    } catch (error) {
      lastError = error;

      // Last attempt failed
      if (attempt === maxRetries) {
        console.error(`[Retry] All ${maxRetries} retries failed in ${context}`);

        // Log to error tracker
        await errorTracker.logError(context, error, {
          ...metadata,
          retryCount: attempt,
          finalAttempt: true
        });

        throw error;
      }

      // Calculate delay with exponential backoff
      const delayMs = initialDelayMs * Math.pow(backoffMultiplier, attempt);

      console.log(`[Retry] Attempt ${attempt + 1}/${maxRetries} failed in ${context}, retrying in ${delayMs}ms`);

      // Log retry attempt
      await errorTracker.logError(context, error, {
        ...metadata,
        retryCount: attempt,
        retrying: true,
        nextRetryIn: delayMs
      });

      // Wait before retrying
      await new Promise(resolve => setTimeout(resolve, delayMs));
    }
  }

  throw lastError; // Should never reach here, but TypeScript needs it
}

// Singleton instance
const errorTracker = new ErrorTracker();

export default errorTracker;
