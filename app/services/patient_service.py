from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.repositories.user_repository import UserRepository
from app.repositories.availability_repository import AvailabilityRepository
from app.repositories.appointment_repository import AppointmentRepository
from app.schemas.user import UserResponse
from app.schemas.availability import AvailabilityResponse
from app.schemas.appointment import AppointmentCreate, AppointmentResponse
from typing import List
from datetime import datetime


class PatientService:
    def __init__(self, db: AsyncSession):
        self.user_repo = UserRepository(db)
        self.availability_repo = AvailabilityRepository(db)
        self.appointment_repo = AppointmentRepository(db)

    async def list_doctors(self) -> List[UserResponse]:
        """List all doctors."""
        doctors = await self.user_repo.get_doctors()
        return [UserResponse.model_validate(doctor) for doctor in doctors]

    async def get_doctor_availability(self, doctor_id: int) -> List[AvailabilityResponse]:
        """Get availability for a specific doctor."""
        # Verify doctor exists
        doctor = await self.user_repo.get_by_id(doctor_id)
        if not doctor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Doctor not found"
            )

        from app.models.user import UserRole
        if doctor.role != UserRole.DOCTOR:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User is not a doctor"
            )

        availabilities = await self.availability_repo.get_by_doctor_id(doctor_id)
        return [AvailabilityResponse.model_validate(avail) for avail in availabilities]

    async def book_appointment(self, patient_id: int, appointment_data: AppointmentCreate) -> AppointmentResponse:
        """Book an appointment."""
        # Verify doctor exists
        doctor = await self.user_repo.get_by_id(appointment_data.doctor_id)
        if not doctor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Doctor not found"
            )

        from app.models.user import UserRole
        if doctor.role != UserRole.DOCTOR:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User is not a doctor"
            )

        # Check if appointment time is in the future
        if appointment_data.appointment_time <= datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Appointment time must be in the future"
            )

        # Check if doctor has availability at this time
        # We'll check if there's any availability slot that contains this time
        availabilities = await self.availability_repo.get_available_slots(
            appointment_data.doctor_id,
            appointment_data.appointment_time,
            appointment_data.appointment_time
        )

        if not availabilities:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Doctor is not available at this time"
            )

        # Check if the appointment time falls within any availability window
        time_available = False
        for avail in availabilities:
            if avail.start_time <= appointment_data.appointment_time <= avail.end_time:
                time_available = True
                break

        if not time_available:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Doctor is not available at this time"
            )

        # Check for double-booking (conflicting appointments)
        has_conflict = await self.appointment_repo.check_conflict(
            appointment_data.doctor_id,
            appointment_data.appointment_time
        )

        if has_conflict:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="This time slot is already booked"
            )

        # Create appointment
        appointment = await self.appointment_repo.create(patient_id, appointment_data)
        return AppointmentResponse.model_validate(appointment)

    async def cancel_appointment(self, patient_id: int, appointment_id: int) -> AppointmentResponse:
        """Cancel an appointment."""
        appointment = await self.appointment_repo.cancel(appointment_id, patient_id)
        if not appointment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Appointment not found or cannot be cancelled"
            )
        return AppointmentResponse.model_validate(appointment)

