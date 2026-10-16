# QA AI Assistants Platform

AI assistants for QA teams: paste a user story, a team of agents (Analyst → Writer → Reviewer)
turns it into structured test cases, consulting a RAG over testing documentation. Approved cases
are published to a (mock) test-management system. Every step is traced in Langfuse.

> Work in progress: this README is expanded in the final phase (architecture diagram, screenshots,
> design decisions). Current status: **Phase 1 – infrastructure skeleton**.

## Stack

FastAPI · LangGraph/LangChain · LiteLLM proxy · Langfuse v3 (self-hosted) · Postgres + pgvector ·
React/Vite/TypeScript · Docker Compose

## Quick start

```bash
cp .env.example .env     # then set GEMINI_API_KEY
docker compose up -d --build
```

| Service  | URL                          | Notes                                              |
| -------- | ---------------------------- | -------------------------------------------------- |
| Backend  | http://localhost:8000/health | Liveness + status of Postgres, LiteLLM and Langfuse |
| API docs | http://localhost:8000/docs   | Swagger UI                                         |
| LiteLLM  | http://localhost:4000        | Model gateway (aliases `qa-llm`, `qa-embeddings`)   |
| Langfuse | http://localhost:3000        | Login with `LANGFUSE_INIT_USER_*` from `.env`       |

The first start takes a few minutes: Langfuse v3 runs ClickHouse, Redis and MinIO next to Postgres
(plan for ~4–6 GB of RAM). Langfuse's project and API keys are provisioned automatically from `.env`.

## Development

```bash
make test    # backend tests (uses uv)
make lint
make logs s=backend
```

See [docs/decisions.md](docs/decisions.md) for the technical decisions made so far.
