from typing import Optional

from pydantic import BaseModel, Field

from ed_core.application.features.common.dtos.update_location_dto import \
    UpdateLocationDto


class UpdateDriverDto(BaseModel):
    profile_image: Optional[str] = Field(None)
    phone_number: Optional[str] = Field(None)
    email: Optional[str] = Field(None)
    location: Optional[UpdateLocationDto] = Field(None)
