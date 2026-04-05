"""create requests table

Revision ID: 8cb65dc6fb18
Revises: 
Create Date: 2026-04-05 17:27:33.361165

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8cb65dc6fb18'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('requests',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('public_id', sa.String(length=32), nullable=False),
        sa.Column('type', sa.Enum('ROM_CONVERSION', name='request_type_enum'), nullable=False),
        sa.Column('status', sa.Enum('PENDING', 'IN_PROGRESS', 'DONE', 'FAILED', name='request_status_enum'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('requests')
