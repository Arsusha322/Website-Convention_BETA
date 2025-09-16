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
    try:
        db_user = db.query(UserData).filter(UserData.email == user.email).first()
        if not db_user:
            raise HTTPException(status_code=401, detail="Неверный email или пароль")

        if not verify_password(user.password, db_user.password_hash):
            raise HTTPException(status_code=401, detail="Неверный email или пароль")

        access_token = security.create_access_token(uid=str(db_user.id))
        response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, access_token)
        return UserLoginResponse(access_token=access_token, token_type="bearer")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/history", response_model=UserHistoryResponse)
def add_history(data: UserHistoryCreate, db: Session = Depends(get_db), user_id: str = Depends(security.get_current_subject)):
    new_record = UserHistory(user_id = user_id, file_name = data.file_name, text_result = data.text_result)
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return new_record

@router.get("/history", response_model=list[UserHistoryResponse])
def get_history(db: Session = Depends(get_db), user_id: str = Depends(security.get_current_subject)):
    return db.query(UserHistory).filter(UserHistory.user_id == user_id).order_by(UserHistory.created_at.desc()).all()