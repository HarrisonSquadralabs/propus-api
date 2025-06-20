import logging
from dataclasses import dataclass
from datetime import datetime, timedelta
from pydantic import EmailStr, ValidationError, parse_obj_as
import emails
from jose import jwt, JWTError
from jinja2 import Environment, FileSystemLoader
import os

from app.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Jinja2
TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")
env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))

@dataclass
class EmailData:
    html_content: str
    subject: str

def render_template(template_name: str, context: dict) -> str:
    template = env.get_template(template_name)
    return template.render(context)

def send_email(
    *,
    email_to: str,
    subject: str = "",
    html_content: str = "",
) -> None:
    assert settings.emails_enabled, "no provided configuration for email variables"
    message = emails.Message(
        subject=subject,
        html=html_content,
        mail_from=(settings.EMAILS_FROM_NAME, settings.EMAILS_FROM_EMAIL),
    )
    smtp_options = {"host": settings.SMTP_HOST, "port": settings.SMTP_PORT}
    if settings.SMTP_TLS:
        smtp_options["tls"] = True
    elif settings.SMTP_SSL:
        smtp_options["ssl"] = True
    if settings.SMTP_USER:
        smtp_options["user"] = settings.SMTP_USER
    if settings.SMTP_PASSWORD:
        smtp_options["password"] = settings.SMTP_PASSWORD
    response = message.send(to=email_to, smtp=smtp_options)
    logger.info(f"send email result: {response}")

def generate_reset_password_email(email_to: str, token: str) -> EmailData:
    project_name = settings.PROJECT_NAME
    reset_link = f"http://localhost:8000/auth/reset-password?token={token}"
    subject = f"{project_name} - Recover your password"
    html_content = render_template(
        "reset_password.html",
        {"project_name": project_name, "reset_link": reset_link}
    )
    return EmailData(html_content=html_content, subject=subject)

def generate_password_reset_token(email: str) -> str:
    try:
        parse_obj_as(EmailStr, email)
    except ValidationError:
        raise ValueError("Invalid email for token generation")
    expire = datetime.utcnow() + timedelta(hours=1)
    to_encode = {"sub": email, "exp": expire}
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def verify_password_reset_token(token: str) -> str | None:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
        email: str = payload.get("sub")
        if email is None:
            return None
        return email
    except JWTError:
        return None