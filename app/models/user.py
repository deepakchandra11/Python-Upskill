from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship, Mapped, mapped_column
import enum
from app.configs.database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.appointment import Appointment
    from app.models.availability import Availability

class UserRole(str, enum.Enum):
    DOCTOR = "Doctor"
    PATIENT = "Patient"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    # Relationships
    availabilities: Mapped[list["Availability"]] = relationship(
        "Availability",
        back_populates="doctor",
        cascade="all, delete-orphan"
    )

    # 🔹 Appointments where user is doctor
    doctor_appointments: Mapped[list["Appointment"]] = relationship(
        "Appointment",
        foreign_keys="Appointment.doctor_id",
        back_populates="doctor"
    )

    # 🔹 Appointments where user is patient
    patient_appointments: Mapped[list["Appointment"]] = relationship(
        "Appointment",
        foreign_keys="Appointment.patient_id",
        back_populates="patient"
    )
