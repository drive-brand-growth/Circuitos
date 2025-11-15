# Circuit Script: Next 7 Days Action Plan
## Solo Founder Implementation Guide

**Goal:** Make a GO/NO-GO decision and execute first sprint
**Timeline:** Next 7 days (starting today)
**Effort:** 20-30 hours total

---

## Day 1 (TODAY): Decision Day

**Time Required:** 2-3 hours
**Outcome:** GO or NO-GO decision with clear rationale

### Morning: Read & Analyze (2 hours)

**Tasks:**
1. ✅ Read `QUALITY_CONTROL_GAP_ANALYSIS.md` (60 min)
   - Pay special attention to "Executive Summary"
   - Understand critical gaps
   - Review solo founder timeline (16 weeks, not 8)

2. ✅ Read `RAILWAY_MIGRATION_GUIDE.md` (30 min)
   - Understand Railway vs Cloudflare tradeoffs
   - Review code examples
   - Assess if this feels manageable

3. ✅ Make GO/NO-GO Decision (30 min)
   - Use decision matrix below

### Decision Matrix

Answer these questions honestly:

| Question | YES | NO |
|----------|-----|-----|
| Do I have 6+ months runway (cash)? | | |
| Can I dedicate 20-30 hours/week for 16 weeks? | | |
| Are customers asking for better infrastructure? | | |
| Is this a competitive advantage vs competitors? | | |
| Do I enjoy building infrastructure over features? | | |
| Will this directly increase revenue? | | |
| Can I afford to NOT work on customer acquisition for 4 months? | | |

**Scoring:**
- **6-7 YES:** GO - Build Circuit Script
- **3-5 YES:** MAYBE - Consider scope-reduced version
- **0-2 YES:** NO-GO - Focus on customers instead

### Afternoon: Make Decision & Commit (1 hour)

**If GO:**
1. ✅ Block calendar: 20-30 hours/week for next 16 weeks
2. ✅ Choose tech stack: Railway (recommended) or Cloudflare
3. ✅ Choose timeline: 16 weeks (realistic) or 8 weeks (risky)
4. ✅ Notify stakeholders: "Building Circuit Script, less availability for 4 months"
5. ✅ Set up accountability: Weekly check-ins with advisor/mentor

**If NO-GO (RECOMMENDED):**
1. ✅ Archive Circuit Script files (move to `/Archive/circuit-script/`)
2. ✅ Document decision: Why you chose NOT to build
3. ✅ Identify quick wins instead (see alternative below)
4. ✅ Focus on revenue: Customer acquisition, feature requests
5. ✅ Set reminder: Re-evaluate in 6 months (when you have a team)

---

## Alternative Path: Quick Wins Instead of Circuit Script

**If you chose NO-GO, do this instead:**

### Quick Win 1: Centralize Logs to Supabase (8 hours)

**Current Problem:** Logs scattered, disappear after 7 days

**Solution:**
```typescript
// Add to EVERY webhook handler:
import { createClient } from '@supabase/supabase-js';

const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_KEY);

async function logToSupabase(executionId: string, event: string, data: any) {
    await supabase.from('webhook_logs').insert({
        execution_id: executionId,
        event_type: event,
        timestamp: new Date().toISOString(),
        data: data,
    });
}

// In your webhook:
const executionId = crypto.randomUUID();
await logToSupabase(executionId, 'contact.created', { email: contact.email });
```

**Effort:** 8 hours
**Benefit:** Searchable logs forever, 90% of Circuit Script's logging value

---

### Quick Win 2: Add Governor Limits (8 hours)

**Current Problem:** No timeout, webhooks can run forever (runaway costs)

**Solution:**
```typescript
// Add to EVERY webhook handler:
const startTime = Date.now();
let apiCallCount = 0;

function checkGovernorLimits() {
    const elapsed = Date.now() - startTime;
    if (elapsed > 30000) {  // 30 seconds
        throw new Error('Timeout: Execution exceeded 30 seconds');
    }
    if (apiCallCount > 50) {  // 50 API calls
        throw new Error('API limit: Exceeded 50 API calls');
    }
}

// Before EVERY external API call:
apiCallCount++;
checkGovernorLimits();
const response = await fetch('https://api.example.com/...');
```

