"""Exercise the customer portal against the real schema from the DB module."""

import hashlib
import uuid
from datetime import date, timedelta

import pytest
from fastapi.testclient import TestClient

from src.warranty_app import dependencies
from src.warranty_app.main import app
from src.warranty_core import TicketStatus
from src.warranty_core.database import get_connection


pytestmark = pytest.mark.integration


@pytest.fixture
def postgres_portal(monkeypatch):
    monkeypatch.setenv("WARRANTY_STORAGE", "postgresql")
    monkeypatch.setenv("PORTAL_LOOKUP_MAX_ATTEMPTS", "100")
    suffix = uuid.uuid4().hex[:12]
    admin_id = f"USR_PORTAL_{suffix}"
    customer_id = f"CUST_PORTAL_{suffix}"
    device_id = f"DEV_PORTAL_{suffix}"
    secret = f"PORTAL_SQL_{suffix}"
    dependencies.reset_container()

    with get_connection() as connection:
        connection.execute(
            """INSERT INTO users (user_id, username, password_hash, full_name, role)
               VALUES (%s, %s, %s, %s, 'ADMIN')""",
            (admin_id, f"portal_test_{suffix}", "fictional_test_hash", "Portal Test Admin"),
        )
        connection.execute(
            """INSERT INTO customers (customer_id, full_name, phone_number)
               VALUES (%s, %s, %s)""",
            (customer_id, "Portal Test Customer", "0901234567"),
        )
        connection.execute(
            """INSERT INTO devices (device_id, serial_number, model_name, brand)
               VALUES (%s, %s, %s, %s)""",
            (device_id, f"SN-PRIVATE-{suffix}-9900", "Portal SQL Test Laptop", "Demo"),
        )

    payload = {
        "admin_user_id": admin_id, "customer_id": customer_id, "device_id": device_id,
        "intake_type": "HOLD_FOR_REPAIR",
        "promised_return_date": (date.today() + timedelta(days=3)).isoformat(),
        "reported_issue": "PRIVATE_INTERNAL_ISSUE", "initial_condition": "PRIVATE_CONDITION",
        "accessories_included": "Test charger", "plain_secret_code": secret,
        "signed_parts": [{"part_name": "RAM", "signature_mark": "PRIVATE_SIGNATURE"}],
        "customer_signature_confirmed": True,
    }
    try:
        with TestClient(app) as client:
            yield client, payload
    finally:
        # Only remove this test's uniquely identified rows; never truncate tables.
        with get_connection() as connection:
            for table in ("ticket_status_history", "signed_components"):
                connection.execute(
                    f"""DELETE FROM {table} WHERE ticket_id IN
                        (SELECT ticket_id FROM warranty_tickets WHERE customer_id = %s)""",
                    (customer_id,),
                )
            connection.execute("DELETE FROM warranty_tickets WHERE customer_id = %s", (customer_id,))
            connection.execute("DELETE FROM devices WHERE device_id = %s", (device_id,))
            connection.execute("DELETE FROM customers WHERE customer_id = %s", (customer_id,))
            connection.execute("DELETE FROM users WHERE user_id = %s", (admin_id,))
        dependencies.reset_container()


def create_ticket(client, payload):
    response = client.post("/api/v1/tickets", json=payload)
    assert response.status_code == 201, response.text
    return response.json()["ticket_id"]


def lookup(client, ticket_id, secret):
    return client.post("/api/v1/portal/lookups", json={
        "ticket_id": ticket_id, "plain_secret_code": secret,
    })


def test_postgresql_intake_to_portal_persists_and_filters_private_data(postgres_portal):
    client, payload = postgres_portal
    ticket_id = create_ticket(client, payload)
    response = lookup(client, ticket_id, payload["plain_secret_code"])
    assert response.status_code == 200
    expected = {
        "ticket_id": ticket_id, "device_model": "Portal SQL Test Laptop",
        "device_serial_masked": "SN****00", "status": "RECEIVED",
        "promised_return_date": payload["promised_return_date"],
    }
    assert response.json() == expected
    assert response.headers["cache-control"] == "no-store"
    for private_value in (
        payload["plain_secret_code"], payload["reported_issue"], "PRIVATE_SIGNATURE", "0901234567",
    ):
        assert private_value not in response.text
    assert ticket_id not in dependencies.container.repository.tickets

    # A new connection sees the committed record and a hash, never the plain code.
    with get_connection() as connection:
        saved = connection.execute(
            "SELECT tracking_code_hash FROM warranty_tickets WHERE ticket_id = %s", (ticket_id,),
        ).fetchone()
    assert saved["tracking_code_hash"] == hashlib.sha256(payload["plain_secret_code"].encode()).hexdigest()

    # Rebuild the in-memory container and open another client/DB connection.
    dependencies.reset_container()
    with TestClient(app) as restarted_client:
        repeated = lookup(restarted_client, ticket_id, payload["plain_secret_code"])
    assert repeated.status_code == 200
    assert repeated.json() == expected


def test_postgresql_wrong_code_and_missing_ticket_are_indistinguishable(postgres_portal):
    client, payload = postgres_portal
    ticket_id = create_ticket(client, payload)
    wrong = lookup(client, ticket_id, "WRONG_SQL_SECRET")
    missing = lookup(client, "TKT_19000101_999999", payload["plain_secret_code"])
    assert wrong.status_code == missing.status_code == 404
    assert wrong.json() == missing.json()
    assert wrong.headers["cache-control"] == missing.headers["cache-control"] == "no-store"


def test_postgresql_device_without_serial_still_has_a_public_result(postgres_portal):
    client, payload = postgres_portal
    ticket_id = create_ticket(client, payload)
    with get_connection() as connection:
        connection.execute("UPDATE devices SET serial_number = NULL WHERE device_id = %s", (payload["device_id"],))
    response = lookup(client, ticket_id, payload["plain_secret_code"])
    assert response.status_code == 200
    assert response.json()["device_serial_masked"] == "****"


@pytest.mark.parametrize("status", list(TicketStatus))
def test_postgresql_portal_reads_the_latest_saved_status(postgres_portal, status):
    client, payload = postgres_portal
    ticket_id = create_ticket(client, payload)
    assert lookup(client, ticket_id, payload["plain_secret_code"]).json()["status"] == "RECEIVED"

    # Arrange a persisted state; this test covers reading it, not the repair workflow.
    with get_connection() as connection:
        connection.execute(
            """UPDATE warranty_tickets SET status = %s, final_return_confirmed = %s
               WHERE ticket_id = %s""",
            (status.value, status == TicketStatus.RETURNED, ticket_id),
        )

    response = lookup(client, ticket_id, payload["plain_secret_code"])
    assert response.status_code == 200
    assert response.json()["status"] == status.value
