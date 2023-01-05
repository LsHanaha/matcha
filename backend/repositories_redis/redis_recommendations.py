"""Handle all interactions with Redis for recommendations."""

from backend.repositories_redis import BaseRedisRepository, redis_reconnect


class UserRecommendationsService(BaseRedisRepository):
    """Class for handling recommendations."""

    @staticmethod
    def _create_user_recommendations_key(user_id: int) -> str:
        """Create key for user recommendations in redis."""
        return f"user-recommendations-{user_id}"

    @redis_reconnect
    async def store_multiple_recommendations(
        self, user_id: int, recommendations: list[int]
    ) -> None:
        """Store recommendations in redis list."""
        await self.delete_all_recommendations(user_id)
        for recommendation in recommendations:
            await self.redis_connection.lpush(
                self._create_user_recommendations_key(user_id), recommendation
            )
        return

    @redis_reconnect
    async def store_one_recommendation(
        self, user_id: int, recommendation_id: int
    ) -> None:
        """Add recommendation for user."""
        await self.redis_connection.lpush(
            self._create_user_recommendations_key(user_id), recommendation_id
        )
        return

    @redis_reconnect
    async def get_all_recommendations(self, user_id: int) -> list[int]:
        """Get recommendations for user."""
        recommendations: list = await self.redis_connection.lrange(
            self._create_user_recommendations_key(user_id), 0, -1
        )
        if not recommendations:
            return []
        return [int(recommendation) for recommendation in recommendations]

    @redis_reconnect
    async def pop_one_recommendation(self, user_id: int) -> int | None:
        """Get one recommendation for user."""
        recommendation: int = await self.redis_connection.rpop(
            self._create_user_recommendations_key(user_id)
        )
        if not recommendation:
            return None
        return int(recommendation)

    @redis_reconnect
    async def collect_count_of_recommendations(self, user_id: int) -> int:
        """Get recommendation count for user."""
        recommendation_count: int = await self.redis_connection.llen(
            self._create_user_recommendations_key(user_id)
        )
        if not recommendation_count:
            return 0
        return int(recommendation_count)

    @redis_reconnect
    async def delete_all_recommendations(self, user_id: int) -> None:
        """Delete recommendations for user."""
        await self.redis_connection.delete(
            self._create_user_recommendations_key(user_id)
        )
        return

    @redis_reconnect
    async def delete_one_recommendation(
        self, user_id: int, recommendation_id: int
    ) -> None:
        """Delete recommendation for user."""
        await self.redis_connection.lrem(
            self._create_user_recommendations_key(user_id), 0, recommendation_id
        )
        return
