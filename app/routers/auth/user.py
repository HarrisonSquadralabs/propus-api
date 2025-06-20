from fastapi import HTTPException, Depends, APIRouter
from app.schemas.user import UserCreate, UserRole
from app.core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import User, CustomerInfo, SupplierInfo
from app.core.security import get_password_hash

router = APIRouter()

@router.post("/users/register")
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == user.email))
    if result.scalar():
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = get_password_hash(user.password)

    first_name = user.first_name
    last_name = user.last_name

    new_user = User(
        email=user.email,
        first_name=first_name,
        last_name=last_name,
        hashed_password=hashed_pw,
        role=user.role.value,
        architect_info=user.architect_info if user.role in [UserRole.architect, UserRole.engineer] else None
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    # Additional info depending on the role
    if user.role == UserRole.customer:
        customer_info = CustomerInfo(user_id=new_user.id, phone=user.phone)
        db.add(customer_info)
        await db.commit()
    elif user.role == UserRole.supplier:
        supplier_info = SupplierInfo(
            user_id=new_user.id,
            phone=user.phone,
            company=user.company,
            address=user.address
        )
        db.add(supplier_info)
        await db.commit()

    return {"msg": f"User {user.role.value} created", "user_id": new_user.id}