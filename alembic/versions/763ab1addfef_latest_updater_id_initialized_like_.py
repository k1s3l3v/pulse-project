"""latest_updater_id initialized like nullable

Revision ID: 763ab1addfef
Revises: 03485ae033f2
Create Date: 2021-11-09 17:00:29.528698

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '763ab1addfef'
down_revision = '03485ae033f2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('project_status', 'latest_updater_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('project_status', 'latest_updater_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###
