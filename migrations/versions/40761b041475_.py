"""empty message

Revision ID: 40761b041475
Revises: d9cf44630b3c
Create Date: 2020-12-20 11:05:42.363051

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '40761b041475'
down_revision = 'd9cf44630b3c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('shows', sa.Column('venue_image_link', sa.String(length=500), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('shows', 'venue_image_link')
    # ### end Alembic commands ###