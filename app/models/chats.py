from enum import StrEnum
from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from .groups import Groups
    from .messages import Messages


class ChatType(StrEnum):
    PRIVATE = "private"
    GROUP = "group"


class Chats(Base):
    __tablename__ = "chats"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    type: Mapped[ChatType]
    groups: Mapped["Groups"] = relationship(
        back_populates="groups_details",
    )
    messages: Mapped[list["Messages"]] = relationship(
        "Messages",
        back_populates="chat",
        cascade="all, delete-orphan",
    )
