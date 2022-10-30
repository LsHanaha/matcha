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


class LocationRepositoryModel(pydantic.BaseModel):
    """Location in database."""

    user_id: int
    ip_addr: str
    country: str
    region: str
    city: str
    latitude: float
    longitude: float
    tz: str | None
