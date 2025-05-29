from app.db.session import get_db
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from app.models.user import UserRole
from sqlalchemy.orm import Session
from app.models.user import User as DBUser

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_db_session() -> Session:
    db = next(get_db())
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    email = payload.get("sub")
    user = get_user_by_email(db, email)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user

def role_required(required_roles: list[UserRole]):
    def wrapper(current_user: DBUser = Depends(get_current_user)):
        if current_user.role not in required_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        return current_user
    return wrapper    