from auth.infrastructure.creational.singleton import Singleton
import auth.config as config
from auth.infrastructure.persistence.configurations.models import Base

from sqlalchemy import URL, MetaData
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
import sqlalchemy.exc


class SQLAlchemyDataBase(metaclass=Singleton):
    metadata: MetaData = Base.metadata

    def __init__(self, db_user: str = config.DB_USER,
                 db_password: str = config.DB_PASSWORD,
                 db_host: str = config.DB_HOST,
                 db_port: int = config.DB_PORT,
                 db_name: str = config.DB_NAME,
                 test_mode: bool = False):
        if test_mode:
            self._url = URL.create(drivername="postgresql+asyncpg", username=db_user, password=db_password,
                                   host=db_host,
                                   port=db_port,
                                   database="test")
        else:
            self._url = URL.create(drivername="postgresql+asyncpg", username=db_user, password=db_password,
                                   host=db_host,
                                   port=db_port,
                                   database=db_name)
        self._async_engine = create_async_engine(self._url)
        self.async_session_maker = async_sessionmaker(self._async_engine, expire_on_commit=False)

    async def create_schema(self):
        async with self._async_engine.begin() as conn:
            await conn.run_sync(self.metadata.create_all)
