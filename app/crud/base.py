from typing import TypeVar, Generic, Type

from sqlmodel import SQLModel, Session, select

ModelType = TypeVar("ModelType", bound=SQLModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=SQLModel)


class CRUDBase(Generic[ModelType, CreateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(self, session: Session, *, id: int) -> ModelType | None:
        return session.get(self.model, id)

    def get_multi(
        self, session: Session, *, offset: int = 0, limit: int = 20
    ) -> list[ModelType]:
        statement = select(self.model).offset(offset).limit(limit)
        return list(session.exec(statement).all())

    def create(self, session: Session, *, obj_in: CreateSchemaType) -> ModelType:
        db_obj = self.model.model_validate(obj_in)
        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return db_obj

    def delete(self, session: Session, *, id: int) -> bool:
        obj = session.get(self.model, id)
        if obj is None:
            return False
        session.delete(obj)
        session.commit()
        return True