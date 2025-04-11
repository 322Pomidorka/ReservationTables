from datetime import datetime

from pydantic import BaseModel


class CreateReservation(BaseModel):
    customer_name: str
    table_id: int
    reservation_time: datetime
    duration_minutes: int