# GHL Workflow Designer + Orchestrator - Integration Guide

**Transform natural language → production-ready GHL workflows**

---

## 🎯 What You Built

You now have TWO powerful AI agents:

### 1. **GHL Workflow Designer**
- **Purpose:** World-class prompt engineer for GHL workflows
- **Input:** Natural language description ("Build a workflow for high-intent GMB leads")
- **Output:** Production-ready workflow JSON + setup instructions
- **Frameworks:** Brunson, Hormozi, Schwartz, TCPA compliance

### 2. **Orchestrator**
- **Purpose:** Coordinates multiple agents for complex tasks
- **Input:** High-level request ("Build a complete lead nurture system")
- **Output:** Execution plan + coordinated agent outputs
- **Agents:** Lead Scorer + Copywriter + Workflow Designer + more

---

## 🚀 Quick Start

### Use Workflow Designer

```bash
curl -X POST https://YOUR_VERCEL_URL/api/claude-agent-memory \
  -H "Content-Type: application/json" \
  -d '{
    "action": "design-workflow",
    "contactId": "designer-session-001",
    "businessId": "my-business",
    "useMemory": true,
    "data": {
      "description": "Build a workflow for GMB directions leads scoring 85+",
      "useCase": "Convert high-intent leads with immediate SMS + email",
      "targetAudience": "Local service businesses",
      "channel": "multi-channel",
      "includeAI": true,
      "complianceLevel": "full"
    }
  }'
```

**Response:**
```json
{
  "success": true,
  "workflow": {
    "workflow_name": "High-Intent GMB Directions Workflow",
    "use_case": "Convert 65-80% of GMB directions leads...",
    "triggers": [...],
    "steps": [...],
    "ghl_setup_instructions": [...]
  },
  "metadata": {
    "agent": "GHL Workflow Designer",
    "tokens": {...}
  }
}
```

### Use Orchestrator

```bash
curl -X POST https://YOUR_VERCEL_URL/api/claude-agent-memory \
  -H "Content-Type: application/json" \
  -d '{
    "action": "orchestrate",
    "contactId": "orchestrator-001",
    "businessId": "my-business",
    "data": {
      "description": "Build a complete lead nurture system: score leads, generate copy, create workflow",
      "context": {
        "business": {
          "name": "CrossFit Brooklyn",
          "category": "Fitness"
        },
        "goal": "65% conversion on high-intent leads"
      },
      "useMemory": true
    }
  }'
```

**Response:**
```json
{
  "success": true,
  "executionPlan": {
    "goal": "Create complete lead nurture automation",
    "execution_plan": [
      {
        "step": 1,
        "agent": "Lead Scorer",
        "action": "score-lead",
        "purpose": "Define high-intent threshold"
      },
      {
        "step": 2,
        "agent": "Copywriter",
        "action": "generate-copy",
        "purpose": "Generate SMS/email copy"
      },
      {
        "step": 3,
        "agent": "GHL Workflow Designer",
        "action": "design-workflow",
        "purpose": "Create complete workflow"
      }
    ]
  },
  "planningResponse": "..."
}
```

---

## 💡 Usage Patterns

### Pattern 1: Generate Single Workflow

**Use:** Workflow Designer
**When:** You know exactly what workflow you need
**Example:** "Create a no-show follow-up workflow"

```javascript
{
  "action": "design-workflow",
  "data": {
    "description": "Follow up with appointment no-shows",
    "channel": "sms",
    "includeAI": true
  }
}
```

### Pattern 2: Build Complete System

**Use:** Orchestrator
**When:** You need multiple agents to work together
**Example:** "Build a complete lead nurture system"

```javascript
{
  "action": "orchestrate",
  "data": {
    "description": "Build complete lead nurture: score → copy → workflow",
    "context": { ... }
  }
}
```

### Pattern 3: Iterative Design (Conversational)

**Use:** Either (with same contactId)
**When:** You want to refine designs through conversation
**Example:** Design → Review → Refine

```javascript
// Request 1
{
  "action": "design-workflow",
  "contactId": "session-123", // SAME ID
  "data": {
    "description": "Email nurture sequence"
  }
}

// Request 2 (refinement)
{
  "action": "design-workflow",
  "contactId": "session-123", // SAME ID
  "data": {
    "description": "Add SMS escalation to previous workflow"
  }
}
```

### Pattern 4: Optimize Existing Workflow

**Use:** Orchestrator
**When:** You have a workflow that's underperforming
**Example:** "My workflow converts at 35%, goal is 65%"

```javascript
{
  "action": "orchestrate",
  "data": {
    "description": "Optimize my GMB workflow - currently 35% conversion, goal 65%",
    "context": {
      "currentWorkflow": { ... },
      "problems": ["Generic messaging", "Slow follow-up"]
    }
  }
}
```

---

## 🏗️ Real-World Use Cases

### Use Case 1: New Business Setup

**Goal:** Set up complete GHL automation from scratch

```javascript
// Step 1: Orchestrate overall system
{
  "action": "orchestrate",
  "data": {
    "description": "I'm a new gym. Set up complete lead automation: GMB leads, email nurture, SMS follow-up"
  }
}

// Orchestrator will coordinate:
// - Lead Scorer (define scoring criteria)
// - Copywriter (generate all copy)
// - Workflow Designer (create workflows)
```

### Use Case 2: Campaign Launch

