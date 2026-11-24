from typing import Dict, List, Optional
from datetime import date
from .domain_models import (
    User,
    Customer,
    Device,
    WarrantyTicket,
    WarrantyAssessment,
    SparePart,
    PartAllocation,
    PartTransaction,
    HandoverSession
)

class InMemoryRepository:
    def __init__(self):
        self.users: Dict[str, User] = {}
        self.customers: Dict[str, Customer] = {}
        self.devices: Dict[str, Device] = {}
        self.tickets: Dict[str, WarrantyTicket] = {}
        self.assessments: Dict[str, WarrantyAssessment] = {}
        self.parts: Dict[str, SparePart] = {}
        self.allocations: Dict[str, PartAllocation] = {}
        self.transactions: List[PartTransaction] = []
        self.handovers: Dict[str, HandoverSession] = {}
        self._daily_ticket_counters: Dict[date, int] = {}

    def get_next_daily_ticket_number(self, target_date: date) -> int:
        current = self._daily_ticket_counters.get(target_date, 0)
        nxt = current + 1
        self._daily_ticket_counters[target_date] = nxt
        return nxt

    def find_user_by_username(self, username: str) -> Optional[User]:
        for user in self.users.values():
            if user.username == username:
                return user
        return None

    def find_ticket_by_id(self, ticket_id: str) -> Optional[WarrantyTicket]:
        return self.tickets.get(ticket_id)

    def find_device_by_serial(self, serial: str) -> Optional[Device]:
        for d in self.devices.values():
            if d.serial_number == serial:
                return d
        return None

    def find_part_by_code(self, code: str) -> Optional[SparePart]:
        for p in self.parts.values():
            if p.part_code == code:
                return p
        return None

    def get_allocations_for_ticket(self, ticket_id: str) -> List[PartAllocation]:
        return [a for a in self.allocations.values() if a.ticket_id == ticket_id]

    def get_pending_handover_for_ticket(self, ticket_id: str) -> Optional[HandoverSession]:
        from .enums import HandoverStatus
        for h in self.handovers.values():
            if h.ticket_id == ticket_id and h.status == HandoverStatus.PENDING:
                return h
        return None
