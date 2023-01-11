"""Creating report table

Revision ID: f1a20247b1de
Revises: 1a5cb014a78e
Create Date: 2022-06-27 06:55:13.426680

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "f1a20247b1de"
down_revision = "1a5cb014a78e"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "report",
        sa.Column("users_cnt", sa.Integer, nullable=False),
        sa.Column("us_users_cnt", sa.Integer, nullable=False),
        sa.Column("non_us_users_cnt", sa.Integer, nullable=False),
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
    conn = op.get_bind()
    conn.execute("INSERT INTO report (users_cnt, us_users_cnt, non_us_users_cnt) values (0, 0, 0)")


def downgrade():
    op.drop_table("report")
