"""Connectivity checks for the services the backend depends on."""

import asyncio
from typing import Literal

import httpx
import psycopg
from pydantic import BaseModel

from app.core.config import Settings

CHECK_TIMEOUT_SECONDS = 3.0


class DependencyStatus(BaseModel):
    status: Literal["ok", "down"]
    detail: str | None = None


async def _check_postgres(settings: Settings) -> DependencyStatus:
    try:
        conn = await psycopg.AsyncConnection.connect(
            settings.database_url, connect_timeout=int(CHECK_TIMEOUT_SECONDS)
        )
        async with conn:
            await conn.execute("SELECT 1")
        return DependencyStatus(status="ok")
    except Exception as exc:
        return DependencyStatus(status="down", detail=str(exc))


async def _check_http(url: str) -> DependencyStatus:
    try:
        async with httpx.AsyncClient(timeout=CHECK_TIMEOUT_SECONDS) as client:
            response = await client.get(url)
            response.raise_for_status()
        return DependencyStatus(status="ok")
    except Exception as exc:
        return DependencyStatus(status="down", detail=str(exc))


async def run_dependency_checks(settings: Settings) -> dict[str, DependencyStatus]:
    """Check Postgres, the LiteLLM proxy and Langfuse concurrently."""
    postgres, litellm, langfuse = await asyncio.gather(
        _check_postgres(settings),
        _check_http(f"{settings.litellm_base_url}/health/liveliness"),
        _check_http(f"{settings.langfuse_host}/api/public/health"),
    )
    return {"postgres": postgres, "litellm": litellm, "langfuse": langfuse}
