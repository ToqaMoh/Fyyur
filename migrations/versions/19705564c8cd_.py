"""empty message

Revision ID: 19705564c8cd
Revises: 6711a7db370e
Create Date: 2020-12-19 08:49:09.144046

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '19705564c8cd'
down_revision = '6711a7db370e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('artists', 'seeking_talent',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    op.drop_column('artists', 'seeking_description')
    op.alter_column('venues', 'seeking_talent',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    op.drop_column('venues', 'seeking_description')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('venues', sa.Column('seeking_description', sa.VARCHAR(length=500), autoincrement=False, nullable=True))
    op.alter_column('venues', 'seeking_talent',
               existing_type=sa.BOOLEAN(),
               nullable=False)
    op.add_column('artists', sa.Column('seeking_description', sa.VARCHAR(length=500), autoincrement=False, nullable=True))
    op.alter_column('artists', 'seeking_talent',
               existing_type=sa.BOOLEAN(),
               nullable=False)
    # ### end Alembic commands ###
