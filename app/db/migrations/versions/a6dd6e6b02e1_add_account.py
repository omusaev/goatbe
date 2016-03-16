"""add_account

Revision ID: a6dd6e6b02e1
Revises: 8e3898afc0d8
Create Date: 2016-03-10 16:06:32.854839

"""

# revision identifiers, used by Alembic.
revision = 'a6dd6e6b02e1'
down_revision = '8e3898afc0d8'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('account',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('status', sa.Enum('active', 'inactive', name='account_status'), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('auth_method', sa.Enum('FB', 'ANONYM', name='account_auth_method'), nullable=False),
    sa.Column('identifier', sa.String(length=255), nullable=False),
    sa.Column('attributes', postgresql.JSON(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('account')
    op.execute("DROP TYPE account_auth_method")
    op.execute("DROP TYPE account_status")
    ### end Alembic commands ###