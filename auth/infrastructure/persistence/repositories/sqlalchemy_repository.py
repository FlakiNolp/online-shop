from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Type

from auth.core.application.abstract_classes.abstract_repository import AbstractRepository
from auth.infrastructure.persistence.configurations.models import User, Product, Order, OrderProduct, Category, Image
from auth.core.application.abstract_classes.abstract_specification import AbstractSpecification


class SQLAlchemyRepository(AbstractRepository):
    model: Type[User | Product | Order | OrderProduct | Category | Image] = None

    def __init__(self, session: AsyncSession):
        self.__session = session

    async def add(self, data: dict):
        try:
            res = await self.__session.scalars(insert(self.model).values(**data).returning(self.model.uuid))
            return res.one()
        except SQLAlchemyError as e:
            await self.__session.rollback()

    async def update(self):
        async with self as session:
            await session

    async def delete(self):
        async with self as session:
            await session

    async def get(self, specification: AbstractSpecification.is_satisfied):
        try:
            res = await self.__session.scalars(select(self.model).filter_by(**specification))
            return res.one()
        except SQLAlchemyError as e:
            print(e)
            await self.__session.rollback()
            return None

    async def join(self):
        async with self as session:
            await session
