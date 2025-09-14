from sqlalchemy import Column, BigInteger, ForeignKey, Text, TIMESTAMP
from sqlalchemy.sql import func
from app.database import Base

class UserData(Base):
    __tablename__ = "user_data"
    id = Column(BigInteger, primary_key=True, index=True)
    email = Column(Text, unique=True, nullable=False)
    password_hash = Column(Text, nullable=False)

class UserHistory(Base):
    __tablename__ = "user_history"
    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey("user_data.id", ondelete="CASCADE"), nullable=False)
    file_name = Column(Text, nullable=False)
    text_result = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
