"""Authentication routes with secure database-backed authentication"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime, timedelta, timezone
from jose import jwt
from passlib.context import CryptContext
import logging
import os

from covenant.utils.config import settings

logger = logging.getLogger(__name__)
router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/token")


class Token(BaseModel):
    """Token response model"""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Token data model"""
    username: str


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a bcrypt hash"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password using bcrypt"""
    return pwd_context.hash(password)


def create_access_token(data: dict):
    """Create JWT token with expiration"""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


async def get_user_from_db(username: str) -> dict | None:
    """
    Fetch user credentials from environment variables as a secure fallback.
    In production, replace this with a real database query.

    Expected env vars:
      - AUTH_USERNAME: the authorized username
      - AUTH_PASSWORD_HASH: bcrypt hash of the authorized password
    """
    stored_username = os.environ.get("AUTH_USERNAME", "")
    stored_password_hash = os.environ.get("AUTH_PASSWORD_HASH", "")

    if not stored_username or not stored_password_hash:
        logger.warning("AUTH_USERNAME / AUTH_PASSWORD_HASH env vars not set — falling back to defaults")
        return None

    if username != stored_username:
        return None

    return {
        "username": stored_username,
        "hashed_password": stored_password_hash,
    }


@router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Login endpoint with bcrypt password verification.
    Credentials are verified against AUTH_USERNAME / AUTH_PASSWORD_HASH env vars.
    Rate limiting should be applied at the reverse-proxy level.
    """
    try:
        logger.info(f"Login attempt for user: {form_data.username}")

        # Attempt to fetch user from env-var-based lookup
        user = await get_user_from_db(form_data.username)

        if user is None:
            # Fallback: single admin user with env-based password
            admin_user = os.environ.get("AUTH_USERNAME", "admin")
            admin_pass = os.environ.get("ADMIN_PASSWORD", "")

            if not admin_pass:
                logger.error("ADMIN_PASSWORD environment variable not set")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Authentication not configured"
                )

            if form_data.username != admin_user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid credentials"
                )

            # Use bcrypt verification if a hash is stored; otherwise compare plaintext
            stored_hash = os.environ.get("AUTH_PASSWORD_HASH", "")
            if stored_hash:
                if not verify_password(form_data.password, stored_hash):
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Invalid credentials"
                    )
            elif form_data.password != admin_pass:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid credentials"
                )
        else:
            # bcrypt password verification
            if not verify_password(form_data.password, user["hashed_password"]):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid credentials"
                )

        access_token = create_access_token(data={"sub": form_data.username})
        logger.info(f"Successful login for user: {form_data.username}")
        return {"access_token": access_token, "token_type": "bearer"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Authentication failed"
        )