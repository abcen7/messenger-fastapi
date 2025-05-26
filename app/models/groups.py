from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.chats import Chats, ChatType

if TYPE_CHECKING:
    from app.models import GroupUserAssociation, Users


class Groups(Chats):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(ForeignKey("chats.id"), primary_key=True)
    creator_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    chat: Mapped["Chats"] = relationship(back_populates="groups")
    creator: Mapped["Users"] = relationship(back_populates="groups_created")

    __mapper_args__ = {
        "polymorphic_identity": ChatType.GROUP,
    }
    # association between Parent -> Association -> Child
    user_details: Mapped[list["GroupUserAssociation"]] = relationship(
        back_populates="group",
    )
