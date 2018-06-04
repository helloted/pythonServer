"""empty message

Revision ID: f06ae33421cb
Revises: 1df175fa1872
Create Date: 2018-05-17 19:45:55.435717

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f06ae33421cb'
down_revision = '1df175fa1872'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('scan_history',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('code', sa.VARBINARY(length=64), nullable=True),
    sa.Column('time', sa.BigInteger(), nullable=True),
    sa.Column('lng', sa.DECIMAL(precision=13, scale=10), nullable=True),
    sa.Column('lat', sa.DECIMAL(precision=13, scale=10), nullable=True),
    sa.Column('location', sa.String(length=256), nullable=True),
    sa.Column('merchant_id', sa.BigInteger(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('scan_history')
    # ### end Alembic commands ###