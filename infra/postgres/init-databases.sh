#!/bin/sh
# Runs once, on first start of an empty Postgres volume.
# One server, two databases: `langfuse` (owned by Langfuse) and `qa_app` (our app + pgvector).
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE langfuse;
    CREATE DATABASE qa_app;
EOSQL

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname qa_app \
    -c "CREATE EXTENSION IF NOT EXISTS vector;"
