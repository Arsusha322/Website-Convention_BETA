from fastapi import APIRouter, Depends, HTTPException, Response, Cookie
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models import UserData, UserHistory
from app.schemas import UserCreate, UserResponse, UserLogin, UserLoginResponse, UserHistoryResponse
from app.utils.password_and_token import hash_password, verify_password, create_access_token, get_current_user
from sqlalchemy import select

router = APIRouter()

@router.post("/", response_model=UserResponse)
async def create_user(user: UserCreate, response: Response, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(UserData).where(UserData.email == user.email))
    db_user = result.scalars().first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email уже зарегистрирован")

    new_user = UserData(email=user.email, password_hash=hash_password(user.password))
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    access_token = create_access_token(user_id=new_user.id)
    response.set_cookie(key="access_token", value=access_token, httponly=True, samesite="lax")
    return new_user


@router.post("/login", response_model=UserLoginResponse)
async def login(user: UserLogin, response: Response, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(UserData).where(UserData.email == user.email))
    db_user = result.scalars().first()
    if not db_user or not verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Неверный email или пароль")

    access_token = create_access_token(user_id=db_user.id)
    response.set_cookie(key="access_token", value=access_token, httponly=True, samesite="lax")
    return UserLoginResponse(access_token=access_token, token_type="bearer")

@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Вы успешно вышли"}


@router.get("/history", response_model=list[UserHistoryResponse])
async def get_history(db: AsyncSession = Depends(get_db), access_token: str | None = Cookie(default=None)):
    user_id = get_current_user(access_token)
    result = await db.execute(select(UserHistory).where(UserHistory.user_id == user_id).order_by(UserHistory.created_at.desc()))
    return result.scalars().all()
