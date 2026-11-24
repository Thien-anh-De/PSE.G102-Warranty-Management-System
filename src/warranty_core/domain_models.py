from dataclasses import dataclass, field
from datetime import datetime, date
from typing import Optional, List
from .enums import (
    TicketStatus,
    IntakeType,
    WarrantyEligibility,
    WarrantyResolution,
    DefectOrigin,
    HandoverStatus,
    TransactionType
)

@dataclass
class User:
    user_id: str
    username: str
    password_hash: str
    full_name: str
    role: str
    is_active: bool = True

@dataclass
class Customer:
    customer_id: str
    full_name: str
    phone_number: str
    email: Optional[str] = None
    address: Optional[str] = None

@dataclass
class Device:
    device_id: str
    serial_number: str
    model_name: str
    brand: str
    purchase_date: Optional[date] = None

@dataclass
class SignedPartItem:
    part_name: str
    signature_mark: str
    notes: Optional[str] = None

@dataclass
class StatusChangeLog:
    log_id: str
    ticket_id: str
    from_status: Optional[TicketStatus]
    to_status: TicketStatus
    changed_by_user_id: str
    changed_at: datetime
    reason: str

@dataclass
class RepairWorkLog:
    log_id: str
    ticket_id: str
    technician_id: str
    created_at: datetime
    diagnosis_findings: str
    actions_performed: str
    pending_tasks: str
    used_parts_summary: Optional[str] = None

@dataclass
class HandoverSession:
    session_id: str
    ticket_id: str
    initiated_by_admin_id: str
    previous_technician_id: str
    target_technician_id: str
    status: HandoverStatus
    created_at: datetime
    decided_at: Optional[datetime] = None
    reason: str = ""
    is_previous_technician_absent: bool = False
    missing_info_notes: Optional[str] = None
    rejection_reason: Optional[str] = None

@dataclass
class SparePart:
    part_id: str
    part_code: str
    part_name: str
    unit: str
    stock_quantity: int
    minimum_threshold: int

    @property
    def is_low_stock(self) -> bool:
        return self.stock_quantity < self.minimum_threshold

@dataclass
class PartAllocation:
    allocation_id: str
    ticket_id: str
    part_id: str
    allocated_quantity: int
    used_quantity: int
    allocated_at: datetime

    @property
    def remaining_usable_quantity(self) -> int:
        return self.allocated_quantity - self.used_quantity

@dataclass
class PartTransaction:
    transaction_id: str
    part_id: str
    transaction_type: TransactionType
    quantity: int
    ticket_id: Optional[str]
    performed_by_user_id: str
    timestamp: datetime
    reference_note: str

@dataclass
class WarrantyAssessment:
    assessment_id: str
    ticket_id: str
    purchase_date: date
    incident_date: date
    is_warranty_valid: bool
    defect_origin: DefectOrigin
    eligibility: WarrantyEligibility
    resolution: WarrantyResolution
    customer_agreed: bool
    replacement_device_serial: Optional[str] = None
    original_device_serial: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)

@dataclass
class WarrantyTicket:
    ticket_id: str
    customer_id: str
    device_id: str
    intake_type: IntakeType
    promised_return_date: date
    reported_issue: str
    initial_condition: str
    accessories_included: str
    status: TicketStatus
    tracking_code_hash: str
    created_at: datetime
    current_technician_id: Optional[str] = None
    signed_parts: List[SignedPartItem] = field(default_factory=list)
    customer_intake_signature_confirmed: bool = False
    final_return_confirmed: bool = False
    return_notes: Optional[str] = None
    cancellation_reason: Optional[str] = None
    status_history: List[StatusChangeLog] = field(default_factory=list)
    work_logs: List[RepairWorkLog] = field(default_factory=list)
