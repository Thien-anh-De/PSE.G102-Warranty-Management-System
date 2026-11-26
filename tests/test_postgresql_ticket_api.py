
import uuid
import pytest

from contextlib import contextmanager
from datetime import date, timedelta

from fastapi.testclient import TestClient

from src.warranty_app.main import app
from src.warranty_app import dependencies

from src.warranty_core.database import get_connection

from src.warranty_core.services.postgresql_ticket_service import (
    PostgreSQLTicketService
)


@pytest.mark.integration
def test_postgresql_ticket_api(monkeypatch):

    suffix = uuid.uuid4().hex[:8]

    admin_id = f"USR_TEST_{suffix}"
    customer_id = f"CUST_TEST_{suffix}"
    device_id = f"DEV_TEST_{suffix}"

    with get_connection() as conn:

        try:

            # Temporary test data

            conn.execute("""
                INSERT INTO users (
                    user_id,
                    username,
                    password_hash,
                    full_name,
                    role
                )
                VALUES (%s, %s, %s, %s, 'ADMIN')
            """, (
                admin_id,
                f"admin_test_{suffix}",
                "test_placeholder",
                "Test Admin"
            ))

            conn.execute("""
                INSERT INTO customers (
                    customer_id,
                    full_name,
                    phone_number
                )
                VALUES (%s, %s, %s)
            """, (
                customer_id,
                f"Test Customer {suffix}",
                "0900000000"
            ))

            conn.execute("""
                INSERT INTO devices (
                    device_id,
                    serial_number,
                    model_name,
                    brand
                )
                VALUES (%s, %s, %s, %s)
            """, (
                device_id,
                f"SN_TEST_{suffix}",
                "Test Laptop",
                "Dell"
            ))

            # Reuse the test transaction

            @contextmanager
            def test_connection():
                yield conn

            service = PostgreSQLTicketService(
                connection_factory=test_connection
            )

            monkeypatch.setenv(
                "WARRANTY_STORAGE",
                "postgresql"
            )

            monkeypatch.setattr(
                dependencies,
                "PostgreSQLTicketService",
                lambda: service
            )

            client = TestClient(app)

            payload = {
                "admin_user_id": admin_id,
                "customer_id": customer_id,
                "device_id": device_id,
                "intake_type": "HOLD_FOR_REPAIR",
                "promised_return_date": (
                    date.today() + timedelta(days=3)
                ).isoformat(),
                "reported_issue": "RAM failure",
                "initial_condition": "Normal appearance",
                "accessories_included": "Charger",
                "plain_secret_code": "TEST_SECRET_01",
                "signed_parts": [
                    {
                        "part_name": "RAM 8GB",
                        "signature_mark": "SIGN_01"
                    }
                ],
                "customer_signature_confirmed": True
            }

            # Test POST API

            response = client.post(
                "/api/v1/tickets",
                json=payload
            )

            assert response.status_code == 201

            ticket_id = response.json()["ticket_id"]

            # Verify PostgreSQL directly

            row = conn.execute("""
                SELECT ticket_id, status
                FROM warranty_tickets
                WHERE ticket_id = %s
            """, (ticket_id,)).fetchone()

            assert row is not None
            assert row["status"] == "RECEIVED"

            # Test GET API

            response = client.get(
                f"/api/v1/tickets/{ticket_id}"
            )

            assert response.status_code == 200

            assert response.json()["ticket_id"] == ticket_id

            assert len(
                response.json()["signed_parts"]
            ) == 1

            # Test search API

            response = client.get(
                "/api/v1/tickets",
                params={
                    "contact_query": f"Test Customer {suffix}"
                }
            )

            assert response.status_code == 200

            assert response.json()["total"] == 1

        finally:

            conn.rollback()
