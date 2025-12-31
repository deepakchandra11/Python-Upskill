from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.repositories.availability_repository import AvailabilityRepository
from app.repositories.appointment_repository import AppointmentRepository
from app.schemas.availability import AvailabilityCreate, AvailabilityResponse
from app.schemas.appointment import AppointmentResponse
from typing import List


class DoctorService:
    def __init__(self, db: AsyncSession):
        self.availability_repo = AvailabilityRepository(db)
        self.appointment_repo = AppointmentRepository(db)

    async def set_availability(self, doctor_id: int, availability_data: AvailabilityCreate) -> AvailabilityResponse:
        """Set availability for a doctor."""
        if availability_data.end_time <= availability_data.start_time:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="End time must be after start time"
            )

        availability = await self.availability_repo.create(doctor_id, availability_data)
        return AvailabilityResponse.model_validate(availability)

    async def get_upcoming_appointments(self, doctor_id: int) -> List[AppointmentResponse]:
        """Get upcoming appointments for a doctor."""
        appointments = await self.appointment_repo.get_by_doctor_id(doctor_id)
        return [AppointmentResponse.model_validate(apt) for apt in appointments]

