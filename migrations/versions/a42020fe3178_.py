"""empty message

Revision ID: a42020fe3178
Revises: 40761b041475
Create Date: 2020-12-20 13:26:12.049506

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a42020fe3178'
down_revision = '40761b041475'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('shows_venue_id_fkey', 'shows', type_='foreignkey')
    op.create_foreign_key(None, 'shows', 'venues', ['venue_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'shows', type_='foreignkey')
    op.create_foreign_key('shows_venue_id_fkey', 'shows', 'venues', ['venue_id'], ['id'])
    # ### end Alembic commands ###
