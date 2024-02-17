"""password

Revision ID: ef6db5e7d547
Revises: 90eefc0e8883
Create Date: 2023-11-28 10:50:16.624326

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'ef6db5e7d547'
down_revision: Union[str, None] = '90eefc0e8883'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'hashed_password',
               existing_type=sa.VARCHAR(length=1024),
               type_=sa.String(length=150),
               existing_nullable=False)
    op.drop_column('user', 'password')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('password', sa.VARCHAR(length=150), autoincrement=False, nullable=False))
    op.alter_column('user', 'hashed_password',
               existing_type=sa.String(length=150),
               type_=sa.VARCHAR(length=1024),
               existing_nullable=False)
    # ### end Alembic commands ###
