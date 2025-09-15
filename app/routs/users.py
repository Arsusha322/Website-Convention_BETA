from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import UserData
from app.schemas import UserCreate, UserResponse, UserLogin, UserLoginResponse
from app.utils import hash_password, verify_password, security

router = APIRouter()

@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(UserData).filter(UserData.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email уже зарегистрирован")

    new_user = UserData(
        email=user.email,
        password_hash=hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login", response_model=UserLoginResponse)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(UserData).filter(UserData.email == user.email).first()
    if not db_user:
        raise HTTPException(status_code=401, detail="Неверный email или пароль")

    if not verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Неверный email или пароль")

    access_token = security.create_access_token(subject=str(db_user.id))
    return UserLoginResponse(access_token=access_token, token_type="bearer")
