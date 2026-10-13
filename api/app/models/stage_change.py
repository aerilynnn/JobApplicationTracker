import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, UUIDPrimaryKeyMixin, str_enum
from app.models.enums import ApplicationStage

if TYPE_CHECKING:
    from app.models.application import Application


class StageChange(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "stage_changes"

    application_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("applications.id", ondelete="CASCADE"), index=True
    )
    from_stage: Mapped[ApplicationStage | None] = mapped_column(
        str_enum(ApplicationStage, "from_stage")
    )
    to_stage: Mapped[ApplicationStage] = mapped_column(str_enum(ApplicationStage, "to_stage"))
    changed_at: Mapped[datetime] = mapped_column(server_default=func.now())

    application: Mapped["Application"] = relationship(back_populates="stage_changes")
