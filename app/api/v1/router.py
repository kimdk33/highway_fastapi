from fastapi import APIRouter

from app.api.v1.endpoints import health, cctv, detection, traffic

api_router = APIRouter()

api_router.include_router(
    health.router,
    prefix="/health",
    tags=["health"],
)

api_router.include_router(
    cctv.router,
    prefix="/cctvs",
    tags=["cctvs"],
)

api_router.include_router(
    detection.router,
    prefix="/detections",
    tags=["detections"],
)

api_router.include_router(
    traffic.router,
    prefix="/traffic",
    tags=["traffic"],
)
