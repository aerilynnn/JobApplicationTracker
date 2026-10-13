import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, UUIDPrimaryKeyMixin, str_enum
from app.models.enums import DocType

if TYPE_CHECKING:
    from app.models.application import Application


class Document(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "documents"

    application_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("applications.id", ondelete="CASCADE"), index=True
    )
    doc_type: Mapped[DocType] = mapped_column(str_enum(DocType, "doc_type"))
    s3_key: Mapped[str] = mapped_column(unique=True)
    original_filename: Mapped[str]
    content_type: Mapped[str]
    size_bytes: Mapped[int]
    uploaded_at: Mapped[datetime] = mapped_column(server_default=func.now())

    application: Mapped["Application"] = relationship(back_populates="documents")