**Effort:** 8 hours
**Benefit:** Prevent runaway costs, 80% of Circuit Script's governor value

---

### Quick Win 3: Write Tests for Virtual LPR (12 hours)

**Current Problem:** No tests, every deploy is a gamble

**Solution:**
```typescript
// tests/virtual-lpr.test.ts
import { VirtualLPR } from '../src/virtual-lpr';

describe('VirtualLPR', () => {
    it('should score high-intent lead >= 70', () => {
        const testLead = {
            id: 'test-123',
            email: 'test@example.com',
            calledBusiness: true,
            viewedPricing: true,
            zip: '10019',
        };

        const score = VirtualLPR.calculate(testLead, {
            medianIncome: 87000,
            distance: 1.5,
        });

        expect(score.total).toBeGreaterThanOrEqual(70);
        expect(score.grade).toBe('A');
    });

    // Add 10-15 more tests covering edge cases
});
```

**Effort:** 12 hours
**Benefit:** Catch bugs before production, 60% of Circuit Script's testing value

---

### Quick Win 4: Create Supabase Dashboard (12 hours)

**Current Problem:** No visibility into webhook performance

**Solution:**
```sql
-- Create view in Supabase
CREATE VIEW webhook_metrics AS
SELECT
    DATE_TRUNC('hour', timestamp) as hour,
    event_type,
    COUNT(*) as total_executions,
    AVG((data->>'duration')::int) as avg_duration_ms,
    COUNT(*) FILTER (WHERE data->>'error' IS NOT NULL) as error_count
FROM webhook_logs
WHERE timestamp >= NOW() - INTERVAL '7 days'
GROUP BY hour, event_type
ORDER BY hour DESC;
```

Then create simple HTML dashboard:
```html
<!-- dashboard.html - Host on GitHub Pages -->
<div id="metrics"></div>
<script>
    // Fetch from Supabase, render charts
    fetch('https://your-project.supabase.co/rest/v1/webhook_metrics')
        .then(r => r.json())
        .then(data => renderChart(data));
</script>
```

**Effort:** 12 hours
**Benefit:** Real-time visibility, 70% of Circuit Script's dashboard value

---

### Total Quick Wins: 40 hours (2 weeks @ 20 hours/week)

**Result:** 80% of Circuit Script's value, 10% of the effort, ZERO migration risk

---

## Days 2-7: If You Chose GO (Build Circuit Script)

### Day 2: Railway Setup (4 hours)

**Morning (2 hours):**
1. ✅ Install Railway CLI: `npm install -g @railway/cli`
2. ✅ Create Railway project: `railway init`
3. ✅ Create GitHub repo: `git init && gh repo create`
4. ✅ Set up project structure (copy from `RAILWAY_MIGRATION_GUIDE.md`)

**Afternoon (2 hours):**
1. ✅ Create Supabase `execution_logs` table (see migration guide)
2. ✅ Add environment variables to Railway
3. ✅ Deploy "Hello World" to Railway: `git push`
4. ✅ Verify deployment: `curl https://your-app.railway.app/health`

**Deliverable:** Empty Express server deployed to Railway

---

### Day 3: CircuitGovernor + CircuitLog (6 hours)

**Morning (3 hours):**
1. ✅ Copy `src/runtime/governor.ts` from migration guide
2. ✅ Write unit tests for CircuitGovernor
3. ✅ Test timeout enforcement (should throw after 30 seconds)
4. ✅ Test API call limits (should throw after 50 calls)

**Afternoon (3 hours):**
1. ✅ Copy `src/runtime/logger.ts` from migration guide
2. ✅ Test logging to Supabase
3. ✅ Query logs from Supabase: `SELECT * FROM execution_logs`
4. ✅ Deploy to Railway: `git push`

