from datetime import datetime

from sqlmodel import SQLModel, Field


class Detection(SQLModel, table=True):
    __tablename__ = "detections"

    id: int | None = Field(default=None, primary_key=True)
    cctv_id: int = Field(foreign_key="cctvs.id", index=True)
    detected_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    anomaly_type: str = Field(max_length=100)
    confidence: float
    bounding_box: str | None = Field(default=None)
    image_path: str | None = Field(default=None, max_length=500)
    is_confirmed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)