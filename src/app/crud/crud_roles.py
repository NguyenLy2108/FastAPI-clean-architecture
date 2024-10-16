from fastcrud import FastCRUD

from ..models.role import Role
from ..schemas.role import RoleCreateInternal, RoleDelete, RoleUpdate, RoleUpdateInternal

CRUDRole = FastCRUD[Role, RoleCreateInternal, RoleUpdate, RoleUpdateInternal, RoleDelete]
crud_roles = CRUDRole(Role)
