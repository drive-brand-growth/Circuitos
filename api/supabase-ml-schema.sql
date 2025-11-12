-- Circuit OS - ML Workflow Optimization Schema
-- Tracks workflow performance, winning patterns, and optimizations

-- Table: workflow_performance
-- Tracks performance metrics for each workflow
CREATE TABLE IF NOT EXISTS workflow_performance (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workflow_id VARCHAR(255) UNIQUE NOT NULL,
  workflow_name VARCHAR(255),
  business_id VARCHAR(255),

  -- Performance metrics
  conversion_rate NUMERIC(5,4), -- 0.6500 = 65%
  engagement_rate NUMERIC(5,4), -- Open rate, click rate
  roi NUMERIC(8,2), -- Return on investment (e.g., 4.25x)
  avg_time_to_convert INTEGER, -- Days
  total_leads INTEGER DEFAULT 0,
  total_conversions INTEGER DEFAULT 0,
  total_revenue NUMERIC(12,2),
  total_cost NUMERIC(12,2),

  -- Last updated
  last_updated TIMESTAMP DEFAULT NOW(),
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_workflow_perf_business ON workflow_performance(business_id);
CREATE INDEX IF NOT EXISTS idx_workflow_perf_conversion ON workflow_performance(conversion_rate DESC);

-- Table: workflow_optimizations
-- Tracks ML-powered optimizations and their results
CREATE TABLE IF NOT EXISTS workflow_optimizations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workflow_id VARCHAR(255) REFERENCES workflow_performance(workflow_id),

  -- ML analysis
  ml_score INTEGER, -- 0-100
  ml_score_breakdown JSONB,

  -- Performance before optimization
  performance_before JSONB,

  -- Recommended optimizations
  optimizations JSONB, -- Array of optimization recommendations
  winning_patterns JSONB, -- Demographic/psychographic/trigger patterns
  ab_tests JSONB, -- Recommended A/B tests

  -- Implementation
  implemented BOOLEAN DEFAULT FALSE,
  implemented_at TIMESTAMP,

  -- Performance after optimization (tracked later)
  performance_after JSONB,
  actual_lift NUMERIC(5,4), -- Actual improvement vs predicted

  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_workflow_opt_workflow ON workflow_optimizations(workflow_id);
CREATE INDEX IF NOT EXISTS idx_workflow_opt_score ON workflow_optimizations(ml_score DESC);
CREATE INDEX IF NOT EXISTS idx_workflow_opt_implemented ON workflow_optimizations(implemented, created_at DESC);

-- Table: conversion_patterns
-- Stores demographic/psychographic patterns from successful conversions
CREATE TABLE IF NOT EXISTS conversion_patterns (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  pattern_type VARCHAR(50) NOT NULL, -- 'demographic', 'psychographic', 'trigger', 'timing'
  pattern_name VARCHAR(100) NOT NULL,

  -- Pattern details
  pattern_data JSONB NOT NULL,

  -- Performance metrics
  conversion_rate NUMERIC(5,4),
  sample_size INTEGER,
  avg_ltv NUMERIC(10,2), -- Lifetime value
  confidence_level VARCHAR(20), -- 'HIGH', 'MEDIUM', 'LOW'

  -- Context
  business_category VARCHAR(100),
  date_range DATERANGE,

  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_pattern_type ON conversion_patterns(pattern_type, conversion_rate DESC);
CREATE INDEX IF NOT EXISTS idx_pattern_category ON conversion_patterns(business_category);

-- Table: market_trends
-- Tracks market trends affecting workflow performance
CREATE TABLE IF NOT EXISTS market_trends (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  trend_type VARCHAR(50) NOT NULL, -- 'seasonal', 'industry', 'economic', 'technology'
  trend_name VARCHAR(100) NOT NULL,

  -- Trend data
  description TEXT,
  impact JSONB, -- What impact this trend has
  recommendations JSONB, -- How to adapt workflows

  -- Validity
  valid_from DATE,
  valid_to DATE,
  confidence_level VARCHAR(20),

  -- Sources
  data_sources TEXT[], -- Where this trend was identified

  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_trend_type ON market_trends(trend_type, valid_from DESC);
CREATE INDEX IF NOT EXISTS idx_trend_active ON market_trends(valid_to) WHERE valid_to > CURRENT_DATE;

-- Table: ab_test_results
-- Tracks A/B test results for continuous improvement
CREATE TABLE IF NOT EXISTS ab_test_results (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workflow_id VARCHAR(255),
  test_name VARCHAR(255) NOT NULL,

  -- Test configuration
  hypothesis TEXT,
  variant_a JSONB NOT NULL, -- Control
  variant_b JSONB NOT NULL, -- Test
  success_metric VARCHAR(100), -- 'conversion_rate', 'engagement_rate', etc.

  -- Results
  variant_a_performance NUMERIC(5,4),
  variant_b_performance NUMERIC(5,4),
  lift NUMERIC(5,4), -- % improvement of B over A
  statistical_significance NUMERIC(3,2), -- p-value
  winner VARCHAR(10), -- 'A', 'B', 'INCONCLUSIVE'

  -- Sample
  sample_size INTEGER,
  started_at TIMESTAMP,
  completed_at TIMESTAMP,

  -- Learnings
  learnings TEXT,

  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_ab_test_workflow ON ab_test_results(workflow_id);
CREATE INDEX IF NOT EXISTS idx_ab_test_winner ON ab_test_results(winner, lift DESC);

-- Function: Get winning patterns for ML optimizer
CREATE OR REPLACE FUNCTION get_winning_patterns()
RETURNS JSON AS $$
DECLARE
  patterns JSON;
BEGIN
  SELECT json_build_object(
    'demographics', (
      SELECT json_agg(row_to_json(t))
      FROM (
        SELECT
          pattern_name,
          pattern_data,
          conversion_rate,
          sample_size,
          avg_ltv,
          confidence_level
        FROM conversion_patterns
        WHERE pattern_type = 'demographic'
          AND confidence_level IN ('HIGH', 'MEDIUM')
          AND sample_size >= 50
        ORDER BY conversion_rate DESC
        LIMIT 10
      ) t
    ),
    'psychographics', (
      SELECT json_agg(row_to_json(t))
      FROM (
        SELECT
          pattern_name,
          pattern_data,
          conversion_rate,
          sample_size,
          avg_ltv,
          confidence_level
        FROM conversion_patterns
        WHERE pattern_type = 'psychographic'
          AND confidence_level IN ('HIGH', 'MEDIUM')
          AND sample_size >= 50
        ORDER BY conversion_rate DESC
        LIMIT 10
      ) t
    ),
    'triggers', (
      SELECT json_agg(row_to_json(t))
      FROM (
        SELECT
          pattern_name,
          pattern_data,
          conversion_rate,
          sample_size,
          confidence_level
        FROM conversion_patterns
        WHERE pattern_type = 'trigger'
          AND confidence_level IN ('HIGH', 'MEDIUM')
          AND sample_size >= 100
        ORDER BY conversion_rate DESC
        LIMIT 10
      ) t
    ),
    'timing', (
      SELECT json_agg(row_to_json(t))
      FROM (
        SELECT
          pattern_name,
          pattern_data,
          conversion_rate,
          sample_size
        FROM conversion_patterns
        WHERE pattern_type = 'timing'
          AND confidence_level IN ('HIGH', 'MEDIUM')
          AND sample_size >= 50
        ORDER BY conversion_rate DESC
        LIMIT 10
      ) t
    )
  )
  INTO patterns;

  RETURN patterns;
END;
$$ LANGUAGE plpgsql;

-- Function: Record conversion with pattern data
CREATE OR REPLACE FUNCTION record_conversion_with_patterns(
  p_workflow_id VARCHAR,
  p_contact_data JSONB,
  p_converted BOOLEAN,
  p_revenue NUMERIC DEFAULT 0
)
RETURNS VOID AS $$
DECLARE
  v_demographics JSONB;
  v_psychographics JSONB;
  v_trigger JSONB;
BEGIN
  -- Update workflow performance
  UPDATE workflow_performance
  SET
    total_leads = total_leads + 1,
    total_conversions = total_conversions + (CASE WHEN p_converted THEN 1 ELSE 0 END),
    total_revenue = total_revenue + p_revenue,
    conversion_rate = (total_conversions + (CASE WHEN p_converted THEN 1 ELSE 0 END))::NUMERIC / (total_leads + 1),
    last_updated = NOW()
  WHERE workflow_id = p_workflow_id;

  -- If conversion, extract and update patterns
  IF p_converted THEN
    -- Extract demographic pattern
    v_demographics = jsonb_build_object(
      'age_range', p_contact_data->>'age_range',
      'income_range', p_contact_data->>'income_range',
      'distance_miles', p_contact_data->>'distance_miles',
      'location', p_contact_data->>'city'
    );

    -- Extract psychographic pattern
    v_psychographics = jsonb_build_object(
      'values', p_contact_data->>'values',
      'interests', p_contact_data->>'interests',
      'lifestyle', p_contact_data->>'lifestyle'
    );

    -- Extract trigger pattern
    v_trigger = jsonb_build_object(
      'signal', p_contact_data->>'intent_signal',
      'source', p_contact_data->>'source'
    );

    -- TODO: Update conversion_patterns table with incremental learning
    -- This would use a more sophisticated ML algorithm in production
  END IF;
END;
$$ LANGUAGE plpgsql;

-- Function: Get workflow optimization suggestions
CREATE OR REPLACE FUNCTION get_optimization_suggestions(p_workflow_id VARCHAR)
RETURNS JSON AS $$
DECLARE
  v_performance RECORD;
  v_patterns JSON;
  v_suggestions JSON;
BEGIN
  -- Get current performance
  SELECT * INTO v_performance
  FROM workflow_performance
  WHERE workflow_id = p_workflow_id;

  -- Get winning patterns
  SELECT get_winning_patterns() INTO v_patterns;

  -- Build suggestions (simplified - AI does the heavy lifting)
  SELECT json_build_object(
    'current_performance', row_to_json(v_performance),
    'winning_patterns', v_patterns,
    'benchmark', json_build_object(
      'industry_avg_conversion', 0.65,
      'top_quartile_conversion', 0.85
    )
  ) INTO v_suggestions;

  RETURN v_suggestions;
END;
$$ LANGUAGE plpgsql;

COMMENT ON TABLE workflow_performance IS 'Tracks performance metrics for each workflow';
COMMENT ON TABLE workflow_optimizations IS 'ML-powered workflow optimizations and results';
COMMENT ON TABLE conversion_patterns IS 'Demographic/psychographic/trigger patterns from successful conversions';
COMMENT ON TABLE market_trends IS 'Market trends affecting workflow performance';
COMMENT ON TABLE ab_test_results IS 'A/B test results for continuous improvement';
