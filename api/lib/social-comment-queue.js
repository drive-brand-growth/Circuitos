/**
 * SOCIAL COMMENT QUEUE MANAGER
 *
 * Purpose: Manage incoming social comments with priority routing and rate limiting
 *
 * Features:
 * 1. Queue management (add, process, prioritize)
 * 2. Priority routing (HOT leads first, then WARM, then COOL)
 * 3. Rate limiting (respect platform API limits)
 * 4. Retry logic (failed responses)
 * 5. Duplicate detection (don't respond twice)
 * 6. Batch processing (catch up on backlog)
 */

import { createClient } from '@supabase/supabase-js';

const supabase = createClient(
  process.env.SUPABASE_URL,
  process.env.SUPABASE_KEY
);

// Priority levels
export const PRIORITY = {
  CRITICAL: 1,    // Viral negative comment, crisis
  HIGH: 2,        // Hot lead (75+), important customer
  MEDIUM: 3,      // Warm lead, genuine question
  LOW: 4,         // Cool lead, engagement
  MINIMAL: 5      // Cold lead, spam
};

// Processing status
export const STATUS = {
  PENDING: 'pending',
  PROCESSING: 'processing',
  RESPONDED: 'responded',
  ESCALATED: 'escalated',
  FAILED: 'failed',
  SKIPPED: 'skipped'
};

/**
 * Add comment to queue
 *
 * @param {Object} commentData
 * @returns {Promise<Object>} Queue entry
 */
export async function addToQueue(commentData) {
  const {
    platform,
    comment_id,
    comment_text,
    commenter,
    post_id,
    post_content,
    received_at
  } = commentData;

  // Check for duplicates
  const { data: existing } = await supabase
    .from('social_comment_queue')
    .select('*')
    .eq('comment_id', comment_id)
    .single();

  if (existing) {
    console.log(`Comment ${comment_id} already in queue`);
    return existing;
  }

  // Determine priority (rough estimation, will be refined by Social Response Agent)
  let priority = PRIORITY.MEDIUM;

  // Keywords that indicate high priority
  const urgentKeywords = ['refund', 'cancel', 'terrible', 'scam', 'lawsuit', 'complaint'];
  const leadKeywords = ['price', 'pricing', 'cost', 'buy', 'purchase', 'interested', 'how to get started'];

  const lowerComment = comment_text.toLowerCase();

  if (urgentKeywords.some(keyword => lowerComment.includes(keyword))) {
    priority = PRIORITY.CRITICAL;
  } else if (leadKeywords.some(keyword => lowerComment.includes(keyword))) {
    priority = PRIORITY.HIGH;
  } else if (comment_text.length < 10 || /^[👍❤️🔥💯🙌]+$/.test(comment_text)) {
    // Short comment or emoji-only
    priority = PRIORITY.LOW;
  }

  // Insert into queue
  const { data, error } = await supabase
    .from('social_comment_queue')
    .insert({
      platform,
      comment_id,
      comment_text,
      commenter_name: commenter.name,
      commenter_profile: commenter,
      post_id,
      post_content,
      priority,
      status: STATUS.PENDING,
      received_at: received_at || new Date().toISOString(),
      retry_count: 0
    })
    .select()
    .single();

  if (error) {
    console.error('Error adding to queue:', error);
    throw error;
  }

  console.log(`Added comment ${comment_id} to queue with priority ${priority}`);
  return data;
}

/**
 * Get next comment to process (highest priority first)
 *
 * @returns {Promise<Object|null>} Next comment or null if queue empty
 */
export async function getNextComment() {
  const { data, error } = await supabase
    .from('social_comment_queue')
    .select('*')
    .eq('status', STATUS.PENDING)
    .order('priority', { ascending: true })  // Lower number = higher priority
    .order('received_at', { ascending: true }) // Older first within same priority
    .limit(1)
    .single();

  if (error && error.code !== 'PGRST116') { // PGRST116 = no rows found
    console.error('Error getting next comment:', error);
    throw error;
  }

  return data || null;
}

