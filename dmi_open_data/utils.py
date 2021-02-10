from datetime import datetime
from math import cos, asin, sqrt, pi


# Constants
CONST_EARTH_RADIUS = 6371       # km
CONST_EARTH_DIAMETER = 12742    # km
EPOCH = datetime.utcfromtimestamp(0)


def date2microseconds(date: datetime) -> int:
    return int((date - EPOCH).total_seconds() * 1000000.0)


def microseconds2date(microseconds: float) -> datetime:
    return datetime.utcfromtimestamp(microseconds / 1000000)


# From Stackoverflow answer
# https://stackoverflow.com/a/21623206/2538589
def distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate distance in km between two geographical points.

    Args:
        lat1 (float): Latitude of point 1.
        lon1 (float): Longitude of point 1.
        lat2 (float): Latitude of point 2.
        lon2 (float): Longitude of point 2.

    Returns:
        float: Haversine distance in km between point 1 and 2.
    """
    p = pi / 180.0
    a = 0.5 - cos((lat2 - lat1) * p) / 2.0 + cos(lat1 * p) * cos(lat2 * p) * (1.0 - cos((lon2 - lon1) * p)) / 2
    return CONST_EARTH_DIAMETER * asin(sqrt(a))  # 2*R*asin...