**Deliverable:** Working governor + logging, deployed to Railway

---

### Day 4: GHL API Client (6 hours)

**Morning (3 hours):**
1. ✅ Copy `src/clients/ghl.ts` from migration guide
2. ✅ Test `getContact()`: Fetch real contact from GHL
3. ✅ Test `updateContact()`: Update custom field
4. ✅ Verify in GHL UI that custom field changed

**Afternoon (3 hours):**
1. ✅ Implement `batchUpdateContacts()` (update 10 contacts at once)
2. ✅ Test with real GHL contacts
3. ✅ Write unit tests (mock fetch)
4. ✅ Deploy to Railway: `git push`

**Deliverable:** Working GHL API client, deployed to Railway

---

### Day 5: Webhook Handler (6 hours)

**Morning (3 hours):**
1. ✅ Copy `src/index.ts` webhook endpoint from migration guide
2. ✅ Test webhook locally:
   ```bash
   npm run dev
   curl -X POST http://localhost:3000/webhook/ghl/contact-created -d '{"contact":{...}}'
   ```
3. ✅ Verify CircuitGovernor starts/ends execution
4. ✅ Verify logs appear in Supabase

**Afternoon (3 hours):**
1. ✅ Deploy to Railway: `git push`
2. ✅ Configure GHL webhook to point to Railway URL
3. ✅ Create test contact in GHL
4. ✅ Verify webhook received, logs in Supabase

**Deliverable:** GHL webhooks working in production

---

### Day 6: Census API + VirtualLPR Stub (6 hours)

**Morning (3 hours):**
1. ✅ Copy `src/clients/census.ts` from migration guide
2. ✅ Test Census API: `batchGetDemographics(['10019', '90210'])`
3. ✅ Verify response has median income, population, etc.
4. ✅ Write unit tests (mock Census API)

**Afternoon (3 hours):**
1. ✅ Copy `src/lib/VirtualLPR.ts` from migration guide
2. ✅ Implement BASIC scoring (just 3-4 rules, not full 1,506 lines)
3. ✅ Test scoring:
   ```typescript
   const score = VirtualLPR.calculate(testLead, censusData);
   console.log(score);  // Should be 0-100
   ```
4. ✅ Deploy to Railway: `git push`

**Deliverable:** Census integration + basic scoring working

---

### Day 7: End-to-End Test + Review (6 hours)

**Morning (3 hours):**
1. ✅ Create test contact in GHL with known properties:
   - ZIP: 10019 (high income)
   - calledBusiness: true
   - viewedPricing: true
2. ✅ Verify webhook triggered
3. ✅ Verify Census API called (check logs)
4. ✅ Verify score calculated (check logs)
5. ✅ Verify GHL custom field updated (check GHL UI)

**Afternoon (3 hours):**
1. ✅ Review week's progress
   - Did you hit 34 hours total?
   - Are you on track for 16-week timeline?
   - Any blockers or surprises?
2. ✅ Plan Week 2 tasks (detailed task list)
3. ✅ Update stakeholders (progress report)
4. ✅ Adjust timeline if needed (be honest about progress)

**Deliverable:** Working end-to-end flow, realistic Week 2 plan

---

## Week 1 Summary (If Building Circuit Script)

**Total Time:** 34 hours
**Completed:**
- ✅ Railway deployment pipeline
- ✅ CircuitGovernor (resource limits)
- ✅ CircuitLog (Supabase logging)
- ✅ GHL API client
- ✅ Webhook handler (receives GHL events)
- ✅ Census API integration
- ✅ Basic VirtualLPR scoring (stub)

**NOT Completed (Week 2+ work):**
- ❌ Full VirtualLPR scoring (1,506-line algorithm)
- ❌ LinkedIn API integration
- ❌ Google Maps API integration
- ❌ Comprehensive testing (>50% coverage)
- ❌ Error handling (retries, circuit breakers)
- ❌ Production hardening

