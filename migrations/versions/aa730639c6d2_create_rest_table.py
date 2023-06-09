"""create rest table

Revision ID: aa730639c6d2
Revises: 0d1eede17dab
Create Date: 2023-05-02 21:30:51.078268

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aa730639c6d2'
down_revision = '0d1eede17dab'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('rest',
    sa.Column('rest_id', sa.Integer(), nullable=False),
    sa.Column('id_ws', sa.Integer(), nullable=False),
    sa.Column('id_art', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('lastdate', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['id_art'], ['article.id_art'], name='fk_id_art'),
    sa.ForeignKeyConstraint(['id_ws'], ['warehouse.id_ws'], name='fk_id_ws'),
    sa.PrimaryKeyConstraint('rest_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('rest')
    # ### end Alembic commands ###
