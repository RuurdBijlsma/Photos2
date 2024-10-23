"""change

Revision ID: 6e8ca8375e53
Revises: 246a64605950
Create Date: 2024-10-16 21:06:52.163539

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "6e8ca8375e53"
down_revision: Union[str, None] = "246a64605950"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("images", sa.Column("user_id", sa.Integer(), nullable=False))
    op.create_foreign_key(None, "images", "users", ["user_id"], ["id"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "images", type_="foreignkey")
    op.drop_column("images", "user_id")
    # ### end Alembic commands ###