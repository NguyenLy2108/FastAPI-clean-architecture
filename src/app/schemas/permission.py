from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field

from ..core.schemas import TimestampSchema


class PermissionBase(BaseModel):
    name: Annotated[str, Field(examples=["product.create"])]


class Permission(TimestampSchema, PermissionBase):
    pass


class PermissionRead(PermissionBase):
    id: int
    created_at: datetime


class PermissionCreate(PermissionBase):
    pass


class PermissionCreateInternal(PermissionCreate):
    pass


class PermissionUpdate(BaseModel):
    name: str | None = None


class PermissionUpdateInternal(PermissionUpdate):
    updated_at: datetime


class PermissionDelete(BaseModel):
    pass
