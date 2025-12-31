from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from typing import Optional, List
from datetime import datetime
from app.models.availability import Availability
from app.schemas.availability import AvailabilityCreate


class AvailabilityRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, doctor_id: int, availability_data: AvailabilityCreate) -> Availability:
        """Create availability for a doctor."""
        db_availability = Availability(
            doctor_id=doctor_id,
            start_time=availability_data.start_time,
            end_time=availability_data.end_time
        )
        self.db.add(db_availability)
        await self.db.commit()
        await self.db.refresh(db_availability)
        return db_availability

    async def get_by_doctor_id(self, doctor_id: int) -> List[Availability]:
        """Get all availabilities for a doctor."""
        result = await self.db.execute(
            select(Availability).where(Availability.doctor_id == doctor_id)
        )
        return list(result.scalars().all())

    async def get_available_slots(
        self,
        doctor_id: int,
        start_time: datetime,
        end_time: datetime
    ) -> List[Availability]:
        """Get available time slots that overlap with the requested time."""
        result = await self.db.execute(
            select(Availability).where(
                and_(
                    Availability.doctor_id == doctor_id,
                    Availability.start_time <= end_time,
                    Availability.end_time >= start_time
                )
            )
        )
        return list(result.scalars().all())

