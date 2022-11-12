"""Repo for redis avatars."""
import base64

import fastapi

from backend.models import models_user
from backend.repositories_redis import BaseRedisRepository, redis_reconnect
from backend.settings import settings_base


class UsersAvatarsRedisRepo(BaseRedisRepository):
    """Class for handling users avatars.

    Store/retrieve/delete
    """

    @staticmethod
    def _create_user_avatars_key(user_id: int) -> str:
        """Create key for user avatars in redis."""
        return f"user-avatars-{user_id}"

    @redis_reconnect
    async def store_avatars(
        self, user_id: int, files: list[models_user.UserAvatar]
    ) -> None:
        """Store avatars."""
        stored_avatars_names_b: list[bytes] = await self._redis_connection.hkeys(
            self._create_user_avatars_key(user_id)
        )
        stored_avatars_names = [name.decode() for name in stored_avatars_names_b]
        if len(stored_avatars_names) >= settings_base.max_count_of_avatars:
            raise fastapi.HTTPException(
                status_code=fastapi.status.HTTP_409_CONFLICT,
                detail=f"Too many avatars for user. Maximum is {settings_base.max_count_of_avatars}",
            )

        for file in files:
            if file.name in stored_avatars_names:
                continue
            await self._redis_connection.hset(
                self._create_user_avatars_key(user_id), file.name, file.file
            )
        return

    @redis_reconnect
    async def collect_avatars(self, user_id: int) -> list[models_user.UserAvatar]:
        """Get avatars for user."""
        user_avatars: dict = await self._redis_connection.hgetall(
            self._create_user_avatars_key(user_id)
        )
        if not user_avatars:
            return []
        result: list[models_user.UserAvatar] = []
        for avatar_name, avatar in user_avatars.items():
            result.append(
                models_user.UserAvatar(
                    name=avatar_name.decode(), file=base64.encodebytes(avatar)
                )
            )
        return result

    @redis_reconnect
    async def delete_avatar(self, user_id, file_name: str) -> bool:
        """Delete avatar."""
        await self._redis_connection.hdel(
            self._create_user_avatars_key(user_id), file_name
        )
        return True
