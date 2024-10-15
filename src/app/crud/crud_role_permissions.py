from fastcrud import FastCRUD

from ..models.role_permission import RolePermission
from ..schemas.role_permission import RolePermissionCreateInternal, RolePermissionDelete, RolePermissionUpdate, RolePermissionUpdateInternal

CRUDRolePermission = FastCRUD[RolePermission, RolePermissionCreateInternal, RolePermissionDelete, RolePermissionUpdate, RolePermissionUpdateInternal]
crud_role_permissions = CRUDRolePermission(RolePermission)
