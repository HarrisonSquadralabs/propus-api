import asyncio
from app.core.database import engine
from app.models import user, project, customer_info, supplier_info, project_file, token, entity
from app.models.user import User


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(User.metadata.create_all)

if __name__ == "__main__":
    asyncio.run(init_models())
