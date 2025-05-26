from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models import Groups, GroupUserAssociation, Messages, MessagesRead


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    full_name: Mapped[str] = mapped_column(String(255))
    hashed_password: Mapped[str] = mapped_column(String(255))

    groups_created: Mapped[list["Groups"]] = relationship(
        back_populates="creator", cascade="all, delete-orphan"
    )
    messages_sent: Mapped[list["Messages"]] = relationship(
        back_populates="sender", cascade="all, delete-orphan"
    )
    messages_read: Mapped[list["MessagesRead"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    # group_details: Mapped[list["GroupUserAssociation"]] = relationship(
    #     back_populates="user",
    # )
