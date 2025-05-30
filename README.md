📌 Цель
Разработать REST API для бронирования столиков в ресторане. Сервис должен позволять создавать, просматривать и удалять брони, а также управлять столиками и временными слотами.

✅ Функциональные требования
Модели:
Table – столик в ресторане:


id: int
name: str (например, "Table 1")
seats: int (количество мест)
location: str (например, "зал у окна", "терраса")
Reservation – бронь:


id: int
customer_name: str
table_id: int (FK на Table)
reservation_time: datetime
duration_minutes: int

Методы API:
Столики:


GET /tables/ — список всех столиков
POST /tables/ — создать новый столик
DELETE /tables/{id} — удалить столик
Брони:


GET /reservations/ — список всех броней
POST /reservations/ — создать новую бронь
DELETE /reservations/{id} — удалить бронь

Логика бронирования:
Нельзя создать бронь, если в указанный временной слот столик уже занят (пересечение по времени и table_id).
Бронь может длиться произвольное количество минут.
Валидации должны обрабатываться на уровне API (например, конфликт брони должен выдавать ошибку с пояснением).


Иструкция по запуску:
* в корне папке создать .env файл с данными о БД
    DB_LB_PORT
    DB_LB_HOST=db
    POSTGRES_DB
    DB_USER
    DB_PASSWORD
    SSL_PATH

* выполнитль каманду в папке с docker-compose 
    docker-compose up -d --build
