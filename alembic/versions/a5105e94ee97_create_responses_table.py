"""create responses table

Revision ID: a5105e94ee97
Revises: 
Create Date: 2017-06-21 15:10:48.536634

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a5105e94ee97'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'responses',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('trigger', sa.String, unique=True),
        sa.Column('response', sa.String),
    )


def downgrade():
    op.drop_table('responses')
