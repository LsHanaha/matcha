"""User can set his/her preference for search."""

import fastapi
from dependency_injector.wiring import Provide, inject
from fastapi_jwt_auth import AuthJWT

from backend import ioc
from backend.models import models_preferences
from backend.repositories import repo_preference as preference_repositories
