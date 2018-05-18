"""empty message

Revision ID: 30237035cfac
Revises: c9f25a08ac6d
Create Date: 2018-05-18 14:21:59.755628

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '30237035cfac'
down_revision = 'c9f25a08ac6d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('person', sa.Column('lazy_delete', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('person', 'lazy_delete')
    # ### end Alembic commands ###
