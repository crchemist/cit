"""add table issues

Revision ID: 1a391246b1e5
Revises: 2d876fb4ab3a
Create Date: 2015-05-12 11:18:03.172057

"""

# revision identifiers, used by Alembic.
revision = '1a391246b1e5'
down_revision = '2d876fb4ab3a'


from alembic import op
import sqlalchemy as sa
from geoalchemy2 import Geography


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'issue',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('reporter', sa.Integer, sa.ForeignKey("user.id")),
        sa.Column('description', sa.String(120), nullable=False),
        sa.Column('coordinates', Geography(geometry_type='GEOMETRY'))
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    pass
    ### end Alembic commands ###