**Goal:** Launch new service/product

```javascript
{
  "action": "orchestrate",
  "data": {
    "description": "Launch new Virtual Training service at $49/mo. Target existing members + past leads."
  }
}
```

### Use Case 3: Crisis Management

**Goal:** Handle negative reviews/PR crisis

```javascript
{
  "action": "orchestrate",
  "data": {
    "description": "We got 3 negative reviews about customer service. Create response plan."
  }
}
```

### Use Case 4: Expansion

**Goal:** Open second location

```javascript
{
  "action": "orchestrate",
  "data": {
    "description": "Opening second location. Create system to route leads by proximity, customize messaging per location."
  }
}
```

---

## 🔧 Integration with GHL

### Step 1: Get Workflow JSON

Call Workflow Designer:

```bash
{
  "action": "design-workflow",
  "data": { ... }
}
```

Receive:
```json
{
  "workflow": {
    "workflow_name": "...",
    "triggers": [...],
    "steps": [
      {
        "step": 1,
        "type": "action",
        "details": {
          "webhook_url": "https://YOUR_VERCEL_URL/api/claude-agent-memory",
          "body": {
            "action": "score-lead",
            "contactId": "{{contact.id}}",
            ...
          }
        }
      }
    ],
    "ghl_setup_instructions": [...]
  }
}
```

### Step 2: Implement in GHL

Follow `ghl_setup_instructions`:

1. Create new workflow in GHL
2. Set trigger (webhook, form, tag, etc.)
3. Add conditions (IF/THEN logic)
4. Add webhook actions (call Claude agents)
5. Map responses to custom fields
6. Add follow-up actions (emails, SMS, etc.)

### Step 3: Test

Use the Test Interface (`/test.html`):
- Dry-run mode (no API cost)
- Mock responses
- Validate before deploying

---

## 📊 Monitoring & Optimization

### Track Performance

Use **Execution History** dashboard (`/executions.html`):
- Success rate by action
- Average duration
- Token usage (cost tracking)
- Replay failed executions

### Monitor Errors

Use **Error Dashboard** (`/errors.html`):
- Critical errors (Slack alerts)
- Retry tracking
- Resolution workflow

### Iterate Based on Data

```javascript
// 1. Review execution history
// 2. Identify underperforming workflows
// 3. Ask Orchestrator to optimize

{
  "action": "orchestrate",
  "data": {
    "description": "My GMB workflow converts at 45%, industry benchmark is 65%. Analyze and optimize.",
    "context": {
      "executionData": { ... }, // From execution history
      "currentPerformance": "45%",
      "goal": "65%"
    }
  }
}
```

---

## 💰 Cost Optimization

### Workflow Designer Costs

- **Tokens:** 2,000-4,000 per workflow (complex designs)
- **Cost:** ~$0.03-$0.07 per workflow design
- **Usage:** Design once, use forever

### Orchestrator Costs

- **Tokens:** 1,500-3,000 (planning only)
- **Cost:** ~$0.02-$0.05 per orchestration request
- **Usage:** For complex multi-agent tasks

### Tips to Reduce Costs

1. **Use Memory** - Designer remembers previous designs, avoids re-explaining
2. **Be Specific** - Clear descriptions = fewer tokens
3. **Design Once** - Create templates, reuse across clients
4. **Test in Dry-Run** - Use Test Interface before production

---

## 🎯 Best Practices

### 1. Start with Orchestrator for Complex Tasks

❌ **Don't:**
```javascript
// Manually call each agent separately
scoreLead() → generateCopy() → designWorkflow()
```

✅ **Do:**
```javascript
// Let Orchestrator coordinate
orchestrate({ description: "Build complete system" })
```

### 2. Use Memory for Iterative Design

```javascript
// Same contactId = continuous conversation
{
  "contactId": "design-session-123", // Keep same ID
  "useMemory": true
}
```

### 3. Provide Context

❌ **Vague:**
```javascript
{ "description": "Make a workflow" }
```

✅ **Specific:**
```javascript
{
  "description": "Create email nurture for GMB leads scoring 70-84",
  "context": {
    "business": { "name": "CrossFit Brooklyn", "category": "Fitness" },
    "goal": "45% conversion",
    "constraints": ["TCPA-compliant", "Budget: $500/mo"]
  }
}
```

### 4. Validate Before Deploying

1. Use Test Interface (`/test.html`)
2. Review generated workflow JSON
3. Check compliance (SMS consent, time restrictions)
4. Test with sample data

---

## 🔮 What's Next

You now have a **self-improving AI system** that:

✅ Designs world-class GHL workflows from natural language
✅ Coordinates multiple agents for complex tasks
✅ Maintains conversational memory for iterative design
✅ Tracks performance with observability dashboards

**Next evolution:** Add ML-powered workflow optimization based on actual performance data (coming soon).

---

## 📚 Examples

See full examples:
- `/api/examples/workflow-designer-examples.js`
- `/api/examples/orchestrator-examples.js`

Run examples:
```bash
cd /home/user/Circuitos/api/examples
node workflow-designer-examples.js
node orchestrator-examples.js
```

---

**Questions?** Check the code comments or review the system prompts in:
- `/api/lib/ghl-workflow-designer.js`
- `/api/lib/orchestrator.js`

**© 2025 Circuit OS™**
**Powered by Claude Sonnet 4.5 + Conversational Memory**
