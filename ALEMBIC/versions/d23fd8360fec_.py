"""empty message

Revision ID: d23fd8360fec
Revises: f06ae33421cb
Create Date: 2018-05-22 15:52:55.757128

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd23fd8360fec'
down_revision = 'f06ae33421cb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('product_info', sa.Column('time', sa.BigInteger(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('product_info', 'time')
    # ### end Alembic commands ###
