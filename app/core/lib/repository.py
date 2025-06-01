from typing import Generic, TypeVar, get_args

from pydantic import BaseModel
from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import with_async_session
from app.models.base import Base

SAModel = TypeVar("SAModel")


class BaseRepository(Generic[SAModel]):
    model: Base

    @with_async_session
    def __init__(self, session: AsyncSession):
        self.session = session

    def __init_subclass__(cls):
        cls.model = get_args(cls.__orig_bases__[0])[0]

    async def get_one(
        self,
        id_: int,
        *where,
        **filter_by,
    ) -> SAModel | None:
        return await self.get_one_or_none(id_, *where, **filter_by)

    async def get_one_or_none(
        self,
        id_: int,
        *where,
        **filter_by,
    ) -> SAModel | None:
        return await self.session.scalar(
            select(self.model)
            .filter_by(
                id=id_,
                deleted_at=None,
                **filter_by,
            )
            .where(*where),
        )

    # async def pagination_select(
    #     self,
    #     dto: Params,
    #     *where,
    #     **filter_by,
    # ) -> tuple[list[T], int]:
    #     instance_set = await self.session.scalars(
    #         select(self.model)
    #         .where(*where)
    #         .filter_by(
    #             deleted_at=None,
    #             **filter_by,
    #         )
    #         .limit(dto.limit)
    #         .offset(dto.offset),
    #     )
    #     return instance_set.unique().all(), await self.count(*where)

    async def select_all(self, *where, **filter_by) -> list[SAModel]:
        instance_set = await self.session.scalars(
            select(self.model).filter_by(deleted_at=None, **filter_by).where(*where),
        )
        return instance_set.unique().all()

    async def create(self, dto: BaseModel) -> SAModel:
        instance = self.model(**dto.model_dump())
        self.session.add(instance)
        await self.session.commit()

        return instance

    async def create_many(self, dto_set: list[BaseModel]) -> list[SAModel]:
        instance_set = [self.model(**dto.model_dump()) for dto in dto_set]
        self.session.add_all(instance_set)
        await self.session.commit()

        return instance_set

    async def update(self, id_: int, **values) -> SAModel:
        await self.session.execute(
            update(self.model).filter_by(id=id_).values(**values),
        )
        await self.session.commit()

        return await self.get_one(id_)

    async def delete(self, id_: int) -> None:
        await self.session.execute(
            update(self.model).filter_by(id=id_).values(deleted_at=func.now()),
        )
        await self.session.commit()

    async def count(self, *where, **filter_by) -> int:
        return await self.session.scalar(
            select(func.count(self.model.id))
            .filter_by(
                **filter_by,
                deleted_at=None,
            )
            .where(*where),
        )
