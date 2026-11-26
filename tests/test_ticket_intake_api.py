from datetime import datetime, timezone

import pytest
from fastapi.testclient import TestClient

from src.warranty_app.dependencies import container, reset_container
from src.warranty_app.main import app


@pytest.fixture(autouse=True)
def reset_app_container():
    app_container = reset_container()
    app_container.clock_service.set_time(datetime(2026, 11, 24, 8, 0, 0, tzinfo=timezone.utc))
    yield
    reset_container()


@pytest.fixture
def client():
    return TestClient(app)


def valid_hold_payload():
    return {
        "admin_user_id": "USR_ADMIN_01",
        "customer_id": "CUST_001",
        "device_id": "DEV_001",
        "intake_type": "HOLD_FOR_REPAIR",
        "promised_return_date": "2026-11-28",
        "reported_issue": "Blue screen error when rendering video",
        "initial_condition": "Minor scratches on bottom chassis",
        "accessories_included": "Power adapter 130W, protective sleeve",
        "plain_secret_code": "SEC_123456",
        "signed_parts": [
            {"part_name": "RAM DDR5 16GB", "signature_mark": "NVA_SIG_1", "notes": None},
            {"part_name": "SSD NVMe 512GB", "signature_mark": "NVA_SIG_2", "notes": None},
        ],
        "customer_signature_confirmed": True,
    }


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_create_ticket_hold_for_repair_success(client):
    response = client.post("/api/v1/tickets", json=valid_hold_payload())
    assert response.status_code == 201
    body = response.json()
    assert body["ticket_id"] == "TKT_20261124_1"
    assert body["status"] == "RECEIVED"
    assert body["intake_type"] == "HOLD_FOR_REPAIR"
    assert len(body["signed_parts"]) == 2
    assert body["customer_intake_signature_confirmed"] is True


def test_create_ticket_same_day_success(client):
    payload = valid_hold_payload()
    payload["intake_type"] = "SAME_DAY"
    payload["signed_parts"] = []
    payload["customer_signature_confirmed"] = False
    response = client.post("/api/v1/tickets", json=payload)
    assert response.status_code == 201
    assert response.json()["intake_type"] == "SAME_DAY"


def test_create_ticket_hold_for_repair_missing_signed_parts_rejected(client):
    payload = valid_hold_payload()
    payload["signed_parts"] = []
    response = client.post("/api/v1/tickets", json=payload)
    assert response.status_code == 400
    assert "requires inspection and signing of components" in response.json()["detail"]


def test_create_ticket_hold_for_repair_missing_signature_rejected(client):
    payload = valid_hold_payload()
    payload["customer_signature_confirmed"] = False
    response = client.post("/api/v1/tickets", json=payload)
    assert response.status_code == 400
    assert "requires verified customer signature" in response.json()["detail"]


def test_list_and_get_ticket(client):
    create_response = client.post("/api/v1/tickets", json=valid_hold_payload())
    assert create_response.status_code == 201
    ticket_id = create_response.json()["ticket_id"]

    list_response = client.get("/api/v1/tickets")
    assert list_response.status_code == 200
    assert list_response.json()["total"] == 1

    get_response = client.get(f"/api/v1/tickets/{ticket_id}")
    assert get_response.status_code == 200
    assert get_response.json()["ticket_id"] == ticket_id


def test_get_ticket_not_found(client):
    response = client.get("/api/v1/tickets/TKT_NOT_FOUND")
    assert response.status_code == 404