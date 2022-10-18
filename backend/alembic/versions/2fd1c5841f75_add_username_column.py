"""add username column.

Revision ID: 2fd1c5841f75
Revises: b53b34e5f518
Create Date: 2022-10-18 22:15:38.184202
"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "2fd1c5841f75"
down_revision = "b53b34e5f518"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column("username", sa.String, unique=True),
    )


def downgrade() -> None:
    op.drop_column("users", "username")
