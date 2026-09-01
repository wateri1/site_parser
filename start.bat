@echo off
title LeadHunter App
echo ========================================================
echo   Starting LeadHunter (FastAPI Backend + React Frontend)
echo ========================================================

start "LeadHunter Backend (FastAPI)" cmd /k "cd backend && venv\Scripts\python.exe -m uvicorn main:app --reload --port 8000"
start "LeadHunter Frontend (React)" cmd /k "cd frontend && npm run dev"

echo.
echo Application launched!
echo Backend API: http://127.0.0.1:8000
echo Frontend UI: http://localhost:5173
echo ========================================================

timeout /t 3 /nobreak >nul
start http://localhost:5173
pause