from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from app.core.session import get_session
from app.schemas.traffic import TrafficInfoCreate, TrafficInfoRead
from app.services.traffic_service import traffic_service

router = APIRouter()



@router.get("/", response_model=list[TrafficInfoRead])
def list_traffic(
    cctv_id: int = Query(...),
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    session: Session = Depends(get_session),
):
    return traffic_service.list_by_cctv(
        session, cctv_id, offset=offset, limit=limit
    )


@router.post("/", response_model=TrafficInfoRead, status_code=201)
def create_traffic(
    data: TrafficInfoCreate, session: Session = Depends(get_session)
):
    return traffic_service.record_traffic(session, data)


@router.get("/latest", response_model=TrafficInfoRead | None)
def get_latest_traffic(
    cctv_id: int = Query(...),
    session: Session = Depends(get_session),
):
    return traffic_service.get_latest_for_cctv(session, cctv_id)