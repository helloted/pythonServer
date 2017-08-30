"""empty message

Revision ID: e0fdb6d0d20a
Revises: f160dc039a48
Create Date: 2017-08-29 14:07:20.243463

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e0fdb6d0d20a'
down_revision = 'f160dc039a48'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('events_history',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('time', sa.BigInteger(), nullable=True),
    sa.Column('store_id', sa.BigInteger(), nullable=True),
    sa.Column('store_name', sa.String(length=50), nullable=True),
    sa.Column('type', sa.Integer(), nullable=True),
    sa.Column('device_sn', sa.String(length=32), nullable=True),
    sa.Column('start_time', sa.BigInteger(), nullable=True),
    sa.Column('end_time', sa.BigInteger(), nullable=True),
    sa.Column('time_between', sa.Integer(), nullable=True),
    sa.Column('value', sa.Integer(), nullable=True),
    sa.Column('float_value', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('fluctuates_histroy',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('time', sa.BigInteger(), nullable=True),
    sa.Column('store_id', sa.BigInteger(), nullable=True),
    sa.Column('store_name', sa.String(length=50), nullable=True),
    sa.Column('type', sa.Integer(), nullable=True),
    sa.Column('value', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('store_daily',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('time', sa.BigInteger(), nullable=True),
    sa.Column('datetime', sa.DateTime(), nullable=True),
    sa.Column('store_id', sa.BigInteger(), nullable=True),
    sa.Column('store_name', sa.String(length=64), nullable=True),
    sa.Column('total_price', sa.Integer(), nullable=True),
    sa.Column('total_tax', sa.Integer(), nullable=True),
    sa.Column('total_count', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_store_daily_time'), 'store_daily', ['time'], unique=False)
    op.add_column(u'deal', sa.Column('store_name', sa.String(length=64), nullable=True))
    op.add_column(u'offline_histroy', sa.Column('time_between', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column(u'offline_histroy', 'time_between')
    op.drop_column(u'deal', 'store_name')
    op.drop_index(op.f('ix_store_daily_time'), table_name='store_daily')
    op.drop_table('store_daily')
    op.drop_table('fluctuates_histroy')
    op.drop_table('events_history')
    # ### end Alembic commands ###