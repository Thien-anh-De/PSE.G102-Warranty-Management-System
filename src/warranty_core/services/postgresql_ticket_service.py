
import hashlib
import uuid

from datetime import datetime, timezone, timedelta

from psycopg import IntegrityError

from ..database import get_connection

from ..postgresql_repository import PostgreSQLRepository

from ..domain_models import (
    WarrantyTicket,
    StatusChangeLog
)

from ..enums import (
    TicketStatus,
    IntakeType,
    UserRole
)

from .ticket_service import TicketServiceError


VIETNAM_TZ = timezone(timedelta(hours=7))


class PostgreSQLTicketService:

    def __init__(self, connection_factory=get_connection):
        self._connection_factory = connection_factory

    # =====================================
    # CREATE WARRANTY TICKET
    # =====================================

    def create_ticket(
        self,
        admin_user_id,
        customer_id,
        device_id,
        intake_type,
        promised_return_date,
        reported_issue,
        initial_condition,
        accessories_included,
        plain_secret_code,
        signed_parts=None,
        customer_signature_confirmed=False
    ):

        try:

            with self._connection_factory() as conn:

                repo = PostgreSQLRepository(conn)

                # Validate Admin

                admin = repo.get_user(admin_user_id)

                if (
                    not admin
                    or not admin.is_active
                    or admin.role != UserRole.ADMIN
                ):

                    raise TicketServiceError(
                        "Only active Admin users can "
                        "create warranty tickets."
                    )

                # Validate customer

                if not repo.get_customer(customer_id):

                    raise TicketServiceError(
                        f"Customer {customer_id} does not exist."
                    )

                # Validate device

                if not repo.get_device(device_id):

                    raise TicketServiceError(
                        f"Device {device_id} does not exist."
                    )

                # Validate ticket information

                if not reported_issue or not initial_condition:

                    raise TicketServiceError(
                        "Reported issue and initial "
                        "condition are mandatory."
                    )

                now = datetime.now(VIETNAM_TZ)
                today = now.date()

                if promised_return_date < today:

                    raise TicketServiceError(
                        "Promised return date "
                        "cannot be in the past."
                    )

                parts = signed_parts or []

                # BR02: Hold-for-repair validation

                if intake_type == IntakeType.HOLD_FOR_REPAIR:

                    if not parts:

                        raise TicketServiceError(
                            "Hold-for-repair intake requires "
                            "inspection and signing of "
                            "components (BR02)."
                        )

                    if not customer_signature_confirmed:

                        raise TicketServiceError(
                            "Hold-for-repair intake requires "
                            "verified customer signature "
                            "handover (BR02)."
                        )

                # Generate ticket ID

                sequence = (
                    repo.get_next_daily_ticket_number(today)
                )

                ticket_id = (
                    f"TKT_{today:%Y%m%d}_{sequence}"
                )

                # Hash customer tracking code

                tracking_hash = hashlib.sha256(
                    plain_secret_code.encode("utf-8")
                ).hexdigest()

                # Create ticket object

                ticket = WarrantyTicket(
                    ticket_id=ticket_id,
                    customer_id=customer_id,
                    device_id=device_id,
                    intake_type=intake_type,
                    promised_return_date=promised_return_date,
                    reported_issue=reported_issue,
                    initial_condition=initial_condition,
                    accessories_included=accessories_included,
                    status=TicketStatus.RECEIVED,
                    tracking_code_hash=tracking_hash,
                    created_at=now,
                    signed_parts=parts,
                    customer_intake_signature_confirmed=(
                        customer_signature_confirmed
                    )
                )

                # Create status history

                initial_log = StatusChangeLog(
                    log_id=str(uuid.uuid4()),
                    ticket_id=ticket_id,
                    from_status=None,
                    to_status=TicketStatus.RECEIVED,
                    changed_by_user_id=admin_user_id,
                    changed_at=now,
                    reason=(
                        "Ticket created upon "
                        "initial device intake"
                    )
                )

                ticket.status_history.append(initial_log)

                # Save to PostgreSQL

                repo.save_new_ticket(
                    ticket,
                    admin_user_id
                )

                return ticket

        except IntegrityError as error:

            raise TicketServiceError(
                "Ticket data violates database constraints."
            ) from error

    # =====================================
    # FIND WARRANTY TICKETS
    # =====================================

    def find_tickets(
        self,
        ticket_id=None,
        contact_query=None,
        serial_number=None
    ):

        with self._connection_factory() as conn:

            repo = PostgreSQLRepository(conn)

            return repo.find_tickets(
                ticket_id=ticket_id,
                contact_query=contact_query,
                serial_number=serial_number
            )
