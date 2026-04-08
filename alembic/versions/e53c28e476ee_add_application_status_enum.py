"""add application status enum

Revision ID: e53c28e476ee
Revises: 3ec74892782f
Create Date: 2026-04-07 22:25:46.402599

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e53c28e476ee'
down_revision: Union[str, Sequence[str], None] = '3ec74892782f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # створюємо enum
    application_status = sa.Enum(
        'saved', 'applied', 'interview', 'offer', 'rejected',
        name='applicationstatus'
    )
    application_status.create(op.get_bind())

    # 🔥 приводимо старі значення до нижнього регістру
    op.execute("UPDATE applications SET status = LOWER(status)")

    # 🔥 тепер міняємо тип
    op.execute(
        "ALTER TABLE applications "
        "ALTER COLUMN status TYPE applicationstatus "
        "USING status::applicationstatus"
    )


def downgrade() -> None:
    # повертаємо назад у VARCHAR
    op.execute(
        "ALTER TABLE applications "
        "ALTER COLUMN status TYPE VARCHAR"
    )

    # видаляємо enum type
    application_status = sa.Enum(
        'saved', 'applied', 'interview', 'offer', 'rejected',
        name='applicationstatus'
    )
    application_status.drop(op.get_bind())