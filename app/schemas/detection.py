from datetime import datetime

from sqlmodel import SQLModel


class DetectionCreate(SQLModel):
    cctv_id: int
    anomaly_type: str
    confidence: float
    bounding_box: str | None = None
    image_path: str | None = None


class DetectionRead(SQLModel):
    id: int
    cctv_id: int
    detected_at: datetime
    anomaly_type: str
    confidence: float
    bounding_box: str | None
    image_path: str | None
    is_confirmed: bool
    created_at: datetime


class DetectionConfirm(SQLModel):
    is_confirmed: bool