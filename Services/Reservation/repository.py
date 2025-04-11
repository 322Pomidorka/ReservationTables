import logging
from datetime import timedelta

from fastapi import Depends
from sqlalchemy import select, func

from Services.Reservation.model import Reservation
from Services.Reservation.schema import CreateReservation
from Services.Table.model import Table
from Shared.Base.BaseRepository import BaseRepository
from Shared.CustomError.custom_error import OverlappingReservationError, NotFoundInDBError
from Shared.Database.Sessions import AsyncDatabase
from Shared.Utils.Handle_db_errors import handle_db_errors


class ReservationsRepository(BaseRepository):
    model = Reservation


    @handle_db_errors
    async def create_reservation(self, reservation):
        """
            Создание брони, с проверкой по времени
        """

        query = select(Table).where(Table.id == reservation.table_id)
        result = await self.session.execute(query)
        table = result.scalars().first()

        if table is None:
            logging.info(f"Столик с заданным id:{reservation.table_id} - не найден")
            raise NotFoundInDBError

        is_overlapping = await self.check_overlapping_reservation(reservation)

        if is_overlapping:
            raise OverlappingReservationError

        db_reservation = Reservation(**reservation.dict())
        self.session.add(db_reservation)
        await self.session.commit()
        await self.session.refresh(db_reservation)

        return db_reservation


    @handle_db_errors
    async def check_overlapping_reservation(self, reservation: CreateReservation) -> bool:
        """
            Проверка на пересечение броней по времени
            Вычисляем начало и конец новой брони, и ищем совпадение в базе
        """

        start_time = reservation.reservation_time
        end_time = start_time + timedelta(minutes=reservation.duration_minutes)

        overlapping_reservation_result = await self.session.execute(
            select(Reservation).where(
                Reservation.table_id == reservation.table_id,
                Reservation.reservation_time < end_time,
                Reservation.reservation_time + func.make_interval(0, 0, 0, 0, 0, Reservation.duration_minutes) > start_time  # type: ignore
            )
        )

        overlapping_reservation = overlapping_reservation_result.scalars().first()

        if overlapping_reservation:
            logging.info(f"У новай брони есть конфликты по времени: {overlapping_reservation}")
            return True

        logging.info(f"У новай брони нет конфликтов по времени")
        return False


async def get_reservations_repository(session=Depends(AsyncDatabase.get_session)):
    return ReservationsRepository(session)