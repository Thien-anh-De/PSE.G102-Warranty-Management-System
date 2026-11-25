from pydantic import BaseModel


class AppConfig(BaseModel):
    """Configuration for the ticket intake application layer."""

    app_name: str = "PSE.G102 Warranty Management - Ticket Intake Module"
    app_version: str = "0.1.0"
    api_prefix: str = "/api/v1"


def get_config() -> AppConfig:
    return AppConfig()