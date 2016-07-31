"""add event uuid

Revision ID: 1fbd2d51357f
Revises: 570e23cbd079
Create Date: 2016-04-24 22:12:49.547546

"""

# revision identifiers, used by Alembic.
revision = '1fbd2d51357f'
down_revision = '570e23cbd079'

from alembic import op
import sqlalchemy as sa
import uuid


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('event', sa.Column('secret', sa.String(length=32), nullable=True))

    connection = op.get_bind()
    events = connection.execute('select id from event')
    for event in events:
        op.execute("UPDATE event SET secret = '%s' WHERE id = %s" % (uuid.uuid4().hex, event[0]))

    op.alter_column('event', 'secret',
               existing_type=sa.VARCHAR(length=32),
               nullable=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('event', 'secret')
    ### end Alembic commands ###