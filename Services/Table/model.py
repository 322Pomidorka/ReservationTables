from sqlalchemy.orm import Mapped, mapped_column, relationship

from Services.Reservation.model import Reservation
from Shared.Base.BaseModel import Base


class Table(Base):
    __tablename__ = "tables"

    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    seats: Mapped[int] = mapped_column(nullable=False)
    location: Mapped[str | None]

    reservations: Mapped[list["Reservation"]] = relationship(back_populates="table", cascade="all, delete-orphan")