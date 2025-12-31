from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.configs.database import get_db
from app.routers.dependencies import get_current_patient, get_current_doctor
from app.services.patient_service import PatientService
from app.services.doctor_service import DoctorService
from app.schemas.user import UserResponse
from app.schemas.availability import AvailabilityResponse, AvailabilityCreate
from app.schemas.appointment import AppointmentResponse
from app.models.user import User
from typing import List

router = APIRouter(prefix="/doctors", tags=["Doctors"])


@router.get("", response_model=List[UserResponse])
async def list_doctors(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_patient)
):
    """List all doctors. (Patient only)"""
    patient_service = PatientService(db)
    return await patient_service.list_doctors()


@router.get("/{doctor_id}/availability", response_model=List[AvailabilityResponse])
async def get_doctor_availability(
    doctor_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_patient)
):
    """Get availability for a specific doctor. (Patient only)"""
    patient_service = PatientService(db)
    return await patient_service.get_doctor_availability(doctor_id)


@router.post("/availability", response_model=AvailabilityResponse)
async def set_availability(
    availability_data: AvailabilityCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_doctor)
):
    """Set availability. (Doctor only)"""
    doctor_service = DoctorService(db)
    return await doctor_service.set_availability(current_user.id, availability_data)


@router.get("/appointments/upcoming", response_model=List[AppointmentResponse])
async def get_upcoming_appointments(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_doctor)
):
    """Get upcoming appointments. (Doctor only)"""
    doctor_service = DoctorService(db)
    return await doctor_service.get_upcoming_appointments(current_user.id)

