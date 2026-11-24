import uuid
from typing import List, Optional
from ..domain_models import (
    SparePart,
    PartAllocation,
    PartTransaction
)
from ..enums import TransactionType, UserRole, TicketStatus
from ..repository import InMemoryRepository
from .clock_service import IClockService

class InventoryServiceError(Exception):
    pass

class InventoryService:
    def __init__(self, repository: InMemoryRepository, clock_service: IClockService):
        self._repo = repository
        self._clock = clock_service

    def register_part(
        self,
        admin_user_id: str,
        part_code: str,
        part_name: str,
        unit: str,
        initial_stock: int,
        minimum_threshold: int
    ) -> SparePart:
        admin_user = self._repo.users.get(admin_user_id)
        if not admin_user or admin_user.role != UserRole.ADMIN:
            raise InventoryServiceError("Only Admin can register spare parts.")

        if self._repo.find_part_by_code(part_code):
            raise InventoryServiceError(f"Part with code {part_code} already exists.")

        if initial_stock < 0 or minimum_threshold < 0:
            raise InventoryServiceError("Initial stock and minimum threshold cannot be negative.")

        part_id = f"PRT_{uuid.uuid4().hex[:8].upper()}"
        part = SparePart(
            part_id=part_id,
            part_code=part_code,
            part_name=part_name,
            unit=unit,
            stock_quantity=initial_stock,
            minimum_threshold=minimum_threshold
        )
        self._repo.parts[part_id] = part

        if initial_stock > 0:
            trx = PartTransaction(
                transaction_id=str(uuid.uuid4()),
                part_id=part_id,
                transaction_type=TransactionType.IMPORT,
                quantity=initial_stock,
                ticket_id=None,
                performed_by_user_id=admin_user_id,
                timestamp=self._clock.now(),
                reference_note="Initial stock registration"
            )
            self._repo.transactions.append(trx)

        return part

    def import_stock(
        self,
        admin_user_id: str,
        part_id: str,
        quantity: int,
        reference_doc: str
    ) -> SparePart:
        admin_user = self._repo.users.get(admin_user_id)
        if not admin_user or admin_user.role != UserRole.ADMIN:
            raise InventoryServiceError("Only Admin can import spare parts.")

        part = self._repo.parts.get(part_id)
        if not part:
            raise InventoryServiceError(f"Part {part_id} not found.")

        if quantity <= 0:
            raise InventoryServiceError("Import quantity must be strictly positive (FR_INV_02).")

        part.stock_quantity += quantity
        trx = PartTransaction(
            transaction_id=str(uuid.uuid4()),
            part_id=part_id,
            transaction_type=TransactionType.IMPORT,
            quantity=quantity,
            ticket_id=None,
            performed_by_user_id=admin_user_id,
            timestamp=self._clock.now(),
            reference_note=f"Receipt: {reference_doc}"
        )
        self._repo.transactions.append(trx)
        return part

    def allocate_part_to_ticket(
        self,
        admin_user_id: str,
        ticket_id: str,
        part_id: str,
        quantity: int,
        note: str = ""
    ) -> PartAllocation:
        admin_user = self._repo.users.get(admin_user_id)
        if not admin_user or admin_user.role != UserRole.ADMIN:
            raise InventoryServiceError("Only Admin can allocate parts to tickets.")

        ticket = self._repo.find_ticket_by_id(ticket_id)
        if not ticket:
            raise InventoryServiceError(f"Ticket {ticket_id} not found.")

        if ticket.status in [TicketStatus.RETURNED, TicketStatus.CANCELLED]:
            raise InventoryServiceError("Cannot allocate parts to completed or cancelled tickets (BR06).")

        part = self._repo.parts.get(part_id)
        if not part:
            raise InventoryServiceError(f"Part {part_id} not found.")

        if quantity <= 0:
            raise InventoryServiceError("Allocation quantity must be positive.")

        if part.stock_quantity < quantity:
            raise InventoryServiceError(
                f"Insufficient stock for {part.part_name}. Required: {quantity}, In stock: {part.stock_quantity}"
            )

        part.stock_quantity -= quantity
        now_dt = self._clock.now()

        existing_allocations = [
            a for a in self._repo.allocations.values()
            if a.ticket_id == ticket_id and a.part_id == part_id
        ]
        if existing_allocations:
            alloc = existing_allocations[0]
            alloc.allocated_quantity += quantity
        else:
            alloc_id = f"ALC_{uuid.uuid4().hex[:8].upper()}"
            alloc = PartAllocation(
                allocation_id=alloc_id,
                ticket_id=ticket_id,
                part_id=part_id,
                allocated_quantity=quantity,
                used_quantity=0,
                allocated_at=now_dt
            )
            self._repo.allocations[alloc_id] = alloc

        trx = PartTransaction(
            transaction_id=str(uuid.uuid4()),
            part_id=part_id,
            transaction_type=TransactionType.ALLOCATE,
            quantity=quantity,
            ticket_id=ticket_id,
            performed_by_user_id=admin_user_id,
            timestamp=now_dt,
            reference_note=note or f"Allocated for ticket {ticket_id}"
        )
        self._repo.transactions.append(trx)
        return alloc

    def record_part_usage(
        self,
        technician_user_id: str,
        ticket_id: str,
        part_id: str,
        used_quantity: int
    ) -> PartAllocation:
        ticket = self._repo.find_ticket_by_id(ticket_id)
        if not ticket:
            raise InventoryServiceError(f"Ticket {ticket_id} not found.")

        if ticket.current_technician_id != technician_user_id:
            raise InventoryServiceError(
                "Only the currently assigned technician can record part usage (BR04)."
            )

        if used_quantity <= 0:
            raise InventoryServiceError("Used quantity must be positive.")

        allocations = [
            a for a in self._repo.allocations.values()
            if a.ticket_id == ticket_id and a.part_id == part_id
        ]
        if not allocations:
            raise InventoryServiceError(
                f"Part {part_id} has not been allocated to ticket {ticket_id}."
            )

        alloc = allocations[0]
        if alloc.remaining_usable_quantity < used_quantity:
            raise InventoryServiceError(
                f"Cannot use {used_quantity}. Max remaining allocated is {alloc.remaining_usable_quantity} (BR06)."
            )

        alloc.used_quantity += used_quantity
        return alloc

    def get_low_stock_parts(self) -> List[SparePart]:
        return [p for p in self._repo.parts.values() if p.is_low_stock]
