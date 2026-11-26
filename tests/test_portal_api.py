from datetime import date, datetime, timezone

import pytest
from fastapi.testclient import TestClient

from src.warranty_app import dependencies
from src.warranty_app.demo import seed_portal_demo_data
from src.warranty_app.main import app
from src.warranty_app.portal_rate_limiter import PortalRateLimiter
from src.warranty_core import DefectOrigin, WarrantyService


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setenv("WARRANTY_STORAGE", "memory")
    monkeypatch.setenv("PORTAL_LOOKUP_MAX_ATTEMPTS", "5")
    monkeypatch.setenv("PORTAL_LOOKUP_WINDOW_SECONDS", "60")
    container = dependencies.reset_container()
    container.clock_service.set_time(datetime(2026, 11, 26, 3, 0, tzinfo=timezone.utc))
    with TestClient(app) as test_client:
        yield test_client
    dependencies.reset_container()


@pytest.fixture
def created_ticket(client):
    response = client.post("/api/v1/tickets", json={
        "admin_user_id": "USR_ADMIN_01", "customer_id": "CUST_001", "device_id": "DEV_001",
        "intake_type": "HOLD_FOR_REPAIR", "promised_return_date": "2026-11-28",
        "reported_issue": "INTERNAL_PRIVATE_ISSUE", "initial_condition": "INTERNAL_CONDITION",
        "accessories_included": "Adapter", "plain_secret_code": "PORTAL_TEST_SECRET",
        "signed_parts": [{"part_name": "RAM", "signature_mark": "PRIVATE_SIGNATURE"}],
        "customer_signature_confirmed": True,
    })
    assert response.status_code == 201
    return response.json()["ticket_id"]


def lookup(client, ticket_id, secret="PORTAL_TEST_SECRET", **kwargs):
    return client.post("/api/v1/portal/lookups", json={
        "ticket_id": ticket_id, "plain_secret_code": secret,
    }, **kwargs)


def test_intake_to_public_lookup_shares_data_and_filters_internal_fields(client, created_ticket):
    response = lookup(client, created_ticket)
    assert response.status_code == 200
    assert response.json() == {
        "ticket_id": created_ticket, "device_model": "Dell XPS 15 9520",
        "device_serial_masked": "SN****00", "status": "RECEIVED",
        "promised_return_date": "2026-11-28",
    }
    assert "PORTAL_TEST_SECRET" not in response.text
    assert "INTERNAL_PRIVATE_ISSUE" not in response.text
    assert "PRIVATE_SIGNATURE" not in response.text
    assert response.headers["cache-control"] == "no-store"
    assert response.headers["x-content-type-options"] == "nosniff"


def test_unknown_ticket_and_wrong_code_have_identical_responses(client, created_ticket):
    wrong_code = lookup(client, created_ticket, "WRONG_SECRET")
    unknown_ticket = lookup(client, "TKT_20261126_999")
    assert wrong_code.status_code == unknown_ticket.status_code == 404
    assert wrong_code.json() == unknown_ticket.json()
    assert wrong_code.headers["cache-control"] == "no-store"


def test_secret_from_another_ticket_cannot_read_target_ticket(client, created_ticket):
    assert lookup(client, created_ticket, "OTHER_TICKET_SECRET").status_code == 404


def test_lookup_reads_current_status_after_domain_update(client, created_ticket):
    container = dependencies.container
    assert lookup(client, created_ticket).json()["status"] == "RECEIVED"
    service = WarrantyService(container.repository, container.clock_service)
    service.evaluate_and_record_policy(
        admin_user_id="USR_ADMIN_01", ticket_id=created_ticket,
        purchase_date=date(2026, 10, 1), incident_date=date(2026, 11, 26),
        is_warranty_valid=True, defect_origin=DefectOrigin.MANUFACTURER, customer_agreed=True,
    )
    assert lookup(client, created_ticket).json()["status"] == "PENDING_ASSIGNMENT"


@pytest.mark.parametrize("payload", [
    {},
    {"ticket_id": " ", "plain_secret_code": "PRIVATE_INPUT"},
    {"ticket_id": "TKT_20261126_1", "plain_secret_code": " "},
    {"ticket_id": "TKT_20261126_1", "plain_secret_code": {"private": "PRIVATE_INPUT"}},
    {"ticket_id": "TKT_20261126_1", "plain_secret_code": "PRIVATE_INPUT" * 30},
    {"ticket_id": "TKT_20261126_1", "plain_secret_code": "PRIVATE_INPUT", "unexpected": True},
])
def test_validation_errors_do_not_echo_submitted_secret(client, payload):
    response = client.post("/api/v1/portal/lookups", json=payload)
    assert response.status_code == 422
    assert set(response.json()) == {"detail"}
    assert "PRIVATE_INPUT" not in response.text
    assert "plain_secret_code" not in response.text
    assert response.headers["cache-control"] == "no-store"


def test_malformed_json_is_sanitized(client):
    response = client.post("/api/v1/portal/lookups", content='{"plain_secret_code":"PRIVATE_INPUT"', headers={"Content-Type": "application/json"})
    assert response.status_code == 422
    assert "PRIVATE_INPUT" not in response.text


def test_rate_limit_blocks_and_expires_without_waiting(client, created_ticket):
    now = [0.0]
    dependencies.container.portal_rate_limiter = PortalRateLimiter(2, 60, clock=lambda: now[0])
    assert lookup(client, created_ticket).status_code == 200
    assert lookup(client, created_ticket, "WRONG_SECRET").status_code == 404
    blocked = lookup(client, created_ticket)
    assert blocked.status_code == 429
    assert blocked.headers["retry-after"] == "60"
    assert blocked.headers["cache-control"] == "no-store"
    now[0] = 60.0
    assert lookup(client, created_ticket).status_code == 200


def test_forwarded_header_cannot_bypass_per_client_limit(client, created_ticket):
    dependencies.container.portal_rate_limiter = PortalRateLimiter(1, 60)
    assert lookup(client, created_ticket, headers={"X-Forwarded-For": "198.51.100.10"}).status_code == 200
    assert lookup(client, created_ticket, headers={"X-Forwarded-For": "198.51.100.20"}).status_code == 429


def test_whitespace_around_ticket_is_normalized_but_secret_is_exact(client, created_ticket):
    assert lookup(client, f"  {created_ticket}  ").status_code == 200
    assert lookup(client, created_ticket, " PORTAL_TEST_SECRET ").status_code == 404


def test_demo_data_is_opt_in_and_follows_domain_workflows(client):
    assert not dependencies.container.repository.tickets
    samples = seed_portal_demo_data(dependencies.container)
    assert [state for _, _, state in samples] == ["UNDER_REPAIR", "WAITING_FOR_PARTS", "WAITING_FOR_RETURN", "CANCELLED"]
    for ticket_id, secret, expected_state in samples:
        response = lookup(client, ticket_id, secret)
        assert response.status_code == 200
        assert response.json()["status"] == expected_state
    with pytest.raises(ValueError):
        seed_portal_demo_data(dependencies.container)
