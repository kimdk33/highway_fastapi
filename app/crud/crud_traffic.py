from sqlmodel import Session, select

from app.crud.base import CRUDBase
from app.models.traffic import TrafficInfo
from app.schemas.traffic import TrafficInfoCreate


class CRUDTraffic(CRUDBase[TrafficInfo, TrafficInfoCreate]):
    def get_by_cctv(
        self,
        session: Session,
        *,
        cctv_id: int,
        offset: int = 0,
        limit: int = 20,
    ) -> list[TrafficInfo]:
        statement = (
            select(TrafficInfo)
            .where(TrafficInfo.cctv_id == cctv_id)
            .order_by(TrafficInfo.recorded_at.desc())
            .offset(offset)
            .limit(limit)
        )
        return list(session.exec(statement).all())

    def get_latest_by_cctv(
        self, session: Session, *, cctv_id: int
    ) -> TrafficInfo | None:
        statement = (
            select(TrafficInfo)
            .where(TrafficInfo.cctv_id == cctv_id)
            .order_by(TrafficInfo.recorded_at.desc())
        )
        return session.exec(statement).first()


traffic_crud = CRUDTraffic(TrafficInfo)