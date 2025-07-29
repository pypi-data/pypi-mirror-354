from ed_domain.core.entities.parcel import ParcelSize
from pydantic import BaseModel


class CreateParcelDto(BaseModel):
    size: ParcelSize
    length: float
    width: float
    height: float
    weight: float
    fragile: bool
