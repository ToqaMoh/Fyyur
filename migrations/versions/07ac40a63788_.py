"""empty message

Revision ID: 07ac40a63788
Revises: 8523e0cbe689
Create Date: 2020-12-22 19:58:23.425225

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '07ac40a63788'
down_revision = '8523e0cbe689'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('artists', sa.Column('past_shows', sa.ARRAY(sa.String()), nullable=True))
    op.add_column('artists', sa.Column('past_shows_count', sa.Integer(), nullable=True))
    op.add_column('artists', sa.Column('upcoming_shows', sa.ARRAY(sa.String()), nullable=True))
    op.add_column('artists', sa.Column('upcoming_shows_count', sa.Integer(), nullable=True))
    op.add_column('shows', sa.Column('artist_image_link', sa.String(length=500), nullable=True))
    op.add_column('shows', sa.Column('artist_name', sa.String(), nullable=False))
    op.add_column('shows', sa.Column('venue_image_link', sa.String(length=500), nullable=True))
    op.add_column('shows', sa.Column('venue_name', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('shows', 'venue_name')
    op.drop_column('shows', 'venue_image_link')
    op.drop_column('shows', 'artist_name')
    op.drop_column('shows', 'artist_image_link')
    op.drop_column('artists', 'upcoming_shows_count')
    op.drop_column('artists', 'upcoming_shows')
    op.drop_column('artists', 'past_shows_count')
    op.drop_column('artists', 'past_shows')
    # ### end Alembic commands ###
