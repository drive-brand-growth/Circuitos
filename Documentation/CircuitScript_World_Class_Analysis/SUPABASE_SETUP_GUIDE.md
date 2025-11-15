# Circuit Script™ - Supabase Setup Guide
## Create Dedicated Database Space

**Goal:** Set up new Supabase project for Circuit Script (separate from existing CircuitOS data)

---

## Step 1: Create New Supabase Project (3 minutes)

1. Go to https://supabase.com/dashboard
2. Click "New Project"
3. **Name:** `circuit-script-production`
4. **Database Password:** (generate strong password, save to password manager)
5. **Region:** Choose closest to your Heroku region (e.g., `us-east-1`)
6. Click "Create new project"

**Wait 2-3 minutes** for provisioning...

---

## Step 2: Get Connection Details (1 minute)

1. Go to Project Settings → Database
2. Copy these values:

```bash
# Save these to .env file (local) and Heroku config vars (production)
SUPABASE_URL=https://YOUR_PROJECT_REF.supabase.co
SUPABASE_ANON_KEY=eyJhbGc...  (public key, safe to use client-side)
SUPABASE_SERVICE_KEY=eyJhbGc...  (secret key, server-side only)
DATABASE_URL=postgresql://postgres:[PASSWORD]@db.YOUR_PROJECT_REF.supabase.co:5432/postgres
```

---

## Step 3: Create Circuit Script Schema (5 minutes)

### A. circuit_logs Table (Centralized Logging)

Run this in Supabase SQL Editor:

```sql
-- Circuit Script Logs Table
CREATE TABLE circuit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

    -- Execution Context
    execution_id TEXT NOT NULL,
    trigger_name TEXT NOT NULL,
    object_name TEXT,
    event_type TEXT,

    -- User/Tenant
    user_id TEXT,
    tenant_id TEXT,

    -- Log Details
    level TEXT NOT NULL CHECK (level IN ('DEBUG', 'INFO', 'WARN', 'ERROR', 'CRITICAL')),
    message TEXT NOT NULL,
    context JSONB,

    -- Performance
    duration_ms INTEGER,
    api_calls_used INTEGER,
    memory_used_mb REAL,

    -- Status
    status TEXT CHECK (status IN ('SUCCESS', 'FAILED', 'TIMEOUT', 'LIMIT_EXCEEDED')),
    error_message TEXT,
    stack_trace TEXT
);

-- Indexes for fast searching
CREATE INDEX idx_circuit_logs_execution_id ON circuit_logs(execution_id);
CREATE INDEX idx_circuit_logs_created_at ON circuit_logs(created_at DESC);
CREATE INDEX idx_circuit_logs_trigger_name ON circuit_logs(trigger_name);
CREATE INDEX idx_circuit_logs_level ON circuit_logs(level);
CREATE INDEX idx_circuit_logs_status ON circuit_logs(status);
CREATE INDEX idx_circuit_logs_user_id ON circuit_logs(user_id);

-- Enable Row Level Security (RLS)
ALTER TABLE circuit_logs ENABLE ROW LEVEL SECURITY;

-- Policy: Service role can do everything
CREATE POLICY "Service role has full access"
ON circuit_logs
FOR ALL
TO service_role
USING (true)
WITH CHECK (true);

COMMENT ON TABLE circuit_logs IS 'Centralized logging for all Circuit Script trigger executions';
```

---

### B. circuit_governor_usage Table (Resource Tracking)

