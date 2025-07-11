"""
Главный модуль приложения FastAPI.

Здесь выполняется:
- Инициализация базы данных при запуске приложения (через lifespan).
- Регистрация маршрутов (в данном случае — маршруты жалоб из routers.complant).
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI

from routers import complant
from database.db import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(complant.router)
