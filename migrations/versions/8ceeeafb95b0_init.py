"""init

Revision ID: 8ceeeafb95b0
Revises: 
Create Date: 2022-07-20 11:46:23.754186

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8ceeeafb95b0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('session', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.create_foreign_key(None, 'session', 'user', ['user_id'], ['id'])
    op.add_column('user', sa.Column('role_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'user', 'role', ['role_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='foreignkey')
    op.drop_column('user', 'role_id')
    op.drop_constraint(None, 'session', type_='foreignkey')
    op.alter_column('session', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###
