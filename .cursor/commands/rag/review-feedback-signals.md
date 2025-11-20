# Review Feedback Signals

Analyze user feedback patterns to identify knowledge base quality issues.

## Steps:

1. Connect to the agentforce database
2. Query the rag_feedback table for recent feedback
3. Identify chunks with negative feedback patterns
4. Flag documents that need re-ingestion

## SQL Query:
```sql
-- Recent feedback summary
SELECT
  feedback_type,
  COUNT(*) as count,
  AVG(feedback_value) as avg_value,
  COUNT(CASE WHEN processed = false THEN 1 END) as unprocessed
FROM rag_feedback
WHERE created_at > NOW() - INTERVAL '7 days'
GROUP BY feedback_type
ORDER BY count DESC;

-- Documents flagged as outdated
SELECT DISTINCT
  d.id,
  d.url,
  d.title,
  d.last_updated,
  COUNT(f.id) as feedback_count
FROM rag_documents d
JOIN rag_feedback f ON d.id = f.document_id
WHERE f.feedback_type IN ('outdated', 'low_quality', 'incorrect')
  AND f.processed = false
GROUP BY d.id, d.url, d.title, d.last_updated
ORDER BY feedback_count DESC
LIMIT 10;
```

## Interpretation:
- **outdated**: Content needs re-crawling (trigger re-ingestion)
- **low_quality**: Content extraction issues (review chunking strategy)
- **incorrect**: Factual errors (verify source or remove)
- **unhelpful**: Ranking issue (feedback reranker will auto-adjust)

## Action Items:
1. For documents with 3+ "outdated" signals: Queue for immediate re-ingestion
2. For persistent "low_quality" signals: Review trafilatura extraction settings
3. For "incorrect" signals: Manual review required before re-ingestion

## Automation Trigger:
The n8n workflow `rag-nightly-reingestion.json` automatically processes this feedback daily. Manual intervention only needed for persistent issues.
