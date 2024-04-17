from abc import ABC, abstractmethod


class AbstractRepository(ABC):
    @abstractmethod
    async def add(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def delete(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def update(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def get_one(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def get_many(self, **kwargs):
        raise NotImplementedError
