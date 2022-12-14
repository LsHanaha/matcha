"""Inversion of control for dependency injector."""

import resources
from dependency_injector import containers, providers

from backend import settings
from backend.api import locations
from backend.events import WebsocketConnectionManager, chat_events, system_events
from backend.mathca import matcha_search, matcha_visits, mathcha_helpers
from backend.repositories import (
    repo_auth,
    repo_chat,
    repo_interests,
    repo_interfaces,
    repo_location,
    repo_matcha,
    repo_preference,
    repo_profile,
    repo_system_events,
    repo_visits,
)
from backend.repositories_redis import redis_avatars, redis_recommendations


class IOCContainer(containers.DeclarativeContainer):
    """God-like container for maintaining dependencies."""

    redis_connection: providers.Resource[resources.RedisResource] = providers.Resource(
        resources.RedisResource
    )
    database_connection: providers.Resource[
        resources.DatabaseResource
    ] = providers.Resource(resources.DatabaseResource)
    websocket_manager: providers.Singleton[
        WebsocketConnectionManager
    ] = providers.Singleton(WebsocketConnectionManager)

    auth_repository: providers.Factory[
        repo_interfaces.AuthRepositoryInterface
    ] = providers.Factory(
        repo_auth.UserAuthDatabaseResourceRepository,
        database_connection=database_connection,
    )
    profile_repository: providers.Factory[
        repo_interfaces.ProfileRepositoryInterface
    ] = providers.Factory(
        repo_profile.UserProfileDatabaseRepository,
        database_connection=database_connection,
    )
    location_repository: providers.Factory[
        repo_interfaces.LocationRepositoryInterface
    ] = providers.Factory(
        repo_location.LocationDatabaseRepository,
        database_connection=database_connection,
    )
    preferences_repository: providers.Factory[
        repo_interfaces.PreferenceRepositoryInterface
    ] = providers.Factory(
        repo_preference.PreferenceDatabaseRepository,
        database_connection=database_connection,
    )
    interests_repository: providers.Factory[
        repo_interfaces.InterestsRepositoryInterface
    ] = providers.Factory(
        repo_interests.InterestsDatabaseRepository,
        database_connection=database_connection,
    )
    visited_users_repository: providers.Factory[
        repo_interfaces.VisitsRepoInterface
    ] = providers.Factory(
        repo_visits.VisitedUsersDatabaseRepo, database_connection=database_connection
    )
    matched_repository: providers.Factory[
        repo_interfaces.MatchedUsersRepoInterface
    ] = providers.Factory(
        repo_visits.MatchedUsersRepoDatabase, database_connection=database_connection
    )
    matcha_search_repository: providers.Factory[
        repo_interfaces.MatchaInterface
    ] = providers.Factory(
        repo_matcha.MatchaDatabaseRepository, database_connection=database_connection
    )
    system_events_repository: providers.Factory[
        repo_interfaces.SystemEventsRepoInterface
    ] = providers.Factory(
        repo_system_events.SystemEventsRepository,
        database_connection=database_connection,
    )
    chat_repository: providers.Factory[
        repo_chat.ChatDatabaseRepository
    ] = providers.Factory(
        repo_chat.ChatDatabaseRepository, database_connection=database_connection
    )

    websocket_system_events: providers.Factory[
        system_events.WebsocketSystemEvents
    ] = providers.Factory(
        system_events.WebsocketSystemEvents,
        repo_system_events=system_events_repository,
        repo_profile=profile_repository,
        ws_manager=websocket_manager,
    )
    websocket_chat_events: providers.Factory[
        chat_events.WebsocketChatEvents
    ] = providers.Factory(
        chat_events.WebsocketChatEvents,
        repo_chat=chat_repository,
        repo_profile=profile_repository,
        ws_manager=websocket_manager,
    )

    user_relationships: providers.Factory[
        matcha_visits.UsersRelationships
    ] = providers.Factory(
        matcha_visits.UsersRelationships,
        repo_profile=profile_repository,
        repo_matched=matched_repository,
        repo_visited=visited_users_repository,
        websocket_system_events=websocket_system_events,
    )
    location_client: providers.Resource[locations.LocationClient] = providers.Resource(
        locations.LocationClient,
        base_url=settings.settings_location.service_url,
    )
    location_service: providers.Factory[locations.LocationService] = providers.Factory(
        locations.LocationService,
        location_client=location_client,
        location_repository=location_repository,
    )
    coordinates_helpers: providers.Resource[
        mathcha_helpers.CoordinatesMatchaHelpers
    ] = providers.Resource(mathcha_helpers.CoordinatesMatchaHelpers)

    avatars_service: providers.Resource[
        redis_avatars.UsersAvatarsRedisRepo
    ] = providers.Resource(
        redis_avatars.UsersAvatarsRedisRepo, redis_connection=redis_connection
    )
    matcha_search_service: providers.Factory[
        matcha_search.MatchaSearch
    ] = providers.Factory(
        matcha_search.MatchaSearch,
        repo_profile=profile_repository,
        repo_matcha_search=matcha_search_repository,
        repo_preferences=preferences_repository,
        repo_locations=location_repository,
        coordinates_helpers=coordinates_helpers,
    )

    recommendations_repo: providers.Resource[
        redis_recommendations.UserRecommendationsService
    ] = providers.Resource(
        redis_recommendations.UserRecommendationsService,
        redis_connection=redis_connection,
    )
    matcha_recommendations_service: providers.Factory[
        matcha_search.MatchaRecommendations
    ] = providers.Factory(
        matcha_search.MatchaRecommendations,
        repo_recommendations=recommendations_repo,
        repo_profile=profile_repository,
        repo_matcha_search=matcha_search_repository,
        repo_preferences=preferences_repository,
        matcha_search_service=matcha_search_service,
    )
