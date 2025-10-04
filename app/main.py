from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import Base, engine
from app.routers import users, files
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:63342"],  # твой фронт
    allow_credentials=True,
    allow_methods=["*"],  # разрешаем все методы (POST, GET, OPTIONS и т.д.)
    allow_headers=["*"],  # разрешаем все заголовки
)

app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(files.router, prefix="/files", tags=["files"])