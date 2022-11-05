"""create preference table.

Revision ID: a0cce1ecf2b8
Revises: dcd83cddf6ca
Create Date: 2022-11-01 16:48:40.422679
"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "a0cce1ecf2b8"
down_revision = "dcd83cddf6ca"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "preferences",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column(
            "user_id",
            sa.Integer,
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            unique=True,
        ),
        sa.Column("sexual_preference", sa.SmallInteger, nullable=False, default=0),
        sa.Column("min_fame_rating", sa.Integer, nullable=False, default=0),
        sa.Column("min_age", sa.Integer, nullable=False, default=18),
        sa.Column("max_age", sa.Integer, nullable=False, default=99),
        sa.Column("max_distance_km", sa.Integer, nullable=False, default=100),
    )


def downgrade() -> None:
    op.drop_table("preferences")
