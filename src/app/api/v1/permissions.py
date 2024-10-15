from typing import Annotated, Any

from fastapi import APIRouter, Depends, Request
from fastcrud.paginated import PaginatedListResponse, compute_offset, paginated_response
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.crud.crud_roles import crud_roles
from src.app.models.role_permission import RolePermission

from src.app.schemas.role import Role, RoleRead
from src.app.schemas.role_permission import RolePermissionRead

from ...api.dependencies import get_current_superuser
from ...core.db.database import async_get_db
from ...core.exceptions.http_exceptions import DuplicateValueException, NotFoundException
from ...crud.crud_permissions import crud_permissions
from ...schemas.permission import PermissionCreate, PermissionCreateInternal, PermissionRead, PermissionUpdate

router = APIRouter(tags=["permissions"])


@router.post("/permission", dependencies=[Depends(get_current_superuser)], status_code=201)
async def write_permission(
    request: Request, permission: PermissionCreate, db: Annotated[AsyncSession, Depends(async_get_db)]
) -> PermissionRead:
    permission_internal_dict = permission.model_dump()
    db_permission = await crud_permissions.exists(db=db, name=permission_internal_dict["name"])
    if db_permission:
        raise DuplicateValueException("Permission Name not available")

    permission_internal = PermissionCreateInternal(**permission_internal_dict)
    created_permission: PermissionRead = await crud_permissions.create(db=db, object=permission_internal)
    return created_permission


@router.get("/permissions", response_model=PaginatedListResponse[PermissionRead])
async def read_permissions(
    request: Request, db: Annotated[AsyncSession, Depends(async_get_db)], page: int = 1, items_per_page: int = 10
) -> dict:
    permissions_data = await crud_permissions.get_multi(
        db=db, offset=compute_offset(page, items_per_page), limit=items_per_page, schema_to_select=PermissionRead
    )

    response: dict[str, Any] = paginated_response(crud_data=permissions_data, page=page, items_per_page=items_per_page)
    return response


@router.get("/permission/{name}", response_model=PermissionRead)
async def read_permission(request: Request, name: str, db: Annotated[AsyncSession, Depends(async_get_db)]) -> dict:
    db_permission: PermissionRead | None = await crud_permissions.get(db=db, schema_to_select=PermissionRead, name=name)
    if db_permission is None:
        raise NotFoundException("Permission not found")

    return db_permission


@router.get("/permissions/{role_id}/role")
async def read_permissions_by_role_id(
    request: Request, role_id: int, db: Annotated[AsyncSession, Depends(async_get_db)]
) -> dict | None:
    db_role = await crud_roles.get(db=db, id=role_id, schema_to_select=RoleRead)
    if db_role is None:
        raise NotFoundException("Role not found")    

    joined: dict = await crud_permissions.get_multi_joined(
        db=db,
        join_model=RolePermission,
        join_prefix="rp_",
        schema_to_select=PermissionRead,
        join_schema_to_select=RolePermissionRead,
        role_id=role_id,
        sort_columns="rp.id",
        sort_orders="asc",
    )

    return joined



@router.patch("/permission/{name}", dependencies=[Depends(get_current_superuser)])
async def patch_permission(
    request: Request, values: PermissionUpdate, name: str, db: Annotated[AsyncSession, Depends(async_get_db)]
) -> dict[str, str]:
    db_permission = await crud_permissions.get(db=db, schema_to_select=PermissionRead, name=name)
    if db_permission is None:
        raise NotFoundException("Permission not found")

    await crud_permissions.update(db=db, object=values, name=name)
    return {"message": "Permission updated"}


@router.delete("/permission/{name}", dependencies=[Depends(get_current_superuser)])
async def erase_permission(request: Request, name: str, db: Annotated[AsyncSession, Depends(async_get_db)]) -> dict[str, str]:
    db_permission = await crud_permissions.get(db=db, schema_to_select=PermissionRead, name=name)
    if db_permission is None:
        raise NotFoundException("Permission not found")

    await crud_permissions.delete(db=db, name=name)
    return {"message": "Permission deleted"}
