
from datetime import date

from .domain_models import (
    User,
    Customer,
    Device,
    WarrantyTicket,
    SignedPartItem,
    StatusChangeLog
)

from .enums import (
    UserRole,
    TicketStatus,
    IntakeType
)


class PostgreSQLRepository:

    def __init__(self, connection):
        self.conn = connection

    # =====================================
    # USER
    # =====================================

    def get_user(self, user_id):

        row = self.conn.execute("""
            SELECT
                user_id,
                username,
                password_hash,
                full_name,
                role,
                is_active
            FROM users
            WHERE user_id = %s
        """, (user_id,)).fetchone()

        return User(**row) if row else None

    # =====================================
    # CUSTOMER
    # =====================================

    def get_customer(self, customer_id):

        row = self.conn.execute("""
            SELECT
                customer_id,
                full_name,
                phone_number,
                email,
                address
            FROM customers
            WHERE customer_id = %s
        """, (customer_id,)).fetchone()

        return Customer(**row) if row else None

    # =====================================
    # DEVICE
    # =====================================

    def get_device(self, device_id):

        row = self.conn.execute("""
            SELECT
                device_id,
                serial_number,
                model_name,
                brand,
                purchase_date
            FROM devices
            WHERE device_id = %s
        """, (device_id,)).fetchone()

        return Device(**row) if row else None

    # =====================================
    # TICKET NUMBER
    # =====================================

    def get_next_daily_ticket_number(
        self,
        target_date: date
    ) -> int:

        row = self.conn.execute("""
            SELECT fn_generate_ticket_id(%s)
                AS ticket_id
        """, (target_date,)).fetchone()

        ticket_id = row["ticket_id"]

        return int(ticket_id.rsplit("_", 1)[1])

    # =====================================
    # CREATE WARRANTY TICKET
    # =====================================

    def save_new_ticket(
        self,
        ticket: WarrantyTicket,
        admin_user_id: str
    ):

        admin = self.get_user(admin_user_id)
        customer = self.get_customer(ticket.customer_id)

        if not admin or not admin.is_active:
            raise ValueError("Invalid or inactive user")

        if admin.role != UserRole.ADMIN:
            raise ValueError("Only Admin can create tickets")

        if not customer:
            raise ValueError("Customer does not exist")

        if ticket.status != TicketStatus.RECEIVED:
            raise ValueError("Invalid initial ticket status")

        if ticket.intake_type == IntakeType.HOLD_FOR_REPAIR:
            if not ticket.signed_parts:
                raise ValueError("Signed components required")

            if not ticket.customer_intake_signature_confirmed:
                raise ValueError("Customer signature required")

        self.conn.execute("""
            INSERT INTO warranty_tickets (
                ticket_id,
                customer_id,
                device_id,
                created_by_user_id,
                contact_name,
                contact_phone,
                intake_type,
                promised_return_date,
                reported_issue,
                initial_condition,
                accessories_included,
                status,
                tracking_code_hash,
                current_technician_id,
                customer_signature_confirmed,
                final_return_confirmed,
                return_notes,
                cancellation_reason,
                created_at
            )
            VALUES (
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s
            )
        """, (
            ticket.ticket_id,
            ticket.customer_id,
            ticket.device_id,
            admin_user_id,
            customer.full_name,
            customer.phone_number,
            ticket.intake_type.value,
            ticket.promised_return_date,
            ticket.reported_issue,
            ticket.initial_condition,
            ticket.accessories_included,
            ticket.status.value,
            ticket.tracking_code_hash,
            ticket.current_technician_id,
            ticket.customer_intake_signature_confirmed,
            ticket.final_return_confirmed,
            ticket.return_notes,
            ticket.cancellation_reason,
            ticket.created_at
        ))

        # Save signed components

        for part in ticket.signed_parts:

            self.conn.execute("""
                INSERT INTO signed_components (
                    ticket_id,
                    part_name,
                    signature_mark,
                    notes
                )
                VALUES (%s, %s, %s, %s)
            """, (
                ticket.ticket_id,
                part.part_name,
                part.signature_mark,
                part.notes
            ))

        # Save ticket status history

        for log in ticket.status_history:

            self.conn.execute("""
                INSERT INTO ticket_status_history (
                    log_id,
                    ticket_id,
                    from_status,
                    to_status,
                    changed_by_user_id,
                    changed_at,
                    reason
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                log.log_id,
                log.ticket_id,
                log.from_status.value
                    if log.from_status else None,
                log.to_status.value,
                log.changed_by_user_id,
                log.changed_at,
                log.reason
            ))

        return ticket

    # =====================================
    # FIND WARRANTY TICKET
    # =====================================

    def find_ticket_by_id(self, ticket_id):

        row = self.conn.execute("""
            SELECT
                ticket_id,
                customer_id,
                device_id,
                intake_type,
                promised_return_date,
                reported_issue,
                initial_condition,
                accessories_included,
                status,
                tracking_code_hash,
                created_at,
                current_technician_id,
                customer_signature_confirmed
                    AS customer_intake_signature_confirmed,
                final_return_confirmed,
                return_notes,
                cancellation_reason

            FROM warranty_tickets
            WHERE ticket_id = %s

        """, (ticket_id,)).fetchone()

        if not row:
            return None

        row["status"] = TicketStatus(row["status"])

        row["intake_type"] = IntakeType(
            row["intake_type"]
        )

        ticket = WarrantyTicket(**row)

        # Load signed components

        parts = self.conn.execute("""
            SELECT
                part_name,
                signature_mark,
                notes
            FROM signed_components
            WHERE ticket_id = %s
            ORDER BY component_id
        """, (ticket_id,)).fetchall()

        ticket.signed_parts = [
            SignedPartItem(**part)
            for part in parts
        ]

        # Load status history

        logs = self.conn.execute("""
            SELECT
                log_id,
                ticket_id,
                from_status,
                to_status,
                changed_by_user_id,
                changed_at,
                reason
            FROM ticket_status_history
            WHERE ticket_id = %s
            ORDER BY changed_at, log_id
        """, (ticket_id,)).fetchall()

        for log in logs:

            log["from_status"] = (
                TicketStatus(log["from_status"])
                if log["from_status"] else None
            )

            log["to_status"] = TicketStatus(
                log["to_status"]
            )

            ticket.status_history.append(
                StatusChangeLog(**log)
            )

        return ticket

    def find_tickets(
        self,
        ticket_id=None,
        contact_query=None,
        serial_number=None
    ):

        conditions = []
        params = []

        if ticket_id:
            conditions.append("""
                strpos(
                    lower(t.ticket_id),
                    lower(%s)
                ) > 0
            """)
            params.append(ticket_id)

        if contact_query:
            conditions.append("""
                (
                    strpos(lower(t.contact_name),
                           lower(%s)) > 0
                    OR
                    strpos(lower(t.contact_phone),
                           lower(%s)) > 0
                )
            """)
            params.extend([
                contact_query,
                contact_query
            ])

        if serial_number:
            conditions.append("""
                strpos(
                    lower(coalesce(d.serial_number, '')),
                    lower(%s)
                ) > 0
            """)
            params.append(serial_number)

        sql = """
            SELECT t.ticket_id
            FROM warranty_tickets t
            JOIN devices d
                ON t.device_id = d.device_id
        """

        if conditions:
            sql += " WHERE " + " OR ".join(conditions)

        sql += " ORDER BY t.created_at DESC, t.ticket_id"

        rows = self.conn.execute(
            sql,
            tuple(params)
        ).fetchall()

        return [
            self.find_ticket_by_id(row["ticket_id"])
            for row in rows
        ]