from sqlmodel import Session

from app.crud.crud_cctv import cctv_crud
from app.schemas.cctv import CCTVCreate, CCTVUpdate
from app.models.cctv import CCTV
from app.core.exceptions import CCTVNotFoundException


class CCTVService:
    def get_cctv(self, session: Session, cctv_id: int) -> CCTV:
        cctv = cctv_crud.get(session, id=cctv_id)
        if not cctv:
            raise CCTVNotFoundException(cctv_id)
        return cctv

    def list_cctvs(
        self, session: Session, offset: int = 0, limit: int = 20
    ) -> list[CCTV]:
        return cctv_crud.get_multi(session, offset=offset, limit=limit)

    def list_by_road(self, session: Session, road_name: str) -> list[CCTV]:
        return cctv_crud.get_by_road(session, road_name=road_name)

    def create_cctv(self, session: Session, data: CCTVCreate) -> CCTV:
        return cctv_crud.create(session, obj_in=data)

    def update_cctv(
        self, session: Session, cctv_id: int, data: CCTVUpdate
    ) -> CCTV:
        cctv = self.get_cctv(session, cctv_id)
        return cctv_crud.update(session, db_obj=cctv, obj_in=data)

    def delete_cctv(self, session: Session, cctv_id: int) -> bool:
        self.get_cctv(session, cctv_id)
        return cctv_crud.delete(session, id=cctv_id)


cctv_service = CCTVService()