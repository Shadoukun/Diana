"""added reactions table

Revision ID: 65ae994d029d
Revises: a5105e94ee97
Create Date: 2017-06-23 20:15:26.034113

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '65ae994d029d'
down_revision = 'a5105e94ee97'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('reactions', 'reaction',
               existing_type=sa.TEXT(),
               nullable=True)
    op.alter_column('reactions', 'trigger',
               existing_type=sa.TEXT(),
               nullable=True)
    op.create_unique_constraint(None, 'reactions', ['trigger'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'reactions', type_='unique')
    op.alter_column('reactions', 'trigger',
               existing_type=sa.TEXT(),
               nullable=False)
    op.alter_column('reactions', 'reaction',
               existing_type=sa.TEXT(),
               nullable=False)
    # ### end Alembic commands ###