```sql
-- Governor Usage Tracking
CREATE TABLE circuit_governor_usage (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

    -- Execution Reference
    execution_id TEXT NOT NULL,
    trigger_name TEXT NOT NULL,

    -- Resource Usage
    execution_time_ms INTEGER NOT NULL,
    api_callouts INTEGER NOT NULL,
    database_queries INTEGER NOT NULL,
    memory_used_mb REAL,

    -- Limits
    timeout_limit_ms INTEGER NOT NULL DEFAULT 30000,
    api_limit INTEGER NOT NULL DEFAULT 50,
    db_limit INTEGER NOT NULL DEFAULT 100,
    memory_limit_mb INTEGER NOT NULL DEFAULT 128,

    -- Status
    limit_exceeded BOOLEAN DEFAULT FALSE,
    limit_type TEXT,  -- 'TIMEOUT', 'API_CALLS', 'DB_QUERIES', 'MEMORY'

    -- Tenant
    tenant_id TEXT
);

CREATE INDEX idx_governor_execution_id ON circuit_governor_usage(execution_id);
CREATE INDEX idx_governor_created_at ON circuit_governor_usage(created_at DESC);
CREATE INDEX idx_governor_limit_exceeded ON circuit_governor_usage(limit_exceeded);

ALTER TABLE circuit_governor_usage ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Service role has full access"
ON circuit_governor_usage
FOR ALL
TO service_role
USING (true)
WITH CHECK (true);

COMMENT ON TABLE circuit_governor_usage IS 'Track governor limit usage per execution';
```

---

### C. circuit_security_events Table (17-Level Security Tracking)

```sql
-- Security Events (Injection Attempts, etc.)
CREATE TABLE circuit_security_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

    -- Event Details
    event_type TEXT NOT NULL CHECK (event_type IN ('INJECTION_ATTEMPT', 'RATE_LIMIT_EXCEEDED', 'INVALID_INPUT', 'UNAUTHORIZED_ACCESS')),
    severity TEXT NOT NULL CHECK (severity IN ('LOW', 'MEDIUM', 'HIGH', 'CRITICAL')),

    -- User Context
    user_id TEXT,
    ip_address INET,
    user_agent TEXT,

    -- Attack Details
    risk_score REAL,  -- 0.0 to 1.0
    detected_patterns JSONB,  -- Array of regex patterns matched
    input_sample TEXT,  -- First 500 chars of malicious input

    -- Action Taken
    blocked BOOLEAN DEFAULT TRUE,
    action TEXT,  -- 'BLOCKED', 'LOGGED', 'RATE_LIMITED'

    -- Reference
    execution_id TEXT,
    trigger_name TEXT
);

CREATE INDEX idx_security_created_at ON circuit_security_events(created_at DESC);
CREATE INDEX idx_security_event_type ON circuit_security_events(event_type);
CREATE INDEX idx_security_severity ON circuit_security_events(severity);
CREATE INDEX idx_security_user_id ON circuit_security_events(user_id);
CREATE INDEX idx_security_blocked ON circuit_security_events(blocked);

ALTER TABLE circuit_security_events ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Service role has full access"
ON circuit_security_events
FOR ALL
TO service_role
USING (true)
WITH CHECK (true);

COMMENT ON TABLE circuit_security_events IS '17-Level Judgment Protocol security event tracking';
```

---

### D. circuit_trigger_registry Table (Trigger Metadata)

```sql
-- Trigger Registry (Track what triggers are deployed)
CREATE TABLE circuit_trigger_registry (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

    -- Trigger Info
    trigger_name TEXT UNIQUE NOT NULL,
    object_name TEXT NOT NULL,  -- 'Contact', 'Opportunity', etc.
    event_types TEXT[] NOT NULL,  -- ['afterInsert', 'afterUpdate']

    -- Status
    enabled BOOLEAN DEFAULT TRUE,
    version TEXT NOT NULL DEFAULT '1.0.0',

    -- Metadata
    description TEXT,
    agent_class TEXT,  -- 'VirtualLPR', 'ReputationGuardian', etc.
    config JSONB,  -- Trigger-specific config

    -- Stats
    execution_count INTEGER DEFAULT 0,
    last_executed_at TIMESTAMP WITH TIME ZONE,
    average_duration_ms REAL,
    error_rate REAL
);

CREATE INDEX idx_trigger_registry_object ON circuit_trigger_registry(object_name);
CREATE INDEX idx_trigger_registry_enabled ON circuit_trigger_registry(enabled);

ALTER TABLE circuit_trigger_registry ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Service role has full access"
ON circuit_trigger_registry
FOR ALL
TO service_role
USING (true)
WITH CHECK (true);

COMMENT ON TABLE circuit_trigger_registry IS 'Registry of all deployed Circuit Script triggers';
```

---

## Step 4: Create Database Functions (5 minutes)

