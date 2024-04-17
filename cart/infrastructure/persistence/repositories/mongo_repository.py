from pymongo.results import InsertOneResult
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import insert, select, Sequence
from typing import Type, List
from motor.motor_asyncio import AsyncIOMotorClientSession, AsyncIOMotorDatabase, AsyncIOMotorCollection

from cart.core.application.abstract_classes.abstract_repository import AbstractRepository
from cart.infrastructure.persistence.configurations.models import (User, Product, Order, OrderProduct, Category, Image, Base)
from cart.core.application.abstract_classes.abstract_specification import AbstractSpecification
from cart.infrastructure.persistence.utils.mongo_database import MongoDatabase


class MongoRepository(AbstractRepository):
    model: MongoDatabase = None

    def __init__(self, session: AsyncIOMotorClientSession, collection: str):
        self._session = session
        self._collection: AsyncIOMotorCollection = self.model.database.get_collection(collection)

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

    async def update(self, data: dict, specification: AbstractSpecification.is_satisfied):
        try:
            await self._collection.update_one(specification, {'$inc': {'count': 1}}, upsert=True, session=self._session)
            #await self._collection.update_one(filter=specification, update={'$addToSet': data['product_id']}, session=self._session)
            #await self._collection.update_one(filter=specification, update=data, session=self._session)
        except Exception as e:
            raise e

    async def add(self, data: dict) -> InsertOneResult:
        return await self._collection.insert_one(document=data, session=await self._session)

    async def delete(self):
        ...

    async def get_one(self, specification: AbstractSpecification.is_satisfied) -> dict:
        ...

    async def get_many(self, specification: AbstractSpecification.is_satisfied = None) -> List[dict]:
        ...
