"""Add course_link_image to Course

Revision ID: 19ef9e0b722f
Revises: 5df9420dc3d9
Create Date: 2024-01-29 19:18:27.942755

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '19ef9e0b722f'
down_revision = '5df9420dc3d9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    op.add_column('course', sa.Column('course_link_image', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('course', 'course_link_image')
    op.create_table('users',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('username', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
    sa.Column('name', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('email', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('phone', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('address', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('password_hash', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='users_pkey'),
    sa.UniqueConstraint('email', name='users_email_key'),
    sa.UniqueConstraint('phone', name='users_phone_key'),
    sa.UniqueConstraint('username', name='users_username_key')
    )
    # ### end Alembic commands ###
