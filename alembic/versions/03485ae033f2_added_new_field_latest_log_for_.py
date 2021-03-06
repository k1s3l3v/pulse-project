"""Added new field latest_log for ProjectStatus table

Revision ID: 03485ae033f2
Revises: ad8e8fd9ca31
Create Date: 2021-11-09 14:58:04.887485

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '03485ae033f2'
down_revision = 'ad8e8fd9ca31'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('project_status', sa.Column('latest_log', sa.JSON(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('project_status', 'latest_log')
    # ### end Alembic commands ###
