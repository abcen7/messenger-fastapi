# from typing import TYPE_CHECKING
#
# from sqlalchemy import ForeignKey, UniqueConstraint
# from sqlalchemy.orm import Mapped, mapped_column, relationship
#
# from .base import Base
#
# if TYPE_CHECKING:
#     from .groups import Groups
#     from .users import Users
#
#
# class GroupUserAssociation(Base):
#     __tablename__ = "group_user_association"
#     __table_args__ = (
#         UniqueConstraint(
#             "group_id",
#             "user_id",
#             name="idx_unique_group_user",
#         ),
#     )
#
#     id: Mapped[int] = mapped_column(primary_key=True)
#     group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"))
#     user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
#
#     # association between Association -> User
#     user: Mapped["Users"] = relationship(
#         back_populates="group_details",
#     )
#     # association between Association -> Group
#     group: Mapped["Groups"] = relationship(
#         back_populates="user_details",
#     )
