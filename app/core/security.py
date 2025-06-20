from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from passlib.context import CryptContext
from app.core.config import settings
## Define the algorithm and password context for hashing

# Create a password context for hashing and verifying passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
## Function to verify a plain password against a hashed password

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

## Function to hash a plain password
def get_password_hash(password: str):
    return pwd_context.hash(password)

## Function to create a JWT access token
def create_access_token(subject: str, expires_delta: timedelta = None):
    if expires_delta is None:
        expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = {"exp": expire, "sub": subject}
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

## Function to decode a JWT access token and return the subject (user identifier
def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None
