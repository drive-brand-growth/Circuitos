-- Circuit OS - Supabase Database Schema
-- Conversational Memory + ML Feedback Loop

-- Table: conversation_history
-- Stores all agent-contact interactions
CREATE TABLE IF NOT EXISTS conversation_history (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  contact_id VARCHAR(255) NOT NULL,
  business_id VARCHAR(255) NOT NULL,
  agent_name VARCHAR(100),
  role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant')),
  content TEXT NOT NULL,
  metadata JSONB DEFAULT '{}',
  created_at TIMESTAMP DEFAULT NOW()
);

-- Indexes for fast lookups
CREATE INDEX IF NOT EXISTS idx_contact_conversations
  ON conversation_history(contact_id, created_at DESC);

CREATE INDEX IF NOT EXISTS idx_business_conversations
  ON conversation_history(business_id, created_at DESC);

CREATE INDEX IF NOT EXISTS idx_agent_history
  ON conversation_history(agent_name, created_at DESC);

-- Table: agent_feedback
-- Stores ML feedback loop data (predicted vs actual outcomes)
CREATE TABLE IF NOT EXISTS agent_feedback (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  conversation_id UUID REFERENCES conversation_history(id) ON DELETE CASCADE,
  contact_id VARCHAR(255) NOT NULL,
  predicted_outcome VARCHAR(50) NOT NULL,
  actual_outcome VARCHAR(50) NOT NULL,
  error_delta NUMERIC(5,3) NOT NULL,
  learned_patterns JSONB DEFAULT '{}',
  created_at TIMESTAMP DEFAULT NOW()
);

-- Index for ML training queries
CREATE INDEX IF NOT EXISTS idx_feedback_errors
  ON agent_feedback(error_delta DESC, created_at DESC);

CREATE INDEX IF NOT EXISTS idx_feedback_outcomes
  ON agent_feedback(predicted_outcome, actual_outcome);

-- Table: ml_retraining_queue
-- Queue for flagged conversations that need ML retraining
CREATE TABLE IF NOT EXISTS ml_retraining_queue (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  conversation_id UUID REFERENCES conversation_history(id) ON DELETE CASCADE,
  error_delta NUMERIC(5,3) NOT NULL,
  priority VARCHAR(20) DEFAULT 'MEDIUM' CHECK (priority IN ('LOW', 'MEDIUM', 'HIGH')),
  status VARCHAR(20) DEFAULT 'PENDING' CHECK (status IN ('PENDING', 'PROCESSING', 'COMPLETED')),
  created_at TIMESTAMP DEFAULT NOW(),
  processed_at TIMESTAMP
);

-- Index for processing queue
CREATE INDEX IF NOT EXISTS idx_retraining_queue
  ON ml_retraining_queue(priority DESC, created_at ASC)
  WHERE status = 'PENDING';

-- Enable Row Level Security (RLS) for production
ALTER TABLE conversation_history ENABLE ROW LEVEL SECURITY;
ALTER TABLE agent_feedback ENABLE ROW LEVEL SECURITY;
ALTER TABLE ml_retraining_queue ENABLE ROW LEVEL SECURITY;

-- Create policies (adjust based on your auth setup)
-- For now, allow all operations with service role key

-- Function: Clean up old conversations (GDPR compliance)
CREATE OR REPLACE FUNCTION cleanup_old_conversations(days_old INTEGER DEFAULT 365)
RETURNS INTEGER AS $$
DECLARE
  deleted_count INTEGER;
BEGIN
  DELETE FROM conversation_history
  WHERE created_at < NOW() - INTERVAL '1 day' * days_old;

  GET DIAGNOSTICS deleted_count = ROW_COUNT;
  RETURN deleted_count;
END;
$$ LANGUAGE plpgsql;

-- Function: Get conversation stats
CREATE OR REPLACE FUNCTION get_conversation_stats(p_contact_id VARCHAR)
RETURNS JSON AS $$
DECLARE
  stats JSON;
BEGIN
  SELECT json_build_object(
    'total_messages', COUNT(*),
    'turn_count', COUNT(*) FILTER (WHERE role = 'user'),
    'agents_involved', COUNT(DISTINCT agent_name),
    'first_interaction', MIN(created_at),
    'last_interaction', MAX(created_at),
    'total_tokens', SUM((metadata->>'tokens')::INTEGER)
  )
  INTO stats
  FROM conversation_history
  WHERE contact_id = p_contact_id;

  RETURN stats;
END;
$$ LANGUAGE plpgsql;

-- Function: Get ML feedback summary
CREATE OR REPLACE FUNCTION get_ml_feedback_summary()
RETURNS JSON AS $$
DECLARE
  summary JSON;
BEGIN
  SELECT json_build_object(
    'total_feedback_records', COUNT(*),
    'avg_error_delta', AVG(error_delta),
    'high_error_count', COUNT(*) FILTER (WHERE error_delta > 0.5),
    'pending_retraining', (SELECT COUNT(*) FROM ml_retraining_queue WHERE status = 'PENDING')
  )
  INTO summary
  FROM agent_feedback;

  RETURN summary;
END;
$$ LANGUAGE plpgsql;

-- View: Recent agent activity
CREATE OR REPLACE VIEW recent_agent_activity AS
SELECT
  agent_name,
  COUNT(*) as message_count,
  COUNT(DISTINCT contact_id) as unique_contacts,
  AVG((metadata->>'tokens')::INTEGER) as avg_tokens,
  MAX(created_at) as last_activity
FROM conversation_history
WHERE created_at > NOW() - INTERVAL '7 days'
  AND role = 'assistant'
GROUP BY agent_name
ORDER BY message_count DESC;

-- View: Feedback accuracy by agent
CREATE OR REPLACE VIEW agent_accuracy AS
SELECT
  ch.agent_name,
  COUNT(af.id) as predictions_made,
  AVG(af.error_delta) as avg_error,
  COUNT(*) FILTER (WHERE af.error_delta < 0.2) as accurate_predictions,
  COUNT(*) FILTER (WHERE af.error_delta > 0.5) as poor_predictions
FROM conversation_history ch
JOIN agent_feedback af ON af.conversation_id = ch.id
WHERE ch.role = 'assistant'
GROUP BY ch.agent_name
ORDER BY avg_error ASC;

-- Sample data for testing (optional)
-- Uncomment to insert test data

/*
INSERT INTO conversation_history (contact_id, business_id, agent_name, role, content, metadata) VALUES
  ('test-contact-1', 'test-business-1', 'Lead Scorer', 'user', 'Score this lead: John Doe, Brooklyn', '{"tokens": 12}'),
  ('test-contact-1', 'test-business-1', 'Lead Scorer', 'assistant', '{"total_score": 78, "grade": "A"}', '{"tokens": 45, "action": "SCORED_LEAD"}'),
  ('test-contact-1', 'test-business-1', 'Copywriter', 'user', 'Generate cold email copy', '{"tokens": 8}'),
  ('test-contact-1', 'test-business-1', 'Copywriter', 'assistant', '{"variants": [{"id": "A", "subject": "..."}, {"id": "B", "subject": "..."}]}', '{"tokens": 234, "action": "GENERATED_COPY"}');
*/

-- Grant permissions (adjust based on your setup)
-- GRANT ALL ON conversation_history TO authenticated;
-- GRANT ALL ON agent_feedback TO authenticated;
-- GRANT ALL ON ml_retraining_queue TO authenticated;
