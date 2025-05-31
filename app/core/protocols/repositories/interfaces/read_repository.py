from typing import Protocol, runtime_checkable

from .generics_types import BaseORMModel


@runtime_checkable
class IReadRepository(Protocol[BaseORMModel]):
    """
    Readonly interface for reading from database
    For clients which doesn't need the writeable operations could be extended by IReadRepository
    """

    async def get_one(
        self,
        *where,
        **filter_by,
    ) -> BaseORMModel:
        ...

    async def get_one_by_id(
        self,
        id_: int,
        *where,
        **filter_by,
    ) -> BaseORMModel:
        ...

    async def get_one_or_none(
        self,
        id_: int,
        *where,
        **filter_by,
    ) -> BaseORMModel | None:
        ...

    async def get_all(
        self,
        *where,
        **filter_by,
    ) -> list[BaseORMModel]:
        ...

    async def count(
        self,
        *where,
        **filter_by,
    ) -> int:
        ...
