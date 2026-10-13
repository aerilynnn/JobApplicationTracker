import uuid
from datetime import date, datetime
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin, str_enum
from app.models.enums import ApplicationStage, ScrapeStatus

if TYPE_CHECKING:
    from app.models.document import Document
    from app.models.reminder import Reminder
    from app.models.stage_change import StageChange
    from app.models.user import User


class Application(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "applications"
    __table_args__ = (
        Index("ix_applications_user_id_stage", "user_id", "stage"),
        CheckConstraint(
            "salary_min IS NULL OR salary_max IS NULL OR salary_max >= salary_min",
            name="salary_range",
        ),
    )

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    company: Mapped[str | None]
    title: Mapped[str | None]
    location: Mapped[str | None]
    job_url: Mapped[str | None]
    description: Mapped[str | None]
    notes: Mapped[str | None]

    stage: Mapped[ApplicationStage] = mapped_column(
        str_enum(ApplicationStage, "stage"), default=ApplicationStage.SAVED
    )
    scrape_status: Mapped[ScrapeStatus] = mapped_column(
        str_enum(ScrapeStatus, "scrape_status"), default=ScrapeStatus.NOT_APPLICABLE
    )

    applied_on: Mapped[date | None]
    salary_min: Mapped[int | None]
    salary_max: Mapped[int | None]
    salary_currency: Mapped[str] = mapped_column(String(3), default="USD")

    last_activity_at: Mapped[datetime] = mapped_column(server_default=func.now(), index=True)

    user: Mapped["User"] = relationship(back_populates="applications")
    stage_changes: Mapped[list["StageChange"]] = relationship(
        back_populates="application", cascade="all, delete-orphan", passive_deletes=True
    )
    documents: Mapped[list["Document"]] = relationship(
        back_populates="application", cascade="all, delete-orphan", passive_deletes=True
    )
    reminders: Mapped[list["Reminder"]] = relationship(
        back_populates="application", cascade="all, delete-orphan", passive_deletes=True
    )
