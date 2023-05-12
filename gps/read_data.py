import json

from api_adapter.osm_api_adapter import OSMApiAdapter
from global_const import MINUTE, MIN_FREQUENCY
from location import Border
from place_constructor.personal_place import PersonalPlace
from place_constructor.public_place import PublicPlace
from place_constructor.temporal_place import TemporalPlace
from user import User


def get_border(info: dict) -> Border:
    if info.get('osm_id', None) is None:
        return Border([])
    coordinates = api.select_query('by_id', info['osm_id'], info.get('osm_type', 'nwr'))[0].geometry()['coordinates']
    if isinstance(coordinates[0][0], list):
        coordinates = coordinates[0]
    coordinates = [coord[::-1] for coord in coordinates]
    return Border(coordinates[0::info.get('discharge', 1)])


api = OSMApiAdapter()

file = open('gps/data.json')
data = json.load(file)

places = {}
for place in data['places']:
    name = place.get('name', None)
    frequency = place.get('frequency', MIN_FREQUENCY) * MINUTE
    places[place['id']] = {'PublicPlace': PublicPlace(name, frequency, place.get('tags', []), api),
                           'PersonalPlace': PersonalPlace(name, frequency, get_border(place)),
                           'TemporalPlace': TemporalPlace(name, frequency),
                           'city': get_border(place)
                           }[place['category']]

users = []
for user in data['users']:
    user_places = {'places': [places[i] for i in user['places']],
                   'cities': [places[i] for i in user['cities']],
                   'temporal': {places[i].name: places[i] for i in user['temporal']}}
    users.append(User(user['app_cloud_id'], user['name'], user_places))
