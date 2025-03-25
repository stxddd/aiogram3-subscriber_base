"""empty message

Revision ID: 96e0296fc1bb
Revises: 9fae17c95cc6
Create Date: 2025-03-25 12:41:17.089320

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '96e0296fc1bb'
down_revision: Union[str, None] = '9fae17c95cc6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('servers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=32), nullable=False),
    sa.Column('port', sa.Integer(), nullable=False),
    sa.Column('count_of_clients', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('connections', sa.Column('server_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'connections', 'servers', ['server_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'connections', type_='foreignkey')
    op.drop_column('connections', 'server_id')
    op.drop_table('servers')
    # ### end Alembic commands ###
