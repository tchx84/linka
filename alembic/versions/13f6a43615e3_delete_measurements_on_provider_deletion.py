"""Delete measurements on provider deletion

Revision ID: 13f6a43615e3
Revises: 8ce29f341ed5
Create Date: 2023-03-21 09:36:14.098851

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '13f6a43615e3'
down_revision = '8ce29f341ed5'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('measurements', schema=None) as batch_op:
        batch_op.drop_constraint('fk_measurement_provider', type_='foreignkey')
        batch_op.create_foreign_key('fk_measurement_provider', 'providers', ['provider_id'], ['id'], ondelete='CASCADE')


def downgrade():
    with op.batch_alter_table('measurements', schema=None) as batch_op:
        batch_op.drop_constraint('fk_measurement_provider', type_='foreignkey')
        batch_op.create_foreign_key('fk_measurement_provider', 'providers', ['provider_id'], ['id'])
