import pytest
from datetime import date
from src.warranty_core import (
    IntakeType,
    SignedPartItem,
    DefectOrigin,
    InventoryServiceError
)

def _setup_active_ticket(ticket_service, warranty_service, repair_service):
    signed_parts = [SignedPartItem(part_name="Fans", signature_mark="SIG")]
    ticket = ticket_service.create_ticket(
        admin_user_id="USR_ADMIN_01",
        customer_id="CUST_001",
        device_id="DEV_001",
        intake_type=IntakeType.HOLD_FOR_REPAIR,
        promised_return_date=date(2026, 11, 28),
        reported_issue="Noisy fan",
        initial_condition="Used",
        accessories_included="Adapter",
        plain_secret_code="SEC_FAN_01",
        signed_parts=signed_parts,
        customer_signature_confirmed=True
    )
    warranty_service.evaluate_and_record_policy(
        admin_user_id="USR_ADMIN_01",
        ticket_id=ticket.ticket_id,
        purchase_date=date(2026, 1, 1),
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

def test_inventory_flow_and_anti_overdraft(
    ticket_service,
    warranty_service,
    repair_service,
    inventory_service
):
    ticket = _setup_active_ticket(ticket_service, warranty_service, repair_service)

    part = inventory_service.register_part(
        admin_user_id="USR_ADMIN_01",
        part_code="FAN-XPS-01",
        part_name="Cooling Fan XPS 15",
        unit="PCS",
        initial_stock=5,
        minimum_threshold=2
    )
    assert part.stock_quantity == 5
    assert part.is_low_stock is False

    alloc = inventory_service.allocate_part_to_ticket(
        admin_user_id="USR_ADMIN_01",
        ticket_id=ticket.ticket_id,
        part_id=part.part_id,
        quantity=2
    )
    assert part.stock_quantity == 3
    assert alloc.allocated_quantity == 2
    assert alloc.remaining_usable_quantity == 2

    used_alloc = inventory_service.record_part_usage(
        technician_user_id="USR_TECH_01",
        ticket_id=ticket.ticket_id,
        part_id=part.part_id,
        used_quantity=1
    )
    assert used_alloc.used_quantity == 1
    assert used_alloc.remaining_usable_quantity == 1
    assert part.stock_quantity == 3

    with pytest.raises(InventoryServiceError) as exc:
        inventory_service.record_part_usage(
            technician_user_id="USR_TECH_01",
            ticket_id=ticket.ticket_id,
            part_id=part.part_id,
            used_quantity=2
        )
    assert "Cannot use 2. Max remaining allocated is 1" in str(exc.value)

def test_inventory_insufficient_stock_rejection(ticket_service, warranty_service, repair_service, inventory_service):
    ticket = _setup_active_ticket(ticket_service, warranty_service, repair_service)
    part = inventory_service.register_part(
        admin_user_id="USR_ADMIN_01",
        part_code="OLED-PANEL-01",
        part_name="OLED Panel 4K",
        unit="PCS",
        initial_stock=1,
        minimum_threshold=2
    )
    with pytest.raises(InventoryServiceError) as exc:
        inventory_service.allocate_part_to_ticket(
            admin_user_id="USR_ADMIN_01",
            ticket_id=ticket.ticket_id,
            part_id=part.part_id,
            quantity=2
        )
    assert "Insufficient stock" in str(exc.value)
