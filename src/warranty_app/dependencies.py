from datetime import date, datetime, timezone

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


class AppContainer:
    """Simple dependency container for the ticket intake module.

    This keeps technology setup isolated from the domain core. The repository is
    in-memory for local demo/testing; it can be replaced by a persistent
    repository implementation without changing the ticket service.
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


def get_ticket_service() -> TicketService:
    return container.ticket_service


def get_repository() -> InMemoryRepository:
    return container.repository


def get_portal_service() -> PortalService:
    return container.portal_service


def get_portal_rate_limiter() -> PortalRateLimiter:
    return container.portal_rate_limiter
