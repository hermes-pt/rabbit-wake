"""fix product_info composite primary key

Revision ID: 1459161ce827
Revises: 966cfec4c78d
Create Date: 2025-07-05 13:16:29.761764

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1459161ce827'
down_revision: Union[str, Sequence[str], None] = '966cfec4c78d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Drop the old table
    op.drop_table('product_info')
    
    # Create new table with composite primary key
    op.create_table('product_info',
        sa.Column('info_id', sa.Integer(), nullable=False),
        sa.Column('variant_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('text', sa.String(), nullable=False),
        sa.Column('show_on_site', sa.Boolean(), nullable=False),
        sa.Column('info_type', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['variant_id'], ['product_variants.id'], ),
        sa.PrimaryKeyConstraint('info_id', 'variant_id')
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Drop the new table
    op.drop_table('product_info')
    
    # Recreate old table structure
    op.create_table('product_info',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('variant_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('text', sa.String(), nullable=False),
        sa.Column('show_on_site', sa.Boolean(), nullable=False),
        sa.Column('info_type', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['variant_id'], ['product_variants.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_product_info_id'), 'product_info', ['id'], unique=False)