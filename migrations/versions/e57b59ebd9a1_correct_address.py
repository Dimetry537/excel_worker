"""correct_address

Revision ID: e57b59ebd9a1
Revises: 67ad8395d339
Create Date: 2025-10-28 09:34:31.955284

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e57b59ebd9a1'
down_revision: Union[str, None] = '67ad8395d339'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Переименование колонки
    op.alter_column('patients', 'adress',
                    new_column_name='address',
                    existing_type=sa.String(),
                    existing_nullable=False)  # Укажите тип и nullable, если нужно

def downgrade():
    # Обратное переименование
    op.alter_column('patients', 'address',
                    new_column_name='adress',
                    existing_type=sa.String(),
                    existing_nullable=False)