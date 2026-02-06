from sqlmodel import Session

from app.crud.crud_traffic import traffic_crud
from app.schemas.traffic import TrafficInfoCreate
from app.models.traffic import TrafficInfo


class TrafficService:
    def record_traffic(
        self, session: Session, data: TrafficInfoCreate
    ) -> TrafficInfo:
        return traffic_crud.create(session, obj_in=data)

    def get_latest_for_cctv(
        self, session: Session, cctv_id: int
    ) -> TrafficInfo | None:
        return traffic_crud.get_latest_by_cctv(session, cctv_id=cctv_id)

    def list_by_cctv(
        self,
        session: Session,
        cctv_id: int,
        offset: int = 0,
        limit: int = 20,
    ) -> list[TrafficInfo]:
        return traffic_crud.get_by_cctv(
            session, cctv_id=cctv_id, offset=offset, limit=limit
        )


traffic_service = TrafficService()