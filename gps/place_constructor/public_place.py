from gps.api_adapter.map_api_adapter import MapApiAdapter
from gps.location import Location
from gps.place_constructor.place import Place


class PublicPlace(Place):
    def __init__(self, name: str, frequency: int, tags: list[str], map_api: MapApiAdapter):
        super().__init__(name, frequency)
        self.map_api = map_api
        self.tags = tags

    def within(self, location: Location) -> bool:
        nearest_elements = self.map_api.select_query('nearest', location, self.tags)
        return len(nearest_elements) > 0
