@echo off
echo 🚀 Starting LLM Data Copilot...
echo.
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo Press Ctrl+C to stop both servers
echo.

start "Backend" cmd /k "cd backend && venv\Scripts\activate && uvicorn app:app --reload --port 8000"
start "Frontend" cmd /k "cd frontend && yarn dev"
