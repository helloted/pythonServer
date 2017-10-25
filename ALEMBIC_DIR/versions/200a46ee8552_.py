"""empty message

Revision ID: 200a46ee8552
Revises: 4e7c54670fb8
Create Date: 2017-10-24 15:23:11.458526

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '200a46ee8552'
down_revision = '4e7c54670fb8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('deal_status', sa.Column('handle_time', sa.BigInteger(), nullable=True))
    op.add_column('deal_status', sa.Column('status', sa.Integer(), nullable=True))
    op.drop_column('deal_status', 'deal_status')
    op.drop_column('deal_status', 'convert_time')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('deal_status', sa.Column('convert_time', mysql.BIGINT(display_width=20), autoincrement=False, nullable=True))
    op.add_column('deal_status', sa.Column('deal_status', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.drop_column('deal_status', 'status')
    op.drop_column('deal_status', 'handle_time')
    # ### end Alembic commands ###