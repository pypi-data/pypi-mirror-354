from typing import Optional

from pydantic import BaseModel

from ed_core.application.features.common.dtos import CreateLocationDto
from ed_core.application.features.common.dtos.update_location_dto import \
    UpdateLocationDto


class UpdateBusinessDto(BaseModel):
    phone_number: Optional[str] = None
    email: Optional[str] = None
    location: Optional[UpdateLocationDto] = None
