from typing import Annotated, Any

from fastapi import APIRouter, Depends, Request
from fastcrud.paginated import PaginatedListResponse, compute_offset, paginated_response
from sqlalchemy.ext.asyncio import AsyncSession

from ...api.dependencies import get_current_superuser
from ...core.db.database import async_get_db
from ...core.exceptions.http_exceptions import DuplicateValueException, NotFoundException
from ...crud.crud_roles import crud_roles   
from ...schemas.role import RoleCreate, RoleCreateInternal, RoleRead, RoleUpdate

router = APIRouter(tags=["roles"])


@router.post("/role", dependencies=[Depends(get_current_superuser)], status_code=201)
async def write_role(
    request: Request, role: RoleCreate, db: Annotated[AsyncSession, Depends(async_get_db)]
) -> RoleRead:
    role_internal_dict = role.model_dump()
    db_role = await crud_roles.exists(db=db, name=role_internal_dict["name"])
    if db_role:
        raise DuplicateValueException("Role Name not available")

    role_internal = RoleCreateInternal(**role_internal_dict)
    created_role: RoleRead = await crud_roles.create(db=db, object=role_internal)
    return created_role


@router.get("/roles", response_model=PaginatedListResponse[RoleRead])
async def read_roles(
    request: Request, db: Annotated[AsyncSession, Depends(async_get_db)], page: int = 1, items_per_page: int = 10
) -> dict:
    roles_data = await crud_roles.get_multi(
        db=db, offset=compute_offset(page, items_per_page), limit=items_per_page, schema_to_select=RoleRead
    )

    response: dict[str, Any] = paginated_response(crud_data=roles_data, page=page, items_per_page=items_per_page)
    return response


@router.get("/role/{name}", response_model=RoleRead)
async def read_role(request: Request, name: str, db: Annotated[AsyncSession, Depends(async_get_db)]) -> dict:
    db_role: RoleRead | None = await crud_roles.get(db=db, schema_to_select=RoleRead, name=name)
    if db_role is None:
        raise NotFoundException("Role not found")

    return db_role


@router.patch("/role/{name}", dependencies=[Depends(get_current_superuser)])
async def patch_role(
    request: Request, values: RoleUpdate, name: str, db: Annotated[AsyncSession, Depends(async_get_db)]
) -> dict[str, str]:
    db_role = await crud_roles.get(db=db, schema_to_select=RoleRead, name=name)
    if db_role is None:
        raise NotFoundException("Role not found")

    await crud_roles.update(db=db, object=values, name=name)
    return {"message": "Role updated"}


@router.delete("/role/{name}", dependencies=[Depends(get_current_superuser)])
async def erase_role(request: Request, name: str, db: Annotated[AsyncSession, Depends(async_get_db)]) -> dict[str, str]:
    db_role = await crud_roles.get(db=db, schema_to_select=RoleRead, name=name)
    if db_role is None:
        raise NotFoundException("Role not found")

    await crud_roles.delete(db=db, name=name)
    return {"message": "Role deleted"}
