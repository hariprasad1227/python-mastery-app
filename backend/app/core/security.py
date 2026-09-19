"""
Production Authentication & Cryptographic Security
Handles bcrypt password hashing, cryptographic JWT creation and verification,
and FastAPI authenticated user dependencies.
"""

import bcrypt
import jwt
from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from backend.app.core.config import settings
from backend.app.db.session import get_db
from backend.app.models.entities import User

# HTTP Bearer token scheme
security_bearer = HTTPBearer(auto_error=False)


def hash_password(password: str) -> str:
    """Hash password using bcrypt."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against bcrypt hash."""
    try:
        return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))
    except Exception:
        return False


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Generate signed JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow()
    })
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> dict:
    """Decode and cryptographically verify JWT token."""
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session token has expired. Please log in again.",
            headers={"WWW-Authenticate": "Bearer"}
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token signature.",
            headers={"WWW-Authenticate": "Bearer"}
        )


async def get_current_user(
    auth_header: Optional[HTTPAuthorizationCredentials] = Depends(security_bearer),
    db: Session = Depends(get_db)
) -> User:
    """
    FastAPI Dependency to enforce authenticated user on protected routes.
    """
    if not auth_header or not auth_header.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required. Please provide a valid Bearer token.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    payload = decode_access_token(auth_header.credentials)
    user_id: str = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token missing user identification subject.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User associated with token not found.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return user


async def get_optional_current_user(
    auth_header: Optional[HTTPAuthorizationCredentials] = Depends(security_bearer),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """
    Returns user if valid token is provided, or None if anonymous.
    """
    if not auth_header or not auth_header.credentials:
        return None
    try:
        payload = decode_access_token(auth_header.credentials)
        user_id: str = payload.get("sub")
        if not user_id:
            return None
        return db.query(User).filter(User.id == user_id).first()
    except HTTPException:
        return None


def check_rate_limit(
    db: Session,
    key: str,
    action: str,
    max_requests: int = 30,
    window_seconds: int = 60
) -> bool:
    """
    Checks and enforces persistent rate limit using RateLimitRecord.
    Raises HTTPException 429 if exceeded.
    """
    import time
    from backend.app.models.entities import RateLimitRecord
    
    now = time.time()
    record = db.query(RateLimitRecord).filter(
        RateLimitRecord.key == key,
        RateLimitRecord.action == action
    ).first()

    if not record or (now - record.window_start) > window_seconds:
        if record:
            record.window_start = now
            record.request_count = 1
        else:
            record = RateLimitRecord(
                key=key,
                action=action,
                window_start=now,
                request_count=1
            )
            db.add(record)
        db.commit()
        return True

    if record.request_count >= max_requests:
        retry_after = max(1, int(window_seconds - (now - record.window_start)) + 1)
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Rate limit exceeded for '{action}'. Please retry in {retry_after}s.",
            headers={"Retry-After": str(retry_after)}
        )

    record.request_count += 1
    db.commit()
    return True

