"""empty message

Revision ID: 5161ddeb2b59
Revises: 783e1f7555bd
Create Date: 2024-11-27 14:17:27.438911

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5161ddeb2b59'
down_revision = '783e1f7555bd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('otp')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('otp', sa.VARCHAR(length=5), nullable=True))

    # ### end Alembic commands ###