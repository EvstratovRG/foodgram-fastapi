"""token

Revision ID: 6c0066f28078
Revises: 6c80dad5ce6e
Create Date: 2023-12-01 16:07:21.955629

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa



# revision identifiers, used by Alembic.
revision: str = '6c0066f28078'
down_revision: Union[str, None] = '6c80dad5ce6e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('token', sa.String(length=250), nullable=True))
    op.add_column('user', sa.Column('is_authenticated', sa.Boolean(), nullable=False, server_default='false'))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'is_authenticated')
    op.drop_column('user', 'token')
    # ### end Alembic commands ###