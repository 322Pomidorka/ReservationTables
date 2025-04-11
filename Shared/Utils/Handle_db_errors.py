from functools import wraps

from sqlalchemy.exc import SQLAlchemyError
from typing_extensions import Any


def handle_db_errors(func):
    """
    Декоратор для обработки ошибок SQLAlchemy
    """
    @wraps(func)
    async def wrapper(*args: Any, **kwargs: Any):
        try:
            return await func(*args, **kwargs)
        except SQLAlchemyError as e:
            print(f"Ошибка базы данных в функции '{func.__name__}': {e}")
            session = args[0].session
            await session.rollback()
            raise
        except Exception as e:
            print(f"Непредвиденная ошибка '{func.__name__}': {e}")
            raise

    return wrapper