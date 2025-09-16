import os
from passlib.context import CryptContext
from authx import AuthX, AuthXConfig
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from app.models import UserData
from app.database import SessionLocal

load_dotenv()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

config = AuthXConfig()
config.JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
config.JWT_ACCESS_COOKIE_NAME = os.getenv("JWT_ACCESS_COOKIE_NAME")
config.JWT_TOKEN_LOCATION = ["cookies"]
config.JWT_COOKIE_CSRF_PROTECT = False

security = AuthX(config=config)

@security.set_subject_getter
def get_user_from_uid(uid: str) -> UserData:
    db: Session = SessionLocal()
    user = db.query(UserData).filter(UserData.id == int(uid)).first()
    db.close()
    return user

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str):
    return pwd_context.verify(password, hashed)
