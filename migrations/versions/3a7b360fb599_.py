"""empty message

Revision ID: 3a7b360fb599
Revises: 
Create Date: 2019-04-28 22:06:20.361030

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3a7b360fb599'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('ingredient', 'ingredient_type')
    op.drop_column('ingredient', 'ingredient_quantity')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ingredient', sa.Column('ingredient_quantity', sa.VARCHAR(length=50), autoincrement=False, nullable=True))
    op.add_column('ingredient', sa.Column('ingredient_type', sa.VARCHAR(length=50), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
