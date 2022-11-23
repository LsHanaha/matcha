"""Models for handling user's location."""

import pydantic


class TimezoneApi(pydantic.BaseModel):
    """Timezone map of IpWhoIS response."""

    id: str
    abbr: str


class IPWhoISApiResponseModel(pydantic.BaseModel):
    """Response of API for determining location by IP."""

    success: bool
    country: str
    region: str
    city: str
    latitude: float
    longitude: float
    timezone: TimezoneApi | None


class CoordinatesLocationModel(pydantic.BaseModel):
    """Model for user coordinates."""

    latitude: float
    longitude: float


class LocationRepositoryModel(CoordinatesLocationModel):
    """Location in database."""

    user_id: int
    ip_addr: str
    country: str
    region: str
    city: str
    tz: str | None


class CoordinatesForSearchUsersModels(pydantic.BaseModel):
    """Model to determine locations for searching users."""

    lat_min: float
    lat_max: float
    lng_min: float
    lng_max: float
