-- Circuit OS - Enhanced Observability Schema
-- Add error tracking, execution history, and scheduled jobs

-- Table: error_log
-- Tracks all errors with severity classification
CREATE TABLE IF NOT EXISTS error_log (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  timestamp TIMESTAMP DEFAULT NOW(),
  context VARCHAR(100) NOT NULL, -- 'score-lead', 'generate-copy', etc.
  error_message TEXT NOT NULL,
  error_stack TEXT,
  contact_id VARCHAR(255),
  business_id VARCHAR(255),
  severity VARCHAR(20) CHECK (severity IN ('CRITICAL', 'HIGH', 'MEDIUM', 'LOW')),
  retry_count INTEGER DEFAULT 0,
  metadata JSONB DEFAULT '{}',
  resolved BOOLEAN DEFAULT FALSE,
  resolved_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_error_severity ON error_log(severity, timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_error_contact ON error_log(contact_id);
CREATE INDEX IF NOT EXISTS idx_error_unresolved ON error_log(resolved, timestamp DESC) WHERE resolved = FALSE;

-- Table: executions
-- Tracks all API executions with full input/output
CREATE TABLE IF NOT EXISTS executions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  execution_id VARCHAR(255) UNIQUE NOT NULL,
  action VARCHAR(100) NOT NULL,
  contact_id VARCHAR(255),
  business_id VARCHAR(255),
  status VARCHAR(20) CHECK (status IN ('RUNNING', 'SUCCESS', 'FAILED')) DEFAULT 'RUNNING',
  started_at TIMESTAMP DEFAULT NOW(),
  completed_at TIMESTAMP,
  duration_ms INTEGER,
  input_data JSONB,
  output_data JSONB,
  tokens_used INTEGER,
  error_message TEXT,
  error_stack TEXT,
  metadata JSONB DEFAULT '{}',
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_execution_contact ON executions(contact_id, started_at DESC);
CREATE INDEX IF NOT EXISTS idx_execution_action ON executions(action, started_at DESC);
CREATE INDEX IF NOT EXISTS idx_execution_status ON executions(status, started_at DESC);
CREATE INDEX IF NOT EXISTS idx_execution_recent ON executions(started_at DESC);

-- Table: scheduled_jobs
-- Track cron jobs and scheduled tasks
CREATE TABLE IF NOT EXISTS scheduled_jobs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  job_name VARCHAR(100) NOT NULL,
  schedule VARCHAR(100), -- cron format
  last_run TIMESTAMP,
  next_run TIMESTAMP,
  status VARCHAR(20) CHECK (status IN ('ACTIVE', 'PAUSED', 'FAILED')),
  run_count INTEGER DEFAULT 0,
  failure_count INTEGER DEFAULT 0,
  last_error TEXT,
  metadata JSONB DEFAULT '{}',
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_scheduled_jobs_next ON scheduled_jobs(next_run ASC) WHERE status = 'ACTIVE';

-- Function: Get error statistics
CREATE OR REPLACE FUNCTION get_error_stats(days INTEGER DEFAULT 7)
RETURNS JSON AS $$
DECLARE
  stats JSON;
BEGIN
  SELECT json_build_object(
    'total_errors', COUNT(*),
    'by_severity', (
      SELECT json_object_agg(severity, count)
      FROM (
        SELECT severity, COUNT(*) as count
        FROM error_log
        WHERE timestamp > NOW() - INTERVAL '1 day' * days
        GROUP BY severity
      ) severity_counts
    ),
    'by_context', (
      SELECT json_object_agg(context, count)
      FROM (
        SELECT context, COUNT(*) as count
        FROM error_log
        WHERE timestamp > NOW() - INTERVAL '1 day' * days
        GROUP BY context
        ORDER BY count DESC
        LIMIT 10
      ) context_counts
    ),
    'unresolved_count', (
      SELECT COUNT(*)
      FROM error_log
      WHERE resolved = FALSE
        AND timestamp > NOW() - INTERVAL '1 day' * days
    ),
    'avg_resolution_time_hours', (
      SELECT EXTRACT(EPOCH FROM AVG(resolved_at - timestamp)) / 3600
      FROM error_log
      WHERE resolved = TRUE
        AND timestamp > NOW() - INTERVAL '1 day' * days
    )
  )
  INTO stats
  FROM error_log
  WHERE timestamp > NOW() - INTERVAL '1 day' * days;

  RETURN stats;
END;
$$ LANGUAGE plpgsql;

-- Function: Get execution statistics
CREATE OR REPLACE FUNCTION get_execution_stats(days INTEGER DEFAULT 7)
RETURNS JSON AS $$
DECLARE
  stats JSON;
BEGIN
  SELECT json_build_object(
    'total_executions', COUNT(*),
    'by_status', (
      SELECT json_object_agg(status, count)
      FROM (
        SELECT status, COUNT(*) as count
        FROM executions
        WHERE started_at > NOW() - INTERVAL '1 day' * days
        GROUP BY status
      ) status_counts
    ),
    'by_action', (
      SELECT json_object_agg(action, count)
      FROM (
        SELECT action, COUNT(*) as count
        FROM executions
        WHERE started_at > NOW() - INTERVAL '1 day' * days
        GROUP BY action
        ORDER BY count DESC
      ) action_counts
    ),
    'avg_duration_ms', (
      SELECT AVG(duration_ms)::INTEGER
      FROM executions
      WHERE started_at > NOW() - INTERVAL '1 day' * days
        AND status = 'SUCCESS'
    ),
    'total_tokens', (
      SELECT SUM(tokens_used)
      FROM executions
      WHERE started_at > NOW() - INTERVAL '1 day' * days
    ),
    'success_rate', (
      SELECT ROUND(
        (COUNT(*) FILTER (WHERE status = 'SUCCESS')::NUMERIC / COUNT(*) * 100),
        2
      )
      FROM executions
      WHERE started_at > NOW() - INTERVAL '1 day' * days
    )
  )
  INTO stats
  FROM executions
  WHERE started_at > NOW() - INTERVAL '1 day' * days;

  RETURN stats;
END;
$$ LANGUAGE plpgsql;

-- Function: Clean up old executions
CREATE OR REPLACE FUNCTION cleanup_old_executions(days_old INTEGER DEFAULT 90)
RETURNS INTEGER AS $$
DECLARE
  deleted_count INTEGER;
BEGIN
  DELETE FROM executions
  WHERE started_at < NOW() - INTERVAL '1 day' * days_old;

  GET DIAGNOSTICS deleted_count = ROW_COUNT;
  RETURN deleted_count;
END;
$$ LANGUAGE plpgsql;

-- Function: Clean up old errors
CREATE OR REPLACE FUNCTION cleanup_old_errors(days_old INTEGER DEFAULT 180)
RETURNS INTEGER AS $$
DECLARE
  deleted_count INTEGER;
BEGIN
  DELETE FROM error_log
  WHERE timestamp < NOW() - INTERVAL '1 day' * days_old
    AND resolved = TRUE;

  GET DIAGNOSTICS deleted_count = ROW_COUNT;
  RETURN deleted_count;
END;
$$ LANGUAGE plpgsql;

-- View: Recent failed executions
CREATE OR REPLACE VIEW recent_failures AS
SELECT
  e.execution_id,
  e.action,
  e.contact_id,
  e.started_at,
  e.duration_ms,
  e.error_message,
  e.metadata
FROM executions e
WHERE e.status = 'FAILED'
  AND e.started_at > NOW() - INTERVAL '7 days'
ORDER BY e.started_at DESC;

-- View: Performance metrics by action
CREATE OR REPLACE VIEW action_performance AS
SELECT
  action,
  COUNT(*) as total_executions,
  COUNT(*) FILTER (WHERE status = 'SUCCESS') as successful,
  COUNT(*) FILTER (WHERE status = 'FAILED') as failed,
  ROUND((COUNT(*) FILTER (WHERE status = 'SUCCESS')::NUMERIC / COUNT(*) * 100), 2) as success_rate,
  AVG(duration_ms) FILTER (WHERE status = 'SUCCESS')::INTEGER as avg_duration_ms,
  PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY duration_ms) FILTER (WHERE status = 'SUCCESS')::INTEGER as median_duration_ms,
  PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY duration_ms) FILTER (WHERE status = 'SUCCESS')::INTEGER as p95_duration_ms,
  SUM(tokens_used) as total_tokens
FROM executions
WHERE started_at > NOW() - INTERVAL '7 days'
GROUP BY action
ORDER BY total_executions DESC;

-- Grant permissions (adjust based on your RLS setup)
-- ALTER TABLE error_log ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE executions ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE scheduled_jobs ENABLE ROW LEVEL SECURITY;

COMMENT ON TABLE error_log IS 'Tracks all errors with severity classification and retry information';
COMMENT ON TABLE executions IS 'Tracks all API executions with full input/output for debugging';
COMMENT ON TABLE scheduled_jobs IS 'Manages scheduled cron jobs and background tasks';
