"""empty message

Revision ID: 4331c2d45daf
Revises: 8a8d02c12409
Create Date: 2020-10-23 15:46:37.993785

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4331c2d45daf'
down_revision = '8a8d02c12409'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('api_keys',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('source', sa.String(), nullable=False),
    sa.Column('api_key_hash', sa.String(length=65), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('api_keys')
    # ### end Alembic commands ###
