# Claude Agent Memory Architecture
## ADK-Level Capabilities Without the Framework

**Version:** 2.0.0
**Purpose:** Add conversational memory + multi-agent collaboration to existing Claude integration
**Cost:** $0 additional infrastructure (uses existing GHL + Supabase)

---

## 🧠 THE PROBLEM WITH CURRENT SETUP

### Current (One-Shot Calls):
```javascript
// Every call is independent - NO MEMORY
const response = await anthropic.messages.create({
  model: 'claude-sonnet-4-5-20250929',
  messages: [{
    role: 'user',
    content: 'Score this lead using BANT'
  }]
});
```

**Limitations:**
- ❌ Agent forgets everything after each call
- ❌ Can't have multi-turn conversations
- ❌ No context from previous interactions
- ❌ Agents can't collaborate (no shared memory)
- ❌ Can't learn from past decisions

---

## ✅ ENHANCED ARCHITECTURE WITH MEMORY

### New Approach (Multi-Turn with Context):
```javascript
// Agent remembers conversation history
const conversationHistory = await getConversationHistory(contactId);

const response = await anthropic.messages.create({
  model: 'claude-sonnet-4-5-20250929',
  messages: conversationHistory, // All past interactions
  system: DMN_PROTOCOL_PROMPT
});

// Save new interaction to memory
await saveToConversation(contactId, response);
```

**Capabilities:**
- ✅ Agents remember all past interactions
- ✅ Multi-turn reasoning ("Let me analyze... now let me generate copy...")
- ✅ Shared context between agents (Lead Scorer → Copywriter)
- ✅ Self-improving via feedback loop
- ✅ ADK-level intelligence without framework

---

## 🏗️ MEMORY STORAGE LAYERS

### Layer 1: SHORT-TERM MEMORY (In-Memory Cache)
**Purpose:** Fast access during active conversation
**Storage:** Node.js Map() or Redis (optional)
**Lifetime:** 30 minutes
**Cost:** FREE

```javascript
const activeConversations = new Map();

// Store conversation in memory for quick access
activeConversations.set(contactId, {
  messages: [...],
  lastActivity: Date.now(),
  agentState: 'scoring_lead'
});
```

### Layer 2: MEDIUM-TERM MEMORY (GHL Custom Fields)
**Purpose:** Store key decisions and scores
**Storage:** GoHighLevel custom fields
**Lifetime:** Permanent
**Cost:** FREE (you already have GHL)

**Custom Fields to Add:**
```json
{
  "conversation_summary": "Scored lead 78/100, sent cold email variant A",
  "agent_decisions": ["BANT=HIGH", "Timing=URGENT", "Channel=EMAIL"],
  "last_agent_action": "Lead Scorer → Copywriter → Email Sent",
  "conversation_turn_count": 3,
  "total_tokens_used": 4582
}
```

### Layer 3: LONG-TERM MEMORY (Supabase PostgreSQL)
**Purpose:** Full conversation history for ML training
**Storage:** Supabase (FREE tier: 500MB)
**Lifetime:** Permanent
**Cost:** FREE

**Database Schema:**
```sql
CREATE TABLE conversation_history (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  contact_id VARCHAR(255) NOT NULL,
  business_id VARCHAR(255) NOT NULL,
  agent_name VARCHAR(100),
  role VARCHAR(20), -- 'user' or 'assistant'
  content TEXT,
  metadata JSONB,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_contact_conversations
  ON conversation_history(contact_id, created_at DESC);

CREATE TABLE agent_feedback (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  conversation_id UUID REFERENCES conversation_history(id),
  predicted_outcome VARCHAR(50), -- 'HIGH_INTENT', 'WILL_CONVERT'
  actual_outcome VARCHAR(50), -- 'CONVERTED', 'NO_RESPONSE'
  error_delta NUMERIC, -- How wrong was the prediction?
  learned_patterns JSONB, -- What did we learn?
  created_at TIMESTAMP DEFAULT NOW()
);
```

---

## 🤖 MULTI-AGENT COLLABORATION WITH SHARED MEMORY

### How Agents Share Context:

```javascript
// Lead Scorer Agent analyzes lead
const scoringResult = await callAgent({
  agentName: 'Lead Scorer',
  contactId: 'abc123',
  task: 'score_lead',
  data: contactData
});

// Scoring result is saved to conversation history
await saveToConversation(contactId, {
  agent: 'Lead Scorer',
  result: scoringResult
});

// Copywriter Agent reads Lead Scorer's decision
const copyResult = await callAgent({
  agentName: 'Copywriter',
  contactId: 'abc123', // Same contact ID
  task: 'generate_copy',
  context: 'READ conversation history first' // Agent sees Lead Scorer's work
});

// Copywriter now knows:
// - Lead score: 78/100
// - BANT breakdown: Budget=HIGH, Authority=DECISION_MAKER
// - Awareness level: 3 (Solution Aware)
// - Pain points: Manual lead qualification eating 15hrs/week
```

