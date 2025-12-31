from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_
from typing import Optional, List
from datetime import datetime
from app.models.appointment import Appointment, AppointmentStatus
from app.schemas.appointment import AppointmentCreate


class AppointmentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, patient_id: int, appointment_data: AppointmentCreate) -> Appointment:
        """Create a new appointment."""
        db_appointment = Appointment(
            doctor_id=appointment_data.doctor_id,
            patient_id=patient_id,
            appointment_time=appointment_data.appointment_time,
            status=AppointmentStatus.SCHEDULED
        )
        self.db.add(db_appointment)
        await self.db.commit()
        await self.db.refresh(db_appointment)
        return db_appointment

    async def get_by_id(self, appointment_id: int) -> Optional[Appointment]:
        """Get appointment by ID."""
        result = await self.db.execute(
            select(Appointment).where(Appointment.id == appointment_id)
        )
        return result.scalar_one_or_none()

    async def check_conflict(
        self,
        doctor_id: int,
        appointment_time: datetime,
        buffer_minutes: int = 30
    ) -> bool:
        """Check if there's a conflicting appointment."""
        from datetime import timedelta
        start_time = appointment_time - timedelta(minutes=buffer_minutes)
        end_time = appointment_time + timedelta(minutes=buffer_minutes)

        result = await self.db.execute(
            select(Appointment).where(
                and_(
                    Appointment.doctor_id == doctor_id,
                    Appointment.status == AppointmentStatus.SCHEDULED,
                    Appointment.appointment_time >= start_time,
                    Appointment.appointment_time <= end_time
                )
            )
        )
        return result.scalar_one_or_none() is not None

    async def get_by_doctor_id(self, doctor_id: int) -> List[Appointment]:
        """Get all appointments for a doctor."""
        result = await self.db.execute(
            select(Appointment).where(
                and_(
                    Appointment.doctor_id == doctor_id,
                    Appointment.status == AppointmentStatus.SCHEDULED
                )
            ).order_by(Appointment.appointment_time)
        )
        return list(result.scalars().all())

    async def get_by_patient_id(self, patient_id: int) -> List[Appointment]:
        """Get all appointments for a patient."""
        result = await self.db.execute(
            select(Appointment).where(
                and_(
                    Appointment.patient_id == patient_id,
                    Appointment.status == AppointmentStatus.SCHEDULED
                )
            ).order_by(Appointment.appointment_time)
        )
        return list(result.scalars().all())

    async def cancel(self, appointment_id: int, user_id: int) -> Optional[Appointment]:
        """Cancel an appointment (only by the patient who booked it)."""
        appointment = await self.get_by_id(appointment_id)
        if not appointment or appointment.patient_id != user_id:
            return None
        if appointment.status != AppointmentStatus.SCHEDULED:
            return None

        appointment.status = AppointmentStatus.CANCELLED
        await self.db.commit()
        await self.db.refresh(appointment)
        return appointment

