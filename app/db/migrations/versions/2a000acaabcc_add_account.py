"""add account

Revision ID: 2a000acaabcc
Revises: b50b4c3469bc
Create Date: 2016-03-20 00:47:09.994806

"""

# revision identifiers, used by Alembic.
revision = '2a000acaabcc'
down_revision = 'b50b4c3469bc'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('account',
    sa.Column('created_at', sa.DateTime(), server_default=sa.text(u"(now() at time zone 'utc')"), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text(u"(now() at time zone 'utc')"), nullable=True),
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('name', sa.String(length=255), server_default='', nullable=False),
    sa.Column('status', sa.String(length=255), server_default='ACTIVE', nullable=False),
    sa.Column('avatar_url', sa.String(length=255), server_default='', nullable=False),
    sa.Column('auth_method', sa.String(length=255), nullable=False),
    sa.Column('identifier', sa.String(length=255), nullable=False),
    sa.Column('attributes', postgresql.JSON(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), server_default=sa.text(u'false'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('account')
    ### end Alembic commands ###
