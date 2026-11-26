import hashlib
from typing import Optional, Dict, Any, Protocol
from ..domain_models import Device, WarrantyTicket


class PortalRepository(Protocol):
    """Read operations shared by the memory and PostgreSQL repositories."""

    def find_ticket_by_id(self, ticket_id: str) -> Optional[WarrantyTicket]: ...

    def get_device(self, device_id: str) -> Optional[Device]: ...

class PortalServiceError(Exception):
    pass

class PortalService:
    def __init__(self, repository: PortalRepository):
        self._repo = repository

    def lookup_ticket_public_status(
        self,
        ticket_id: str,
        plain_secret_code: str
    ) -> Dict[str, Any]:
        ticket = self._repo.find_ticket_by_id(ticket_id)
        if not ticket:
            raise PortalServiceError("Verification failed: invalid ticket code or secret key.")

        candidate_hash = hashlib.sha256(plain_secret_code.encode("utf-8")).hexdigest()
        if candidate_hash != ticket.tracking_code_hash:
            raise PortalServiceError("Verification failed: invalid ticket code or secret key.")

        device = self._repo.get_device(ticket.device_id)
        device_model = device.model_name if device else "Standard Equipment"
        raw_serial = (device.serial_number or "") if device else ""

        if len(raw_serial) > 4:
            masked_serial = raw_serial[:2] + "****" + raw_serial[-2:]
        else:
            masked_serial = "****"

        return {
            "ticket_id": ticket.ticket_id,
            "device_model": device_model,
            "device_serial_masked": masked_serial,
            "status": ticket.status.value,
            "intake_type": ticket.intake_type.value,
            "promised_return_date": str(ticket.promised_return_date),
            "reported_issue": ticket.reported_issue
        }
