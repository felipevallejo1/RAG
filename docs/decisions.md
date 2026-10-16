# Design decisions

Short records of the decisions that shape the project. Newest at the bottom.

## 1. Langfuse v3 (self-hosted)
**Decision:** run Langfuse v3 with its full dependency set (Postgres, ClickHouse, Redis, MinIO).
**Why:** v3 is the maintained version. v2 needs only Postgres but is in maintenance mode.
**Trade-off:** ~8 containers and 4–6 GB of RAM instead of ~2 containers.

## 2. One Postgres server, two databases
**Decision:** a single `pgvector/pgvector` instance hosts `langfuse` and `qa_app`
(created by `infra/postgres/init-databases.sh`).
**Why:** fewer containers; Postgres also serves as the vector store, so the RAG needs no extra service.

## 3. LiteLLM as the only LLM gateway
**Decision:** the backend only knows the aliases `qa-llm` and `qa-embeddings`; the provider is chosen in
`infra/litellm/config.yaml`.
**Why:** switching provider (OpenAI → Anthropic → Ollama) is a config change, not a code change.
**Default:** OpenAI, because one API key covers chat and embeddings.

## 4. Compose layout
**Decision:** the stack lives in `infra/docker-compose.yml`; the root `docker-compose.yml` only
`include`s it and passes `.env`, so `docker compose up` works from the repo root.

## 5. `/health` reports dependencies but never fails
**Decision:** `/health` returns 200 with `status: "degraded"` when a dependency is down.
**Why:** it works as a liveness probe (no restart loop from an upstream outage) and as a quick
diagnostic for the demo.
