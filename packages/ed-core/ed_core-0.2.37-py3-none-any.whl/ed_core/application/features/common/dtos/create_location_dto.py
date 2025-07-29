from pydantic import BaseModel


class CreateLocationDto(BaseModel):
    address: str
    latitude: float
    longitude: float
    postal_code: str
