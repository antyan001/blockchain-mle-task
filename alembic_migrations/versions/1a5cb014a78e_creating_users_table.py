"""Creating users table

Revision ID: 1a5cb014a78e
Revises: 
Create Date: 2022-06-25 21:00:17.741726

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "1a5cb014a78e"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("city", sa.String(length=250), nullable=False),
        sa.Column("state", sa.String(length=250), nullable=True),
        sa.Column("country", sa.String(length=250), nullable=False),
        sa.Column("postcode", sa.String(length=32), nullable=False),
        sa.Column(
            "created_date",
            sa.DateTime(),
            server_default=sa.text("TIMEZONE('utc', CURRENT_TIMESTAMP)"),
            nullable=False,
        ),
        sa.Column(
            "updated_date",
            sa.DateTime(),
            server_default=sa.text("TIMEZONE('utc', CURRENT_TIMESTAMP)"),
            nullable=False,
        ),
    )


def downgrade():
    op.drop_table("users")
