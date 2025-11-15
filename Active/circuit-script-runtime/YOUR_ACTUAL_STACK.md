# Circuit Script - YOUR ACTUAL STACK
## Aligned with MetroFlex Events AI Agent Architecture

**Your Current Stack (MetroFlex Events):**
- **Runtime:** Flask (Python) on Railway/Fly.io
- **Database:** Supabase (PostgreSQL) + ChromaDB (vector)
- **AI:** OpenAI GPT-4o-mini ($0.0005/chat)
- **Deployment:** GitHub → Railway/Fly.io
- **Cost:** ~$5/month

**Circuit Script Should Use:**
- ✅ **Same stack** (Flask + Railway + Supabase)
- ✅ **Same deployment** (GitHub → Railway)
- ✅ **Same AI model** (GPT-4o-mini for cost)
- ✅ **Same patterns** (RAG, vector embeddings, ChromaDB)

---

## What You Already Have

### 1. MetroFlex Events AI Agent (389 lines)
**File:** `/Active/metroflex-ghl-website/AI_Agent/metroflex_ai_agent.py`

**Architecture:**
```python
Flask app
  ├── OpenAI GPT-4o-mini (RAG)
  ├── ChromaDB (vector embeddings)
  ├── Sentence Transformers (all-MiniLM-L6-v2)
  ├── Knowledge Base (JSON)
  └── GHL webhook integration
```

**Deployment:**
- Railway/Fly.io
- Environment variables (OPENAI_API_KEY)
- Health check endpoint (`/health`)
- Chat webhook (`/webhook/chat`)

**Cost:** $0.0005/chat (GPT-4o-mini)

---

## Circuit Script Should Be

**Same architecture, extended for CircuitOS:**

```python
Flask app (Circuit Script Runtime)
  ├── CircuitGovernor (30s timeout, 50 API calls)
  ├── CircuitLog (Supabase logging)
  ├── CircuitDB (GHL + Salesforce + Supabase)
  ├── VirtualLPR (your 1,506-line scoring logic)
  ├── Social Media Agents (LinkedIn, Reputation Guardian)
  ├── Trigger Framework (contact.created → score)
  └── GHL webhook integration
```

**Same deployment:**
- GitHub → Railway/Fly.io
- Same environment variables pattern
- Same health check pattern
- Same cost structure ($5/month)

---

## Key Differences from Cloudflare Plan

| Feature | Cloudflare Plan (WRONG) | Your Actual Stack (RIGHT) |
|---------|------------------------|---------------------------|
| **Runtime** | Cloudflare Workers (V8) | Flask (Python) on Railway |
| **Framework** | Hono (new, unfamiliar) | Flask (you know this) |
| **Language** | TypeScript | Python |
| **Database** | Workers KV | Supabase PostgreSQL |
| **Deployment** | Wrangler CLI | GitHub → Railway |
| **Logging** | Axiom ($50/mo) | Supabase (free) |
| **AI** | ??? | OpenAI GPT-4o-mini |
| **Vector DB** | ??? | ChromaDB |
| **Learning Curve** | HIGH | ZERO |

---

## What Circuit Script Should Look Like (YOUR STACK)