/**
 * Get batch of comments to process
 *
 * @param {number} limit - Max number of comments to retrieve
 * @returns {Promise<Array>} Array of comments
 */
export async function getBatchComments(limit = 10) {
  const { data, error } = await supabase
    .from('social_comment_queue')
    .select('*')
    .eq('status', STATUS.PENDING)
    .order('priority', { ascending: true })
    .order('received_at', { ascending: true })
    .limit(limit);

  if (error) {
    console.error('Error getting batch comments:', error);
    throw error;
  }

  return data || [];
}

/**
 * Update comment status
 *
 * @param {string} commentId
 * @param {string} status
 * @param {Object} metadata - Additional data (response, error, etc.)
 * @returns {Promise<Object>} Updated comment
 */
export async function updateCommentStatus(commentId, status, metadata = {}) {
  const updates = {
    status,
    updated_at: new Date().toISOString(),
    ...metadata
  };

  if (status === STATUS.RESPONDED) {
    updates.responded_at = new Date().toISOString();
  } else if (status === STATUS.FAILED) {
    updates.retry_count = (metadata.retry_count || 0) + 1;
    updates.last_error = metadata.error;
  }

  const { data, error } = await supabase
    .from('social_comment_queue')
    .update(updates)
    .eq('comment_id', commentId)
    .select()
    .single();

  if (error) {
    console.error('Error updating comment status:', error);
    throw error;
  }

  return data;
}

/**
 * Mark comment as processing (to prevent duplicate processing)
 *
 * @param {string} commentId
 * @returns {Promise<Object>}
 */
export async function markAsProcessing(commentId) {
  return updateCommentStatus(commentId, STATUS.PROCESSING, {
    processing_started_at: new Date().toISOString()
  });
}

/**
 * Retry failed comments
 *
 * @param {number} maxRetries - Max retry attempts
 * @returns {Promise<Array>} Comments to retry
 */
export async function getFailedComments(maxRetries = 3) {
  const { data, error } = await supabase
    .from('social_comment_queue')
    .select('*')
    .eq('status', STATUS.FAILED)
    .lt('retry_count', maxRetries)
    .order('retry_count', { ascending: true })
    .limit(10);

  if (error) {
    console.error('Error getting failed comments:', error);
    throw error;
  }

  return data || [];
}

/**
 * Get queue statistics
 *
 * @returns {Promise<Object>} Queue stats
 */
export async function getQueueStats() {
  const { data: all } = await supabase
    .from('social_comment_queue')
    .select('status, priority, platform');

  if (!all) return null;

  const stats = {
    total: all.length,
    by_status: {
      pending: all.filter(c => c.status === STATUS.PENDING).length,
      processing: all.filter(c => c.status === STATUS.PROCESSING).length,
      responded: all.filter(c => c.status === STATUS.RESPONDED).length,
      escalated: all.filter(c => c.status === STATUS.ESCALATED).length,
      failed: all.filter(c => c.status === STATUS.FAILED).length,
      skipped: all.filter(c => c.status === STATUS.SKIPPED).length
    },
    by_priority: {
      critical: all.filter(c => c.priority === PRIORITY.CRITICAL).length,
      high: all.filter(c => c.priority === PRIORITY.HIGH).length,
      medium: all.filter(c => c.priority === PRIORITY.MEDIUM).length,
      low: all.filter(c => c.priority === PRIORITY.LOW).length,
      minimal: all.filter(c => c.priority === PRIORITY.MINIMAL).length
    },
    by_platform: {}
  };

  // Count by platform
  all.forEach(c => {
    stats.by_platform[c.platform] = (stats.by_platform[c.platform] || 0) + 1;
  });

  return stats;
}

