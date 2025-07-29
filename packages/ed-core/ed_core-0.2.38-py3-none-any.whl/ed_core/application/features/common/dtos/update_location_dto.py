from pydantic import BaseModel

CITY = "Addis Ababa"
COUNTRY = "Ethiopia"


class UpdateLocationDto(BaseModel):
    address: str
    latitude: float
    longitude: float
    postal_code: str
