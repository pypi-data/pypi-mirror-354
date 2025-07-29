from uuid import UUID

from pydantic import BaseModel

from ed_core.application.features.common.dtos import CreateLocationDto
from ed_core.application.features.driver.dtos.create_car_dto import \
    CreateCarDto


class CreateDriverDto(BaseModel):
    user_id: UUID
    first_name: str
    last_name: str
    profile_image: str
    phone_number: str
    email: str
    location: CreateLocationDto
    car: CreateCarDto
