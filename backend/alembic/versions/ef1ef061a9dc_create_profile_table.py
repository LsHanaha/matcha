"""create profile table.

Revision ID: ef1ef061a9dc
Revises: 2fd1c5841f75
Create Date: 2022-10-18 22:33:09.268632
"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "ef1ef061a9dc"
down_revision = "2fd1c5841f75"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "profiles",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE")),
        sa.Column("first_name", sa.String, nullable=False),
        sa.Column("last_name", sa.String, nullable=False),
        sa.Column("birthday", sa.Date, nullable=False),
        sa.Column("gender", sa.SmallInteger, nullable=False),
        sa.Column("sexual_preferences", sa.SmallInteger, nullable=False),
        sa.Column("biography", sa.Text, nullable=True),
        sa.Column("main_photo", sa.String, nullable=False),
    )


def downgrade() -> None:
    op.drop_table("profiles")
