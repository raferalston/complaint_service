"""
Модуль для анализа категории жалобы через OpenAI.

Функции:
---------
- complaint_category_analyze:
    Отправляет запрос к внешнему OpenAI для определения категории жалобы.
    Использует модель GPT-3.5-Turbo, формируя запрос с инструкцией на русском языке.

    Аргументы:
        - text (str): Текст жалобы для анализа.

    Возвращает:
        - str: Название категории, определённое моделью (одно из: "техническая", "оплата", "другое").
--------

Важно:
    - Используется temperature=0 для предсказуемого результата.
    - Требует настройки API_KEY и API_ENDPOINT в конфигурации (core/settings).
"""

import httpx
from core.config import settings


API_KEY = settings.API_OPENAI_KEY
API_ENDPOINT = settings.OPENAI_ENDPOINT_URL


async def complaint_category_analyze(text: str) -> str:
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
                {
                    "role": "user",
                    "content": f'Определи категорию жалобы: "{text}". Варианты: техническая, оплата, другое. Ответ только одним словом.'
                }
            ],
        "temperature": 0
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                API_ENDPOINT, 
                headers=headers, 
                json=payload
            )
            response.raise_for_status()
            data = response.json()
            choices = data.get("choices")

            if not choices or not isinstance(choices, list):
                raise ValueError("Некорректный формат ответа: отсутствует список 'choices'")

            message = choices[0].get("message")
            if not message or "content" not in message:
                raise ValueError("Некорректный формат ответа: отсутствует 'message.content'")

            content = message["content"].strip()
            return content
        
        except httpx.HTTPStatusError as e:
            print("HTTP Status Error:", e)
            raise
        except httpx.RequestError as e:
            print("Request Error:", e)
            raise
        except (ValueError, KeyError, TypeError) as e:
            print("Ошибка обработки ответа от API:", e)
            raise ValueError("Некорректный ответ от сервера анализа категории жалобы") from e
