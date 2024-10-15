from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field

from ..core.schemas import TimestampSchema


class RolePermissionBase(BaseModel):
    role_id: int
    permission_id: int


class RolePermission(TimestampSchema, RolePermissionBase):
    pass


class RolePermissionRead(RolePermissionBase):
    id: int
    created_at: datetime


class RolePermissionCreate(RolePermissionBase):
    pass


class RolePermissionCreateInternal(RolePermissionCreate):
    pass


class RolePermissionUpdate(BaseModel):
    role_id: int | None = None
    permission_id: int | None = None


class RolePermissionUpdateInternal(RolePermissionUpdate):
    updated_at: datetime


class RolePermissionDelete(BaseModel):
    pass
