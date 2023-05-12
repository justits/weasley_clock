from abc import ABC, abstractmethod

from gps.location import Location


class MapApiAdapter(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def _create_connection(self):
        pass

    @abstractmethod
    def select_query(self, query_method, *args):
        pass

    @staticmethod
    def _query_nearest(location: Location, tags: list) -> str:
        pass

    @staticmethod
    def _query_by_id(way_id: int, type_element: str) -> str:
        pass
