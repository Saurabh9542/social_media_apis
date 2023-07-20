"""add fkey to post table

Revision ID: 61b1c7b8317c
Revises: 9adfcb6a4f9d
Create Date: 2023-07-20 11:58:19.216368

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '61b1c7b8317c'
down_revision = '9adfcb6a4f9d'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk',source_table='posts', referent_table='users',
                          local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE"
                          )
    pass


def downgrade() :
    op.drop_constraint('posts_users_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass
