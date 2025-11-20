# Query RAG with Quality Gates

Test a RAG query with full quality validation enabled.

## Purpose:
Validate that retrieved documents are relevant and answers are grounded (no hallucinations).

## Steps:

1. Submit query with quality gates enabled
2. Review relevance score (should be >0.7)
3. Check hallucination detection results
4. Analyze performance metrics

## API Request:
```bash
curl -X POST http://localhost:5001/api/rag/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are the MetroFlex licensing packages and costs?",
    "limit": 5,
    "threshold": 0.5,
    "skip_cache": false,
    "skip_quality_gates": false
  }' | jq
```

## Expected Response Structure:
```json
{
  "query": "...",
  "route": "single_step",
  "cached": false,
  "results": [...],
  "count": 3,
  "quality_check": {
    "relevance": {
      "relevant": true,
      "score": 0.92,
      "reasoning": "Documents directly address licensing packages"
    },
    "recommendation": "approved"
  },
  "performance": {
    "total_time_ms": 245.67,
    "cache_hit": false,
    "retrieval_executed": true,
    "feedback_reranked": true
  }
}
```

## Quality Gate Recommendations:
- **approved**: Use results as-is
- **retrieve_more**: Documents not relevant, try different query or web search
- **regenerate**: Answer has hallucinations (shouldn't happen with just retrieval)

## Troubleshooting:
If relevance score is consistently low (<0.5):
1. Check if knowledge base has relevant content (query /api/rag/documents)
2. Try broadening query or using different keywords
3. Consider ingesting additional sources

If performance is slow (>500ms):
1. Check if semantic cache is enabled (should show in response)
2. Verify Redis is healthy: `docker compose ps redis`
3. Review pgvector index: `EXPLAIN ANALYZE` on vector queries
