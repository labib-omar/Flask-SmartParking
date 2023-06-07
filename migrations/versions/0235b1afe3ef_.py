"""empty message

Revision ID: 0235b1afe3ef
Revises: 5ebaffb35922
Create Date: 2023-06-07 21:58:13.309495

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0235b1afe3ef'
down_revision = '5ebaffb35922'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('reservations', sa.Column('reservation_datetime', sa.DateTime(), nullable=False))
    op.drop_column('reservations', 'reservation_date')
    op.drop_column('reservations', 'reservation_time')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('reservations', sa.Column('reservation_time', sa.DATETIME(), nullable=True))
    op.add_column('reservations', sa.Column('reservation_date', sa.DATE(), nullable=False))
    op.drop_column('reservations', 'reservation_datetime')
    # ### end Alembic commands ###