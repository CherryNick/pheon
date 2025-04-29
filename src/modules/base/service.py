from dataclasses import dataclass

from src.app_config import Config
from src.infra.repositories.sqlalchemy.uow import SqlAlchemyRepositories


@dataclass(slots=True)
class BaseService:
    config: Config


@dataclass(slots=True)
class SqlAlchemyService(BaseService):
    repos: SqlAlchemyRepositories
