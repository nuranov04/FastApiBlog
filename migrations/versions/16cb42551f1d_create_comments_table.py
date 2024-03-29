"""create comments table

Revision ID: 16cb42551f1d
Revises: b2df9e1f4a0c
Create Date: 2023-04-17 06:11:25.104803

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '16cb42551f1d'
down_revision = 'b2df9e1f4a0c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('comment',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['post_id'], ['post.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_comment_id'), 'comment', ['id'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_comment_id'), table_name='comment')
    op.drop_table('comment')
    # ### end Alembic commands ###
