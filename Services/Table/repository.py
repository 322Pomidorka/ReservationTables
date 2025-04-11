from fastapi import Depends

from Services.Table.model import Table
from Shared.Base.BaseRepository import BaseRepository
from Shared.Database.Sessions import AsyncDatabase


class TablesRepository(BaseRepository):
    model = Table


async def get_tables_repository(session: AsyncDatabase = Depends(AsyncDatabase.get_session)):
    return TablesRepository(session)


tables_repository: TablesRepository = Depends(get_tables_repository)