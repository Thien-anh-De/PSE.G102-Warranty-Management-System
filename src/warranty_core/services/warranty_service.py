import uuid
from datetime import date
from typing import Optional
from ..domain_models import WarrantyAssessment, StatusChangeLog
from ..enums import (
    TicketStatus,
    WarrantyEligibility,
    WarrantyResolution,
    DefectOrigin,
    UserRole
)
from ..repository import InMemoryRepository
from .clock_service import IClockService

class WarrantyServiceError(Exception):
    pass

class WarrantyService:
    def __init__(self, repository: InMemoryRepository, clock_service: IClockService):
        self._repo = repository
        self._clock = clock_service

    def evaluate_and_record_policy(
        self,
        admin_user_id: str,
        ticket_id: str,
        purchase_date: date,
        incident_date: date,
        is_warranty_valid: bool,
        defect_origin: DefectOrigin,
        customer_agreed: bool,
        replacement_device_serial: Optional[str] = None
    ) -> WarrantyAssessment:
        admin_user = self._repo.users.get(admin_user_id)
        if not admin_user or admin_user.role != UserRole.ADMIN:
            raise WarrantyServiceError("Only Admin can evaluate warranty policy.")

        ticket = self._repo.find_ticket_by_id(ticket_id)
        if not ticket:
            raise WarrantyServiceError(f"Ticket {ticket_id} does not exist.")

        if ticket.status != TicketStatus.RECEIVED:
            raise WarrantyServiceError(
                f"Warranty policy must be evaluated in RECEIVED status. Current: {ticket.status.value}"
            )

        days_since_purchase = (incident_date - purchase_date).days

        if not is_warranty_valid:
            eligibility = WarrantyEligibility.INELIGIBLE
            resolution = WarrantyResolution.PAID_REPAIR
        elif defect_origin == DefectOrigin.UNCLEAR:
            eligibility = WarrantyEligibility.INSUFFICIENT_INFO
            resolution = WarrantyResolution.PENDING_DECISION
        elif defect_origin == DefectOrigin.USER_DAMAGE:
            eligibility = WarrantyEligibility.INELIGIBLE
            resolution = WarrantyResolution.PAID_REPAIR
        else:
            eligibility = WarrantyEligibility.ELIGIBLE
            if 0 <= days_since_purchase <= 3:
                resolution = WarrantyResolution.ONE_TO_ONE_EXCHANGE
            else:
                resolution = WarrantyResolution.FREE_REPAIR

        if resolution == WarrantyResolution.ONE_TO_ONE_EXCHANGE and not replacement_device_serial:
            raise WarrantyServiceError(
                "1-to-1 Exchange resolution requires replacement device serial number."
            )

        if resolution == WarrantyResolution.PAID_REPAIR and not customer_agreed:
            raise WarrantyServiceError(
                "Paid repair requires verified customer agreement before advancement (BR03, FR_WAR_02)."
            )

        now_dt = self._clock.now()
        assessment_id = f"WAR_{uuid.uuid4().hex[:8].upper()}"
        assessment = WarrantyAssessment(
            assessment_id=assessment_id,
            ticket_id=ticket_id,
            purchase_date=purchase_date,
            incident_date=incident_date,
            is_warranty_valid=is_warranty_valid,
            defect_origin=defect_origin,
            eligibility=eligibility,
            resolution=resolution,
            customer_agreed=customer_agreed,
            replacement_device_serial=replacement_device_serial,
            created_at=now_dt
        )
        self._repo.assessments[ticket_id] = assessment

        if eligibility != WarrantyEligibility.INSUFFICIENT_INFO and (
            resolution != WarrantyResolution.PAID_REPAIR or customer_agreed
        ):
            ticket.status = TicketStatus.PENDING_ASSIGNMENT
            log = StatusChangeLog(
                log_id=str(uuid.uuid4()),
                ticket_id=ticket_id,
                from_status=TicketStatus.RECEIVED,
                to_status=TicketStatus.PENDING_ASSIGNMENT,
                changed_by_user_id=admin_user_id,
                changed_at=now_dt,
                reason=f"Warranty assessed: {eligibility.value} - Resolution: {resolution.value}"
            )
            ticket.status_history.append(log)

        return assessment
