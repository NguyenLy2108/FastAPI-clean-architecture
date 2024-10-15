# 1. Clean Architecture System Design
 <a href="">
      <img src="https://blog.cleancoder.com/uncle-bob/images/2012-08-13-the-clean-architecture/CleanArchitecture.jpg" alt="Clean Architecture">
  </a>

_Frameworks & Drivers: View, UI, ..._
_Interface Adapters:_ 
- src/app/main.py => core/setup.py: set up connection to Redis, PostgreSQL
- app/api/ => Analyze, build routers (controlers)
_Application Business Rules:_ 
- app/crud: build business logic 
_Enterprise Business Rules:_ 
- app/schemas, app/models: Create the new entities and relationships
    
# 2. Project Structure

```sh
.
├── Dockerfile                          # Dockerfile for building the application container.
├── docker-compose.yml                  # Docker Compose file for defining multi-container applications.
├── pyproject.toml                      # Poetry configuration file with project metadata and dependencies.
├── README.md                           # Project README providing information and instructions.
├── LICENSE.md                          # License file for the project.
│
├── tests                               # Unit and integration tests for the application.
│   ├──helpers                          # Helper functions for tests.
│   │   ├── generators.py               # Helper functions for generating test data.
│   │   └── mocks.py                    # Mock function for testing.
│   ├── __init__.py
│   ├── conftest.py                     # Configuration and fixtures for pytest.
│   └── test_user.py                    # Test cases for user-related functionality.
│
└── src                                 # Source code directory.
    ├── __init__.py                     # Initialization file for the src package.
    ├── alembic.ini                     # Configuration file for Alembic (database migration tool).
    ├── poetry.lock                     # Poetry lock file specifying exact versions of dependencies.
    │
    ├── app                             # Main application directory.
    │   ├── __init__.py                 # Initialization file for the app package.
    │   ├── main.py                     # Main entry point of the FastAPI application.
    │   │
    │   │
    │   ├── api                         # Folder containing API-related logic.
    │   │   ├── __init__.py
    │   │   ├── dependencies.py         # Defines dependencies for use across API endpoints (auth, permission)
    │   │   │
    │   │   └── v1                      # Version 1 of the API.
    │   │       ├── __init__.py
    │   │       ├── categories.py       # API route for category of products.
    │   │       ├── login.py            # API route for user login.
    │   │       ├── logout.py           # API route for user logout.
    │   │       ├── permissions.py      # API routes for permission management.
    │   │       ├── products.py         # API routes for product operations..
    │   │       ├── role_permissions.py # API routes for role permission management.
    │   │       ├── roles.py            # API routes for user role functionalities.
    │   │       └── users.py            # API routes for user management.
    │   │
    │   ├── core                        # Core utilities and configurations for the application.
    │   │   ├── __init__.py
    │   │   ├── config.py               # Configuration settings for the application.
    │   │   ├── logger.py               # Configuration for application logging.
    │   │   ├── schemas.py              # Pydantic schemas for data validation.
    │   │   ├── security.py             # Security utilities, such as password hashing.
    │   │   ├── setup.py                # Setup file for the FastAPI app instance.
    │   │   │
    │   │   ├── db                      # Core Database related modules.
    │   │   │   ├── __init__.py
    │   │   │   ├── crud_token_blacklist.py  # CRUD operations for token blacklist.
    │   │   │   ├── database.py         # Database connectivity and session management.
    │   │   │   ├── models.py           # Core Database models.
    │   │   │   └── token_blacklist.py  # Model for token blacklist functionality.
    │   │   │
    │   │   ├── exceptions              # Custom exception classes.
    │   │   │   ├── __init__.py
    │   │   │   ├── cache_exceptions.py # Exceptions related to cache operations.
    │   │   │   └── http_exceptions.py  # HTTP-related exceptions. 
    │   │   │
    │   │   └── utils                   #  Utility functions and helpers.
    │   │       ├── __init__.py 
    │   │       └── cache.py            # Cache-related utilities.
    │   │
    │   ├── crud                        # CRUD operations for the application.
    │   │   ├── __init__.py
    │   │   ├── crud_categories.py      # CRUD operations for categories.
    │   │   ├── crud_permissions.py     # CRUD operations for permissions.
    │   │   ├── crud_products.py        # CRUD operations for products.
    │   │   ├── crud_role_permissions.py # CRUD operations for role permissions.
    │   │   ├── crud_roles.py           # CRUD operations for roles.
    │   │   └── crud_users.py           # CRUD operations for users.
    │   │
    │   ├── logs                        # Directory for log files.
    │   │   └── app.log                 # Log file for the application.
    │   │
    │   ├── middleware                  # Middleware components for the application.
    │   │   └── client_cache_middleware.py  # Middleware for client-side caching.
    │   │
    │   ├── models                      # ORM models for the application.
    │   │   ├── __init__.py
    │   │   ├── category.py             # ORM model for categories.
    │   │   ├── permission.py           # ORM model for permissions.
    │   │   ├── product.py              # ORM model for products.
    │   │   ├── role_permission.py      # ORM model for role permissions.
    │   │   ├── role.py                 # ORM model for roles.
    │   │   └── user.py                 # ORM model for users.
    │   │
    │   └── schemas                     # Pydantic schemas for data validation.
    │       ├── __init__.py
    │       ├── category.py             # Schema for category.
    │       ├── permission.py           # Schema for permission data.
    │       ├── product.py              # Schema for product data.
    │       ├── role_permission.py      # Schema for role permission data.
    │       └── role.py                 # Schema for user data.
    │       └── user.py                 # Schema for user data.
    │
    ├── migrations                      # Alembic migration scripts for database changes.
    │   ├── README
    │   ├── env.py                      # Environment configuration for Alembic.
    │   ├── script.py.mako              # Template script for Alembic migrations.
    │   │
    │   └── versions                    # Individual migration scripts.
    │       └── README.MD
    │
    └── scripts                         # Utility scripts for the application.
        ├── __init__.py
        ├── create_first_superuser.py   # Script to create the first superuser.
        └── create_first_role.py        # Script to create the first user role.
```

