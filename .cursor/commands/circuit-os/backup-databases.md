# Backup Circuit OS Databases

Create and verify database backups for disaster recovery.

## Automated Backups:

The backup service runs automatically:
- **Schedule**: Daily at 2 AM
- **Retention**: 7 daily, 4 weekly, 6 monthly
- **Location**: `/docker/postgres-backup/`
- **Databases**: agentforce, ml_audit, circuit_runtime

Configuration in `docker-compose.yml`:
```yaml
backup:
  image: prodrigestivill/postgres-backup-local:16
  environment:
    - SCHEDULE=@daily
    - BACKUP_KEEP_DAYS=7
    - BACKUP_KEEP_WEEKS=4
    - BACKUP_KEEP_MONTHS=6
```

## Manual Backup:

### Full Backup (All Databases)
```bash
# Create backup directory
mkdir -p ./backups/$(date +%Y-%m-%d)

# Backup all databases
docker exec circuitos-db pg_dumpall -U circuitos | gzip > ./backups/$(date +%Y-%m-%d)/all-databases.sql.gz

# Verify backup size
ls -lh ./backups/$(date +%Y-%m-%d)/
```

### Individual Database Backup
```bash
# Backup agentforce (RAG data)
docker exec circuitos-db pg_dump -U circuitos agentforce | gzip > ./backups/$(date +%Y-%m-%d)/agentforce.sql.gz

# Backup ml_audit (ML model data)
docker exec circuitos-db pg_dump -U circuitos ml_audit | gzip > ./backups/$(date +%Y-%m-%d)/ml_audit.sql.gz

# Backup circuit_runtime
docker exec circuitos-db pg_dump -U circuitos circuit_runtime | gzip > ./backups/$(date +%Y-%m-%d)/circuit_runtime.sql.gz
```

### RAG-Specific Backup (Just Vector Data)
```bash
# Export only RAG tables
docker exec circuitos-db pg_dump -U circuitos agentforce \
  -t rag_documents \
  -t rag_chunks \
  -t rag_feedback \
  | gzip > ./backups/$(date +%Y-%m-%d)/rag-only.sql.gz
```

## Restore from Backup:

### Restore Full Database
```bash
# Stop services first
docker compose stop metroflex-ai

# Restore
gunzip -c ./backups/2025-01-15/agentforce.sql.gz | \
  docker exec -i circuitos-db psql -U circuitos agentforce

# Restart services
docker compose up -d metroflex-ai
```

### Restore Specific Table
```bash
# Drop existing table
docker exec circuitos-db psql -U circuitos agentforce -c "DROP TABLE IF EXISTS rag_chunks CASCADE;"

# Restore from backup
gunzip -c ./backups/2025-01-15/rag-only.sql.gz | \
  docker exec -i circuitos-db psql -U circuitos agentforce
```

## Verify Backup Integrity:

```bash
# Check backup file is not corrupted
gunzip -t ./backups/$(date +%Y-%m-%d)/agentforce.sql.gz && echo "✅ Backup is valid"

# Check backup size (should be >1MB for real data)
du -h ./backups/$(date +%Y-%m-%d)/*.gz

# Verify table counts match
docker exec circuitos-db psql -U circuitos agentforce -c "
SELECT
  'rag_documents' as table,
  COUNT(*) as count
FROM rag_documents
UNION ALL
SELECT
  'rag_chunks' as table,
  COUNT(*) as count
FROM rag_chunks
UNION ALL
SELECT
  'rag_feedback' as table,
  COUNT(*) as count
FROM rag_feedback;
"
```

## Backup to Cloud (S3/Backblaze):

### Setup (One-Time)
```bash
# Install AWS CLI
pip install awscli

# Configure credentials
aws configure set aws_access_key_id YOUR_KEY
aws configure set aws_secret_access_key YOUR_SECRET
aws configure set default.region us-east-1
```

### Upload Backup
```bash
# Compress and upload
tar -czf - ./backups/$(date +%Y-%m-%d) | \
  aws s3 cp - s3://circuit-os-backups/$(date +%Y-%m-%d).tar.gz

# Verify upload
aws s3 ls s3://circuit-os-backups/
```

### Automated Cloud Backup (Add to Cron)
```bash
# Add to crontab
0 3 * * * /home/user/Circuitos/scripts/backup-to-cloud.sh
```

## Disaster Recovery Checklist:

1. [ ] Backup exists and is recent (<24 hours)
2. [ ] Backup file is not corrupted (gunzip -t passes)
3. [ ] Backup is uploaded to cloud storage
4. [ ] Recovery procedure has been tested
5. [ ] Team knows how to access backups
6. [ ] Backups are encrypted (if containing sensitive data)

## Backup Best Practices:

- **3-2-1 Rule**: 3 copies, 2 different media, 1 offsite
- Test restores monthly (last Friday)
- Monitor backup service health in Grafana
- Alert if backup hasn't run in 36 hours
- Encrypt backups before uploading to cloud
- Document restore procedure for team
