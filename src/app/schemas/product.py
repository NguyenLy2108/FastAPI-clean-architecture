from datetime import datetime
from typing import Annotated
from unicodedata import category

from pydantic import BaseModel, ConfigDict, Field

from ..core.schemas import PersistentDeletion, TimestampSchema, UUIDSchema


class ProductBase(BaseModel):
    name: Annotated[str, Field(min_length=2, max_length=150, examples=["This is the first product"])]
    description: Annotated[str, Field(min_length=1, max_length=63206, examples=["This is the description of this product."])]
    category_id: Annotated[int, Field(examples=[1])]

class Product(TimestampSchema, ProductBase, UUIDSchema, PersistentDeletion):    
    media_url: Annotated[
        str | None,
        Field(pattern=r"^(https?|ftp)://[^\s/$.?#].[^\s]*$", examples=["https://www.productimageurl.com"], default=None),
    ]
    created_by_user_id: int  

class ProductRead(BaseModel):
    id: int
    name: Annotated[str, Field(min_length=2, max_length=150, examples=["This is the first product"])]
    description: Annotated[str, Field(min_length=1, max_length=63206, examples=["This is the description of this product."])]
    media_url: Annotated[
        str | None,
        Field(examples=["https://www.productimageurl.com"], default=None),
    ]
    created_by_user_id: int
    category_id: int
    created_at: datetime

class ProductCreate(ProductBase):
    model_config = ConfigDict(extra="forbid")

    media_url: Annotated[
        str | None,
        Field(pattern=r"^(https?|ftp)://[^\s/$.?#].[^\s]*$", examples=["https://www.postimageurl.com"], default=None),
    ]


class ProductCreateInternal(ProductCreate):
    created_by_user_id: int


class ProductUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: Annotated[str | None, Field(min_length=2, max_length=150, examples=["This is my updated product"], default=None)]
    description: Annotated[
        str | None,
        Field(min_length=1, max_length=63206, examples=["This is the updated description of this product."], default=None),
    ]
    category_id: Annotated[int | None, Field(examples=[1])]
    media_url: Annotated[
        str | None,
        Field(pattern=r"^(https?|ftp)://[^\s/$.?#].[^\s]*$", examples=["https://www.productimageurl.com"], default=None),
    ]


class ProductUpdateInternal(ProductUpdate):
    updated_at: datetime


class ProductDelete(BaseModel):
    model_config = ConfigDict(extra="forbid")

    is_deleted: bool
    deleted_at: datetime

class ProductRestoreDeleted(BaseModel):
    is_deleted: bool
