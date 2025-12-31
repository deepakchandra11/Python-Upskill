from pydantic import BaseModel
from datetime import datetime
from app.models.appointment import AppointmentStatus


class AppointmentCreate(BaseModel):
    doctor_id: int
    appointment_time: datetime


class AppointmentResponse(BaseModel):
    id: int
    doctor_id: int
    patient_id: int
    appointment_time: datetime
    status: AppointmentStatus

    class Config:
        from_attributes = True


class AppointmentCancel(BaseModel):
    appointment_id: int

