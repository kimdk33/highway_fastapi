from fastapi import HTTPException, status


class CCTVNotFoundException(HTTPException):
    def __init__(self, cctv_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"CCTV with id {cctv_id} not found",
        )


class DetectionNotFoundException(HTTPException):
    def __init__(self, detection_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Detection with id {detection_id} not found",
        )