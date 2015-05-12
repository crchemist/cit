"""create tables

Revision ID: 3ad1cf34f2f0
Revises: 528a609600b3
Create Date: 2015-05-12 10:25:10.058400

"""

# revision identifiers, used by Alembic.
revision = '3ad1cf34f2f0'
down_revision = '528a609600b3'

from alembic import op
import sqlalchemy as sa


def upgrade():
    pass


def downgrade():
    op.drop_column('user', 'is_superuser')