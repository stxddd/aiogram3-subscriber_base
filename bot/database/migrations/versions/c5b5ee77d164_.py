"""empty message

Revision ID: c5b5ee77d164
Revises: 066a15d5f112
Create Date: 2025-02-03 19:00:35.477854

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c5b5ee77d164'
down_revision: Union[str, None] = '066a15d5f112'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tables', sa.Column('user_tg_id', sa.BigInteger(), nullable=True))
    op.drop_constraint('tables_owner_tg_id_fkey', 'tables', type_='foreignkey')
    op.create_foreign_key(None, 'tables', 'users', ['user_tg_id'], ['tg_id'], ondelete='CASCADE')
    op.drop_column('tables', 'owner_tg_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tables', sa.Column('owner_tg_id', sa.BIGINT(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'tables', type_='foreignkey')
    op.create_foreign_key('tables_owner_tg_id_fkey', 'tables', 'users', ['owner_tg_id'], ['tg_id'], ondelete='CASCADE')
    op.drop_column('tables', 'user_tg_id')
    # ### end Alembic commands ###
