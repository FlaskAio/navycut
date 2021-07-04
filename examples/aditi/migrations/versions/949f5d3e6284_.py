"""empty message

Revision ID: 949f5d3e6284
Revises: e7255b2d5649
Create Date: 2021-07-04 13:55:23.268739

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_jsonfield
import navycut


# revision identifiers, used by Alembic.
revision = '949f5d3e6284'
down_revision = 'e7255b2d5649'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('blog',
    sa.Column('id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('picture', navycut.orm.sqla.types.ImageType(length=255), nullable=False),
    sa.Column('body', sa.Text(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('name')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('blog')
    # ### end Alembic commands ###