**Result:** Agents collaborate like a real team, not isolated workers.

---

## 💾 IMPLEMENTATION: MEMORY MANAGER

### Core Memory Functions:

```javascript
// api/lib/memory-manager.js

import { createClient } from '@supabase/supabase-js';

const supabase = createClient(
  process.env.SUPABASE_URL,
  process.env.SUPABASE_KEY
);

// In-memory cache for active conversations
const activeConversations = new Map();
const CACHE_TTL = 30 * 60 * 1000; // 30 minutes

class MemoryManager {

  /**
   * Get full conversation history for a contact
   */
  async getConversationHistory(contactId, maxTurns = 10) {
    // 1. Check in-memory cache first (fastest)
    const cached = activeConversations.get(contactId);
    if (cached && Date.now() - cached.lastActivity < CACHE_TTL) {
      return cached.messages;
    }

    // 2. Fetch from Supabase (persistent storage)
    const { data, error } = await supabase
      .from('conversation_history')
      .select('role, content, agent_name, metadata, created_at')
      .eq('contact_id', contactId)
      .order('created_at', { ascending: true })
      .limit(maxTurns * 2); // Each turn = user + assistant

    if (error) {
      console.error('Error fetching conversation:', error);
      return [];
    }

    // 3. Format for Claude API
    const messages = data.map(msg => ({
      role: msg.role,
      content: msg.content
    }));

    // 4. Cache in memory
    activeConversations.set(contactId, {
      messages,
      lastActivity: Date.now()
    });

    return messages;
  }

  /**
   * Save a new message to conversation history
   */
  async saveMessage(contactId, businessId, agentName, role, content, metadata = {}) {
    // 1. Save to Supabase (persistent)
    const { data, error } = await supabase
      .from('conversation_history')
      .insert({
        contact_id: contactId,
        business_id: businessId,
        agent_name: agentName,
        role,
        content,
        metadata
      })
      .select();

    if (error) {
      console.error('Error saving message:', error);
      return null;
    }

    // 2. Update in-memory cache
    const cached = activeConversations.get(contactId);
    if (cached) {
      cached.messages.push({ role, content });
      cached.lastActivity = Date.now();
    } else {
      activeConversations.set(contactId, {
        messages: [{ role, content }],
        lastActivity: Date.now()
      });
    }

    return data[0];
  }

  /**
   * Get conversation summary (for GHL custom fields)
   */
  async getSummary(contactId) {
    const messages = await this.getConversationHistory(contactId);

    return {
      turnCount: Math.floor(messages.length / 2),
      lastAgent: messages[messages.length - 1]?.metadata?.agent_name,
      totalTokens: messages.reduce((sum, m) => sum + (m.metadata?.tokens || 0), 0)
    };
  }

  /**
   * Record agent feedback for ML training
   */
  async recordFeedback(conversationId, predicted, actual, learnedPatterns) {
    const errorDelta = this.calculateError(predicted, actual);

    await supabase
      .from('agent_feedback')
      .insert({
        conversation_id: conversationId,
        predicted_outcome: predicted,
        actual_outcome: actual,
        error_delta: errorDelta,
        learned_patterns: learnedPatterns
      });

    // Trigger ML model update if error is significant
    if (errorDelta > 0.3) {
      await this.triggerModelRetraining(conversationId);
    }
  }

  calculateError(predicted, actual) {
    // Simple example: HIGH_INTENT vs NO_RESPONSE = large error
    const scoreMap = {
      'CONVERTED': 1.0,
      'HIGH_ENGAGEMENT': 0.7,
      'SOME_RESPONSE': 0.4,
      'NO_RESPONSE': 0.0
    };

    return Math.abs(
      (scoreMap[predicted] || 0) - (scoreMap[actual] || 0)
    );
  }

  async triggerModelRetraining(conversationId) {
    // Queue for ML retraining (implement based on your ML pipeline)
    console.log(`[ML] Flagged conversation ${conversationId} for retraining`);
  }

  /**
   * Clean up old conversations from cache
   */
  cleanupCache() {
    const now = Date.now();
    for (const [contactId, data] of activeConversations.entries()) {
      if (now - data.lastActivity > CACHE_TTL) {
        activeConversations.delete(contactId);
      }
    }
  }
}

// Run cleanup every 10 minutes
setInterval(() => new MemoryManager().cleanupCache(), 10 * 60 * 1000);

export default new MemoryManager();
```

