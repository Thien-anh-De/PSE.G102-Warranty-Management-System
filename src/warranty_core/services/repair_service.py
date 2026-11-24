import uuid
from datetime import datetime
from typing import Optional
from ..domain_models import (
    WarrantyTicket,
    StatusChangeLog,
    RepairWorkLog,
    HandoverSession
)
from ..enums import (
    TicketStatus,
    HandoverStatus,
    UserRole
)
from ..repository import InMemoryRepository
from .clock_service import IClockService

class RepairServiceError(Exception):
    pass

class RepairService:
    VALID_TRANSITIONS = {
        TicketStatus.RECEIVED: {TicketStatus.PENDING_ASSIGNMENT, TicketStatus.CANCELLED},
        TicketStatus.PENDING_ASSIGNMENT: {TicketStatus.UNDER_INSPECTION, TicketStatus.CANCELLED},
        TicketStatus.UNDER_INSPECTION: {TicketStatus.UNDER_REPAIR, TicketStatus.WAITING_FOR_RESULT_CHECK},
        TicketStatus.UNDER_REPAIR: {TicketStatus.WAITING_FOR_PARTS, TicketStatus.WAITING_FOR_RESULT_CHECK},
        TicketStatus.WAITING_FOR_PARTS: {TicketStatus.UNDER_REPAIR},
        TicketStatus.WAITING_FOR_RESULT_CHECK: {TicketStatus.UNDER_REPAIR, TicketStatus.WAITING_FOR_RETURN},
        TicketStatus.WAITING_FOR_RETURN: {TicketStatus.WAITING_FOR_RESULT_CHECK, TicketStatus.RETURNED},
        TicketStatus.RETURNED: set(),
        TicketStatus.CANCELLED: set()
    }

    def __init__(self, repository: InMemoryRepository, clock_service: IClockService):
        self._repo = repository
        self._clock = clock_service

    def assign_technician(
        self,
        admin_user_id: str,
        ticket_id: str,
        technician_user_id: str
    ) -> WarrantyTicket:
        admin_user = self._repo.users.get(admin_user_id)
        if not admin_user or admin_user.role != UserRole.ADMIN:
            raise RepairServiceError("Only Admin can assign technicians.")

        tech_user = self._repo.users.get(technician_user_id)
        if not tech_user or tech_user.role != UserRole.TECHNICIAN or not tech_user.is_active:
            raise RepairServiceError(
                f"Technician {technician_user_id} must be an active technician."
            )

        ticket = self._repo.find_ticket_by_id(ticket_id)
        if not ticket:
            raise RepairServiceError(f"Ticket {ticket_id} does not exist.")

        if ticket.status != TicketStatus.PENDING_ASSIGNMENT:
            raise RepairServiceError(
                f"Technician can only be assigned in PENDING_ASSIGNMENT. Current: {ticket.status.value}"
            )

        now_dt = self._clock.now()
        ticket.current_technician_id = technician_user_id
        ticket.status = TicketStatus.UNDER_INSPECTION

        log = StatusChangeLog(
            log_id=str(uuid.uuid4()),
            ticket_id=ticket_id,
            from_status=TicketStatus.PENDING_ASSIGNMENT,
            to_status=TicketStatus.UNDER_INSPECTION,
            changed_by_user_id=admin_user_id,
            changed_at=now_dt,
            reason=f"Assigned to technician {tech_user.username}"
        )
        ticket.status_history.append(log)
        return ticket

    def update_repair_status(
        self,
        technician_user_id: str,
        ticket_id: str,
        new_status: TicketStatus,
        reason: str,
        diagnosis_findings: str,
        actions_performed: str,
        pending_tasks: str
    ) -> WarrantyTicket:
        ticket = self._repo.find_ticket_by_id(ticket_id)
        if not ticket:
            raise RepairServiceError(f"Ticket {ticket_id} not found.")

        if ticket.current_technician_id != technician_user_id:
            raise RepairServiceError(
                "Only the assigned technician currently in charge can update progress (BR04)."
            )

        allowed_targets = self.VALID_TRANSITIONS.get(ticket.status, set())
        if new_status not in allowed_targets:
            raise RepairServiceError(
                f"Invalid state transition from {ticket.status.value} to {new_status.value} (BR09)."
            )

        if not reason or not actions_performed:
            raise RepairServiceError(
                "Reason and actions performed are required when changing repair status (BR05)."
            )

        now_dt = self._clock.now()
        prev_status = ticket.status
        ticket.status = new_status

        status_log = StatusChangeLog(
            log_id=str(uuid.uuid4()),
            ticket_id=ticket_id,
            from_status=prev_status,
            to_status=new_status,
            changed_by_user_id=technician_user_id,
            changed_at=now_dt,
            reason=reason
        )
        ticket.status_history.append(status_log)

        work_log = RepairWorkLog(
            log_id=str(uuid.uuid4()),
            ticket_id=ticket_id,
            technician_id=technician_user_id,
            created_at=now_dt,
            diagnosis_findings=diagnosis_findings,
            actions_performed=actions_performed,
            pending_tasks=pending_tasks
        )
        ticket.work_logs.append(work_log)

        return ticket

    def add_work_log(
        self,
        technician_user_id: str,
        ticket_id: str,
        diagnosis_findings: str,
        actions_performed: str,
        pending_tasks: str
    ) -> RepairWorkLog:
        ticket = self._repo.find_ticket_by_id(ticket_id)
        if not ticket:
            raise RepairServiceError(f"Ticket {ticket_id} not found.")

        if ticket.current_technician_id != technician_user_id:
            raise RepairServiceError("Only the assigned technician can append work logs (BR04).")

        now_dt = self._clock.now()
        work_log = RepairWorkLog(
            log_id=str(uuid.uuid4()),
            ticket_id=ticket_id,
            technician_id=technician_user_id,
            created_at=now_dt,
            diagnosis_findings=diagnosis_findings,
            actions_performed=actions_performed,
            pending_tasks=pending_tasks
        )
        ticket.work_logs.append(work_log)
        return work_log

    def initiate_handover(
        self,
        admin_user_id: str,
        ticket_id: str,
        target_technician_id: str,
        reason: str,
        is_previous_technician_absent: bool = False,
        missing_info_notes: Optional[str] = None
    ) -> HandoverSession:
        admin_user = self._repo.users.get(admin_user_id)
        if not admin_user or admin_user.role != UserRole.ADMIN:
            raise RepairServiceError("Only Admin can initiate technician handovers (BR07).")

        ticket = self._repo.find_ticket_by_id(ticket_id)
        if not ticket:
            raise RepairServiceError(f"Ticket {ticket_id} not found.")

        if not ticket.current_technician_id:
            raise RepairServiceError("Cannot handover a ticket with no assigned technician.")

        target_tech = self._repo.users.get(target_technician_id)
        if not target_tech or target_tech.role != UserRole.TECHNICIAN or not target_tech.is_active:
            raise RepairServiceError("Target technician must be an active technician.")

        if ticket.current_technician_id == target_technician_id:
            raise RepairServiceError("Target technician cannot be the current technician.")

        existing_pending = self._repo.get_pending_handover_for_ticket(ticket_id)
        if existing_pending:
            raise RepairServiceError(
                "A pending handover session already exists for this ticket (BR07)."
            )

        now_dt = self._clock.now()
        session_id = f"HO_{uuid.uuid4().hex[:8].upper()}"
        session = HandoverSession(
            session_id=session_id,
            ticket_id=ticket_id,
            initiated_by_admin_id=admin_user_id,
            previous_technician_id=ticket.current_technician_id,
            target_technician_id=target_technician_id,
            status=HandoverStatus.PENDING,
            created_at=now_dt,
            reason=reason,
            is_previous_technician_absent=is_previous_technician_absent,
            missing_info_notes=missing_info_notes
        )
        self._repo.handovers[session_id] = session
        return session

    def respond_to_handover(
        self,
        target_technician_id: str,
        session_id: str,
        accept: bool,
        rejection_reason: Optional[str] = None
    ) -> HandoverSession:
        session = self._repo.handovers.get(session_id)
        if not session:
            raise RepairServiceError(f"Handover session {session_id} not found.")

        if session.target_technician_id != target_technician_id:
            raise RepairServiceError("Only the specified target technician can respond.")

        if session.status != HandoverStatus.PENDING:
            raise RepairServiceError("Handover session is not in PENDING state.")

        ticket = self._repo.find_ticket_by_id(session.ticket_id)
        if not ticket:
            raise RepairServiceError(f"Ticket {session.ticket_id} not found.")

        now_dt = self._clock.now()
        session.decided_at = now_dt

        if not accept:
            if not rejection_reason:
                raise RepairServiceError("Rejection reason is mandatory when declining handover (BR07).")
            session.status = HandoverStatus.REJECTED
            session.rejection_reason = rejection_reason
            return session

        session.status = HandoverStatus.ACCEPTED
        prev_tech_id = ticket.current_technician_id
        ticket.current_technician_id = target_technician_id

        log = StatusChangeLog(
            log_id=str(uuid.uuid4()),
            ticket_id=ticket.ticket_id,
            from_status=ticket.status,
            to_status=ticket.status,
            changed_by_user_id=target_technician_id,
            changed_at=now_dt,
            reason=f"Handover accepted. Transferred from {prev_tech_id} to {target_technician_id}."
        )
        ticket.status_history.append(log)
        return session
