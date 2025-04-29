import os
from pathlib import Path

import pytest
from asgi_lifespan import LifespanManager
from httpx import ASGITransport, AsyncClient
from pytest_asyncio import fixture as async_fixture
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import Session, sessionmaker

from src.app import init_app
from tests.factories.user import user_factory  # noqa

from src.infra.sqlite.db import create_sync_db_engine
from src.app_config import Config
from src.infra.models.base import Base


sqlite_path = Path(__file__).resolve().parent.parent / "test.db"


@pytest.fixture(scope="session")
def test_config() -> Config:
    config = Config()
    config.database.path = str(sqlite_path)
    yield config
    os.remove(sqlite_path)


@pytest.fixture(scope="session")
async def engine(test_config: Config):
    engine = create_async_engine(test_config.database.uri, echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest.fixture(scope="function")
async def session(engine) -> AsyncSession:
    async_session = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)
    async with async_session() as session:
        yield session


@pytest.fixture(scope="session")
def sync_engine(test_config: Config):
    engine = create_sync_db_engine(test_config.database)
    yield engine
    engine.dispose()


@pytest.fixture(scope="function")
def sync_session(sync_engine) -> Session:
    session_maker = sessionmaker(bind=sync_engine, expire_on_commit=False)
    with session_maker() as session:
        yield session


@async_fixture(scope="function")
async def client(test_config) -> AsyncClient:
    app = init_app(test_config)
    async with LifespanManager(app):
        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://testserver",
            follow_redirects=True,
        ) as client:
            yield client
