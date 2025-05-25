from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models import Users
    from app.models.group_user_association import GroupUserAssociation


class Groups(Base):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(ForeignKey("chats.id"), primary_key=True)
    title: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    creator_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    creator: Mapped["Users"] = relationship(back_populates="groups")
    users: Mapped[list["Users"]] = relationship(
        secondary="group_user_association",
        back_populates="groups",
    )
    # association between Parent -> Association -> Child
    users_details: Mapped[list["GroupUserAssociation"]] = relationship(
        back_populates="groups",
    )
