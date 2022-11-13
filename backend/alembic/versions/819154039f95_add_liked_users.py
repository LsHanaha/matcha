"""add liked users.

Revision ID: 819154039f95
Revises: a0cce1ecf2b8
Create Date: 2022-11-13 22:35:31.052547
"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "819154039f95"
down_revision = "a0cce1ecf2b8"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "matches",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column(
            "first_user_id", sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE")
        ),
        sa.Column(
            "second_user_id", sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE")
        ),
    )
    op.create_unique_constraint(
        "uc_users_pair_matches", "matches", ["first_user_id", "second_user_id"]
    )


def downgrade() -> None:
    op.drop_table("matches")
