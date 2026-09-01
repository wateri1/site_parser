Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "  Starting LeadHunter (FastAPI Backend + React Frontend)" -ForegroundColor Green
Write-Host "========================================================" -ForegroundColor Cyan

Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd backend; .\venv\Scripts\python.exe -m uvicorn main:app --reload --port 8000"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd frontend; npm run dev"

Write-Host "`nApplication launched successfully!" -ForegroundColor Green
Write-Host "Backend API:  http://127.0.0.1:8000" -ForegroundColor Yellow
Write-Host "Frontend UI:  http://localhost:5173" -ForegroundColor Yellow
Write-Host "========================================================" -ForegroundColor Cyan