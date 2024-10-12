"""mistakes

Revision ID: 15d3c2a43b44
Revises: 8fecb2702702
Create Date: 2024-10-12 19:25:30.778498

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '15d3c2a43b44'
down_revision: Union[str, None] = '8fecb2702702'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_table("requirements")
    op.create_table('mistakes',
                    sa.Column('id', sa.Integer, nullable=False, unique=True),
                    sa.Column('created_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"),
                              nullable=False),
                    sa.Column('reason', sa.String, nullable=False),
                    sa.PrimaryKeyConstraint("id"),
                    sa.UniqueConstraint("id")
                    )


def downgrade() -> None:
    op.drop_table("mistakes")