**On Track?**
- If you completed all Day 2-7 tasks: YES, continue to Week 2
- If you only completed 50%: Adjust timeline to 20-24 weeks
- If you completed <50%: Consider NO-GO (focus on quick wins instead)

---

## Week 2 Preview (If Still On Track)

**Goal:** Complete Virtual LPR migration (full scoring algorithm)

**Monday-Tuesday: Port Full Scoring Algorithm (12 hours)**
- Copy all 1,506 lines from your SKILL.md
- Implement fit score (40 points)
- Implement intent score (40 points)
- Implement timing score (20 points)

**Wednesday-Thursday: Testing (12 hours)**
- Write 15-20 unit tests
- Test edge cases (missing data, API failures)
- Achieve 50% code coverage (not 75%)

**Friday: Shadow Mode (6 hours)**
- Run Circuit Script alongside current webhook
- Compare results (should match 100%)
- Log discrepancies
- Fix bugs

**Deliverable:** Full Virtual LPR scoring, tested, running in shadow mode

---

## Decision Checkpoint (End of Day 1)

### If You Chose GO:

**Commit to:**
- [ ] 20-30 hours/week for next 16 weeks
- [ ] Railway tech stack (not Cloudflare)
- [ ] Realistic timeline (16 weeks, not 8)
- [ ] Weekly progress reviews (be honest about delays)
- [ ] NO-GO escape hatch (if falling behind after Week 4)

**Calendar blocks:**
- [ ] Monday: 6 hours (Day 2 tasks)
- [ ] Tuesday: 6 hours (Day 3 tasks)
- [ ] Wednesday: 6 hours (Day 4 tasks)
- [ ] Thursday: 6 hours (Day 5 tasks)
- [ ] Friday: 6 hours (Day 6 tasks)
- [ ] Weekend: 4 hours (Day 7 tasks)

---

### If You Chose NO-GO:

**Commit to:**
- [ ] Archive Circuit Script files
- [ ] Focus on Quick Wins (40 hours over 2 weeks)
- [ ] Customer acquisition (not infrastructure)
- [ ] Re-evaluate in 6 months (when you have team/revenue)

**Calendar blocks:**
- [ ] Week 1: 20 hours (Quick Wins 1-2)
- [ ] Week 2: 20 hours (Quick Wins 3-4)
- [ ] Week 3: Focus on customers

---

## Final Recommendation

**As your Quality Control Agent, my recommendation is NO-GO.**

**Why?**
1. **Opportunity Cost:** 320 hours = 8 weeks of customer work
2. **Zero Revenue Impact:** Customers don't care about your infrastructure
3. **High Risk:** 90% of the code doesn't exist yet
4. **Solo Founder Reality:** 16 weeks is a LONG time alone
5. **Better Alternative:** Quick Wins give you 80% value, 10% effort

**But...**

If you're passionate about building infrastructure, enjoy the challenge, and have 6+ months runway, then GO.

Just be honest about the timeline (16 weeks), use Railway (not Cloudflare), and commit to the weekly schedule.

**Either way, make the decision TODAY and commit.**

Don't spend 2 weeks "thinking about it" - that's 40 hours wasted.

---

## Checklist for Today

- [ ] Read `QUALITY_CONTROL_GAP_ANALYSIS.md` (60 min)
- [ ] Read `RAILWAY_MIGRATION_GUIDE.md` (30 min)
- [ ] Answer Decision Matrix questions (15 min)
- [ ] Make GO or NO-GO decision (15 min)
- [ ] Block calendar for next 7 days (15 min)
- [ ] Notify stakeholders of decision (15 min)
- [ ] Begin Day 2 tasks (if GO) or Quick Wins (if NO-GO)

**Total Time Today:** 2.5 hours

**Tomorrow:** Either start Day 2 tasks (Circuit Script) or Quick Win 1 (logs)

---

**Good luck! Be honest with yourself. It's OK to choose NO-GO.**

**The best builders know when NOT to build.**

---

**End of 7-Day Action Plan**
