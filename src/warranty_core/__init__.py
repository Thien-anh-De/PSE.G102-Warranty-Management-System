from .enums import (
    UserRole,
    TicketStatus,
    IntakeType,
    WarrantyEligibility,
    WarrantyResolution,
    DefectOrigin,
    HandoverStatus,
    TransactionType,
    SlaGroup
)
from .domain_models import (
    User,
    Customer,
    Device,
    SignedPartItem,
    StatusChangeLog,
    RepairWorkLog,
    HandoverSession,
    SparePart,
    PartAllocation,
    PartTransaction,
    WarrantyAssessment,
    WarrantyTicket
)
from .repository import InMemoryRepository
from .services.clock_service import IClockService, SystemClockService, SimulatedClockService
from .services.email_service import IEmailService, MockEmailService, EmailMessage
from .services.ticket_service import TicketService, TicketServiceError
from .services.warranty_service import WarrantyService, WarrantyServiceError
from .services.repair_service import RepairService, RepairServiceError
from .services.inventory_service import InventoryService, InventoryServiceError
from .services.sla_service import SlaService
from .services.portal_service import PortalService, PortalServiceError

__all__ = [
    "UserRole",
    "TicketStatus",
    "IntakeType",
    "WarrantyEligibility",
    "WarrantyResolution",
    "DefectOrigin",
    "HandoverStatus",
    "TransactionType",
    "SlaGroup",
    "User",
    "Customer",
    "Device",
    "SignedPartItem",
    "StatusChangeLog",
    "RepairWorkLog",
    "HandoverSession",
    "SparePart",
    "PartAllocation",
    "PartTransaction",
    "WarrantyAssessment",
    "WarrantyTicket",
    "InMemoryRepository",
    "IClockService",
    "SystemClockService",
    "SimulatedClockService",
    "IEmailService",
    "MockEmailService",
    "EmailMessage",
    "TicketService",
    "TicketServiceError",
    "WarrantyService",
    "WarrantyServiceError",
    "RepairService",
    "RepairServiceError",
    "InventoryService",
    "InventoryServiceError",
    "SlaService",
    "PortalService",
    "PortalServiceError",
]
