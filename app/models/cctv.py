from datetime import datetime, timezone

from geoalchemy2 import Geometry
from sqlalchemy import Column
from sqlmodel import SQLModel, Field


class CCTV(SQLModel, table=True):
    __tablename__ = "cctvs"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=200, index=True)
    road_name: str = Field(max_length=200)
    direction: str = Field(max_length=50)
    location: str | None = Field(
        default=None,
        sa_column=Column(Geometry(geometry_type="POINT", srid=4326)),
    )
    stream_url: str = Field(max_length=500)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))