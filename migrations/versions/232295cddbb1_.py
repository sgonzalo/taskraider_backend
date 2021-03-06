"""empty message

Revision ID: 232295cddbb1
Revises: 7be72339c0e4
Create Date: 2020-02-13 02:33:06.243576

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '232295cddbb1'
down_revision = '7be72339c0e4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('password', table_name='company')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('password', 'company', ['password'], unique=True)
    # ### end Alembic commands ###
