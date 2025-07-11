"""
Модуль для работы с жалобами в базе данных.

Содержит:
- Определения моделей и перечислений (Enums) для статусов, тональностей и категорий жалоб.
- CRUD-функции для создания, обновления и получения жалоб.
- Асинхронная работа с базой данных через SQLAlchemy AsyncSession.

Используется в сервисах FastAPI для хранения и обработки жалоб.
"""

import enum
from datetime import datetime, timedelta

from sqlalchemy import Column, Integer, String, DateTime, Enum, func, select
from sqlalchemy.exc import SQLAlchemyError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from .db import Base


class StatusEnum(str, enum.Enum):
    """Перечисление статусов жалобы."""
    open = "open"
    closed = "closed"

class SentimentEnum(str, enum.Enum):
    """Перечисление тональностей жалобы."""
    positive = "positive"
    negative = "negative"
    neutral = "neutral"

class CategoryEnum(str, enum.Enum):
    """Перечисление категорий жалобы."""
    technical = "техническая"
    payment = "оплата"
    other = "другое"

class Complaint(Base):
    """Модель жалобы для базы данных."""
    __tablename__ = "complaints"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    status = Column(Enum(StatusEnum), default=StatusEnum.open)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    sentiment = Column(Enum(SentimentEnum), nullable=True)
    category = Column(Enum(CategoryEnum), default=CategoryEnum.other)


async def create_complaint_record(
        db: AsyncSession,
        analysis_result: dict,
        text: str,
        category: CategoryEnum = CategoryEnum.other,
        status: StatusEnum = StatusEnum.open
    ) -> Complaint:
    """
    Создает новую запись жалобы в базе данных.

    :param db: Асинхронная сессия базы данных.
    :param analysis_result: Результат анализа тональности (словарь).
    :param text: Текст жалобы.
    :param category: Категория жалобы.
    :param status: Статус жалобы.
    :return: Созданная жалоба.
    """
    sentiment_str = analysis_result.get("sentiment", "NEUTRAL").lower()
    sentiment = SentimentEnum[sentiment_str.lower()] if sentiment_str.lower() in SentimentEnum.__members__ else SentimentEnum.neutral

    complaint = Complaint(
        text=text,
        sentiment=sentiment,
        category=category,
        status=status
    )

    try:
        db.add(complaint)
        await db.commit()
        return complaint
    except SQLAlchemyError:
        await db.rollback()
        raise


async def update_complaint_category(
        db: AsyncSession,
        complaint_id: int,
        new_category: str
    ) -> Complaint:
    """
    Обновляет категорию существующей жалобы.

    :param db: Асинхронная сессия базы данных.
    :param complaint_id: ID жалобы.
    :param new_category: Новая категория (строка).
    :return: Обновленная жалоба.
    """
    try:
        result = await db.execute(
            select(Complaint).where(Complaint.id == complaint_id)
        )
        complaint = result.scalar_one_or_none()

        if complaint is None:
            raise NoResultFound(f"Complaint with id {complaint_id} not found")

        category = next(
            (member for member in CategoryEnum if member.value == new_category),
            None
        )
        complaint.category = category
        await db.commit()
        return complaint
    except SQLAlchemyError:
        await db.rollback()
        raise


async def get_recent_open_complaint_records(
        db: AsyncSession,
        current_time: datetime,
        hours: int = 1
    ) -> list[Complaint]:
    """
    Получение жалоб со статусом 'open' за указанный период времени (по умолчанию за последний час).

    :param db: Сессия базы данных.
    :param current_time: Время, от которого считается интервал.
    :param hours: Количество часов для поиска (по умолчанию 1 час).
    :return: Список жалоб.
    """
    start_time = current_time - timedelta(hours=hours)

    stmt = select(Complaint).where(
        Complaint.status == 'open',
        Complaint.timestamp >= start_time
    )
    result = await db.execute(stmt)
    complaints = result.scalars().all()
    return complaints


async def close_complaint_status(db: AsyncSession, complaint_id: int, new_status: StatusEnum):
    """
    Закрывает жалобу, обновляя её статус.

    :param db: Асинхронная сессия базы данных.
    :param complaint_id: ID жалобы.
    :param new_status: Новый статус (из StatusEnum).
    :return: Обновленная жалоба.
    """
    try:
        result = await db.execute(select(Complaint).where(Complaint.id == complaint_id))
        complaint = result.scalar_one_or_none()

        if complaint is None:
            raise ValueError(f"Complaint with id {complaint_id} not found")

        complaint.status = new_status
        await db.commit()
        await db.refresh(complaint)
        return complaint
    except SQLAlchemyError:
        await db.rollback()
        raise