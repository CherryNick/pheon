from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")


class RepositoryProtocol(ABC, Generic[T]):
    @abstractmethod
    async def get_by_id(self, id_: int) -> T | None:
        ...

    @abstractmethod
    async def add(self, obj: T) -> None:
        ...

    @abstractmethod
    async def delete(self, obj: T) -> None:
        ...
