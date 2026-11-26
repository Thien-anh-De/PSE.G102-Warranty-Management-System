import os
from datetime import date, datetime, timezone
from typing import Iterator

from fastapi import HTTPException
from psycopg import Error as DatabaseError

from src.warranty_core import (
    Customer,
    Device,
    InMemoryRepository,
    PortalService,
    SimulatedClockService,
    TicketService,
    User,
    UserRole,
)

from src.warranty_app.config import get_config
from src.warranty_app.portal_rate_limiter import PortalRateLimiter
from src.warranty_core.database import get_connection
from src.warranty_core.postgresql_repository import PostgreSQLRepository
from src.warranty_core.services.postgresql_ticket_service import (
    PostgreSQLTicketService
)


class AppContainer:
    """Memory services for local demos and tests.

    Request dependencies select PostgreSQL when configured. Database connections
    belong to individual requests and are never stored in this shared container.
    """

    def __init__(self) -> None:
        self.repository = InMemoryRepository()
        self.clock_service = SimulatedClockService(datetime.now(timezone.utc))
        self.ticket_service = TicketService(self.repository, self.clock_service)
        self.portal_service = PortalService(self.repository)
        config = get_config()
        self.portal_rate_limiter = PortalRateLimiter(
            max_attempts=config.portal_lookup_max_attempts,
            window_seconds=config.portal_lookup_window_seconds,
        )
        self.seed_demo_data()

    def seed_demo_data(self) -> None:
        """Seed minimal data for local demo of the ticket intake module."""
        if self.repository.users:
            return

        admin = User(
            user_id="USR_ADMIN_01",
            username="admin1",
            password_hash="hash_admin1",
            full_name="System Administrator",
            role=UserRole.ADMIN,
            is_active=True,
        )
        customer = Customer(
            customer_id="CUST_001",
            full_name="Nguyen Van A",
            phone_number="0987654321",
            email="nguyenvana@example.com",
            address="123 Nguyen Trai, Ha Noi",
        )
        device = Device(
            device_id="DEV_001",
            serial_number="SN-DELL-889900",
            model_name="Dell XPS 15 9520",
            brand="Dell",
            purchase_date=date(2026, 10, 1),
        )
        self.repository.users[admin.user_id] = admin
        self.repository.customers[customer.customer_id] = customer
        self.repository.devices[device.device_id] = device


container = AppContainer()


def reset_container() -> AppContainer:
    global container
    container = AppContainer()
    return container


def get_storage_mode() -> str:
    """Use the same storage selection for ticket intake and customer lookup."""
    storage = os.getenv("WARRANTY_STORAGE", "memory").strip().lower()
    if storage not in {"memory", "postgresql"}:
        raise ValueError(f"Unsupported storage mode: {storage}")
    return storage


def get_ticket_service():
    if get_storage_mode() == "postgresql":
        return PostgreSQLTicketService()
    return container.ticket_service


def get_repository() -> InMemoryRepository:
    return container.repository


def get_portal_service() -> Iterator[PortalService]:
    if get_storage_mode() == "memory":
        yield container.portal_service
        return

    try:
        # Every lookup owns its connection; concurrent requests share no cursor
        # or transaction. The connection closes after success or verification failure.
        with get_connection() as connection:
            yield PortalService(PostgreSQLRepository(connection))
    except DatabaseError:
        raise HTTPException(
            status_code=503,
            detail="Hệ thống tra cứu tạm thời không khả dụng. Vui lòng thử lại sau.",
        ) from None


def get_portal_rate_limiter() -> PortalRateLimiter:
    return container.portal_rate_limiter
