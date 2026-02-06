from datetime import datetime

from sqlmodel import SQLModel, Field


class TrafficInfo(SQLModel, table=True):
    __tablename__ = "traffic_info"

    id: int | None = Field(default=None, primary_key=True)
    cctv_id: int = Field(foreign_key="cctvs.id", index=True)
    recorded_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    vehicle_count: int = Field(default=0)
    avg_speed: float | None = Field(default=None)
    congestion_level: str = Field(max_length=20, default="normal")
    created_at: datetime = Field(default_factory=datetime.utcnow)