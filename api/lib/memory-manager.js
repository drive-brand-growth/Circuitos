/**
 * Circuit OS - Claude Agent Memory Manager
 *
 * Provides ADK-level conversational memory without framework overhead
 * - Multi-turn conversations
 * - Agent collaboration via shared context
 * - ML feedback loop integration
 * - Zero-cost storage (Supabase free tier)
 */

import { createClient } from '@supabase/supabase-js';

const supabase = createClient(
  process.env.SUPABASE_URL,
  process.env.SUPABASE_KEY
);

// In-memory cache for active conversations (30 min TTL)
const activeConversations = new Map();
const CACHE_TTL = 30 * 60 * 1000; // 30 minutes

class MemoryManager {

  /**
   * Get full conversation history for a contact
   * Returns messages in Claude API format
   */
  async getConversationHistory(contactId, maxTurns = 20) {
    try {
      // 1. Check in-memory cache first (fastest)
      const cached = activeConversations.get(contactId);
      if (cached && Date.now() - cached.lastActivity < CACHE_TTL) {
        console.log(`[Memory] Cache HIT for ${contactId}`);
        return cached.messages;
      }

      console.log(`[Memory] Cache MISS for ${contactId}, fetching from DB`);

      // 2. Fetch from Supabase (persistent storage)
      const { data, error } = await supabase
        .from('conversation_history')
        .select('role, content, agent_name, metadata, created_at')
        .eq('contact_id', contactId)
        .order('created_at', { ascending: true })
        .limit(maxTurns * 2); // Each turn = user + assistant

      if (error) {
        console.error('[Memory] Error fetching conversation:', error);
        return [];
      }

      // 3. Format for Claude API
      const messages = data.map(msg => ({
        role: msg.role,
        content: msg.content
      }));

      // 4. Cache in memory for fast access
      activeConversations.set(contactId, {
        messages,
        lastActivity: Date.now(),
        metadata: {
          turnCount: Math.floor(messages.length / 2),
          lastAgent: data[data.length - 1]?.agent_name
        }
      });

      console.log(`[Memory] Loaded ${messages.length} messages for ${contactId}`);
      return messages;

    } catch (error) {
      console.error('[Memory] Error in getConversationHistory:', error);
      return [];
    }
  }

  /**
   * Save a new message to conversation history
   */
  async saveMessage(contactId, businessId, agentName, role, content, metadata = {}) {
    try {
      // 1. Save to Supabase (persistent)
      const { data, error } = await supabase
        .from('conversation_history')
        .insert({
          contact_id: contactId,
          business_id: businessId,
          agent_name: agentName,
          role,
          content,
          metadata: {
            ...metadata,
            timestamp: new Date().toISOString(),
            tokens: this.estimateTokens(content)
          }
        })
        .select();

      if (error) {
        console.error('[Memory] Error saving message:', error);
        return null;
      }

      // 2. Update in-memory cache
      const cached = activeConversations.get(contactId);
      if (cached) {
        cached.messages.push({ role, content });
        cached.lastActivity = Date.now();
        cached.metadata.turnCount = Math.floor(cached.messages.length / 2);
        cached.metadata.lastAgent = agentName;
      } else {
        activeConversations.set(contactId, {
          messages: [{ role, content }],
          lastActivity: Date.now(),
          metadata: { turnCount: 1, lastAgent: agentName }
        });
      }

      console.log(`[Memory] Saved message from ${agentName} for ${contactId}`);
      return data[0];

    } catch (error) {
      console.error('[Memory] Error in saveMessage:', error);
      return null;
    }
  }

  /**
   * Get conversation summary (for GHL custom fields)
   */
  async getSummary(contactId) {
    try {
      const cached = activeConversations.get(contactId);
      if (cached) {
        return {
          turnCount: cached.metadata.turnCount,
          lastAgent: cached.metadata.lastAgent,
          lastActivity: new Date(cached.lastActivity).toISOString(),
          cached: true
        };
      }

      // Fetch from database if not in cache
      const { data, error } = await supabase
        .from('conversation_history')
        .select('agent_name, created_at, metadata')
        .eq('contact_id', contactId)
        .order('created_at', { ascending: false })
        .limit(1);

      if (error || !data || data.length === 0) {
        return { turnCount: 0, lastAgent: null, lastActivity: null };
      }

      const { count } = await supabase
        .from('conversation_history')
        .select('*', { count: 'exact', head: true })
        .eq('contact_id', contactId);

      return {
        turnCount: Math.floor((count || 0) / 2),
        lastAgent: data[0].agent_name,
        lastActivity: data[0].created_at,
        cached: false
      };

    } catch (error) {
      console.error('[Memory] Error in getSummary:', error);
      return { turnCount: 0, lastAgent: null, lastActivity: null };
    }
  }

