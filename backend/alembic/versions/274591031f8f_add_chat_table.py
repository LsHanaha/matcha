"""add chat table.

Revision ID: 274591031f8f
Revises: 64a73dc33bc7
Create Date: 2023-01-07 19:20:27.294578
"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "274591031f8f"
down_revision = "64a73dc33bc7"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "chat_messages",
        sa.Column("id", sa.BigInteger, primary_key=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE")),
        sa.Column(
            "target_user_id", sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE")
        ),
        sa.Column(
            "message_time",
            sa.DateTime,
            server_default=sa.text("now()"),
            server_onupdate=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("message", sa.String, nullable=False),
        sa.Column(
            "is_read",
            sa.Boolean,
            server_default=sa.schema.DefaultClause("0"),
            nullable=False,
        ),
    )

    op.create_unique_constraint(
        "uc_users_pair_chat", "chat_messages", ["user_id", "target_user_id"]
    )


def downgrade() -> None:
    op.drop_table("chat_messages")
