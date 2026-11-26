"""Opt-in, fictional data for demonstrating the customer portal locally."""

import argparse
from datetime import date, datetime, timezone
from typing import List, Tuple

from src.warranty_app.dependencies import AppContainer
from src.warranty_core import (
    DefectOrigin,
    Device,
    IntakeType,
    RepairService,
    SignedPartItem,
    TicketStatus,
    User,
    UserRole,
    WarrantyService,
)


def seed_portal_demo_data(container: AppContainer) -> List[Tuple[str, str, str]]:
    if container.repository.tickets:
        raise ValueError("Demo data must be loaded into an empty in-memory repository.")
    container.clock_service.set_time(datetime(2026, 11, 26, 3, 0, tzinfo=timezone.utc))
    repo = container.repository
    repo.users["USR_TECH_01"] = User(
        user_id="USR_TECH_01", username="demo_technician", password_hash="demo_only",
        full_name="Kỹ thuật viên minh họa", role=UserRole.TECHNICIAN,
    )
    warranty_service = WarrantyService(repo, container.clock_service)
    repair_service = RepairService(repo, container.clock_service)
    samples = [
        ("Dell XPS 15 9520", "Dell", "SN-DELL-889900", TicketStatus.UNDER_REPAIR),
        ("ASUS Vivobook 15", "ASUS", "SN-ASUS-222244", TicketStatus.WAITING_FOR_PARTS),
        ("HP ProBook 440", "HP", "SN-HP-334455", TicketStatus.WAITING_FOR_RETURN),
        ("Lenovo ThinkPad T14", "Lenovo", "SN-LENOVO-556677", TicketStatus.CANCELLED),
    ]
    lookups = []
    for index, (model, brand, serial, target_status) in enumerate(samples, start=1):
        device_id = f"DEV_DEMO_{index}"
        repo.devices[device_id] = Device(
            device_id=device_id, serial_number=serial, model_name=model,
            brand=brand, purchase_date=date(2026, 10, 1),
        )
        secret_code = f"HT-DEMO-{index:03d}"
        ticket = container.ticket_service.create_ticket(
            admin_user_id="USR_ADMIN_01", customer_id="CUST_001", device_id=device_id,
            intake_type=IntakeType.HOLD_FOR_REPAIR,
            promised_return_date=date(2026, 11, 28),
            reported_issue="Dữ liệu minh họa cho bài tập lớn.",
            initial_condition="Thiết bị minh họa, không phải hồ sơ khách hàng thật.",
            accessories_included="Bộ sạc minh họa", plain_secret_code=secret_code,
            signed_parts=[SignedPartItem(part_name="RAM", signature_mark="DEMO_SIGNATURE")],
            customer_signature_confirmed=True,
        )
        if target_status == TicketStatus.CANCELLED:
            container.ticket_service.cancel_ticket_pre_repair(
                admin_user_id="USR_ADMIN_01", ticket_id=ticket.ticket_id,
                cancellation_reason="Tình huống hủy phiếu minh họa.",
                device_returned_to_customer=True,
            )
        else:
            warranty_service.evaluate_and_record_policy(
                admin_user_id="USR_ADMIN_01", ticket_id=ticket.ticket_id,
                purchase_date=date(2026, 10, 1), incident_date=date(2026, 11, 26),
                is_warranty_valid=True, defect_origin=DefectOrigin.MANUFACTURER,
                customer_agreed=True,
            )
            repair_service.assign_technician(
                admin_user_id="USR_ADMIN_01", ticket_id=ticket.ticket_id,
                technician_user_id="USR_TECH_01",
            )
            transitions = [TicketStatus.UNDER_REPAIR]
            if target_status == TicketStatus.WAITING_FOR_PARTS:
                transitions.append(TicketStatus.WAITING_FOR_PARTS)
            elif target_status == TicketStatus.WAITING_FOR_RETURN:
                transitions.extend([TicketStatus.WAITING_FOR_RESULT_CHECK, TicketStatus.WAITING_FOR_RETURN])
            for new_status in transitions:
                repair_service.update_repair_status(
                    technician_user_id="USR_TECH_01", ticket_id=ticket.ticket_id,
                    new_status=new_status, reason="Chuyển trạng thái minh họa.",
                    diagnosis_findings="Kết quả kiểm tra minh họa.",
                    actions_performed="Thao tác xử lý minh họa.", pending_tasks="Theo tình huống demo.",
                )
        lookups.append((ticket.ticket_id, secret_code, ticket.status.value))
    return lookups


def main() -> None:
    import uvicorn

    from src.warranty_app import dependencies
    from src.warranty_app.main import app, frontend_directory

    parser = argparse.ArgumentParser(description="Chạy cổng bảo hành với dữ liệu minh họa trong RAM.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=3000)
    args = parser.parse_args()
    if not frontend_directory.is_dir():
        parser.error("Chưa có giao diện. Chạy npm ci và npm run build trong thư mục frontend trước.")
    lookups = seed_portal_demo_data(dependencies.container)
    print("\nCHẾ ĐỘ MINH HỌA — chỉ có dữ liệu giả, mất khi dừng ứng dụng.")
    for ticket_id, secret_code, status in lookups:
        print(f"{ticket_id} | {secret_code} | {status}")
    print(f"Mở http://{args.host}:{args.port}\n")
    uvicorn.run(app, host=args.host, port=args.port)


if __name__ == "__main__":
    main()
