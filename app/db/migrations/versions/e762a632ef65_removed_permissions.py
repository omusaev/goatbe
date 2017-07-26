"""removed permissions

Revision ID: e762a632ef65
Revises: 79864fcb4544
Create Date: 2017-07-26 12:50:28.324803

"""

# revision identifiers, used by Alembic.
revision = 'e762a632ef65'
down_revision = '79864fcb4544'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    op.drop_column('participant', 'permissions')


def downgrade():
    op.add_column('participant', sa.Column('permissions', postgresql.JSON(), autoincrement=False, nullable=True))

