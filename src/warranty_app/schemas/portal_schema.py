from datetime import date

from pydantic import BaseModel, ConfigDict, Field, SecretStr, field_validator

from src.warranty_core import TicketStatus


class PortalLookupRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ticket_id: str = Field(min_length=1, max_length=64)
    plain_secret_code: SecretStr = Field(min_length=1, max_length=256)

    @field_validator("ticket_id", mode="before")
    @classmethod
    def strip_ticket_id(cls, value):
        return value.strip() if isinstance(value, str) else value

    @field_validator("plain_secret_code")
    @classmethod
    def reject_blank_secret(cls, value: SecretStr) -> SecretStr:
        if not value.get_secret_value().strip():
            raise ValueError("Lookup code is required.")
        return value


class PortalLookupResponse(BaseModel):
    """The explicit allowlist of fields available to a customer."""

    ticket_id: str
    device_model: str
    device_serial_masked: str
    status: TicketStatus
    promised_return_date: date
