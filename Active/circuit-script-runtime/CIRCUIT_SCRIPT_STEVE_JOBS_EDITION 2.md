# Circuit Script™ - Steve Jobs Edition
## The Simplest Thing That Could Possibly Work

**Reality Check:** Your 34,000+ lines of agent logic don't need a new platform. They need a **unified execution layer**.

---

## The Problem (In Steve Jobs Terms)

**Current State:**
- 34,357 lines of brilliant agent logic (Virtual LPR, social media agents, ML feedback loops)
- Scattered across Flask webhooks, Railway functions, GHL workflows
- Prompt injection protections in 17 places
- Judgment Protocol duplicated everywhere
- Debugging = checking 10 different log streams

**What You Actually Need:**
```
One place to run all your agents.
One place to enforce governor limits.
One place to see logs.
One place to deploy.
```

That's it. Everything else is noise.

---

## Steve Jobs Design Principles (From Your Docs)

### 1. Speed Obsession
- Page load: <1.5s
- Analysis: <5s (10,000 deals)
- "Holy shit" moment: <2 minutes

### 2. Dark Knight Foundation
- Pure black (#0B0C0D) - operators work at night
- Steel typography (#E3E7EB, #C2C8CF)
- Neon green signals (#38FF6A) - truth/action
- Red critical alerts (#FF5555) - problems

### 3. No Bullshit
- If it doesn't make revenue faster, cut it
- If it takes >2 minutes to understand, simplify it
- If you can't deploy it in <5 minutes, rebuild it

---

## Circuit Script - The Simplest Version

### What It Actually Is

**Before Circuit Script:**
```python
# 15 separate Flask routes
@app.route('/webhooks/ghl/contact-created')
@app.route('/webhooks/ghl/opportunity-updated')
@app.route('/webhooks/linkedin/profile-viewed')
# ... 12 more routes

# Duplicated logic everywhere
def check_prompt_injection(input):  # Copied in 17 files
def enforce_governor_limits():      # Copied in 17 files
def log_to_supabase():              # Copied in 17 files
```

**After Circuit Script:**
```python
# circuit_script/triggers/contact_trigger.py
from circuit_script import CircuitTrigger, CircuitDB, CircuitLog, VirtualLPR

class ContactTrigger(CircuitTrigger):

    @trigger('Contact', ['afterInsert'])
    async def score_new_leads(self, context):
        # Your EXACT Virtual LPR logic (1,505 lines)
        scores = await VirtualLPR.scoreLeads(context.newRecords)
        await CircuitDB.update('Contact', scores)

        # Route hot leads
        hot_leads = [s for s in scores if s.total >= 70]
        if hot_leads:
            await self.routeToSales(hot_leads)

# That's it. Governor limits, logging, injection protection = handled by runtime.
```

---

## Your Actual Tech Stack (No Guessing)

Based on `/Active/metroflex-ghl-website/AI_Agent/`:

**Current Production Stack:**
- **Runtime:** Flask + Python 3.11
- **AI Model:** OpenAI GPT-4o-mini ($0.0005/chat)
- **Vector DB:** ChromaDB (local, free)
- **Database:** Supabase (PostgreSQL)
- **Deployment:** Heroku or DigitalOcean ($7-12/month)
- **Integration:** GoHighLevel API + webhooks

**Cost:** ~$10-15/month total

---

## Circuit Script Implementation (Flask Version)

### What Gets Built

```
circuit-script/
├── runtime/
│   ├── governor.py          (Enforce 30s timeout, 50 API calls, 128MB)
│   ├── logger.py            (Centralized Supabase logging)
│   ├── security.py          (17-level Judgment Protocol, injection protection)
│   └── trigger_registry.py  (Maps GHL webhooks → your triggers)
│
├── core/
│   ├── CircuitDB.py         (GHL/Salesforce query wrapper)
│   ├── CircuitTrigger.py    (Base class for triggers)
│   └── CircuitLog.py        (Structured logging)
│
├── agents/
│   ├── VirtualLPR.py        (Your 1,505-line scoring logic - UNCHANGED)
│   ├── ReputationGuardian.py (Your 1,038-line review logic - UNCHANGED)
│   ├── OmnichannelOrchestrator.py (Your 1,061-line sequence logic - UNCHANGED)
│   └── MLFeedbackLoop.py    (Your feedback loop - UNCHANGED)
│
└── triggers/
    ├── ContactTrigger.py    (NEW: Score leads on insert/update)
    ├── OpportunityTrigger.py (NEW: Track pipeline changes)
    └── ReviewTrigger.py     (NEW: Respond to reviews)
```

**Total new code:** ~800 lines (runtime + core)
**Migrated code:** 34,357 lines (your existing logic, mostly copy-paste)

---

## Before vs After (Your MetroFlex AI Agent)

### Before: Scattered Flask Routes

```python
# metroflex_ai_agent.py (389 lines)

@app.route('/api/chat', methods=['POST'])
def chat():
    # Manual injection check
    if check_injection(request.json['message']):
        return jsonify({'error': 'Blocked'}), 403

    # Manual rate limiting
    if exceeded_rate_limit(user_id):
        return jsonify({'error': 'Rate limit'}), 429

    # Manual timeout handling (NONE! Can run forever!)
    response = call_openai(request.json['message'])

    # Manual logging (scattered)
    print(f"User {user_id} asked: {request.json['message']}")

    return jsonify({'response': response})
```

**Problems:**
- No timeout enforcement (can blow budget)
- No centralized logging (prints to console, lost in 7 days)
- Injection check duplicated in 15+ routes
- No governor limits (API calls, memory, execution time)

---

### After: Circuit Script Trigger

```python
# circuit_script/triggers/ChatTrigger.py

from circuit_script import CircuitTrigger, CircuitLog, OpenAI

class ChatTrigger(CircuitTrigger):

    @trigger('Chat', ['onCreate'])
    async def handleChat(self, context):
        # Injection check = automatic (runtime handles it)
        # Rate limiting = automatic (runtime handles it)
        # Timeout = automatic (30s max enforced by governor)

        message = context.newRecord.message

        # Call OpenAI (governor enforces 50 API call limit)
        response = await OpenAI.chat(message)

        # Logging = automatic (structured, permanent in Supabase)
        CircuitLog.info(f"Chat response generated", {
            'userId': context.newRecord.userId,
            'messageLength': len(message),
            'responseLength': len(response)
        })

        # Update GHL with response
        await CircuitDB.update('Chat', {
            'id': context.newRecord.id,
            'response': response,
            'status': 'completed'
        })

# Governor enforced automatically:
# - 30 second timeout (kills execution if exceeded)
# - 50 API call limit (prevents budget blowout)
# - 128MB memory limit (prevents memory leaks)
```

**Benefits:**
- Timeout enforced (can't blow budget)
- Centralized logging (Supabase, searchable forever)
- Injection protection (handled once in runtime)
- Governor limits (automatic enforcement)

---

## Migration Plan (Solo Founder, 8 Weeks)

### Week 1-2: Build Runtime (40 hours)
**What:** Core runtime + governor + logging + security

```bash
# Day 1-2: Governor
circuit-script/runtime/governor.py
- Enforce 30s timeout (Promise.race wrapper)
- Track API call count (50 max)
- Track memory usage (128MB max)
- Kill execution if limits exceeded

# Day 3-4: Security
circuit-script/runtime/security.py
- Port your 17-level Judgment Protocol
- Consolidate prompt injection patterns
- Single source of truth (no duplication)

# Day 5-7: Logging
circuit-script/runtime/logger.py
- Supabase integration (your existing DB)
- Structured logging (JSON format)
- Execution traces (track every trigger)

# Day 8-10: Trigger Registry
circuit-script/runtime/trigger_registry.py
- Map GHL webhooks → triggers
- Route to correct handler
- Error handling + retries
```

**Deliverable:**
- Circuit Script runtime works
- Can execute simple trigger from GHL webhook
- Governor limits enforced
- Logs visible in Supabase

---

### Week 3-4: Migrate Virtual LPR (40 hours)

**What:** Port your 1,505-line Virtual LPR logic

```bash
# Day 1-3: Port Scoring Logic
circuit-script/agents/VirtualLPR.py
- Copy/paste your EXACT scoring algorithm
- Change only: imports + DB calls
- NO changes to scoring math (it works!)

# Day 4-5: Create ContactTrigger
circuit-script/triggers/ContactTrigger.py
- afterInsert: Score new leads
- afterUpdate: Re-score if intent changed
- Route hot leads (score ≥70)

# Day 6-8: Shadow Mode Testing
- Run Circuit Script alongside current webhook
- Compare results (should match 100%)
- Log discrepancies
- Fix any bugs

# Day 9-10: Cutover
- Switch GHL webhook to Circuit Script
- Monitor for 48 hours
- Disable old Flask route
```

**Deliverable:**
- Virtual LPR runs in Circuit Script
- 100% of contacts scored
- Zero errors
- <50ms latency (same as before)

---

### Week 5-6: Migrate Social Media Agents (40 hours)

**What:** Port Reputation Guardian + Omnichannel Orchestrator + LinkedIn

```bash
# Day 1-3: Reputation Guardian (1,038 lines)
circuit-script/agents/ReputationGuardian.py
- Copy/paste review monitoring logic
- Create ReviewTrigger (new review detected)
- Auto-generate responses

# Day 4-6: Omnichannel Orchestrator (1,061 lines)
circuit-script/agents/OmnichannelOrchestrator.py
- Copy/paste sequence logic
- Create CampaignTrigger
- Email → LinkedIn → SMS routing

# Day 7-10: Cutover + Testing
- Switch webhooks one at a time
- Monitor for 24 hours each
- Fix any bugs
```

**Deliverable:**
- All social media agents in Circuit Script
- LinkedIn enrichment automatic
- Review monitoring automatic

---

### Week 7-8: Polish + Launch (40 hours)

**What:** Documentation, testing, optimization

```bash
# Day 1-3: Write Tests
- Unit tests (50%+ coverage)
- Integration tests (GHL webhooks)
- Load tests (1000 contacts/min)

# Day 4-6: Documentation
- Quick start guide
- API reference
- Migration guide for other agents

# Day 7-10: Optimization
- Add caching (reduce API calls)
- Optimize hot paths
- Performance tuning
```

**Deliverable:**
- Circuit Script production-ready
- All 34,357 lines migrated
- Tests passing
- Documentation complete

---

## What Changes (Minimal)

### Your Code (90% UNCHANGED)

**Virtual LPR Scoring:**
```python
# Before (in Flask route)
def calculate_score(lead, enriched):
    fit_score = 0
    if lead.industry == 'Technology': fit_score += 3
    # ... 1,500 more lines (EXACT SAME)
    return fit_score + intent_score + timing_score

# After (in Circuit Script)
class VirtualLPR:
    @staticmethod
    def calculate(lead, enriched):
        fit_score = 0
        if lead.industry == 'Technology': fit_score += 3
        # ... 1,500 more lines (EXACT SAME)
        return fit_score + intent_score + timing_score
```

**Only changes:**
1. Wrapped in a class (minor)
2. Import changes (minor)
3. DB calls use `CircuitDB` instead of `supabase` (minor)

**YOUR SCORING LOGIC = 100% IDENTICAL**

---

### Infrastructure (Simplified)

**Before:**
- 15+ Flask routes (scattered)
- Manual governor checks (inconsistent)
- Manual logging (prints everywhere)
- Manual injection checks (duplicated 17 times)
- Deploy = git push, hope it works

**After:**
- 1 unified runtime
- Automatic governor (enforced for all triggers)
- Automatic logging (centralized in Supabase)
- Automatic security (single source of truth)
- Deploy = `circuit-script deploy` (with tests!)

---

## Cost Comparison (Your Actual Stack)

### Before (Current)
| Service | Cost | Purpose |
|---------|------|---------|
| Heroku Dyno | $7/mo | Flask app |
| OpenAI API | ~$5/mo | GPT-4o-mini (efficient!) |
| Supabase | Free | Database + logging |
| **Total** | **$12/mo** | |

### After (Circuit Script)
| Service | Cost | Purpose |
|---------|------|---------|
| Heroku Dyno | $7/mo | Circuit Script runtime |
| OpenAI API | ~$5/mo | GPT-4o-mini (same) |
| Supabase | Free | Database + logging |
| **Total** | **$12/mo** | **SAME COST!** |

**Savings:** $0 (same cost, but 10x better architecture)

---

## What You Get (The Real Benefits)

### 1. Centralized Everything

**Before:**
```
Debugging a lead scoring issue:
1. Check GHL webhook logs
2. Check Flask console logs (disappear after restart)
3. Check Supabase database
4. Check OpenAI API logs
5. Manually correlate timestamps
Total time: 30 minutes
```

**After:**
```
Debugging a lead scoring issue:
1. Search Supabase logs by contact email
2. See entire execution trace in one view
Total time: 2 minutes
```

---

### 2. Governor Limits (Prevent Budget Blowout)

**Before:**
```python
# NO TIMEOUT! Can run forever if API hangs
response = await openai.chat(message)
# If this hangs, you're billed until Heroku kills it (30+ seconds)
```

**After:**
```python
# Circuit Script governor KILLS execution at 30 seconds
# Max 50 API calls per execution
# Max 128MB memory
# Automatic enforcement, no manual checks needed
```

**Real scenario prevented:**
- Bug causes infinite loop calling OpenAI
- Before: $500 surprise bill
- After: Execution killed at 30s, $0.50 max damage

---

### 3. Security (Single Source of Truth)

**Before:**
```
17 different files with injection checks
- Some check for "ignore previous instructions"
- Some check for "DAN mode"
- Some check for "show system prompt"
- Easy to miss a pattern in one file
- Updates require changing 17 files
```

**After:**
```
1 security module (circuit-script/runtime/security.py)
- All 17 levels of Judgment Protocol
- All injection patterns
- Update once, applies everywhere
- Impossible to forget
```

---

## The Steve Jobs Test

**Question:** If Steve Jobs reviewed Circuit Script, what would he say?

**Answer:**
✅ "Why do I need this?" → Makes your 34K lines actually deployable
✅ "Is it fast?" → Same speed, better logging
✅ "Can I understand it in 2 minutes?" → Yes (this doc)
✅ "Can I deploy it in 5 minutes?" → Yes (after Week 8)
✅ "Does it make me money faster?" → Yes (faster debugging = faster iteration)

**Verdict:** Ship it.

---

## Decision Time

### Option A: Keep Current Architecture
**Pros:**
- Works today (sort of)
- Familiar

**Cons:**
- 15+ Flask routes duplicating logic
- No governor limits (can blow budget)
- Logging scattered (30 min to debug)
- Injection checks duplicated 17 times
- Deploy = manual, no tests

**Risk:** Technical debt compounds, eventually unmaintainable

---

### Option B: Build Circuit Script (8 Weeks)
**Pros:**
- Same cost ($12/month)
- 10x faster debugging (2 min vs 30 min)
- Governor limits prevent blowouts
- Security centralized (update once)
- Deploy with confidence (tests required)
- Your 34K lines = unchanged (just reorganized)

**Cons:**
- 8 weeks of work (160 hours)
- Learning curve (1-2 days)

**Risk:** Minimal (shadow mode testing, instant rollback)

---

## Next Steps (If You're In)

### This Week (5 hours)
1. Review this doc
2. Read [CRITICAL_GAP_ANALYSIS.md](./CRITICAL_GAP_ANALYSIS.md)
3. Read [BEFORE_VS_AFTER.md](./BEFORE_VS_AFTER.md)
4. Decision: Build Circuit Script or not?

### Week 1 (If Yes)
1. Set up new GitHub repo: `circuit-script-runtime`
2. Copy Flask deployment structure (Heroku + Supabase)
3. Build governor.py (30s timeout enforcement)
4. Build logger.py (Supabase integration)
5. Build security.py (port Judgment Protocol)
6. Test with simple trigger

### Week 2-8 (Execution)
- Follow migration plan above
- One agent at a time (Virtual LPR → Social Media → Others)
- Shadow mode testing (no production risk)
- Cutover when 100% match

---

## The Bottom Line

**Circuit Script is NOT:**
- A new programming language (it's Python)
- A new cloud platform (uses your Heroku + Supabase)
- A rewrite of your logic (copy/paste 90% of it)

**Circuit Script IS:**
- A unified runtime for your 34K lines
- Governor limits (30s timeout, 50 API calls, 128MB)
- Centralized logging (Supabase, searchable)
- Centralized security (17-level Judgment Protocol, once)
- Deploy with confidence (tests required)

**Timeline:** 8 weeks solo (160 hours)
**Cost:** $0 additional (same Heroku + Supabase stack)
**Risk:** Low (shadow mode + instant rollback)
**Benefit:** 10x faster debugging, prevent budget blowouts, maintainable codebase

---

## Steve Jobs Would Say

> "This is not about adding features. This is about removing chaos. Your agents are brilliant. Your infrastructure is scattered. Circuit Script fixes that. Ship it."

---

**Ready to start?** Let me know and I'll generate:
1. `circuit-script/runtime/governor.py` (complete)
2. `circuit-script/runtime/security.py` (17-level Judgment Protocol)
3. `circuit-script/runtime/logger.py` (Supabase integration)
4. `circuit-script/core/CircuitDB.py` (GHL wrapper)
5. `circuit-script/triggers/ContactTrigger.py` (Virtual LPR example)

**Not ready?** That's fine too. Your current stack works. Circuit Script is for when you want to scale without the chaos.

---

**© 2025 CircuitOS™ - Circuit Script Steve Jobs Edition**
**Status:** Ready to Build
**Timeline:** 8 Weeks Solo
**Cost:** $0 Additional
**Risk:** Low

**"Simplicity is the ultimate sophistication." - Steve Jobs**
