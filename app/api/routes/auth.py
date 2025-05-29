from fastapi import APIRouter, Depends
from app.schemas.user import UserCreate, UserLogin, UserRead, Token, PasswordReset
from app.services.auth_service import register_user, login_user
from app.utils.token import verify_email_token
from app.core.security import hash_password
from app.crud.user import get_user_by_email
from pydantic import EmailStr
from app.models.user import UserRole
from app.utils.email import send_password_reset_email
from app.utils.token import create_email_token
from app.models.user import User as DBUser
from app.api.deps import get_db_session, role_required
from fastapi import HTTPException
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/register", response_model=UserRead)
async def register(user: UserCreate, db: Session = Depends(get_db_session)):
    return await register_user(db, user)

@router.get("/verify-email")
def verify_email(token: str, db: Session = Depends(get_db_session)):
    email = verify_email_token(token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    
    user = get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.is_verified = True
    db.commit()
    return {"msg": "Email verified successfully!"}    

@router.post("/reset-password-request")
async def request_password_reset(email: EmailStr, db: Session = Depends(get_db_session)):
    user = get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    token = create_email_token(email)
    await send_password_reset_email(email, token)
    return {"msg": "Password reset link sent."}    

@router.post("/reset-password")
def reset_password(data: PasswordReset, db: Session = Depends(get_db_session)):
    email = verify_email_token(data.token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    
    user = get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.hashed_password = hash_password(data.new_password)
    db.commit()
    return {"msg": "Password reset successful."}    

@router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db_session)):
    return login_user(db, user)

@router.get("/admin-only")
def admin_data(current_user = Depends(role_required([UserRole.ADMIN]))):
    return {"msg": f"Welcome admin {current_user.email}!"}    

