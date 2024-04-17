from abc import ABC, abstractmethod

import auth.infrastructure.persistence.repositories as repositories


class AbstractUnitOfWork(ABC):
    user: repositories.user_repository.UserRepository
    product: repositories.product_repository.ProductRepository
    image: repositories.image_repository.ImageRepository
    category: repositories.category_repository.CategoryRepository
    order: repositories.order_repository.OrderRepository
    order_product: repositories.order_product_repository.OrderProductRepository

    @abstractmethod
    def __init__(self):
        raise NotImplementedError

    @abstractmethod
    async def __aenter__(self):
        raise NotImplementedError

    @abstractmethod
    async def __aexit__(self, *args):
        raise NotImplementedError

    @abstractmethod
    async def commit(self):
        raise NotImplementedError

    @abstractmethod
    async def rollback(self):
        raise NotImplementedError

    @abstractmethod
    async def flush(self, *args):
        raise NotImplementedError
