from typing import Annotated, AsyncIterator

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.app_config import Config


def get_config(req: Request) -> Config:
    return req.app.state.config


ConfigDep = Annotated[Config, Depends(get_config)]


async def get_db(request: Request) -> AsyncIterator[AsyncSession]:
    session_factory: async_sessionmaker[AsyncSession] = request.app.state.db_session_factory
    async with session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()


GetDBSessionDep = Annotated[AsyncSession, Depends(get_db)]
