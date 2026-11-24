import pytest
from datetime import date
from src.warranty_core import (
    IntakeType,
    TicketStatus,
    SignedPartItem,
    DefectOrigin,
    HandoverStatus,
    RepairServiceError
)

def _setup_ticket_in_under_inspection(ticket_service, warranty_service, repair_service):
    signed_parts = [SignedPartItem(part_name="CPU", signature_mark="SIG")]
    ticket = ticket_service.create_ticket(
        admin_user_id="USR_ADMIN_01",
        customer_id="CUST_001",
        device_id="DEV_001",
        intake_type=IntakeType.HOLD_FOR_REPAIR,
        promised_return_date=date(2026, 11, 28),
        reported_issue="Thermal throttling",
        initial_condition="Good",
        accessories_included="Adapter",
        plain_secret_code="SEC_REPAIR_01",
        signed_parts=signed_parts,
        customer_signature_confirmed=True
    )
    warranty_service.evaluate_and_record_policy(
        admin_user_id="USR_ADMIN_01",
        ticket_id=ticket.ticket_id,
        purchase_date=date(2026, 1, 10),
        incident_date=date(2026, 11, 24),
        is_warranty_valid=True,
        defect_origin=DefectOrigin.MANUFACTURER,
        customer_agreed=True
    )
    repair_service.assign_technician(
        admin_user_id="USR_ADMIN_01",
        ticket_id=ticket.ticket_id,
        technician_user_id="USR_TECH_01"
    )
    return ticket

def test_technician_assignment_and_role_guard(ticket_service, warranty_service, repair_service):
    ticket = _setup_ticket_in_under_inspection(ticket_service, warranty_service, repair_service)
    assert ticket.status == TicketStatus.UNDER_INSPECTION
    assert ticket.current_technician_id == "USR_TECH_01"

    with pytest.raises(RepairServiceError) as exc:
        repair_service.update_repair_status(
            technician_user_id="USR_TECH_02",
            ticket_id=ticket.ticket_id,
            new_status=TicketStatus.UNDER_REPAIR,
            reason="Unauthorized tech update",
            diagnosis_findings="Faulty fan",
            actions_performed="Replaced fan",
            pending_tasks="None"
        )
    assert "Only the assigned technician currently in charge can update progress" in str(exc.value)

def test_valid_and_invalid_state_transitions(ticket_service, warranty_service, repair_service):
    ticket = _setup_ticket_in_under_inspection(ticket_service, warranty_service, repair_service)

    with pytest.raises(RepairServiceError) as exc:
        repair_service.update_repair_status(
            technician_user_id="USR_TECH_01",
            ticket_id=ticket.ticket_id,
            new_status=TicketStatus.RETURNED,
            reason="Premature return jump",
            diagnosis_findings="None",
            actions_performed="None",
            pending_tasks="None"
        )
    assert "Invalid state transition" in str(exc.value)

    repair_service.update_repair_status(
        technician_user_id="USR_TECH_01",
        ticket_id=ticket.ticket_id,
        new_status=TicketStatus.UNDER_REPAIR,
        reason="Diagnosis confirmed heatsink defect",
        diagnosis_findings="Heatsink pipe cracked",
        actions_performed="Disassembled cooling assembly",
        pending_tasks="Install replacement heatsink"
    )
    assert ticket.status == TicketStatus.UNDER_REPAIR
    assert len(ticket.work_logs) == 1

def test_handover_protocol_with_absent_technician(ticket_service, warranty_service, repair_service):
    ticket = _setup_ticket_in_under_inspection(ticket_service, warranty_service, repair_service)

    session = repair_service.initiate_handover(
        admin_user_id="USR_ADMIN_01",
        ticket_id=ticket.ticket_id,
        target_technician_id="USR_TECH_02",
        reason="Technician 1 on sudden medical leave",
        is_previous_technician_absent=True,
        missing_info_notes="Diagnostics recorded in work log #1"
    )
    assert session.status == HandoverStatus.PENDING
    assert session.is_previous_technician_absent is True
    assert ticket.current_technician_id == "USR_TECH_01"

    updated_session = repair_service.respond_to_handover(
        target_technician_id="USR_TECH_02",
        session_id=session.session_id,
        accept=True
    )
    assert updated_session.status == HandoverStatus.ACCEPTED
    assert ticket.current_technician_id == "USR_TECH_02"

def test_handover_rejection_requires_reason(ticket_service, warranty_service, repair_service):
    ticket = _setup_ticket_in_under_inspection(ticket_service, warranty_service, repair_service)

    session = repair_service.initiate_handover(
        admin_user_id="USR_ADMIN_01",
        ticket_id=ticket.ticket_id,
        target_technician_id="USR_TECH_02",
        reason="Rebalancing workload"
    )
    with pytest.raises(RepairServiceError) as exc:
        repair_service.respond_to_handover(
            target_technician_id="USR_TECH_02",
            session_id=session.session_id,
            accept=False,
            rejection_reason=""
        )
    assert "Rejection reason is mandatory" in str(exc.value)
