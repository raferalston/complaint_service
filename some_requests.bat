@echo off
chcp 65001 >nul

curl -X POST "http://127.0.0.1:8000/complaints/" -H "Content-Type: application/json" -d "{\"text\": \"тест 1 !оплата\"}"
curl -X POST "http://127.0.0.1:8000/complaints/" -H "Content-Type: application/json" -d "{\"text\": \"тест 2 !техническая\"}"
curl -X POST "http://127.0.0.1:8000/complaints/" -H "Content-Type: application/json" -d "{\"text\": \"тест 3 !тест\"}"
curl -X POST "http://127.0.0.1:8000/complaints/" -H "Content-Type: application/json" -d "{\"text\": \"тест 4 !другое love\"}"
curl -X POST "http://127.0.0.1:8000/complaints/" -H "Content-Type: application/json" -d "{\"text\": \"тест 5 !другое bad\"}"
curl -X POST "http://127.0.0.1:8000/complaints/" -H "Content-Type: application/json" -d "{\"text\": \"тест 6 !другое ok\"}"

pause
