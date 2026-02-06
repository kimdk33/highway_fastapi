from sqlmodel import SQLModel


class PaginationParams(SQLModel):
    offset: int = 0
    limit: int = 20


class PaginatedResponse[T](SQLModel):
    items: list[T]
    total: int
    offset: int
    limit: int


class ErrorResponse(SQLModel):
    detail: str