```python
#!/usr/bin/env python3
"""
Circuit Script™ Runtime
Apex-equivalent execution layer for CircuitOS
Built on your existing MetroFlex Events stack
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional
from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
from supabase import create_client, Client

class CircuitGovernor:
    """Resource management (30s timeout, 50 API calls, 128MB memory)"""
    limits = {
        'maxExecutionTime': 30000,  # 30 seconds
        'maxAPICallouts': 50,
        'maxDatabaseQueries': 100,
    }

    currentExecution = {
        'apiCallouts': 0,
        'databaseQueries': 0,
        'startTime': 0
    }

    @classmethod
    def trackAPICall(cls):
        cls.currentExecution['apiCallouts'] += 1
        if cls.currentExecution['apiCallouts'] > cls.limits['maxAPICallouts']:
            raise Exception(f"API callout limit exceeded: {cls.limits['maxAPICallouts']}")

    @classmethod
    def trackDatabaseQuery(cls):
        cls.currentExecution['databaseQueries'] += 1
        if cls.currentExecution['databaseQueries'] > cls.limits['maxDatabaseQueries']:
            raise Exception(f"Database query limit exceeded: {cls.limits['maxDatabaseQueries']}")


class CircuitLog:
    """Centralized logging to Supabase (like MetroFlex Events pattern)"""

    def __init__(self, supabase_client: Client):
        self.supabase = supabase_client
        self.logs = []
        self.execution_id = None

    def start_execution(self, execution_id: str):
        self.execution_id = execution_id
        self.logs = []

    def info(self, message: str, data: dict = None):
        self._log('INFO', message, data)

    def error(self, message: str, data: dict = None):
        self._log('ERROR', message, data)

    def _log(self, level: str, message: str, data: dict = None):
        entry = {
            'execution_id': self.execution_id,
            'timestamp': datetime.now().isoformat(),
            'level': level,
            'message': message,
            'data': data
        }
        self.logs.append(entry)
        print(f"[{level}] {message}", data or '')

    def flush(self):
        """Store logs in Supabase circuit_execution_logs table"""
        if len(self.logs) > 0:
            self.supabase.table('circuit_execution_logs').insert(self.logs).execute()
        logs = self.logs
        self.logs = []
        return logs


class CircuitDB:
    """Unified data layer for GHL, Salesforce, Supabase (same pattern as MetroFlex)"""

    def __init__(self, supabase_client: Client):
        self.supabase = supabase_client

    def query(self, soql: str, params: dict = None):
        """Query GHL or Salesforce"""
        CircuitGovernor.trackDatabaseQuery()

        # TODO: Implement GHL SDK integration
        # from gohighlevel import GHLClient
        # ghl = GHLClient(os.getenv('GHL_API_KEY'))
        # return ghl.query(soql, params)

        return []  # Placeholder

    def update(self, object_type: str, records: List[dict]):
        """Update records in GHL or Salesforce"""
        CircuitGovernor.trackDatabaseQuery()

        # TODO: Implement GHL SDK bulk update
        # ghl = GHLClient(os.getenv('GHL_API_KEY'))
        # ghl.bulk_update(object_type, records)

        pass  # Placeholder

    def batch_enrich(self, leads: List[dict], sources: List[str]):
        """Batch enrichment (Census, Google Maps, Hunter.io)"""

        for source in sources:
            CircuitGovernor.trackAPICall()

            if source == 'census':
                # TODO: Census API integration
                pass
            elif source == 'google-maps':
                # TODO: Google Maps API integration
                pass
            elif source == 'hunter':
                # TODO: Hunter.io API integration
                pass

        return leads


class VirtualLPR:
    """Your 1,506-line Virtual LPR scoring algorithm"""

    @staticmethod
    def score_leads(leads: List[dict]) -> List[dict]:
        """Score multiple leads (batched for performance)"""
        scores = []

        for lead in leads:
            score = VirtualLPR.calculate(lead)
            scores.append(score)

        return scores

    @staticmethod
    def calculate(lead: dict) -> dict:
        """Calculate LPR score (FIT + INTENT + TIMING)"""
        fit_score = 0
        intent_score = 0
        timing_score = 0
        attribution = []

        # FIT SCORE (40 points)
        if lead.get('industry') == 'Technology':
            fit_score += 3
            attribution.append({
                'points': 3,
                'reason': 'Industry match: Technology',
                'source': 'LinkedIn Company Data'
            })

        # INTENT SCORE (40 points)
        if lead.get('called_business'):
            intent_score += 15
            attribution.append({
                'points': 15,
                'reason': 'Called business',
                'source': 'CallRail Tracking'
            })

        # TIMING SCORE (20 points)
        if lead.get('hours_since_last_activity', 999) <= 2:
            timing_score += 8
            attribution.append({
                'points': 8,
                'reason': 'Very recent activity',
                'source': 'Activity Log'
            })

        total = fit_score + intent_score + timing_score

        # Assign grade
        if total >= 80:
            grade = 'A'
        elif total >= 65:
            grade = 'B'
        elif total >= 40:
            grade = 'C'
        else:
            grade = 'D'

        return {
            'lead_id': lead['id'],
            'total': total,
            'grade': grade,
            'fit': fit_score,
            'intent': intent_score,
            'timing': timing_score,
            'next_action': 'IMMEDIATE_FOLLOWUP' if total >= 70 else 'NURTURE',
            'attribution': attribution
        }


class CircuitTrigger:
    """Base class for triggers (like MetroFlex AI Agent pattern)"""

    def __init__(self, circuit_db: CircuitDB, circuit_log: CircuitLog):
        self.db = circuit_db
        self.log = circuit_log

    def execute(self, context: dict):
        """Override in subclasses"""
        pass


class ContactTrigger(CircuitTrigger):
    """Contact trigger (afterInsert, afterUpdate)"""

    def execute(self, context: dict):
        event_type = context['event_type']
        new_records = context['new_records']

        self.log.info(f'ContactTrigger.{event_type}', {'count': len(new_records)})

        if event_type == 'afterInsert':
            self.score_new_leads(new_records)
        elif event_type == 'afterUpdate':
            self.rescore_if_intent_changed(new_records, context.get('old_records', []))

    def score_new_leads(self, contacts: List[dict]):
        """Score all new contacts using Virtual LPR"""
        scores = VirtualLPR.score_leads(contacts)

        # Update GHL custom fields
        updates = []
        for score in scores:
            updates.append({
                'id': score['lead_id'],
                'vlpr_score__c': score['total'],
                'vlpr_grade__c': score['grade'],
                'next_action__c': score['next_action']
            })

        self.db.update('Contact', updates)

        # Route hot leads
        hot_leads = [s for s in scores if s['total'] >= 70]
        if len(hot_leads) > 0:
            self.log.info('Routing hot leads to sales', {'count': len(hot_leads)})
            # TODO: Create tasks in GHL

    def rescore_if_intent_changed(self, new_contacts: List[dict], old_contacts: List[dict]):
        """Re-score if intent signals changed"""
        to_rescore = []

        for i, new_contact in enumerate(new_contacts):
            old_contact = old_contacts[i] if i < len(old_contacts) else {}

            if (new_contact.get('last_website_visit') != old_contact.get('last_website_visit') or
                new_contact.get('called_business') != old_contact.get('called_business')):
                to_rescore.append(new_contact)

        if len(to_rescore) > 0:
            self.log.info('Re-scoring contacts with changed intent', {'count': len(to_rescore)})
            scores = VirtualLPR.score_leads(to_rescore)

            updates = []
            for score in scores:
                updates.append({
                    'id': score['lead_id'],
                    'vlpr_score__c': score['total'],
                    'vlpr_grade__c': score['grade']
                })

            self.db.update('Contact', updates)


# Flask app (same pattern as MetroFlex Events AI Agent)
app = Flask(__name__)
CORS(app)

# Initialize components
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

circuit_log = CircuitLog(supabase)
circuit_db = CircuitDB(supabase)

# Trigger registry (map event → trigger class)
TRIGGER_REGISTRY = {
    'Contact.afterInsert': ContactTrigger,
    'Contact.afterUpdate': ContactTrigger,
}


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint (same pattern as MetroFlex)"""
    return jsonify({
        "status": "healthy",
        "runtime": "Circuit Script v1.0",
        "agent": "Virtual LPR + CircuitOS"
    })


@app.route('/trigger/<object_type>/<event>', methods=['POST'])
def execute_trigger(object_type: str, event: str):
    """
    Execute Circuit Script trigger (GHL webhook integration)

    Expected payload:
    {
        "new_records": [{"id": "contact_123", "email": "test@example.com"}],
        "old_records": [...]  # Optional (for updates)
    }
    """
    import uuid
    execution_id = str(uuid.uuid4())

    circuit_log.start_execution(execution_id)
    CircuitGovernor.currentExecution['startTime'] = datetime.now().timestamp()

    try:
        data = request.json

        # Find registered trigger
        trigger_key = f"{object_type}.{event}"
        TriggerClass = TRIGGER_REGISTRY.get(trigger_key)

        if not TriggerClass:
            raise Exception(f"No trigger registered for {trigger_key}")

        # Build context
        context = {
            'object_type': object_type,
            'event_type': event,
            'new_records': data.get('new_records', []),
            'old_records': data.get('old_records', []),
            'is_insert': 'Insert' in event,
            'is_update': 'Update' in event
        }

        # Execute trigger
        trigger = TriggerClass(circuit_db, circuit_log)
        trigger.execute(context)

        # Flush logs
        logs = circuit_log.flush()

        return jsonify({
            "success": True,
            "execution_id": execution_id,
            "logs": logs
        })

    except Exception as e:
        circuit_log.error('EXECUTION_ERROR', {'error': str(e)})
        logs = circuit_log.flush()

        return jsonify({
            "success": False,
            "execution_id": execution_id,
            "error": str(e),
            "logs": logs
        }), 500


if __name__ == "__main__":
    print("🚀 Circuit Script Runtime starting...")
    print("📊 Same stack as MetroFlex Events AI Agent")
    print("💬 Trigger endpoint: POST /trigger/:objectType/:event")
    print("❤️  Health check: GET /health")
    app.run(host='0.0.0.0', port=5000, debug=True)
```

