from pydantic import BaseModel
from datetime import datetime


class AvailabilityCreate(BaseModel):
    start_time: datetime
    end_time: datetime


class AvailabilityResponse(BaseModel):
    id: int
    doctor_id: int
    start_time: datetime
    end_time: datetime

    class Config:
        from_attributes = True

