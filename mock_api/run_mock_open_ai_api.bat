@echo off
setlocal

REM Указываем путь к виртуальному окружению и модулю приложения
set VENV_PATH=..\env
set ACTIVATE_SCRIPT=%VENV_PATH%\Scripts\activate.bat
set APP_MODULE=mock_api\mock_open_ai_api:app

REM Проверяем наличие виртуального окружения
if not exist "%ACTIVATE_SCRIPT%" (
    echo No env found "%VENV_PATH%".
    echo create it with:
    echo python -m venv env
    pause
    exit /b
)

REM Активируем виртуальное окружение
call "%ACTIVATE_SCRIPT%"
echo "%ACTIVATE_SCRIPT%"

REM Проверяем наличие uvicorn
where uvicorn >nul 2>nul
IF ERRORLEVEL 1 (
    echo Uvicorn не найден. Устанавливаю зависимости...
    pip install fastapi uvicorn
)

REM Запуск сервера
echo Running mock Open AI...
uvicorn mock_open_ai_api:mock_app --host 127.0.0.1 --port 8002 --reload

endlocal
pause
