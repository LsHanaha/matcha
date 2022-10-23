"""Handle user location in database."""
from databases.interfaces import Record

from backend.models import location_models
from backend.repositories import BaseAsyncRepository, interfaces, postgres_reconnect


class LocationDatabaseRepository(
    BaseAsyncRepository, interfaces.LocationRepositoryInterface
):
    """User location repository."""

    @postgres_reconnect
    async def collect_user_location(
        self, user_id: int
    ) -> location_models.LocationRepositoryModel | None:
        """Collect user location."""
        location_record: Record | None = await self.database_connection.execute(
            """
                SELECT *
                FROM user_locations
                WHERE user_id=:user_id
            """,
            {"user_id": user_id},
        )
        if not location_record:
            return None
        return location_models.LocationRepositoryModel(**dict(location_record))

    @postgres_reconnect
    async def update_user_location(
        self, user_id: int, new_location: location_models.LocationRepositoryModel
    ) -> bool:
        """Update location for a user."""
        result: int = await self.database_connection.execute(
            """
            INSERT INTO user_locations(user_id, ip_addr, country, region, city, latitude, longitude, tz)
            VALUES (:user_id, :ip_addr, :country, :region, :city, :latitude, :longitude, :tz)
            ON CONFLICT(user_id)
            DO UPDATE SET
            ip_addr=:ip_addr, country=:country, region=:region, city=:city, latitude=:latitude, longitude=:longitude, tz=:tz
            WHERE user_id=:user_id
            RETURNING 1;
            """,
            new_location.dict(),
        )
        return result