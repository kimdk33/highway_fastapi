from sqlmodel import Session, select

from app.crud.base import CRUDBase
from app.models.cctv import CCTV
from app.schemas.cctv import CCTVCreate, CCTVUpdate


class CRUDCCTV(CRUDBase[CCTV, CCTVCreate]):
    def get_by_road(self, session: Session, *, road_name: str) -> list[CCTV]:
        statement = select(CCTV).where(CCTV.road_name == road_name)
        return list(session.exec(statement).all())

    def get_active(
        self, session: Session, *, offset: int = 0, limit: int = 20
    ) -> list[CCTV]:
        statement = (
            select(CCTV)
            .where(CCTV.is_active == True)  # noqa: E712
            .offset(offset)
            .limit(limit)
        )
        return list(session.exec(statement).all())

    def update(
        self, session: Session, *, db_obj: CCTV, obj_in: CCTVUpdate
    ) -> CCTV:
        update_data = obj_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_obj, key, value)
        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return db_obj


cctv_crud = CRUDCCTV(CCTV)