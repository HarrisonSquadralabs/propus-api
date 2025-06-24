import asyncio
from app.core.database import engine
from app.models import supplier_role, user, project, customer_role, architect_role, permission, role_permissions, token, entity
from app.models.user import User


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(User.metadata.create_all)

if __name__ == "__main__":
    asyncio.run(init_models())
