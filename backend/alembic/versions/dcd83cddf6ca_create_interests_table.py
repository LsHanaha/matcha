"""create interests table.

Revision ID: dcd83cddf6ca
Revises: c6b86fe5e283
Create Date: 2022-10-21 23:15:01.804084
"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "dcd83cddf6ca"
down_revision = "c6b86fe5e283"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "interests",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.Text, nullable=False, unique=True),
    )


def downgrade() -> None:
    op.drop_table("interests")
