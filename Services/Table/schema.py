from pydantic import BaseModel


class CreateTable(BaseModel):
    name: str
    seats: int
    location: str