from sqlmodel import Session

from app.crud.crud_detection import detection_crud
from app.schemas.detection import DetectionCreate, DetectionConfirm
from app.models.detection import Detection
from app.core.exceptions import DetectionNotFoundException


class DetectionService:
    def record_detection(
        self, session: Session, data: DetectionCreate
    ) -> Detection:
        return detection_crud.create(session, obj_in=data)

    def get_detection(self, session: Session, detection_id: int) -> Detection:
        detection = detection_crud.get(session, id=detection_id)
        if not detection:
            raise DetectionNotFoundException(detection_id)
        return detection

    def list_by_cctv(
        self,
        session: Session,
        cctv_id: int,
        offset: int = 0,
        limit: int = 20,
    ) -> list[Detection]:
        return detection_crud.get_by_cctv(
            session, cctv_id=cctv_id, offset=offset, limit=limit
        )

    def list_unconfirmed(
        self, session: Session, offset: int = 0, limit: int = 20
    ) -> list[Detection]:
        return detection_crud.get_unconfirmed(
            session, offset=offset, limit=limit
        )

    def confirm_detection(
        self, session: Session, detection_id: int, data: DetectionConfirm
    ) -> Detection:
        detection = self.get_detection(session, detection_id)
        detection.is_confirmed = data.is_confirmed
        session.add(detection)
        session.commit()
        session.refresh(detection)
        return detection


detection_service = DetectionService()