import logging

import sqlalchemy.engine.url as SQURL
from Shared.Base.Settings import Settings
from sqlalchemy import exc
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession


class AsyncDBSessions:

    def __init__(self):
        self.__URL = SQURL.URL.create(
            drivername="postgresql+asyncpg",
            username=Settings.database.user,
            password=Settings.database.password,
            host=Settings.database.host,
            port=Settings.database.port,
            database=Settings.database.database,
        )
        self.__engine = create_async_engine(self.__URL,
                                          pool_size=5,
                                          max_overflow=10,)
        self.__factory = async_sessionmaker(self.__engine, class_=AsyncSession, expire_on_commit=False)


    def get_url(self):
        return str(self.__URL)


    async def get_session(self) -> AsyncSession:
        async with self.__factory() as session:
            try:
                yield session
            except exc.SQLAlchemyError as error:
                logging.error(f"Ошибка при создании сессии базы данных: {error}", exc_info=True)
                await session.rollback()
                raise


AsyncDatabase = AsyncDBSessions()