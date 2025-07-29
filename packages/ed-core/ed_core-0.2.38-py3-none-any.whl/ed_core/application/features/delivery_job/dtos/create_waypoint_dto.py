from datetime import datetime
from uuid import UUID

from ed_domain.core.entities.waypoint import WaypointStatus, WaypointType
from pydantic import BaseModel


class CreateWaypointDto(BaseModel):
    order_id: UUID
    expected_arrival_time: datetime
    actual_arrival_time: datetime
    sequence: int
    waypoint_type: WaypointType
    waypoint_status: WaypointStatus
