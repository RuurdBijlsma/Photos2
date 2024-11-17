"""empty message

Revision ID: 28a5bd29d1c9
Revises: b21bdf97abf7
Create Date: 2024-11-17 14:02:52.010866

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from pgvecto_rs.sqlalchemy import VECTOR
from pgvecto_rs.types import IndexOption, Hnsw


# revision identifiers, used by Alembic.
revision: str = '28a5bd29d1c9'
down_revision: Union[str, None] = 'b21bdf97abf7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('visual_information', sa.Column('document_summary', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('visual_information', 'document_summary')
    # ### end Alembic commands ###