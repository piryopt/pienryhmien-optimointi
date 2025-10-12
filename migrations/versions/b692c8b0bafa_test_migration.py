"""Test migration

Revision ID: b692c8b0bafa
Revises: 
Create Date: 2025-10-12 15:42:44.553260

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b692c8b0bafa'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("ALTER TABLE survey_choices ADD COLUMN important BOOLEAN DEFAULT FALSE;")


def downgrade() -> None:
    op.execute("ALTER TABLE survey_choices DROP COLUMN important;")
