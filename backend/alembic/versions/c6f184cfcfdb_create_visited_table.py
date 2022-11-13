"""create visited table.

Revision ID: c6f184cfcfdb
Revises: ef1ef061a9dc
Create Date: 2022-10-19 22:46:22.903096
"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "c6f184cfcfdb"
down_revision = "ef1ef061a9dc"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "visits",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE")),
        sa.Column(
            "target_user_id", sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE")
        ),
        sa.Column("last_visit_time", sa.DateTime, onupdate=sa.func.current_timestamp()),
        sa.Column("is_liked", sa.Boolean, default=False),
        sa.Column("is_blocked", sa.Boolean, default=False),
        sa.Column("is_reported", sa.Boolean, default=False),
    )
    op.create_unique_constraint(
        "uc_users_pair_visits", "visits", ["user_id", "target_user_id"]
    )


def downgrade() -> None:
    op.drop_table("visits")
