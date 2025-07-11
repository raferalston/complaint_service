"""
Модуль конфигурации базы данных для приложения.

Использует:
- SQLite в асинхронном режиме через `aiosqlite`.
- SQLAlchemy для описания моделей и управления сессиями.

Содержит:
- Инициализацию базы данных.
- Получение асинхронной сессии для использования в приложении.

Параметры:
- DATABASE_URL: строка подключения к базе данных (по умолчанию SQLite файл в ./database/complaints.db).
"""

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base


db_path = "./database/complaints.db"
DATABASE_URL = f"sqlite+aiosqlite:///{db_path}"

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)
Base = declarative_base()


async def init_db():
    """
    Инициализация базы данных (создание всех таблиц).

    Используется при первом запуске приложения или после изменений моделей.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_db():
    """
    Получение асинхронной сессии базы данных.

    Используется как dependency в FastAPI.
    """
    async with AsyncSessionLocal() as session:
        yield session