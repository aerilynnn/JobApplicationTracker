from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.application import Application


class User(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str]

    applications: Mapped[list["Application"]] = relationship(
        back_populates="user", cascade="all, delete-orphan", passive_deletes=True
    )
