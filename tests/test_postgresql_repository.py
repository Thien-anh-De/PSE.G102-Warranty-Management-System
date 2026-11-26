
import hashlib
import uuid
import pytest

from datetime import date, datetime, timezone, timedelta

from src.warranty_core.database import get_connection

from src.warranty_core.postgresql_repository import (
    PostgreSQLRepository
)

from src.warranty_core.domain_models import (
    WarrantyTicket,
    SignedPartItem,
    StatusChangeLog
)

from src.warranty_core.enums import (
    TicketStatus,
    IntakeType
)


@pytest.mark.integration
def test_repository_connection():

    with get_connection() as conn:

        repo = PostgreSQLRepository(conn)

        result = repo.get_user(
            "NON_EXISTENT_USER_" + uuid.uuid4().hex
        )

        assert result is None


@pytest.mark.integration
def test_create_and_read_ticket():

    suffix = uuid.uuid4().hex[:8]

    admin_id = f"USR_TEST_{suffix}"
    customer_id = f"CUST_TEST_{suffix}"
    device_id = f"DEV_TEST_{suffix}"

    today = date.today()
    now = datetime.now(timezone.utc)

    with get_connection() as conn:

        try:

            # Temporary test user

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

            # Temporary customer

            conn.execute("""
                INSERT INTO customers (
                    customer_id,
                    full_name,
                    phone_number
                )
                VALUES (%s, %s, %s)
            """, (
                customer_id,
                "Test Customer",
                "0900000000"
            ))

            # Temporary device

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

            repo = PostgreSQLRepository(conn)

            # Generate ticket number

            sequence = repo.get_next_daily_ticket_number(
                today
            )

            ticket_id = (
                f"TKT_{today:%Y%m%d}_{sequence}"
            )

            # Create domain model

            ticket = WarrantyTicket(
                ticket_id=ticket_id,
                customer_id=customer_id,
                device_id=device_id,
                intake_type=IntakeType.HOLD_FOR_REPAIR,
                promised_return_date=today + timedelta(days=3),
                reported_issue="RAM failure",
                initial_condition="Normal appearance",
                accessories_included="Charger",
                status=TicketStatus.RECEIVED,
                tracking_code_hash=hashlib.sha256(
                    b"TEST_SECRET"
                ).hexdigest(),
                created_at=now,
                customer_intake_signature_confirmed=True,
                signed_parts=[
                    SignedPartItem(
                        part_name="RAM 8GB",
                        signature_mark="SIGN_TEST_01"
                    )
                ]
            )

            ticket.status_history.append(
                StatusChangeLog(
                    log_id=str(uuid.uuid4()),
                    ticket_id=ticket_id,
                    from_status=None,
                    to_status=TicketStatus.RECEIVED,
                    changed_by_user_id=admin_id,
                    changed_at=now,
                    reason="Test ticket creation"
                )
            )

            # Save to PostgreSQL

            repo.save_new_ticket(ticket, admin_id)

            # Read from PostgreSQL

            saved_ticket = repo.find_ticket_by_id(
                ticket_id
            )

            assert saved_ticket is not None

            assert saved_ticket.ticket_id == ticket_id

            assert saved_ticket.status == (
                TicketStatus.RECEIVED
            )

            assert saved_ticket.customer_id == customer_id

            assert len(saved_ticket.signed_parts) == 1

            assert len(saved_ticket.status_history) == 1

            assert saved_ticket.signed_parts[0].part_name == (
                "RAM 8GB"
            )

        finally:

            # Remove all temporary test data

            conn.rollback()

    # Verify test data has been rolled back

    with get_connection() as conn:

        repo = PostgreSQLRepository(conn)

        assert repo.find_ticket_by_id(ticket_id) is None
        assert repo.get_user(admin_id) is None
