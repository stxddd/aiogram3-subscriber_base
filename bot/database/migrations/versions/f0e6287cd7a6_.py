"""empty message

Revision ID: f0e6287cd7a6
Revises: cb0739f1ce23
Create Date: 2025-02-03 18:56:39.624726

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f0e6287cd7a6'
down_revision: Union[str, None] = 'cb0739f1ce23'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('lines', sa.Column('client_name', sa.String(length=32), nullable=False))
    op.add_column('lines', sa.Column('client_price', sa.Integer(), nullable=False))
    op.add_column('lines', sa.Column('client_date_from', sa.String(length=20), nullable=False))
    op.add_column('lines', sa.Column('client_date_to', sa.String(length=20), nullable=False))
    op.drop_column('lines', 'clinet_name')
    op.drop_column('lines', 'clinet_date_from')
    op.drop_column('lines', 'clinet_date_to')
    op.drop_column('lines', 'clinet_price')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('lines', sa.Column('clinet_price', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('lines', sa.Column('clinet_date_to', sa.VARCHAR(length=20), autoincrement=False, nullable=False))
    op.add_column('lines', sa.Column('clinet_date_from', sa.VARCHAR(length=20), autoincrement=False, nullable=False))
    op.add_column('lines', sa.Column('clinet_name', sa.VARCHAR(length=32), autoincrement=False, nullable=False))
    op.drop_column('lines', 'client_date_to')
    op.drop_column('lines', 'client_date_from')
    op.drop_column('lines', 'client_price')
    op.drop_column('lines', 'client_name')
    # ### end Alembic commands ###
