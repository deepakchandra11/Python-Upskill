from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from app.configs.database import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user import User


class Availability(Base):
    __tablename__ = "availabilities"

    id: Mapped[int] = mapped_column(primary_key=True)
    doctor_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    start_time: Mapped[datetime] = mapped_column(nullable=False)
    end_time: Mapped[datetime] = mapped_column(nullable=False)

    # Relationships
    doctor: Mapped["User"] = relationship(
        "User",
        foreign_keys=[doctor_id],
        back_populates="availabilities"
    )

