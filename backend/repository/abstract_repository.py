from abc import abstractmethod, ABC

class AbstractRepository(ABC):

    @abstractmethod
    def get(self, id: int, lazy: bool):
        raise NotImplementedError()

    @abstractmethod
    def create(self, data: dict):
        raise NotImplementedError()

