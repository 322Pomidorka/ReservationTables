import logging

from fastapi import APIRouter, HTTPException

from Services.Table.schema import CreateTable
from Services.Table.serivce import tables_service
from Shared.CustomError.custom_error import NotFoundInDBError

tables_router = APIRouter()


@tables_router.get('/tables/', name='получение всех столиков')
async def all_tables(service = tables_service):
    try:
        tables =  await service.get_all_tables()
        logging.info(f"Получен список столиков")

        return tables
    except Exception as e:
        logging.error(f"Ошибка при получении списка столиков: {e}")
        raise HTTPException(status_code=500, detail=e)


@tables_router.post('/tables/', name='создание столика')
async def create_tables(table: CreateTable, service = tables_service):
    try:
        db_table = await service.create_table(table)
        logging.info(f"Создан новый столик: {db_table}")

        return db_table
    except Exception as e:
        logging.error(f"Ошибка при создании столика: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=e)


@tables_router.delete('/tables/{id}', name='удаление столика')
async def delete_tables(id: int, service = tables_service):
    try:
        result = await service.delete_table(id)
        logging.info(f"Столик с id: {id} удален")

        return result
    except NotFoundInDBError as e:
        logging.error(f"Ошибка при удалении столика (не найдет стол с id:{id}): {e}", exc_info=True)
        raise HTTPException(status_code=404, detail=e)
    except Exception as e:
        logging.error(f"Ошибка при удалении столика: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=e)