from typing import Awaitable, Protocol, runtime_checkable

from .generics_types import DTO, BaseORMModel


@runtime_checkable
class IWriteRepository(Protocol[BaseORMModel, DTO]):
    """
    Interface for create/update/delete operations
    """

    async def create(
        self,
        dto: DTO,
    ) -> BaseORMModel:
        ...

    async def update(
        self,
        id_: int,
        **values,
    ) -> BaseORMModel:
        ...

    async def delete(
        self,
        id_: int,
    ) -> None:
        ...

    async def create_many(
        self,
        dto_list: list[DTO],
    ) -> list[BaseORMModel]:
        ...
