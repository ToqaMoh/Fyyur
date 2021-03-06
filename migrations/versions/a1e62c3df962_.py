"""empty message

Revision ID: a1e62c3df962
Revises: 4b8cb8cb7bc3
Create Date: 2020-12-17 22:29:09.116434

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a1e62c3df962'
down_revision = '4b8cb8cb7bc3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('City',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('city', sa.String(length=120), nullable=False),
    sa.Column('state', sa.String(length=120), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('Venue', sa.Column('city_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'Venue', 'City', ['city_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'Venue', type_='foreignkey')
    op.drop_column('Venue', 'city_id')
    op.drop_table('City')
    # ### end Alembic commands ###
