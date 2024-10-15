# 1. Clean Architecture System Design
 <a href="">
      <img src="https://blog.cleancoder.com/uncle-bob/images/2012-08-13-the-clean-architecture/CleanArchitecture.jpg" alt="Clean Architecture">
  </a>

Frameworks & Drivers: View, UI, ...
Interface Adapters: 
- src/app/main.py => core/setup.py: set up connection to Redis, PostgreSQL
- app/api/ => Analyze, build routers (controlers)
Application Business Rules: 
- app/crud: build business logic 
Enterprise Business Rules: 
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
    │   │   ├── logger.py             # Configuration for application logging.
    │   │   ├── schemas.py            # Pydantic schemas for data validation.
    │   │   ├── security.py           # Security utilities, such as password hashing.
    │   │   ├── setup.py              # Setup file for the FastAPI app instance.
    │   │   │
    │   │   ├── db                    # Core Database related modules.
    │   │   │   ├── __init__.py
    │   │   │   ├── crud_token_blacklist.py  # CRUD operations for token blacklist.
    │   │   │   ├── database.py       # Database connectivity and session management.
    │   │   │   ├── models.py         # Core Database models.
    │   │   │   └── token_blacklist.py  # Model for token blacklist functionality.
    │   │   │
    │   │   ├── exceptions            # Custom exception classes.
    │   │   │   ├── __init__.py
    │   │   │   ├── cache_exceptions.py   # Exceptions related to cache operations.
    │   │   │   └── http_exceptions.py    # HTTP-related exceptions.
    │   │   │
    │   │   ├── utils                 # Utility functions and helpers.
    │   │   │   ├── __init__.py
    │   │   │   ├── cache.py          # Cache-related utilities.
    │   │   │   ├── queue.py          # Utilities for task queue management.
    │   │   │   └── rate_limit.py     # Rate limiting utilities.
    │   │   │
    │   │   └── worker                # Worker script for background tasks.
    │   │       ├── __init__.py
    │   │       ├── settings.py       # Worker configuration and settings.
    │   │       └── functions.py      # Async task definitions and management.
    │   │
    │   ├── crud                      # CRUD operations for the application.
    │   │   ├── __init__.py
    │   │   ├── crud_categories.py    # CRUD operations for categories.
    │   │   ├── crud_permissions.py   # CRUD operations for permissions.
    │   │   ├── crud_products.py      # CRUD operations for products.
    │   │   ├── crud_role_permissions.py # CRUD operations for role permissions.
    │   │   ├── crud_roles.py         # CRUD operations for roles.
    │   │   └── crud_users.py         # CRUD operations for users.
    │   │
    │   ├── logs                      # Directory for log files.
    │   │   └── app.log               # Log file for the application.
    │   │
    │   ├── middleware                # Middleware components for the application.
    │   │   └── client_cache_middleware.py  # Middleware for client-side caching.
    │   │
    │   ├── models                    # ORM models for the application.
    │   │   ├── __init__.py
    │   │   ├── category.py           # ORM model for categories.
    │   │   ├── permission.py         # ORM model for permissions.
    │   │   ├── product.py            # ORM model for products.
    │   │   ├── role_permission.py    # ORM model for role permissions.
    │   │   ├── role.py               # ORM model for roles.
    │   │   └── user.py               # ORM model for users.
    │   │
    │   └── schemas                   # Pydantic schemas for data validation.
    │       ├── __init__.py
    │       ├── category.py           # Schema for category.
    │       ├── permission.py         # Schema for permission data.
    │       ├── product.py            # Schema for product data.
    │       ├── role_permission.py    # Schema for role permission data.
    │       └── role.py               # Schema for user data.
    │       └── user.py               # Schema for user data.
    │
    ├── migrations                    # Alembic migration scripts for database changes.
    │   ├── README
    │   ├── env.py                    # Environment configuration for Alembic.
    │   ├── script.py.mako            # Template script for Alembic migrations.
    │   │
    │   └── versions                  # Individual migration scripts.
    │       └── README.MD
    │
    └── scripts                       # Utility scripts for the application.
        ├── __init__.py
        ├── create_first_superuser.py # Script to create the first superuser.
        └── create_first_role.py      # Script to create the first user role.
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

