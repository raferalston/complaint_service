# 📂 Структура приложения

```
env/
app/
│   .env.debug
│   .env.prod
│   main.py
│   run_main_app.bat
│
├—— core/
├—— database/
├—— routers/
├—— schemas/
├—— services/
├—— tests/
│
mock_api/
│   mock_open_ai_api.py
│   run_mock_open_ai_api.bat
│   mock_sentiment_api.py
│   run_mock_sentiment_api.bat
│
workflow/
│   *.png  # изображения для пояснений
│
requirements.txt
some_requests.bat
```

---

## 🚀 Как использовать для ручного теста mock-серверов

### 1. Активировать виртуальное окружение и установить зависимости:

```
py -m venv env
env\Scripts\activate
pip install requirements.txt
```

### 2. Запустить основные приложения и mock-сервисы:

```
app/run_main_app.bat
mock_api/run_mock_open_ai_api.bat
mock_api/run_mock_sentiment_api.bat
```

### 3. Заполнить базу данных (*app/database/complaints.db*):

* Через готовый скрипт:

```
some_requests.bat
```

* Или через `curl`:

```
curl -X POST "http://127.0.0.1:8000/complaints/" -H "Content-Type: application/json" -d "{\"text\": \"тест 1 !оплата\"}" ^
curl -X POST "http://127.0.0.1:8000/complaints/" -H "Content-Type: application/json" -d "{\"text\": \"тест 2 !техническая\"}" ^
curl -X POST "http://127.0.0.1:8000/complaints/" -H "Content-Type: application/json" -d "{\"text\": \"тест 3 !тест\"}" ^
curl -X POST "http://127.0.0.1:8000/complaints/" -H "Content-Type: application/json" -d "{\"text\": \"тест 4 !другое love\"}" ^
curl -X POST "http://127.0.0.1:8000/complaints/" -H "Content-Type: application/json" -d "{\"text\": \"тест 5 !другое bad\"}" ^
curl -X POST "http://127.0.0.1:8000/complaints/" -H "Content-Type: application/json" -d "{\"text\": \"тест 6 !другое ok\"}"
```

📷 Результат в базе данных:
![База данных](workflow/02_database.png)

---

## 🔄 Тестирование workflow в n8n

### Требуется:

* Telegram-бот ([@BotFather](https://t.me/BotFather))
* Google Sheets (сервисный аккаунт + OAuth2)

### Шаги:

1. **Google Sheet для жалоб:**

![Google Sheets](workflow/03_excel.png)

2. **Telegram-бот:**

![Telegram Bot](workflow/04_tg.png)

3. **HTTP Request Node для запроса жалоб:**

![HTTP Request](workflow/05_get_open.png)

4. **Switch Node для ветвления по категории:**

![Switch Node](workflow/06_switch.png)

5. **Уведомление в Telegram:**

![Отправка в Telegram](workflow/07_tg_send.png)

6. **Запись в Google Sheets:**

![Запись в Google Sheets](workflow/08_sheets_send.png)

7. **Закрытие жалобы через API:**

![Закрытие жалобы](workflow/09_database_finally.png)

---

## 📦 Конфигурация для реальных API

Создай файл `.env.prod` в папке `app`:

```env
API_LAYER_KEY=...
API_OPENAI_KEY=...
COMPLAINT_API_KEY=api-prod
LAYER_ENDPOINT_URL=https://api.apilayer.com/sentiment/analysis
OPENAI_ENDPOINT_URL=https://api.openai.com/v1/chat/completions
```
