"""Make recorded explictly TZ aware

Revision ID: 8ce29f341ed5
Revises: 691e64c5a637
Create Date: 2023-03-20 11:39:25.252235

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8ce29f341ed5'
down_revision = '691e64c5a637'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('measurements', schema=None) as batch_op:
        batch_op.alter_column('recorded', type_=sa.DateTime(timezone=True))


def downgrade():
    with op.batch_alter_table('measurements', schema=None) as batch_op:
        batch_op.alter_column('recorded', type_=sa.DateTime(timezone=False))
