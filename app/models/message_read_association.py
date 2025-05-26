from datetime import UTC, datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models import Messages
    from app.models.users import Users


class MessagesRead(Base):
    __tablename__ = "messages_read"

    message_id: Mapped[int] = mapped_column(ForeignKey("messages.id"), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    read_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        default=datetime.now(UTC),
        onupdate=func.now(),
    )

    messages: Mapped["Messages"] = relationship(back_populates="reads")
    user: Mapped["Users"] = relationship(back_populates="messages_read")