# 4. Caching

The `cache` decorator allows you to cache the results of FastAPI endpoint functions, enhancing response times and reducing the load on your application by storing and retrieving data in a cache.

Caching the response of an endpoint is really simple, just apply the `cache` decorator to the endpoint function.

> \[!WARNING\]
> Note that you should always pass request as a variable to your endpoint function if you plan to use the cache decorator.

```python
...
from app.core.utils.cache import cache


@app.get("/sample/{my_id}")
@cache(key_prefix="sample_data", expiration=3600, resource_id_name="my_id")
async def sample_endpoint(request: Request, my_id: int):
    # Endpoint logic here
    return {"data": "my_data"}
```

The way it works is:

- the data is saved in redis with the following cache key: `sample_data:{my_id}`
- then the time to expire is set as 3600 seconds (that's the default)

Another option is not passing the `resource_id_name`, but passing the `resource_id_type` (default int):

```python
...
from app.core.utils.cache import cache


@app.get("/sample/{my_id}")
@cache(key_prefix="sample_data", resource_id_type=int)
async def sample_endpoint(request: Request, my_id: int):
    # Endpoint logic here
    return {"data": "my_data"}
```

In this case, what will happen is:

- the `resource_id` will be inferred from the keyword arguments (`my_id` in this case)
- the data is saved in redis with the following cache key: `sample_data:{my_id}`
- then the the time to expire is set as 3600 seconds (that's the default)

Passing resource_id_name is usually preferred.

### 5.9 More Advanced Caching

The behaviour of the `cache` decorator changes based on the request method of your endpoint.
It caches the result if you are passing it to a **GET** endpoint, and it invalidates the cache with this key_prefix and id if passed to other endpoints (**PATCH**, **DELETE**).

#### Invalidating Extra Keys

If you also want to invalidate cache with a different key, you can use the decorator with the `to_invalidate_extra` variable.

In the following example, I want to invalidate the cache for a certain `user_id`, since I'm deleting it, but I also want to invalidate the cache for the list of users, so it will not be out of sync.

```python
# The cache here will be saved as "{username}_posts:{username}":
@router.get("/{username}/posts", response_model=List[PostRead])
@cache(key_prefix="{username}_posts", resource_id_name="username")
async def read_posts(request: Request, username: str, db: Annotated[AsyncSession, Depends(async_get_db)]):
    ...


...

# Invalidating cache for the former endpoint by just passing the key_prefix and id as a dictionary:
@router.delete("/{username}/post/{id}")
@cache(
    "{username}_post_cache",
    resource_id_name="id",
    to_invalidate_extra={"{username}_posts": "{username}"},  # also invalidate "{username}_posts:{username}" cache
)
async def erase_post(
    request: Request,
    username: str,
    id: int,
    current_user: Annotated[UserRead, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(async_get_db)],
):
    ...


# And now I'll also invalidate when I update the user:
@router.patch("/{username}/post/{id}", response_model=PostRead)
@cache("{username}_post_cache", resource_id_name="id", to_invalidate_extra={"{username}_posts": "{username}"})
async def patch_post(
    request: Request,
    username: str,
    id: int,
    values: PostUpdate,
    current_user: Annotated[UserRead, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(async_get_db)],
):
    ...
```

> \[!WARNING\]
> Note that adding `to_invalidate_extra` will not work for **GET** requests.

#### Invalidate Extra By Pattern

Let's assume we have an endpoint with a paginated response, such as:

```python
@router.get("/{username}/posts", response_model=PaginatedListResponse[PostRead])
@cache(
    key_prefix="{username}_posts:page_{page}:items_per_page:{items_per_page}",
    resource_id_name="username",
    expiration=60,
)
async def read_posts(
    request: Request,
    username: str,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    page: int = 1,
    items_per_page: int = 10,
):
    db_user = await crud_users.get(db=db, schema_to_select=UserRead, username=username, is_deleted=False)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    posts_data = await crud_posts.get_multi(
        db=db,
        offset=compute_offset(page, items_per_page),
        limit=items_per_page,
        schema_to_select=PostRead,
        created_by_user_id=db_user["id"],
        is_deleted=False,
    )

    return paginated_response(crud_data=posts_data, page=page, items_per_page=items_per_page)
```

Just passing `to_invalidate_extra` will not work to invalidate this cache, since the key will change based on the `page` and `items_per_page` values.
To overcome this we may use the `pattern_to_invalidate_extra` parameter:

```python
@router.patch("/{username}/post/{id}")
@cache("{username}_post_cache", resource_id_name="id", pattern_to_invalidate_extra=["{username}_posts:*"])
async def patch_post(
    request: Request,
    username: str,
    id: int,
    values: PostUpdate,
    current_user: Annotated[UserRead, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(async_get_db)],
):
    ...
```

Now it will invalidate all caches with a key that matches the pattern `"{username}_posts:*`, which will work for the paginated responses.

> \[!CAUTION\]
> Using `pattern_to_invalidate_extra` can be resource-intensive on large datasets. Use it judiciously and consider the potential impact on Redis performance. Be cautious with patterns that could match a large number of keys, as deleting many keys simultaneously may impact the performance of the Redis server.

#### Client-side Caching

For `client-side caching`, all you have to do is let the `Settings` class defined in `app/core/config.py` inherit from the `ClientSideCacheSettings` class. You can set the `CLIENT_CACHE_MAX_AGE` value in `.env,` it defaults to 60 (seconds).

### 5.10 ARQ Job Queues

Depending on the problem your API is solving, you might want to implement a job queue. A job queue allows you to run tasks in the background, and is usually aimed at functions that require longer run times and don't directly impact user response in your frontend. As a rule of thumb, if a task takes more than 2 seconds to run, can be executed asynchronously, and its result is not needed for the next step of the user's interaction, then it is a good candidate for the job queue.

> [!TIP]
> Very common candidates for background functions are calls to and from LLM endpoints (e.g. OpenAI or Openrouter). This is because they span tens of seconds and often need to be further parsed and saved.

#### Background task creation

For simple background tasks, you can just create a function in the `app/core/worker/functions.py` file. For more complex tasks, we recommend you to create a new file in the `app/core/worker` directory.

```python
async def sample_background_task(ctx, name: str) -> str:
    await asyncio.sleep(5)
    return f"Task {name} is complete!"
```

Then add the function to the `WorkerSettings` class `functions` variable in `app/core/worker/settings.py` to make it available to the worker. If you created a new file in the `app/core/worker` directory, then simply import this function in the `app/core/worker/settings.py` file:

```python
from .functions import sample_background_task
from .your_module import sample_complex_background_task

class WorkerSettings:
    functions = [sample_background_task, sample_complex_background_task]
    ...
```

#### Add the task to an endpoint

Once you have created the background task, you can add it to any endpoint of your choice to be enqueued. The best practice is to enqueue the task in a **POST** endpoint, while having a **GET** endpoint to get more information on the task. For more details on how job results are handled, check the [ARQ docs](https://arq-docs.helpmanual.io/#job-results).

```python
@router.post("/task", response_model=Job, status_code=201)
async def create_task(message: str):
    job = await queue.pool.enqueue_job("sample_background_task", message)
    return {"id": job.job_id}


@router.get("/task/{task_id}")
async def get_task(task_id: str):
    job = ArqJob(task_id, queue.pool)
    return await job.info()
```

And finally run the worker in parallel to your fastapi application.

> [!IMPORTANT]
> For any change to the `sample_background_task` to be reflected in the worker, you need to restart the worker (e.g. the docker container).

If you are using `docker compose`, the worker is already running.
If you are doing it from scratch, run while in the `root` folder:

```sh
poetry run arq src.app.core.worker.settings.WorkerSettings
```

#### Database session with background tasks

With time your background functions will become 'workflows' increasing in complexity and requirements. Probably, you will need to use a database session to get, create, update, or delete data as part of this workflow.

To do this, you can add the database session to the `ctx` object in the `startup` and `shutdown` functions in `app/core/worker/functions.py`, like in the example below:

```python
from arq.worker import Worker
from ...core.db.database import async_get_db

async def startup(ctx: Worker) -> None:
    ctx["db"] = await anext(async_get_db())
    logging.info("Worker Started")


async def shutdown(ctx: Worker) -> None:
    await ctx["db"].close()
    logging.info("Worker end")
```

This will allow you to have the async database session always available in any background function and automatically close it on worker shutdown. Once you have this database session, you can use it as follows:

```python
from arq.worker import Worker

async def your_background_function(
    ctx: Worker,
    post_id: int,
    ...
) -> Any:
    db = ctx["db"]
    post = crud_posts.get(db=db, schema_to_select=PostRead, id=post_id)
    ...
```

> [!WARNING]
> When using database sessions, you will want to use Pydantic objects. However, these objects don't mingle well with the seralization required by ARQ tasks and will be retrieved as a dictionary.

### 5.11 Rate Limiting

To limit how many times a user can make a request in a certain interval of time (very useful to create subscription plans or just to protect your API against DDOS), you may just use the `rate_limiter` dependency:

```python
from fastapi import Depends

from app.api.dependencies import rate_limiter
from app.core.utils import queue
from app.schemas.job import Job


@router.post("/task", response_model=Job, status_code=201, dependencies=[Depends(rate_limiter)])
async def create_task(message: str):
    job = await queue.pool.enqueue_job("sample_background_task", message)
    return {"id": job.job_id}
```

By default, if no token is passed in the header (that is - the user is not authenticated), the user will be limited by his IP address with the default `limit` (how many times the user can make this request every period) and `period` (time in seconds) defined in `.env`.

Even though this is useful, real power comes from creating `tiers` (categories of users) and standard `rate_limits` (`limits` and `periods` defined for specific `paths` - that is - endpoints) for these tiers.

All of the `tier` and `rate_limit` models, schemas, and endpoints are already created in the respective folders (and usable only by superusers). You may use the `create_tier` script to create the first tier (it uses the `.env` variable `TIER_NAME`, which is all you need to create a tier) or just use the api:

Here I'll create a `free` tier:

<p align="left">
    <img src="https://user-images.githubusercontent.com/43156212/282275103-d9c4f511-4cfa-40c6-b882-5b09df9f62b9.png" alt="passing name = free to api request body" width="70%" height="auto">
</p>

And a `pro` tier:

<p align="left">
    <img src="https://user-images.githubusercontent.com/43156212/282275107-5a6ca593-ccc0-4965-b2db-09ec5ecad91c.png" alt="passing name = pro to api request body" width="70%" height="auto">
</p>

Then I'll associate a `rate_limit` for the path `api/v1/tasks/task` for each of them, I'll associate a `rate limit` for the path `api/v1/tasks/task`.

> \[!WARNING\]
> Do not forget to add `api/v1/...` or any other prefix to the beggining of your path. For the structure of the boilerplate, `api/v1/<rest_of_the_path>`

1 request every hour (3600 seconds) for the free tier:

<p align="left">
    <img src="https://user-images.githubusercontent.com/43156212/282275105-95d31e19-b798-4f03-98f0-3e9d1844f7b3.png" alt="passing path=api/v1/tasks/task, limit=1, period=3600, name=api_v1_tasks:1:3600 to free tier rate limit" width="70%" height="auto">
</p>

10 requests every hour for the pro tier:

<p align="left">
    <img src="https://user-images.githubusercontent.com/43156212/282275108-deec6f46-9d47-4f01-9899-ca42da0f0363.png" alt="passing path=api/v1/tasks/task, limit=10, period=3600, name=api_v1_tasks:10:3600 to pro tier rate limit" width="70%" height="auto">
</p>

Now let's read all the tiers available (`GET api/v1/tiers`):

```javascript
{
  "data": [
    {
      "name": "free",
      "id": 1,
      "created_at": "2023-11-11T05:57:25.420360"
    },
    {
      "name": "pro",
      "id": 2,
      "created_at": "2023-11-12T00:40:00.759847"
    }
  ],
  "total_count": 2,
  "has_more": false,
  "page": 1,
  "items_per_page": 10
}
```

And read the `rate_limits` for the `pro` tier to ensure it's working (`GET api/v1/tier/pro/rate_limits`):

```javascript
{
  "data": [
    {
      "path": "api_v1_tasks_task",
      "limit": 10,
      "period": 3600,
      "id": 1,
      "tier_id": 2,
      "name": "api_v1_tasks:10:3600"
    }
  ],
  "total_count": 1,
  "has_more": false,
  "page": 1,
  "items_per_page": 10
}
```

Now, whenever an authenticated user makes a `POST` request to the `api/v1/tasks/task`, they'll use the quota that is defined by their tier.
You may check this getting the token from the `api/v1/login` endpoint, then passing it in the request header:

```sh
curl -X POST 'http://127.0.0.1:8000/api/v1/tasks/task?message=test' \
-H 'Authorization: Bearer <your-token-here>'
```

> \[!TIP\]
> Since the `rate_limiter` dependency uses the `get_optional_user` dependency instead of `get_current_user`, it will not require authentication to be used, but will behave accordingly if the user is authenticated (and token is passed in header). If you want to ensure authentication, also use `get_current_user` if you need.

To change a user's tier, you may just use the `PATCH api/v1/user/{username}/tier` endpoint.
Note that for flexibility (since this is a boilerplate), it's not necessary to previously inform a tier_id to create a user, but you probably should set every user to a certain tier (let's say `free`) once they are created.

> \[!WARNING\]
> If a user does not have a `tier` or the tier does not have a defined `rate limit` for the path and the token is still passed to the request, the default `limit` and `period` will be used, this will be saved in `app/logs`.

### 5.12 JWT Authentication

#### 5.12.1 Details

The JWT in this boilerplate is created in the following way:

1. **JWT Access Tokens:** how you actually access protected resources is passing this token in the request header.
1. **Refresh Tokens:** you use this type of token to get an `access token`, which you'll use to access protected resources.

The `access token` is short lived (default 30 minutes) to reduce the damage of a potential leak. The `refresh token`, on the other hand, is long lived (default 7 days), and you use it to renew your `access token` without the need to provide username and password every time it expires.

Since the `refresh token` lasts for a longer time, it's stored as a cookie in a secure way:

```python
# app/api/v1/login

...
response.set_cookie(
    key="refresh_token",
    value=refresh_token,
    httponly=True,  # Prevent access through JavaScript
    secure=True,  # Ensure cookie is sent over HTTPS only
    samesite="Lax",  # Default to Lax for reasonable balance between security and usability
    max_age=number_of_seconds,  # Set a max age for the cookie
)
...
```

You may change it to suit your needs. The possible options for `samesite` are:

- `Lax`: Cookies will be sent in top-level navigations (like clicking on a link to go to another site), but not in API requests or images loaded from other sites.
- `Strict`: Cookies are sent only on top-level navigations from the same site that set the cookie, enhancing privacy but potentially disrupting user sessions.
- `None`: Cookies will be sent with both same-site and cross-site requests.

#### 5.12.2 Usage

What you should do with the client is:

- `Login`: Send credentials to `/api/v1/login`. Store the returned access token in memory for subsequent requests.
- `Accessing Protected Routes`: Include the access token in the Authorization header.
- `Token Renewal`: On access token expiry, the front end should automatically call `/api/v1/refresh` for a new token.
- `Login Again`: If refresh token is expired, credentials should be sent to `/api/v1/login` again, storing the new access token in memory.
- `Logout`: Call /api/v1/logout to end the session securely.

This authentication setup in the provides a robust, secure, and user-friendly way to handle user sessions in your API applications.

### 5.13 Running

If you are using docker compose, just running the following command should ensure everything is working:

```sh
docker compose up
```

If you are doing it from scratch, ensure your postgres and your redis are running, then
while in the `root` folder, run to start the application with uvicorn server:

```sh
poetry run uvicorn src.app.main:app --reload
```

And for the worker:

```sh
poetry run arq src.app.core.worker.settings.WorkerSettings
```
### 5.14 Create Application

If you want to stop tables from being created every time you run the api, you should disable this here:

```python
# app/main.py

from .api import router
from .core.config import settings
from .core.setup import create_application

# create_tables_on_start defaults to True
app = create_application(router=router, settings=settings, create_tables_on_start=False)
```

This `create_application` function is defined in `app/core/setup.py`, and it's a flexible way to configure the behavior of your application.

A few examples:

- Deactivate or password protect /docs
- Add client-side cache middleware
- Add Startup and Shutdown event handlers for cache, queue and rate limit

### 5.15 Opting Out of Services

To opt out of services (like `Redis`, `Queue`, `Rate Limiter`), head to the `Settings` class in `src/app/core/config`:

```python
# src/app/core/config
import os
from enum import Enum

from pydantic_settings import BaseSettings
from starlette.config import Config

current_file_dir = os.path.dirname(os.path.realpath(__file__))
env_path = os.path.join(current_file_dir, "..", "..", ".env")
config = Config(env_path)
...

class Settings(
    AppSettings,
    PostgresSettings,
    CryptSettings,
    FirstUserSettings,
    TestSettings,
    RedisCacheSettings,
    ClientSideCacheSettings,
    RedisQueueSettings,
    RedisRateLimiterSettings,
    DefaultRateLimitSettings,
    EnvironmentSettings,
):
    pass


settings = Settings()
```

And remove the Settings of the services you do not need. For example, without using redis (removed `Cache`, `Queue` and `Rate limit`):

```python
class Settings(
    AppSettings,
    PostgresSettings,
    CryptSettings,
    FirstUserSettings,
    TestSettings,
    ClientSideCacheSettings,
    DefaultRateLimitSettings,
    EnvironmentSettings,
):
    pass
```

Then comment or remove the services you do not want from `docker-compose.yml`. Here, I removed `redis` and `worker` services:

```yml
version: '3.8'

services:
  web:
    build:
      context: .
      dockerfile: Dockerfile
    # -------- replace with comment to run with gunicorn --------
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    # command: gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
    env_file:
      - ./src/.env
    # -------- replace with comment if you are using nginx --------
    ports:
      - "8000:8000"
    # expose:
    #   - "8000"
    depends_on:
      - db
      - redis
    volumes:
      - ./src/app:/code/app
      - ./src/.env:/code/.env
  db:
    image: postgres:13
    env_file:
      - ./src/.env
    volumes:
      - postgres-data:/var/lib/postgresql/data
    # -------- replace with comment to run migrations with docker --------
    expose:
      - "5432"
    # ports:
    #  - 5432:5432

volumes:
  postgres-data:
  redis-data:
  #pgadmin-data:
```

## 6. Running in Production

### 6.1 Uvicorn Workers with Gunicorn

In production you may want to run using gunicorn to manage uvicorn workers:

```sh
command: gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

Here it's running with 4 workers, but you should test it depending on how many cores your machine has.

To do this if you are using docker compose, just replace the comment:
This part in `docker-compose.yml`:

```YAML
# docker-compose.yml

# -------- replace with comment to run with gunicorn --------
command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
# command: gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

Should be changed to:

```YAML
# docker-compose.yml

# -------- replace with comment to run with uvicorn --------
# command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
command: gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

And the same in `Dockerfile`:
This part:

```Dockerfile
# Dockerfile

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
# CMD ["gunicorn", "app.main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker". "-b", "0.0.0.0:8000"]
```

Should be changed to:

```Dockerfile
# Dockerfile

# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
CMD ["gunicorn", "app.main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker". "-b", "0.0.0.0:8000"]
```

> \[!CAUTION\]
> Do not forget to set the `ENVIRONMENT` in `.env` to `production` unless you want the API docs to be public.

### 6.2 Running with NGINX

NGINX is a high-performance web server, known for its stability, rich feature set, simple configuration, and low resource consumption. NGINX acts as a reverse proxy, that is, it receives client requests, forwards them to the FastAPI server (running via Uvicorn or Gunicorn), and then passes the responses back to the clients.

To run with NGINX, you start by uncommenting the following part in your `docker-compose.yml`:

```python
# docker-compose.yml

...
# -------- uncomment to run with nginx --------
# nginx:
#   image: nginx:latest
#   ports:
#     - "80:80"
#   volumes:
#     - ./default.conf:/etc/nginx/conf.d/default.conf
#   depends_on:
#     - web
...
```

Which should be changed to:

```YAML
# docker-compose.yml

...
  #-------- uncomment to run with nginx --------
  nginx:
    image: nginx:latest
    ports:
      - "80:80"
    volumes:
      - ./default.conf:/etc/nginx/conf.d/default.conf
    depends_on:
      - web
...
```

Then comment the following part:

```YAML
# docker-compose.yml

services:
  web:
    ...
    # -------- Both of the following should be commented to run with nginx --------
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    # command: gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

Which becomes:

```YAML
# docker-compose.yml

services:
  web:
    ...
    # -------- Both of the following should be commented to run with nginx --------
    # command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    # command: gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

Then pick the way you want to run (uvicorn or gunicorn managing uvicorn workers) in `Dockerfile`.
The one you want should be uncommented, comment the other one.

```Dockerfile
# Dockerfile

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
# CMD ["gunicorn", "app.main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker". "-b", "0.0.0.0:8000"]
```

And finally head to `http://localhost/docs`.

#### 6.2.1 One Server

If you want to run with one server only, your setup should be ready. Just make sure the only part that is not a comment in `default.conf` is:

```conf
# default.conf

# ---------------- Running With One Server ----------------
server {
    listen 80;

    location / {
        proxy_pass http://web:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

So just type on your browser: `http://localhost/docs`.

#### 6.2.2 Multiple Servers

NGINX can distribute incoming network traffic across multiple servers, improving the efficiency and capacity utilization of your application.

To run with multiple servers, just comment the `Running With One Server` part in `default.conf` and Uncomment the other one:

```conf
# default.conf

# ---------------- Running With One Server ----------------
...

# ---------------- To Run with Multiple Servers, Uncomment below ----------------
upstream fastapi_app {
    server fastapi1:8000;  # Replace with actual server names or IP addresses
    server fastapi2:8000;
    # Add more servers as needed
}

server {
    listen 80;

    location / {
        proxy_pass http://fastapi_app;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

And finally, on your browser: `http://localhost/docs`.

> \[!WARNING\]
> Note that we are using `fastapi1:8000` and `fastapi2:8000` as examples, you should replace it with the actual name of your service and the port it's running on.

## 7. Testing

While in the tests folder, create your test file with the name "test\_{entity}.py", replacing entity with what you're testing

```sh
touch test_items.py
```

Finally create your tests (you may want to copy the structure in test_user.py)

Now, to run:

### 7.1  Docker Compose

First you need to uncomment the following part in the `docker-compose.yml` file:

```YAML
  #-------- uncomment to run tests --------
  # pytest:
  #   build:
  #     context: .
  #     dockerfile: Dockerfile
  #   env_file:
  #     - ./src/.env
  #   depends_on:
  #     - db
  #     - redis
  #   command: python -m pytest ./tests
  #   volumes:
  #     - .:/code
```

You'll get:

```YAML
  #-------- uncomment to run tests --------
  pytest:
    build:
      context: .
      dockerfile: Dockerfile
    env_file:
      - ./src/.env
    depends_on:
      - db
      - redis
    command: python -m pytest ./tests
    volumes:
      - .:/code
```

Start the Docker Compose services:

```sh
docker-compose up -d
```

It will automatically run the tests, but if you want to run again later:

```sh
docker-compose run --rm pytest
```

### 7.2  From Scratch

While in the `root` folder, run:

```sh
poetry run python -m pytest
```

## 8. Contributing

Read [contributing](CONTRIBUTING.md).

## 9. References

This project was inspired by a few projects, it's based on them with things changed to the way I like (and pydantic, sqlalchemy updated)

- [`Full Stack FastAPI and PostgreSQL`](https://github.com/tiangolo/full-stack-fastapi-postgresql) by @tiangolo himself
- [`FastAPI Microservices`](https://github.com/Kludex/fastapi-microservices) by @kludex which heavily inspired this boilerplate
- [`Async Web API with FastAPI + SQLAlchemy 2.0`](https://github.com/rhoboro/async-fastapi-sqlalchemy) for sqlalchemy 2.0 ORM examples
- [`FastaAPI Rocket Boilerplate`](https://github.com/asacristani/fastapi-rocket-boilerplate/tree/main) for docker compose

## 10. License

[`MIT`](LICENSE.md)

## 11. Contact

Igor Magalhaes – [@igormagalhaesr](https://twitter.com/igormagalhaesr) – igormagalhaesr@gmail.com
[github.com/igorbenav](https://github.com/igorbenav/)
