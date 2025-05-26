from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .chats import Chats
    from .message_read_association import MessagesRead
    from .users import Users


class Messages(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.id"))
    sender_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    text: Mapped[str] = mapped_column(Text)

    chat: Mapped["Chats"] = relationship("Chats", back_populates="messages")
    sender: Mapped["Users"] = relationship("Users", back_populates="messages")
    reads: Mapped[list["MessagesRead"]] = relationship(
        back_populates="messages",
        cascade="all, delete-orphan",
    )
