"""Changed relationship in ProjectCriterionValue on ProjectCriterion

Revision ID: cc19bb3fc61f
Revises: 763ab1addfef
Create Date: 2021-11-14 21:48:01.122096

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cc19bb3fc61f'
down_revision = '763ab1addfef'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('project_criterion_value_project_id_project_criterion_id_fkey', 'project_criterion_value', type_='foreignkey')
    op.create_foreign_key('project_criterion_value_project_criterion_id_fkey', 'project_criterion_value', 'project_criterion', ['project_criterion_id'], ['project_criterion_id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('project_criterion_value_project_criterion_id_fkey', 'project_criterion_value', type_='foreignkey')
    op.create_foreign_key('project_criterion_value_project_id_project_criterion_id_fkey', 'project_criterion_value', 'project_specific_criterion', ['project_id', 'project_criterion_id'], ['project_id', 'project_criterion_id'], ondelete='CASCADE')
    # ### end Alembic commands ###