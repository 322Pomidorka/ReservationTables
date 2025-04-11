from fastapi import Depends

from Services.Table.repository import get_tables_repository, TablesRepository
from Services.Table.schema import CreateTable


class TablesService:

    def __init__(self, repository: TablesRepository = Depends(get_tables_repository)):
        self.__repository = repository


    async def get_all_tables(self):
        """
            Получение всех столиков
        """
        return await self.__repository.all()


    async def create_table(self, table: CreateTable):
        """
            Создание столика
        """
        return await self.__repository.create({**table.__dict__})


    async def delete_table(self, id: int):
        """
            Удаление столика
        """
        return await self.__repository.delete(id)


async def get_tables_service(repository: TablesRepository = Depends(get_tables_repository)):
    return TablesService(repository=repository)


tables_service: TablesService = Depends(get_tables_service)