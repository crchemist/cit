"""add column is_superuser to model

Revision ID: 4c28f392154d
Create Date: 2015-05-09 23:49:12.260119

"""

# revision identifiers, used by Alembic.
revision = '4c28f392154d'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('user', sa.Column('is_superuser', sa.Boolean))


def downgrade():
    op.drop_column('user', 'is_superuser')
