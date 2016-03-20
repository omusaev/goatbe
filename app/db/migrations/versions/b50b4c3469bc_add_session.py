"""add session

Revision ID: b50b4c3469bc
Revises: b90671508d1b
Create Date: 2016-03-20 00:46:01.142179

"""

# revision identifiers, used by Alembic.
revision = 'b50b4c3469bc'
down_revision = 'b90671508d1b'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('session',
    sa.Column('id', sa.String(length=32), nullable=False),
    sa.Column('data', sa.PickleType(), nullable=True),
    sa.Column('expire_at', sa.DateTime(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text(u"(now() at time zone 'utc')"), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text(u"(now() at time zone 'utc')"), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('session')
    ### end Alembic commands ###
