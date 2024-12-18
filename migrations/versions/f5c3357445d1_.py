"""empty message

Revision ID: f5c3357445d1
Revises: bc1837ae22a6
Create Date: 2024-12-15 10:11:05.169090

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f5c3357445d1'
down_revision = 'bc1837ae22a6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('pin',
               existing_type=sa.VARCHAR(length=4),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('pin',
               existing_type=sa.VARCHAR(length=4),
               nullable=True)

    # ### end Alembic commands ###
