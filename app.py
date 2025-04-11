import logging

import uvicorn
from fastapi import APIRouter, FastAPI

from Services.Reservation.router import reservations_router
from Services.Table.router import tables_router

# Настройка логирования
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


app = FastAPI(docs_url='/api/docs')

# Routers
router = APIRouter()
# Tables
router.include_router(tables_router, tags=['Table | Tables'], prefix='/tables')
# Reservations
router.include_router(reservations_router, tags=['Reservation | Reservations'], prefix='/reservations')


app.include_router(router, prefix='/api/v1')


if __name__ == '__main__':
    uvicorn.run("app:app", host='0.0.0.0', port=8009, reload=True)