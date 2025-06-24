from fastapi import APIRouter, Request, Depends, HTTPException, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID

from app.core.config import settings
from app.core.database import get_db
from app.models import User, CustomerRole, SupplierRole, Role, RoleType

router = APIRouter(prefix="/auth/google", tags=["auth-google"])

GOOGLE_CLIENT_ID = settings.GOOGLE_CLIENT_ID
GOOGLE_CLIENT_SECRET = settings.GOOGLE_CLIENT_SECRET

config = Config(environ={
    "GOOGLE_CLIENT_ID": GOOGLE_CLIENT_ID,
    "GOOGLE_CLIENT_SECRET": GOOGLE_CLIENT_SECRET,
})

oauth = OAuth(config)
oauth.register(
    name='google',
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)

templates = Jinja2Templates(directory="app/templates")

@router.get("/login")
async def login_via_google(request: Request):
    redirect_uri = request.url_for('auth_google_callback')
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get("/callback")
async def auth_google_callback(request: Request, db: AsyncSession = Depends(get_db)):
    token = await oauth.google.authorize_access_token(request)
    user_info = await oauth.google.userinfo(token=token)
    
    email = user_info["email"]
    first_name = user_info.get("given_name", "")
    last_name = user_info.get("family_name", "")

    result = await db.execute(select(User).where(User.email == email))
    user = result.scalars().first()

    if not user:
        user = User(
            email=email,
            first_name=first_name,
            last_name=last_name,
            hashed_password=None,
            role=None,
            is_completed=False
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)

    if not user.is_completed:
        return RedirectResponse(url=f"/auth/google/complete-registration?user_id={user.id}")
    else:
        return RedirectResponse(url="http://localhost:8000/docs")  

@router.get("/complete-registration")
async def show_complete_registration_form(request: Request, user_id: UUID):
    return templates.TemplateResponse("complete_registration.html", {"request": request, "user_id": user_id})

@router.post("/complete-registration")
async def complete_registration(
    request: Request,
    user_id: UUID = Form(...),
    role: str = Form(...),
    architect_info: str = Form(None),
    customer_phone: str = Form(None),
    supplier_phone: str = Form(None),
    company: str = Form(None),
    address: str = Form(None),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    result = await db.execute(select(Role).where(Role.type == role))
    db_role = result.scalars().first()
    if not db_role:
        raise HTTPException(status_code=400, detail="Invalid role selected")

    if role == RoleType.customer and not customer_phone:
        raise HTTPException(status_code=400, detail="Customer phone is required")
    elif role == RoleType.supplier and (not supplier_phone or not company or not address):
        raise HTTPException(status_code=400, detail="Supplier info is incomplete")
    elif role == RoleType.architect and not architect_info:
        raise HTTPException(status_code=400, detail="Architect info is required")

    user.role = db_role
    user.architect_info = architect_info
    user.is_completed = True
    db.add(user)
    await db.commit()
    await db.refresh(user)

    if role == RoleType.customer:
        db.add(CustomerRole(user_id=user.id, phone=customer_phone))
    elif role == RoleType.supplier:
        db.add(SupplierRole(
            user_id=user.id,
            phone=supplier_phone,
            company=company,
            address=address
        ))
    await db.commit()

    return templates.TemplateResponse("registration_completed.html", {"request": request, "user": user})
