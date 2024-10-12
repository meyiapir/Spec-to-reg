"""requirements

Revision ID: 8fecb2702702
Revises: 46d4485804d7
Create Date: 2024-10-12 13:51:06.587838

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8fecb2702702'
down_revision: Union[str, None] = '46d4485804d7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("requirements",
                    sa.Column("username", sa.String, nullable=False, unique=True),
                    sa.Column("name", sa.String, nullable=False),
                    sa.Column("password", sa.String, nullable=False)
                    )


def downgrade() -> None:
    op.drop_table("requirements")