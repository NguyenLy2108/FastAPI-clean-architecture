from typing import Annotated, Any

from fastapi import APIRouter, Depends, Request
from fastcrud.paginated import PaginatedListResponse, compute_offset, paginated_response
from sqlalchemy.ext.asyncio import AsyncSession

from ...api.dependencies import get_current_superuser
from ...core.db.database import async_get_db
from ...core.exceptions.http_exceptions import DuplicateValueException, NotFoundException
from ...crud.crud_categories import crud_categories
from ...schemas.category import CategoryCreate, CategoryCreateInternal, CategoryRead, CategoryUpdate

router = APIRouter(tags=["categories"])


@router.post("/category", dependencies=[Depends(get_current_superuser)], status_code=201)
async def write_category(
    request: Request, category: CategoryCreate, db: Annotated[AsyncSession, Depends(async_get_db)]
) -> CategoryRead:
    category_internal_dict = category.model_dump()
    db_category = await crud_categories.exists(db=db, name=category_internal_dict["name"])
    if db_category:
        raise DuplicateValueException("Category Name not available")

    category_internal = CategoryCreateInternal(**category_internal_dict)
    created_category: CategoryRead = await crud_categories.create(db=db, object=category_internal)
    return created_category


@router.get("/categories", response_model=PaginatedListResponse[CategoryRead])
async def read_categories(
    request: Request, db: Annotated[AsyncSession, Depends(async_get_db)], page: int = 1, items_per_page: int = 10
) -> dict:
    categories_data = await crud_categories.get_multi(
        db=db, offset=compute_offset(page, items_per_page), limit=items_per_page, schema_to_select=CategoryRead
    )

    response: dict[str, Any] = paginated_response(crud_data=categories_data, page=page, items_per_page=items_per_page)
    return response


@router.get("/category/{name}", response_model=CategoryRead)
async def read_category(request: Request, name: str, db: Annotated[AsyncSession, Depends(async_get_db)]) -> dict:
    db_category: CategoryRead | None = await crud_categories.get(db=db, schema_to_select=CategoryRead, name=name)
    if db_category is None:
        raise NotFoundException("Category not found")

    return db_category


@router.patch("/category/{name}", dependencies=[Depends(get_current_superuser)])
async def patch_category(
    request: Request, values: CategoryUpdate, name: str, db: Annotated[AsyncSession, Depends(async_get_db)]
) -> dict[str, str]:
    db_category = await crud_categories.get(db=db, schema_to_select=CategoryRead, name=name)
    if db_category is None:
        raise NotFoundException("Category not found")

    await crud_categories.update(db=db, object=values, name=name)
    return {"message": "Category updated"}


@router.delete("/category/{name}", dependencies=[Depends(get_current_superuser)])
async def erase_category(request: Request, name: str, db: Annotated[AsyncSession, Depends(async_get_db)]) -> dict[str, str]:
    db_category = await crud_categories.get(db=db, schema_to_select=CategoryRead, name=name)
    if db_category is None:
        raise NotFoundException("Category not found")

    await crud_categories.delete(db=db, name=name)
    return {"message": "Category deleted"}
