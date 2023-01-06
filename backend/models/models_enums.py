"""Enums for different models."""

import enum


class SexualPreferencesEnum(enum.IntEnum):
    """Sexual preferences for user."""

    BI = 0
    HETEROSEXUAL = 1
    HOMOSEXUAL = 2


class GenderEnum(enum.IntEnum):
    """Gender of users."""

    MALE = 0
    FEMALE = 1


class SearchOrderEnum(enum.IntEnum):
    """Order of search."""

    ASC = 0
    DESC = 1


class SocketEventTypesEnum(enum.IntEnum):
    """Types of socket events."""

    SYSTEM = 0
    CHAT = 1


class SocketSystemTypesEnum(enum.IntEnum):
    """Types for system events."""

    LIKE = 0
    MATCH = 1
    UNLIKE = 2
    GUEST = 3
    MESSAGE = 4
