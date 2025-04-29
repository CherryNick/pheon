from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import Engine, insert, select
from starlette.middleware.cors import CORSMiddleware

from src.app_config import Config
from src.extensions.logger import logger
from src.infra.models import Base, User
from src.infra.sqlite.db import create_db_engine, create_session_factory, create_sync_db_engine
from src.modules.auth.routes import router as auth_router
from src.utils import pwd_context


def insert_system_user(sync_engine: Engine, system_user_password: str) -> None:
    try:
        with sync_engine.connect() as connection:
            stmt_check = select(User).where(User.id == 1)
            result = connection.execute(stmt_check).first()
            if result:
                logger.info("System user already exists. Skipping insertion.")
                return

            stmt_insert = insert(User).values(
                id=1,
                username="system",
                password_hash=pwd_context.hash(system_user_password),
            )
            connection.execute(stmt_insert)
            connection.commit()
            logger.info("System user inserted successfully.")
    except Exception as e:
        logger.error("Failed to insert system user.")
        logger.exception(e)
        raise


def init_app(config: Config) -> FastAPI:
    try:
        sync_engine = create_sync_db_engine(config.database)
        Base.metadata.create_all(sync_engine)
        insert_system_user(sync_engine, config.system.user_password)
        sync_engine.dispose()

        engine = create_db_engine(config.database)
        session_factory = create_session_factory(engine)
    except Exception as e:
        logger.error("Failed to create database engine or session factory")
        logger.exception(e)
        raise SystemExit(1) from e

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> None:
        app.state.config = config
        app.state.db_session_factory = session_factory
        yield

    app = FastAPI(
        title="Pheon REST API",
        redirect_slashes=False,
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.cors_origins,
        allow_credentials=True,
        allow_methods=("GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS"),
        allow_headers=(
            "Access-Control-Allow-Headers",
            "Content-Language",
            "Content-Type",
            "Authorization",
            "Access-Control-Allow-Origin",
        ),
    )

    app.include_router(auth_router)

    return app
