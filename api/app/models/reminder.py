import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Index, func, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, UUIDPrimaryKeyMixin, str_enum
from app.models.enums import ReminderKind, ReminderStatus

if TYPE_CHECKING:
    from app.models.application import Application


class Reminder(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "reminders"
    __table_args__ = (
        Index(
            "uq_reminders_one_pending_per_kind",
            "application_id",
            "kind",
            unique=True,
            postgresql_where=text("status = 'pending'"),
        ),
    )

    application_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("applications.id", ondelete="CASCADE"), index=True
    )
    kind: Mapped[ReminderKind] = mapped_column(str_enum(ReminderKind, "kind"))
    due_at: Mapped[datetime]
    status: Mapped[ReminderStatus] = mapped_column(
        str_enum(ReminderStatus, "status"), default=ReminderStatus.PENDING
    )
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    application: Mapped["Application"] = relationship(back_populates="reminders")
