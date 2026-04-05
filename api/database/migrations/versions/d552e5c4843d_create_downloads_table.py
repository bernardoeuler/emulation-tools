"""create downloads table

Revision ID: d552e5c4843d
Revises: 8cb65dc6fb18
Create Date: 2026-04-05 17:40:47.666828

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd552e5c4843d'
down_revision: Union[str, Sequence[str], None] = '8cb65dc6fb18'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('downloads',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('public_id', sa.String(length=32), nullable=False),
        sa.Column('request_id', sa.Integer(), nullable=False),
        sa.Column('status', sa.Enum('PENDING', 'READY', 'FAILED', name='download_status_enum'), nullable=False),
        sa.Column('file_uri', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['request_id'], ['requests.id'], )
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('downloads')
