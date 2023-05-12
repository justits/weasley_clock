from haversine import haversine
from shapely.ops import nearest_points
from shapely.geometry import Point, Polygon, LineString
import datetime

from gps.global_const import KILOMETER


class Location:
    def __init__(self, latitude: int, longitude: int):
        self.latitude = latitude
        self.longitude = longitude

    def __sub__(self, other) -> float:
        near = nearest_points(self.shapely, other.shapely)
        return haversine((near[0].x, near[0].y), (near[1].x, near[1].y)) * KILOMETER

    @property
    def shapely(self) -> Point:
        return Point(self.latitude, self.longitude)


class Border:
    def __init__(self, coordinates: list) -> None:
        self.coordinates = coordinates
        self.type = 'poly' if len(coordinates) > 0 and coordinates[0] != coordinates[-1] else 'line'

    def __sub__(self, other) -> float:
        near = nearest_points(self.shapely, other.shapely)
        return haversine((near[0].x, near[0].y), (near[1].x, near[1].y)) * KILOMETER

    @property
    def shapely(self) -> Point:
        return {'poly': Polygon(self.coordinates),
                'line': LineString(self.coordinates)}[self.type]

    def within(self, location: Location) -> bool:
        return location.shapely.within(self.shapely)


class GPSLocation:
    def __init__(self, location: Location, timestamp: datetime.datetime):
        self.location = location
        self.timestamp = timestamp

    def __sub__(self, other) -> float:
        if other is None or self is None or (self.timestamp - other.timestamp).seconds == 0:
            return 0
        print(self.location - other.location, abs((self.timestamp - other.timestamp).seconds))
        return (self.location - other.location) / abs((self.timestamp - other.timestamp).seconds)
