from datetime import UTC, datetime

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from ..core.db.database import Base


class RolePermission(Base):
    __tablename__ = "role_permission"

    id: Mapped[int] = mapped_column("id", autoincrement=True, nullable=False, unique=True, primary_key=True, init=False)
    role_id: Mapped[int] = mapped_column(ForeignKey("role.id"), index=True)
    permission_id: Mapped[int] = mapped_column(ForeignKey("permission.id"), index=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default_factory=lambda: datetime.now(UTC))
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)
