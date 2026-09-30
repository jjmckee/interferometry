"""Add jobs table

Revision ID: c91e8d699d8c
Revises: 0d2dc8ecb93b
Create Date: 2026-09-29 13:40:52.023770

"""
from datetime import datetime, UTC
from typing import Sequence, Union
from uuid import uuid4

import sqlalchemy as sa
from alembic import op

from app.models.jobs import JobStatus


# revision identifiers, used by Alembic.
revision: str = 'c91e8d699d8c'
down_revision: Union[str, Sequence[str], None] = '0d2dc8ecb93b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "jobs",
        sa.Column(
            name="id",
            type_=sa.UUID,
            primary_key=True,
            server_default=sa.func.gen_random_uuid()
        ),
        sa.Column(
            name="type",
            type_=sa.String,
            nullable=False,
        ),
        sa.Column(
            name="parameters",
            type_=sa.JSON,
            nullable=False,
        ),
        sa.Column(
            name="status",
            type_=sa.Enum(JobStatus, name="jobstatus"),
            nullable=False,
        ),
        sa.Column(
            name="result",
            type_=sa.JSON,
            nullable=False,
        ),
        sa.Column(
            name="error",
            type_=sa.String,
            nullable=True
        ),
        sa.Column(
            name="compute_time",
            type_=sa.Integer,
            nullable=True
        ),
        sa.Column(
            name="created_at",
            type_=sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now()
        ),
        sa.Column(
            name="updated_at",
            type_=sa.DateTime(timezone=True),
            nullable=True,
            onupdate=lambda: datetime.now(UTC)
        ),
    )

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("jobs")
    op.execute("DROP TYPE jobstatus")   
