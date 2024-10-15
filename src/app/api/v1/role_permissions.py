from typing import Annotated

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.schemas.role import RoleRead

from ...api.dependencies import get_current_superuser
from ...core.db.database import async_get_db
from ...core.exceptions.http_exceptions import DuplicateValueException, NotFoundException
from ...crud.crud_role_permissions import crud_role_permissions
from ...schemas.role_permission import RolePermissionCreate, RolePermissionCreateInternal, RolePermissionRead

router = APIRouter(tags=["role_permissions"])


@router.post("/role_permission", dependencies=[Depends(get_current_superuser)], status_code=201)
async def write_role_permission(
    request: Request, role_permission: RolePermissionCreate, db: Annotated[AsyncSession, Depends(async_get_db)]
) -> RolePermissionRead:
    role_permission_internal_dict = role_permission.model_dump()
    db_role_permission = await crud_role_permissions.exists(
        db=db, 
        role_id=role_permission_internal_dict["role_id"], 
        permission_id=role_permission_internal_dict["permission_id"]
    )
    if db_role_permission:
        raise DuplicateValueException("Role Permission not available")

    role_permission_internal = RolePermissionCreateInternal(**role_permission_internal_dict)
    created_role_permission: RolePermissionRead = await crud_role_permissions.create(db=db, object=role_permission_internal)
    return created_role_permission
    

@router.delete("/role_permission/{id}", dependencies=[Depends(get_current_superuser)])
async def erase_role_permission(request: Request, id: int, db: Annotated[AsyncSession, Depends(async_get_db)]) -> dict[str, str]:
    db_role_permission = await crud_role_permissions.get(db=db, schema_to_select=RoleRead, id=id)
    if db_role_permission is None:
        raise NotFoundException("Role Permission not found")

    await crud_role_permissions.delete(db=db, id=id)
    return {"message": "Role Permission deleted"}
