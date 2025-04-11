from fastapi import Depends

from Services.Reservation.repository import ReservationsRepository, get_reservations_repository
from Services.Reservation.schema import CreateReservation


class ReservationsService:

    def __init__(self, repository: ReservationsRepository = Depends(get_reservations_repository)):
        self.__repository = repository


    async def get_all_reservations(self):
        return await self.__repository.all()


    async def create_reservation(self, reservation: CreateReservation):
        return await self.__repository.create_reservation(reservation)


    async def delete_reservation(self, id: int):
        return await self.__repository.delete(id)


async def get_reservations_service(repository: ReservationsRepository = Depends(get_reservations_repository)):
    return ReservationsService(repository=repository)


reservations_service: ReservationsService = Depends(get_reservations_service)