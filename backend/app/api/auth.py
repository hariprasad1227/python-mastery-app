"""
Authentication API Router
Persistent PostgreSQL / SQLAlchemy authentication with real bcrypt hashing and JWT tokens.
"""

from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel, field_validator
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
import re

from backend.app.db.session import get_db
from backend.app.models.entities import User, Profile, UserProgress, Challenge
from backend.app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user,
    check_rate_limit
)

router = APIRouter(prefix="/auth", tags=["auth"])


class SignUpRequest(BaseModel):
    email: str
    password: str
    username: str
    display_name: Optional[str] = None

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        v = v.strip().lower()
        if not re.match(r"^[^@]+@[^@]+\.[^@]+$", v):
            raise ValueError("Invalid email format.")
        return v

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 6:
            raise ValueError("Password must be at least 6 characters long.")
        return v


class LoginRequest(BaseModel):
    email: str
    password: str


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: Dict[str, Any]


@router.post("/signup", response_model=AuthResponse)
async def signup(req: SignUpRequest, db: Session = Depends(get_db)):
    check_rate_limit(db, key=req.email.strip().lower(), action="auth_signup", max_requests=10, window_seconds=60)
    # Check for existing email or username
    existing_user = db.query(User).filter(
        (User.email == req.email.strip().lower()) | (User.username == req.username.strip())
    ).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An account with this email or username already exists."
        )

    # Create new User
    new_user = User(
        email=req.email.strip().lower(),
        username=req.username.strip(),
        password_hash=hash_password(req.password)
    )
    db.add(new_user)
    db.flush() # Populate new_user.id

    # Create user profile
    profile = Profile(
        user_id=new_user.id,
        display_name=req.display_name or req.username,
        total_xp=0,
        current_level=1,
        current_streak=0,
        longest_streak=0
    )
    db.add(profile)

    # Initialize task progress: Chal-1 available, remaining locked
    all_challenges = db.query(Challenge).order_by(Challenge.order_index).all()
    for idx, chal in enumerate(all_challenges):
        status_val = "available" if idx == 0 else "locked"
        db.add(UserProgress(
            user_id=new_user.id,
            challenge_id=chal.id,
            status=status_val,
            attempts_count=0,
            earned_xp=0
        ))

    db.commit()
    db.refresh(new_user)

    # Issue signed cryptographic JWT
    token = create_access_token(data={"sub": new_user.id, "email": new_user.email})

    return AuthResponse(
        access_token=token,
        user={
            "id": new_user.id,
            "email": new_user.email,
            "username": new_user.username,
            "display_name": profile.display_name,
            "total_xp": profile.total_xp,
            "current_level": profile.current_level
        }
    )


@router.post("/login", response_model=AuthResponse)
async def login(req: LoginRequest, db: Session = Depends(get_db)):
    check_rate_limit(db, key=req.email.strip().lower(), action="auth_login", max_requests=15, window_seconds=60)
    user = db.query(User).filter(User.email == req.email.strip().lower()).first()
    if not user or not verify_password(req.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password."
        )

    token = create_access_token(data={"sub": user.id, "email": user.email})
    profile = user.profile

    return AuthResponse(
        access_token=token,
        user={
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "display_name": profile.display_name if profile else user.username,
            "total_xp": profile.total_xp if profile else 0,
            "current_level": profile.current_level if profile else 1
        }
    )


@router.get("/me")
async def get_me(current_user: User = Depends(get_current_user)):
    profile = current_user.profile
    return {
        "authenticated": True,
        "user": {
            "id": current_user.id,
            "email": current_user.email,
            "username": current_user.username,
            "display_name": profile.display_name if profile else current_user.username,
            "total_xp": profile.total_xp if profile else 0,
            "current_level": profile.current_level if profile else 1,
            "current_streak": profile.current_streak if profile else 0
        }
    }


@router.post("/logout")
async def logout():
    # Client drops JWT token from localStorage/cookies
    return {"message": "Successfully logged out."}
