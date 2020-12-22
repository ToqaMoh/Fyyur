"""empty message

Revision ID: 082773815602
Revises: b19c8e375353
Create Date: 2020-12-22 20:20:08.234486

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '082773815602'
down_revision = 'b19c8e375353'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('shows',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('start_time', sa.DateTime(), nullable=False),
    sa.Column('venue_id', sa.Integer(), nullable=False),
    sa.Column('venue_name', sa.String(), nullable=False),
    sa.Column('venue_image_link', sa.String(length=500), nullable=True),
    sa.Column('artist_id', sa.Integer(), nullable=False),
    sa.Column('artist_name', sa.String(), nullable=False),
    sa.Column('artist_image_link', sa.String(length=500), nullable=True),
    sa.ForeignKeyConstraint(['artist_id'], ['artists.id'], ),
    sa.ForeignKeyConstraint(['venue_id'], ['venues.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('shows')
    # ### end Alembic commands ###
