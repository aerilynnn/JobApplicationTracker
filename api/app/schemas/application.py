import uuid
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict

from app.models.enums import ApplicationStage, ScrapeStatus


class ApplicationBase(BaseModel):
    """Fields a client is allowed to set on an application."""

    company: str | None = None
    title: str | None = None
    location: str | None = None
    job_url: str | None = None
    description: str | None = None
    notes: str | None = None
    applied_on: date | None = None
    salary_min: int | None = None
    salary_max: int | None = None
    salary_currency: str = "USD"


class ApplicationCreate(ApplicationBase):
    """Request body for POST /applications."""

    company: str
    title: str
    stage: ApplicationStage = ApplicationStage.SAVED


class ApplicationRead(ApplicationBase):
    """Response body: what the API sends back."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    stage: ApplicationStage
    scrape_status: ScrapeStatus
    last_activity_at: datetime
    updated_at: datetime
    created_at: datetime
