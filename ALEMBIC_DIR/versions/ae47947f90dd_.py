"""empty message

Revision ID: ae47947f90dd
Revises: 6a884cfe782b
Create Date: 2017-07-10 14:13:13.839192

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ae47947f90dd'
down_revision = '6a884cfe782b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('comment',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('comment_id', sa.BigInteger(), nullable=False),
    sa.Column('article_id', sa.BigInteger(), nullable=False),
    sa.Column('commenter_id', sa.BigInteger(), nullable=True),
    sa.Column('text', sa.TEXT(), nullable=True),
    sa.Column('type', sa.Integer(), nullable=True),
    sa.Column('replied_user_id', sa.BigInteger(), nullable=True),
    sa.Column('replied_user_name', sa.String(length=64), nullable=True),
    sa.Column('replied_comment_id', sa.BigInteger(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_comment_article_id'), 'comment', ['article_id'], unique=False)
    op.create_index(op.f('ix_comment_comment_id'), 'comment', ['comment_id'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_comment_comment_id'), table_name='comment')
    op.drop_index(op.f('ix_comment_article_id'), table_name='comment')
    op.drop_table('comment')
    # ### end Alembic commands ###
