import pytest
from fastapi.testclient import TestClient

from app.api import health
from app.core.checks import DependencyStatus
from app.main import app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def _patch_checks(monkeypatch: pytest.MonkeyPatch, **statuses: str) -> None:
    async def fake_checks(_settings):
        return {name: DependencyStatus(status=status) for name, status in statuses.items()}

    monkeypatch.setattr(health, "run_dependency_checks", fake_checks)


def test_health_ok_when_all_dependencies_up(client, monkeypatch):
    _patch_checks(monkeypatch, postgres="ok", litellm="ok", langfuse="ok")

    response = client.get("/health")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["dependencies"]["postgres"]["status"] == "ok"


def test_health_degraded_but_200_when_a_dependency_is_down(client, monkeypatch):
    _patch_checks(monkeypatch, postgres="ok", litellm="down", langfuse="ok")

    response = client.get("/health")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "degraded"
    assert body["dependencies"]["litellm"]["status"] == "down"
