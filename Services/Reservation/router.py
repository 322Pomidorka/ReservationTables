import logging

from fastapi import APIRouter, HTTPException

from Services.Reservation.schema import CreateReservation
from Services.Reservation.serivce import reservations_service
from Shared.CustomError.custom_error import NotFoundInDBError, OverlappingReservationError

reservations_router = APIRouter()


@reservations_router.get('/reservations/', name='получение всех броней')
async def all_reservations(service = reservations_service):
    try:
        reservations = await service.get_all_reservations()
        logging.info(f"Получен список броней")

        return reservations
    except Exception as e:
        logging.error(f"Ошибка при получении списка броней: {e}")
        raise HTTPException(status_code=500, detail=e)


@reservations_router.post('/reservations/', name='создание брони')
async def create_reservations(reservation: CreateReservation, service = reservations_service):
    try:
        db_reservation = await service.create_reservation(reservation)
        logging.info(f"Создана новая бронь: {db_reservation}")

        return db_reservation
    except NotFoundInDBError as e:
        logging.error(f"Ошибка при создании брони (не найден стол с id:{reservation.table_id}): {e}", exc_info=True)
        raise HTTPException(status_code=404, detail=e)
    except OverlappingReservationError as e:
        logging.error(f"Ошибка при создании брони (конфликт по времени): {e}", exc_info=True)
        raise HTTPException(status_code=400, detail=e)
    except Exception as e:
        logging.error(f"Ошибка при создании брони: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=e)


@reservations_router.delete('/reservations/{id}', name='удаление брони')
async def delete_reservations(id: int, service = reservations_service):
    try:
        result = await service.delete_reservation(id)
        logging.info(f"Бронь с id: {id} удалена")

        return result
    except NotFoundInDBError as e:
        logging.error(f"Ошибка при удалении брони (не найдена бронь с id:{id}): {e}", exc_info=True)
        raise HTTPException(status_code=404, detail=e)
    except Exception as e:
        logging.error(f"Ошибка при удалении брони: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=e)