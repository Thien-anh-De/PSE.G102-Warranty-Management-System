import pytest
from datetime import datetime, date, timezone
from src.warranty_core import (
    InMemoryRepository,
    SimulatedClockService,
    MockEmailService,
    TicketService,
    WarrantyService,
    RepairService,
    InventoryService,
    SlaService,
    PortalService,
    User,
    UserRole,
    Customer,
    Device
)

@pytest.fixture
def repo():
    r = InMemoryRepository()
    admin = User(
        user_id="USR_ADMIN_01",
        username="admin1",
        password_hash="hash_admin1",
        full_name="System Administrator",
        role=UserRole.ADMIN,
        is_active=True
    )
    tech1 = User(
        user_id="USR_TECH_01",
        username="tech1",
        password_hash="hash_tech1",
        full_name="Technician One",
        role=UserRole.TECHNICIAN,
        is_active=True
    )
    tech2 = User(
        user_id="USR_TECH_02",
        username="tech2",
        password_hash="hash_tech2",
        full_name="Technician Two",
        role=UserRole.TECHNICIAN,
        is_active=True
    )
    r.users[admin.user_id] = admin
    r.users[tech1.user_id] = tech1
    r.users[tech2.user_id] = tech2

    cust = Customer(
        customer_id="CUST_001",
        full_name="Nguyen Van A",
        phone_number="0987654321",
        email="nguyenvana@example.com",
        address="123 Nguyen Trai, Ha Noi"
    )
    r.customers[cust.customer_id] = cust

    dev = Device(
        device_id="DEV_001",
        serial_number="SN-DELL-889900",
        model_name="Dell XPS 15 9520",
        brand="Dell",
        purchase_date=date(2026, 10, 1)
    )
    r.devices[dev.device_id] = dev

    return r

@pytest.fixture
def clock():
    fixed_time = datetime(2026, 11, 24, 8, 0, 0, tzinfo=timezone.utc)
    return SimulatedClockService(fixed_time)

@pytest.fixture
def email_service():
    return MockEmailService()

@pytest.fixture
def ticket_service(repo, clock):
    return TicketService(repo, clock)

@pytest.fixture
def warranty_service(repo, clock):
    return WarrantyService(repo, clock)

@pytest.fixture
def repair_service(repo, clock):
    return RepairService(repo, clock)

@pytest.fixture
def inventory_service(repo, clock):
    return InventoryService(repo, clock)

@pytest.fixture
def sla_service(repo, clock, email_service):
    return SlaService(repo, clock, email_service)

@pytest.fixture
def portal_service(repo):
    return PortalService(repo)
