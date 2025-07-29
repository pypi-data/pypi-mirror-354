from uuid import UUID

from pydantic import BaseModel

from ed_core.application.features.common.dtos.create_location_dto import \
    CreateLocationDto


class CreateConsumerDto(BaseModel):
    user_id: UUID
    first_name: str
    last_name: str
    phone_number: str
    email: str
    location: CreateLocationDto
