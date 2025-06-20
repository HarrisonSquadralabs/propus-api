from fastapi import APIRouter, Request, Depends, HTTPException, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.config import settings
from app.core.database import get_db
from app.models import User, CustomerInfo, SupplierInfo

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
    client_kwargs={
        'scope': 'openid email profile'
    }
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
            role="pending", 
            is_completed=False
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
    if not user.is_completed:
        return RedirectResponse(url=f"/auth/google/complete-registration?user_id={user.id}")
    else:
        return RedirectResponse("http://localhost:8000/docs")
    
@router.get("/complete-registration")
async def show_complete_registration_form(request: Request, user_id: int):
    return templates.TemplateResponse("complete_registration.html", {"request": request, "user_id": user_id})
   
@router.post("/complete-registration")
async def complete_registration(
    request: Request,
    user_id: int = Form(...),
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
    user.role = role
    user.architect_info = architect_info
    user.is_completed = True
    db.add(user)
    await db.commit()
    await db.refresh(user)

    
    if role == "Customer":
        customer_info = CustomerInfo(user_id=user.id, phone=customer_phone)
        db.add(customer_info)
        await db.commit()
    elif role == "Supplier":
        supplier_info = SupplierInfo(
            user_id=user.id,
            phone=supplier_phone,
            company=company,
            address=address
        )
        db.add(supplier_info)
        await db.commit()

    return templates.TemplateResponse("registration_completed.html", {"request": request, "user": user})