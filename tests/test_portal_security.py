import pytest
from datetime import date
from src.warranty_core import (
    IntakeType,
    SignedPartItem,
    PortalServiceError
)

def test_portal_public_tracking_success_and_sanitization(
    ticket_service,
    portal_service
):
    signed_parts = [SignedPartItem(part_name="Screen", signature_mark="SIG")]
    ticket = ticket_service.create_ticket(
        admin_user_id="USR_ADMIN_01",
        customer_id="CUST_001",
        device_id="DEV_001",
        intake_type=IntakeType.HOLD_FOR_REPAIR,
        promised_return_date=date(2026, 11, 28),
        reported_issue="Screen flickering",
        initial_condition="Good",
        accessories_included="Charger",
        plain_secret_code="SECRET_KEY_7788",
        signed_parts=signed_parts,
        customer_signature_confirmed=True
    )

    public_data = portal_service.lookup_ticket_public_status(
        ticket_id=ticket.ticket_id,
        plain_secret_code="SECRET_KEY_7788"
    )
    assert public_data["ticket_id"] == ticket.ticket_id
    assert public_data["status"] == "RECEIVED"
    assert public_data["device_model"] == "Dell XPS 15 9520"
    assert public_data["device_serial_masked"] == "SN****00"
    assert "work_logs" not in public_data
    assert "phone_number" not in public_data

def test_portal_wrong_secret_code_rejected(ticket_service, portal_service):
    signed_parts = [SignedPartItem(part_name="Screen", signature_mark="SIG")]
    ticket = ticket_service.create_ticket(
        admin_user_id="USR_ADMIN_01",
        customer_id="CUST_001",
        device_id="DEV_001",
        intake_type=IntakeType.HOLD_FOR_REPAIR,
        promised_return_date=date(2026, 11, 28),
        reported_issue="Screen flickering",
        initial_condition="Good",
        accessories_included="Charger",
        plain_secret_code="CORRECT_CODE",
        signed_parts=signed_parts,
        customer_signature_confirmed=True
    )

    with pytest.raises(PortalServiceError) as exc:
        portal_service.lookup_ticket_public_status(
            ticket_id=ticket.ticket_id,
            plain_secret_code="WRONG_CODE"
        )
    assert "Verification failed" in str(exc.value)
