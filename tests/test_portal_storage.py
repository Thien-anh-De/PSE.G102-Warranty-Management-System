import sys

from fastapi.testclient import TestClient
from psycopg import OperationalError

from src.warranty_app import dependencies, demo
from src.warranty_app.main import app


def test_database_unavailable_returns_private_retryable_response(monkeypatch):
    monkeypatch.setenv("WARRANTY_STORAGE", "postgresql")

    def unavailable_connection():
        raise OperationalError("PRIVATE_DATABASE_HOST_AND_CREDENTIAL_DETAILS")

    monkeypatch.setattr(dependencies, "get_connection", unavailable_connection)
    dependencies.reset_container()
    try:
        with TestClient(app) as client:
            response = client.post("/api/v1/portal/lookups", json={
                "ticket_id": "TKT_20261126_1", "plain_secret_code": "PRIVATE_SECRET",
            })
        assert response.status_code == 503
        assert response.headers["cache-control"] == "no-store"
        assert "PRIVATE_DATABASE" not in response.text
        assert "PRIVATE_SECRET" not in response.text
    finally:
        dependencies.reset_container()


def test_explicit_ram_demo_works_when_normal_api_uses_postgresql(monkeypatch, tmp_path):
    import uvicorn
    import src.warranty_app.main as application

    monkeypatch.setenv("WARRANTY_STORAGE", "postgresql")
    monkeypatch.setattr(application, "frontend_directory", tmp_path)
    monkeypatch.setattr(sys, "argv", ["demo", "--port", "3000"])

    def check_demo_application(application, **kwargs):
        with TestClient(application) as client:
            response = client.post("/api/v1/portal/lookups", json={
                "ticket_id": "TKT_20261126_1", "plain_secret_code": "HT-DEMO-001",
            })
        assert response.status_code == 200
        assert response.json()["status"] == "UNDER_REPAIR"

    monkeypatch.setattr(uvicorn, "run", check_demo_application)
    dependencies.reset_container()
    try:
        demo.main()
    finally:
        dependencies.reset_container()
