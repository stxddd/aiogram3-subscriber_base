"""empty message

Revision ID: d6bfd8d3b86b
Revises: 96e0296fc1bb
Create Date: 2025-03-25 13:46:15.235404

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd6bfd8d3b86b'
down_revision: Union[str, None] = '96e0296fc1bb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('clients', 'username')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('clients', sa.Column('username', sa.VARCHAR(length=32), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