---

## 🎯 USAGE PATTERNS

### Pattern 1: Multi-Turn Agent Conversation

```javascript
// Turn 1: Lead Scorer analyzes
const scoringMessages = [
  { role: 'user', content: 'Analyze this lead: John Doe, Brooklyn, visited GMB 2hrs ago' }
];

const scoringResult = await anthropic.messages.create({
  model: 'claude-sonnet-4-5-20250929',
  messages: scoringMessages
});

await memoryManager.saveMessage(
  contactId,
  businessId,
  'Lead Scorer',
  'assistant',
  scoringResult.content[0].text
);

// Turn 2: Copywriter uses Lead Scorer's context
const conversationHistory = await memoryManager.getConversationHistory(contactId);

conversationHistory.push({
  role: 'user',
  content: 'Now generate cold email copy for this lead using the scoring analysis above'
});

const copyResult = await anthropic.messages.create({
  model: 'claude-sonnet-4-5-20250929',
  messages: conversationHistory // Copywriter sees Lead Scorer's work!
});
```

### Pattern 2: Agent Reads Past Decisions

```javascript
// Get conversation summary before acting
const summary = await memoryManager.getSummary(contactId);

if (summary.turnCount > 5) {
  // This lead has been contacted multiple times
  // Adjust strategy: Don't be too aggressive
  prompt += '\nNOTE: Lead has seen 5+ messages. Be subtle, not pushy.';
}
```

### Pattern 3: ML Feedback Loop

```javascript
// After outreach, record what actually happened
setTimeout(async () => {
  const didConvert = await checkConversion(contactId);

  await memoryManager.recordFeedback(
    conversationId,
    predicted: 'HIGH_INTENT', // What Lead Scorer predicted
    actual: didConvert ? 'CONVERTED' : 'NO_RESPONSE',
    learnedPatterns: {
      signals: ['GMB_CALL', 'PROXIMITY_<1MI'],
      worked: didConvert,
      industry: 'fitness'
    }
  );
}, 24 * 60 * 60 * 1000); // Check after 24 hours
```

---

## 📊 BENEFITS vs GOOGLE ADK

| Feature | **Your Enhanced Setup** | **Google ADK** |
|---------|------------------------|----------------|
| Conversational Memory | ✅ Full history in Supabase | ✅ Built-in state mgmt |
| Multi-Agent Collaboration | ✅ Shared conversation context | ✅ A2A protocol |
| ML Feedback Loop | ✅ Custom (optimized for Virtual LPR) | ⚠️ Framework-dependent |
| Cost | ✅ $0 infrastructure (Supabase free) | ⚠️ Framework overhead |
| Control | ✅ Full control over memory logic | ❌ Framework abstractions |
| Vendor Lock-in | ✅ None (standard PostgreSQL) | ❌ Google ecosystem |
| Production-Ready | ✅ Build on existing system | ❌ Requires migration |

---

## 🚀 DEPLOYMENT CHECKLIST

### Phase 1: Setup Storage (15 min)
- [ ] Create Supabase account (free)
- [ ] Run SQL schema (create tables)
- [ ] Get Supabase URL + API key
- [ ] Add to Vercel env vars

### Phase 2: Deploy Memory Manager (30 min)
- [ ] Create `api/lib/memory-manager.js`
- [ ] Install Supabase client: `npm install @supabase/supabase-js`
- [ ] Test memory functions
- [ ] Deploy to Vercel

### Phase 3: Update Agents (1 hour)
- [ ] Enhance `score-lead` endpoint with memory
- [ ] Enhance `generate-copy` endpoint with memory
- [ ] Add `respond-to-review` endpoint with memory
- [ ] Test multi-agent collaboration

### Phase 4: Add ML Feedback (1 hour)
- [ ] Create feedback recording endpoint
- [ ] Hook into GHL conversion tracking
- [ ] Build basic retraining trigger
- [ ] Monitor feedback loop

---

## 💡 KEY INSIGHT

**You don't need Google ADK because:**

1. **Claude's native API supports multi-turn conversations** - just send message history
2. **Supabase gives you persistent memory** - same as ADK's state management
3. **Your DMN Protocol is more optimized** - tailored for Virtual LPR, not generic
4. **You maintain full control** - no framework abstractions or breaking changes

**This architecture gives you:**
- ADK-level agent intelligence
- Multi-agent collaboration
- Conversational memory
- Self-improving ML loop
- $0 additional infrastructure cost
- No vendor lock-in

---

**Next:** Implement the enhanced Claude API integration with memory 🚀
