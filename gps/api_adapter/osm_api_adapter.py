from OSMPythonTools.overpass import Overpass

from gps.api_adapter.map_api_adapter import MapApiAdapter
from gps.global_const import MAX_RADIUS
from gps.location import Location


class OSMApiAdapter(MapApiAdapter):
    def __init__(self):
        super().__init__()
        self._create_connection()

    def _create_connection(self):
        self.overpass = Overpass()

    def select_query(self, query_method, *args):
        query = {'nearest': self._query_nearest,
                 'by_id': self._query_by_id}[query_method](*args)
        return self.overpass.query(query).elements()

    @staticmethod
    def _query_nearest(location: Location, tags=None) -> str:
        query = '('
        if tags is not None:
            for key, value in tags:
                query += f'nwr[{key}={value}](around:{MAX_RADIUS}, {location.latitude}, {location.longitude});'
        else:
            query += f'around:{MAX_RADIUS}, {location.latitude}, {location.longitude}'
        query += '); out geom;'
        return query

    @staticmethod
    def _query_by_id(way_id: int, type_element='nwr') -> str:
        return f'{type_element}({way_id}); out geom;'
