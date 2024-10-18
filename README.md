<h1 align="center"> Clean architecture with FastAPI</h1>
 <a href="">
      <img src="https://blog.cleancoder.com/uncle-bob/images/2012-08-13-the-clean-architecture/CleanArchitecture.jpg" alt="Clean Architecture">
  </a>

This repo creates an extendable async API using FastAPI, Pydantic V2, SQLAlchemy 2.0 and PostgreSQL:

- [`FastAPI`](https://fastapi.tiangolo.com): modern Python web framework for building APIs
- [`Pydantic V2`](https://docs.pydantic.dev/2.4/): the most widely used data Python validation library, rewritten in Rust [`(5x-50x faster)`](https://docs.pydantic.dev/latest/blog/pydantic-v2-alpha/)
- [`SQLAlchemy 2.0`](https://docs.sqlalchemy.org/en/20/changelog/whatsnew_20.html): Python SQL toolkit and Object Relational Mapper
- [`PostgreSQL`](https://www.postgresql.org): The World's Most Advanced Open Source Relational Database
- [`Redis`](https://redis.io): Open source, in-memory data store used by millions as a cache, message broker and more.
- [`Docker Compose`](https://docs.docker.com/compose/) With a single command, create and start all the services from your configuration.
- [`NGINX`](https://nginx.org/en/) High-performance low resource consumption web server used for Reverse Proxy and Load Balancing.

# 1. Contents
1. [Contents](#1-contents)
1. [Project Structure with Clean Architecture](#2-project-tructure)
1. [Features](#3-features)
1. [Prerequisites](#4-prerequisites)
   1. [Clone repo](#41-clone-repo)
   1. [Environment Variables (.env)](#42-environment-variables-env)
   1. [Docker Compose](#43-docker-compose-preferred)
   1. [From Scratch](#44-from-scratch)
1. [Usage](#5-usage)
   1. [Docker Compose](#51-docker-compose)
   1. [From Scratch](#52-from-scratch)
      1. [Install Dependencis](#521-dependencies)
      1. [Running PostgreSQL, Redis With Docker](#522-running-postgresql-redis-with-docker)    
      1. [Running the API](#523-running-the-api)  
   1. [Database Migrations](#53-database-migrations)

# 2. Project Structure with Clean Architecture.
_Frameworks & Drivers: View, UI, ..._

_Interface Adapters:_ 

- src/app/main.py => core/setup.py: set up connection to Redis, PostgreSQL
- app/api/ => Analyze, build routers (controlers)
_Application Business Rules:_

- app/crud: build business logic 
_Enterprise Business Rules:_ 

- app/schemas, app/models: Create the new entities and relationships
    
_Project Structure_

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


# 4. Prerequisites
## 4.1 Clone repo:
```sh
git clone https://github.com/NguyenLy2108/FastAPI-clean-architecture.git
```
## 4.2 Environment variables (.env)
Create a .env file inside src directory.

_Create the following app settings variables_
```
# ------------- app settings -------------
APP_NAME="Your app name here"
APP_DESCRIPTION="Your app description here"
APP_VERSION="0.1"
CONTACT_NAME="Your name"
CONTACT_EMAIL="Your email"
LICENSE_NAME="The license you picked"
```

_For the database create:_

```
# ------------- database -------------
POSTGRES_USER="your_postgres_user"
POSTGRES_PASSWORD="your_password"
POSTGRES_SERVER="your_server" # default "localhost", if using docker compose you should use "db"
POSTGRES_PORT=5432 # default "5432", if using docker compose you should use "5432"
POSTGRES_DB="your_db"
```
_For redis caching:_

```
# ------------- redis cache-------------
REDIS_CACHE_HOST="your_host" # default "localhost", if using docker compose you should use "redis"
REDIS_CACHE_PORT=6379 # default "6379", if using docker compose you should use "6379"
```
_Secret key to encrypt token:_
```
# ------------- encrypt -------------
SECRET_KEY= # result of openssl rand -hex 32
ALGORITHM= # pick an algorithm, default HS256
ACCESS_TOKEN_EXPIRE_MINUTES= # minutes until token expires, default 30
REFRESH_TOKEN_EXPIRE_DAYS= # days until token expires, default 7
```
## 4.3 Docker Compose

_Install docker, docker compose if you don't have it yet_[Click here](https://docs.docker.com/)

_Check docker, docker-compose version on terminal_
```sh
docker --version
docker-compose --version
```

## 4.4 From Scartch
_Install poetry:_

```sh
pip install poetry
```

_**If you don't have database yet (postgre or redis)? you can create with docker.**_

_Ensure you have docker, Install docker if you don't have it yet_

- Create and run postgre with docker:

```sh
docker pull postgres
```

And pick the port, name, user and password, replacing the fields:

```sh
docker run -d \
    -p {PORT}:{PORT} \
    --name {NAME} \
    -e POSTGRES_PASSWORD={PASSWORD} \
    -e POSTGRES_USER={USER} \
    postgres
```

Such as:

```sh
docker run -d \
    -p 5432:5432 \
    --name postgres \
    -e POSTGRES_PASSWORD=1234 \
    -e POSTGRES_USER=postgres \
    postgres
```

- Create and run redis with docker:
```sh
docker pull redis:alpine
```

And pick the name and port, replacing the fields:

```sh
docker run -d \
  --name {NAME}  \
  -p {PORT}:{PORT} \
redis:alpine
```

Such as

```sh
docker run -d \
  --name redis  \
  -p 6379:6379 \
redis:alpine
```

# 5. Usage

## 5.1 Docker Compose
If your setup is done. You just need to ensure that when you run (while in the base folder):

```sh
docker compose up
```

And get the following outputs:

```sh
fastapi-clean-architecture-api-1    | INFO:     Will watch for changes in these directories: ['/code']
fastapi-clean-architecture-api-1    | INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)   
fastapi-clean-architecture-api-1    | INFO:     Started reloader process [1] using StatReload
fastapi-clean-architecture-api-1    | INFO:     Started server process [8]
fastapi-clean-architecture-api-1    | INFO:     Waiting for application startup.
fastapi-clean-architecture-api-1    | INFO:     Application startup complete.
```
You can click (http://localhost/docs) to see swagger_documentation
## 5.2 From Scratch
### 5.2.1 Install dependencies:

```sh
poetry install
```

### 5.2.2 Running PostgreSQL and Redis with Docker.
_Check if the postgre database and redis are running; if not, please start them with Docker and image name._

```sh
docker run -t <image_name> .
```
### 5.2.3 Running the API:

```sh
poetry run uvicorn src.app.main:app --reload
```
And get the following outputs on terminal:
```sh
PS E:\Visualcode\FastAPI-clean-architecture> poetry run uvicorn src.app.main:app --reload
INFO:     Will watch for changes in these directories: ['E:\\Visualcode\\FastAPI-clean-architecture']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [25320] using StatReload
```
And you can click (http://127.0.0.1:8000) to see swagger_documentation

## 5.3 Database Migrations

To create the tables if you did not create the endpoints, ensure that you import the models in src/app/models/__init__.py. This step is crucial to create the new tables.

While in the `src` folder, run Alembic migrations:

```sh
poetry run alembic revision --autogenerate
```

And to apply the migration

```sh
poetry run alembic upgrade head
```