### A. Log Trigger Execution

```sql
-- Function to insert log entry
CREATE OR REPLACE FUNCTION log_trigger_execution(
    p_execution_id TEXT,
    p_trigger_name TEXT,
    p_level TEXT,
    p_message TEXT,
    p_context JSONB DEFAULT '{}'::JSONB,
    p_duration_ms INTEGER DEFAULT NULL,
    p_status TEXT DEFAULT 'SUCCESS'
)
RETURNS UUID AS $$
DECLARE
    v_log_id UUID;
BEGIN
    INSERT INTO circuit_logs (
        execution_id,
        trigger_name,
        level,
        message,
        context,
        duration_ms,
        status
    ) VALUES (
        p_execution_id,
        p_trigger_name,
        p_level,
        p_message,
        p_context,
        p_duration_ms,
        p_status
    ) RETURNING id INTO v_log_id;

    RETURN v_log_id;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
```

---

### B. Track Governor Usage

```sql
-- Function to track governor usage
CREATE OR REPLACE FUNCTION track_governor_usage(
    p_execution_id TEXT,
    p_trigger_name TEXT,
    p_execution_time_ms INTEGER,
    p_api_callouts INTEGER,
    p_database_queries INTEGER,
    p_memory_used_mb REAL DEFAULT NULL
)
RETURNS BOOLEAN AS $$
DECLARE
    v_limit_exceeded BOOLEAN DEFAULT FALSE;
    v_limit_type TEXT DEFAULT NULL;
BEGIN
    -- Check limits
    IF p_execution_time_ms > 30000 THEN
        v_limit_exceeded := TRUE;
        v_limit_type := 'TIMEOUT';
    ELSIF p_api_callouts > 50 THEN
        v_limit_exceeded := TRUE;
        v_limit_type := 'API_CALLS';
    ELSIF p_database_queries > 100 THEN
        v_limit_exceeded := TRUE;
        v_limit_type := 'DB_QUERIES';
    ELSIF p_memory_used_mb > 128 THEN
        v_limit_exceeded := TRUE;
        v_limit_type := 'MEMORY';
    END IF;

    -- Insert usage record
    INSERT INTO circuit_governor_usage (
        execution_id,
        trigger_name,
        execution_time_ms,
        api_callouts,
        database_queries,
        memory_used_mb,
        limit_exceeded,
        limit_type
    ) VALUES (
        p_execution_id,
        p_trigger_name,
        p_execution_time_ms,
        p_api_callouts,
        p_database_queries,
        p_memory_used_mb,
        v_limit_exceeded,
        v_limit_type
    );

    RETURN v_limit_exceeded;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
```

---

### C. Update Trigger Stats

```sql
-- Function to update trigger stats
CREATE OR REPLACE FUNCTION update_trigger_stats(
    p_trigger_name TEXT,
    p_duration_ms INTEGER,
    p_success BOOLEAN
)
RETURNS VOID AS $$
BEGIN
    UPDATE circuit_trigger_registry
    SET
        execution_count = execution_count + 1,
        last_executed_at = NOW(),
        average_duration_ms = COALESCE(
            (average_duration_ms * execution_count + p_duration_ms) / (execution_count + 1),
            p_duration_ms
        ),
        error_rate = CASE
            WHEN p_success THEN error_rate * execution_count / (execution_count + 1)
            ELSE (error_rate * execution_count + 1) / (execution_count + 1)
        END,
        updated_at = NOW()
    WHERE trigger_name = p_trigger_name;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
```

---

## Step 5: Seed Initial Data (2 minutes)

```sql
-- Seed trigger registry with Virtual LPR
INSERT INTO circuit_trigger_registry (
    trigger_name,
    object_name,
    event_types,
    description,
    agent_class,
    version
) VALUES
(
    'ContactTrigger.score_new_leads',
    'Contact',
    ARRAY['afterInsert'],
    'Score new leads using Virtual LPR algorithm',
    'VirtualLPR',
    '1.0.0'
),
(
    'ContactTrigger.rescore_on_intent_change',
    'Contact',
    ARRAY['afterUpdate'],
    'Re-score contacts when intent signals change',
    'VirtualLPR',
    '1.0.0'
),
(
    'ReviewTrigger.handle_new_review',
    'Review',
    ARRAY['afterInsert'],
    'Automatically respond to new reviews',
    'ReputationGuardian',
    '1.0.0'
);
```

