# Ingest NPC Events Website

Crawl and ingest the latest NPC bodybuilding event information into the RAG knowledge base.

## Steps:

1. Identify the main NPC events page URL (typically npcnewsonline.com)
2. Use the RAG ingestion API to crawl and index the page
3. Verify successful ingestion by checking chunk count
4. Review any errors or warnings

## Example URLs to ingest:
- https://npcnewsonline.com/2026-classic-rules
- https://npcnewsonline.com/better-bodies-classic
- https://npcnewsonline.com/branch-warren-classic

## API Endpoint:
```bash
curl -X POST http://localhost:5001/api/rag/ingest_url \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://npcnewsonline.com/...",
    "metadata": {
      "category": "events",
      "source": "npc",
      "priority": "high"
    }
  }'
```

## Expected Output:
- success: true
- chunks_created: 10-30 (varies by page)
- document_id: auto-generated

## Follow-up:
After ingestion, test retrieval with: "What are the 2026 NPC event rules?"
