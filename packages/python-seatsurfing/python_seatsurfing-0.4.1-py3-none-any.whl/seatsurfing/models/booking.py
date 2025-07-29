from typing import Optional
from pydantic import BaseModel, Field


class Location(BaseModel):
    """Location object holding all the information about a location (eg. office)"""

    id: str
    organizationId: str
    map_width: int = Field(alias="mapWidth")
    map_height: int = Field(alias="mapHeight")
    map_mime_type: str = Field(alias="mapMimeType")
    name: str
    description: str
    max_concurrent_booking: int = Field(alias="maxConcurrentBookings")
    timezone: str
    enabled: bool


class Space(BaseModel):
    """Space object that corresponds to a single seat."""

    id: str
    available: bool
    location_id: str = Field(alias="locationId")
    location: Optional[Location] = None
    name: str
    x: int
    y: int
    width: int
    height: int
    rotation: int


class Booking(BaseModel):
    """Booking object, holding all information about a single booking."""

    id: str
    user_id: str = Field(alias="userId")
    user_email: str = Field(alias="userEmail")
    space: Space
    space_id: str = Field(alias="spaceId")
    enter: str
    leave: str
    subject: Optional[str]


class BookingCreateOrUpdateDTO(BaseModel):
    """Booking object used only to create or update an existing booking."""

    enter: str
    leave: str
    space_id: str = Field(serialization_alias="spaceId")
    subject: str
    user_email: Optional[str] = Field(serialization_alias="userEmail", default="")
