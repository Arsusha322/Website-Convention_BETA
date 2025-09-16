from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import UserData, UserHistory
from app.schemas import UserCreate, UserResponse, UserLogin, UserLoginResponse, UserHistoryCreate, UserHistoryResponse
from app.utils import hash_password, verify_password, security, config

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
def login(user: UserLogin, response: Response, db: Session = Depends(get_db)):
    db_user = db.query(UserData).filter(UserData.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Неверный email или пароль")

    access_token = security.create_access_token(uid=str(db_user.id))
    response.set_cookie(
        key=config.JWT_ACCESS_COOKIE_NAME,
        value=access_token,
        httponly=True
    )
    return UserLoginResponse(access_token=access_token, token_type="bearer")

@router.post("/history", response_model=UserHistoryResponse)
def add_history(data: UserHistoryCreate, db: Session = Depends(get_db), current_user: UserData = Depends(security.get_current_subject)):
    new_record = UserHistory(user_id=current_user.id, file_name=data.file_name, text_result=data.text_result)
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return new_record

@router.get("/history", response_model=list[UserHistoryResponse])
def get_history(
    db: Session = Depends(get_db),
    current_user: UserData = Depends(security.get_current_subject)
):
    return db.query(UserHistory).filter(UserHistory.user_id == current_user.id).order_by(UserHistory.created_at.desc()).all()
