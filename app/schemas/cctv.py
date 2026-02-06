from datetime import datetime

from sqlmodel import SQLModel


class CCTVCreate(SQLModel):
    name: str
    road_name: str
    direction: str
    latitude: float
    longitude: float
    stream_url: str
    is_active: bool = True


class CCTVUpdate(SQLModel):
    name: str | None = None
    road_name: str | None = None
    direction: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    stream_url: str | None = None
    is_active: bool | None = None


class CCTVRead(SQLModel):
    id: int
    name: str
    road_name: str
    direction: str
    latitude: float | None = None
    longitude: float | None = None
    stream_url: str
    is_active: bool
    created_at: datetime
    updated_at: datetime