---

## Step 6: Configure Environment Variables (2 minutes)

### Local Development (.env file)

```bash
# Create .env file (DON'T commit to git!)
cat > .env << 'EOF'
# Supabase
SUPABASE_URL=https://YOUR_PROJECT_REF.supabase.co
SUPABASE_ANON_KEY=eyJhbGc...
SUPABASE_SERVICE_KEY=eyJhbGc...

# OpenAI
OPENAI_API_KEY=sk-...

# GoHighLevel
GHL_API_KEY=...

# Environment
ENV=development
DEBUG=True
EOF
```

### Heroku Production

```bash
# Set Heroku config vars
heroku config:set SUPABASE_URL=https://YOUR_PROJECT_REF.supabase.co
heroku config:set SUPABASE_SERVICE_KEY=eyJhbGc...
heroku config:set OPENAI_API_KEY=sk-...
heroku config:set GHL_API_KEY=...
heroku config:set ENV=production
```

---

## Step 7: Test Connection (2 minutes)

```python
# test_supabase_connection.py

from supabase import create_client, Client
import os

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_SERVICE_KEY")

supabase: Client = create_client(url, key)

# Test insert
response = supabase.table("circuit_logs").insert({
    "execution_id": "test-001",
    "trigger_name": "TestTrigger",
    "level": "INFO",
    "message": "Connection test successful!",
    "context": {"test": True}
}).execute()

print(f"✅ Supabase connection successful! Log ID: {response.data[0]['id']}")

# Test query
logs = supabase.table("circuit_logs").select("*").limit(1).execute()
print(f"✅ Query successful! Found {len(logs.data)} logs")
```

Run:
```bash
python test_supabase_connection.py
```

---

## Supabase Dashboard Views (Helpful Queries)

### View Recent Logs

```sql
SELECT
    created_at,
    trigger_name,
    level,
    message,
    duration_ms,
    status
FROM circuit_logs
ORDER BY created_at DESC
LIMIT 100;
```

### View Governor Limit Violations

```sql
SELECT
    created_at,
    trigger_name,
    limit_type,
    execution_time_ms,
    api_callouts,
    database_queries
FROM circuit_governor_usage
WHERE limit_exceeded = TRUE
ORDER BY created_at DESC;
```

### View Security Events

```sql
SELECT
    created_at,
    event_type,
    severity,
    risk_score,
    detected_patterns,
    input_sample
FROM circuit_security_events
WHERE severity IN ('HIGH', 'CRITICAL')
ORDER BY created_at DESC;
```

### Trigger Performance Report

```sql
SELECT
    trigger_name,
    execution_count,
    average_duration_ms,
    error_rate,
    last_executed_at
FROM circuit_trigger_registry
ORDER BY execution_count DESC;
```

---

## Backup Strategy (Important!)

### Daily Backups (Automated)

1. Go to Project Settings → Database → Backups
2. Enable daily backups (free tier: 7 days retention)
3. For production: Upgrade to Pro ($25/mo) for 30-day retention

### Manual Backup (Before Migrations)

```bash
# Dump database
pg_dump $DATABASE_URL > backup_$(date +%Y%m%d).sql

# Restore if needed
psql $DATABASE_URL < backup_20250101.sql
```

---

## Next Steps

1. ✅ Supabase project created
2. ✅ Schema created (circuit_logs, circuit_governor_usage, circuit_security_events, circuit_trigger_registry)
3. ✅ Functions created (logging, governor tracking, stats updates)
4. ✅ Environment variables configured
5. ✅ Connection tested
6. → **Next:** Start Week 1 (build circuit_script/runtime/logger.py to use this database)

---

**© 2025 CircuitOS™ - Supabase Setup Complete**
**Database:** circuit-script-production
**Tables:** 4 (logs, governor_usage, security_events, trigger_registry)
**Ready for:** Week 1 implementation
