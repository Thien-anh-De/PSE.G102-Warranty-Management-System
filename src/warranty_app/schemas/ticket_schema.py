from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from src.warranty_core import IntakeType, TicketStatus


class SignedPartItemSchema(BaseModel):
    part_name: str = Field(..., min_length=1, description="Tên linh kiện được ký nhận")
    signature_mark: str = Field(..., min_length=1, description="Ký hiệu/chữ ký đối chiếu")
    notes: Optional[str] = Field(default=None, description="Ghi chú bổ sung")


class CreateTicketRequest(BaseModel):
    admin_user_id: str = Field(..., description="Mã Admin thực hiện tiếp nhận")
    customer_id: str = Field(..., description="Mã khách hàng")
    device_id: str = Field(..., description="Mã thiết bị")
    intake_type: IntakeType = Field(..., description="Loại tiếp nhận: SAME_DAY hoặc HOLD_FOR_REPAIR")
    promised_return_date: date = Field(..., description="Ngày hẹn trả")
    reported_issue: str = Field(..., min_length=1, description="Lỗi/tình trạng khách báo")
    initial_condition: str = Field(..., min_length=1, description="Tình trạng ban đầu khi tiếp nhận")
    accessories_included: str = Field(..., description="Phụ kiện đi kèm")
    plain_secret_code: str = Field(..., min_length=4, description="Mã bí mật để khách tra cứu")
    signed_parts: List[SignedPartItemSchema] = Field(default_factory=list)
    customer_signature_confirmed: bool = Field(default=False)


class StatusChangeLogSchema(BaseModel):
    log_id: str
    from_status: Optional[TicketStatus]
    to_status: TicketStatus
    changed_by_user_id: str
    changed_at: datetime
    reason: str


class TicketResponse(BaseModel):
    ticket_id: str
    customer_id: str
    device_id: str
    intake_type: IntakeType
    promised_return_date: date
    reported_issue: str
    initial_condition: str
    accessories_included: str
    status: TicketStatus
    created_at: datetime
    current_technician_id: Optional[str]
    signed_parts: List[SignedPartItemSchema]
    customer_intake_signature_confirmed: bool
    status_history: List[StatusChangeLogSchema]


class TicketListResponse(BaseModel):
    total: int
    items: List[TicketResponse]


class ErrorResponse(BaseModel):
    detail: str