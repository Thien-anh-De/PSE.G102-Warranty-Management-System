import os

from pydantic import BaseModel, Field


class AppConfig(BaseModel):
    """Configuration for the ticket intake application layer."""

    app_name: str = "PSE.G102 Warranty Management - Ticket Intake Module"
    app_version: str = "0.1.0"
    api_prefix: str = "/api/v1"
    portal_lookup_max_attempts: int = Field(default=5, ge=1, le=1000)
    portal_lookup_window_seconds: int = Field(default=60, ge=1, le=86400)


def get_config() -> AppConfig:
    return AppConfig(
        portal_lookup_max_attempts=int(os.getenv("PORTAL_LOOKUP_MAX_ATTEMPTS", "5")),
        portal_lookup_window_seconds=int(os.getenv("PORTAL_LOOKUP_WINDOW_SECONDS", "60")),
    )
