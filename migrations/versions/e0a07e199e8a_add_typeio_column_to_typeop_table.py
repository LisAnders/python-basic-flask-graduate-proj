"""add typeio column to typeop table

Revision ID: e0a07e199e8a
Revises: 36b5fb78de87
Create Date: 2023-05-06 12:30:17.624918

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e0a07e199e8a'
down_revision = '36b5fb78de87'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('typeop', schema=None) as batch_op:
        batch_op.add_column(sa.Column('typeio', sa.Integer(), nullable=False))
        batch_op.create_unique_constraint(None, ['typeio'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('typeop', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_column('typeio')

    # ### end Alembic commands ###