# 3. Features.
- User Management API: crud, read user with role,..
- Role, Permission Management API
- Product, Category Management API
- Authorization: use dependencies "get_current_user" to check user from jwt token and "requires_permission" to check access permission from role.
```python
...
@router.post(
    "/{username}/product", 
    response_model=ProductRead, 
    status_code=201, 
    dependencies=[Depends(requires_permission('product.create'))]
)
async def write_product(
    request: Request,
    username: str,
    product: ProductCreate,
    current_user: Annotated[UserRead, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(async_get_db)],   
) -> ProductRead:
    db_user = await crud_users.get(db=db, schema_to_select=UserRead, username=username, is_deleted=False)
    if db_user is None:
        raise NotFoundException("User not found")

    if current_user["id"] != db_user["id"]:
        raise ForbiddenException()

    product_internal_dict = product.model_dump()
    product_internal_dict["created_by_user_id"] = db_user["id"]

    post_internal = ProductCreateInternal(**product_internal_dict)
    created_product: ProductRead = await crud_products.create(db=db, object=post_internal)
    return created_product
```
requires_permission function
```python
...
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
```

# 4. Run
Create a .env file inside src directory:
## 4.1 Docker Compose
```sh
docker compose up
```
## 4.2 From Scratch
Install poetry:

```sh
pip install poetry
```
Install packages:

```sh
poetry install
```
Run API:

```sh
poetry run uvicorn src.app.main:app --reload
```
## 4.3 Use pip
Install packages:

```sh
pip install -r requirement.txt
```
Run API:

```sh
python -m uvicorn src.app.main:app --reload
```