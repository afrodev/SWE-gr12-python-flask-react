"""empty message

Revision ID: 653cde7a6438
Revises: 4b47661a03d9
Create Date: 2023-11-22 19:32:01.894521

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '653cde7a6438'
down_revision = '4b47661a03d9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('image_url')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('image_url', sa.VARCHAR(length=500), nullable=True))

    # ### end Alembic commands ###
