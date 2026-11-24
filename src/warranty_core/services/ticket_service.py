import hashlib
import uuid
from datetime import datetime, date
from typing import List, Optional
from ..domain_models import (
    WarrantyTicket,
    Customer,
    Device,
    SignedPartItem,
    StatusChangeLog
)
from ..enums import TicketStatus, IntakeType, UserRole
from ..repository import InMemoryRepository
from .clock_service import IClockService

class TicketServiceError(Exception):
    pass

class TicketService:
    def __init__(self, repository: InMemoryRepository, clock_service: IClockService):
        self._repo = repository
        self._clock = clock_service

    def create_ticket(
        self,
        admin_user_id: str,
        customer_id: str,
        device_id: str,
        intake_type: IntakeType,
        promised_return_date: date,
        reported_issue: str,
        initial_condition: str,
        accessories_included: str,
        plain_secret_code: str,
        signed_parts: Optional[List[SignedPartItem]] = None,
        customer_signature_confirmed: bool = False
    ) -> WarrantyTicket:
        admin_user = self._repo.users.get(admin_user_id)
        if not admin_user or admin_user.role != UserRole.ADMIN:
            raise TicketServiceError("Only active Admin users can create warranty tickets.")

        customer = self._repo.customers.get(customer_id)
        if not customer:
            raise TicketServiceError(f"Customer {customer_id} does not exist.")

        device = self._repo.devices.get(device_id)
        if not device:
            raise TicketServiceError(f"Device {device_id} does not exist.")

        if not reported_issue or not initial_condition:
            raise TicketServiceError("Reported issue and initial condition are mandatory.")

        now_dt = self._clock.now()
        today_d = self._clock.today()

        if promised_return_date < today_d:
            raise TicketServiceError("Promised return date cannot be in the past.")

        parts_list = signed_parts or []
        if intake_type == IntakeType.HOLD_FOR_REPAIR:
            if not parts_list:
                raise TicketServiceError(
                    "Hold-for-repair intake requires inspection and signing of components (BR02)."
                )
            if not customer_signature_confirmed:
                raise TicketServiceError(
                    "Hold-for-repair intake requires verified customer signature handover (BR02)."
                )

        daily_seq = self._repo.get_next_daily_ticket_number(today_d)
        date_str = today_d.strftime("%Y%m%d")
        ticket_id = f"TKT_{date_str}_{daily_seq}"

        tracking_hash = hashlib.sha256(plain_secret_code.encode("utf-8")).hexdigest()

        ticket = WarrantyTicket(
            ticket_id=ticket_id,
            customer_id=customer_id,
            device_id=device_id,
            intake_type=intake_type,
            promised_return_date=promised_return_date,
            reported_issue=reported_issue,
            initial_condition=initial_condition,
            accessories_included=accessories_included,
            status=TicketStatus.RECEIVED,
            tracking_code_hash=tracking_hash,
            created_at=now_dt,
            signed_parts=parts_list,
            customer_intake_signature_confirmed=customer_signature_confirmed
        )

        initial_log = StatusChangeLog(
            log_id=str(uuid.uuid4()),
            ticket_id=ticket_id,
            from_status=None,
            to_status=TicketStatus.RECEIVED,
            changed_by_user_id=admin_user_id,
            changed_at=now_dt,
            reason="Ticket created upon initial device intake"
        )
        ticket.status_history.append(initial_log)

        self._repo.tickets[ticket_id] = ticket
        return ticket

    def find_tickets(
        self,
        ticket_id: Optional[str] = None,
        contact_query: Optional[str] = None,
        serial_number: Optional[str] = None
    ) -> List[WarrantyTicket]:
        results = []
        for ticket in self._repo.tickets.values():
            if ticket_id and ticket_id.lower() in ticket.ticket_id.lower():
                results.append(ticket)
                continue

            if serial_number:
                device = self._repo.devices.get(ticket.device_id)
                if device and serial_number.lower() in device.serial_number.lower():
                    results.append(ticket)
                    continue

            if contact_query:
                customer = self._repo.customers.get(ticket.customer_id)
                if customer and (
                    contact_query.lower() in customer.phone_number.lower()
                    or contact_query.lower() in customer.full_name.lower()
                ):
                    results.append(ticket)
                    continue

            if not ticket_id and not contact_query and not serial_number:
                results.append(ticket)

        return results

    def finalize_return(
        self,
        admin_user_id: str,
        ticket_id: str,
        components_signature_verified: bool,
        test_run_passed: bool,
        customer_accepted: bool,
        discrepancy_notes: Optional[str] = None
    ) -> WarrantyTicket:
        admin_user = self._repo.users.get(admin_user_id)
        if not admin_user or admin_user.role != UserRole.ADMIN:
            raise TicketServiceError("Only Admin can execute final device return.")

        ticket = self._repo.find_ticket_by_id(ticket_id)
        if not ticket:
            raise TicketServiceError(f"Ticket {ticket_id} not found.")

        if ticket.status != TicketStatus.WAITING_FOR_RETURN:
            raise TicketServiceError(
                f"Ticket must be in WAITING_FOR_RETURN to close. Current: {ticket.status.value}"
            )

        now_dt = self._clock.now()

        if not components_signature_verified or not test_run_passed or not customer_accepted:
            ticket.status = TicketStatus.WAITING_FOR_RESULT_CHECK
            log = StatusChangeLog(
                log_id=str(uuid.uuid4()),
                ticket_id=ticket_id,
                from_status=TicketStatus.WAITING_FOR_RETURN,
                to_status=TicketStatus.WAITING_FOR_RESULT_CHECK,
                changed_by_user_id=admin_user_id,
                changed_at=now_dt,
                reason=f"Return failed inspection: {discrepancy_notes or 'Defect or signature discrepancy'}"
            )
            ticket.status_history.append(log)
            return ticket

        ticket.status = TicketStatus.RETURNED
        ticket.final_return_confirmed = True
        ticket.return_notes = "Customer verified components, signatures, and successful test run."
        log = StatusChangeLog(
            log_id=str(uuid.uuid4()),
            ticket_id=ticket_id,
            from_status=TicketStatus.WAITING_FOR_RETURN,
            to_status=TicketStatus.RETURNED,
            changed_by_user_id=admin_user_id,
            changed_at=now_dt,
            reason="Customer accepted delivery after full component verification"
        )
        ticket.status_history.append(log)
        return ticket

    def cancel_ticket_pre_repair(
        self,
        admin_user_id: str,
        ticket_id: str,
        cancellation_reason: str,
        device_returned_to_customer: bool
    ) -> WarrantyTicket:
        admin_user = self._repo.users.get(admin_user_id)
        if not admin_user or admin_user.role != UserRole.ADMIN:
            raise TicketServiceError("Only Admin can cancel tickets.")

        ticket = self._repo.find_ticket_by_id(ticket_id)
        if not ticket:
            raise TicketServiceError(f"Ticket {ticket_id} not found.")

        if ticket.status not in [TicketStatus.RECEIVED, TicketStatus.PENDING_ASSIGNMENT]:
            raise TicketServiceError(
                "Tickets can only be cancelled prior to repair commencement (BR09)."
            )

        if not device_returned_to_customer:
            raise TicketServiceError(
                "Physical return confirmation is mandatory for cancellation (BR09)."
            )

        now_dt = self._clock.now()
        prev_status = ticket.status
        ticket.status = TicketStatus.CANCELLED
        ticket.cancellation_reason = cancellation_reason
        log = StatusChangeLog(
            log_id=str(uuid.uuid4()),
            ticket_id=ticket_id,
            from_status=prev_status,
            to_status=TicketStatus.CANCELLED,
            changed_by_user_id=admin_user_id,
            changed_at=now_dt,
            reason=f"Cancelled pre-repair: {cancellation_reason}"
        )
        ticket.status_history.append(log)
        return ticket
