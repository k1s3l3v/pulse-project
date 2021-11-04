"""Create MADO sequence

Revision ID: 60e99e4f1a42
Revises:
Create Date: 2021-10-08 19:02:36.963731

"""
from alembic import op
from sqlalchemy.schema import Sequence, CreateSequence, DropSequence


# revision identifiers, used by Alembic.
revision = '60e99e4f1a42'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute(CreateSequence(Sequence('mado_seq')))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute(DropSequence(Sequence('mado_seq')))
    # ### end Alembic commands ###