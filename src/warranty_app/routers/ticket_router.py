from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from src.warranty_app.dependencies import get_ticket_service
from src.warranty_app.schemas.ticket_schema import (
    CreateTicketRequest,
    ErrorResponse,
    SignedPartItemSchema,
    StatusChangeLogSchema,
    TicketListResponse,
    TicketResponse,
)
from src.warranty_core import SignedPartItem, TicketService, TicketServiceError

router = APIRouter(prefix="/tickets", tags=["Ticket Intake"])


def to_ticket_response(ticket) -> TicketResponse:
    return TicketResponse(
        ticket_id=ticket.ticket_id,
        customer_id=ticket.customer_id,
        device_id=ticket.device_id,
        intake_type=ticket.intake_type,
        promised_return_date=ticket.promised_return_date,
        reported_issue=ticket.reported_issue,
        initial_condition=ticket.initial_condition,
        accessories_included=ticket.accessories_included,
        status=ticket.status,
        created_at=ticket.created_at,
        current_technician_id=ticket.current_technician_id,
        signed_parts=[
            SignedPartItemSchema(
                part_name=p.part_name,
                signature_mark=p.signature_mark,
                notes=p.notes,
            )
            for p in ticket.signed_parts
        ],
        customer_intake_signature_confirmed=ticket.customer_intake_signature_confirmed,
        status_history=[
            StatusChangeLogSchema(
                log_id=log.log_id,
                from_status=log.from_status,
                to_status=log.to_status,
                changed_by_user_id=log.changed_by_user_id,
                changed_at=log.changed_at,
                reason=log.reason,
            )
            for log in ticket.status_history
        ],
    )


@router.post(
    "",
    response_model=TicketResponse,
    status_code=201,
    responses={400: {"model": ErrorResponse}},
    summary="Tiếp nhận và tạo phiếu bảo hành",
)
def create_ticket(
    payload: CreateTicketRequest,
    ticket_service: TicketService = Depends(get_ticket_service),
) -> TicketResponse:
    try:
        ticket = ticket_service.create_ticket(
            admin_user_id=payload.admin_user_id,
            customer_id=payload.customer_id,
            device_id=payload.device_id,
            intake_type=payload.intake_type,
            promised_return_date=payload.promised_return_date,
            reported_issue=payload.reported_issue,
            initial_condition=payload.initial_condition,
            accessories_included=payload.accessories_included,
            plain_secret_code=payload.plain_secret_code,
            signed_parts=[
                SignedPartItem(
                    part_name=item.part_name,
                    signature_mark=item.signature_mark,
                    notes=item.notes,
                )
                for item in payload.signed_parts
            ],
            customer_signature_confirmed=payload.customer_signature_confirmed,
        )
        return to_ticket_response(ticket)
    except TicketServiceError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get(
    "",
    response_model=TicketListResponse,
    summary="Danh sách/tìm kiếm phiếu tiếp nhận",
)
def list_tickets(
    ticket_id: Optional[str] = Query(default=None, description="Mã phiếu"),
    contact_query: Optional[str] = Query(default=None, description="Tên/SĐT khách hàng"),
    serial_number: Optional[str] = Query(default=None, description="Số serial thiết bị"),
    ticket_service: TicketService = Depends(get_ticket_service),
) -> TicketListResponse:
    tickets = ticket_service.find_tickets(
        ticket_id=ticket_id,
        contact_query=contact_query,
        serial_number=serial_number,
    )
    items = [to_ticket_response(ticket) for ticket in tickets]
    return TicketListResponse(total=len(items), items=items)


@router.get(
    "/{ticket_id}",
    response_model=TicketResponse,
    responses={404: {"model": ErrorResponse}},
    summary="Chi tiết phiếu tiếp nhận",
)
def get_ticket(
    ticket_id: str,
    ticket_service: TicketService = Depends(get_ticket_service),
) -> TicketResponse:
    tickets = ticket_service.find_tickets(ticket_id=ticket_id)
    exact = [ticket for ticket in tickets if ticket.ticket_id == ticket_id]
    if not exact:
        raise HTTPException(status_code=404, detail=f"Ticket {ticket_id} not found.")
    return to_ticket_response(exact[0])