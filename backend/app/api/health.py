from typing import Annotated, Literal

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.core.checks import DependencyStatus, run_dependency_checks
from app.core.config import Settings, get_settings

router = APIRouter(tags=["health"])


class HealthResponse(BaseModel):
    status: Literal["ok", "degraded"]
    version: str
    dependencies: dict[str, DependencyStatus]


@router.get("/health", response_model=HealthResponse)
async def health(settings: Annotated[Settings, Depends(get_settings)]) -> HealthResponse:
    """Liveness plus dependency status.

    Always answers 200 while the API process is up; `status` is "degraded" when a
    dependency is unreachable, so container restarts are not triggered by an
    upstream outage.
    """
    dependencies = await run_dependency_checks(settings)
    all_ok = all(dep.status == "ok" for dep in dependencies.values())
    return HealthResponse(
        status="ok" if all_ok else "degraded",
        version=settings.app_version,
        dependencies=dependencies,
    )
