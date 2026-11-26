import time
import pytest
from datetime import datetime, date, timedelta, timezone

from src.warranty_core.domain_models import WarrantyTicket, Device
from src.warranty_core.enums import TicketStatus, IntakeType
from src.warranty_core.services.dashboard_service import DashboardService, DashboardServiceError


@pytest.fixture
def dashboard_service(repo, clock):
    return DashboardService(repo, clock)


def _create_sample_ticket(
    ticket_id: str,
    device_id: str,
    status: TicketStatus,
    created_at: datetime,
    promised_return_date: date,
    tech_id: str = None,
) -> WarrantyTicket:
    return WarrantyTicket(
        ticket_id=ticket_id,
        customer_id="CUST_001",
        device_id=device_id,
        intake_type=IntakeType.HOLD_FOR_REPAIR,
        promised_return_date=promised_return_date,
        reported_issue="Loi man hinh",
        initial_condition="Binh thuong",
        accessories_included="Sac",
        status=status,
        tracking_code_hash="hash_secret",
        created_at=created_at,
        current_technician_id=tech_id,
    )


def test_dashboard_rbac_denies_technician(dashboard_service):
    """T06 / NFR_SEC_01: Từ chối 100% truy cập trái quyền từ Kỹ thuật viên."""
    with pytest.raises(DashboardServiceError):
        dashboard_service.get_dashboard_summary(actor_user_id="USR_TECH_01")


def test_dashboard_kpi_and_multi_filter_accuracy(repo, dashboard_service):
    """T11 / FR_DASH_01 & FR_DASH_02: Kiểm tra độ chính xác 100% số liệu tổng hợp và bộ lọc đồng thời."""
    dev2 = Device(
        device_id="DEV_002",
        serial_number="SN-ASUS-112233",
        model_name="Asus ROG Strix G15",
        brand="Asus",
    )
    repo.devices[dev2.device_id] = dev2

    repo.tickets["TKT_20261118_1"] = _create_sample_ticket(
        "TKT_20261118_1",
        "DEV_001",
        TicketStatus.UNDER_REPAIR,
        datetime(2026, 11, 18, 9, 0, tzinfo=timezone.utc),
        date(2026, 11, 20),
        "USR_TECH_01",
    )
    repo.tickets["TKT_20261121_1"] = _create_sample_ticket(
        "TKT_20261121_1",
        "DEV_002",
        TicketStatus.WAITING_FOR_PARTS,
        datetime(2026, 11, 21, 10, 0, tzinfo=timezone.utc),
        date(2026, 11, 26),
        "USR_TECH_01",
    )
    repo.tickets["TKT_20261115_1"] = _create_sample_ticket(
        "TKT_20261115_1",
        "DEV_001",
        TicketStatus.RETURNED,
        datetime(2026, 11, 15, 8, 30, tzinfo=timezone.utc),
        date(2026, 11, 19),
        "USR_TECH_02",
    )

    all_summary = dashboard_service.get_dashboard_summary(actor_user_id="USR_ADMIN_01")
    assert all_summary["total_tickets"] == 3
    assert all_summary["overdue_tickets"] == 1
    assert all_summary["by_status"][TicketStatus.UNDER_REPAIR.value] == 1
    assert all_summary["by_status"][TicketStatus.WAITING_FOR_PARTS.value] == 1
    assert all_summary["by_status"][TicketStatus.RETURNED.value] == 1

    filtered_summary = dashboard_service.get_dashboard_summary(
        actor_user_id="USR_ADMIN_01",
        start_date=date(2026, 11, 20),
        end_date=date(2026, 11, 24),
        technician_id="USR_TECH_01",
        model_name="Asus",
    )
    assert filtered_summary["total_tickets"] == 1
    assert filtered_summary["overdue_tickets"] == 0
    assert filtered_summary["by_status"][TicketStatus.WAITING_FOR_PARTS.value] == 1


def test_dashboard_export_excel_and_pdf(repo, dashboard_service):
    """FR_DASH_03 / T13: Xuất báo cáo Excel và PDF A4 có đầy đủ thông tin chốt dữ liệu và bộ lọc."""
    repo.tickets["TKT_20261124_1"] = _create_sample_ticket(
        "TKT_20261124_1",
        "DEV_001",
        TicketStatus.UNDER_INSPECTION,
        datetime(2026, 11, 24, 8, 0, tzinfo=timezone.utc),
        date(2026, 11, 27),
        "USR_TECH_01",
    )

    excel_text = dashboard_service.export_report_excel(
        actor_user_id="USR_ADMIN_01", model_name="Dell"
    ).read().decode("utf-8-sig")
    assert "Thoi diem chot du lieu" in excel_text
    assert "Dell" in excel_text
    assert "Tong so phieu theo bo loc,1" in excel_text

    pdf_bytes = dashboard_service.export_report_pdf(
        actor_user_id="USR_ADMIN_01", model_name="Dell"
    ).read()
    assert pdf_bytes.startswith(b"%PDF-1.4")
    assert b"/MediaBox [0 0 595 842]" in pdf_bytes
    assert b"Dell" in pdf_bytes


def test_dashboard_performance_with_5000_tickets(repo, dashboard_service):
    """TB.11 & T12 / NFR_PERF_02: Nạp 5.000 phiếu, tải thống kê <= 2s và xuất báo cáo <= 3s."""
    base_dt = datetime(2026, 11, 1, 8, 0, tzinfo=timezone.utc)
    statuses = list(TicketStatus)

    for i in range(5000):
        tid = f"TKT_PERF_{i:04d}"
        st = statuses[i % len(statuses)]
        tech = "USR_TECH_01" if i % 2 == 0 else "USR_TECH_02"
        repo.tickets[tid] = _create_sample_ticket(
            tid,
            "DEV_001",
            st,
            base_dt + timedelta(hours=i % 500),
            date(2026, 11, 20) + timedelta(days=i % 10),
            tech,
        )

    t0 = time.perf_counter()
    summary = dashboard_service.get_dashboard_summary(actor_user_id="USR_ADMIN_01")
    elapsed_summary = time.perf_counter() - t0

    assert summary["total_tickets"] == 5000
    assert elapsed_summary <= 2.0

    t1 = time.perf_counter()
    dashboard_service.export_report_excel(actor_user_id="USR_ADMIN_01")
    dashboard_service.export_report_pdf(actor_user_id="USR_ADMIN_01")
    elapsed_export = time.perf_counter() - t1

    assert elapsed_export <= 3.0