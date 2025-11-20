# Analyze Semantic Cache Performance

Review the RAG semantic cache statistics to identify optimization opportunities.

## Steps:

1. Fetch current cache stats from the API
2. Calculate cache hit rate (hits / total queries)
3. Identify patterns in cached queries
4. Recommend adjustments to TTL or threshold if needed

## API Endpoint:
```bash
curl http://localhost:5001/api/rag/cache/stats | jq
```

## Key Metrics to Review:
- **buckets**: Number of cache buckets (should scale with query diversity)
- **total_entries**: Total cached query-result pairs
- **ttl**: Time-to-live in seconds (default: 3600s = 1 hour)
- **threshold**: Similarity threshold for cache hits (default: 0.95)

## Performance Indicators:
- **Good**: 30%+ cache hit rate
- **Excellent**: 50%+ cache hit rate
- **Needs tuning**: <15% cache hit rate

## Optimization Recommendations:
- If hit rate is low and buckets are high: Consider lowering similarity threshold to 0.90
- If hit rate is high but entries grow unbounded: Reduce TTL to 1800s (30 min)
- If queries are very diverse: Increase bucket size or accept lower hit rate

## Follow-up Actions:
1. If cache needs tuning, update `RAG_CACHE_TTL` in docker-compose.yml
2. Clear cache after config changes: `POST /api/rag/cache/clear`
3. Monitor for 24 hours and re-analyze
