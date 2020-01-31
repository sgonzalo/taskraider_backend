"""empty message

Revision ID: 788c93f93546
Revises: 00d9e204615b
Create Date: 2020-01-31 01:50:15.697096

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '788c93f93546'
down_revision = '00d9e204615b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('employer_profile',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('company_info', sa.String(length=250), nullable=False),
    sa.Column('employer_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['employer_id'], ['employer.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('company_info')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('employer_profile')
    # ### end Alembic commands ###
