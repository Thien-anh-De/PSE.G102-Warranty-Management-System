from fastapi import FastAPI

from src.warranty_app.config import get_config
from src.warranty_app.routers.ticket_router import router as ticket_router

config = get_config()

app = FastAPI(
    title=config.app_name,
    version=config.app_version,
    description="Module tiếp nhận phiếu bảo hành (Nguyễn Việt Hoàng - Chương 5).",
)

app.include_router(ticket_router, prefix=config.api_prefix)


@app.get("/health", tags=["Health"])
def health_check() -> dict:
    return {"status": "ok", "module": "ticket-intake"}