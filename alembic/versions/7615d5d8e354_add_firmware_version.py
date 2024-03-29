"""Add firmware version

Revision ID: 7615d5d8e354
Revises: cd509524593e
Create Date: 2022-03-02 19:51:17.188416

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7615d5d8e354'
down_revision = 'cd509524593e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('measurements', sa.Column('version', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('measurements', 'version')
    # ### end Alembic commands ###
