import asyncio
import logging

from sqlalchemy import select

from ..app.core.config import config
from ..app.core.db.database import AsyncSession, local_session
from ..app.models import Role

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def create_first_role(session: AsyncSession) -> None:
    try:
        role_name = config("ROLE_NAME", default="admin")

        query = select(Role).where(Role.name == role_name)
        result = await session.execute(query)
        role = result.scalar_one_or_none()

        if role is None:
            session.add(Role(name=role_name))
            await session.commit()
            logger.info(f"Role '{role_name}' created successfully.")

        else:
            logger.info(f"Role '{role_name}' already exists.")

    except Exception as e:
        logger.error(f"Error creating role: {e}")


async def main():
    async with local_session() as session:
        await create_first_role(session)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
