from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from app.core.session import get_session
from app.schemas.cctv import CCTVCreate, CCTVRead, CCTVUpdate
from app.services.cctv_service import cctv_service

router = APIRouter()


@router.get("/", response_model=list[CCTVRead])
def list_cctvs(
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    session: Session = Depends(get_session),
):
    return cctv_service.list_cctvs(session, offset=offset, limit=limit)


@router.post("/", response_model=CCTVRead, status_code=201)
def create_cctv(data: CCTVCreate, session: Session = Depends(get_session)):
    return cctv_service.create_cctv(session, data)


@router.get("/{cctv_id}", response_model=CCTVRead)
def get_cctv(cctv_id: int, session: Session = Depends(get_session)):
    return cctv_service.get_cctv(session, cctv_id)


@router.patch("/{cctv_id}", response_model=CCTVRead)
def update_cctv(
    cctv_id: int, data: CCTVUpdate, session: Session = Depends(get_session)
):
    return cctv_service.update_cctv(session, cctv_id, data)


@router.delete("/{cctv_id}", status_code=204)
def delete_cctv(cctv_id: int, session: Session = Depends(get_session)):
    cctv_service.delete_cctv(session, cctv_id)
