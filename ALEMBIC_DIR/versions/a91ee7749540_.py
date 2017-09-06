"""empty message

Revision ID: a91ee7749540
Revises: e2672a6f3435
Create Date: 2017-09-04 15:12:51.620819

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a91ee7749540'
down_revision = 'e2672a6f3435'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('device', sa.Column('cut_cmds', sa.JSON(), nullable=True))
    op.add_column('device', sa.Column('justification', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('device', 'justification')
    op.drop_column('device', 'cut_cmds')
    # ### end Alembic commands ###
