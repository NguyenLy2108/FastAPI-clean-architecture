from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field

from ..core.schemas import TimestampSchema


class RoleBase(BaseModel):
    name: Annotated[str, Field(examples=["admin"])]


class Role(TimestampSchema, RoleBase):
    pass


class RoleRead(RoleBase):
    id: int
    created_at: datetime


class RoleCreate(RoleBase):
    pass

class RoleCreateInternal(RoleCreate):
    pass


class RoleUpdate(BaseModel):
    name: str | None = None


class RoleUpdateInternal(RoleUpdate):
    updated_at: datetime


class RoleDelete(BaseModel):
    pass
