from datetime import datetime
from typing import (
    Any, 
    List,
    Optional
)
from uuid import UUID

from pydantic import BaseModel

from app.models.jobs import JobStatus, JobType


class JobCreate(BaseModel):
    type: JobType
    parameters: dict[str, Any]


class JobResponse(JobCreate):
    id: UUID
    type: JobType
    status: JobStatus
    parameters: dict[str, Any]
    result: dict[str, Any]
    error: Optional[str] = None
    compute_time: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class JobListResponse(BaseModel):
    total: int
    jobs: List[JobResponse]

    class Config:
        from_attributes = True