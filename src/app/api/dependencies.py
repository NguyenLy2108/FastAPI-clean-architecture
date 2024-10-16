from typing import Annotated, Any

from fastapi import Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from ..crud.crud_permissions import crud_permissions
from ..models.role_permission import RolePermission

from ..schemas.permission import  PermissionRead
from ..schemas.role_permission import RolePermissionRead

from ..core.db.database import async_get_db
from ..core.exceptions.http_exceptions import ForbiddenException, UnauthorizedException
from ..core.logger import logging
from ..core.security import oauth2_scheme, verify_token
from ..crud.crud_users import crud_users
from ..models.user import User

logger = logging.getLogger(__name__)

async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], db: Annotated[AsyncSession, Depends(async_get_db)]
) -> dict[str, Any] | None:
    token_data = await verify_token(token, db)
    if token_data is None:
        raise UnauthorizedException("User not authenticated.")

    if "@" in token_data.username_or_email:
        user: dict | None = await crud_users.get(db=db, email=token_data.username_or_email, is_deleted=False)
    else:
        user = await crud_users.get(db=db, username=token_data.username_or_email, is_deleted=False)

    if user:
        return user

    raise UnauthorizedException("User not authenticated.")


async def get_optional_user(request: Request, db: AsyncSession = Depends(async_get_db)) -> dict | None:
    token = request.headers.get("Authorization")
    if not token:
        return None

    try:
        token_type, _, token_value = token.partition(" ")
        if token_type.lower() != "bearer" or not token_value:
            return None

        token_data = await verify_token(token_value, db)
        if token_data is None:
            return None

        return await get_current_user(token_value, db=db)

    except HTTPException as http_exc:
        if http_exc.status_code != 401:
            logger.error(f"Unexpected HTTPException in get_optional_user: {http_exc.detail}")
        return None

    except Exception as exc:
        logger.error(f"Unexpected error in get_optional_user: {exc}")
        return None


async def get_current_superuser(current_user: Annotated[dict, Depends(get_current_user)]) -> dict:
    if not current_user["is_superuser"]:
        raise ForbiddenException("You do not have enough privileges.")

    return current_user


def requires_permission(permission_name: str):
    async def permission_checker(
        db: AsyncSession = Depends(async_get_db), 
        user: User | None = Depends(get_optional_user)
    ):
        user_permission: dict = await crud_permissions.get_joined(
            db=db,
            join_model=RolePermission,
            join_prefix="rp_",
            schema_to_select=PermissionRead,
            join_schema_to_select=RolePermissionRead,
            join_type="inner",
            role_id=user["role_id"], 
            name = permission_name,  
        ) 
        
        if user_permission is None:            
            raise HTTPException(status_code=403, detail="Not enough permissions")
       
    return permission_checker
