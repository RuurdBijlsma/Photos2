"""empty message

Revision ID: a5040acf49b7
Revises: 01d149d925d2
Create Date: 2024-11-25 14:24:51.611431

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'a5040acf49b7'
down_revision: Union[str, None] = '01d149d925d2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('visual_information',
                  sa.Column('summary', sa.String(), nullable=True))
    op.alter_column('visual_information', 'caption',
                    existing_type=sa.VARCHAR(),
                    nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('visual_information', 'caption',
                    existing_type=sa.VARCHAR(),
                    nullable=True)
    op.drop_column('visual_information', 'summary')
    # ### end Alembic commands ###
