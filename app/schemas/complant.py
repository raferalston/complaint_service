"""
Модуль схем (Pydantic) для валидации входящих данных и формирования ответов API, связанных с жалобами.

Классы:
--------
- ComplantInput:
    Схема для входных данных при создании жалобы.
    Поля:
        - text (str): Текст жалобы.

- StatusEnum:
    Перечисление возможных статусов жалобы.
    Значения:
        - open: Жалоба открыта.
        - closed: Жалоба закрыта.

- SentimentEnum:
    Перечисление возможных вариантов тональности жалобы.
    Значения:
        - positive: Позитивная.
        - negative: Негативная.
        - neutral: Нейтральная.

- CategoryEnum:
    Перечисление возможных категорий жалобы.
    Значения:
        - technical: Техническая проблема.
        - payment: Оплата.
        - other: Другое.

- ComplaintResponse:
    Схема для ответа API с информацией о жалобе.
    Поля:
        - id (int): Идентификатор жалобы.
        - status (StatusEnum): Статус жалобы.
        - sentiment (Optional[SentimentEnum]): Тональность (может отсутствовать).
        - category (Optional[CategoryEnum]): Категория (может отсутствовать).
"""

from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field

from database.models import StatusEnum, SentimentEnum, CategoryEnum


class ComplantInput(BaseModel):
    text: str = Field(..., description="Текст жалобы")


class StatusEnum(str, Enum):
    open = "open"
    closed = "closed"


class SentimentEnum(str, Enum):
    positive = "positive"
    negative = "negative"
    neutral = "neutral"


class CategoryEnum(str, Enum):
    technical = "техническая"
    payment = "оплата"
    other = "другое"


class ComplaintResponse(BaseModel):
    """Схема для ответа с данными жалобы."""
    id: int
    status: StatusEnum
    sentiment: Optional[SentimentEnum] = None
    category: Optional[CategoryEnum] = None
