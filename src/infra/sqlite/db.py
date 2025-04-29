from sqlalchemy import Engine, create_engine
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.app_config import DataBaseConfig


def create_db_engine(config: DataBaseConfig) -> AsyncEngine:
    if config.pool_size is not None:
        return create_async_engine(
            config.uri,
            echo=config.echo,
            pool_size=config.pool_size,
            max_overflow=config.max_overflow,
            pool_timeout=config.pool_timeout,
            pool_recycle=config.pool_recycle,
        )
    else:
        return create_async_engine(
            config.uri,
            echo=config.echo,
        )

def create_sync_db_engine(config: DataBaseConfig) -> Engine:
    if config.pool_size is not None:
        return create_engine(
            config.sync_uri,
            echo=config.echo,
            pool_size=config.pool_size,
            max_overflow=config.max_overflow,
            pool_timeout=config.pool_timeout,
            pool_recycle=config.pool_recycle,
        )
    else:
        return create_engine(
            config.sync_uri,
            echo=config.echo,
        )


def create_session_factory(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(
        bind=engine,
        expire_on_commit=False,
        class_=AsyncSession,
    )
