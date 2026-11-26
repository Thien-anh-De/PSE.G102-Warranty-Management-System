from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.warranty_app.config import get_config
from src.warranty_app.routers.ticket_router import router as ticket_router
from src.warranty_app.routers.portal_router import router as portal_router

config = get_config()

app = FastAPI(
    title=config.app_name,
    version=config.app_version,
    description="Module tiếp nhận phiếu bảo hành (Nguyễn Việt Hoàng - Chương 5).",
)

app.include_router(ticket_router, prefix=config.api_prefix)
app.include_router(portal_router, prefix=config.api_prefix)


@app.get("/health", tags=["Health"])
def health_check() -> dict:
    return {"status": "ok", "module": "ticket-intake"}


# Next.js static export and the API share one origin, including in the demo.
frontend_directory = Path(__file__).resolve().parents[2] / "frontend" / "out"
if frontend_directory.is_dir():
    app.mount("/", StaticFiles(directory=frontend_directory, html=True), name="customer-portal")
