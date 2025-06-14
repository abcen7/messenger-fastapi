"""added deleted at

Revision ID: ce8280e99fa0
Revises: 790cdd64bae7
Create Date: 2025-05-31 14:03:06.532402

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "ce8280e99fa0"
down_revision: Union[str, None] = "790cdd64bae7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "chat_members",
        sa.Column(
            "deleted_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
    )
    op.add_column(
        "chats",
        sa.Column(
            "deleted_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
    )
    op.add_column(
        "messages",
        sa.Column(
            "deleted_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
    )
    op.add_column(
        "users",
        sa.Column(
            "deleted_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("users", "deleted_at")
    op.drop_column("messages", "deleted_at")
    op.drop_column("chats", "deleted_at")
    op.drop_column("chat_members", "deleted_at")
    # ### end Alembic commands ###
