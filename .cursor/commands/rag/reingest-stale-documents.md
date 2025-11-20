# Re-ingest Stale Documents

Identify and re-crawl documents that are outdated or have negative feedback.

## Steps:

1. Query for stale documents (older than 7 days OR flagged by feedback)
2. Review list and confirm which to re-ingest
3. Trigger re-ingestion for each document
4. Verify updated content and mark feedback as processed

## API Flow:

### Step 1: Get stale documents
```bash
curl "http://localhost:5001/api/rag/stale?days=7" | jq '.stale_documents'
```

### Step 2: Re-ingest specific document
```bash
curl -X POST http://localhost:5001/api/rag/reingest/123 | jq
```

### Step 3: Verify success
```bash
curl http://localhost:5001/api/rag/health | jq
```

## Automated Re-ingestion:
The n8n workflow handles this automatically every night:
- File: `/n8n/workflows/rag-nightly-reingestion.json`
- Schedule: Daily at 2 AM
- Criteria: Documents older than 7 days OR with negative feedback
- Notifications: Slack alerts to #rag-updates channel

## Manual Override:
If you need to force re-ingestion of a specific URL (bypassing document ID):
```bash
curl -X POST http://localhost:5001/api/rag/ingest_url \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://npcnewsonline.com/2026-rules",
    "metadata": {"force_update": true}
  }'
```

This will:
1. Crawl the URL fresh
2. Generate new content hash
3. Replace existing document if URL matches
4. Create new chunks with updated embeddings

## Best Practices:
- Re-ingest event pages before major competitions
- Re-ingest licensing info when packages change
- Monitor feedback signals weekly to catch issues early
- Don't re-ingest more than 50 documents at once (rate limiting)
