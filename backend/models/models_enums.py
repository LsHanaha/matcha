"""Enums for different models."""


import enum


class SexualPreferencesEnum(enum.IntEnum):
    """Sexual preferences for user."""

    BI: int = 0
    HETEROSEXUAL: int = 1
    HOMOSEXUAL: int = 2


class GenderEnum(enum.IntEnum):
    """Gender of users."""

    MALE: int = 0
    FEMALE: int = 1


class SearchOrder(enum.IntEnum):
    """Order of search."""

    ASC: int = 0
    DESC: int = 1
