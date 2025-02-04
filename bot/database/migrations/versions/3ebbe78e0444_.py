"""empty message

Revision ID: 3ebbe78e0444
Revises: c5b5ee77d164
Create Date: 2025-02-04 15:46:36.019819

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3ebbe78e0444'
down_revision: Union[str, None] = 'c5b5ee77d164'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('downloads_today', sa.Integer(), nullable=True))
    op.add_column('users', sa.Column('last_download_date', sa.Date(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'last_download_date')
    op.drop_column('users', 'downloads_today')
    # ### end Alembic commands ###
