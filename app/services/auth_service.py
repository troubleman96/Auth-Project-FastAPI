from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserLogin
from app.utils.token import create_access_token
from datetime import timedelta, datetime
from app.crud.user import get_user_by_email, create_user
from app.core.security import verify_password
from app.core.config import settings
from app.utils.token import create_email_token
from app.utils.email import send_verification_email, send_email_async

async def register_user(db: Session, user: UserCreate):
    existing_user = get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = create_user(db, user)

    # Email verification
    token = create_email_token(new_user.email)
    #send_verification_email(new_user.email, token)
    verification_link = f"http://localhost:8000/auth/verify-email?token={token}"
    await send_email_async(
        to=new_user.email,
        subject="Verify your email",
        body=f"Click this link to verify your email: {verification_link}"
    )

    return new_user


def login_user(db: Session, user: UserLogin):
    db_user = get_user_by_email(db, user.email)
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(
        data={"sub": db_user.email},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return {"access_token": access_token, "token_type": "bearer"}
