from abc import ABC, abstractmethod


class AbstractSpecification(ABC):
    @abstractmethod
    def is_satisfied(self, *args):
        raise NotImplementedError
