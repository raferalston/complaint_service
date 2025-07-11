"""
Модуль маршрутов FastAPI для работы с жалобами.

Функционал:
- Создание жалобы (с вызовом внешних API для анализа тональности и категории).
- Получение списка жалоб со статусом 'open' за последний час.
- Обновление статуса жалобы на 'closed'.

Все защищено API-ключом через заголовок `complaint-api-key`.
"""

import asyncio

from datetime import datetime

from fastapi import APIRouter, HTTPException, Depends, Header, Query
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from core.config import settings
from database.db import get_db
from database.models import create_complaint_record, update_complaint_category, get_recent_open_complaint_records, close_complaint_status
from database.models import StatusEnum
from schemas.complant import ComplantInput, ComplaintResponse
from services.complaint_category_service import complaint_category_analyze
from services.sentiment_service import sentiment_analyze


router = APIRouter()

class UpdateStatusRequest(BaseModel):
    """Модель запроса для обновления статуса жалобы."""
    id: int


@router.post("/complaints/close-status/")
async def update_status(
        data: UpdateStatusRequest,
        db: AsyncSession = Depends(get_db),
        apikey: str = Header(..., alias="complaint-api-key"),
    ):
    """
    Обновить статус жалобы на 'closed'.

    Требуется API-ключ.
    """
    if apikey != settings.COMPLAINT_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    try:
        complaint = await close_complaint_status(db, data.id, StatusEnum.closed)
        return {
            "id": complaint.id,
            "status": complaint.status,
            "timestamp": complaint.timestamp
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.get("/complaints/open-recent")
async def get_recent_open_complaints(
        current_time: str = Query(..., description="Текущее время в формате ISO 8601"),
        apikey: str = Header(..., alias="complaint-api-key"),
        db: AsyncSession = Depends(get_db)
    ):
    """
    Получить все жалобы со статусом 'open' за последний час.

    Требуется API-ключ.
    """
    if apikey != settings.COMPLAINT_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    
    try:
        query_time = datetime.fromisoformat(current_time)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid datetime format. Use ISO 8601 format.")
    
    try:
        complaints = await get_recent_open_complaint_records(db, query_time, hours=1)

        return [
            {
                "id": c.id,
                "text": c.text,
                "status": c.status,
                "timestamp": c.timestamp.isoformat(),
                "sentiment": c.sentiment,
                "category": c.category
            }
            for c in complaints
        ]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.post("/complaints/", response_model=ComplaintResponse)
async def create_complaint(request: ComplantInput, db: AsyncSession = Depends(get_db)):
    """
    Создать новую жалобу.

    Выполняет:
    1. Анализ тональности (sentiment).
    2. Сохранение жалобы в базе данных.
    3. Определение категории жалобы (technical, payment, other).
    4. Обновление категории в базе данных.

    Возвращает ComplaintResponse
    """
    try:
        complaint_text = request.text

        # Параллельно вызываем оба внешних API
        sentiment_task = asyncio.create_task(sentiment_analyze(complaint_text))
        category_task = asyncio.create_task(complaint_category_analyze(complaint_text))

        # Ждём ответа sentiment (нужен для создания записи в БД)
        sentiment = await sentiment_task
        complaint = await create_complaint_record(db, sentiment, complaint_text)

        # Ждём категорию (можно уже после создания complaint)
        complaint_analyze = await category_task
        updated_complaint = await update_complaint_category(
            db=db,
            complaint_id=complaint.id,
            new_category=complaint_analyze
        )

        return ComplaintResponse(
            id=updated_complaint.id,
            status=updated_complaint.status,
            sentiment=updated_complaint.sentiment,
            category=updated_complaint.category
        ) 

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
