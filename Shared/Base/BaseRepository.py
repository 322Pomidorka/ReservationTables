import logging

from Shared.Base.Settings import Settings
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from Shared.CustomError.custom_error import NotFoundInDBError
from Shared.Utils.Handle_db_errors import handle_db_errors


class BaseRepository:
    """
        Базовый класс для работы с БД
    """

    model = None

    def __init__(self, session):
        self.session: AsyncSession = session


    @handle_db_errors
    async def id(self, model_id: int):
        model = await self.session.get(self.model, model_id)
        if model is not None:
            return model
        raise NotFoundInDBError


    @handle_db_errors
    async def all(self):
        query = select(self.model)
        result = await self.session.execute(query)
        return result.scalars().all()


    @handle_db_errors
    async def create(self, data: dict):
        model = self.model(**data)
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return model


    @handle_db_errors
    async def delete(self, model_id: int):
        model = await self.id(model_id)
        if not model:
            raise NotFoundInDBError
        await self.session.delete(model)
        await self.session.commit()
        return 200