  /**
   * Record agent feedback for ML training
   */
  async recordFeedback(contactId, conversationId, predicted, actual, learnedPatterns = {}) {
    try {
      const errorDelta = this.calculateError(predicted, actual);

      const { data, error } = await supabase
        .from('agent_feedback')
        .insert({
          conversation_id: conversationId,
          contact_id: contactId,
          predicted_outcome: predicted,
          actual_outcome: actual,
          error_delta: errorDelta,
          learned_patterns: learnedPatterns
        })
        .select();

      if (error) {
        console.error('[Memory] Error recording feedback:', error);
        return null;
      }

      console.log(`[ML] Recorded feedback: ${predicted} → ${actual} (error: ${errorDelta.toFixed(2)})`);

      // Trigger ML model update if error is significant
      if (errorDelta > 0.3) {
        await this.triggerModelRetraining(conversationId, errorDelta);
      }

      return data[0];

    } catch (error) {
      console.error('[Memory] Error in recordFeedback:', error);
      return null;
    }
  }

  /**
   * Calculate prediction error
   */
  calculateError(predicted, actual) {
    const scoreMap = {
      'CONVERTED': 1.0,
      'HIGH_ENGAGEMENT': 0.7,
      'SOME_RESPONSE': 0.4,
      'NO_RESPONSE': 0.0,
      'UNSUBSCRIBED': -0.2
    };

    const predictedScore = scoreMap[predicted] || 0.5;
    const actualScore = scoreMap[actual] || 0;

    return Math.abs(predictedScore - actualScore);
  }

  /**
   * Trigger ML model retraining
   */
  async triggerModelRetraining(conversationId, errorDelta) {
    try {
      // Queue for ML retraining (implement based on your ML pipeline)
      await supabase
        .from('ml_retraining_queue')
        .insert({
          conversation_id: conversationId,
          error_delta: errorDelta,
          priority: errorDelta > 0.5 ? 'HIGH' : 'MEDIUM',
          status: 'PENDING'
        });

      console.log(`[ML] Flagged conversation ${conversationId} for retraining (error: ${errorDelta.toFixed(2)})`);

    } catch (error) {
      console.error('[ML] Error triggering retraining:', error);
    }
  }

  /**
   * Estimate token count (rough approximation)
   */
  estimateTokens(text) {
    // Rough estimate: ~4 characters per token
    return Math.ceil(text.length / 4);
  }

  /**
   * Clean up old conversations from cache
   */
  cleanupCache() {
    const now = Date.now();
    let cleaned = 0;

    for (const [contactId, data] of activeConversations.entries()) {
      if (now - data.lastActivity > CACHE_TTL) {
        activeConversations.delete(contactId);
        cleaned++;
      }
    }

    if (cleaned > 0) {
      console.log(`[Memory] Cleaned up ${cleaned} expired conversations from cache`);
    }
  }

  /**
   * Clear all conversation history for a contact (GDPR compliance)
   */
  async clearHistory(contactId) {
    try {
      // Remove from cache
      activeConversations.delete(contactId);

      // Remove from database
      const { error } = await supabase
        .from('conversation_history')
        .delete()
        .eq('contact_id', contactId);

      if (error) {
        console.error('[Memory] Error clearing history:', error);
        return false;
      }

      console.log(`[Memory] Cleared all history for ${contactId}`);
      return true;

    } catch (error) {
      console.error('[Memory] Error in clearHistory:', error);
      return false;
    }
  }

  /**
   * Get agent collaboration context
   * Returns a summary of what other agents have done for this contact
   */
  async getAgentContext(contactId) {
    try {
      const { data, error } = await supabase
        .from('conversation_history')
        .select('agent_name, role, content, created_at, metadata')
        .eq('contact_id', contactId)
        .eq('role', 'assistant')
        .order('created_at', { ascending: false })
        .limit(5);

      if (error || !data) {
        return [];
      }

      return data.map(msg => ({
        agent: msg.agent_name,
        action: this.extractAction(msg.content),
        timestamp: msg.created_at,
        metadata: msg.metadata
      }));

    } catch (error) {
      console.error('[Memory] Error in getAgentContext:', error);
      return [];
    }
  }

  /**
   * Extract key action from agent message
   */
  extractAction(content) {
    // Simple extraction - can be enhanced
    if (content.includes('"total_score"')) return 'SCORED_LEAD';
    if (content.includes('"subject"')) return 'GENERATED_COPY';
    if (content.includes('"response"')) return 'RESPONDED_TO_REVIEW';
    return 'PROCESSED';
  }
}

// Create singleton instance
const memoryManager = new MemoryManager();

// Run cleanup every 10 minutes
if (typeof setInterval !== 'undefined') {
  setInterval(() => memoryManager.cleanupCache(), 10 * 60 * 1000);
}

export default memoryManager;
