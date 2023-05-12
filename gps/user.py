from gps.global_const import WALK_SPEED, MIN_FREQUENCY, MINUTE
from gps.location import GPSLocation
from gps.place_constructor.temporal_place import TemporalPlace


class User:
    place = TemporalPlace('start', MIN_FREQUENCY * MINUTE)
    gps_location = None

    def __init__(self, app_cloud_id: str, name: str, places: dict) -> None:
        self.app_cloud_id = app_cloud_id
        self.name = name
        self.places = places

    @property
    def place_name(self) -> str:
        return self.place.name

    @property
    def frequency(self) -> int:
        return self.place.frequency

    def change_place(self, gps_location: GPSLocation) -> None:
        print(self.name, 0 if gps_location is None else gps_location - self.gps_location)
        if gps_location is None:
            self.place = self.places['temporal']['lost']
            return
        speed = gps_location - self.gps_location
        self.gps_location = gps_location
        if sum([city.within(gps_location.location) for city in self.places['cities']]) == 0:
            self.place = self.places['temporal']['travel']
            return

        if speed > WALK_SPEED:
            self.place = self.places['temporal']['transit']
            return

        for place in self.places['places']:
            if place.within(gps_location.location):
                self.place = place
                return

    def print(self):
        print(self.name, end=': ')
        print(self.place.name, end=' ')
        if self.gps_location is not None:
            print('lat: ', self.gps_location.location.latitude, end=' ')
            print('lon: ', self.gps_location.location.longitude, end=' ')
            print('time: ', self.gps_location.timestamp, end='\n')
