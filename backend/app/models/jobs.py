from datetime import datetime, UTC
from enum import StrEnum
from uuid import uuid4

from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    Integer,
    JSON,
    String,
    UUID,
    func,
    text
)

from ..db.session import Base


class JobStatus(StrEnum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class JobType(StrEnum):
    INTERFEROMETRY = "INTERFEROMETRY"


class Job(Base):
    __tablename__ = "jobs"

    id = Column(
        type_=UUID,
        primary_key=True,
        index=True,
        server_default=func.gen_random_uuid()
    )
    type = Column(
        type_=Enum(JobType),
        nullable=False,
    )
    parameters = Column(
        type_=JSON,
        nullable=False,
        default={}
    )
    status = Column(
        type_=Enum(JobStatus),
        nullable=False,
        default=JobStatus.PENDING
    )
    result = Column(
        type_=JSON,
        nullable=False,
        default={}
    )
    error = Column(
        type_=String,
        nullable=True
    )
    compute_time = Column(
        type_=Integer,
        nullable=True
    )
    created_at = Column(
        type_=DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )
    updated_at = Column(
        type_=DateTime(timezone=True),
        nullable=True,
        onupdate=lambda: datetime.now(UTC)
    )