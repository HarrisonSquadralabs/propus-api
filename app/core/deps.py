from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.config import settings
from app.models.user import User, UserRole
from app.core.database import get_db  
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login/access-token")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")  
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception


    result = await db.execute(select(User).where(User.email == email))
    user = result.scalars().first()

    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

async def get_current_active_superuser(
    current_user: User = Depends(get_current_user)
) -> User:
    if not current_user.is_superuser:
        raise HTTPException(status_code=400, detail="User lacks superuser privileges")
    return current_user

def require_role(required_role: UserRole):
    async def role_checker(current_user: User = Depends(get_current_active_user)):
        if current_user.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
              detail=f"Access denied: required role {required_role}, you have {current_user.role}"
            )
        return current_user
    return role_checker