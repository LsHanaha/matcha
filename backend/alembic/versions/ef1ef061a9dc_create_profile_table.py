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
        sa.Column(
            "user_id",
            sa.Integer,
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            unique=True,
        ),
        sa.Column("first_name", sa.String, nullable=False),
        sa.Column("last_name", sa.String, nullable=False),
        sa.Column("birthday", sa.Date, nullable=False),
        sa.Column("gender", sa.SmallInteger, nullable=False),
        sa.Column("sexual_orientation", sa.SmallInteger, nullable=False, default=0),
        sa.Column("biography", sa.Text, nullable=True),
        sa.Column("main_photo_name", sa.String, nullable=False),
        sa.Column("fame_rating", sa.Integer, default=0),
        sa.Column("last_online", sa.DateTime, nullable=True),
        sa.Column("interests", sa.ARRAY(sa.Integer, dimensions=2), nullable=True),
        sa.Column("city", sa.String, nullable=False),
    )
    op.create_check_constraint("ch_profiles_fame_rating", "profiles", "fame_rating>=0")


def downgrade() -> None:
    op.drop_table("profiles")
