from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.future import select
from app.models.user import User
from app.schemas.user import UserInDB
from app.core.security import verify_password, get_password_hash

async def get_user(db: AsyncSession, email: str) -> UserInDB | None:
    query = select(User).options(selectinload(User.role)).where(User.email == email)
    result = await db.execute(query)
    user = result.scalars().first()
    if user:
        return UserInDB(
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            disabled=user.disabled,
            hashed_password=user.hashed_password,
            role_name=user.role.type.value
        )
    return None


async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    query = select(User).options(selectinload(User.role)).where(User.email == email)
    result = await db.execute(query)
    return result.scalars().first() 

async def authenticate_user(db: AsyncSession, email: str, password: str) -> UserInDB:
    user = await get_user_by_email(db, email)
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    if user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return UserInDB(
        id=user.id,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        disabled=user.disabled,
        hashed_password=user.hashed_password,
        role_name=user.role.type.value
    )


async def register_user(
    db: AsyncSession,
    password: str,
    first_name: str,
    last_name: str,
    email: str,
    architect_info: str | None = None,
    role: str = "customer"
) -> User:
    existing_user = await get_user(db, email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = get_password_hash(password)

    new_user = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        hashed_password=hashed_password,
        architect_info=architect_info,
        disabled=False,
        role=role,
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

