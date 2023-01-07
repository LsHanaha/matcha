"""add system notifications.

Revision ID: 64a73dc33bc7
Revises: 819154039f95
Create Date: 2023-01-06 22:29:36.219636
"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "64a73dc33bc7"
down_revision = "819154039f95"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "system_events",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE")),
        sa.Column(
            "target_user_id", sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE")
        ),
        sa.Column("event_type", sa.Integer, nullable=False),
        sa.Column(
            "event_time",
            sa.DateTime,
            server_default=sa.text("now()"),
            server_onupdate=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("is_read", sa.Boolean, default=False, nullable=False),
    )

    op.create_unique_constraint(
        "uc_users_pair_system", "system_events", ["user_id", "target_user_id"]
    )


def downgrade() -> None:
    op.drop_table("system_events")
