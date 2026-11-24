from datetime import date, timedelta
from src.warranty_core import (
    IntakeType,
    TicketStatus,
    SignedPartItem
)

def test_sla_0800_grouping_and_dispatch(
    ticket_service,
    sla_service,
    email_service,
    clock
):
    today = clock.today()
    tomorrow = today + timedelta(days=1)
    overdue_day = today - timedelta(days=2)

    signed_parts = [SignedPartItem(part_name="Board", signature_mark="SIG")]

    ticket_overdue = ticket_service.create_ticket(
        admin_user_id="USR_ADMIN_01",
        customer_id="CUST_001",
        device_id="DEV_001",
        intake_type=IntakeType.HOLD_FOR_REPAIR,
        promised_return_date=today,
        reported_issue="Overdue case",
        initial_condition="Used",
        accessories_included="None",
        plain_secret_code="SEC_1",
        signed_parts=signed_parts,
        customer_signature_confirmed=True
    )
    ticket_overdue.promised_return_date = overdue_day
    ticket_overdue.status = TicketStatus.UNDER_REPAIR

    ticket_due_today = ticket_service.create_ticket(
        admin_user_id="USR_ADMIN_01",
        customer_id="CUST_001",
        device_id="DEV_001",
        intake_type=IntakeType.HOLD_FOR_REPAIR,
        promised_return_date=today,
        reported_issue="Due today case",
        initial_condition="Used",
        accessories_included="None",
        plain_secret_code="SEC_2",
        signed_parts=signed_parts,
        customer_signature_confirmed=True
    )
    ticket_due_today.status = TicketStatus.UNDER_REPAIR

    ticket_waiting_parts = ticket_service.create_ticket(
        admin_user_id="USR_ADMIN_01",
        customer_id="CUST_001",
        device_id="DEV_001",
        intake_type=IntakeType.HOLD_FOR_REPAIR,
        promised_return_date=today + timedelta(days=5),
        reported_issue="Waiting parts case",
        initial_condition="Used",
        accessories_included="None",
        plain_secret_code="SEC_3",
        signed_parts=signed_parts,
        customer_signature_confirmed=True
    )
    ticket_waiting_parts.status = TicketStatus.WAITING_FOR_PARTS

    ticket_due_tomorrow = ticket_service.create_ticket(
        admin_user_id="USR_ADMIN_01",
        customer_id="CUST_001",
        device_id="DEV_001",
        intake_type=IntakeType.HOLD_FOR_REPAIR,
        promised_return_date=tomorrow,
        reported_issue="Due tomorrow case",
        initial_condition="Used",
        accessories_included="None",
        plain_secret_code="SEC_4",
        signed_parts=signed_parts,
        customer_signature_confirmed=True
    )
    ticket_due_tomorrow.status = TicketStatus.UNDER_REPAIR

    report = sla_service.build_daily_0800_sla_report()
    assert report["total_red_alert"] == 3
    assert report["total_attention"] == 1

    group_1_ids = [item["ticket"].ticket_id for item in report["group_1_red_alert"]]
    assert ticket_overdue.ticket_id in group_1_ids
    assert ticket_due_today.ticket_id in group_1_ids
    assert ticket_waiting_parts.ticket_id in group_1_ids

    group_2_ids = [item["ticket"].ticket_id for item in report["group_2_attention"]]
    assert ticket_due_tomorrow.ticket_id in group_2_ids

    sent = sla_service.dispatch_daily_0800_email("manager@hungthien.vn")
    assert sent is True
    sent_msgs = email_service.get_sent_messages()
    assert len(sent_msgs) == 1
    assert "DAILY SLA DIGEST" in sent_msgs[0].body_text
    assert "GROUP 1: RED ALERT" in sent_msgs[0].body_text
