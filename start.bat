@echo off
chcp 65001 >nul
title LeadHunter Launcher
color 0b

echo ========================================================
echo   Запуск LeadHunter (FastAPI Backend + React Frontend)
echo ========================================================
echo.

:: Сброс глобальных переменных Python, которые могут вызывать ModuleNotFoundError
set "PYTHONHOME="
set "PYTHONPATH="

cd /d "%~dp0backend"

:: Проверка наличия и работоспособности venv
if not exist "venv\Scripts\python.exe" (
    echo [ОШИБКА] Виртуальное окружение не найдено!
    echo Пожалуйста, запустите install.bat для первоначальной установки.
    echo.
    pause
    exit /b 1
)

call venv\Scripts\python.exe -c "import encodings" >nul 2>&1
if errorlevel 1 (
    echo [ВНИМАНИЕ] Окружение venv не запускается на этом компьютере
    echo (такое происходит, если проект был скопирован с другого ПК).
    echo.
    echo Запускаем автоматическое восстановление окружения через install.bat...
    pause
    cd /d "%~dp0"
    call install.bat
    exit /b
)

cd /d "%~dp0"

echo [1/2] Запуск бэкенда (FastAPI на порту 8000)...
start "LeadHunter Backend (FastAPI)" cmd /k "chcp 65001 >nul && cd /d \"%~dp0backend\" && set \"PYTHONHOME=\" && set \"PYTHONPATH=\" && venv\Scripts\python.exe -m uvicorn main:app --reload --port 8000"

echo [2/2] Запуск интерфейса (React на порту 5173)...
start "LeadHunter Frontend (React)" cmd /k "chcp 65001 >nul && cd /d \"%~dp0frontend\" && npm run dev"

echo.
echo ========================================================
echo   Приложение успешно запущено!
echo   Бэкенд API:  http://127.0.0.1:8000
echo   Фронтенд UI: http://localhost:5173
echo ========================================================

timeout /t 3 /nobreak >nul
start http://localhost:5173
pause