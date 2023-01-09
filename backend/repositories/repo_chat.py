"""repository for chat."""
import datetime

from databases.interfaces import Record

from backend.models import models_events
from backend.repositories import (
    BaseAsyncRepository,
    postgres_reconnect,
    repo_interfaces,
)


class ChatDatabaseRepository(BaseAsyncRepository, repo_interfaces.ChatRepoInterface):
    """Repository for chat."""

    @postgres_reconnect
    async def store_new_message(
        self, message: models_events.ChatEventModel
    ) -> models_events.ChatEventModel | None:
        """Store new message."""
        result: Record | None = await self.database_connection.fetch_one(
            """
            INSERT INTO chat_messages(user_id, target_user_id, matcha_pair_id, text)
            VALUES (:user_id, :target_user_id, :matcha_pair_id, :text)
            ON CONFLICT ON CONSTRAINT uc_users_pair_chat 
            DO NOTHING
            RETURNING *;
            """,
            message.dict(exclude={"message_time", "is_read"}),
        )
        if not result:
            return None
        return models_events.ChatEventModel(**dict(result))

    @postgres_reconnect
    async def retrieve_messages(
        self,
        matcha_pair_id: int,
        limit: int,
        offset: int,
        last_message_time: datetime.datetime | None = None,
    ) -> list[models_events.ChatEventModel]:
        """Retrieve messages for chatting room."""
        messages: list[Record] = await self.database_connection.fetch_all(
            """
            SELECT *
            FROM chat_messages
            WHERE matcha_pair_id=:matcha_pair_id and message_time < :last_message_time
            ORDER BY message_time DESC
            LIMIT :limit
            OFFSET :offset
            """,
            {
                "matcha_pair_id": matcha_pair_id,
                "limit": limit,
                "offset": offset,
                "last_message_time": last_message_time
                if last_message_time
                else datetime.datetime.now(),
            },
        )
        return [models_events.ChatEventModel(**dict(message)) for message in messages]

    @postgres_reconnect
    async def update_is_read(self, user_id: int, target_user_id: int) -> bool:
        """Update is_read field for all messages for users pair."""
        result: bool = await self.database_connection.execute(
            """
            UPDATE chat_messages
            SET is_read=true
            WHERE user_id=:user_id and target_user_id=:target_user_id AND is_read=false AND message_time < NOW()
            RETURNING true;
            """,
            {"user_id": user_id, "target_user_id": target_user_id},
        )
        return bool(result)

    @postgres_reconnect
    async def get_current_chats_for_user(
        self, user_id: int
    ) -> list[models_events.ChatBaseInfoModel]:
        """Get all chats with profiles for user_id."""
        result: list[Record] = await self.database_connection.fetch_all(
            """
            SELECT user_id as target_user_id, first_name, last_name, main_photo_name, matcha_pair_id
            FROM (
                SELECT COALESCE(NULLIF(first_user_id, :user_id), NULLIF(second_user_id, :user_id)) as chat_user_id, 
                       matcha_pair_id 
                FROM ( 
                    SELECT DISTINCT matcha_pair_id
                    FROM chat_messages
                    WHERE user_id=:user_id OR target_user_id=:user_id
                ) as msgs
                LEFT JOIN matches as match
                ON msgs.matcha_pair_id = match.id
                ORDER BY match.id DESC
            ) as chat_users
            LEFT JOIN profiles as p
            ON p.user_id = chat_users.chat_user_id
            """,
            {"user_id": user_id},
        )
        if not result:
            return []
        return [models_events.ChatBaseInfoModel(**dict(record)) for record in result]
