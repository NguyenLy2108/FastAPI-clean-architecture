from datetime import UTC, datetime
from unicodedata import category

from sqlalchemy import DateTime, String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from ..core.db.database import Base

class Category(Base):
    __tablename__ = "category"

    id: Mapped[int] = mapped_column("id", autoincrement=True, nullable=False, unique=True, primary_key=True, init=False)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    category_parent_id: Mapped[int | None] = mapped_column(Integer, default=None)
    path: Mapped[str| None] = mapped_column(String, default=None)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default_factory=lambda: datetime.now(UTC))
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)
