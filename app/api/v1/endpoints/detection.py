from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from app.core.session import get_session
from app.schemas.detection import DetectionCreate, DetectionRead, DetectionConfirm
from app.services.detection_service import detection_service

router = APIRouter()


@router.get("/", response_model=list[DetectionRead])
def list_detections(
    cctv_id: int | None = Query(None),
    unconfirmed_only: bool = Query(False),
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    session: Session = Depends(get_session),
):
    if unconfirmed_only:
        return detection_service.list_unconfirmed(
            session, offset=offset, limit=limit
        )
    if cctv_id is not None:
        return detection_service.list_by_cctv(
            session, cctv_id, offset=offset, limit=limit
        )
    return detection_service.list_all(session, offset=offset, limit=limit)


@router.post("/", response_model=DetectionRead, status_code=201)
def create_detection(
    data: DetectionCreate, session: Session = Depends(get_session)
):
    return detection_service.record_detection(session, data)


@router.get("/{detection_id}", response_model=DetectionRead)
def get_detection(
    detection_id: int, session: Session = Depends(get_session)
):
    return detection_service.get_detection(session, detection_id)


@router.patch("/{detection_id}/confirm", response_model=DetectionRead)
def confirm_detection(
    detection_id: int,
    data: DetectionConfirm,
    session: Session = Depends(get_session),
):
    return detection_service.confirm_detection(session, detection_id, data)
