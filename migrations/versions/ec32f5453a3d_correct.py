"""correct

Revision ID: ec32f5453a3d
Revises: 15d3c2a43b44
Create Date: 2024-10-12 20:07:00.530712

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ec32f5453a3d'
down_revision: Union[str, None] = '15d3c2a43b44'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('correct',
                    sa.Column('id', sa.Integer, nullable=False, unique=True),
                    sa.Column('created_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"),
                              nullable=False),
                    sa.Column('comment', sa.String, nullable=True),
                    sa.PrimaryKeyConstraint("id"),
                    sa.UniqueConstraint("id")
                    )


def downgrade() -> None:
    op.drop_table("correct")