"""add column is_superuser to model
Revision ID: 2d876fb4ab3a
Revises: 53c52e7884df
Create Date: 2015-05-09 23:49:12.260119
"""

# revision identifiers, used by Alembic.
revision = '2d876fb4ab3a'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('user', sa.Column('is_superuser', sa.Boolean))


def downgrade():
    op.drop_column('user', 'is_superuser')