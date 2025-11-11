# Circuit OS - Claude Agent Memory API

**Version 2.0** - ADK-Level Intelligence Without the Framework

## 🎯 What This Is

Enhanced Claude API integration with **conversational memory** that gives your agents:

- ✅ **Multi-turn conversations** - Agents remember all past interactions
- ✅ **Agent collaboration** - Shared context between agents (Lead Scorer → Copywriter)
- ✅ **Self-improving ML loop** - Learn from actual outcomes
- ✅ **Zero infrastructure cost** - Supabase + Vercel free tiers
- ✅ **No vendor lock-in** - Direct Claude API, standard PostgreSQL

## 📂 File Structure

```
api/
├── claude-agent-memory.js          # Main API endpoint (deploy to Vercel)
├── lib/
│   └── memory-manager.js           # Memory storage & retrieval
├── examples/
│   └── multi-agent-workflow.js     # Usage examples
├── supabase-schema.sql             # Database schema
├── package.json                    # Dependencies
├── claude-memory-architecture.md   # Architecture documentation
├── DEPLOYMENT-GUIDE.md             # Step-by-step deployment
└── README.md                       # This file
```

## 🚀 Quick Start

### 1. Deploy (30 minutes)
Follow **DEPLOYMENT-GUIDE.md** for complete instructions.

Quick version:
```bash
# Install dependencies
npm install

# Deploy to Vercel
npx vercel --prod

# Add environment variables
npx vercel env add CLAUDE_API_KEY production
npx vercel env add SUPABASE_URL production
npx vercel env add SUPABASE_KEY production
```

### 2. Test
```bash
curl -X POST https://YOUR_VERCEL_URL/api/claude-agent-memory \
  -H "Content-Type: application/json" \
  -d '{
    "action": "score-lead",
    "contactId": "test-123",
    "businessId": "biz-456",
    "useMemory": true,
    "data": {
      "contact": {"first_name": "John", "city": "Brooklyn"},
      "business": {"name": "Test Gym", "category": "Fitness"}
    }
  }'
```

## 📖 Usage

### Available Actions

1. **`score-lead`** - Lead Scorer agent (BANT/MEDDIC/CHAMP + Virtual LPR)
2. **`generate-copy`** - Copywriter agent (Brunson + Schwartz + Hormozi)
3. **`respond-to-review`** - Reputation Guardian agent
4. **`get-summary`** - Get conversation summary for a contact
5. **`record-feedback`** - Record ML feedback (predicted vs actual outcome)

### Multi-Agent Workflow Example

```javascript
// Step 1: Score lead
const scoringResult = await fetch(API_URL, {
  method: 'POST',
  body: JSON.stringify({
    action: 'score-lead',
    contactId: 'contact-123',
    businessId: 'biz-456',
    useMemory: true,
    data: { contact, business }
  })
});

// Step 2: Generate copy (sees Lead Scorer's analysis!)
const copyResult = await fetch(API_URL, {
  method: 'POST',
  body: JSON.stringify({
    action: 'generate-copy',
    contactId: 'contact-123', // SAME contactId
    businessId: 'biz-456',
    useMemory: true,
    data: { contact, channel: 'EMAIL', awareness_level: 'Solution Aware', business }
  })
});

// Copywriter agent now has full context from Lead Scorer!
```

See **examples/multi-agent-workflow.js** for complete examples.

## 💾 Memory Architecture

### 3-Layer Storage

1. **In-Memory Cache** (30 min TTL) - Fast access for active conversations
2. **Supabase PostgreSQL** - Persistent storage, full history
3. **GHL Custom Fields** - Summary data for quick reference

### Database Tables

- `conversation_history` - All agent-contact interactions
- `agent_feedback` - ML feedback loop (predicted vs actual)
- `ml_retraining_queue` - Conversations flagged for model improvement

## 🆚 vs Google ADK

| Feature | **This Setup** | **Google ADK** |
|---------|---------------|----------------|
| Model Quality | Claude Sonnet 4.5 (best) | Model-agnostic |
| Conversational Memory | ✅ Supabase | ✅ Built-in |
| Multi-Agent Collaboration | ✅ Shared context | ✅ A2A protocol |
| Cost | $0 infra + $50-300 API | Same or higher |
| Vendor Lock-in | ✅ None | ❌ Google ecosystem |
| Customization | ✅ Full control | ⚠️ Framework limits |

**Bottom line:** Same or better capabilities, zero lock-in, full control.

## 💰 Cost

- **Vercel:** $0/month (free tier: 100GB bandwidth)
- **Supabase:** $0/month (free tier: 500MB, 50K rows)
- **Claude API:** ~$80-300/month (usage-based, 1000-5000 leads/mo)

**Total:** $80-300/month vs $200-500/month for typical ADK setup

## 📚 Documentation

- **DEPLOYMENT-GUIDE.md** - Step-by-step deployment instructions
- **claude-memory-architecture.md** - Technical architecture deep-dive
- **examples/multi-agent-workflow.js** - Working code examples

## 🔧 Troubleshooting

### Memory not persisting?
- Check Supabase credentials in Vercel env vars
- Verify tables were created (run supabase-schema.sql)
- Use service_role key, not anon key

### High token usage?
- Reduce `maxTurns` in memory-manager.js (default: 20)
- Limit conversation history to recent interactions

### Agents not collaborating?
- Ensure same `contactId` is used across agent calls
- Verify `useMemory: true` in request body

## 🎯 Next Steps

1. **Deploy:** Follow DEPLOYMENT-GUIDE.md
2. **Test:** Run examples/multi-agent-workflow.js
3. **Integrate:** Connect to GHL workflows
4. **Monitor:** Track usage in Anthropic Console
5. **Optimize:** Tune memory retention and agent prompts

---

**Questions?** Review the docs or check code comments.

**© 2025 Circuit OS™**
