from fastapi import APIRouter

from .login import router as login_router
from .logout import router as logout_router
from .users import router as users_router
from .products import router as products_router
from .categories import router as categories_router
from .roles import router as roles_router
from .permissions import router as permissions_router
from .role_permissions import router as role_permissions_router

router = APIRouter(prefix="/v1")
router.include_router(login_router)
router.include_router(logout_router)
router.include_router(users_router)
router.include_router(products_router)
router.include_router(categories_router)
router.include_router(roles_router)
router.include_router(permissions_router)
router.include_router(role_permissions_router)