/**
 * Clean up old processed comments (keep for analytics, but archive)
 *
 * @param {number} daysToKeep - Days to keep in active queue
 * @returns {Promise<number>} Number of archived comments
 */
export async function archiveOldComments(daysToKeep = 30) {
  const cutoffDate = new Date();
  cutoffDate.setDate(cutoffDate.getDate() - daysToKeep);

  const { data } = await supabase
    .from('social_comment_queue')
    .update({ archived: true })
    .in('status', [STATUS.RESPONDED, STATUS.SKIPPED])
    .lt('responded_at', cutoffDate.toISOString())
    .select();

  return data?.length || 0;
}

/**
 * Process queue with rate limiting
 *
 * @param {Function} processFunction - Function to process each comment
 * @param {Object} options
 *   - batchSize: Number of comments to process at once
 *   - delayMs: Delay between batches (rate limiting)
 * @returns {Promise<Object>} Processing results
 */
export async function processQueue(processFunction, options = {}) {
  const {
    batchSize = 5,
    delayMs = 2000 // 2 seconds between batches
  } = options;

  const results = {
    processed: 0,
    succeeded: 0,
    failed: 0,
    escalated: 0,
    errors: []
  };

  let hasMore = true;

  while (hasMore) {
    const batch = await getBatchComments(batchSize);

    if (batch.length === 0) {
      hasMore = false;
      break;
    }

    for (const comment of batch) {
      try {
        // Mark as processing
        await markAsProcessing(comment.comment_id);

        // Process comment
        const result = await processFunction(comment);

        // Update status based on result
        if (result.routing_decision === 'ESCALATION') {
          await updateCommentStatus(comment.comment_id, STATUS.ESCALATED, {
            response_data: result
          });
          results.escalated++;
        } else if (result.routing_decision === 'NO_RESPONSE') {
          await updateCommentStatus(comment.comment_id, STATUS.SKIPPED, {
            response_data: result
          });
        } else {
          await updateCommentStatus(comment.comment_id, STATUS.RESPONDED, {
            response_data: result
          });
          results.succeeded++;
        }

        results.processed++;

      } catch (error) {
        console.error(`Error processing comment ${comment.comment_id}:`, error);

        await updateCommentStatus(comment.comment_id, STATUS.FAILED, {
          error: error.message,
          retry_count: comment.retry_count
        });

        results.failed++;
        results.errors.push({
          comment_id: comment.comment_id,
          error: error.message
        });
      }

      // Small delay between individual comments
      await new Promise(resolve => setTimeout(resolve, 500));
    }

    // Delay between batches
    if (hasMore) {
      await new Promise(resolve => setTimeout(resolve, delayMs));
    }
  }

  return results;
}

/**
 * Real-time queue monitoring (get pending count)
 *
 * @returns {Promise<number>} Pending comment count
 */
export async function getPendingCount() {
  const { count, error } = await supabase
    .from('social_comment_queue')
    .select('*', { count: 'exact', head: true })
    .eq('status', STATUS.PENDING);

  if (error) {
    console.error('Error getting pending count:', error);
    return 0;
  }

  return count || 0;
}

/**
 * Get comments by priority level
 *
 * @param {number} priorityLevel
 * @returns {Promise<Array>}
 */
export async function getCommentsByPriority(priorityLevel) {
  const { data, error } = await supabase
    .from('social_comment_queue')
    .select('*')
    .eq('priority', priorityLevel)
    .eq('status', STATUS.PENDING)
    .order('received_at', { ascending: true });

  if (error) {
    console.error('Error getting comments by priority:', error);
    throw error;
  }

  return data || [];
}

export default {
  PRIORITY,
  STATUS,
  addToQueue,
  getNextComment,
  getBatchComments,
  updateCommentStatus,
  markAsProcessing,
  getFailedComments,
  getQueueStats,
  archiveOldComments,
  processQueue,
  getPendingCount,
  getCommentsByPriority
};
