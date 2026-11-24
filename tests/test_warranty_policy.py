import pytest
from datetime import date
from src.warranty_core import (
    IntakeType,
    TicketStatus,
    SignedPartItem,
    WarrantyEligibility,
    WarrantyResolution,
    DefectOrigin,
    WarrantyServiceError
)

def test_warranty_exchange_within_three_days(ticket_service, warranty_service):
    signed_parts = [SignedPartItem(part_name="Mainboard", signature_mark="SIG")]
    ticket = ticket_service.create_ticket(
        admin_user_id="USR_ADMIN_01",
        customer_id="CUST_001",
        device_id="DEV_001",
        intake_type=IntakeType.HOLD_FOR_REPAIR,
        promised_return_date=date(2026, 11, 28),
        reported_issue="Device will not turn on",
        initial_condition="Brand new",
        accessories_included="Box and accessories",
        plain_secret_code="SEC_EXCHANGE",
        signed_parts=signed_parts,
        customer_signature_confirmed=True
    )

    assessment = warranty_service.evaluate_and_record_policy(
        admin_user_id="USR_ADMIN_01",
        ticket_id=ticket.ticket_id,
        purchase_date=date(2026, 11, 22),
        incident_date=date(2026, 11, 24),
        is_warranty_valid=True,
        defect_origin=DefectOrigin.MANUFACTURER,
        customer_agreed=True,
        replacement_device_serial="SN-DELL-NEW-001"
    )
    assert assessment.eligibility == WarrantyEligibility.ELIGIBLE
    assert assessment.resolution == WarrantyResolution.ONE_TO_ONE_EXCHANGE
    assert ticket.status == TicketStatus.PENDING_ASSIGNMENT

def test_warranty_free_repair_after_exchange_window(ticket_service, warranty_service):
    signed_parts = [SignedPartItem(part_name="Display", signature_mark="SIG")]
    ticket = ticket_service.create_ticket(
        admin_user_id="USR_ADMIN_01",
        customer_id="CUST_001",
        device_id="DEV_001",
        intake_type=IntakeType.HOLD_FOR_REPAIR,
        promised_return_date=date(2026, 11, 28),
        reported_issue="Faint line across display",
        initial_condition="Good",
        accessories_included="Power adapter",
        plain_secret_code="SEC_FREE_REP",
        signed_parts=signed_parts,
        customer_signature_confirmed=True
    )

    assessment = warranty_service.evaluate_and_record_policy(
        admin_user_id="USR_ADMIN_01",
        ticket_id=ticket.ticket_id,
        purchase_date=date(2026, 1, 15),
        incident_date=date(2026, 11, 24),
        is_warranty_valid=True,
        defect_origin=DefectOrigin.MANUFACTURER,
        customer_agreed=True
    )
    assert assessment.eligibility == WarrantyEligibility.ELIGIBLE
    assert assessment.resolution == WarrantyResolution.FREE_REPAIR
    assert ticket.status == TicketStatus.PENDING_ASSIGNMENT

def test_warranty_paid_repair_requires_customer_agreement(ticket_service, warranty_service):
    signed_parts = [SignedPartItem(part_name="Chassis", signature_mark="SIG")]
    ticket = ticket_service.create_ticket(
        admin_user_id="USR_ADMIN_01",
        customer_id="CUST_001",
        device_id="DEV_001",
        intake_type=IntakeType.HOLD_FOR_REPAIR,
        promised_return_date=date(2026, 11, 28),
        reported_issue="Liquid spillage on keyboard",
        initial_condition="Water damaged",
        accessories_included="Power adapter",
        plain_secret_code="SEC_PAID",
        signed_parts=signed_parts,
        customer_signature_confirmed=True
    )

    with pytest.raises(WarrantyServiceError) as exc:
        warranty_service.evaluate_and_record_policy(
            admin_user_id="USR_ADMIN_01",
            ticket_id=ticket.ticket_id,
            purchase_date=date(2026, 1, 15),
            incident_date=date(2026, 11, 24),
            is_warranty_valid=True,
            defect_origin=DefectOrigin.USER_DAMAGE,
            customer_agreed=False
        )
    assert "Paid repair requires verified customer agreement" in str(exc.value)

def test_warranty_unclear_origin_stays_in_received(ticket_service, warranty_service):
    signed_parts = [SignedPartItem(part_name="GPU", signature_mark="SIG")]
    ticket = ticket_service.create_ticket(
        admin_user_id="USR_ADMIN_01",
        customer_id="CUST_001",
        device_id="DEV_001",
        intake_type=IntakeType.HOLD_FOR_REPAIR,
        promised_return_date=date(2026, 11, 28),
        reported_issue="Intermittent crash",
        initial_condition="Good",
        accessories_included="Adapter",
        plain_secret_code="SEC_UNCLEAR",
        signed_parts=signed_parts,
        customer_signature_confirmed=True
    )

    assessment = warranty_service.evaluate_and_record_policy(
        admin_user_id="USR_ADMIN_01",
        ticket_id=ticket.ticket_id,
        purchase_date=date(2026, 1, 15),
        incident_date=date(2026, 11, 24),
        is_warranty_valid=True,
        defect_origin=DefectOrigin.UNCLEAR,
        customer_agreed=True
    )
    assert assessment.eligibility == WarrantyEligibility.INSUFFICIENT_INFO
    assert assessment.resolution == WarrantyResolution.PENDING_DECISION
    assert ticket.status == TicketStatus.RECEIVED
