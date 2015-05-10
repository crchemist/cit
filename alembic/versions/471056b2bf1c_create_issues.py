"""Create Issues

Revision ID: 471056b2bf1c
Revises: None
Create Date: 2015-05-10 04:30:05.090048

"""

# revision identifiers, used by Alembic.
revision = '471056b2bf1c'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'issues',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('reporter', sa.Integer, (sa.ForeignKey("user.id"))),
        sa.Column('description', sa.String(120)),
        sa.Column('coordinates', sa.String(120)),
    )

def downgrade():
    op.drop_table('issues')