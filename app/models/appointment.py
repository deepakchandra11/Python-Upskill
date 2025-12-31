from sqlalchemy import Integer, ForeignKey, Enum
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
import enum
from app.configs.database import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user import User


class AppointmentStatus(str, enum.Enum):
    SCHEDULED = "scheduled"
    CANCELLED = "cancelled"
    COMPLETED = "completed"


class Appointment(Base):
    __tablename__ = "appointments"

    id: Mapped[int] = mapped_column(primary_key=True)
    doctor_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    patient_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    appointment_time: Mapped[datetime] = mapped_column(nullable=False)
    status: Mapped[AppointmentStatus] = mapped_column(Enum(AppointmentStatus), default=AppointmentStatus.SCHEDULED, nullable=False)

    # 🔹 Relationships
    doctor: Mapped["User"] = relationship(
        "User",
        foreign_keys=[doctor_id],
        back_populates="doctor_appointments"
    )

    patient: Mapped["User"] = relationship(
        "User",
        foreign_keys=[patient_id],
        back_populates="patient_appointments"
    )

