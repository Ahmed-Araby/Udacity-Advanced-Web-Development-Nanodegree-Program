"""empty message

Revision ID: ba835a060d32
Revises: e7289970a79c
Create Date: 2020-11-22 00:44:53.909554

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ba835a060d32'
down_revision = 'e7289970a79c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('artist', 'city',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    op.alter_column('artist', 'phone',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    op.alter_column('artist', 'state',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    op.drop_constraint('one_show_byArtist_atATime', 'show', type_='unique')
    op.create_unique_constraint('one_show_byArtist_atATime', 'show', ['venue_id', 'start_time'])
    op.drop_constraint('one_show_perVenue_atATime', 'show', type_='unique')
    op.create_unique_constraint('one_show_perVenue_atATime', 'show', ['artist_id', 'start_time'])
    op.alter_column('venue', 'phone',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('venue', 'phone',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    op.drop_constraint('one_show_perVenue_atATime', 'show', type_='unique')
    op.create_unique_constraint('one_show_perVenue_atATime', 'show', ['venue_id', 'start_time'])
    op.drop_constraint('one_show_byArtist_atATime', 'show', type_='unique')
    op.create_unique_constraint('one_show_byArtist_atATime', 'show', ['artist_id', 'start_time'])
    op.alter_column('artist', 'state',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    op.alter_column('artist', 'phone',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    op.alter_column('artist', 'city',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    # ### end Alembic commands ###
