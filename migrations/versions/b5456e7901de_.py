"""empty message

Revision ID: b5456e7901de
Revises: 0b2c7dd30baf
Create Date: 2024-11-27 10:44:52.713447

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b5456e7901de'
down_revision = '0b2c7dd30baf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('referred_by', sa.String(length=80), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('referred_by')

    # ### end Alembic commands ###
