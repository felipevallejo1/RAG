from fastapi import FastAPI

from app.api import health
from app.core.config import get_settings


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title="QA AI Assistants Platform",
        version=settings.app_version,
        description="LangGraph agents that turn user stories into structured test cases.",
    )
    app.include_router(health.router)
    return app


app = create_app()
