@echo off
title LeadHunter - Установка компонентов
echo ========================================================
echo   LeadHunter: Автоматическая установка компонентов
echo ========================================================
echo.

echo [1/3] Проверка Python и Node.js...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ОШИБКА] Python не найден! Установите Python с python.org и поставьте галочку "Add Python to PATH".
    pause
    exit /b 1
)

node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ОШИБКА] Node.js не найден! Установите Node.js с nodejs.org.
    pause
    exit /b 1
)

echo [2/3] Настройка бэкенда (Python)...
cd backend
if not exist "venv" (
    python -m venv venv
)
call venv\Scripts\pip install -r requirements.txt
cd ..

echo.
echo [3/3] Настройка фронтенда (React)...
cd frontend
call npm install
cd ..

echo.
echo ========================================================
echo   Установка успешно завершена!
echo   Теперь вы можете запускать приложение через start.bat
echo ========================================================
pause