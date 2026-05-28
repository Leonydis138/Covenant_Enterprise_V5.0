"""Tests for FastAPI app health and request protections."""
from fastapi.testclient import TestClient

from covenant import main as main_module


def test_health_endpoint_contains_operational_fields():
    client = TestClient(main_module.app)
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] in {"healthy", "degraded"}
    assert "uptime_seconds" in body
    assert isinstance(body["uptime_seconds"], int)
    assert "checks" in body
    assert "database" in body["checks"]


def test_rate_limiter_blocks_excess_requests():
    previous_enabled = main_module.settings.RATE_LIMIT_ENABLED
    previous_max = main_module.settings.RATE_LIMIT_MAX_REQUESTS
    previous_window = main_module.settings.RATE_LIMIT_WINDOW_SECONDS
    main_module.settings.RATE_LIMIT_ENABLED = True
    main_module.settings.RATE_LIMIT_MAX_REQUESTS = 2
    main_module.settings.RATE_LIMIT_WINDOW_SECONDS = 60
    main_module.rate_limit_store.clear()

    try:
        client = TestClient(main_module.app)
        assert client.get("/").status_code == 200
        assert client.get("/").status_code == 200
        blocked = client.get("/")
        assert blocked.status_code == 429
        assert blocked.json()["type"] == "rate_limit_exceeded"
    finally:
        main_module.rate_limit_store.clear()
        main_module.settings.RATE_LIMIT_ENABLED = previous_enabled
        main_module.settings.RATE_LIMIT_MAX_REQUESTS = previous_max
        main_module.settings.RATE_LIMIT_WINDOW_SECONDS = previous_window
