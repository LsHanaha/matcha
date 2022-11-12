"""Get user gps location."""

import backoff
import fastapi
import httpx

from backend.models import models_location
from backend.repositories import repo_interfaces
from backend.settings import settings_location


class LocationClient:
    """Client for connecting to API for location."""

    def __init__(self, base_url: str, default_headers: dict[str, str] | None = None):
        self._base_url: str = base_url
        self._default_headers: dict[str, str] | None = default_headers
        self._http_client: httpx.AsyncClient = httpx.AsyncClient(
            base_url=self._base_url, headers=self._default_headers
        )

    def _retry_error_handler(self) -> None:
        """Raise FastAPI error in case of repeated network error."""
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Cannot fetch current location",
        )

    @backoff.on_exception(
        backoff.expo,
        (httpx.ConnectError, httpx.ConnectTimeout, httpx.NetworkError),
        max_tries=settings_location.max_retries,
        on_giveup=_retry_error_handler,
    )
    async def collect_location(
        self, ip_addr: str, headers: None | dict[str, str] = None
    ) -> models_location.IPWhoISApiResponseModel:
        """Collect Location data by ip."""
        response: httpx.Response = await self._http_client.get(
            url=ip_addr, headers=headers
        )
        try:
            response.raise_for_status()
        except Exception as unexpected_exception:
            raise fastapi.HTTPException(
                status_code=response.status_code, detail=str(unexpected_exception)
            )
        response_data: models_location.IPWhoISApiResponseModel = (
            models_location.IPWhoISApiResponseModel(**response.json())
        )
        return response_data


class LocationService:
    """Collect and handle user location."""

    def __init__(
        self,
        location_client: LocationClient,
        location_repository: repo_interfaces.LocationRepositoryInterface,
    ):
        self._location_client: LocationClient = location_client
        self._location_repository: repo_interfaces.LocationRepositoryInterface = (
            location_repository
        )

    async def get_user_location(
        self, user_id: int
    ) -> models_location.LocationRepositoryModel | None:
        """Get user location from database."""
        return await self._location_repository.collect_user_location(user_id)

    async def update_user_location(
        self,
        user_id: int,
        new_ip_addr: str,
    ) -> None | bool:
        """Collect user location by his ip."""
        location_in_database: models_location.LocationRepositoryModel = (
            await self._location_repository.collect_user_location(user_id)
        )
        if location_in_database.ip_addr == new_ip_addr:
            # Refresh nor required
            return
        new_location: models_location.IPWhoISApiResponseModel = (
            await self._location_client.collect_location(new_ip_addr)
        )
        if not new_location or not new_location.success:
            # Not possible to handle location
            return None
        is_updated: bool = await self._location_repository.update_user_location(
            user_id,
            models_location.LocationRepositoryModel(
                user_id=user_id,
                ip_addr=new_ip_addr,
                country=new_location.country,
                region=new_location.region,
                city=new_location.city,
                latitude=new_location.latitude,
                longitude=new_location.longitude,
                tz=new_location.timezone.abbr if new_location.timezone else None,
            ),
        )
        return is_updated
