from datetime import UTC, datetime
from typing import TYPE_CHECKING

from sqlalchemy import TIMESTAMP, ForeignKey, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .chats import Chats
    from .users import Users


class Messages(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.id"))
    sender_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    text: Mapped[str] = mapped_column(Text)
    read_at: Mapped[datetime | None] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=None,
        default=None,
        onupdate=func.now(),
    )

    chat: Mapped["Chats"] = relationship("Chats", back_populates="messages")
    sender: Mapped["Users"] = relationship("Users", back_populates="messages_sent")
