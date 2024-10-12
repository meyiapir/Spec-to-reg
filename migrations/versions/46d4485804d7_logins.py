"""logins

Revision ID: 46d4485804d7
Revises: 
Create Date: 2024-10-12 12:27:57.452324

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '46d4485804d7'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("logins",
                    sa.Column("username", sa.String, nullable=False, unique=True),
                    sa.Column("name", sa.String, nullable=False),
                    sa.Column("password", sa.String, nullable=False)
                    )

    op.execute("""
        INSERT INTO logins (username, name, password) 
        VALUES ('admin', 'admin', 'admin')
    """)


def downgrade() -> None:
    op.drop_table("logins")

