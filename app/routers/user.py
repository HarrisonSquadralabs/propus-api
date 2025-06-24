from fastapi import APIRouter, status, HTTPException, Depends
from app.schemas.user import UserCreate, UserRead, UserUpdate
from sqlalchemy.orm import joinedload
from app.core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID
from app.models import (
    User,
    CustomerRole,
    SupplierRole,
    ArchitectRole,
    RoleType
)
from app.core.security import get_password_hash

router = APIRouter()

@router.post("/users/register")
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
  
    result = await db.execute(select(User).where(User.email == user.email))
    if result.scalar():
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = get_password_hash(user.password)

    role_instance = None

    if user.role == RoleType.customer:
        role_instance = CustomerRole(phone=user.phone, address=user.address)
    elif user.role == RoleType.supplier:
        role_instance = SupplierRole(phone=user.phone, company=user.company, address=user.address)
    elif user.role == RoleType.architect:
        role_instance = ArchitectRole(entity_type=user.architect_info)
    else:
        raise HTTPException(status_code=400, detail="Unsupported role")

    db.add(role_instance)
    await db.commit()
    await db.refresh(role_instance)

    new_user = User(
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        hashed_password=hashed_pw,
        role_id=role_instance.id
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return {
        "msg": f"User {user.role.value} created",
        "user_id": new_user.id,
        "role_id": role_instance.id
    }
@router.get("/users/all", response_model=list[UserRead])
async def get_all_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(User).options(joinedload(User.role))
    )
    users = result.scalars().all()

    if not users:
        raise HTTPException(status_code=404, detail="No users found")

    return [
        UserRead(
            id=user.id,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            is_completed=user.is_completed,
            role_id=user.role.id,
            role_name=user.role.type.value
        )
        for user in users
    ]
@router.get("/users/{user_id}", response_model=UserRead)
async def get_user(user_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(User).options(joinedload(User.role)).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return UserRead(
        id=user.id,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        is_completed=user.is_completed,
        role_id=user.role.id,
        role_name=user.role.type.value
    )
@router.patch("/users/{user_id}", response_model=UserRead)
async def update_user(user_id: UUID, update_data: UserUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(User).options(joinedload(User.role)).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    for field, value in update_data.dict(exclude_unset=True).items():
        setattr(user, field, value)

    await db.commit()
    await db.refresh(user)

    return UserRead(
        id=user.id,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        is_completed=user.is_completed,
        role_id=user.role.id,
        role_name=user.role.type.value
    )

@router.delete("/users/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user(user_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await db.delete(user)
    await db.commit()

    return {"msg": f"User with ID {user_id} deleted successfully"}
