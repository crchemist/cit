"""Added Issues table

Revision ID: 4c28f392154d
Revises: 2d876fb4ab3a
Create Date: 2015-05-10 04:07:37.629446

"""

# revision identifiers, used by Alembic.
revision = '4c28f392154d'
down_revision = '2d876fb4ab3a'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('issues',
    sa.Column('id', sa.INTEGER(), server_default="nextval('issues_id_seq'::regclass)", nullable=False),
    sa.Column('reporter', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('description', sa.VARCHAR(length=120), autoincrement=False, nullable=True),
    sa.Column('coordinates', sa.NullType(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['reporter'], [u'user.id'], name=u'issues_reporter_fkey'),
    sa.PrimaryKeyConstraint('id', name=u'issues_pkey')
    )

def downgrade():
    op.drop_table('issues')
