from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import insert, select, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Type, List

from cart.core.application.abstract_classes.abstract_repository import AbstractRepository
from cart.infrastructure.persistence.configurations.models import (User, Product, Order, OrderProduct, Category, Image, Base)
from cart.core.application.abstract_classes.abstract_specification import AbstractSpecification


class SQLAlchemyRepository(AbstractRepository):
    model: Type[User | Product | Order | OrderProduct | Category | Image] = None

    def __init__(self, session: AsyncSession):
        self._session = session

    @classmethod
    def __dict__(cls, results) -> List[dict] | dict:
        if isinstance(results, Sequence):
            if len(results) > 1:
                return [i.__dict__ for i in results]
            else:
                return {}
        elif isinstance(results, Base):
            return results.__dict__
        else:
            return [list(i) for i in results]

    async def add(self, data: dict) -> User | Product | Order | OrderProduct | Category | Image:
        try:
            res = self.model(**data)
            self._session.add(res)
            return res
        except SQLAlchemyError as e:
            await self._session.rollback()
            raise e

    async def update(self, data: dict, specification: AbstractSpecification.is_satisfied) -> dict:
        ...

    async def delete(self):
        async with self as session:
            await session

    async def get_one(self, specification: AbstractSpecification.is_satisfied) -> dict:
        try:
            return self.__dict__((await self._session.scalars(select(self.model).filter_by(**specification))).one())
        except SQLAlchemyError as e:
            raise e

    async def get_many(self, specification: AbstractSpecification.is_satisfied = None) -> Sequence[model]:
        if specification is None:
            specification = {}
        try:
            return (await self._session.scalars(select(self.model).filter_by(**specification))).all()
        except SQLAlchemyError as e:
            print(e)

    async def join(self):
        async with self as session:
            await session
