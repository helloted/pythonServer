"""empty message

Revision ID: 6c7131d31405
Revises: 320664d19dfa
Create Date: 2017-11-13 18:54:33.703470

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6c7131d31405'
down_revision = '320664d19dfa'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('lottery',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('order_sn', sa.String(length=64), nullable=True),
    sa.Column('order_time', sa.BigInteger(), nullable=True),
    sa.Column('lottery_time', sa.BigInteger(), nullable=True),
    sa.Column('user_id', sa.BigInteger(), nullable=True),
    sa.Column('lottery_status', sa.Integer(), nullable=True),
    sa.Column('lottery_content', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_lottery_order_sn'), 'lottery', ['order_sn'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_lottery_order_sn'), table_name='lottery')
    op.drop_table('lottery')
    # ### end Alembic commands ###
