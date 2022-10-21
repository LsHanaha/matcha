"""create gps table.

Revision ID: c6b86fe5e283
Revises: c6f184cfcfdb
Create Date: 2022-10-21 22:46:19.660711
"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "c6b86fe5e283"
down_revision = "c6f184cfcfdb"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "gps",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE")),
        sa.Column("ip_addr", sa.String, nullable=False),
        sa.Column("country", sa.String, nullable=False),
        sa.Column("region", sa.String, nullable=True),
        sa.Column("city", sa.String, nullable=False),
        sa.Column("lat", sa.Float, nullable=False),
        sa.Column("lng", sa.Float, nullable=False),
        sa.Column("tz", sa.String, nullable=True),
    )


def downgrade() -> None:
    op.drop_table("gps")
