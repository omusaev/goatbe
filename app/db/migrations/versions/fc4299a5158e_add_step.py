"""add step

Revision ID: fc4299a5158e
Revises: 5ed1a6ff7e24
Create Date: 2016-03-20 00:56:57.029117

"""

# revision identifiers, used by Alembic.
revision = 'fc4299a5158e'
down_revision = '5ed1a6ff7e24'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('step',
    sa.Column('created_at', sa.DateTime(), server_default=sa.text(u"(now() at time zone 'utc')"), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text(u"(now() at time zone 'utc')"), nullable=True),
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('title', sa.String(length=255), server_default='', nullable=False),
    sa.Column('description', sa.Text(), server_default='', nullable=False),
    sa.Column('type', sa.String(length=255), server_default='COMMON', nullable=False),
    sa.Column('event_id', sa.BigInteger(), nullable=False),
    sa.Column('attributes', postgresql.JSON(), nullable=True),
    sa.ForeignKeyConstraint(['event_id'], [u'event.id'], name='step_event_id', ondelete='CASCADE', use_alter=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_foreign_key('step_event_id', 'step', 'event', ['event_id'], ['id'], ondelete='CASCADE', use_alter=True)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('step_event_id', 'step', type_='foreignkey')
    op.drop_table('step')
    ### end Alembic commands ###
