from datetime import timedelta
from typing import List, Dict, Any
from ..enums import TicketStatus, SlaGroup
from ..repository import InMemoryRepository
from .clock_service import IClockService
from .email_service import IEmailService

class SlaService:
    def __init__(
        self,
        repository: InMemoryRepository,
        clock_service: IClockService,
        email_service: IEmailService
    ):
        self._repo = repository
        self._clock = clock_service
        self._email = email_service

    def build_daily_0800_sla_report(self) -> Dict[str, Any]:
        today = self._clock.today()
        tomorrow = today + timedelta(days=1)

        group_1_tickets = []
        group_2_tickets = []
        visited_ticket_ids = set()

        uncompleted_statuses = {
            TicketStatus.RECEIVED,
            TicketStatus.PENDING_ASSIGNMENT,
            TicketStatus.UNDER_INSPECTION,
            TicketStatus.UNDER_REPAIR,
            TicketStatus.WAITING_FOR_PARTS,
            TicketStatus.WAITING_FOR_RESULT_CHECK
        }

        for ticket in self._repo.tickets.values():
            if ticket.status not in uncompleted_statuses:
                continue

            is_due_today = ticket.promised_return_date == today
            is_overdue = ticket.promised_return_date < today
            is_waiting_parts = ticket.status == TicketStatus.WAITING_FOR_PARTS

            if is_due_today or is_overdue or is_waiting_parts:
                reason = []
                if is_overdue:
                    reason.append(f"Overdue (promised {ticket.promised_return_date})")
                elif is_due_today:
                    reason.append("Due today")
                if is_waiting_parts:
                    reason.append("Waiting for parts")

                group_1_tickets.append({
                    "ticket": ticket,
                    "reason": ", ".join(reason)
                })
                visited_ticket_ids.add(ticket.ticket_id)

        for ticket in self._repo.tickets.values():
            if ticket.status not in uncompleted_statuses:
                continue
            if ticket.ticket_id in visited_ticket_ids:
                continue

            if ticket.promised_return_date == tomorrow:
                group_2_tickets.append({
                    "ticket": ticket,
                    "reason": f"Due tomorrow ({tomorrow})"
                })
                visited_ticket_ids.add(ticket.ticket_id)

        return {
            "report_date": today,
            "generated_at": self._clock.now(),
            "group_1_red_alert": group_1_tickets,
            "group_2_attention": group_2_tickets,
            "total_red_alert": len(group_1_tickets),
            "total_attention": len(group_2_tickets)
        }

    def dispatch_daily_0800_email(self, admin_recipient_email: str) -> bool:
        report = self.build_daily_0800_sla_report()
        report_date_str = report["report_date"].strftime("%Y-%m-%d")

        body_lines = [
            f"DAILY SLA DIGEST - {report_date_str} (08:00 DISPATCH)",
            "============================================================",
            f"GROUP 1: RED ALERT (Total: {report['total_red_alert']})",
            "------------------------------------------------------------"
        ]

        if not report["group_1_red_alert"]:
            body_lines.append("  (No tickets in Group 1)")
        else:
            for item in report["group_1_red_alert"]:
                t = item["ticket"]
                device = self._repo.devices.get(t.device_id)
                dev_str = f"{device.model_name} (SN: {device.serial_number})" if device else t.device_id
                tech_user = self._repo.users.get(t.current_technician_id) if t.current_technician_id else None
                tech_str = tech_user.username if tech_user else "Unassigned"
                body_lines.append(
                    f"  * Ticket: {t.ticket_id} | Device: {dev_str} | Tech: {tech_str} | "
                    f"Due: {t.promised_return_date} | Status: {t.status.value} | Reason: {item['reason']}"
                )

        body_lines.append("\n============================================================")
        body_lines.append(f"GROUP 2: ATTENTION - DUE TOMORROW (Total: {report['total_attention']})")
        body_lines.append("------------------------------------------------------------")

        if not report["group_2_attention"]:
            body_lines.append("  (No tickets in Group 2)")
        else:
            for item in report["group_2_attention"]:
                t = item["ticket"]
                device = self._repo.devices.get(t.device_id)
                dev_str = f"{device.model_name} (SN: {device.serial_number})" if device else t.device_id
                tech_user = self._repo.users.get(t.current_technician_id) if t.current_technician_id else None
                tech_str = tech_user.username if tech_user else "Unassigned"
                body_lines.append(
                    f"  * Ticket: {t.ticket_id} | Device: {dev_str} | Tech: {tech_str} | "
                    f"Due: {t.promised_return_date} | Status: {t.status.value} | Reason: {item['reason']}"
                )

        subject = f"[Warranty Alert 08:00] Daily SLA Status Digest - {report_date_str}"
        body_text = "\n".join(body_lines)
        return self._email.send_email(admin_recipient_email, subject, body_text)
