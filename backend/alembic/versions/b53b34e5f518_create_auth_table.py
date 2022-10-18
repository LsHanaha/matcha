"""create auth table.

Revision ID: b53b34e5f518
Revises:
Create Date: 2022-10-09 20:04:16.704259
"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "b53b34e5f518"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.BigInteger, primary_key=True),
        sa.Column("email", sa.String, unique=True),
        sa.Column("password", sa.String),
        sa.Column("is_active", sa.Boolean, default=False),
    )
    op.create_index("users_emails_idx", "users", ["email"])


def downgrade() -> None:
    op.drop_table("users")
