from datetime import datetime

from sqlmodel import SQLModel


class TrafficInfoCreate(SQLModel):
    cctv_id: int
    vehicle_count: int
    avg_speed: float | None = None
    congestion_level: str = "normal"


class TrafficInfoRead(SQLModel):
    id: int
    cctv_id: int
    recorded_at: datetime
    vehicle_count: int
    avg_speed: float | None
    congestion_level: str
    created_at: datetime