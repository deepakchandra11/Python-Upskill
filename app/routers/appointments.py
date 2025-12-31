from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.configs.database import get_db
from app.routers.dependencies import get_current_patient
from app.services.patient_service import PatientService
from app.schemas.appointment import AppointmentCreate, AppointmentResponse
from app.models.user import User

router = APIRouter(prefix="/appointments", tags=["Appointments"])


@router.post("", response_model=AppointmentResponse, status_code=status.HTTP_201_CREATED)
async def book_appointment(
    appointment_data: AppointmentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_patient)
):
    """Book an appointment. (Patient only)"""
    patient_service = PatientService(db)
    return await patient_service.book_appointment(current_user.id, appointment_data)


@router.post("/{appointment_id}/cancel", response_model=AppointmentResponse)
async def cancel_appointment(
    appointment_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_patient)
):
    """Cancel an appointment. (Patient only)"""
    patient_service = PatientService(db)
    return await patient_service.cancel_appointment(current_user.id, appointment_id)

