"""empty message

Revision ID: 378e51239cfe
Revises: 6fe53a4251ad
Create Date: 2020-12-20 06:56:57.365273

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '378e51239cfe'
down_revision = '6fe53a4251ad'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('shows',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('start_time', sa.DateTime(), nullable=False),
    sa.Column('venue_id', sa.Integer(), nullable=False),
    sa.Column('venue_name', sa.String(), nullable=False),
    sa.Column('artist_id', sa.Integer(), nullable=False),
    sa.Column('artist_name', sa.String(), nullable=False),
    sa.Column('artist_image_link', sa.String(length=120), nullable=True),
    sa.ForeignKeyConstraint(['artist_id'], ['artists.id'], ),
    sa.ForeignKeyConstraint(['venue_id'], ['venues.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('shows')
    # ### end Alembic commands ###