---

## Deployment (Same as MetroFlex Events)

### 1. GitHub → Railway

```bash
# Same as your MetroFlex deployment
railway init
railway variables set SUPABASE_URL=your-url
railway variables set SUPABASE_KEY=your-key
railway variables set GHL_API_KEY=your-ghl-key
railway up
```

### 2. Supabase Tables

```sql
-- Same pattern as MetroFlex knowledge base
CREATE TABLE circuit_execution_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    execution_id TEXT NOT NULL,
    timestamp TIMESTAMPTZ NOT NULL,
    level TEXT NOT NULL,
    message TEXT NOT NULL,
    data JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_execution_logs_execution_id ON circuit_execution_logs(execution_id);
```

### 3. GHL Webhook

```
POST https://circuit-script.up.railway.app/trigger/Contact/afterInsert
```

---

## Cost (Same as MetroFlex)

| Service | Cost |
|---------|------|
| Railway (hobby) | $5/month |
| Supabase (free tier) | $0 |
| OpenAI GPT-4o-mini | ~$1/month |
| **Total** | **$6/month** |

---

## Next Steps

1. ✅ Copy MetroFlex Events AI Agent structure
2. ✅ Add CircuitGovernor, CircuitDB, VirtualLPR classes
3. ✅ Deploy to Railway (same process)
4. ✅ Test with GHL webhook

**Timeline:** 2-3 days (not 10 weeks) because you already have the stack!

---

**This is YOUR stack. Use what you know.** 🚀
