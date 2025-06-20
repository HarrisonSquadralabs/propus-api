from fastapi import FastAPI
from app.routers import project
from app.routers.auth import auth, user, auth_google
from starlette.middleware.sessions import SessionMiddleware
from app.core.config import settings

app = FastAPI()

app.include_router(user.router)
app.include_router(auth.router, prefix="/auth")
app.include_router(auth_google.router)
app.include_router(project.router)
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)

