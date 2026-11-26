from typing import Callable

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.routing import APIRoute

from src.warranty_app.dependencies import get_portal_rate_limiter, get_portal_service
from src.warranty_app.portal_rate_limiter import PortalRateLimiter
from src.warranty_app.schemas.portal_schema import PortalLookupRequest, PortalLookupResponse
from src.warranty_core import PortalService, PortalServiceError


class PortalRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_handler = super().get_route_handler()

        async def private_response_handler(request: Request) -> Response:
            try:
                response = await original_handler(request)
            except RequestValidationError:
                # FastAPI's default validation response can echo the submitted secret.
                response = JSONResponse(
                    status_code=422,
                    content={"detail": "Vui lòng nhập mã phiếu và mã tra cứu hợp lệ."},
                )
            except HTTPException as exc:
                response = JSONResponse(
                    status_code=exc.status_code,
                    content={"detail": exc.detail},
                    headers=exc.headers,
                )
            response.headers["Cache-Control"] = "no-store"
            response.headers["Pragma"] = "no-cache"
            response.headers["X-Content-Type-Options"] = "nosniff"
            return response

        return private_response_handler


router = APIRouter(prefix="/portal/lookups", tags=["Customer Portal"], route_class=PortalRoute)


def enforce_lookup_limit(
    request: Request,
    limiter: PortalRateLimiter = Depends(get_portal_rate_limiter),
) -> None:
    # Forwarded headers are trusted only when the ASGI server has verified its proxy.
    client_address = request.client.host if request.client else "unknown"
    retry_after = limiter.consume(client_address)
    if retry_after is not None:
        raise HTTPException(
            status_code=429,
            detail="Bạn đã tra cứu quá nhiều lần. Vui lòng thử lại sau.",
            headers={"Retry-After": str(retry_after)},
        )


@router.post(
    "",
    response_model=PortalLookupResponse,
    dependencies=[Depends(enforce_lookup_limit)],
    summary="Tra cứu tiến độ bằng mã phiếu và mã tra cứu bí mật",
    responses={
        404: {"description": "Thông tin tra cứu không hợp lệ."},
        422: {"description": "Dữ liệu đầu vào không hợp lệ; không trả lại mã bí mật."},
        429: {"description": "Vượt giới hạn tra cứu; có tiêu đề Retry-After."},
        503: {"description": "CSDL tạm thời không khả dụng; không trả chi tiết kết nối."},
    },
)
def lookup_ticket(
    payload: PortalLookupRequest,
    portal_service: PortalService = Depends(get_portal_service),
) -> PortalLookupResponse:
    try:
        public_data = portal_service.lookup_ticket_public_status(
            ticket_id=payload.ticket_id,
            plain_secret_code=payload.plain_secret_code.get_secret_value(),
        )
    except PortalServiceError:
        raise HTTPException(
            status_code=404,
            detail="Thông tin tra cứu không hợp lệ hoặc không tìm thấy phiếu bảo hành.",
        ) from None
    return PortalLookupResponse.model_validate(public_data)
