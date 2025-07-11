"""
Модуль для выполнения анализа тональности текста через APILayer.

Функция:
- sentiment_analyze: Отправляет текст на анализ тональности и возвращает результат.

Важно:
- Требует настройки API_KEY и API_ENDPOINT в конфигурации (core/settings).
"""

import httpx
from core.config import settings


API_KEY = settings.API_LAYER_KEY
API_ENDPOINT = settings.LAYER_ENDPOINT_URL


async def sentiment_analyze(text: str) -> dict:
    headers = {
        "apikey": API_KEY
    }
    payload = {
        "text": text
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                API_ENDPOINT,
                headers=headers,
                data=payload
            )
            response.raise_for_status()
            data = response.json()
            return data
        except httpx.HTTPStatusError as e:
            print("HTTP Status Error:", e)
            raise
        except httpx.RequestError as e:
            print("Request Error:", e)
            raise

