"""Opt-in fictional PostgreSQL records for trying the customer lookup portal."""

from datetime import datetime, timedelta
import hashlib

from src.warranty_core import IntakeType, SignedPartItem
from src.warranty_core.database import get_connection
from src.warranty_core.services.postgresql_ticket_service import PostgreSQLTicketService, VIETNAM_TZ


ADMIN_ID = "USR_PORTAL_DEMO"
CUSTOMER_ID = "CUST_PORTAL_DEMO"
DEVICE_ID = "DEV_PORTAL_DEMO"
SECRET_CODE = "HT-SQL-DEMO-001"


def seed_demo_ticket():
    """Add fictional prerequisites and reuse the ticket when run again."""
    with get_connection() as connection:
        connection.execute(
            """INSERT INTO users (user_id, username, password_hash, full_name, role)
               VALUES (%s, %s, %s, %s, 'ADMIN') ON CONFLICT (user_id) DO NOTHING""",
            (ADMIN_ID, "portal_demo_admin", "DEMO_ONLY_NO_LOGIN", "Quản trị viên minh họa"),
        )
        connection.execute(
            """INSERT INTO customers (customer_id, full_name, phone_number)
               VALUES (%s, %s, %s) ON CONFLICT (customer_id) DO NOTHING""",
            (CUSTOMER_ID, "Khách hàng minh họa", "0900000000"),
        )
        connection.execute(
            """INSERT INTO devices (device_id, serial_number, model_name, brand)
               VALUES (%s, %s, %s, %s) ON CONFLICT (device_id) DO NOTHING""",
            (DEVICE_ID, "SN-SQL-DEMO-9900", "Dell XPS 15 9520", "Dell"),
        )
        existing = connection.execute(
            """SELECT ticket_id FROM warranty_tickets
               WHERE customer_id = %s AND device_id = %s AND tracking_code_hash = %s
               ORDER BY created_at DESC LIMIT 1""",
            (CUSTOMER_ID, DEVICE_ID, hashlib.sha256(SECRET_CODE.encode()).hexdigest()),
        ).fetchone()

    if existing:
        return existing["ticket_id"]

    ticket = PostgreSQLTicketService().create_ticket(
        admin_user_id=ADMIN_ID, customer_id=CUSTOMER_ID, device_id=DEVICE_ID,
        intake_type=IntakeType.HOLD_FOR_REPAIR,
        promised_return_date=datetime.now(VIETNAM_TZ).date() + timedelta(days=3),
        reported_issue="Sự cố minh họa cho bài tập lớn.",
        initial_condition="Thiết bị minh họa, không phải hồ sơ khách hàng thực tế.",
        accessories_included="Bộ sạc minh họa", plain_secret_code=SECRET_CODE,
        signed_parts=[SignedPartItem(part_name="RAM", signature_mark="PORTAL_DEMO_SIGNATURE")],
        customer_signature_confirmed=True,
    )
    return ticket.ticket_id


if __name__ == "__main__":
    ticket_id = seed_demo_ticket()
    print("DỮ LIỆU MINH HỌA ĐÃ LƯU TRONG POSTGRESQL")
    print(f"Mã phiếu: {ticket_id}")
    print(f"Mã tra cứu: {SECRET_CODE}")
    print("Dùng lệnh uvicorn trong hướng dẫn để tra cứu từ PostgreSQL.")
