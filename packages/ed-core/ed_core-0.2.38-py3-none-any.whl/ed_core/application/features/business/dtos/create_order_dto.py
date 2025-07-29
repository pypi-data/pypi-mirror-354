from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from ed_core.application.features.business.dtos.create_parcel_dto import \
    CreateParcelDto


class CreateOrderDto(BaseModel):
    consumer_id: UUID
    latest_time_of_delivery: datetime
    parcel: CreateParcelDto
