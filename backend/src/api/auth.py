# src/api/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import Dict, Any
from ..models.user import UserCreate, UserRead, User
from ..services.auth import get_password_hash, create_access_token, verify_password
from .dependencies import get_db
from datetime import timedelta
from pydantic import BaseModel

router = APIRouter()

# Request body model for login (keeps swagger clean)
class LoginRequest(BaseModel):
    email: str
    password: str

# Response model for auth endpoints
class AuthUserResponse(BaseModel):
    success: bool
    user: UserRead
    token: str

@router.post("/register", response_model=AuthUserResponse)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user."""
    # Check if user already exists
    existing_user_query = select(User).where(User.email == user.email)
    existing_user = db.exec(existing_user_query).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create new user
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # Create access token
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": str(db_user.id)}, expires_delta=access_token_expires
    )

    return {
        "success": True,
        "user": UserRead.from_orm(db_user),
        "token": access_token
    }


@router.post("/login", response_model=AuthUserResponse)
async def login(payload: LoginRequest, db: Session = Depends(get_db)):
    """Login an existing user."""
    # Find user by email
    user_query = select(User).where(User.email == payload.email)
    db_user = db.exec(user_query).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    # Verify password using central service function
    if not verify_password(payload.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    # Create access token
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": str(db_user.id)}, expires_delta=access_token_expires
    )

    return {
        "success": True,
        "user": UserRead.from_orm(db_user),
        "token": access_token
    }
