from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks, Request
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta
from app.schemas.user import Token, UserPublic
from app.services.user_services import authenticate_user, get_user_by_email, register_user
from app.core.security import create_access_token, get_password_hash
from app.core.config import settings
from app.core.database import get_db
from app.core.deps import get_current_active_user
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.utils.utils import (
    generate_password_reset_token,
    generate_reset_password_email,
    send_email,
    verify_password_reset_token,
)
from app.schemas import Message, NewPassword

templates = Jinja2Templates(directory="app/templates")

router = APIRouter(tags=["auth"])

# --- LOGIN ---
@router.post("/login/access-token", response_model=Token)
async def login_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=user.email,
        expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


#   PASSWORD RECOVERY
@router.post("/password-recovery/{email}")
async def recover_password(
    email: EmailStr,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    user = await get_user_by_email(db, email=email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    token = generate_password_reset_token(email=user.email)
    email_data = generate_reset_password_email(email_to=user.email, token=token)

    background_tasks.add_task(
        send_email,
        email_to=user.email,
        subject=email_data.subject,
        html_content=email_data.html_content,
    )

    return {"msg": "Recovery email sent"}

@router.post("/reset-password/", response_model=Message)
async def reset_password_api(
    body: NewPassword,
    db: AsyncSession = Depends(get_db)
):
    email = verify_password_reset_token(token=body.token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    user = await get_user_by_email(db, email=email)
    if not user or user.disabled:
        raise HTTPException(status_code=400, detail="User not found or inactive")

    hashed_password = get_password_hash(body.new_password)
    user.hashed_password = hashed_password

    db.add(user)
    await db.commit()
    await db.refresh(user)

    return Message(message="Password updated successfully")

@router.get("/reset-password", response_class=HTMLResponse)
async def show_token_html(request: Request, token: str):
    return templates.TemplateResponse("show_token.html", {"request": request, "token": token})