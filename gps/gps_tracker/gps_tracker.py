from abc import ABC, abstractmethod


class GPSTracker(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def _create_connection(self):
        pass

    @abstractmethod
    def select_query(self, query_method):
        pass
