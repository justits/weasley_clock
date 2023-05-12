from abc import ABC, abstractmethod


class Place(ABC):
    def __init__(self, name: str, frequency: int) -> None:
        self.name = name
        self.frequency = frequency

    @abstractmethod
    def within(self, location) -> bool:
        pass
