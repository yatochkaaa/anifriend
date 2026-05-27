"""fix case insensitive username index

Revision ID: 4c37d0f94e9f
Revises: 3bfe13dac4b7
Create Date: 2026-05-27 18:15:30.887075

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4c37d0f94e9f'
down_revision: Union[str, Sequence[str], None] = '3bfe13dac4b7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_index('uq_users_username_lower', 'users', [sa.text('LOWER(username)')], unique=True)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index('uq_users_username_lower', 'users')
