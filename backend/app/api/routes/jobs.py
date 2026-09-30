from typing import List, Optional
from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    Response
)
from sqlalchemy import (
    JSON, 
    and_,
    func,
    select
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.jobs import (
    JobCreate,
    JobListResponse,
    JobResponse
)
from app.db.session import get_async_db
from app.models.jobs import Job, JobStatus


router = APIRouter(tags=["Processing Jobs"])


@router.post(
    "/jobs", 
    response_model=JobResponse, 
    status_code=201
)
async def create_job(
    job: JobCreate, 
    db: AsyncSession = Depends(get_async_db)
):
    """Create a new job in the database."""
    db_job = Job(**job.model_dump())

    db.add(db_job)

    await db.commit()
    await db.refresh(db_job)

    return db_job


@router.get(
    "/jobs", 
    response_model=JobListResponse
)
async def list_jobs(
    db: AsyncSession = Depends(get_async_db),
    status: Optional[List[JobStatus]] = Query(None),
    skip: int = 0,
    limit: int = 20,
):
    query = select(Job)

    if status:
        query = query.where(Job.status.in_(status))

    total_result = await db.execute(
        select(
            func.count()
        ).select_from(
            query
        )
    )
    total = total_result.scalar_one()

    job_result = await db.execute(
        query.order_by(Job.created_at.desc())
        .offset(skip)
        .limit(limit)
    )

    jobs = job_result.scalars().all()

    return {"total": total, "jobs": jobs}


@router.get(
    "/jobs/{id}",
    response_model=JobResponse
)
async def get_job(
    id: UUID,
    db: AsyncSession = Depends(get_async_db),
):
    result = await db.execute(
        select(
            Job
        ).where(
            Job.id == id
        )
    )

    job = result.scalar_one_or_none()

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    return job