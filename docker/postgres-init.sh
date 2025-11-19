#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    CREATE DATABASE agentforce;
    CREATE DATABASE ml_audit;
    CREATE DATABASE circuit_runtime;
    CREATE DATABASE metroflex_events;
    CREATE DATABASE metroflex_gym;

    GRANT ALL PRIVILEGES ON DATABASE agentforce TO $POSTGRES_USER;
    GRANT ALL PRIVILEGES ON DATABASE ml_audit TO $POSTGRES_USER;
    GRANT ALL PRIVILEGES ON DATABASE circuit_runtime TO $POSTGRES_USER;
    GRANT ALL PRIVILEGES ON DATABASE metroflex_events TO $POSTGRES_USER;
    GRANT ALL PRIVILEGES ON DATABASE metroflex_gym TO $POSTGRES_USER;
EOSQL

echo "✅ Databases created: agentforce, ml_audit, circuit_runtime, metroflex_events, metroflex_gym"

# Enable pgvector extension for RAG functionality in agentforce database
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "agentforce" <<-EOSQL
    CREATE EXTENSION IF NOT EXISTS vector;
EOSQL

echo "✅ pgvector extension enabled in agentforce database"
