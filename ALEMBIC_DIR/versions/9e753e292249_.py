"""empty message

Revision ID: 9e753e292249
Revises: 2b20ac4cf0da
Create Date: 2017-08-15 15:00:51.788927

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '9e753e292249'
down_revision = '2b20ac4cf0da'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('device', 'app_print_baudrate',
               existing_type=mysql.VARCHAR(length=32),
               nullable=True)
    op.alter_column('device', 'app_received_baudrate',
               existing_type=mysql.VARCHAR(length=32),
               nullable=True)
    op.alter_column('device', 'app_version',
               existing_type=mysql.VARCHAR(length=32),
               nullable=True)
    op.alter_column('device', 'capture_baudrate',
               existing_type=mysql.VARCHAR(length=32),
               nullable=True)
    op.alter_column('device', 'local_setting_version',
               existing_type=mysql.BIGINT(display_width=20),
               nullable=True)
    op.alter_column('device', 'newest_setting_version',
               existing_type=mysql.BIGINT(display_width=20),
               nullable=True)
    op.alter_column('device', 'newest_url',
               existing_type=mysql.VARCHAR(length=128),
               nullable=True)
    op.alter_column('device', 'problem',
               existing_type=mysql.TINYINT(display_width=1),
               nullable=True)
    op.alter_column('device', 'wifi_encrypt_type',
               existing_type=mysql.VARCHAR(length=32),
               nullable=True)
    op.alter_column('device', 'wifi_name',
               existing_type=mysql.VARCHAR(length=64),
               nullable=True)
    op.alter_column('device', 'wifi_password',
               existing_type=mysql.VARCHAR(length=64),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('device', 'wifi_password',
               existing_type=mysql.VARCHAR(length=64),
               nullable=False)
    op.alter_column('device', 'wifi_name',
               existing_type=mysql.VARCHAR(length=64),
               nullable=False)
    op.alter_column('device', 'wifi_encrypt_type',
               existing_type=mysql.VARCHAR(length=32),
               nullable=False)
    op.alter_column('device', 'problem',
               existing_type=mysql.TINYINT(display_width=1),
               nullable=False)
    op.alter_column('device', 'newest_url',
               existing_type=mysql.VARCHAR(length=128),
               nullable=False)
    op.alter_column('device', 'newest_setting_version',
               existing_type=mysql.BIGINT(display_width=20),
               nullable=False)
    op.alter_column('device', 'local_setting_version',
               existing_type=mysql.BIGINT(display_width=20),
               nullable=False)
    op.alter_column('device', 'capture_baudrate',
               existing_type=mysql.VARCHAR(length=32),
               nullable=False)
    op.alter_column('device', 'app_version',
               existing_type=mysql.VARCHAR(length=32),
               nullable=False)
    op.alter_column('device', 'app_received_baudrate',
               existing_type=mysql.VARCHAR(length=32),
               nullable=False)
    op.alter_column('device', 'app_print_baudrate',
               existing_type=mysql.VARCHAR(length=32),
               nullable=False)
    # ### end Alembic commands ###
