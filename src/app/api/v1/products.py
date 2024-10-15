from typing import Annotated, Any

from fastapi import APIRouter, Depends, Request
from fastcrud.paginated import PaginatedListResponse, compute_offset, paginated_response
from sqlalchemy.ext.asyncio import AsyncSession

from ...api.dependencies import get_current_superuser, get_current_user, requires_permission
from ...core.db.database import async_get_db
from ...core.exceptions.http_exceptions import NotFoundException
from ...core.utils.cache import cache
from ...crud.crud_products import crud_products
from ...schemas.product import ProductCreate, ProductCreateInternal, ProductRead, ProductUpdate
from ...schemas.user import UserRead

router = APIRouter(tags=["products"])


@router.post(
    "/product", 
    response_model=ProductRead, 
    status_code=201, 
    dependencies=[Depends(requires_permission('product.create'))]
)
async def write_product(  
    product: ProductCreate,
    current_user: Annotated[UserRead, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(async_get_db)],   
) -> ProductRead:  
    product_internal_dict = product.model_dump()
    product_internal_dict["created_by_user_id"] = current_user["id"]

    post_internal = ProductCreateInternal(**product_internal_dict)
    created_product: ProductRead = await crud_products.create(db=db, object=post_internal)
    return created_product


@router.get("/products", response_model=PaginatedListResponse[ProductRead])
@cache(
    key_prefix="products:page_{page}:items_per_page:{items_per_page}",   
    expiration=60,
)
async def read_products(
    db: Annotated[AsyncSession, Depends(async_get_db)],
    page: int = 1,
    items_per_page: int = 10,
) -> dict:
    products_data = await crud_products.get_multi(
        db=db,
        offset=compute_offset(page, items_per_page),
        limit=items_per_page,
        schema_to_select=ProductRead,        
        is_deleted=False,
    )

    response: dict[str, Any] = paginated_response(crud_data=products_data, page=page, items_per_page=items_per_page)
    return response


@router.get("/product/{id}", response_model=ProductRead)
@cache(key_prefix="product_cache", resource_id_name="id")
async def read_product(
    request: Request, id: int, db: Annotated[AsyncSession, Depends(async_get_db)]
) -> dict:
    db_product: ProductRead | None = await crud_products.get(
        db=db, schema_to_select=ProductRead, id=id, is_deleted=False
    )
    if db_product is None:
        raise NotFoundException("Product not found")

    return db_product


@router.patch("/product/{id}", dependencies=[Depends(requires_permission('product.update'))])
@cache("product_cache", resource_id_name="id", pattern_to_invalidate_extra=["products:*"])
async def patch_post(   
    id: int,
    values: ProductUpdate,
    current_user: Annotated[UserRead, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(async_get_db)],
) -> dict[str, str]:
    db_product = await crud_products.get(db=db, schema_to_select=ProductRead, id=id, is_deleted=False)
    if db_product is None:
        raise NotFoundException("Product not found")

    await crud_products.update(db=db, object=values, id=id)
    return {"message": "Product updated"}


@router.delete("/product/{id}", dependencies=[Depends(requires_permission('product.delete'))])
@cache("product_cache", resource_id_name="id")
async def erase_product(   
    id: int,
    current_user: Annotated[UserRead, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(async_get_db)],
) -> dict[str, str]:    
    db_product = await crud_products.get(db=db, schema_to_select=ProductRead, id=id, is_deleted=False)
    if db_product is None:
        raise NotFoundException("Product not found")

    await crud_products.delete(db=db, id=id)

    return {"message": "Product deleted"}


@router.delete("/db_product/{id}", dependencies=[Depends(get_current_superuser)])
@cache("product_cache", resource_id_name="id")
async def erase_db_product(
    id: int, db: Annotated[AsyncSession, Depends(async_get_db)]
) -> dict[str, str]:    
    db_product = await crud_products.get(db=db, schema_to_select=ProductRead, id=id, is_deleted=False)
    if db_product is None:
        raise NotFoundException("Product not found")

    await crud_products.db_delete(db=db, id=id)
    return {"message": "Product deleted from the database"}
