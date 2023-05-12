from gps.global_const import MAX_RADIUS
from gps.location import Location, Border
from gps.place_constructor.place import Place


class PersonalPlace(Place):
    def __init__(self, name: str, frequency: int, border: Border) -> None:
        super().__init__(name, frequency)
        self.border = border

    def within(self, location: Location) -> bool:
        if self.border.within(location):
            return True
        return self.border - location < MAX_RADIUS
