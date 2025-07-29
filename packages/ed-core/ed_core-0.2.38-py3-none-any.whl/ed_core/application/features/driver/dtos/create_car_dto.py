from pydantic import BaseModel


class CreateCarDto(BaseModel):
    make: str
    model: str
    year: int
    color: str
    seats: int
    license_plate: str
    registration_number: str
