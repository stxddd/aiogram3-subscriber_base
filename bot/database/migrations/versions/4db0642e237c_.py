"""empty message

Revision ID: 4db0642e237c
Revises: 033a5395b976
Create Date: 2025-02-24 14:57:43.386044

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4db0642e237c'
down_revision: Union[str, None] = '033a5395b976'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('connections', sa.Column('client_id', sa.Integer(), nullable=True))
    op.drop_constraint('connections_user_tg_id_fkey', 'connections', type_='foreignkey')
    op.create_foreign_key(None, 'connections', 'clients', ['client_id'], ['id'], ondelete='CASCADE')
    op.drop_column('connections', 'days_late')
    op.drop_column('connections', 'user_tg_id')
    op.drop_column('connections', 'tg_username')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('connections', sa.Column('tg_username', sa.VARCHAR(length=32), autoincrement=False, nullable=False))
    op.add_column('connections', sa.Column('user_tg_id', sa.BIGINT(), autoincrement=False, nullable=True))
    op.add_column('connections', sa.Column('days_late', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'connections', type_='foreignkey')
    op.create_foreign_key('connections_user_tg_id_fkey', 'connections', 'users', ['user_tg_id'], ['tg_id'], ondelete='CASCADE')
    op.drop_column('connections', 'client_id')
    # ### end Alembic commands ###
