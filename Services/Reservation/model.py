from datetime import datetime

from sqlalchemy import DateTime, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from Shared.Base.BaseModel import Base


class Reservation(Base):
    __tablename__ = "reservations"


    customer_name: Mapped[str] = mapped_column(nullable=False)
    reservation_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    duration_minutes: Mapped[int] = mapped_column(nullable=False)

    table_id: Mapped[int] = mapped_column(ForeignKey("tables.id"))
    table = relationship('Table', back_populates="reservations")