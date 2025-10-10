"""2025-10-10-09:11_correct_adress

Revision ID: 67ad8395d339
Revises: 4abe1671df48
Create Date: 2025-10-10 09:11:14.405620

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '67ad8395d339'
down_revision: Union[str, None] = '4abe1671df48'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    # Переименовываем колонку без удаления/добавления
    op.alter_column('patients', 'address', new_column_name='adress')

def downgrade():
    # Обратное переименование
    op.alter_column('patients', 'adress', new_column_name='address')
