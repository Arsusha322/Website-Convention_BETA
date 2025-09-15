from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import Base, engine
from app.routs import users

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(users.router, prefix="/users", tags=["users"])
