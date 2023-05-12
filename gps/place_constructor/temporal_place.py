from gps.place_constructor.place import Place


class TemporalPlace(Place):
    def __init__(self, name, frequency):
        super().__init__(name, frequency)

    def within(self, location) -> bool:
        return True
