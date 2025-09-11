"""2025-09-11-07:01_add_isactive_cax

Revision ID: d3484eb9feba
Revises: 68013df97df0
Create Date: 2025-09-11 07:01:24.962892

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'd3484eb9feba'
down_revision: Union[str, None] = '68013df97df0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # Добавляем столбец is_active с типом Boolean, значением по умолчанию true и ограничением NOT NULL
    op.add_column('cax_codes', sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('true')))
    
    # Опционально: если вы хотите, чтобы server_default не применялся к новым строкам после миграции,
    # можно убрать server_default после применения
    op.alter_column('cax_codes', 'is_active', server_default=None)

def downgrade() -> None:
    # Удаляем столбец is_active при откате миграции
    op.drop_column('cax_codes', 'is_active')