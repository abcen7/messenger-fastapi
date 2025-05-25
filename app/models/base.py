from datetime import UTC, datetime
from typing import Optional

from sqlalchemy import func
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column


class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        # TODO: change it to https://github.com/Netflix/dispatch/blob/master/src/dispatch/database/core.py#L51
        return f"{cls.__name__.lower()}"

    created_at: Mapped[Optional[datetime]] = mapped_column(
        server_default=func.now(),
        default=datetime.now(UTC),
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        server_default=func.now(),
        default=datetime.now(UTC),
        onupdate=func.now(),
    )
