"""add description to products

Revision ID: 507c29d31117
Revises: ee2fd9a5c4d8
Create Date: 2022-01-20 12:50:29.063926

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '507c29d31117'
down_revision = 'ee2fd9a5c4d8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('products', sa.Column('description', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('products', 'description')
    # ### end Alembic commands ###
