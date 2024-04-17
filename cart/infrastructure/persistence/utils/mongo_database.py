from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorClientSession

from cart.infrastructure.creational.singleton import Singleton
import cart.config as config


class MongoDatabase(metaclass=Singleton):
    def __init__(self, mongo_user: str = config.MONGO_USER,
                 mongo_password: str = config.MONGO_PASSWORD,
                 mongo_host: str = config.MONGO_HOST,
                 mongo_port: int = config.MONGO_PORT,
                 test_mode: bool = False):
        if test_mode:
            self.motor = AsyncIOMotorClient(mongo_host, mongo_port, username=mongo_user, password=mongo_password,
                                            uuidRepresentation='standard')
            self.database = self.motor.get_database("cart")
        else:
            self.motor = AsyncIOMotorClient(mongo_host, mongo_port, username=mongo_user, password=mongo_password,
                                            uuidRepresentation='standard')
            self.database = self.motor.get_database("cart")

    async def get_session(self) -> AsyncIOMotorClientSession:
        async with await self.motor.start_session() as session:
            try:
                yield session
            finally:
                await session.end_session()
