"""add title column

Revision ID: 8f87b4278205
Revises: ae54a49b7124
Create Date: 2023-07-20 11:43:22.454862

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8f87b4278205'
down_revision = 'ae54a49b7124'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
