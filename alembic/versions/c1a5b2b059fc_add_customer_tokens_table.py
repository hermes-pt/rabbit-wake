"""add customer tokens table

Revision ID: c1a5b2b059fc
Revises: ce38d9aea784
Create Date: 2025-07-10 21:06:46.659432

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c1a5b2b059fc'
down_revision: Union[str, Sequence[str], None] = 'ce38d9aea784'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'customer_tokens',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('phone', sa.String(20), nullable=False),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('token', sa.Text(), nullable=False),
        sa.Column('token_type', sa.String(50), nullable=True),
        sa.Column('valid_until', sa.DateTime(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    
    op.create_index('idx_customer_tokens_phone', 'customer_tokens', ['phone'])
    op.create_index('idx_customer_tokens_email', 'customer_tokens', ['email'])
    op.create_index('idx_customer_tokens_valid_until', 'customer_tokens', ['valid_until'])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index('idx_customer_tokens_valid_until', table_name='customer_tokens')
    op.drop_index('idx_customer_tokens_email', table_name='customer_tokens')
    op.drop_index('idx_customer_tokens_phone', table_name='customer_tokens')
    op.drop_table('customer_tokens')
