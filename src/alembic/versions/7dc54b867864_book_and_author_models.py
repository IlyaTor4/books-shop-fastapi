"""book and author models

Revision ID: 7dc54b867864
Revises: af4c96f52f82
Create Date: 2024-11-07 13:15:40.514429

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7dc54b867864'
down_revision: Union[str, None] = 'af4c96f52f82'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('author',
    sa.Column('uid', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.PrimaryKeyConstraint('uid'),
    sa.UniqueConstraint('name')
    )
    op.create_table('book',
    sa.Column('uid', sa.UUID(), nullable=False),
    sa.Column('title', sa.String(length=64), nullable=False),
    sa.Column('publication_year', sa.Integer(), nullable=False),
    sa.Column('pages', sa.Integer(), nullable=False),
    sa.Column('genre', sa.String(length=64), nullable=False),
    sa.PrimaryKeyConstraint('uid'),
    sa.UniqueConstraint('title')
    )
    op.create_table('author_book',
    sa.Column('author_uid', sa.UUID(), nullable=False),
    sa.Column('book_uid', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['author_uid'], ['author.uid'], ),
    sa.ForeignKeyConstraint(['book_uid'], ['book.uid'], ),
    sa.PrimaryKeyConstraint('author_uid', 'book_uid')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('author_book')
    op.drop_table('book')
    op.drop_table('author')
    # ### end Alembic commands ###
