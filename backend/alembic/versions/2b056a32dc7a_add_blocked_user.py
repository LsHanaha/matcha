"""add blocked user.

Revision ID: 2b056a32dc7a
Revises: a0cce1ecf2b8
Create Date: 2022-11-13 11:41:05.873304
"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "2b056a32dc7a"
down_revision = "a0cce1ecf2b8"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "blocked_users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column(
            "user_id",
            sa.Integer,
            sa.ForeignKey("users.id", ondelete="CASCADE"),
        ),
        sa.Column(
            "target_user_id",
            sa.Integer,
            sa.ForeignKey("users.id", ondelete="CASCADE"),
        ),
        sa.Column("reported", sa.Boolean, nullable=True),
    )
    op.create_unique_constraint(
        "uc_blocked_users_pairs", "blocked_users", ["user_id", "target_user_id"]
    )


def downgrade() -> None:
    op.drop_table("blocked_users")
