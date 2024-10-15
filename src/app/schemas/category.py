from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field

from ..core.schemas import TimestampSchema


class CategoryBase(BaseModel):
    name: Annotated[str, Field(examples=["cosmetic"])]
    category_parent_id: Annotated[int | None, Field(examples=["1"])]


class Category(TimestampSchema, CategoryBase):
    pass


class CategoryRead(CategoryBase):
    id: int
    path: str | None = None
    created_at: datetime


class CategoryCreate(CategoryBase):
    pass


class CategoryCreateInternal(CategoryCreate):
    pass


class CategoryUpdate(BaseModel):
    name: str | None = None
    category_parent_id: int | None = None


class CategoryUpdateInternal(CategoryUpdate):
    updated_at: datetime


class CategoryDelete(BaseModel):
    pass
