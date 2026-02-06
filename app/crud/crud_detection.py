from sqlmodel import Session, select

from app.crud.base import CRUDBase
from app.models.detection import Detection
from app.schemas.detection import DetectionCreate


class CRUDDetection(CRUDBase[Detection, DetectionCreate]):
    def get_by_cctv(
        self,
        session: Session,
        *,
        cctv_id: int,
        offset: int = 0,
        limit: int = 20,
    ) -> list[Detection]:
        statement = (
            select(Detection)
            .where(Detection.cctv_id == cctv_id)
            .order_by(Detection.detected_at.desc())
            .offset(offset)
            .limit(limit)
        )
        return list(session.exec(statement).all())

    def get_unconfirmed(
        self, session: Session, *, offset: int = 0, limit: int = 20
    ) -> list[Detection]:
        statement = (
            select(Detection)
            .where(Detection.is_confirmed == False)  # noqa: E712
            .order_by(Detection.detected_at.desc())
            .offset(offset)
            .limit(limit)
        )
        return list(session.exec(statement).all())


detection_crud = CRUDDetection(Detection)