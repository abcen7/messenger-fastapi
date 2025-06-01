from typing_extensions import Protocol, runtime_checkable

from .generics_types import DTO, BaseORMModel
from .read_repository import IReadRepository
from .write_repository import IWriteRepository


@runtime_checkable
class IRepository(
    IReadRepository[BaseORMModel],
    IWriteRepository[BaseORMModel, DTO],
    Protocol[BaseORMModel, DTO],
):
    """
    Full interface of repository for read/write operations
    """

    pass
