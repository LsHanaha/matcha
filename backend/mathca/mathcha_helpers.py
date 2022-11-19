"""Helpers functions."""
from math import asin, cos, radians, sin, sqrt

from backend.models.models_location import CoordinatesLocationModel

_EARTH_RADIUS_KM: int = 6371

_DISTANCE_BETWEEN_LATITUDE_KM: float = 110.8
_DISTANCE_BETWEEN_LONGITUDE_EQUATOR: float = 111.3


def calculate_distance_from_coords(
    coord1: CoordinatesLocationModel,
    coord2: CoordinatesLocationModel,
) -> float:
    """Calculate distance between two points with Haversine formula."""

    longitude1: float = radians(coord1.longitude)
    latitude1: float = radians(coord1.latitude)
    longitude2: float = radians(coord2.longitude)
    latitude2: float = radians(coord2.latitude)

    delta_longitude: float = longitude2 - longitude1
    delta_latitude: float = latitude2 - latitude1

    a: float = (
        sin(delta_latitude / 2) ** 2
        + cos(latitude1) * cos(latitude2) * sin(delta_longitude / 2) ** 2
    )
    return 2 * asin(sqrt(a)) * _EARTH_RADIUS_KM


def calculate_coords_from_distance(
    coords: CoordinatesLocationModel, distance: int
) -> tuple[float, float, float, float]:
    """Calculate coordinates from point and distance.

    Returns
    """
    lat_delta: float = distance / _DISTANCE_BETWEEN_LATITUDE_KM
    lng_delta: float = (coords.latitude / 90) * _DISTANCE_BETWEEN_LONGITUDE_EQUATOR
    return (
        coords.latitude - lat_delta,
        coords.latitude + lat_delta,
        coords.longitude - lng_delta,
        coords.longitude + lng_delta,
    )
