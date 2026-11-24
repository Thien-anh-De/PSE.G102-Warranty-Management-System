import pytest
from datetime import date
from src.warranty_core import (
    IntakeType,
    TicketStatus,
    SignedPartItem,
    TicketServiceError
)

def test_create_ticket_hold_for_repair_success(ticket_service, repo, clock):
    signed_parts = [
        SignedPartItem(part_name="RAM DDR5 16GB", signature_mark="NVA_SIG_1"),
        SignedPartItem(part_name="SSD NVMe 512GB", signature_mark="NVA_SIG_2")
    ]
    ticket = ticket_service.create_ticket(
        admin_user_id="USR_ADMIN_01",
        customer_id="CUST_001",
        device_id="DEV_001",
        intake_type=IntakeType.HOLD_FOR_REPAIR,
        promised_return_date=date(2026, 11, 28),
        reported_issue="Blue screen error when rendering video",
        initial_condition="Minor scratches on bottom chassis",
        accessories_included="Power adapter 130W, protective sleeve",
        plain_secret_code="SEC_123456",
        signed_parts=signed_parts,
        customer_signature_confirmed=True
    )
    assert ticket.ticket_id == "TKT_20261124_1"
    assert ticket.status == TicketStatus.RECEIVED
    assert len(ticket.signed_parts) == 2
    assert ticket.customer_intake_signature_confirmed is True
    assert len(ticket.status_history) == 1
    assert repo.find_ticket_by_id("TKT_20261124_1") is not None

def test_create_ticket_missing_signed_parts_rejected(ticket_service):
    with pytest.raises(TicketServiceError) as exc:
        ticket_service.create_ticket(
            admin_user_id="USR_ADMIN_01",
            customer_id="CUST_001",
            device_id="DEV_001",
            intake_type=IntakeType.HOLD_FOR_REPAIR,
            promised_return_date=date(2026, 11, 28),
            reported_issue="Motherboard short circuit",
            initial_condition="Used",
            accessories_included="None",
            plain_secret_code="SEC_123456",
            signed_parts=[],
            customer_signature_confirmed=True
        )
    assert "requires inspection and signing of components" in str(exc.value)

def test_create_ticket_missing_customer_signature_confirmation_rejected(ticket_service):
    signed_parts = [SignedPartItem(part_name="Screen", signature_mark="SIG")]
    with pytest.raises(TicketServiceError) as exc:
        ticket_service.create_ticket(
            admin_user_id="USR_ADMIN_01",
            customer_id="CUST_001",
            device_id="DEV_001",
            intake_type=IntakeType.HOLD_FOR_REPAIR,
            promised_return_date=date(2026, 11, 28),
            reported_issue="Screen flickering",
            initial_condition="Good",
            accessories_included="Charger",
            plain_secret_code="SEC_123456",
            signed_parts=signed_parts,
            customer_signature_confirmed=False
        )
    assert "requires verified customer signature" in str(exc.value)

def test_finalize_return_success(ticket_service, repo):
    signed_parts = [SignedPartItem(part_name="Battery", signature_mark="SIG_BATT")]
    ticket = ticket_service.create_ticket(
        admin_user_id="USR_ADMIN_01",
        customer_id="CUST_001",
        device_id="DEV_001",
        intake_type=IntakeType.HOLD_FOR_REPAIR,
        promised_return_date=date(2026, 11, 28),
        reported_issue="Battery drains rapidly",
        initial_condition="Normal",
        accessories_included="Adapter",
        plain_secret_code="SEC_BATT_99",
        signed_parts=signed_parts,
        customer_signature_confirmed=True
    )
    ticket.status = TicketStatus.WAITING_FOR_RETURN

    returned_ticket = ticket_service.finalize_return(
        admin_user_id="USR_ADMIN_01",
        ticket_id=ticket.ticket_id,
        components_signature_verified=True,
        test_run_passed=True,
        customer_accepted=True
    )
    assert returned_ticket.status == TicketStatus.RETURNED
    assert returned_ticket.final_return_confirmed is True

def test_finalize_return_discrepancy_reverts_to_result_check(ticket_service):
    signed_parts = [SignedPartItem(part_name="Battery", signature_mark="SIG_BATT")]
    ticket = ticket_service.create_ticket(
        admin_user_id="USR_ADMIN_01",
        customer_id="CUST_001",
        device_id="DEV_001",
        intake_type=IntakeType.HOLD_FOR_REPAIR,
        promised_return_date=date(2026, 11, 28),
        reported_issue="Battery test",
        initial_condition="Normal",
        accessories_included="Adapter",
        plain_secret_code="SEC_BATT_99",
        signed_parts=signed_parts,
        customer_signature_confirmed=True
    )
    ticket.status = TicketStatus.WAITING_FOR_RETURN

    reverted_ticket = ticket_service.finalize_return(
        admin_user_id="USR_ADMIN_01",
        ticket_id=ticket.ticket_id,
        components_signature_verified=True,
        test_run_passed=False,
        customer_accepted=False,
        discrepancy_notes="Thermal test exceeded limit"
    )
    assert reverted_ticket.status == TicketStatus.WAITING_FOR_RESULT_CHECK

def test_cancel_ticket_pre_repair_allowed(ticket_service):
    signed_parts = [SignedPartItem(part_name="LCD", signature_mark="SIG")]
    ticket = ticket_service.create_ticket(
        admin_user_id="USR_ADMIN_01",
        customer_id="CUST_001",
        device_id="DEV_001",
        intake_type=IntakeType.HOLD_FOR_REPAIR,
        promised_return_date=date(2026, 11, 28),
        reported_issue="Test cancel",
        initial_condition="Normal",
        accessories_included="Adapter",
        plain_secret_code="SEC_CANCEL",
        signed_parts=signed_parts,
        customer_signature_confirmed=True
    )
    cancelled = ticket_service.cancel_ticket_pre_repair(
        admin_user_id="USR_ADMIN_01",
        ticket_id=ticket.ticket_id,
        cancellation_reason="Customer requested device retrieval before inspection",
        device_returned_to_customer=True
    )
    assert cancelled.status == TicketStatus.CANCELLED
    assert cancelled.cancellation_reason is not None
