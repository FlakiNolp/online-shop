from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import insert, select, Sequence, Row
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Type, List, Tuple

from api.core.application.abstract_classes.abstract_repository import AbstractRepository
from api.infrastructure.persistence.configurations.models import (User, Product, Order, OrderProduct, Category, Image, Base)
from api.core.application.abstract_classes.abstract_specification import AbstractSpecification


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
        elif len(results) >= 1 and isinstance(results[0], Row):
            return [list(i) for i in results]
        return [i for i in results]

    async def add(self, data: dict):
        try:
            res = await self._session.scalars(insert(self.model).values(**data).returning(self.model.uuid))
            return res.one()
        except SQLAlchemyError as e:
            print(e)
            await self._session.rollback()
            raise e

    async def update(self):
        async with self as session:
            await session

    async def delete(self):
        async with self as session:
            await session

    async def get_one(self, specification: AbstractSpecification.is_satisfied) -> dict:
        try:
            return self.__dict__((await self._session.scalars(select(self.model).filter_by(**specification))).one())
        except SQLAlchemyError as e:
            raise e

    async def get_many(self, specification: AbstractSpecification.is_satisfied = None) -> List[dict]:
        if specification is None:
            specification = {}
        try:
            return self.__dict__((await self._session.scalars(select(self.model).filter_by(**specification))).all())
        except SQLAlchemyError as e:
            print(e)

    async def join(self):
        async with self as session:
            await session
