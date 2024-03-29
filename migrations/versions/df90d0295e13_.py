"""empty message

Revision ID: df90d0295e13
Revises: 386af47671b9
Create Date: 2023-06-07 00:36:57.642733

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'df90d0295e13'
down_revision = '386af47671b9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('parking_areas',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('free_spaces', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('reservations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('parking_area_id', sa.Integer(), nullable=False),
    sa.Column('reservation_date', sa.Date(), nullable=False),
    sa.ForeignKeyConstraint(['parking_area_id'], ['parking_areas.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('reservations')
    op.drop_table('parking_areas')
    # ### end Alembic commands ###
