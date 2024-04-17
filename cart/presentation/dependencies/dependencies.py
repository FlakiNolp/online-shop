from typing import Annotated
from fastapi import Depends, Cookie, Header
from functools import lru_cache
from motor.motor_asyncio import AsyncIOMotorClientSession

from cart.infrastructure.persistence.utils.unit_of_work import UnitOfWork
from cart.core.application.abstract_classes.abstract_unit_of_work import AbstractUnitOfWork
from cart.config import SECRET_KEY, ALGORITHM
from cart.infrastructure.utils.auth import Auth
from cart.infrastructure.persistence.utils.mongo_database import MongoDatabase

UOWDepend = Annotated[AbstractUnitOfWork, Depends(UnitOfWork)]
mongodb = MongoDatabase()


@lru_cache()
def get_auth() -> Auth:
    return Auth(SECRET_KEY, ALGORITHM)


async def authenticate_user(access_token: Annotated[str, Header(alias="Authorization")],
                            auth: Auth = Depends(get_auth, use_cache=True)):
    return await auth.decode_token(access_token)


async def get_mongo(mongo: AsyncIOMotorClientSession = Depends(mongodb.get_session)):
    return mongo


auth_depend = Annotated[AbstractUnitOfWork, Depends(authenticate_user)]
