from fastcrud import FastCRUD

from ..models.permission import Permission
from ..schemas.permission import PermissionCreateInternal, PermissionDelete, PermissionUpdate, PermissionUpdateInternal

CRUDPermission = FastCRUD[Permission, PermissionCreateInternal, PermissionUpdate, PermissionUpdateInternal, PermissionDelete]
crud_permissions = CRUDPermission(Permission)
