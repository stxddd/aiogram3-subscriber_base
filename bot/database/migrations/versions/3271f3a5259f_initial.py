"""Initial

Revision ID: 3271f3a5259f
Revises: 
Create Date: 2025-01-28 18:03:48.140366

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "3271f3a5259f"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "tables",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("owner_tg_id", sa.BigInteger(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("tg_id", sa.BigInteger(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "lines",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("owner_tg_id", sa.BigInteger(), nullable=False),
        sa.Column("table_id", sa.Integer(), nullable=True),
        sa.Column("subscriber_tg_id", sa.String(), nullable=False),
        sa.Column("subscriber_price", sa.Integer(), nullable=False),
        sa.Column("subscriber_date", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(
            ["table_id"],
            ["tables.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("lines")
    op.drop_table("users")
    op.drop_table("tables")
    # ### end Alembic commands ###
