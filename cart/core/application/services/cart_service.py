from fastapi import HTTPException
from pymongo.results import InsertOneResult
from motor.motor_asyncio import AsyncIOMotorClientSession

from cart.presentation.schemas.cart import ProductId
from cart.infrastructure.persistence.utils.mongo_database import MongoDatabase

mongo = MongoDatabase()


class CartService:
    @staticmethod
    async def add_to_cart(mongo_session: AsyncIOMotorClientSession, new_product: ProductId, collection: str, quantity: int) -> InsertOneResult | HTTPException:
        try:
            if res := await mongo.database.get_collection(collection).find_one({"product_id": new_product.product_id}, session=mongo_session):
                if res.get("quantity") < quantity:
                    return await mongo.database.get_collection(collection).update_one({"product_id": new_product.product_id}, {'$inc': {'quantity': 1}}, upsert=True, session=mongo_session)
                else:
                    raise HTTPException(status_code=400, detail="Товар закончился")
            else:
                return await mongo.database.get_collection(collection).update_one(
                    {"product_id": new_product.product_id}, {'$inc': {'quantity': 1}}, upsert=True, session=mongo_session)
        except Exception as e:
            raise e

    @staticmethod
    async def remove_one_product(mongo_session: AsyncIOMotorClientSession, new_product: ProductId, collection: str):
        try:
            if res := await mongo.database.get_collection(collection).find_one({"product_id": new_product.product_id},
                                                                               session=mongo_session):
                if res.get("quantity") > 1:
                    await mongo.database.get_collection(collection).find_one_and_update(filter={"product_id": new_product.product_id}, update={'$inc': {'quantity': -1}}, upsert=True, session=mongo_session)
                elif res.get("quantity") == 1:
                    await mongo.database.get_collection(collection).delete_one(filter={"product_id": new_product.product_id}, session=mongo_session)
            else:
                raise HTTPException(status_code=404, detail="Товара нет в корзине")
        except Exception as e:
            raise e

    @staticmethod
    async def get_all_products(mongo_session: AsyncIOMotorClientSession, collection: str):
        try:
            res = await mongo.database.get_collection(collection).find(session=mongo_session).to_list(length=1000)
            if res:
                result = []
                for i in res:
                    result.append({"product_id": i["product_id"], "quantity": i["quantity"]})
                return result
            raise HTTPException(status_code=400, detail="Корзина пустая")
        except Exception as e:
            raise e

    @staticmethod
    async def clear_all_products(mongo_session: AsyncIOMotorClientSession, collection: str):
        try:
            res = await mongo.database.drop_collection(collection, session=mongo_session)
            if res:
                return res
            raise HTTPException(status_code=400, detail='Непридвиденная ошибка')
        except Exception as e:
            raise e
